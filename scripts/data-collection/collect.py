from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from collector_core import RunOptions, analyze_school, collect_school, load_collector, read_school_sources, write_cross_school_analysis, write_school_data


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[1]
WORKBOOK = ROOT / "data" / "data-collection" / "prof_info_page_links.xlsx"
SCHOOL_ALIASES = {"ntu-comm-engin-ds": "ntu-comm-engin-ds-network"}


def available_collectors() -> dict[str, Path]:
    return {path.parent.name: path for path in SCRIPT_DIR.glob("*/collector.py") if path.parent.name != "tests"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="蒐集各研究所中英文師資資料並產生品質分析")
    parser.add_argument("--school", default="all", help="系所 ID，或 all")
    parser.add_argument("--headed", action="store_true", help="顯示 Playwright 瀏覽器")
    parser.add_argument("--skip-analysis", action="store_true", help="不產生分析輸出")
    parser.add_argument("--dry-run", action="store_true", help="只驗證設定，不連線、不寫檔")
    parser.add_argument("--insecure", action="store_true", help="停用 TLS 憑證驗證")
    parser.add_argument("--timeout", type=float, default=30.0, help="每次請求逾時秒數")
    parser.add_argument("--delay", type=float, default=0.35, help="請求間隔秒數")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    collectors = available_collectors()
    sources = read_school_sources(WORKBOOK)
    requested_school = SCHOOL_ALIASES.get(args.school, args.school)
    selected = sorted(collectors) if requested_school == "all" else [requested_school]
    unknown = [school for school in selected if school not in collectors]
    if unknown:
        print(f"未知系所：{', '.join(unknown)}", file=sys.stderr)
        print(f"可用系所：{', '.join(sorted(collectors))}", file=sys.stderr)
        return 2
    missing_source = [school for school in selected if school not in sources]
    if missing_source:
        print(f"連結表缺少：{', '.join(missing_source)}", file=sys.stderr)
        return 2
    if args.dry_run:
        print(json.dumps({school: sources[school] for school in selected}, ensure_ascii=False, indent=2))
        return 0

    options = RunOptions(ROOT, args.headed, args.skip_analysis, args.insecure, args.timeout, args.delay)
    reports = []
    failed = False
    for index, school in enumerate(selected, 1):
        print(f"[{index}/{len(selected)}] {school}", flush=True)
        module = load_collector(collectors[school])
        try:
            result = module.collect(sources[school], options) if hasattr(module, "collect") else collect_school(module.CONFIG, sources[school], options)
            write_school_data(result, module.CONFIG, ROOT, sources[school])
            if not args.skip_analysis:
                reports.append(analyze_school(result, ROOT))
            if result.errors:
                failed = True
                print(f"  完成但有 {len(result.errors)} 個錯誤；教師 {len(result.faculty)} 人", file=sys.stderr)
            else:
                print(f"  教師 {len(result.faculty)} 人；中文 {len(result.zh_records)}、英文 {len(result.en_records)}")
        except Exception as exc:
            failed = True
            print(f"  執行失敗：{exc}", file=sys.stderr)
    if reports and not args.skip_analysis:
        if args.school != "all":
            existing = []
            analysis_root = ROOT / "analysis" / "data-collection"
            for path in analysis_root.glob("*/quality-report.json"):
                try:
                    existing.append(json.loads(path.read_text(encoding="utf-8")))
                except (OSError, json.JSONDecodeError):
                    pass
            reports = existing
        write_cross_school_analysis(reports, ROOT)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
