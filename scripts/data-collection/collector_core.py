from __future__ import annotations

import csv
import base64
import hashlib
import importlib.util
import io
import json
import os
import re
import tempfile
import time
import unicodedata
import urllib.parse
import zipfile
from collections import Counter, deque
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo


ACADEMIC_WORDS = (
    "教授", "師資", "教師", "講座", "研究員", "學者", "專任", "兼任", "合聘", "客座",
    "名譽", "榮譽", "退休", "專案", "約聘", "實務", "faculty", "professor", "lecturer",
    "researcher", "emeritus", "adjunct", "joint", "visiting", "chair", "teacher",
)
ADMIN_WORDS = (
    "行政人員", "行政團隊", "行政技術", "行政專員", "系辦同仁", "職員", "組員", "助教", "秘書", "辦事員", "工友",
    "staff", "department staff", "office staff", "administration", "administrative", "secretary", "assistant staff",
)
ROLE_PAGE_WORDS = (
    "系主任", "副主任", "主任", "所長", "專任", "兼任", "合聘", "客座", "名譽", "榮譽", "退休", "專案", "約聘", "實務", "師資", "教師", "教授",
    "full-time", "full time", "adjunct", "part-time", "part time", "joint", "visiting", "emeritus", "retired",
    "faculty", "professor", "teacher", "contract", "project-based", "professional expert",
)
ROLE_MAP = {
    "full_time": ("專任", "full-time", "full time", "assistant professor", "associate professor"),
    "adjunct": ("兼任", "adjunct", "part-time", "part time"),
    "joint": ("合聘", "joint"),
    "visiting": ("客座", "訪問", "visiting"),
    "emeritus": ("名譽", "榮譽", "退休", "emeritus", "honorary", "retired"),
    "chair": ("講座", "chair professor", "distinguished professor"),
    "project": ("專案", "約聘", "契約", "project", "contract"),
    "practice": ("實務", "professional expert", "professor of practice"),
}
COMMON_CARD_SELECTORS = (
    ".member-card", ".captain-member-card", ".member-item", ".faculty-item", ".faculty-card",
    ".teacher-item", ".teacher-card", ".staff-item", ".people-item", ".person", ".member",
    ".col-sm-6 .card", ".col-md-4 .card", ".col-md-3 .card", "article.profile", "li.profile",
)
NAME_SELECTORS = (
    ".member-name", ".faculty-name", ".teacher-name", ".member-data-value-name", "a.namelink", ".name", ".card-title", ".mtitle", "span.style35",
    "h1", "h2", "h3", "h4", "strong",
)
TITLE_SELECTORS = (
    ".member-data-value-1", ".member-title", ".faculty-title", ".teacher-title", ".position", ".job-title", ".title",
)
EDUCATION_SELECTORS = (".member-data-value-degree", ".member-degree", ".degree", ".education", ".edu", ".academic")
RESEARCH_SELECTORS = (
    ".member-data-value-2", ".member-research", ".member-description", ".research", ".expertise", ".specialty", ".field",
)
PROFILE_HINTS = ("member", "faculty", "teacher", "professor", "people", "profile", "detail", "show")
LABELS = {
    "name": ("姓名", "name"),
    "education": ("學歷", "教育背景", "最高學歷", "degree", "education", "academic qualification"),
    "research": ("專長及研究領域", "主要研究領域", "研究領域摘要", "研究領域", "研究興趣", "研究專長", "專長領域", "領域", "專長", "research interests", "research expertise", "research field summary", "research field", "research focus", "research area", "area of expertise", "expertise", "specialty"),
    "title": ("職稱", "現職", "position", "title"),
}
RESEARCH_FIELD_LABELS = ("主要研究領域", "研究領域", "research field")
RESEARCH_SUMMARY_LABELS = ("研究領域摘要", "research field summary")

FIELD_NOISE = {
    "title": {
        "個人資料", "詳細資料", "detailed information", "faculty", "faculty members",
        "教師", "師資", "摘要", "summary",
    },
    "education": {
        "s", "degree", "degrees", "education", "academic qualification", "學歷", "教育背景",
        "經歷", "榮譽", "經歷 榮譽", "experience", "honors", "experience honors",
    },
    "research": {
        "研究領域", "研究興趣", "研究專長", "專長", "領域", "摘要", "summary",
        "research field", "research interests", "research expertise", "research field summary",
        "個人資料", "detailed information", "暫無資料", "no data available",
    },
}


def now_iso() -> str:
    return datetime.now(ZoneInfo("Asia/Taipei")).isoformat(timespec="seconds")


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKC", str(value)).replace("\u00a0", " ")
    text = re.sub(r"[\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff]", "", text)
    return re.sub(r"\s+", " ", text).strip(" \t\r\n|,;；")


def unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        value = clean_text(value)
        key = value.casefold()
        if value and key not in seen:
            result.append(value)
            seen.add(key)
    return result


def normalized_name(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"[^0-9a-z\u3400-\u9fff]", "", value)


def has_cjk(value: str) -> bool:
    return bool(re.search(r"[\u3400-\u9fff]", value))


def has_latin(value: str) -> bool:
    return bool(re.search(r"[A-Za-z]", value))


def split_names(text: str, lang: str) -> tuple[str, str]:
    text = clean_text(text)
    text = re.sub(r"^(姓名|Name)\s*[:：]\s*", "", text, flags=re.I)
    bilingual = re.match(r"^([\u3400-\u9fff·]{2,8})\s+([A-Za-z][A-Za-z .'-]{2,80})$", text)
    if bilingual:
        return clean_text(bilingual.group(1)), clean_text(bilingual.group(2))
    parts = unique(re.split(r"\s*[|／/]\s*|\s*[（(]\s*|\s*[）)]\s*", text))
    zh = next((p for p in parts if has_cjk(p) and len(p) <= 20), "")
    en = next((p for p in parts if has_latin(p) and not has_cjk(p) and len(p.split()) <= 8), "")
    if not zh and lang == "zh" and has_cjk(text) and len(text) <= 30:
        zh = text
    if not en and lang == "en" and has_latin(text) and len(text.split()) <= 8:
        en = text
    return zh, en


def classify_roles(*values: str) -> list[str]:
    text = " ".join(values).casefold()
    roles = [role for role, terms in ROLE_MAP.items() if any(term in text for term in terms)]
    if not roles and any(term in text for term in ("professor", "教授", "lecturer", "教師", "faculty")):
        roles.append("faculty")
    return unique(roles)


def is_pure_admin(*values: str) -> bool:
    text = " ".join(values).casefold()
    return any(word in text for word in ADMIN_WORDS) and not any(word in text for word in ACADEMIC_WORDS)


def stable_url_id(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    useful = [(k, v) for k, v in query if k.casefold() in {"id", "uid", "member", "prof", "teacher", "sn"}]
    path_tail = parsed.path.rstrip("/").split("/")[-1]
    numeric_suffix = re.search(r"(?:-|^)(\d{3,})$", path_tail)
    if numeric_suffix:
        return numeric_suffix.group(1)
    if useful:
        return "&".join(f"{k}={v}" for k, v in useful)
    if path_tail and path_tail.casefold() not in {"faculty", "members", "member", "prof", "csie"}:
        return path_tail
    return ""


@dataclass
class SourceRecord:
    school_id: str
    language: str
    name_zh: str = ""
    name_en: str = ""
    titles: list[str] = field(default_factory=list)
    education: list[str] = field(default_factory=list)
    research_interests: list[str] = field(default_factory=list)
    research_fields: list[str] = field(default_factory=list)
    research_field_summaries: list[str] = field(default_factory=list)
    emails: list[str] = field(default_factory=list)
    listing_urls: list[str] = field(default_factory=list)
    profile_urls: list[str] = field(default_factory=list)
    personal_urls: list[str] = field(default_factory=list)
    stable_ids: list[str] = field(default_factory=list)
    section: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "school_id": self.school_id,
            "language": self.language,
            "name_zh": self.name_zh,
            "name_en": self.name_en,
            "titles": unique(self.titles),
            "education": unique(self.education),
            "research_interests": unique(self.research_interests),
            "research_fields": unique(self.research_fields),
            "research_field_summaries": unique(self.research_field_summaries),
            "emails": unique(x.casefold() for x in self.emails),
            "listing_urls": unique(self.listing_urls),
            "profile_urls": unique(self.profile_urls),
            "personal_urls": unique(self.personal_urls),
            "stable_ids": unique(self.stable_ids),
            "section": clean_text(self.section),
        }


