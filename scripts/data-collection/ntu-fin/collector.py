from collector_core import SchoolConfig, collect_school

CONFIG = SchoolConfig(
    school_id="ntu-fin",
    allowed_hosts=("management.ntu.edu.tw",),
    card_selectors=(".teachers_line_yellow span.mr15", ".faculty-list li", ".faculty-item", ".teacher_list li", ".col_teacher"),
    name_selectors=("a",),
    education_selectors=("#tab2 > .con_title2 + .tx14", "#tab2 .con_title2 + .tx14"),
    research_field_heading_selectors=("#tab1 .con_title2",),
    research_summary_heading_selectors=("#tab1 .con_title2",),
    section_selectors=(".teachers_con1",),
    profile_patterns=(r"/Fin/faculty/", r"/faculty/detail", r"faculty.*fid="),
    category_patterns=(r"/Fin/faculty", r"faculty.*type="),
)


def collect(source, options):
    return collect_school(CONFIG, source, options)
