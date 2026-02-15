from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_config, update_config
from .languages import SUPPORTED_LANGS, t
from .report import format_report
from .scanner import scan_path


def _prompt_language(default_lang: str) -> str:
    langs = ",".join(SUPPORTED_LANGS)
    raw = input(t(default_lang, "choose_lang", langs=langs, d=default_lang)).strip().lower()
    if not raw:
        return default_lang
    if raw not in SUPPORTED_LANGS:
        return default_lang
    return raw


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sentinel", description="Sentinel mini SOC learning tool")
    p.add_argument("--path", required=True, help="Folder or file path to scan (e.g., sample_logs)")
    p.add_argument("--lang", default=None, help="Override language (en,tr,de,es,fr,it,ru)")
    p.add_argument("--set-lang", action="store_true", help="Prompt and save language")
    p.add_argument("--bf", type=int, default=None, help="Bruteforce threshold (default from config)")
    p.add_argument("--admin", type=int, default=None, help="Admin hits threshold (default from config)")
    return p


def main(argv=None) -> int:
    cfg = load_config()
    lang = cfg.language

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.set_lang:
        new_lang = _prompt_language(lang)
        cfg = update_config({"language": new_lang})
        lang = cfg.language
        print(t(lang, "saved_lang", selected=cfg.language))

    if args.lang:
        lang = args.lang.lower() if args.lang.lower() in SUPPORTED_LANGS else lang

    bruteforce_threshold = args.bf if args.bf is not None else cfg.bruteforce_threshold
    admin_hits_threshold = args.admin if args.admin is not None else cfg.admin_hits_threshold

    scan_target = Path(args.path).expanduser()

    if not scan_target.exists():
        print(t(lang, "err_path", p=str(scan_target)))
        return 2

    print(t(lang, "scanning"))
    result = scan_path(scan_target, bruteforce_threshold, admin_hits_threshold)

    print(t(lang, "found_files", n=len(result.files)))
    print("")
    print(format_report(lang, result.findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())