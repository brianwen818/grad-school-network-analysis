from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="ntu-cs-ie",
    allowed_hosts=("www.csie.ntu.edu.tw",),
    extra_urls_zh=(
        "https://www.csie.ntu.edu.tw/zh_tw/member/joint_appointment",
        "https://www.csie.ntu.edu.tw/zh_tw/member/%E5%85%BC%E4%BB%BB%E5%B8%AB%E8%B3%87",
    ),
    extra_urls_en=(
        "https://www.csie.ntu.edu.tw/en/member/joint_appointment",
        "https://www.csie.ntu.edu.tw/en/member/Adjunct",
    ),
    card_selectors=(".i-member-item", ".member-item", ".faculty-item", ".list-item"),
    name_selectors=(".member-data-value-name",),
    title_selectors=(".member-data-value-2",),
    research_selectors=(".member-data-value-7",),
    section_selectors=(".i-member-status-title",),
    profile_patterns=(r"/member/[^/?#]+/[^/?#]+", r"/people/", r"/faculty/"),
    category_patterns=(r"/member/",),
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
