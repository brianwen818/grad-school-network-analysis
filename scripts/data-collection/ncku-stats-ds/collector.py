from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="ncku-stats-ds",
    allowed_hosts=("stat.ncku.edu.tw",),
    card_selectors=(".teacher", ".faculty", ".member", ".module-item", ".list-item", "table tr"),
    profile_patterns=(r"task=(?:pageinfo|showcontent|showdetail)",),
    category_patterns=(r"task=showlist", r"page=", r"index=", r"adjunct", r"emeritus", r"joint", r"retired", r"兼任", r"合聘", r"退休"),
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
