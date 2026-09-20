from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="ncku-cs-ie",
    allowed_hosts=("www.csie.ncku.edu.tw",),
    extra_urls_zh=(
        "https://www.csie.ncku.edu.tw/zh-hant/members/joint",
        "https://www.csie.ncku.edu.tw/zh-hant/members/adjunct",
    ),
    extra_urls_en=(
        "https://www.csie.ncku.edu.tw/en/members/joint",
        "https://www.csie.ncku.edu.tw/en/members/adjunct",
    ),
    card_selectors=(".member-list-area .card", ".member-card", ".member-item", ".faculty-item", ".people-card", ".views-row"),
    name_selectors=("h3.card-title", "h4.card-title"),
    title_selectors=(".card-subtitle",),
    profile_patterns=(r"/members/(?:csie|joint|adjunct)/\d+", r"/members/\d+", r"/member/\d+", r"/people/\d+"),
    category_patterns=(r"/members/(?:csie|joint|adjunct)",),
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
