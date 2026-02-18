from __future__ import annotations

import os
import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from env_loader import load_env_file
from oauth_client import OAuthPKCEClient, OAuthSettings, load_token
from usage_service import codex_daily_summary, insert_codex_sample_session


def resolve_refresh_interval_ms() -> int:
    raw = os.getenv("AUIW_REFRESH_INTERVAL_SEC", "3600").strip()
    try:
        seconds = int(raw)
    except ValueError:
        seconds = 3600
    seconds = max(60, seconds)
    return seconds * 1000


class UsageDashboardApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("AI Usage Watcher - Codex Dashboard")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.compact_mode = self.screen_width <= 1024 or self.screen_height <= 768
        self.is_fullscreen = True
        self.refresh_interval_ms = resolve_refresh_interval_ms()
        self.refresh_job_id: str | None = None

        self.login_status_var = tk.StringVar(value="로그인 상태: 미로그인")
        self.total_tokens_var = tk.StringVar(value="총 토큰: 0")
        self.total_requests_var = tk.StringVar(value="총 요청: 0")
        self.total_sessions_var = tk.StringVar(value="총 세션: 0")
        self.last_refresh_var = tk.StringVar(value="최근 갱신: -")
        self.auto_refresh_var = tk.StringVar(
            value=f"자동 갱신: {self.refresh_interval_ms // 60000}분"
        )

        self._configure_window()
        self._configure_styles()
        self._build_layout()
        self._load_saved_auth_status()
        self.refresh_usage_table()
        self._schedule_next_refresh()

    def _configure_window(self) -> None:
        if self.compact_mode:
            self.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
            self.minsize(480, 320)
        else:
            self.geometry("1080x720")
            self.minsize(900, 580)

        self.attributes("-fullscreen", True)
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._exit_fullscreen)

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        if self.compact_mode:
            self.option_add("*Font", "Segoe UI 10")
            style.configure("Treeview", rowheight=32, font=("Segoe UI", 10))
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
            self.title_font = ("Segoe UI", 14, "bold")
            self.subtitle_font = ("Segoe UI", 9)
            self.container_padding = 8
            self.section_padding = 8
        else:
            self.option_add("*Font", "Segoe UI 11")
            style.configure("Treeview", rowheight=30, font=("Segoe UI", 11))
            style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
            self.title_font = ("Segoe UI", 18, "bold")
            self.subtitle_font = ("Segoe UI", 10)
            self.container_padding = 16
            self.section_padding = 12

    def _toggle_fullscreen(self, _: tk.Event | None = None) -> None:
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def _exit_fullscreen(self, _: tk.Event | None = None) -> None:
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)

    def _build_layout(self) -> None:
        root = ttk.Frame(self, padding=self.container_padding)
        root.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(
            root,
            text="Codex 사용량 대시보드 (Windows MVP)",
            font=self.title_font,
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            root,
            text="최초 로그인은 OAuth, 사용량 데이터는 로컬 SQLite 조회",
            font=self.subtitle_font,
        )
        subtitle.pack(anchor="w", pady=(4, 8))

        hint = ttk.Label(
            root, text="화면 팁: F11 전체화면 토글, Esc 전체화면 종료", font=self.subtitle_font
        )
        hint.pack(anchor="w", pady=(0, 10))

        auth_frame = ttk.LabelFrame(root, text="인증", padding=self.section_padding)
        auth_frame.pack(fill=tk.X)

        ttk.Label(auth_frame, textvariable=self.login_status_var).pack(
            side=tk.LEFT, anchor=tk.W
        )
        ttk.Button(
            auth_frame, text="OAuth 로그인", command=self.start_oauth_login
        ).pack(side=tk.RIGHT, padx=(8, 0))

        summary_frame = ttk.LabelFrame(root, text="요약", padding=self.section_padding)
        summary_frame.pack(fill=tk.X, pady=(10, 10))

        if self.compact_mode:
            ttk.Label(summary_frame, textvariable=self.total_sessions_var).pack(
                anchor=tk.W, pady=(0, 2)
            )
            ttk.Label(summary_frame, textvariable=self.total_requests_var).pack(
                anchor=tk.W, pady=(0, 2)
            )
            ttk.Label(summary_frame, textvariable=self.total_tokens_var).pack(anchor=tk.W)
        else:
            ttk.Label(summary_frame, textvariable=self.total_sessions_var).pack(
                side=tk.LEFT, padx=(0, 16)
            )
            ttk.Label(summary_frame, textvariable=self.total_requests_var).pack(
                side=tk.LEFT, padx=(0, 16)
            )
            ttk.Label(summary_frame, textvariable=self.total_tokens_var).pack(side=tk.LEFT)

        actions_frame = ttk.Frame(root)
        actions_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Button(actions_frame, text="새로고침", command=self.refresh_usage_table).pack(side=tk.LEFT)
        ttk.Button(
            actions_frame, text="Codex 샘플 1건 생성", command=self.insert_sample_and_refresh
        ).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Label(actions_frame, textvariable=self.auto_refresh_var).pack(
            side=tk.RIGHT, padx=(10, 0)
        )
        ttk.Label(actions_frame, textvariable=self.last_refresh_var).pack(
            side=tk.RIGHT, padx=(10, 0)
        )

        table_frame = ttk.LabelFrame(root, text="Codex 일별 사용량", padding=self.section_padding)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("day", "sessions", "requests", "tokens")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.table.heading("day", text="날짜")
        self.table.heading("sessions", text="세션 수")
        self.table.heading("requests", text="요청 수")
        self.table.heading("tokens", text="토큰(추정)")
        table_width = max(480, self.screen_width - 120)
        day_width = int(table_width * 0.36)
        metric_width = int((table_width - day_width) / 3)
        self.table.column("day", width=day_width, anchor=tk.W)
        self.table.column("sessions", width=metric_width, anchor=tk.CENTER)
        self.table.column("requests", width=metric_width, anchor=tk.CENTER)
        self.table.column("tokens", width=metric_width, anchor=tk.CENTER)
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _load_saved_auth_status(self) -> None:
        token = load_token()
        if not token:
            self.login_status_var.set("로그인 상태: 미로그인")
            return
        token_hint = token.get("token_type", "saved").upper()
        self.login_status_var.set(f"로그인 상태: OAuth 완료 ({token_hint})")

    def start_oauth_login(self) -> None:
        def worker() -> None:
            try:
                settings = OAuthSettings.from_env()
                client = OAuthPKCEClient(settings)
                token = client.authenticate(timeout_sec=180)
                token_hint = token.get("token_type", "saved").upper()
                self.after(
                    0,
                    lambda: self.login_status_var.set(
                        f"로그인 상태: OAuth 완료 ({token_hint})"
                    ),
                )
                self.after(
                    0, lambda: messagebox.showinfo("OAuth", "로그인이 완료되었습니다.")
                )
            except Exception as exc:  # noqa: BLE001
                self.after(
                    0,
                    lambda: messagebox.showerror(
                        "OAuth 오류",
                        (
                            "로그인에 실패했습니다.\n"
                            f"{exc}\n\n"
                            "desktop_win/.env.example를 참고해 OAuth 환경변수를 설정해 주세요."
                        ),
                    ),
                )

        threading.Thread(target=worker, daemon=True).start()

    def insert_sample_and_refresh(self) -> None:
        try:
            session_id = insert_codex_sample_session()
            self.refresh_usage_table()
            messagebox.showinfo("샘플 생성", f"Codex 샘플 세션 생성 완료: {session_id}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("샘플 생성 실패", str(exc))

    def refresh_usage_table(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)

        rows = codex_daily_summary()
        total_sessions = 0
        total_requests = 0
        total_tokens = 0

        for row in rows:
            total_sessions += row["sessions"]
            total_requests += row["requests"]
            total_tokens += row["tokens"]
            self.table.insert(
                "",
                tk.END,
                values=(
                    row["day"],
                    row["sessions"],
                    row["requests"],
                    row["tokens"],
                ),
            )

        self.total_sessions_var.set(f"총 세션: {total_sessions}")
        self.total_requests_var.set(f"총 요청: {total_requests}")
        self.total_tokens_var.set(f"총 토큰: {total_tokens}")
        self.last_refresh_var.set(
            f"최근 갱신: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def _schedule_next_refresh(self) -> None:
        self.refresh_job_id = self.after(self.refresh_interval_ms, self._run_periodic_refresh)

    def _run_periodic_refresh(self) -> None:
        self.refresh_usage_table()
        self._schedule_next_refresh()


def main() -> None:
    load_env_file()
    app = UsageDashboardApp()
    app.mainloop()


if __name__ == "__main__":
    main()
