from __future__ import annotations

import os
from pathlib import Path


def app_data_dir() -> Path:
    appdata = os.getenv("APPDATA")
    if appdata:
        return Path(appdata) / "AIUsageWatcher"
    return Path.home() / ".ai-usage-watcher"


def oauth_token_path() -> Path:
    return app_data_dir() / "oauth_token.json"

