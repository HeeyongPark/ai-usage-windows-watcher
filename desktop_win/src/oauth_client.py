from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import threading
import urllib.parse
import urllib.request
import webbrowser
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

from paths import oauth_token_path


@dataclass(frozen=True)
class OAuthSettings:
    auth_url: str
    token_url: str
    client_id: str
    scope: str
    redirect_host: str
    redirect_port: int

    @property
    def redirect_uri(self) -> str:
        return f"http://{self.redirect_host}:{self.redirect_port}/callback"

    @classmethod
    def from_env(cls) -> "OAuthSettings":
        auth_url = os.getenv("AUIW_OAUTH_AUTH_URL", "").strip()
        token_url = os.getenv("AUIW_OAUTH_TOKEN_URL", "").strip()
        client_id = os.getenv("AUIW_OAUTH_CLIENT_ID", "").strip()
        scope = os.getenv("AUIW_OAUTH_SCOPE", "openid profile email offline_access")
        redirect_host = os.getenv("AUIW_OAUTH_REDIRECT_HOST", "127.0.0.1")
        redirect_port = int(os.getenv("AUIW_OAUTH_REDIRECT_PORT", "8765"))

        missing = []
        if not auth_url:
            missing.append("AUIW_OAUTH_AUTH_URL")
        if not token_url:
            missing.append("AUIW_OAUTH_TOKEN_URL")
        if not client_id:
            missing.append("AUIW_OAUTH_CLIENT_ID")

        if missing:
            missing_text = ", ".join(missing)
            raise ValueError(f"OAuth env not configured: {missing_text}")

        return cls(
            auth_url=auth_url,
            token_url=token_url,
            client_id=client_id,
            scope=scope,
            redirect_host=redirect_host,
            redirect_port=redirect_port,
        )


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    server_version = "AUIWOAuth/1.0"
    code: str | None = None
    state: str | None = None
    error: str | None = None
    done_event: threading.Event | None = None

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        query = urllib.parse.parse_qs(parsed.query)
        self.__class__.code = query.get("code", [None])[0]
        self.__class__.state = query.get("state", [None])[0]
        self.__class__.error = query.get("error", [None])[0]
        if self.__class__.done_event:
            self.__class__.done_event.set()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><h3>Login completed. You can close this window.</h3></body></html>"
        )

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        return


def _base64url(input_bytes: bytes) -> str:
    return base64.urlsafe_b64encode(input_bytes).decode("utf-8").rstrip("=")


def _pkce_pair() -> tuple[str, str]:
    verifier = _base64url(secrets.token_bytes(32))
    challenge = _base64url(hashlib.sha256(verifier.encode("utf-8")).digest())
    return verifier, challenge


def _exchange_token(settings: OAuthSettings, code: str, code_verifier: str) -> dict[str, Any]:
    payload = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "client_id": settings.client_id,
            "code": code,
            "code_verifier": code_verifier,
            "redirect_uri": settings.redirect_uri,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        settings.token_url,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310
        return json.loads(response.read().decode("utf-8"))


def _open_auth_page(auth_request_url: str) -> None:
    opened = webbrowser.open(auth_request_url)
    if not opened:
        raise RuntimeError(
            "브라우저를 자동으로 열지 못했습니다. 아래 URL을 직접 열어 로그인해 주세요.\n"
            f"{auth_request_url}"
        )


def save_token(token_payload: dict[str, Any]) -> Path:
    token_path = oauth_token_path()
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(
        json.dumps(token_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return token_path


def load_token() -> dict[str, Any] | None:
    token_path = oauth_token_path()
    if not token_path.exists():
        return None
    return json.loads(token_path.read_text(encoding="utf-8"))


class OAuthPKCEClient:
    def __init__(self, settings: OAuthSettings) -> None:
        self.settings = settings

    def authenticate(self, timeout_sec: int = 180) -> dict[str, Any]:
        state = secrets.token_urlsafe(16)
        code_verifier, code_challenge = _pkce_pair()

        OAuthCallbackHandler.code = None
        OAuthCallbackHandler.state = None
        OAuthCallbackHandler.error = None
        OAuthCallbackHandler.done_event = threading.Event()

        server = HTTPServer(
            (self.settings.redirect_host, self.settings.redirect_port),
            OAuthCallbackHandler,
        )
        server.timeout = timeout_sec
        server_thread = threading.Thread(target=server.handle_request, daemon=True)
        server_thread.start()

        query = urllib.parse.urlencode(
            {
                "response_type": "code",
                "client_id": self.settings.client_id,
                "redirect_uri": self.settings.redirect_uri,
                "scope": self.settings.scope,
                "state": state,
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
            }
        )
        auth_request_url = f"{self.settings.auth_url}?{query}"
        try:
            _open_auth_page(auth_request_url)
        except Exception:
            server.server_close()
            raise

        event = OAuthCallbackHandler.done_event
        if not event or not event.wait(timeout=timeout_sec):
            server.server_close()
            raise TimeoutError("OAuth login timed out.")

        server.server_close()

        if OAuthCallbackHandler.error:
            raise RuntimeError(f"OAuth error: {OAuthCallbackHandler.error}")
        if OAuthCallbackHandler.state != state:
            raise RuntimeError("OAuth state mismatch.")
        if not OAuthCallbackHandler.code:
            raise RuntimeError("OAuth callback did not return authorization code.")

        token_payload = _exchange_token(
            self.settings,
            code=OAuthCallbackHandler.code,
            code_verifier=code_verifier,
        )
        save_token(token_payload)
        return token_payload
