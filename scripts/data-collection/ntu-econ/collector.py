from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="ntu-econ",
    allowed_hosts=("econ.ntu.edu.tw",),
    card_selectors=("article.kt-blocks-post-grid-item", ".faculty_list li", ".teacher-list li", ".member-list li", ".entry-content table tr"),
    name_selectors=(".entry-title",),
    section_selectors=(".wp-block-kadence-advancedheading",),
    profile_patterns=(r"/faculty/", r"/teacher/", r"/archives/\d+"),
    category_patterns=(r"faculty", r"teacher"),
    max_pages=60,
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
