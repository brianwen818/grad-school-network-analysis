# 資料說明 / Data dictionary

三個階段的輸出各自放在一個子目錄，後一階段吃前一階段的結果：

```
data-collection/   ←  scripts/data-collection/collect.py      官網原始擷取
data-preprocessing/←  scripts/data-preprocessing/*.ipynb      清洗與標準化
network-analysis/  ←  scripts/network-analysis/current-version/1,2 分類表、節點表、邊表
```

- 資料蒐集日：**2026-09-09**
- 教師紀錄數：**741**（系所層級不跨校去重；合聘教授會出現在多個系所）
- 授權與免責聲明：見 [../LICENSE-data](../LICENSE-data)

> **email 欄位已假名化。** 所有信箱都是 `<16 碼 hex>@redacted.invalid` 形式的不可逆 token。
> 同一個原始信箱固定對應同一個 token，因此靠信箱做的比對（合聘去重、系辦共用信箱偵測）
> 結果與原始資料完全一致，但無法還原成真實信箱。

---

## 1. `data-collection/<school_id>/`

14 個系所各一個目錄。`school_id` 為 `nccu-fin`、`ntu-cs-ie`、`nycu-info-mag-fin` 等。

| 檔案 | 內容 |
| --- | --- |
| `raw/zh.json`, `raw/en.json` | 中英文頁面各自的**原始擷取紀錄**，未配對、未清洗。著作權屬各校，僅供查核 |
| `faculty.json` | 中英配對後的雙語紀錄（本階段的正式輸出） |
| `faculty.csv` | 同上，UTF-8 BOM，方便 Excel 直接開 |
| `run.json` | 該次執行的紀錄：`collected_at`、`pages`、`counts`、`errors`、`warnings`、`validation_issues` |

`faculty.json` 每筆的欄位：

| 欄位 | 型別 | 說明 |
| --- | --- | --- |
| `faculty_id` | str | `<school_id>-<中文姓名>-<10 碼 hash>`，本階段的唯一鍵 |
| `school_id` | str | 系所代號 |
| `name_zh` / `name_en` | str | 官網上的中／英文姓名（未清洗，可能含冒號等殘留符號） |
| `role_groups` | list | `full_time` / `adjunct` / `joint` / `chair` / `visiting` / `emeritus` / `project` / `practice` |
| `titles_zh` / `titles_en` | list | 職稱原文 |
| `education_zh` / `education_en` | list | 學歷原文，多半是 `國別 \| 學校 \| 系所 \| 學位 \| 起訖` 這種以 `\|` 分隔的字串 |
| `research_interests_zh` / `_en` | list | 研究領域原文，分隔符號各校不一（`、`／`,`／換行都有） |
| `listing_urls_zh` / `_en` | list | 該筆資料來自哪幾個師資列表頁 |
| `profile_urls_zh` / `_en` | list | 個人頁面網址 |
| `personal_urls` | list | 教師自建的個人／實驗室網站 |
| `emails` | list | **已假名化的 token** |
| `merge_status` | str | `matched`（中英配對成功）／`zh_only`／`en_only` |
| `merge_method` | str | 配對依據：`stable_id`（頁面 ID）／`email`／`name` |
| `collected_at` | str | ISO 8601，含時區 |

## 2. `data-preprocessing/`

| 檔案 | 內容 |
| --- | --- |
| `faculty_standardized.json` / `.csv` | **主資料集**，741 筆，欄位見下表 |
| `standardization_mapping.csv` | 原文 → 標準化值的完整對照表（研究領域、職稱、學校名） |
| `research_interests_standardized_long.csv` | 教師 × 研究領域的 long format，一列一組 |
| `education_standardized_long.csv` | 教師 × 學歷的 long format |
| `titles_standardized_long.csv` | 教師 × 職稱的 long format |
| `manual_review_queue.csv` | 自動規則無法判定、需人工覆核的項目 |

`faculty_standardized.json` 在第 1 階段欄位之上，多了這些（`_standardized_en` = 經字典對映成標準英文詞；
`_union_en` = 中英兩側標準化結果取聯集，分析實際使用的就是 union 欄）：

