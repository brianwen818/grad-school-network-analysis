from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="nthu-cs",
    allowed_hosts=("dcs.site.nthu.edu.tw", "dcs-en.site.nthu.edu.tw"),
    pdf_urls_zh=("https://dcs.site.nthu.edu.tw/var/file/174/1174/img/641740754.pdf",),
    post_urls_zh=tuple(
        f"https://dcs.site.nthu.edu.tw/app/index.php?Action=mobileloadmod&Type=mobile_rcg_mstr&Nbr={number}"
        for number in (1107, 461, 429, 1108, 430, 465)
    ),
    post_urls_en=tuple(
        f"https://dcs-en.site.nthu.edu.tw/app/index.php?Action=mobileloadmod&Type=mobile_rcg_mstr&Nbr={number}"
        for number in (1110, 674, 661, 1112, 662, 675)
    ),
    dynamic=True,
    allow_pdf=True,
    card_selectors=(".d-item.v-id", ".mcard", ".module-specialist", ".teacher", ".faculty", ".listBS li"),
    profile_patterns=(r"/p/406-1174-", r"/p/404-1174-", r"/p/406-1010-", r"/p/405-1010-"),
    category_patterns=(r"/p/412-(?:1174|1010)-", r"adjunct", r"emeritus", r"joint", r"兼任", r"合聘", r"退休"),
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
