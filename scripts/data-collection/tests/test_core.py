from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from collector_core import (  # noqa: E402
    SchoolConfig,
    SchoolResult,
    SourceRecord,
    analyze_school,
    classify_roles,
    clean_text,
    discover_links,
    extract_records_from_html,
    is_pure_admin,
    load_collector,
    merge_languages,
    normalized_name,
    pair_records_by_role_order,
    read_school_sources,
    validate_faculty,
    write_cross_school_analysis,
    write_school_data,
)


class NormalizationTests(unittest.TestCase):
    def test_name_normalization(self):
        self.assertEqual(normalized_name("Chih-Hung Lin"), "chihhunglin")
        self.assertEqual(normalized_name(" 王 小明 "), "王小明")

    def test_clean_text_removes_invisible_formatting_marks(self):
        self.assertEqual(clean_text("金融科技\u200b\u200d\ufeff"), "金融科技")

    def test_role_classification_and_admin_filter(self):
        self.assertEqual(classify_roles("系主任／教授"), ["faculty"])
        self.assertIn("adjunct", classify_roles("兼任教授"))
        self.assertTrue(is_pure_admin("行政人員／秘書"))
        self.assertFalse(is_pure_admin("系主任／教授"))


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.config = SchoolConfig("sample", ("example.edu.tw",), card_selectors=(".faculty-card",))

    def test_extract_bilingual_card_and_exclude_staff(self):
        html = """
        <main><h2>專任教授</h2>
          <div class="faculty-card">
            <h3 class="member-name">王小明 <small>Ming Wang</small></h3>
            <div class="member-title">系主任／教授</div>
            <div class="member-degree">Example University Ph.D.</div>
            <div class="member-research">Machine Learning, Networks</div>
            <a href="mailto:ming@example.edu.tw">mail</a>
            <a href="/faculty/ming">profile</a>
          </div>
          <h2>行政人員</h2>
          <div class="faculty-card"><h3 class="member-name">陳秘書</h3><div class="member-title">秘書</div></div>
        </main>"""
        rows = extract_records_from_html(html, "https://example.edu.tw/faculty", "zh", self.config)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].name_zh, "王小明")
        self.assertEqual(rows[0].name_en, "Ming Wang")
        self.assertEqual(rows[0].education, ["Example University Ph.D."])
        self.assertEqual(rows[0].research_interests, ["Machine Learning, Networks"])

    def test_template_only_page_has_no_records(self):
        html = '<main><div class="faculty-card"><h3>{{faculty.name}}</h3></div></main>'
        self.assertEqual(extract_records_from_html(html, "https://example.edu.tw/faculty", "zh", self.config), [])

    def test_degrees_navigation_is_not_a_value_and_degree_table_is_parsed(self):
        html = """
        <main><h1 class="member-name">Jane Chen</h1>
          <ul><li><a>Degrees</a></li><li><a>Experience</a></li></ul>
          <table>
            <tr><th>Country</th><th>School Name</th><th>Department</th><th>Degree</th><th>Duration</th></tr>
            <tr><td>USA</td><td>Example University</td><td>Finance</td><td>Ph.D.</td><td>2000-2005</td></tr>
          </table>
        </main>"""
        rows = extract_records_from_html(html, "https://example.edu.tw/faculty/jane", "en", self.config, detail=True)
        self.assertEqual(rows[0].education, ["USA | Example University | Finance | Ph.D. | 2000-2005"])
        self.assertNotIn("s", rows[0].education)

    def test_title_sibling_sections_support_bilingual_label(self):
        html = """
        <main><h1 class="member-name">王小明</h1>
          <div class="title">學歷(Education)</div><div class="txt">國立臺灣大學 統計學博士</div>
          <div class="title">研究專長(Research Expertise)</div><div class="txt">高維度統計</div>
        </main>"""
        rows = extract_records_from_html(html, "https://example.edu.tw/member/1", "zh", self.config, detail=True)
        self.assertEqual(rows[0].education, ["國立臺灣大學 統計學博士"])
        self.assertEqual(rows[0].research_interests, ["高維度統計"])
        self.assertEqual(rows[0].titles, [])

    def test_inline_table_cell_label_and_value_are_parsed(self):
        html = """
        <main><h1 class="member-name">Jane Chen</h1><table><tr>
          <td><strong>Research focus :</strong> Algorithms, CAD</td>
        </tr></table></main>"""
        rows = extract_records_from_html(html, "https://example.edu.tw/member/1", "en", self.config, detail=True)
        self.assertEqual(rows[0].research_interests, ["Algorithms, CAD"])

    def test_adjacent_span_labels_and_nycu_profile_link_are_parsed(self):
        config = SchoolConfig(
            "nycu-info-mag-fin", ("imf.nycu.edu.tw",), card_selectors=(".ed_txt",),
            name_selectors=("strong",), profile_patterns=(r"/app/artwebsite/view",),
        )
        html = """
        <main><h2>專任師資</h2><div class="ed_txt">
          <a href="/imf/ch/app/artwebsite/view?module=artwebsite&amp;id=20414&amp;serno=person"><strong>林智勇</strong></a><br>
          <span><span>職稱：</span></span><span>教授兼系主任</span><br>
          <span><span>學歷：</span></span><span>國立臺灣大學財務金融博士</span><br>
          <span><span>專長：</span></span><span>公司理財、行為財務、金融科技</span>
        </div></main>"""
        listing_url = "https://imf.nycu.edu.tw/imf/ch/app/artwebsite/view?id=21165"
        rows = extract_records_from_html(html, listing_url, "zh", config)
        self.assertEqual(rows[0].titles, ["教授兼系主任", "專任師資"])
        self.assertEqual(rows[0].education, ["國立臺灣大學財務金融博士"])
        self.assertEqual(rows[0].research_interests, ["公司理財、行為財務、金融科技"])
        profiles, _categories, _pdfs = discover_links(html, listing_url, config)
        self.assertEqual(profiles, ["https://imf.nycu.edu.tw/imf/ch/app/artwebsite/view?module=artwebsite&id=20414&serno=person"])

    def test_nycu_malformed_wrapper_and_strong_label_text_are_parsed(self):
        config = SchoolConfig(
            "nycu-info-mag-fin", ("imf.nycu.edu.tw",), card_selectors=(".ed_txt",),
            name_selectors=("strong",),
        )
        zh_html = """
        <main><div class="ed_txt"><strong>黃思皓</strong><br>
          <span><span>職稱：</span>教授<br>
          <span>學歷：</span>國立清華大學資訊工程博士<br>
          <span>專長：</span>人工智慧精準行銷與推薦系統、金融科技<br>
          <span>電子郵件：</span>faculty@example.edu.tw</span>
        </div></main>"""
        zh_rows = extract_records_from_html(zh_html, "https://imf.nycu.edu.tw/imf/ch/faculty", "zh", config)
        self.assertEqual(zh_rows[0].titles, ["教授"])
        self.assertEqual(zh_rows[0].education, ["國立清華大學資訊工程博士"])
        self.assertEqual(zh_rows[0].research_interests, ["人工智慧精準行銷與推薦系統、金融科技"])

        en_html = """
        <main><div class="ed_txt"><strong>Name</strong>: Tian-Shyr Dai<br>
          <strong>Title</strong>: Professor<br>
          <strong>Education</strong>: PhD, National Taiwan University<br>
          <strong>Research expertise</strong>: Derivative Pricing, Credit Risk<br>
        </div></main>"""
        en_rows = extract_records_from_html(en_html, "https://imf.nycu.edu.tw/imf/en/faculty", "en", config)
        self.assertEqual(en_rows[0].name_en, "Tian-Shyr Dai")
        self.assertEqual(en_rows[0].titles, ["Professor"])
        self.assertEqual(en_rows[0].research_interests, ["Derivative Pricing, Credit Risk"])

    def test_department_heading_is_not_a_person(self):
        config = SchoolConfig("nycu-info-mag-fin", ("imf.nycu.edu.tw",), name_selectors=("strong",))
        html = '<main><strong>系所成員</strong></main>'
        self.assertEqual(extract_records_from_html(html, "https://imf.nycu.edu.tw/imf/ch/app/folder/5983", "zh", config), [])

    def test_shared_role_heading_applies_to_consecutive_cards(self):
        config = SchoolConfig(
            "sample", ("example.edu.tw",), card_selectors=("article.profile",),
            name_selectors=(".entry-title",), section_selectors=(".role-heading",),
        )
        html = """
        <main><h2 class="role-heading">教授</h2>
          <article class="profile"><h2 class="entry-title">王小明</h2></article>
          <article class="profile"><h2 class="entry-title">陳大華</h2><h3></h3></article>
        </main>"""
        rows = extract_records_from_html(html, "https://example.edu.tw/faculty", "zh", config)
        self.assertEqual([row.titles for row in rows], [["教授"], ["教授"]])

    def test_detail_table_name_title_and_research_are_extracted(self):
        html = """
        <main><h1>Faculty Profile</h1><table>
          <tr><th>姓名</th><td>王小明</td></tr>
          <tr><th>職稱</th><td>副教授</td></tr>
          <tr><th>研究專長</th><td>機制設計</td></tr>
        </table></main>"""
        rows = extract_records_from_html(html, "https://example.edu.tw/archives/123", "zh", self.config, detail=True)
        self.assertEqual(rows[0].name_zh, "王小明")
        self.assertEqual(rows[0].titles, ["副教授"])
        self.assertEqual(rows[0].research_interests, ["機制設計"])

    def test_management_tabs_do_not_cross_into_other_sections(self):
        config = SchoolConfig(
            "sample", ("example.edu.tw",),
            education_selectors=("#tab2 > .con_title2 + .tx14",),
            research_field_heading_selectors=("#tab1 .con_title2",),
            research_summary_heading_selectors=("#tab1 .con_title2",),
        )
        html = """
        <main><h1 class="member-name">王小明</h1>
          <div id="tab1"><div class="con_title2">主要研究領域</div><div class="tx14">公司理財、IPO 與 SPAC</div>
            <div class="con_title2">研究領域摘要</div><div class="tx14">公司治理與資本市場實證研究</div>
            <div class="con_title2">學歷</div><div class="tx14">不應進入研究欄位</div>
            <div class="con_title2">課程</div><div class="tx14">投資學</div></div>
          <div id="tab2"><div class="con_title2">學歷</div><div class="tx14">Example University, Ph.D.</div>
            <div class="con_title2">經歷</div><div class="tx14">Example University, Professor</div></div>
        </main>"""
        rows = extract_records_from_html(html, "https://example.edu.tw/faculty/1", "zh", config, detail=True)
        self.assertEqual(rows[0].research_interests, ["公司理財、IPO 與 SPAC", "公司治理與資本市場實證研究"])
        self.assertEqual(rows[0].research_fields, ["公司理財、IPO 與 SPAC"])
        self.assertEqual(rows[0].research_field_summaries, ["公司治理與資本市場實證研究"])
        self.assertEqual(rows[0].education, ["Example University, Ph.D."])

    def test_administrative_section_is_excluded_and_not_followed(self):
        config = SchoolConfig(
            "ntu-econ", ("econ.ntu.edu.tw",), card_selectors=("article.profile",),
            name_selectors=(".entry-title",), section_selectors=(".role-heading",),
            profile_patterns=(r"/archives/\d+",),
        )
        html = """
        <main><h2 class="role-heading">助理教授</h2>
          <article class="profile"><h3 class="entry-title"><a href="/archives/100">王小明</a></h3></article>
          <h2 class="role-heading">系辦同仁</h2>
          <article class="profile"><h3 class="entry-title"><a href="/archives/200">陳組員</a></h3></article>
        </main>"""
        rows = extract_records_from_html(html, "https://econ.ntu.edu.tw/archives/1", "zh", config)
        self.assertEqual([row.name_zh for row in rows], ["王小明"])
        profiles, _categories, _pdfs = discover_links(html, "https://econ.ntu.edu.tw/archives/1", config)
        self.assertEqual(profiles, ["https://econ.ntu.edu.tw/archives/100"])

    def test_retired_heading_survives_blank_and_name_headings(self):
        html = """
        <main><h2>Retired Professors</h2>
          <div class="faculty-card"><h3 class="member-name">Jane Chen</h3><h4></h4></div>
          <div class="faculty-card"><h3 class="member-name">John Lin</h3><h4></h4></div>
        </main>"""
        rows = extract_records_from_html(html, "https://example.edu.tw/faculty", "en", self.config)
        self.assertEqual([row.titles for row in rows], [["Retired Professors"], ["Retired Professors"]])

    def test_page_titles_and_administrative_specialist_are_excluded(self):
        html = """
        <main><div class="faculty-card"><h3 class="member-name">教師</h3></div>
          <div class="faculty-card"><h3 class="member-name">榮譽獎勵</h3></div>
          <div class="faculty-card"><h3 class="member-name">蔡明潔</h3><div class="member-title">行政專員</div></div>
        </main>"""
        self.assertEqual(extract_records_from_html(html, "https://example.edu.tw/faculty", "zh", self.config), [])


