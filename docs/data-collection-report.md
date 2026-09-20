# 研究所師資資料蒐集與結果報告

本報告記錄 `scripts/data-collection` 師資蒐集系統的實作方式，以及 2026-09-09 完整執行 14 個系所後的結果。這裡的「人數」是各系所內的 canonical 師資紀錄數；同一位教師若出現在不同系所，仍會各自保留，不做跨校去重。

## 1. 蒐集目標與範圍

來源清單為 [`data/data-collection/prof_info_page_links.xlsx`](../data/data-collection/prof_info_page_links.xlsx) 的 `工作表1`，系統會讀取每列的學校 ID、中文網址、英文網址及 notes。

蒐集範圍包括系所官網列出的專任、兼任、合聘、客座、講座、名譽、退休、專案、約聘、研究及實務教師等學術人員。純行政人員會排除；若某人同時具有教授與主任、所長等行政職務，仍視為學術人員保留。

只下載系所官網及其站內頁面。外部個人網站、實驗室網站只保存網址，作為來源資訊或雙語配對線索，不下載其內容。中文與英文來源分開蒐集，不自行翻譯、補寫或推測官網未提供的學歷與研究領域。

`ntu-comm-engin-ds` 會映射至 `ntu-comm-engin-ds-network`，避免資料、程式與分析產生兩套目錄。

## 2. 蒐集流程

主要入口是 [`scripts/data-collection/collect.py`](../scripts/data-collection/collect.py)，共用邏輯集中於 [`collector_core.py`](../scripts/data-collection/collector_core.py)，每個系所各有一份只描述網站規則的 `collector.py`。

一次完整執行依序進行下列工作：

1. 讀取 Excel 中的 14 個系所、雙語網址與 notes，並套用學校 ID alias。
2. 中文與英文來源分開處理，追蹤職稱分類頁、分頁和站內個人詳情頁。
3. 靜態 HTML 不足時，優先呼叫頁面本身公開引用的同源 JSON 或 POST 模組；仍無法取得時才使用 Playwright 渲染後 DOM。清大資工另外保留系所正式 PDF 備援。
4. 正規化空白、Unicode、姓名及網址，排除模板內容、純行政人員與重複來源紀錄。
5. 中文與英文紀錄依下列順序配對：站內穩定 ID、email、相同個人頁網址、頁面直接提供的中英姓名、正規化姓名。無法唯一判定時保留為 `zh_only` 或 `en_only`，不強行合併。
6. 以暫存檔寫完後原子替換正式檔，接著產生缺漏、雙語差異、完整率與跨校摘要。

HTTP 請求包含重試、指數退避、逾時與節流。單一頁面失敗不會中止其他頁面或學校，但會寫入該校 `run.json`，並讓總控命令回傳非零狀態。

## 3. 各校網站處理方式

| school_id | 主要蒐集方式 |
| --- | --- |
| `nycu-info-mag-fin` | 讀取中英文專任、合聘與兼任清單，解析相鄰 `span` 或 `strong` 標籤後文字，並追蹤 `artwebsite/view` 站內個人詳情頁；無 email 的雙語別名依官網相同角色與排列順序配對。 |
| `nycu-cs` | 直接解析中英文師資卡片；共用的 `Retired Professors` heading 會套用到後續退休教師卡片，不追蹤外部個人網站。 |
| `ntu-im` | 解析職稱區段清單，再進入臺大管理學院站內個人詳情頁；研究與學歷分別只取 `#tab1`、`#tab2` 的主要內容，避免跨入摘要、經歷、課程及論文。 |
| `ntu-fin` | 解析職稱區段清單，再進入臺大管理學院站內個人詳情頁；研究資料依標題精確讀取 `主要研究領域`／`Research Field` 與 `研究領域摘要`／`Research Field Summary` 的相鄰內容，學歷則取 `#tab2` 主要內容，避免研究欄位跨入學歷、經歷、課程及論文。 |
| `ntu-econ` | 解析文章式師資網格，將系主任、教授、副教授等共用分類套用到後續卡片；遇到 `系辦同仁`／`Staff` 區段即排除其中卡片且不追蹤其個人頁，教師個人頁則由姓名／職稱／研究專長表格讀值並合併。 |
| `ntu-ds` | 依頁面使用的 `getdata_faculty.php` 同源 JSON 端點讀取核心、專案及兼任分類，分別帶入中英文語言參數；保留 Playwright 備援。 |
| `ntu-cs-ie` | 涵蓋 Faculty、合聘及兼任分類，並追蹤站內個人頁。 |
| `ntu-comm-engin-ds-network` | 解析臺大電信所資料科學與網路組的中英文表格。 |
| `nthu-qf` | 中英文共用頁分別解析，追蹤各職稱分類與站內詳情頁。 |
| `nthu-cs` | 呼叫頁面公開引用的 6 個中文及 6 個英文站內 POST 模組，涵蓋主任／副主任、榮譽講座、專任、合聘、兼任及榮譽退休；另有 Playwright 與正式學生手冊 PDF 備援。 |
| `nccu-mb` | 追蹤 Full-time、Part-time、Emeritus 等分類、所有分頁及站內個人頁；學歷由學校／系所／學位表格逐列解析，並排除行政專員。 |
| `nccu-fin` | 讀取 `members_1`、`members_2`、分頁及站內個人頁；學歷由學校／系所／學位表格逐列解析。 |
| `ncku-cs-ie` | 涵蓋專任、合聘及兼任清單，並讀取站內個人詳情。 |
| `ncku-stats-ds` | 追蹤專任、兼任、講座／名譽、合聘／客座及退休分類、分頁與詳情頁；詳情頁以 `.title` 後相鄰 `.txt` 解析 `學歷(Education)` 與研究區塊，並排除「教師／榮譽獎勵」頁面標題。 |

