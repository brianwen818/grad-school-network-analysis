from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from collector_core import HttpClient, RunOptions, extract_records_from_html, load_collector, read_school_sources  # noqa: E402


@unittest.skipUnless(os.environ.get("FACULTY_LIVE_TESTS") == "1", "設定 FACULTY_LIVE_TESTS=1 才執行官網測試")
class LiveSmokeTests(unittest.TestCase):
    def test_static_seed_pages_respond_and_are_not_template_only(self):
        root = SCRIPT_DIR.parents[1]
        sources = read_school_sources(root / "data/data-collection/prof_info_page_links.xlsx")
        client = HttpClient(RunOptions(root, timeout=30, delay=0))
        for path in sorted(SCRIPT_DIR.glob("*/collector.py")):
            module = load_collector(path)
            if module.CONFIG.dynamic:
                continue
            url = sources[module.CONFIG.school_id]["url_ch"]
            html = client.get(url)
            self.assertGreater(len(html), 1000, module.CONFIG.school_id)
            rows = extract_records_from_html(html, url, "zh", module.CONFIG)
            self.assertGreater(len(rows), 0, module.CONFIG.school_id)


if __name__ == "__main__":
    unittest.main()