| 欄位 | 型別 | 覆蓋率 | 說明 |
| --- | --- | --- | --- |
| `professor_name` | str | 100% | 清洗後的姓名，跨階段的顯示名稱 |
| `titles_standardized_en` | list | 99.0% | 標準化職稱，例如 `Associate Professor` |
| `titles_zh_translated_en` | list | 96.2% | 中文職稱翻成英文後再標準化 |
| `titles_union_en` | list | 97.5% | 上面兩者的聯集 |
| `research_interests_standardized_en` | list | 90.5% | 標準化研究領域，例如 `Artificial Intelligence` |
| `research_interests_zh_translated_en` | list | 87.5% | 中文研究領域翻譯後標準化 |
| `research_interests_union_en` | list | **92.5%** | 聯集，**網路分析的輸入** |
| `research_fields_*` | list | — | 與 `research_interests_*` 平行的一組欄位，對應官網另一個「研究領域」欄 |
| `research_field_summaries_*` | null | 0% | 預留欄位，本次蒐集的系所都沒有這個欄 |
| `education_standardized_en` | list | 59.2% | `學位, 系所, 學校` 的字串形式 |
| `education_structured` | list | 59.2% | 拆成 `{degree, field, institution}` 的 dict |
| `education_union_en` | list | 59.2% | 聯集 |
| `preprocessed_at` | str | 100% | 本階段執行時間 |

> 學歷覆蓋率偏低是因為台大資工與台大資料科學學程的官網不提供學歷（該兩系為 0%）。

## 3. `network-analysis/`

| 檔案／目錄 | 內容 |
| --- | --- |
| `research_taxonomy.csv` | 人工編定的三層研究領域分類：`keyword_en, parent_l2, parent_l1, faculty_count, source, note`（170 個領域 → 46 個 L2 → 16 個 L1） |
| `keyword_idf.csv` | 每個領域的全體人數與 IDF 權重：`keyword_en, parent_l2, parent_l1, n_faculty_overall, idf` |
| `person_identity_map.csv` | `faculty_id` → `person_id` 的對映，用來把合聘教授併成一個人：`faculty_id, person_id, school_id, professor_name, name_en, emails, n_records_in_person, n_schools_in_person, person_school_ids, status, match_note` |
| `shared_contact_emails.csv` | 被判定為系辦／聯絡窗口、排除於身分比對之外的信箱 |
| `manual_identity_decisions.csv` | 同名不同人／同人不同名的人工裁定表 |
| `units_manifest.json` | 18 個分析單位（14 系所 + 3 組 + 全體）的定義 |
| `by-school/<school_id>/` | 每個系所一組節點表與邊表 |
| `by-group/<group>/` | `cs`、`ds`、`fin-and-econ` 三組（組內跨校去重） |
| `overall/` | 全體（跨 14 系所去重） |

每個單位目錄底下都是同樣三張表：

| 檔案 | 欄位 |
| --- | --- |
| `professor_nodes.csv` | `node_id, professor_name, name_en, school_ids, role_groups, n_keywords, phd_institution, n_appointments` |
| `keyword_nodes.csv` | `keyword_en, parent_l2, parent_l1, n_faculty_in_unit, n_faculty_overall, idf` |
| `prof_keyword_edges.csv` | `node_id, keyword_en, source` —— 教授–研究領域二分網路的邊 |

邊表的 `source` 欄位標示這條邊來自哪個系所的資料（合聘教授在組／全體層級被併成一個
`node_id`，但每條邊仍記得原本的出處）。`overall/` 另外多一張 `professor_nodes_nodedup.csv`，
是**去重前**的教師節點表，用來核對去重影響了哪些人。
教授網路與研究領域網路都是由這張二分網路投影而成，建構方式見
[../docs/network-analysis-report.md](../docs/network-analysis-report.md)。

---

## 讀取範例

```python
import json
import pandas as pd

with open("data/data-preprocessing/faculty_standardized.json", encoding="utf-8") as fh:
    faculty = json.load(fh)

edges = pd.read_csv("data/network-analysis/overall/prof_keyword_edges.csv")
nodes = pd.read_csv("data/network-analysis/overall/professor_nodes.csv")

import networkx as nx
B = nx.Graph()
B.add_nodes_from(nodes["node_id"], bipartite=0)
B.add_nodes_from(edges["keyword_en"].unique(), bipartite=1)
B.add_edges_from(edges[["node_id", "keyword_en"]].itertuples(index=False, name=None))
print(B)
```

CSV 一律為 UTF-8 **with BOM**（給 Excel 用）；`pandas.read_csv` 會自動處理，
若用其他工具請指定 `utf-8-sig`。