## 4. 資料與分析輸出

每校正式資料位於 `data/data-collection/<school>/`：

- `faculty.json`：雙語合併後的 canonical 紀錄；研究資料保留相容的 `research_interests_zh/en` 聯集，並另以 `research_fields_zh/en`、`research_field_summaries_zh/en` 區分主要研究領域與摘要來源。
- `faculty.csv`：一位教師一列，陣列欄位以 ` | ` 展平。
- `raw/zh.json`、`raw/en.json`：雙語合併前的來源紀錄。
- `run.json`：執行時間、起始來源、notes、造訪頁面、筆數、警告、錯誤及驗證狀態。

每校分析位於 `analysis/data-collection/<school>/`：

- `quality-report.json`：人數、職稱、配對狀態、欄位完整率及執行問題。
- `bilingual-differences.csv`：以 `faculty_id` 記錄中英文缺漏及差異。
- `missing-fields.csv`：缺少英文名、學歷或研究領域的紀錄。

跨校結果為 [`collection-summary.csv`](../analysis/data-collection/collection-summary.csv) 與 [`collection-report.md`](../analysis/data-collection/collection-report.md)。分析檔不會寫入 `data`，其中的 `faculty_id` 均可回指對應學校的 `faculty.json`。

## 5. 本次執行結果

目前結果為 14 校、741 筆 canonical 師資紀錄。`nycu-info-mag-fin`、`ntu-fin` 與 `ntu-econ` 已於 2026-09-09 依修正後邏輯重新蒐集，其餘系所沿用同日完整執行結果；所有學校的 `run.json` 皆為 `success: true`，總警告數、錯誤數及 validation issues 皆為 0。

下表的完整率以 canonical 人數為分母；「中英配對」表示同一筆紀錄同時有中文及英文來源，不代表所有雙語欄位都有內容。

| school_id | 人數 | 中文原始 | 英文原始 | 中英配對 | 英文名 | 中文學歷 | 英文學歷 | 中文研究 | 英文研究 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `nccu-fin` | 23 | 23 | 23 | 100.0% | 87.0% | 95.7% | 95.7% | 100.0% | 69.6% |
| `nccu-mb` | 22 | 22 | 22 | 100.0% | 81.8% | 90.9% | 90.9% | 90.9% | 68.2% |
| `ncku-cs-ie` | 62 | 62 | 62 | 100.0% | 100.0% | 80.7% | 100.0% | 95.2% | 90.3% |
| `ncku-stats-ds` | 47 | 40 | 36 | 61.7% | 76.6% | 44.7% | 42.6% | 68.1% | 68.1% |
| `nthu-cs` | 81 | 78 | 64 | 75.3% | 79.0% | 96.3% | 79.0% | 96.3% | 79.0% |
| `nthu-qf` | 19 | 19 | 19 | 100.0% | 10.5% | 94.7% | 94.7% | 94.7% | 94.7% |
| `ntu-comm-engin-ds-network` | 25 | 25 | 25 | 100.0% | 100.0% | 100.0% | 92.0% | 100.0% | 100.0% |
| `ntu-cs-ie` | 90 | 90 | 88 | 97.8% | 100.0% | 0.0% | 0.0% | 100.0% | 97.8% |
| `ntu-ds` | 69 | 69 | 69 | 100.0% | 100.0% | 0.0% | 0.0% | 94.2% | 23.2% |
| `ntu-econ` | 49 | 42 | 45 | 77.5% | 91.8% | 85.7% | 81.6% | 85.7% | 83.7% |
| `ntu-fin` | 43 | 43 | 43 | 100.0% | 100.0% | 100.0% | 100.0% | 76.7% | 74.4% |
| `ntu-im` | 31 | 31 | 31 | 100.0% | 100.0% | 100.0% | 100.0% | 96.8% | 96.8% |
| `nycu-cs` | 152 | 152 | 152 | 100.0% | 100.0% | 100.0% | 100.0% | 99.3% | 99.3% |
| `nycu-info-mag-fin` | 28 | 28 | 28 | 100.0% | 100.0% | 100.0% | 96.4% | 67.9% | 64.3% |