class MergeAndOutputTests(unittest.TestCase):
    def setUp(self):
        self.zh = SourceRecord("sample", "zh", name_zh="王小明", name_en="Ming Wang", titles=["兼任教授"],
                               education=["臺灣大學博士"], research_interests=["機器學習"],
                               research_fields=["機器學習"],
                               emails=["ming@example.edu.tw"], listing_urls=["https://example.edu.tw/zh/faculty"])
        self.en = SourceRecord("sample", "en", name_en="Ming Wang", titles=["Adjunct Professor"],
                               education=["Ph.D., NTU"], research_interests=["Machine Learning"],
                               research_fields=["Machine Learning"],
                               emails=["ming@example.edu.tw"], listing_urls=["https://example.edu.tw/en/faculty"])

    def test_merge_by_email(self):
        rows = merge_languages("sample", [self.zh], [self.en], "2026-01-01T00:00:00+08:00")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["merge_status"], "matched")
        self.assertEqual(rows[0]["merge_method"], "email")
        self.assertIn("adjunct", rows[0]["role_groups"])
        self.assertEqual(rows[0]["research_fields_zh"], ["機器學習"])
        self.assertEqual(rows[0]["research_fields_en"], ["Machine Learning"])

    def test_role_aligned_order_can_pair_bilingual_aliases(self):
        zh = [
            SourceRecord("sample", "zh", name_zh="徐熊健", titles=["兼任教授"]),
            SourceRecord("sample", "zh", name_zh="游家牧", titles=["合聘教授"]),
        ]
        en = [
            SourceRecord("sample", "en", name_en="Shyong Jian Shyu", titles=["Adjunct Professor"]),
            SourceRecord("sample", "en", name_en="Unrelated Name", titles=["Professor"]),
        ]
        self.assertTrue(pair_records_by_role_order(zh, en))
        rows = merge_languages("sample", zh, en, "2026-01-01T00:00:00+08:00")
        self.assertEqual(len(rows), 3)
        matched = next(row for row in rows if row["merge_status"] == "matched")
        self.assertEqual(matched["name_zh"], "徐熊健")
        self.assertEqual(matched["name_en"], "Shyong Jian Shyu")

    def test_ambiguous_names_are_not_forced(self):
        zh = [SourceRecord("sample", "zh", name_en="Same Name"), SourceRecord("sample", "zh", name_en="Same Name")]
        en = [SourceRecord("sample", "en", name_en="Same Name")]
        rows = merge_languages("sample", zh, en, "2026-01-01T00:00:00+08:00")
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(row["merge_status"] != "matched" for row in rows))

    def test_outputs_and_analysis_are_separated(self):
        faculty = merge_languages("sample", [self.zh], [self.en], "2026-01-01T00:00:00+08:00")
        result = SchoolResult("sample", [self.zh.as_dict()], [self.en.as_dict()], faculty,
                              ["https://example.edu.tw/zh/faculty"], [], [], "2026-01-01T00:00:00+08:00")
        config = SchoolConfig("sample", ("example.edu.tw",))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_school_data(result, config, root, {"url_ch": "https://example.edu.tw/zh/faculty", "url_eng": "https://example.edu.tw/en/faculty"})
            report = analyze_school(result, root)
            write_cross_school_analysis([report], root)
            self.assertTrue((root / "data/data-collection/sample/faculty.json").exists())
            self.assertTrue((root / "data/data-collection/sample/faculty.csv").exists())
            self.assertFalse((root / "data/data-collection/sample/bilingual-differences.csv").exists())
            self.assertTrue((root / "analysis/data-collection/sample/bilingual-differences.csv").exists())
            self.assertTrue((root / "analysis/data-collection/collection-summary.csv").exists())
            ids = {row["faculty_id"] for row in faculty}
            with (root / "analysis/data-collection/sample/bilingual-differences.csv").open(encoding="utf-8-sig") as handle:
                self.assertTrue(all(row["faculty_id"] in ids for row in csv.DictReader(handle)))

    def test_validation_rejects_external_source_url(self):
        faculty = merge_languages("sample", [self.zh], [self.en], "2026-01-01T00:00:00+08:00")
        faculty[0]["profile_urls_zh"] = ["https://external.example/profile"]
        issues = validate_faculty(SchoolConfig("sample", ("example.edu.tw",)), faculty)
        self.assertTrue(any("超出允許網域" in issue for issue in issues))


