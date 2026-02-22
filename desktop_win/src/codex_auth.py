from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class CodexLoginStatus:
    logged_in: bool
    detail: str


def _codex_command() -> str:
    path = shutil.which("codex")
    if not path:
        raise FileNotFoundError("`codex` CLI를 찾지 못했습니다.")
    return path


def _run_codex(args: list[str], timeout_sec: int) -> subprocess.CompletedProcess[str]:
    command = [_codex_command(), *args]
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )


def _combined_output(process: subprocess.CompletedProcess[str]) -> str:
    return "\n".join([process.stdout.strip(), process.stderr.strip()]).strip()


def codex_login_status(timeout_sec: int = 8) -> CodexLoginStatus:
    try:
        process = _run_codex(["login", "status"], timeout_sec=timeout_sec)
    except FileNotFoundError as exc:
        return CodexLoginStatus(logged_in=False, detail=str(exc))
    except subprocess.TimeoutExpired:
        return CodexLoginStatus(logged_in=False, detail="Codex 로그인 상태 확인이 시간 초과되었습니다.")

    output = _combined_output(process)
    if "Logged in using" in output:
        provider = output.split("Logged in using", 1)[1].strip() or "ChatGPT"
        return CodexLoginStatus(logged_in=True, detail=provider)

    if "Not logged in" in output:
        return CodexLoginStatus(logged_in=False, detail="Codex 미로그인")

    if process.returncode == 0:
        return CodexLoginStatus(logged_in=False, detail=output or "Codex 로그인 상태를 확인할 수 없습니다.")

    return CodexLoginStatus(
        logged_in=False,
        detail=output or f"Codex 상태 확인 실패(returncode={process.returncode})",
    )


def codex_login_device_auth(timeout_sec: int = 300) -> CodexLoginStatus:
    try:
        process = _run_codex(["login", "--device-auth"], timeout_sec=timeout_sec)
    except FileNotFoundError as exc:
        return CodexLoginStatus(logged_in=False, detail=str(exc))
    except subprocess.TimeoutExpired:
        return CodexLoginStatus(
            logged_in=False,
            detail=(
                "Codex device-auth 로그인이 시간 초과되었습니다. "
                "브라우저에서 인증 완료 후 다시 시도해 주세요."
            ),
        )

    status = codex_login_status(timeout_sec=8)
    if status.logged_in:
        return status

    output = _combined_output(process)
    if output:
        return CodexLoginStatus(logged_in=False, detail=output)
    return CodexLoginStatus(
        logged_in=False,
        detail="Codex 로그인에 실패했습니다. 터미널에서 `codex login --device-auth`를 먼저 시도해 주세요.",
    )
