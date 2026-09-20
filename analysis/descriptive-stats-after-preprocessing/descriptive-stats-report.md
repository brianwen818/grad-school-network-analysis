# 資料預處理後描述統計

產生時間：2026-09-09T16:29:00+08:00

## 分析範圍

- 教授資料：741 筆
- 研究所／系所：14 個
- Canonical 輸入：`data/data-collection/<school_id>/faculty.json`
- 執行環境：`python (Python 3.12.3)`

## 欄位覆蓋率與詞彙收斂

| field | faculty_with_standardized_value | faculty_total | faculty_coverage_pct | raw_non_noise_values | raw_unique_values | standardized_values | standardized_unique_values | source_entries_mapped_pct | source_entries_requiring_review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| title | 734 | 741 | 99.1 | 1863 | 230 | 1072 | 31 | 94.8 | 99 |
| education | 530 | 741 | 71.5 | 1528 | 1183 | 900 | 367 | 73.5 | 405 |
| research_interest | 662 | 741 | 89.3 | 1315 | 1220 | 1953 | 170 | 63.3 | 1836 |

## 各系所覆蓋率

| school_id | faculty_count | title_coverage_pct | education_coverage_pct | research_interest_coverage_pct | mean_titles_per_faculty | mean_education_entries_per_faculty | mean_research_fields_per_faculty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nccu-fin | 23 | 100.0 | 95.7 | 100.0 | 1.7 | 2.3 | 2.7 |
| nccu-mb | 22 | 90.9 | 90.9 | 81.8 | 1.09 | 2.09 | 2.0 |
| ncku-cs-ie | 62 | 98.4 | 80.6 | 82.3 | 1.13 | 3.21 | 3.05 |
| ncku-stats-ds | 47 | 97.9 | 44.7 | 83.0 | 2.19 | 1.36 | 2.64 |
| nthu-cs | 81 | 100.0 | 100.0 | 93.8 | 1.78 | 1.09 | 2.56 |
| nthu-qf | 19 | 100.0 | 94.7 | 89.5 | 2.0 | 2.47 | 2.37 |
| ntu-comm-engin-ds-network | 25 | 100.0 | 100.0 | 100.0 | 1.0 | 1.24 | 2.96 |
| ntu-cs-ie | 90 | 100.0 | 0.0 | 97.8 | 1.94 | 0.0 | 2.84 |
| ntu-ds | 69 | 100.0 | 0.0 | 85.5 | 1.04 | 0.0 | 2.43 |
| ntu-econ | 49 | 93.9 | 100.0 | 89.8 | 0.96 | 1.12 | 2.04 |
| ntu-fin | 43 | 100.0 | 95.3 | 74.4 | 1.09 | 1.09 | 2.0 |
| ntu-im | 31 | 100.0 | 77.4 | 96.8 | 1.06 | 0.84 | 3.1 |
| nycu-cs | 152 | 100.0 | 99.3 | 92.8 | 1.43 | 1.35 | 2.78 |
| nycu-info-mag-fin | 28 | 100.0 | 100.0 | 67.9 | 1.36 | 1.39 | 2.82 |

## 最常見研究領域

| research_interest_en | faculty_count |
| --- | --- |
| Artificial Intelligence | 109 |
| Machine Learning | 94 |
| Multimedia Systems | 57 |
| Deep Learning | 54 |
| Computer Vision | 54 |
| Algorithms | 49 |
| Image Processing | 40 |
| Information Security | 39 |
| Data Mining | 39 |
| Corporate Finance | 34 |
| Optimization | 33 |
| Computer Networks | 33 |
| Statistics | 32 |
| Embedded Systems | 32 |
| Bioinformatics | 31 |
| Econometrics | 30 |
| Internet of Things | 30 |
| Big Data Analytics | 27 |
| Wireless Networks | 25 |
| Signal Processing | 24 |

## 最常見職稱

| title_en | faculty_count |
| --- | --- |
| Professor | 414 |
| Associate Professor | 108 |
| Assistant Professor | 90 |
| Emeritus Professor | 66 |
| Adjunct Professor | 55 |
| Distinguished Professor | 34 |
| Department Chair | 28 |
| Chair Professor | 28 |
| Jointly Appointed Professor | 27 |
| Adjunct Faculty | 26 |
| Retired Faculty | 24 |
| Research Fellow | 16 |
| Visiting Professor | 16 |
| Joint Faculty | 15 |
| Full-Time Faculty | 15 |
| Adjunct Assistant Professor | 15 |
| Technical Specialist (Professor Rank) | 14 |
| Distinguished Chair Professor | 13 |
| Honorary Chair Professor | 13 |
| Associate Research Fellow | 12 |

## 最常見博士畢業學校

| institution_en | faculty_count |
| --- | --- |
| National Taiwan University | 77 |
| National Chiao Tung University | 42 |
| National Tsing Hua University | 29 |
| University of Illinois Urbana-Champaign | 17 |
| University of California, Los Angeles | 15 |
| National Cheng Kung University | 14 |
| The Ohio State University | 14 |
| University of Wisconsin-Madison | 13 |
| University of Chicago | 13 |
| Northwestern University | 11 |
| University of California, Berkeley | 10 |
| University of Maryland, College Park | 9 |
| University of Southern California | 9 |
| Columbia University | 8 |
| University of Washington | 8 |
| Pennsylvania State University | 7 |
| Texas A&M University | 7 |
| Purdue University | 7 |
| University of Michigan | 7 |
| Cornell University | 6 |

## 主要結果

- 標準化後最常見的研究領域是 `Artificial Intelligence`（109 人），其次是 `Machine Learning`（94 人）。
- 最常見職稱是 `Professor`（414 人）。
- 已成功辨識的博士學歷中，最常見學校是 `National Taiwan University`（77 人）。
- 學歷覆蓋率同時受官網缺值與來源格式影響；本流程只納入能辨識學位且可可靠對應學校的項目，不由任職或工作描述推測學歷。
- 研究資料將主要研究領域與研究領域摘要分開清洗及標準化，最後才合併 canonical 值；摘要中的防詐聲明等非研究內容不納入統計。
- `ntu-cs-ie` 與 `ntu-ds` 的系所官網來源未提供學歷，因此依收集政策維持空白，不使用外部個人網站補值。

## 解讀限制

- 覆蓋率表示該教授至少有一個可靠的標準化值；缺少來源資料不視為 0。
- 同一位教授可有多個職稱、學歷或研究領域，因此類別人次不會加總成教授總數。
- 無法解析或只能部分解析的來源值保留在 `data/data-preprocessing/manual_review_queue.csv`，不會硬猜後納入 canonical 統計。
- 系所間差異同時反映真實師資組成與來源網頁完整度，不宜直接解讀為系所排名。
