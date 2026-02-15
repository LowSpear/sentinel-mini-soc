```python
__version__ = "0.1.0"

sentinel/config.py

import json
from pathlib import Path

DEFAULT_CONFIG = {"lang": "en"}

def config_path() -> Path:
    # config.json in project root (same folder where you run)
    return Path("config.json")

def load_config() -> dict:
    path = config_path()
    if not path.exists():
        return DEFAULT_CONFIG.copy()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(cfg: dict) -> None:
    path = config_path()
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")