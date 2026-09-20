from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="nccu-mb",
    allowed_hosts=("banking.nccu.edu.tw",),
    card_selectors=(".i-member-item", ".member-item", ".faculty-item", ".list-item", ".item"),
    name_selectors=(".member-data-value-name",),
    title_selectors=(".member-data-value-1",),
    research_selectors=(".member-data-value-2",),
    section_selectors=(".i-member-status-title",),
    profile_patterns=(r"/Members/[^/?#]+/[^/?#]+", r"/member/", r"/people/"),
    category_patterns=(r"/Members", r"page_no=", r"full.?time", r"part.?time", r"retired", r"emeritus"),
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
