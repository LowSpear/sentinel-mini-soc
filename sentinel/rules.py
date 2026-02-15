from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


IP_RE = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")


@dataclass
class Finding:
    rule_id: str
    title_key: str
    threshold: int
    ip_counts: Dict[str, int]


def _extract_ip(line: str) -> Optional[str]:
    m = IP_RE.search(line)
    return m.group(0) if m else None


def detect_bruteforce(lines: Iterable[str], threshold: int) -> Optional[Finding]:
    counts: Dict[str, int] = {}
    for line in lines:
        up = line.upper()
        if "FAILED LOGIN" in up or "LOGIN FAILED" in up or "AUTH FAILED" in up:
            ip = _extract_ip(line)
            if not ip:
                continue
            counts[ip] = counts.get(ip, 0) + 1

    hits = {ip: c for ip, c in counts.items() if c >= threshold}
    if not hits:
        return None
    return Finding(
        rule_id="BRUTEFORCE",
        title_key="rule_bruteforce",
        threshold=threshold,
        ip_counts=hits,
    )


def detect_admin_hits(lines: Iterable[str], threshold: int) -> Optional[Finding]:
    counts: Dict[str, int] = {}
    admin_keywords = ("/admin", "/wp-admin", "/administrator", "/login", "/wp-login")

    for line in lines:
        low = line.lower()
        if any(k in low for k in admin_keywords):
            ip = _extract_ip(line)
            if not ip:
                continue
            counts[ip] = counts.get(ip, 0) + 1

    hits = {ip: c for ip, c in counts.items() if c >= threshold}
    if not hits:
        return None
    return Finding(
        rule_id="ADMIN_HITS",
        title_key="rule_admin_hits",
        threshold=threshold,
        ip_counts=hits,
    )


def run_all(lines: List[str], bruteforce_threshold: int, admin_hits_threshold: int) -> List[Finding]:
    findings: List[Finding] = []

    f1 = detect_bruteforce(lines, bruteforce_threshold)
    if f1:
        findings.append(f1)

    f2 = detect_admin_hits(lines, admin_hits_threshold)
    if f2:
        findings.append(f2)

    return findings