@dataclass(frozen=True)
class SchoolConfig:
    school_id: str
    allowed_hosts: tuple[str, ...]
    extra_urls_zh: tuple[str, ...] = ()
    extra_urls_en: tuple[str, ...] = ()
    pdf_urls_zh: tuple[str, ...] = ()
    pdf_urls_en: tuple[str, ...] = ()
    json_urls_zh: tuple[str, ...] = ()
    json_urls_en: tuple[str, ...] = ()
    post_urls_zh: tuple[str, ...] = ()
    post_urls_en: tuple[str, ...] = ()
    dynamic: bool = False
    follow_profiles: bool = True
    follow_categories: bool = True
    allow_pdf: bool = False
    card_selectors: tuple[str, ...] = ()
    name_selectors: tuple[str, ...] = ()
    title_selectors: tuple[str, ...] = ()
    education_selectors: tuple[str, ...] = ()
    research_selectors: tuple[str, ...] = ()
    research_heading_selectors: tuple[str, ...] = ()
    research_field_heading_selectors: tuple[str, ...] = ()
    research_summary_heading_selectors: tuple[str, ...] = ()
    section_selectors: tuple[str, ...] = ()
    profile_patterns: tuple[str, ...] = ()
    category_patterns: tuple[str, ...] = ()
    pair_by_role_order: bool = False
    max_pages: int = 80


@dataclass
class RunOptions:
    root: Path
    headed: bool = False
    skip_analysis: bool = False
    insecure: bool = False
    timeout: float = 30.0
    delay: float = 0.35


@dataclass
class SchoolResult:
    school_id: str
    zh_records: list[dict[str, Any]]
    en_records: list[dict[str, Any]]
    faculty: list[dict[str, Any]]
    pages: list[str]
    warnings: list[str]
    errors: list[str]
    collected_at: str


class HttpClient:
    def __init__(self, options: RunOptions):
        try:
            import requests
        except ImportError as exc:
            raise RuntimeError("缺少 requests；請執行 pip install -r scripts/data-collection/requirements.txt") from exc
        self.requests = requests
        self.options = options
        if options.insecure:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "grad-school-social-network/1.0 (faculty research; respectful crawler)",
            "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        })

    def get(self, url: str, binary: bool = False) -> bytes | str:
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                response = self.session.get(
                    url, timeout=self.options.timeout, verify=not self.options.insecure, allow_redirects=True
                )
                response.raise_for_status()
                time.sleep(self.options.delay)
                if binary:
                    return response.content
                if not response.encoding or response.encoding.casefold() in {"iso-8859-1", "ascii"}:
                    response.encoding = response.apparent_encoding or "utf-8"
                return response.text
            except Exception as exc:  # requests has several transport exceptions
                last_error = exc
                if attempt < 2:
                    time.sleep(0.75 * (2 ** attempt))
        raise RuntimeError(f"下載失敗 {url}: {last_error}")

    def post(self, url: str, referer: str = "") -> str:
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                headers = {"Referer": referer} if referer else {}
                response = self.session.post(
                    url, headers=headers, timeout=self.options.timeout,
                    verify=not self.options.insecure, allow_redirects=True,
                )
                response.raise_for_status()
                time.sleep(self.options.delay)
                if not response.encoding or response.encoding.casefold() in {"iso-8859-1", "ascii"}:
                    response.encoding = response.apparent_encoding or "utf-8"
                return response.text
            except Exception as exc:
                last_error = exc
                if attempt < 2:
                    time.sleep(0.75 * (2 ** attempt))
        raise RuntimeError(f"POST 下載失敗 {url}: {last_error}")


def _xml_workbook_rows(path: Path) -> list[dict[str, str]]:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    rel_ns = {"p": "http://schemas.openxmlformats.org/package/2006/relationships"}
    with zipfile.ZipFile(path) as archive:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", ns):
                shared.append("".join(t.text or "" for t in si.iterfind(".//m:t", ns)))
        wb = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        rel_map = {r.attrib["Id"]: r.attrib["Target"] for r in rels.findall("p:Relationship", rel_ns)}
        sheet = wb.find("m:sheets/m:sheet", ns)
        if sheet is None:
            return []
        target = rel_map[sheet.attrib[f"{{{ns['r']}}}id"]].lstrip("/")
        sheet_path = target if target.startswith("xl/") else f"xl/{target}"
        xml = ET.fromstring(archive.read(sheet_path))
        table: list[list[str]] = []
        for row in xml.findall(".//m:sheetData/m:row", ns):
            values: dict[int, str] = {}
            for cell in row.findall("m:c", ns):
                ref = cell.attrib.get("r", "A1")
                letters = re.match(r"[A-Z]+", ref).group(0)
                col = 0
                for char in letters:
                    col = col * 26 + ord(char) - 64
                kind = cell.attrib.get("t")
                if kind == "inlineStr":
                    value = "".join(t.text or "" for t in cell.iterfind(".//m:t", ns))
                else:
                    node = cell.find("m:v", ns)
                    value = node.text if node is not None and node.text is not None else ""
                    if kind == "s" and value:
                        value = shared[int(value)]
                values[col - 1] = value
            width = max(values, default=-1) + 1
            table.append([values.get(i, "") for i in range(width)])
    if not table:
        return []
    headers = [clean_text(x) for x in table[0]]
    return [{headers[i]: clean_text(row[i] if i < len(row) else "") for i in range(len(headers))} for row in table[1:]]


def read_school_sources(path: Path) -> dict[str, dict[str, str]]:
    try:
        from openpyxl import load_workbook
    except ImportError:
        rows = _xml_workbook_rows(path)
    else:
        workbook = load_workbook(path, read_only=True, data_only=True)
        sheet = workbook[workbook.sheetnames[0]]
        iterator = sheet.iter_rows(values_only=True)
        headers = [clean_text(x) for x in next(iterator)]
        rows = [{headers[i]: clean_text(row[i] if i < len(row) else "") for i in range(len(headers))} for row in iterator]
        workbook.close()
    aliases = {"ntu-comm-engin-ds": "ntu-comm-engin-ds-network"}
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = aliases.get(row.get("school", ""), row.get("school", ""))
        if key:
            result[key] = {"url_ch": row.get("url_ch", ""), "url_eng": row.get("url_eng", ""), "note": row.get("note", "")}
    return result


def host_allowed(url: str, allowed_hosts: Iterable[str]) -> bool:
    host = (urllib.parse.urlsplit(url).hostname or "").casefold()
    return any(host == allowed.casefold() or host.endswith("." + allowed.casefold()) for allowed in allowed_hosts)


def page_language_url(url: str, lang: str) -> str:
    return url


def _soup(html: str):
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise RuntimeError("缺少 beautifulsoup4；請執行 pip install -r scripts/data-collection/requirements.txt") from exc
    try:
        return BeautifulSoup(html, "lxml")
    except Exception:
        return BeautifulSoup(html, "html.parser")


def _text_from_first(node: Any, selectors: Iterable[str]) -> str:
    for selector in selectors:
        found = node.select_one(selector)
        if found:
            value = clean_text(found.get_text(" ", strip=True))
            if value:
                return value
    return ""


