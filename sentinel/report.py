from __future__ import annotations

from typing import List

from .languages import t
from .rules import Finding


def _fmt_ip_counts(ip_counts: dict) -> str:
    return str(ip_counts)


def format_report(lang: str, findings: List[Finding]) -> str:
    out = []
    out.append(t(lang, "report"))
    out.append(t(lang, "findings", n=len(findings)))
    out.append("")

    if not findings:
        out.append(t(lang, "no_findings"))
        return "\n".join(out)

    for i, f in enumerate(findings, start=1):
        out.append(f"{i}) {t(lang, f.title_key)}")
        out.append(f"   - {t(lang, 'threshold', n=f.threshold)}")
        out.append(f"   - {t(lang, 'ip_counts', m=_fmt_ip_counts(f.ip_counts))}")
        out.append("")

    return "\n".join(out).rstrip()