### 結果解讀

- 配對率較低不等於抓取失敗。例如清大資工與成大統計的中英文官網名單本身並不完全相同，因此未能唯一配對者按規則保留為單語紀錄。
- 清大量化財務使用中英文共用頁；雖然來源紀錄可配對，多數教師沒有官網提供的英文姓名，因此英文名完整率只有 10.5%。
- 臺大資工及臺大資料科學的來源頁未提供學歷，所以學歷完整率為 0%。系統刻意不從外部網站補資料，也不推測學位。
- 臺大資料科學 API 中部分 `ei_research_en` 為空，即使中文或共用研究欄位存在，英文研究完整率仍只依英文原文計算。
- 目前 741 筆包含 `nycu-info-mag-fin` 28 人、`nccu-mb` 22 人、`ncku-stats-ds` 47 人與 `ntu-econ` 49 人。NYCU 資財系的「系所成員」頁面標題、成大統計的「教師／榮譽獎勵」頁面標題假紀錄，以及臺大經濟中英文官網各 8 筆系辦同仁資料均已排除；臺大經濟中英文姓名無法唯一配對時仍依保守規則保留單語紀錄。
- 欄位修正後，NCCU 兩系不再出現 `education=["s"]` 或 `經歷 榮譽`；成大統計英文學歷原文完整率為 42.6%；排除系辦同仁後，臺大經濟研究原文完整率為 85.7%／83.7%；NYCU 資工所有 152 人均有職稱來源。
- 臺大財金現在同時蒐集主要研究領域與研究領域摘要，中文／英文研究完整率為 76.7%／74.4%；例如顏廣杰的中文主要研究領域空白，但其研究領域摘要已保留。臺大資管仍只讀取研究欄位，不把摘要、學歷、經歷、課程或論文併入研究資料，研究完整率為 96.8%／96.8%。
- 一位教師可以同時屬於多個 `role_groups`，例如 `full_time` 與 `chair`，因此各職稱計數相加可能大於該校總人數。
- NYCU 資財系專任師資 15 人的中英文研究領域均已完整取得；全體 28 人的研究完整率為 67.9%／64.3%，剩餘缺漏來自合聘或兼任清單原文本身未填研究專長。該校中英文名單人數與角色順序一致，無 email 的中英文別名據此配對；若未來兩邊筆數不同，系統會停止套用順序配對並寫入警告。

## 6. 驗證與測試

本次驗收完成以下檢查：

- 14 個 collector 均能載入，且與 Excel 中的 14 個 canonical school ID 一致。
- 所有 `faculty.json` 符合預定欄位結構，`faculty_id` 在校內唯一。
- `faculty.csv` 與 `faculty.json` 人數一致。
- 正式資料的 listing/profile URL 都屬於各校允許網域。
- 沒有被規則判定為純行政人員的正式紀錄。
- 分析 CSV 中的每個 `faculty_id` 都存在於對應 `faculty.json`。
- 跨校摘要包含 14 校，總人數與各校正式資料相符。
- 23 項本機測試通過，另有 1 項需明確啟用的 14 校官方頁面 live smoke test 預設略過；本次另以正式 collector 完整重跑 `ntu-fin` 與 `ntu-econ`，兩校皆成功且無警告、錯誤或 validation issues。

測試 fixture 位於 `scripts/data-collection/tests/fixtures/site_cases.json`，涵蓋全部 14 個 collector。測試內容包括姓名正規化、職稱分類、行政區段排除且不追蹤其個人頁、教授兼行政職保留、雙語配對、歧義姓名不強制配對、來源網域限制、模板頁排除、`Degrees` 頁籤、學歷表格、標題與相鄰內容、共用職稱 heading、表格型個人頁、管理學院主要研究領域與研究領域摘要 tabs、退休教授空職稱，以及資料與分析目錄分離。

## 7. 重跑方式

安裝一般相依套件：

```powershell
python -m pip install -r scripts/data-collection/requirements.txt
```

執行全部學校或單一學校：

```powershell
python scripts/data-collection/collect.py --school all
python scripts/data-collection/collect.py --school ntu-fin
python scripts/data-collection/collect.py --school ntu-comm-engin-ds
```

其他選項：

- `--skip-analysis`：只更新正式與原始資料，不重建分析。
- `--dry-run`：只顯示將處理的來源，不連線、不寫檔。
- `--headed`：Playwright 備援時顯示瀏覽器。
- `--insecure`：僅在受控網路造成 TLS 憑證鏈驗證失敗時暫用；一般環境不建議使用。

需要瀏覽器備援時再安裝：

```powershell
python -m pip install -r scripts/data-collection/requirements-browser.txt
python -m playwright install chromium
```

執行測試：

```powershell
python -m unittest discover -s scripts/data-collection/tests -v
```

網站內容、分類與版型可能日後變更。每次重新蒐集後應先檢查 `run.json`，再查看 `analysis/data-collection/collection-report.md`、各校缺漏清單及雙語差異清單。