def _normalize_label(value: str) -> str:
    value = clean_text(value).strip(":： ").casefold()
    # Many bilingual sites render labels as, for example, 學歷(Education).
    value = re.sub(r"\s*[（(][^()（）]{1,80}[）)]\s*$", "", value)
    return clean_text(value).strip(":： ").casefold()


def _split_labeled_text(text: str, labels: Iterable[str]) -> tuple[bool, str]:
    text = clean_text(text)
    normalized_labels = {_normalize_label(label) for label in labels}
    if _normalize_label(text) in normalized_labels:
        return True, ""
    for separator in ("：", ":"):
        if separator in text:
            left, right = text.split(separator, 1)
            if _normalize_label(left) in normalized_labels:
                return True, clean_text(right)
    for label in sorted(labels, key=len, reverse=True):
        match = re.match(rf"^{re.escape(label)}\s+(.+)$", text, re.I)
        if match:
            return True, clean_text(match.group(1))
    return False, ""


def _is_role_section(text: str) -> bool:
    normalized = clean_text(text).casefold()
    blocked = {"榮譽獎勵", "個人資料", "詳細資料", "detailed information"}
    return bool(
        normalized and len(normalized) <= 160
        and normalized not in {value.casefold() for value in blocked}
        and any(word in normalized for word in ROLE_PAGE_WORDS)
    )


def _nearest_section(node: Any, selectors: Iterable[str] = ()) -> str:
    for selector in selectors:
        found = None
        if selector.startswith("."):
            found = node.find_previous(class_=selector[1:])
        elif selector.startswith("#"):
            found = node.find_previous(id=selector[1:])
        if found:
            value = clean_text(found.get_text(" ", strip=True))
            if _is_role_section(value):
                return value
    # A category heading commonly applies to several following cards. Walk past
    # empty headings and previous faculty names until the nearest role heading.
    for heading in node.find_all_previous(["h1", "h2", "h3", "h4", "h5", "h6"]):
        value = clean_text(heading.get_text(" ", strip=True))
        if _is_role_section(value):
            return value
        if is_pure_admin(value):
            return value
        if value in {"榮譽獎勵", "個人資料", "詳細資料"}:
            return ""
    return ""


def _content_root(soup: Any) -> Any:
    for selector in ("main#main-content", "main", "article", "#content", ".page-content", ".main-content", ".content"):
        found = soup.select_one(selector)
        if found is not None:
            return found
    return soup.body or soup


def _labeled_values(node: Any, labels: Iterable[str]) -> list[str]:
    output: list[str] = []
    # Key/value table rows are the most reliable representation.
    for row in node.select("tr"):
        cells = [clean_text(cell.get_text(" ", strip=True)) for cell in row.select(":scope > th, :scope > td")]
        if len(cells) < 2:
            continue
        matched, inline_value = _split_labeled_text(cells[0], labels)
        if matched:
            value = inline_value or clean_text(" | ".join(value for value in cells[1:] if value))
            if value:
                output.append(value)

    # Definition lists and exact section headings are also structurally safe.
    for term in node.select("dt"):
        matched, inline_value = _split_labeled_text(term.get_text(" ", strip=True), labels)
        if not matched:
            continue
        definition = term.find_next_sibling("dd")
        value = inline_value or clean_text(definition.get_text(" ", strip=True) if definition else "")
        if value:
            output.append(value)
    for heading in node.select("h1, h2, h3, h4, h5, h6, .title"):
        matched, inline_value = _split_labeled_text(heading.get_text(" ", strip=True), labels)
        if not matched:
            continue
        sibling = heading.find_next_sibling()
        value = inline_value or clean_text(sibling.get_text(" ", strip=True) if sibling else "")
        if value:
            output.append(value)

    # Some NYCU pages put a label and its value in adjacent inline markup, either
    # as two spans or as a strong label followed by a raw text node. Read only
    # until the next line break so separate navigation entries cannot be paired.
    for candidate in node.select("span, strong, b"):
        matched, inline_value = _split_labeled_text(candidate.get_text(" ", strip=True), labels)
        if not matched or inline_value:
            continue
        parts: list[str] = []
        for sibling in candidate.next_siblings:
            if getattr(sibling, "name", None) == "br":
                break
            if getattr(sibling, "get_text", None):
                part = clean_text(sibling.get_text(" ", strip=True))
            else:
                part = clean_text(str(sibling))
            if part:
                parts.append(part)
        value = clean_text(" ".join(parts)).lstrip(":： ")
        value_is_label, _ = _split_labeled_text(value, labels)
        if value and not value_is_label:
            output.append(value)

    # Compact inline nodes only: never read an entire parent container.
    block_tags = {"article", "div", "dl", "li", "ol", "p", "section", "table", "tr", "ul"}
    for candidate in node.select("li, p, div, span, td, th"):
        if candidate.name == "div" and any(child.name in block_tags for child in candidate.children if getattr(child, "name", None)):
            continue
        text = clean_text(candidate.get_text(" ", strip=True))
        if not text or len(text) > 1000:
            continue
        matched, value = _split_labeled_text(text, labels)
        # A malformed wrapper can contain several <br>-separated fields. In
        # that case its first label matches but the "value" is the rest of the
        # card; the individual inline labels above are the reliable source.
        embedded_label = any(
            re.search(rf"(?:^|\s){re.escape(label)}\s*[:：]", value, re.I)
            for group in LABELS.values() for label in group
        )
        if matched and value and not embedded_label:
            output.append(value)
    return unique(output)


def _values_after_labeled_headings(node: Any, selectors: Iterable[str], labels: Iterable[str]) -> list[str]:
    output: list[str] = []
    for selector in selectors:
        for heading in node.select(selector):
            matched, inline_value = _split_labeled_text(heading.get_text(" ", strip=True), labels)
            if not matched:
                continue
            sibling = heading.find_next_sibling()
            value = inline_value or clean_text(sibling.get_text(" ", strip=True) if sibling else "")
            if value:
                output.append(value)
    return unique(output)


def _education_table_values(node: Any) -> list[str]:
    output: list[str] = []
    school_labels = {"school", "school name", "university", "學校", "學校名稱"}
    degree_labels = {"degree", "學位"}
    for table in node.select("table"):
        rows = table.select("tr")
        for header_index, row in enumerate(rows):
            headers = [_normalize_label(cell.get_text(" ", strip=True)) for cell in row.select(":scope > th, :scope > td")]
            school_index = next((i for i, value in enumerate(headers) if value in school_labels), None)
            degree_index = next((i for i, value in enumerate(headers) if value in degree_labels), None)
            if school_index is None or degree_index is None:
                continue
            for data_row in rows[header_index + 1:]:
                cells = [clean_text(cell.get_text(" ", strip=True)) for cell in data_row.select(":scope > th, :scope > td")]
                if max(school_index, degree_index) >= len(cells) or not cells[school_index] or not cells[degree_index]:
                    continue
                value = " | ".join(cell for cell in cells if cell)
                if value:
                    output.append(value)
            break
    return unique(output)


def _valid_field_values(values: Iterable[str], field_name: str, raw_name: str = "") -> list[str]:
    output: list[str] = []
    all_labels = {_normalize_label(label) for group in LABELS.values() for label in group}
    noise = {_normalize_label(value) for value in FIELD_NOISE[field_name]}
    for value in unique(values):
        value = clean_text(value).lstrip(":： ")
        normalized = _normalize_label(value)
        lowered = value.casefold()
        if not normalized or normalized in noise or normalized in all_labels or value == raw_name:
            continue
        if field_name == "research" and (
            "research field summary education" in lowered
            or "summary education courses" in lowered
            or ("研究領域摘要" in value and "學歷" in value)
        ):
            continue
        output.append(value)
    return unique(output)


def _inferred_education(node: Any) -> list[str]:
    terms = ("博士", "碩士", "學士", "ph.d", "phd", "doctor of", "master of", "bachelor of")
    values: list[str] = []
    for text in node.stripped_strings:
        value = clean_text(text)
        lowered = value.casefold()
        if 3 <= len(value) <= 300 and any(term in lowered for term in terms):
            if not any(label.casefold() == lowered.rstrip(":： ") for label in LABELS["education"]):
                values.append(value)
    return unique(values)


