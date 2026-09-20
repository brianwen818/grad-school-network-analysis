from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="ntu-comm-engin-ds-network",
    allowed_hosts=("gice.ntu.edu.tw",),
    card_selectors=("table[width='769']", ".professor", ".teacher", ".faculty", ".member_box"),
    profile_patterns=(r"Professor.*(?:id|sn)=", r"F_.*(?:id|sn)=", r"/faculty/"),
    category_patterns=(r"group=DS", r"Professor_mygice", r"F_mygice"),
    follow_categories=False,
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
