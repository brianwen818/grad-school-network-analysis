from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="ntu-ds",
    allowed_hosts=("ds.ntu.edu.tw",),
    json_urls_zh=(
        "https://ds.ntu.edu.tw/fn/getdata_faculty.php?type=core&lang=tw",
        "https://ds.ntu.edu.tw/fn/getdata_faculty.php?type=pt&lang=tw",
        "https://ds.ntu.edu.tw/fn/getdata_faculty.php?type=at&lang=tw",
    ),
    json_urls_en=(
        "https://ds.ntu.edu.tw/fn/getdata_faculty.php?type=core&lang=en",
        "https://ds.ntu.edu.tw/fn/getdata_faculty.php?type=pt&lang=en",
        "https://ds.ntu.edu.tw/fn/getdata_faculty.php?type=at&lang=en",
    ),
    dynamic=True,
    card_selectors=(".faculty-card", ".faculty-list li", ".teacher-card", ".v-card"),
    profile_patterns=(r"/faculty/[^/?#]+$", r"/teacher/", r"/member/"),
    category_patterns=(r"/faculty/(?:core|support|project|adjunct|director)", r"faculty"),
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