def _looks_like_name(text: str) -> bool:
    text = clean_text(text)
    if not text or len(text) > 90 or any(mark in text for mark in ("@", "http://", "https://")):
        return False
    non_people = {
        "教授成員", "師資陣容", "專任教師", "兼任教師", "合聘教師", "退休教授",
        "榮譽教授", "榮譽講座", "教師", "榮譽獎勵", "個人資料", "詳細資料",
        "系所成員", "faculty", "faculty & staff", "faculty members", "members", "teachers", "detailed information",
    }
    if normalized_name(text) in {normalized_name(value) for value in non_people}:
        return False
    zh, en = split_names(text, "zh" if has_cjk(text) else "en")
    if zh and 2 <= len(normalized_name(zh)) <= 12:
        return True
    return bool(en and 2 <= len(en.split()) <= 6 and not any(x in en.casefold() for x in ACADEMIC_WORDS + ADMIN_WORDS))


def _usable_detail_name(text: str) -> bool:
    blocked = {"正體中文", "简体中文", "繁體中文", "english", "home", "首頁", "網站導覽", "faculty", "members"}
    return bool(text and normalized_name(text) not in {normalized_name(x) for x in blocked})


def extract_records_from_html(html: str, url: str, lang: str, config: SchoolConfig, detail: bool = False) -> list[SourceRecord]:
    soup = _soup(html)
    root = _content_root(soup)
    selectors = config.card_selectors + COMMON_CARD_SELECTORS
    cards: list[Any] = []
    seen_nodes: set[int] = set()
    for selector in selectors:
        for node in root.select(selector):
            if id(node) not in seen_nodes:
                cards.append(node)
                seen_nodes.add(id(node))
    if detail or not cards:
        cards = [root]

    records: list[SourceRecord] = []
    seen_keys: set[tuple[str, str]] = set()
    for card in cards:
        section = _nearest_section(card, config.section_selectors)
        raw_name = _text_from_first(card, config.name_selectors + NAME_SELECTORS)
        inline_title = ""
        inline_match = re.match(r"^([\u3400-\u9fff·]{2,8})\s+((?:專任|兼任|名譽|榮譽|客座|合聘|退休)?.{0,12}(?:教授|教師|講座|研究員).*)$", raw_name)
        if inline_match:
            raw_name = clean_text(inline_match.group(1))
            inline_title = clean_text(inline_match.group(2))
        else:
            english_inline = re.match(r"^((?:(?:Distinguished|Assistant|Associate|Adjunct|Visiting)\s+)?Professor(?:\s+Emeritus)?|Lecturer)\s+(.+)$", raw_name, re.I)
            if english_inline:
                inline_title = clean_text(english_inline.group(1))
                raw_name = clean_text(english_inline.group(2))
            else:
                english_suffix = re.match(r"^(.+?)\s+((?:(?:Distinguished|Assistant|Associate|Adjunct|Visiting)\s+)?Professor(?:\s+Emeritus)?|Lecturer)$", raw_name, re.I)
                if english_suffix:
                    raw_name = clean_text(english_suffix.group(1))
                    inline_title = clean_text(english_suffix.group(2))
        if not _looks_like_name(raw_name):
            raw_name = next((value for value in _labeled_values(card, LABELS["name"]) if _looks_like_name(value)), "")
        if not _looks_like_name(raw_name):
            links = card.select('a[href*="member"], a[href*="faculty"], a[href*="prof"], a[href*="teacher"], a[href*="detail"]')
            raw_name = next((clean_text(link.get_text(" ", strip=True)) for link in links if _looks_like_name(link.get_text(" ", strip=True))), "")
        if not _looks_like_name(raw_name):
            continue
        name_zh, name_en = split_names(raw_name, lang)
        if not (name_zh or name_en):
            continue

        title_values = [inline_title]
        title = _text_from_first(card, config.title_selectors + TITLE_SELECTORS)
        if title and title != raw_name:
            title_values.append(title)
        title_values.extend(_labeled_values(card, LABELS["title"]))
        if section and _is_role_section(section):
            title_values.append(section)
        title_values = _valid_field_values(title_values, "title", raw_name)
        if is_pure_admin(*title_values) or is_pure_admin(section, *title_values):
            continue

        education = [_text_from_first(card, config.education_selectors + EDUCATION_SELECTORS)]
        education.extend(_labeled_values(card, LABELS["education"]))
        education.extend(_education_table_values(card))
        education = _valid_field_values(education, "education", raw_name)
        if not education:
            education.extend(_inferred_education(card))
            education = _valid_field_values(education, "education", raw_name)
        research = [_text_from_first(card, config.research_selectors + RESEARCH_SELECTORS)]
        research.extend(_values_after_labeled_headings(card, config.research_heading_selectors, LABELS["research"]))
        research.extend(_labeled_values(card, LABELS["research"]))
        research = _valid_field_values(research, "research", raw_name)
        research_fields = _valid_field_values(
            _values_after_labeled_headings(card, config.research_field_heading_selectors, RESEARCH_FIELD_LABELS),
            "research", raw_name,
        )
        research_field_summaries = _valid_field_values(
            _values_after_labeled_headings(card, config.research_summary_heading_selectors, RESEARCH_SUMMARY_LABELS),
            "research", raw_name,
        )
        if config.research_field_heading_selectors or config.research_summary_heading_selectors:
            research = unique([*research_fields, *research_field_summaries])
        else:
            research_fields = research
        emails = [a.get("href", "")[7:].split("?")[0] for a in card.select('a[href^="mailto:"]')]
        emails.extend(re.findall(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", card.get_text(" ", strip=True), re.I))
        for script in card.select("script.e-enc"):
            match = re.search(r'atob\(["\']([A-Za-z0-9+/=]+)["\']\)', script.get_text(" ", strip=True))
            if match:
                try:
                    decoded = base64.b64decode(match.group(1)).decode("utf-8")
                    if "@" in decoded:
                        emails.append(decoded)
                except Exception:
                    pass
        profile_urls: list[str] = []
        personal_urls: list[str] = []
        for link in card.select("a[href]"):
            absolute = urllib.parse.urljoin(url, link.get("href", ""))
            scheme = urllib.parse.urlsplit(absolute).scheme
            if scheme not in {"http", "https"}:
                continue
            if host_allowed(absolute, config.allowed_hosts):
                href_text = absolute.casefold()
                link_text = clean_text(link.get_text(" ", strip=True))
                link_classes = link.get("class", [])
                if not detail and absolute != url and ("namelink" in link_classes or "i-member-link" in link_classes or
                                        any(hint in href_text for hint in PROFILE_HINTS) or
                                        _relevant_link(absolute, link_text, "profile", config)):
                    profile_urls.append(absolute)
            else:
                personal_urls.append(absolute)
        if detail:
            profile_urls = [url]
        stable_ids = [stable_url_id(x) for x in profile_urls]
        record = SourceRecord(
            school_id=config.school_id,
            language=lang,
            name_zh=name_zh,
            name_en=name_en,
            titles=title_values,
            education=education,
            research_interests=research,
            research_fields=research_fields,
            research_field_summaries=research_field_summaries,
            emails=unique(emails),
            listing_urls=[] if detail else [url],
            profile_urls=[url] if detail else unique(profile_urls),
            personal_urls=unique(personal_urls),
            stable_ids=unique(x for x in stable_ids if x),
            section=section,
        )
        key = (normalized_name(record.name_zh or record.name_en), url)
        if key not in seen_keys:
            records.append(record)
            seen_keys.add(key)
    return records


def _relevant_link(url: str, text: str, kind: str, config: SchoolConfig) -> bool:
    combined = f"{url} {text}".casefold()
    if is_pure_admin(text, url):
        return False
    patterns = config.profile_patterns if kind == "profile" else config.category_patterns
    if kind == "profile":
        if patterns:
            return any(re.search(pattern, combined, re.I) for pattern in patterns)
        return any(hint in combined for hint in PROFILE_HINTS) and bool(stable_url_id(url))
    is_pagination = any(k in url.casefold() for k in ("page_no=", "page=")) and bool(re.search(r"(?:next|previous|下一|上一|\d+)", text, re.I))
    role_link = any(word in text.casefold() for word in ROLE_PAGE_WORDS)
    path_hint = any(hint in url.casefold() for hint in ("member", "faculty", "teacher", "professor", "showlist", "folder", "artwebsite"))
    configured = not patterns or any(re.search(pattern, combined, re.I) for pattern in patterns)
    return is_pagination or (role_link and (path_hint or configured))


def discover_links(html: str, base_url: str, config: SchoolConfig) -> tuple[list[str], list[str], list[str]]:
    soup = _soup(html)
    profiles: list[str] = []
    categories: list[str] = []
    pdfs: list[str] = []
    profile_link_nodes: set[int] = set()
    for selector in config.card_selectors + COMMON_CARD_SELECTORS:
        for card in soup.select(selector):
            if is_pure_admin(_nearest_section(card, config.section_selectors)):
                continue
            profile_link_nodes.update(id(link) for link in card.select("a[href]"))
    for link in soup.select("a[href]"):
        href = urllib.parse.urljoin(base_url, link.get("href", "")).split("#")[0]
        text = clean_text(link.get_text(" ", strip=True))
        if not host_allowed(href, config.allowed_hosts):
            continue
        path = urllib.parse.urlsplit(href).path.casefold()
        if path.endswith(".pdf"):
            if config.allow_pdf and (any(word in text.casefold() for word in ROLE_PAGE_WORDS) or
                                     any(word in href.casefold() for word in ("faculty", "teacher", "professor"))):
                pdfs.append(href)
        elif ("namelink" in link.get("class", []) or "i-member-link" in link.get("class", [])) and stable_url_id(href):
            profiles.append(href)
        elif id(link) in profile_link_nodes and _relevant_link(href, text, "profile", config):
            profiles.append(href)
        elif _relevant_link(href, text, "category", config):
            categories.append(href)
    return unique(profiles), unique(categories), unique(pdfs)


def _record_key(record: SourceRecord) -> str:
    if record.stable_ids:
        return "id:" + record.stable_ids[0].casefold()
    if record.emails:
        return "mail:" + record.emails[0].casefold()
    if record.profile_urls:
        return "url:" + record.profile_urls[0].casefold()
    return "name:" + normalized_name(record.name_zh or record.name_en)


def combine_source_records(records: list[SourceRecord]) -> list[SourceRecord]:
    grouped: dict[str, SourceRecord] = {}
    for record in records:
        key = _record_key(record)
        current = grouped.get(key)
        if current is None:
            grouped[key] = record
            continue
        current.name_zh = current.name_zh or record.name_zh
        current.name_en = current.name_en or record.name_en
        for attr in ("titles", "education", "research_interests", "research_fields", "research_field_summaries", "emails", "listing_urls", "profile_urls", "personal_urls", "stable_ids"):
            setattr(current, attr, unique(getattr(current, attr) + getattr(record, attr)))
        current.section = current.section or record.section
    return list(grouped.values())


def merge_detail(listing: SourceRecord, detail: SourceRecord) -> SourceRecord:
    if not listing.name_zh and _usable_detail_name(detail.name_zh):
        listing.name_zh = detail.name_zh
    if not listing.name_en and _usable_detail_name(detail.name_en):
        listing.name_en = detail.name_en
    for attr in ("titles", "education", "research_interests", "research_fields", "research_field_summaries", "emails", "profile_urls", "personal_urls", "stable_ids"):
        setattr(listing, attr, unique(getattr(listing, attr) + getattr(detail, attr)))
    return listing


def _match_score(zh: SourceRecord, en: SourceRecord) -> tuple[int, str]:
    if set(x.casefold() for x in zh.stable_ids) & set(x.casefold() for x in en.stable_ids):
        return 100, "stable_id"
    if set(x.casefold() for x in zh.emails) & set(x.casefold() for x in en.emails):
        return 90, "email"
    if set(x.casefold() for x in zh.profile_urls + zh.personal_urls) & set(x.casefold() for x in en.profile_urls + en.personal_urls):
        return 80, "url"
    names_zh = {normalized_name(x) for x in (zh.name_zh, zh.name_en) if x}
    names_en = {normalized_name(x) for x in (en.name_zh, en.name_en) if x}
    if names_zh & names_en:
        return 70, "name"
    return 0, ""


def _faculty_id(school_id: str, zh: SourceRecord | None, en: SourceRecord | None) -> str:
    record = zh or en
    assert record is not None
    identity = (record.stable_ids or record.emails or record.profile_urls or [record.name_zh or record.name_en])[0]
    digest = hashlib.sha1(f"{school_id}|{identity.casefold()}".encode("utf-8")).hexdigest()[:10]
    slug = normalized_name(record.name_en or record.name_zh)[:32] or "faculty"
    return f"{school_id}-{slug}-{digest}"


def merge_languages(school_id: str, zh_records: list[SourceRecord], en_records: list[SourceRecord], collected_at: str) -> list[dict[str, Any]]:
    candidates: list[tuple[int, int, int, str]] = []
    for zi, zh in enumerate(zh_records):
        for ei, en in enumerate(en_records):
            score, reason = _match_score(zh, en)
            if score:
                candidates.append((score, zi, ei, reason))
    candidates.sort(reverse=True)
    used_zh: set[int] = set()
    used_en: set[int] = set()
    pairs: list[tuple[SourceRecord | None, SourceRecord | None, str]] = []
    for score, zi, ei, reason in candidates:
        if zi not in used_zh and ei not in used_en:
            same_zh_score = sum(1 for s, z, _e, _r in candidates if z == zi and s == score)
            same_en_score = sum(1 for s, _z, e, _r in candidates if e == ei and s == score)
            if same_zh_score == 1 and same_en_score == 1:
                pairs.append((zh_records[zi], en_records[ei], reason))
                used_zh.add(zi)
                used_en.add(ei)
    pairs.extend((record, None, "") for i, record in enumerate(zh_records) if i not in used_zh)
    pairs.extend((None, record, "") for i, record in enumerate(en_records) if i not in used_en)

    faculty: list[dict[str, Any]] = []
    for zh, en, reason in pairs:
        z = zh or SourceRecord(school_id, "zh")
        e = en or SourceRecord(school_id, "en")
        roles = classify_roles(*(z.titles + e.titles + [z.section, e.section]))
        faculty.append({
            "faculty_id": _faculty_id(school_id, zh, en),
            "school_id": school_id,
            "name_zh": z.name_zh or e.name_zh,
            "name_en": e.name_en or z.name_en,
            "role_groups": roles,
            "titles_zh": unique(z.titles),
            "titles_en": unique(e.titles),
            "education_zh": unique(z.education),
            "education_en": unique(e.education),
            "research_interests_zh": unique(z.research_interests),
            "research_interests_en": unique(e.research_interests),
            "research_fields_zh": unique(z.research_fields),
            "research_fields_en": unique(e.research_fields),
            "research_field_summaries_zh": unique(z.research_field_summaries),
            "research_field_summaries_en": unique(e.research_field_summaries),
            "listing_urls_zh": unique(z.listing_urls),
            "listing_urls_en": unique(e.listing_urls),
            "profile_urls_zh": unique(z.profile_urls),
            "profile_urls_en": unique(e.profile_urls),
            "personal_urls": unique(z.personal_urls + e.personal_urls),
            "emails": unique(z.emails + e.emails),
            "merge_status": "matched" if zh and en else ("zh_only" if zh else "en_only"),
            "merge_method": reason,
            "collected_at": collected_at,
        })
    return sorted(faculty, key=lambda x: (normalized_name(x["name_zh"]), normalized_name(x["name_en"])))


def pair_records_by_role_order(zh_records: list[SourceRecord], en_records: list[SourceRecord]) -> bool:
    """Add match IDs for a site whose bilingual lists use the same role-aligned order."""
    if len(zh_records) != len(en_records):
        return False
    for index, (zh, en) in enumerate(zip(zh_records, en_records, strict=True), 1):
        zh_roles = set(classify_roles(zh.section, *zh.titles))
        en_roles = set(classify_roles(en.section, *en.titles))
        if not zh_roles.intersection(en_roles):
            continue
        position_id = f"bilingual-role-order:{index}"
        zh.stable_ids = unique([*zh.stable_ids, position_id])
        en.stable_ids = unique([*en.stable_ids, position_id])
    return True


def _render_dynamic(url: str, options: RunOptions) -> tuple[str, list[Any]]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("動態頁需要 playwright；請安裝 requirements 並執行 python -m playwright install chromium") from exc
    payloads: list[Any] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not options.headed)
        page = browser.new_page(locale="zh-TW")

        def capture(response: Any) -> None:
            try:
                if urllib.parse.urlsplit(response.url).hostname == urllib.parse.urlsplit(url).hostname and "json" in response.headers.get("content-type", ""):
                    payloads.append(response.json())
            except Exception:
                pass

        page.on("response", capture)
        page.goto(url, wait_until="networkidle", timeout=int(options.timeout * 1000))
        page.wait_for_timeout(750)
        html = page.content()
        browser.close()
    return html, payloads


def _json_people(payload: Any, config: SchoolConfig, lang: str, url: str) -> list[SourceRecord]:
    output: list[SourceRecord] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            keys = {str(k).casefold(): k for k in value}
            if "ei_id" in keys and ("ei_name_tw" in keys or "ei_name_en" in keys):
                name_tw = clean_text(value.get(keys.get("ei_name_tw", ""), ""))
                name_en = clean_text(value.get(keys.get("ei_name_en", ""), ""))
                zh_match = re.search(r"[\u3400-\u9fff]{2,8}", name_tw)
                name_zh = zh_match.group(0) if zh_match else ""
                if not name_en:
                    _unused_zh, name_en = split_names(name_tw, "zh")
                title_key = "ei_title_tw" if lang == "zh" else "ei_title_en"
                research_key = "ei_research_tw" if lang == "zh" else "ei_research_en"
                link_keys = ("ei_link_tw", "ei_link_en", "ei_lablink_tw", "ei_lablink_en")
                internal_urls: list[str] = []
                personal_urls: list[str] = []
                for link_key in link_keys:
                    actual_key = keys.get(link_key)
                    link = clean_text(value.get(actual_key, "")) if actual_key is not None else ""
                    if not link:
                        continue
                    absolute = urllib.parse.urljoin(url, link)
                    (internal_urls if host_allowed(absolute, config.allowed_hosts) else personal_urls).append(absolute)
                faculty_type = clean_text(value.get(keys.get("ei_type", ""), ""))
                section = {"core": "核心師資", "pt": "專案教師", "at": "兼任教師"}.get(faculty_type, faculty_type)
                record = SourceRecord(
                    school_id=config.school_id,
                    language=lang,
                    name_zh=name_zh,
                    name_en=name_en,
                    titles=unique([clean_text(value.get(keys.get(title_key, ""), "")), section]),
                    research_interests=unique([clean_text(value.get(keys.get(research_key, ""), ""))]),
                    research_fields=unique([clean_text(value.get(keys.get(research_key, ""), ""))]),
                    emails=unique([clean_text(value.get(keys.get("ei_email", ""), ""))]),
                    listing_urls=[url],
                    profile_urls=unique(internal_urls),
                    personal_urls=unique(personal_urls),
                    stable_ids=unique([clean_text(value.get(keys["ei_id"], ""))]),
                    section=section,
                )
                if (record.name_zh or record.name_en) and not is_pure_admin(*record.titles):
                    output.append(record)
                return
            name_key = next((keys[k] for k in ("name", "name_zh", "name_en", "cname", "ename") if k in keys), None)
            if name_key is not None and _looks_like_name(clean_text(value[name_key])):
                raw_name = clean_text(value[name_key])
                zh, en = split_names(raw_name, lang)
                def pick(*candidates: str) -> list[str]:
                    vals = [value[keys[k]] for k in candidates if k in keys]
                    flat: list[str] = []
                    for item in vals:
                        flat.extend(item if isinstance(item, list) else [item])
                    return unique(clean_text(x) for x in flat if not isinstance(x, (dict, list)))
                output.append(SourceRecord(
                    school_id=config.school_id, language=lang, name_zh=zh, name_en=en,
                    titles=pick("title", "position", "job_title"),
                    education=pick("education", "degree"),
                    research_interests=pick("research", "research_interests", "expertise", "specialty"),
                    research_fields=pick("research", "research_interests", "expertise", "specialty"),
                    emails=pick("email"), listing_urls=[url],
                    stable_ids=pick("id", "uid", "slug"),
                ))
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload)
    return output


