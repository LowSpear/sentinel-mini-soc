from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from .rules import Finding, run_all


@dataclass
class ScanResult:
    files: List[Path]
    findings: List[Finding]


def _read_text_safely(path: Path) -> List[str]:
    try:
        return path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return []


def discover_log_files(root: Path) -> List[Path]:
    root = root.expanduser().resolve()
    if root.is_file():
        return [root]

    if not root.exists():
        return []

    exts = {".log", ".txt"}
    files: List[Path] = []
    for p in root.rglob("*"):
        if p.is_file() and (p.suffix.lower() in exts):
            files.append(p)
    return sorted(files)


def scan_path(path: Path, bruteforce_threshold: int, admin_hits_threshold: int) -> ScanResult:
    files = discover_log_files(path)
    all_lines: List[str] = []

    for f in files:
        all_lines.extend(_read_text_safely(f))

    findings = run_all(all_lines, bruteforce_threshold, admin_hits_threshold)
    return ScanResult(files=files, findings=findings)


def scan(path_str: str, bruteforce_threshold: int, admin_hits_threshold: int) -> Tuple[int, ScanResult]:
    path = Path(path_str)
    result = scan_path(path, bruteforce_threshold, admin_hits_threshold)
    return len(result.files), result