class ConfigurationTests(unittest.TestCase):
    def test_workbook_and_all_collectors(self):
        root = SCRIPT_DIR.parents[1]
        sources = read_school_sources(root / "data/data-collection/prof_info_page_links.xlsx")
        cases = json.loads((SCRIPT_DIR / "tests/fixtures/site_cases.json").read_text(encoding="utf-8"))
        collectors = sorted(SCRIPT_DIR.glob("*/collector.py"))
        self.assertEqual(len(collectors), 14)
        self.assertEqual(set(sources), set(cases))
        for path in collectors:
            module = load_collector(path)
            self.assertEqual(module.CONFIG.school_id, path.parent.name)
            self.assertIn(path.parent.name, sources)
            case = cases[path.parent.name]
            for lang in ("zh", "en"):
                name = case[lang]
                html = f'<main><h2>Faculty</h2><div class="faculty-card"><h3 class="member-name">{name}</h3><div class="member-title">Professor</div><div class="member-degree">Ph.D.</div><div class="member-research">Data Science</div></div></main>'
                rows = extract_records_from_html(html, f'https://{module.CONFIG.allowed_hosts[0]}/faculty', lang, module.CONFIG)
                self.assertEqual(len(rows), 1, path.parent.name)


if __name__ == "__main__":
    unittest.main()
