from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="ntu-im",
    allowed_hosts=("management.ntu.edu.tw",),
    card_selectors=(".teachers_line_green span.mr15", ".faculty-list li", ".faculty-item", ".teacher_list li", ".col_teacher"),
    name_selectors=("a",),
    education_selectors=("#tab2 > .con_title2 + .tx14", "#tab2 .con_title2 + .tx14"),
    research_selectors=("#tab1 > .con_title2 + .tx14", "#tab1 .con_title2 + .tx14"),
    section_selectors=(".teachers_con1",),
    profile_patterns=(r"/IM/faculty/", r"/faculty/detail", r"faculty.*fid="),
    category_patterns=(r"/IM/faculty", r"faculty.*type="),
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
