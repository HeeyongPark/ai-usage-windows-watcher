from __future__ import annotations

import builtins
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_storage_falls_back_to_sqlite_extension_when_stdlib_missing(monkeypatch) -> None:
    storage_path = ROOT / "storage.py"
    spec = importlib.util.spec_from_file_location("storage_fallback_module", storage_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)

    real_import = builtins.__import__

    def blocked_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "sqlite3":
            raise ModuleNotFoundError("No module named 'sqlite3'")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    spec.loader.exec_module(module)

    assert hasattr(module.sqlite3, "connect")
