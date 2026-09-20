from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="nthu-qf",
    allowed_hosts=("qf.site.nthu.edu.tw",),
    card_selectors=(".module-ptlist .listBS", ".mcard", ".module-specialist", ".teacher", ".faculty"),
    name_selectors=(".mtitle",),
    profile_patterns=(r"/p/40[456]-1366-", r"/app/index\.php.*member"),
    category_patterns=(r"/p/412-1366-", r"adjunct", r"兼任", r"faculty"),
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
