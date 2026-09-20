from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="nycu-info-mag-fin",
    allowed_hosts=("imf.nycu.edu.tw",),
    card_selectors=(".ed_txt", ".module-specialist", ".module-member", ".mcard"),
    name_selectors=("strong",),
    profile_patterns=(r"/app/artwebsite/view", r"/app/index\.php.*action=member", r"/member/", r"/people/"),
    category_patterns=(r"id=(?:21165|5985|5986)", r"folder/\d+", r"faculty", r"teacher", r"member"),
    pair_by_role_order=True,
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
