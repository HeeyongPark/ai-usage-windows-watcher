from __future__ import annotations

import os
import queue
import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from budget_rules import evaluate_budget_alert, load_budget_rule_settings
from codex_auth import codex_login_device_auth, codex_login_status
from env_loader import load_env_file
from usage_service import (
    codex_daily_summary,
    codex_weekly_summary,
    insert_codex_sample_session,
)


def resolve_refresh_interval_ms() -> int:
    raw = os.getenv("AUIW_REFRESH_INTERVAL_SEC", "3600").strip()
    try:
        seconds = int(raw)
    except ValueError:
        seconds = 3600
    seconds = max(60, seconds)
    return seconds * 1000


def resolve_codex_login_timeout_sec() -> int:
    raw = os.getenv("AUIW_CODEX_LOGIN_TIMEOUT_SEC", "300").strip()
    try:
        seconds = int(raw)
    except ValueError:
        seconds = 300
    return max(60, seconds)


def _font_option_value(size: int) -> str:
    return f"{{Segoe UI}} {size}"


class UsageDashboardApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("AI Usage Watcher - Codex Dashboard")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.compact_mode = self.screen_width <= 1024 or self.screen_height <= 768
        self.is_fullscreen = True
        self.refresh_interval_ms = resolve_refresh_interval_ms()
        self.codex_login_timeout_sec = resolve_codex_login_timeout_sec()
        self.refresh_job_id: str | None = None
        self.codex_login_in_progress = False
        self.codex_result_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self.budget_settings = load_budget_rule_settings()

        self.login_status_var = tk.StringVar(value="로그인 상태: Codex 미로그인")
        self.total_tokens_var = tk.StringVar(value="총 토큰: 0")
        self.total_requests_var = tk.StringVar(value="총 요청: 0")
        self.total_sessions_var = tk.StringVar(value="총 세션: 0")
        self.last_refresh_var = tk.StringVar(value="최근 갱신: -")
        self.auto_refresh_var = tk.StringVar(
            value=f"자동 갱신: {self.refresh_interval_ms // 60000}분"
        )
        self.budget_status_var = tk.StringVar(value="예산 상태: 계산 중")
        self.budget_detail_var = tk.StringVar(value="일/주 사용량 집계 중")

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
            self.option_add("*Font", _font_option_value(10))
            style.configure("Treeview", rowheight=32, font=("Segoe UI", 10))
            style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
            self.title_font = ("Segoe UI", 14, "bold")
            self.subtitle_font = ("Segoe UI", 9)
            self.container_padding = 8
            self.section_padding = 8
        else:
            self.option_add("*Font", _font_option_value(11))
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
            text="Codex 로그인(ChatGPT OAuth)은 Codex CLI를 통해 수행, 사용량 데이터는 로컬 SQLite 조회",
            font=self.subtitle_font,
        )
        subtitle.pack(anchor="w", pady=(4, 8))

        hint = ttk.Label(
            root, text="화면 팁: F11 전체화면 토글, Esc 전체화면 종료", font=self.subtitle_font
        )
        hint.pack(anchor="w", pady=(0, 10))

        auth_frame = ttk.LabelFrame(root, text="Codex 인증", padding=self.section_padding)
        auth_frame.pack(fill=tk.X)

        ttk.Label(auth_frame, textvariable=self.login_status_var).pack(
            side=tk.LEFT, anchor=tk.W
        )
        self.codex_login_button = ttk.Button(
            auth_frame, text="Codex 로그인", command=self.start_codex_login
        )
        self.codex_login_button.pack(side=tk.RIGHT, padx=(8, 0))

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

        alert_frame = ttk.LabelFrame(root, text="예산 알림 규칙", padding=self.section_padding)
        alert_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(alert_frame, textvariable=self.budget_status_var).pack(anchor=tk.W)
        ttk.Label(alert_frame, textvariable=self.budget_detail_var).pack(anchor=tk.W, pady=(2, 0))

        table_frame = ttk.LabelFrame(root, text="Codex 사용량 (일/주)", padding=self.section_padding)
        table_frame.pack(fill=tk.BOTH, expand=True)
        table_width = max(480, self.screen_width - 120)
        metric_width = int(table_width * 0.2)

        notebook = ttk.Notebook(table_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        daily_tab = ttk.Frame(notebook)
        weekly_tab = ttk.Frame(notebook)
        notebook.add(daily_tab, text="일별")
        notebook.add(weekly_tab, text="주별")

        daily_columns = ("day", "sessions", "requests", "tokens")
        self.daily_table = ttk.Treeview(daily_tab, columns=daily_columns, show="headings")
        self.daily_table.heading("day", text="날짜")
        self.daily_table.heading("sessions", text="세션 수")
        self.daily_table.heading("requests", text="요청 수")
        self.daily_table.heading("tokens", text="토큰(추정)")
        self.daily_table.column("day", width=int(table_width * 0.4), anchor=tk.W)
        self.daily_table.column("sessions", width=metric_width, anchor=tk.CENTER)
        self.daily_table.column("requests", width=metric_width, anchor=tk.CENTER)
        self.daily_table.column("tokens", width=metric_width, anchor=tk.CENTER)
        self.daily_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        daily_scrollbar = ttk.Scrollbar(daily_tab, orient=tk.VERTICAL, command=self.daily_table.yview)
        self.daily_table.configure(yscrollcommand=daily_scrollbar.set)
        daily_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        weekly_columns = ("week", "sessions", "requests", "tokens")
        self.weekly_table = ttk.Treeview(weekly_tab, columns=weekly_columns, show="headings")
        self.weekly_table.heading("week", text="주차")
        self.weekly_table.heading("sessions", text="세션 수")
        self.weekly_table.heading("requests", text="요청 수")
        self.weekly_table.heading("tokens", text="토큰(추정)")
        self.weekly_table.column("week", width=int(table_width * 0.4), anchor=tk.W)
        self.weekly_table.column("sessions", width=metric_width, anchor=tk.CENTER)
        self.weekly_table.column("requests", width=metric_width, anchor=tk.CENTER)
        self.weekly_table.column("tokens", width=metric_width, anchor=tk.CENTER)
        self.weekly_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        weekly_scrollbar = ttk.Scrollbar(
            weekly_tab, orient=tk.VERTICAL, command=self.weekly_table.yview
        )
        self.weekly_table.configure(yscrollcommand=weekly_scrollbar.set)
        weekly_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _load_saved_auth_status(self) -> None:
        status = codex_login_status(timeout_sec=5)
        if not status.logged_in:
            self.login_status_var.set("로그인 상태: Codex 미로그인")
            return
        self.login_status_var.set(f"로그인 상태: Codex 로그인 완료 ({status.detail})")

    def _set_codex_login_ui_state(self, in_progress: bool) -> None:
        self.codex_login_in_progress = in_progress
        if in_progress:
            self.codex_login_button.state(["disabled"])
            self.login_status_var.set("로그인 상태: Codex 로그인 진행 중 (브라우저 확인)")
            return
        self.codex_login_button.state(["!disabled"])

    def _poll_codex_login_result(self) -> None:
        try:
            result_type, result_value = self.codex_result_queue.get_nowait()
        except queue.Empty:
            self.after(200, self._poll_codex_login_result)
            return

        self._set_codex_login_ui_state(False)
        if result_type == "success":
            self.login_status_var.set(f"로그인 상태: Codex 로그인 완료 ({result_value})")
            messagebox.showinfo("Codex 로그인", "Codex 로그인이 완료되었습니다.")
            return

        self.login_status_var.set("로그인 상태: Codex 미로그인")
        messagebox.showerror(
            "Codex 로그인 오류",
            (
                "로그인에 실패했습니다.\n"
                f"{result_value}\n\n"
                "터미널에서 `codex login --device-auth`가 동작하는지 먼저 확인해 주세요."
            ),
        )

    def start_codex_login(self) -> None:
        if self.codex_login_in_progress:
            return

        self._set_codex_login_ui_state(True)

        def worker() -> None:
            try:
                status = codex_login_status(timeout_sec=8)
                if status.logged_in:
                    self.codex_result_queue.put(("success", status.detail))
                    return

                login_status = codex_login_device_auth(
                    timeout_sec=self.codex_login_timeout_sec
                )
                if login_status.logged_in:
                    self.codex_result_queue.put(("success", login_status.detail))
                    return

                self.codex_result_queue.put(("error", login_status.detail))
            except Exception as exc:  # noqa: BLE001
                self.codex_result_queue.put(("error", str(exc)))

        threading.Thread(target=worker, daemon=True).start()
        self.after(200, self._poll_codex_login_result)

    def insert_sample_and_refresh(self) -> None:
        try:
            session_id = insert_codex_sample_session()
            self.refresh_usage_table()
            messagebox.showinfo("샘플 생성", f"Codex 샘플 세션 생성 완료: {session_id}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("샘플 생성 실패", str(exc))

    def refresh_usage_table(self) -> None:
        for item in self.daily_table.get_children():
            self.daily_table.delete(item)
        for item in self.weekly_table.get_children():
            self.weekly_table.delete(item)

        daily_rows = codex_daily_summary()
        weekly_rows = codex_weekly_summary()
        total_sessions = 0
        total_requests = 0
        total_tokens = 0

        for row in daily_rows:
            total_sessions += row["sessions"]
            total_requests += row["requests"]
            total_tokens += row["tokens"]
            self.daily_table.insert(
                "",
                tk.END,
                values=(
                    row["day"],
                    row["sessions"],
                    row["requests"],
                    row["tokens"],
                ),
            )

        for row in weekly_rows:
            self.weekly_table.insert(
                "",
                tk.END,
                values=(
                    row["week"],
                    row["sessions"],
                    row["requests"],
                    row["tokens"],
                ),
            )

        self.total_sessions_var.set(f"총 세션: {total_sessions}")
        self.total_requests_var.set(f"총 요청: {total_requests}")
        self.total_tokens_var.set(f"총 토큰: {total_tokens}")

        daily_tokens = daily_rows[0]["tokens"] if daily_rows else 0
        weekly_tokens = weekly_rows[0]["tokens"] if weekly_rows else 0
        budget_alert = evaluate_budget_alert(
            daily_tokens=daily_tokens,
            weekly_tokens=weekly_tokens,
            settings=self.budget_settings,
        )
        self.budget_status_var.set(f"예산 상태: {budget_alert.message}")
        self.budget_detail_var.set(
            (
                f"당일 {budget_alert.daily_tokens}/{self.budget_settings.daily_token_budget} tokens, "
                f"주간 {budget_alert.weekly_tokens}/{self.budget_settings.weekly_token_budget} tokens"
            )
        )

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
