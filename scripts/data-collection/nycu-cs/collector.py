from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="nycu-cs",
    allowed_hosts=("www.cs.nycu.edu.tw",),
    card_selectors=(".member-card", ".captain-member-card"),
    education_selectors=(".card-body > small", ".member-degree"),
    profile_patterns=(r"/members/detail/",),
    follow_profiles=False,
    follow_categories=False,
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
