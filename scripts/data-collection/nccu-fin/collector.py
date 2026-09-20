from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="nccu-fin",
    allowed_hosts=("finance.nccu.edu.tw",),
    extra_urls_zh=(
        "https://finance.nccu.edu.tw/zh_tw/Members/members_2",
    ),
    extra_urls_en=(
        "https://finance.nccu.edu.tw/en/Members/members_2",
    ),
    card_selectors=(".i-member-item", ".member-item", ".faculty-item", ".list-item", ".item"),
    name_selectors=(".member-data-value-name",),
    title_selectors=(".member-data-value-1",),
    research_selectors=(".member-data-value-2",),
    section_selectors=(".i-member-status-title",),
    profile_patterns=(r"/Members/[^/?#]+/[^/?#]+", r"/member/", r"/people/"),
    category_patterns=(r"/Members/members_[123]", r"page_no=", r"part.?time", r"emeritus"),
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