def _pdf_records(content: bytes, url: str, lang: str, config: SchoolConfig) -> list[SourceRecord]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return []
    text = "\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(content)).pages)
    # The handbook also contains administrative contacts and blank forms. Limit
    # this fallback to the faculty chapter to keep those names out of the data.
    faculty_start = text.find("師 資")
    if faculty_start >= 0:
        text = text[faculty_start:]
    faculty_end = text.find("二、系辦職員聯絡方式")
    if faculty_end >= 0:
        text = text[:faculty_end]

    records: list[SourceRecord] = []
    lines = [clean_text(line) for line in text.splitlines()]
    lines = [line for line in lines if line]
    joined_lines: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if re.search(r"@[A-Z0-9.\-]+\.t$", line, re.I) and index + 1 < len(lines) and lines[index + 1].casefold() == "w":
            line += "w"
            index += 1
        elif "@" in line and index + 1 < len(lines) and re.fullmatch(r"\.[A-Za-z]{2,4}", lines[index + 1]):
            line += lines[index + 1]
            index += 1
        joined_lines.append(line)
        index += 1
    email_positions = [(i, match.group(0)) for i, line in enumerate(joined_lines)
                       if (match := re.search(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", line, re.I))]
    previous = 0
    current_section = ""
    section_terms = ("專任教師", "退休教授", "榮譽講座", "合聘教師", "兼任教師", "實務教師")
    blocked_names = {
        "資工系", "資安所", "主任兼", "副系主任", "所長", "職稱", "姓名", "畢業學校",
        "專長", "辦公室", "分機", "台達", "炯朗", "清華", "大學", "學院", "博士", "碩士",
        "特聘", "助理", "清華講", "特聘講", "資應所", "中研院",
    }
    for position, email in email_positions:
        window = joined_lines[previous:position + 1]
        previous = position + 1
        for line in window:
            if any(term in line for term in section_terms):
                current_section = next(term for term in section_terms if term in line)
        degree_index = next((i for i, line in enumerate(window) if any(
            term in line.casefold() for term in ("博士", "碩士", "ph.d", "phd", "doctor", "master")
        )), -1)
        name = ""
        name_index = -1
        for i, line in enumerate(window):
            role_name = re.search(
                r"(?:教授|講師|實務教師)\s+((?:[\u3400-\u9fff]\s*){2,4})(?=\s|$)",
                line,
            )
            if role_name:
                name, name_index = re.sub(r"\s+", "", role_name.group(1)), i
                break
        search_start = (degree_index - 1) if degree_index >= 0 else (len(window) - 1)
        for i in range(search_start, -1, -1):
            if name:
                break
            candidate = re.sub(r"\s+", "", window[i])
            if (re.fullmatch(r"[\u3400-\u9fff]{2,4}", candidate) and candidate not in blocked_names and
                    not any(word in candidate for word in ("教授", "主任", "所長", "大學", "學院"))):
                name, name_index = candidate, i
                break
        if not name or not _looks_like_name(name):
            continue
        education_parts: list[str] = []
        if degree_index >= 0:
            education_parts = window[name_index:degree_index + 1]
            if education_parts:
                education_parts[0] = clean_text(education_parts[0].split(name, 1)[-1])
                degree_match = re.search(r"(?:博士|碩士|Ph\.?D\.?|Doctor|Master)", education_parts[-1], re.I)
                if degree_match:
                    education_parts[-1] = clean_text(education_parts[-1][:degree_match.end()])
        else:
            education_parts = [line for line in window[name_index + 1:-1] if "大學" in line or "學院" in line]
        education = clean_text(" ".join(education_parts))
        research_parts: list[str] = []
        research_start = degree_index + 1 if degree_index >= 0 else name_index + 1
        if degree_index >= 0 and degree_index < len(window):
            degree_line = window[degree_index]
            degree_tail = re.split(r"(?:博士|碩士|Ph\.?D\.?|Doctor|Master)", degree_line, maxsplit=1, flags=re.I)
            if len(degree_tail) == 2 and clean_text(degree_tail[1]):
                research_parts.append(clean_text(degree_tail[1]))
        for line in window[research_start:-1]:
            if (re.fullmatch(r"[\d\s~\-]+", line) or line in {"台達", "炯朗"} or
                    re.match(r"^(?:台達|炯朗)\s*\d", line)):
                break
            if (line not in {"職稱 姓名 畢業學校 專長 辦公室 分機 E-mail"} and
                    not (degree_index < 0 and ("大學" in line or "學院" in line))):
                research_parts.append(line)
        role_parts = [line for line in window[max(0, name_index - 4):name_index + 1] if any(word in line for word in ("教授", "講座", "專任", "兼任", "合聘", "退休"))]
        output_title = clean_text(" ".join(role_parts)) or current_section or "教師"
        records.append(SourceRecord(
            config.school_id, lang, name_zh=name if lang == "zh" else "", name_en=name if lang == "en" else "",
            titles=unique([output_title, current_section]), education=unique([education]),
            research_interests=unique([clean_text(" ".join(research_parts))]), emails=[email.casefold()],
            research_fields=unique([clean_text(" ".join(research_parts))]),
            listing_urls=[url], stable_ids=[email.casefold()], section=current_section or "PDF faculty table",
        ))
    return records


def collect_school(config: SchoolConfig, source: dict[str, str], options: RunOptions) -> SchoolResult:
    client = HttpClient(options)
    warnings: list[str] = []
    errors: list[str] = []
    visited_pages: list[str] = []
    by_language: dict[str, list[SourceRecord]] = {"zh": [], "en": []}
    seeds = {
        "zh": unique([source.get("url_ch", ""), *config.extra_urls_zh]),
        "en": unique([source.get("url_eng", ""), *config.extra_urls_en]),
    }
    for lang, language_seeds in seeds.items():
        json_urls = config.json_urls_zh if lang == "zh" else config.json_urls_en
        for json_url in unique(json_urls):
            if not host_allowed(json_url, config.allowed_hosts):
                errors.append(f"json {json_url}: source host is not allowed")
                continue
            try:
                payload = json.loads(str(client.get(json_url)))
                by_language[lang].extend(_json_people(payload, config, lang, json_url))
                visited_pages.append(json_url)
            except Exception as exc:
                errors.append(f"json {json_url}: {exc}")
        post_urls = config.post_urls_zh if lang == "zh" else config.post_urls_en
        referer = next((url for url in language_seeds if url), "")
        for post_url in unique(post_urls):
            if not host_allowed(post_url, config.allowed_hosts):
                errors.append(f"post {post_url}: source host is not allowed")
                continue
            try:
                html = client.post(post_url, referer=referer)
                by_language[lang].extend(extract_records_from_html(html, post_url, lang, config))
                visited_pages.append(post_url)
            except Exception as exc:
                errors.append(f"post {post_url}: {exc}")
        queue = deque((url, "listing") for url in language_seeds if url)
        queued = {url for url in language_seeds if url}
        visited_language: set[str] = set()
        profile_queue: list[str] = []
        pdf_queue: list[str] = list(config.pdf_urls_zh if lang == "zh" else config.pdf_urls_en)
        while queue and len(visited_language) < config.max_pages:
            url, kind = queue.popleft()
            if url in visited_language:
                continue
            if not host_allowed(url, config.allowed_hosts):
                warnings.append(f"略過非允許網域：{url}")
                continue
            try:
                html = str(client.get(url))
                payloads: list[Any] = []
                if (config.dynamic and not by_language[lang] and
                        ("{{" in html or len(extract_records_from_html(html, url, lang, config)) == 0)):
                    try:
                        html, payloads = _render_dynamic(url, options)
                    except Exception as exc:
                        warnings.append(f"dynamic {url}: {exc}")
                visited_pages.append(url)
                visited_language.add(url)
                page_records = extract_records_from_html(html, url, lang, config, detail=(kind == "profile"))
                for payload in payloads:
                    page_records.extend(_json_people(payload, config, lang, url))
                by_language[lang].extend(page_records)
                profiles, categories, pdfs = discover_links(html, url, config)
                if config.follow_profiles and kind == "listing":
                    profile_queue.extend(profiles)
                if config.follow_categories and kind == "listing":
                    for link in categories:
                        if link not in queued and len(queued) < config.max_pages:
                            queue.append((link, "listing"))
                            queued.add(link)
                if config.allow_pdf:
                    pdf_queue.extend(pdfs)
            except Exception as exc:
                errors.append(f"listing {url}: {exc}")
        for url in unique(profile_queue)[: config.max_pages]:
            if url in visited_language:
                continue
            try:
                html = str(client.get(url))
                visited_pages.append(url)
                visited_language.add(url)
                details = extract_records_from_html(html, url, lang, config, detail=True)
                for detail in details:
                    best: tuple[int, SourceRecord] | None = None
                    for listing in by_language[lang]:
                        score, _ = _match_score(listing, detail)
                        if normalized_name(listing.name_zh or listing.name_en) == normalized_name(detail.name_zh or detail.name_en):
                            score = max(score, 70)
                        if best is None or score > best[0]:
                            best = (score, listing)
                    if best and best[0] >= 70:
                        merge_detail(best[1], detail)
                    else:
                        by_language[lang].append(detail)
            except Exception as exc:
                warnings.append(f"profile {url}: {exc}")
        if config.allow_pdf and len(by_language[lang]) < 5:
            for pdf_url in unique(pdf_queue):
                try:
                    by_language[lang].extend(_pdf_records(client.get(pdf_url, binary=True), pdf_url, lang, config))
                    visited_pages.append(pdf_url)
                except Exception as exc:
                    warnings.append(f"pdf {pdf_url}: {exc}")

    zh = combine_source_records(by_language["zh"])
    en = combine_source_records(by_language["en"])
    if config.pair_by_role_order and not pair_records_by_role_order(zh, en):
        warnings.append("中英文名單筆數不同，未套用角色與順序配對")
    collected_at = now_iso()
    faculty = merge_languages(config.school_id, zh, en, collected_at)
    if not zh:
        errors.append("中文來源沒有解析出任何師資")
    if not en:
        errors.append("英文來源沒有解析出任何師資")
    if any("{{" in item for item in errors):
        errors.append("動態頁仍包含未渲染模板")
    return SchoolResult(config.school_id, [r.as_dict() for r in zh], [r.as_dict() for r in en], faculty,
                        unique(visited_pages), unique(warnings), unique(errors), collected_at)


FACULTY_COLUMNS = (
    "faculty_id", "school_id", "name_zh", "name_en", "role_groups", "titles_zh", "titles_en",
    "education_zh", "education_en", "research_interests_zh", "research_interests_en",
    "research_fields_zh", "research_fields_en", "research_field_summaries_zh", "research_field_summaries_en",
    "listing_urls_zh", "listing_urls_en", "profile_urls_zh", "profile_urls_en", "personal_urls",
    "emails", "merge_status", "merge_method", "collected_at",
)


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False, dir=path.parent, suffix=".tmp") as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def write_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]], columns: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8-sig", newline="", delete=False, dir=path.parent, suffix=".tmp") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: " | ".join(row.get(key, [])) if isinstance(row.get(key), list) else row.get(key, "") for key in columns})
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def validate_faculty(config: SchoolConfig, faculty: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    ids: set[str] = set()
    for row in faculty:
        faculty_id = row.get("faculty_id", "")
        if not faculty_id or faculty_id in ids:
            issues.append(f"重複或空白 faculty_id：{faculty_id}")
        ids.add(faculty_id)
        if not (row.get("name_zh") or row.get("name_en")):
            issues.append(f"{faculty_id} 缺少姓名")
        if is_pure_admin(*(row.get("titles_zh", []) + row.get("titles_en", []))):
            issues.append(f"{faculty_id} 疑似純行政人員")
        for key in ("listing_urls_zh", "listing_urls_en", "profile_urls_zh", "profile_urls_en"):
            for url in row.get(key, []):
                if not host_allowed(url, config.allowed_hosts):
                    issues.append(f"{faculty_id} 的 {key} 超出允許網域：{url}")
    return unique(issues)


def write_school_data(result: SchoolResult, config: SchoolConfig, root: Path, source: dict[str, str]) -> None:
    school_dir = root / "data" / "data-collection" / result.school_id
    write_json(school_dir / "raw" / "zh.json", result.zh_records)
    write_json(school_dir / "raw" / "en.json", result.en_records)
    write_json(school_dir / "faculty.json", result.faculty)
    write_csv(school_dir / "faculty.csv", result.faculty, FACULTY_COLUMNS)
    validation = validate_faculty(config, result.faculty)
    write_json(school_dir / "run.json", {
        "school_id": result.school_id,
        "started_from": {"zh": source.get("url_ch", ""), "en": source.get("url_eng", "")},
        "note": source.get("note", ""),
        "collected_at": result.collected_at,
        "pages": result.pages,
        "counts": {"zh_raw": len(result.zh_records), "en_raw": len(result.en_records), "faculty": len(result.faculty)},
        "warnings": result.warnings,
        "errors": result.errors,
        "validation_issues": validation,
        "success": not result.errors and not validation,
    })


def _difference_rows(faculty: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    fields = (("name", "name_zh", "name_en"), ("titles", "titles_zh", "titles_en"),
              ("education", "education_zh", "education_en"),
              ("research_interests", "research_interests_zh", "research_interests_en"))
    for person in faculty:
        for label, zh_key, en_key in fields:
            zh_value = person.get(zh_key, "")
            en_value = person.get(en_key, "")
            zh_text = " | ".join(zh_value) if isinstance(zh_value, list) else clean_text(zh_value)
            en_text = " | ".join(en_value) if isinstance(en_value, list) else clean_text(en_value)
            if not zh_text and not en_text:
                kind = "missing_both"
            elif not zh_text:
                kind = "missing_zh"
            elif not en_text:
                kind = "missing_en"
            elif normalized_name(zh_text) != normalized_name(en_text):
                kind = "both_present_different"
            else:
                continue
            rows.append({"faculty_id": person["faculty_id"], "field": label, "difference_type": kind,
                         "zh_value": zh_text, "en_value": en_text})
    return rows


def analyze_school(result: SchoolResult, root: Path) -> dict[str, Any]:
    output_dir = root / "analysis" / "data-collection" / result.school_id
    status_counts = Counter(row["merge_status"] for row in result.faculty)
    role_counts = Counter(role for row in result.faculty for role in row["role_groups"])
    total = len(result.faculty)
    def rate(field: str) -> float:
        return round(sum(bool(row.get(field)) for row in result.faculty) / total, 4) if total else 0.0
    report = {
        "school_id": result.school_id,
        "analyzed_at": now_iso(),
        "faculty_count": total,
        "role_counts": dict(sorted(role_counts.items())),
        "merge_status_counts": dict(sorted(status_counts.items())),
        "bilingual_match_rate": round(status_counts.get("matched", 0) / total, 4) if total else 0.0,
        "field_completion_rates": {
            "name_zh": rate("name_zh"), "name_en": rate("name_en"),
            "education_zh": rate("education_zh"), "education_en": rate("education_en"),
            "research_interests_zh": rate("research_interests_zh"),
            "research_interests_en": rate("research_interests_en"),
        },
        "pages_visited": len(result.pages),
        "warnings": result.warnings,
        "errors": result.errors,
    }
    differences = _difference_rows(result.faculty)
    missing: list[dict[str, str]] = []
    for person in result.faculty:
        missing_fields = [field for field in ("name_en", "education_zh", "education_en", "research_interests_zh", "research_interests_en") if not person.get(field)]
        if missing_fields:
            missing.append({"faculty_id": person["faculty_id"], "name_zh": person.get("name_zh", ""),
                            "name_en": person.get("name_en", ""), "missing_fields": " | ".join(missing_fields)})
    write_json(output_dir / "quality-report.json", report)
    write_csv(output_dir / "bilingual-differences.csv", differences,
              ("faculty_id", "field", "difference_type", "zh_value", "en_value"))
    write_csv(output_dir / "missing-fields.csv", missing, ("faculty_id", "name_zh", "name_en", "missing_fields"))
    return report


def write_cross_school_analysis(reports: list[dict[str, Any]], root: Path) -> None:
    output_dir = root / "analysis" / "data-collection"
    rows: list[dict[str, Any]] = []
    for report in sorted(reports, key=lambda x: x["school_id"]):
        rates = report["field_completion_rates"]
        rows.append({
            "school_id": report["school_id"], "faculty_count": report["faculty_count"],
            "bilingual_match_rate": report["bilingual_match_rate"],
            "name_en_rate": rates["name_en"], "education_zh_rate": rates["education_zh"],
            "education_en_rate": rates["education_en"], "research_zh_rate": rates["research_interests_zh"],
            "research_en_rate": rates["research_interests_en"], "pages_visited": report["pages_visited"],
            "warning_count": len(report["warnings"]), "error_count": len(report["errors"]),
        })
    columns = ("school_id", "faculty_count", "bilingual_match_rate", "name_en_rate", "education_zh_rate",
               "education_en_rate", "research_zh_rate", "research_en_rate", "pages_visited", "warning_count", "error_count")
    write_csv(output_dir / "collection-summary.csv", rows, columns)
    total_people = sum(row["faculty_count"] for row in rows)
    failing = [row["school_id"] for row in rows if row["error_count"]]
    lines = ["# 師資資料蒐集報告", "", f"更新時間：{now_iso()}", "", f"系所數：{len(rows)}", f"教師紀錄數：{total_people}", ""]
    if failing:
        lines.extend(["## 需要處理的系所", "", *[f"- {school}" for school in failing], ""])
    lines.extend(["## 各校摘要", "", "| 系所 | 人數 | 雙語配對率 | 警告 | 錯誤 |", "| --- | ---: | ---: | ---: | ---: |"])
    lines.extend(f"| {row['school_id']} | {row['faculty_count']} | {row['bilingual_match_rate']:.1%} | {row['warning_count']} | {row['error_count']} |" for row in rows)
    atomic_text(output_dir / "collection-report.md", "\n".join(lines) + "\n")


def load_collector(path: Path):
    name = "faculty_site_" + hashlib.sha1(str(path).encode()).hexdigest()[:12]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"無法載入 collector：{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not isinstance(getattr(module, "CONFIG", None), SchoolConfig):
        raise RuntimeError(f"{path} 未提供 SchoolConfig CONFIG")
    return module
