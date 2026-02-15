from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict


APP_DIR_NAME = ".sentinel"
CONFIG_NAME = "config.json"


@dataclass
class SentinelConfig:
    language: str = "en"
    bruteforce_threshold: int = 5
    admin_hits_threshold: int = 3


def _config_dir() -> Path:
    home = Path.home()
    return home / APP_DIR_NAME


def config_path() -> Path:
    return _config_dir() / CONFIG_NAME


def ensure_config_dir() -> None:
    _config_dir().mkdir(parents=True, exist_ok=True)


def load_config() -> SentinelConfig:
    ensure_config_dir()
    path = config_path()
    if not path.exists():
        cfg = SentinelConfig()
        save_config(cfg)
        return cfg

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        cfg = SentinelConfig()
        save_config(cfg)
        return cfg

    return SentinelConfig(
        language=str(raw.get("language", "en")),
        bruteforce_threshold=int(raw.get("bruteforce_threshold", 5)),
        admin_hits_threshold=int(raw.get("admin_hits_threshold", 3)),
    )


def save_config(cfg: SentinelConfig) -> None:
    ensure_config_dir()
    path = config_path()
    path.write_text(json.dumps(asdict(cfg), indent=2, ensure_ascii=False), encoding="utf-8")


def update_config(patch: Dict[str, Any]) -> SentinelConfig:
    cfg = load_config()
    data = asdict(cfg)
    data.update(patch)
    new_cfg = SentinelConfig(
        language=str(data.get("language", "en")),
        bruteforce_threshold=int(data.get("bruteforce_threshold", 5)),
        admin_hits_threshold=int(data.get("admin_hits_threshold", 3)),
    )
    save_config(new_cfg)
    return new_cfg
