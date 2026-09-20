# 資料預處理報告

產生時間：2026-09-09T16:29:00+08:00

## 目標與範圍

本流程處理 14 個研究所／系所、共 741 位教授的學歷、研究領域／興趣與職稱。教授姓名優先使用中文，只有缺少中文姓名時才使用英文；其餘三個欄位的 canonical 名稱一律使用英文。

## 執行內容

1. 依 `docs/data-collection-report.md` 載入各系所 canonical `faculty.json`，並確認 `faculty_id` 在全資料中唯一。
2. 完整保留中文與英文原始欄位；研究資料另保留主要研究領域與研究領域摘要的來源欄位，再新增各自的 canonical 結果、聯集候選與結構化學歷。
3. 移除網頁導覽文字、段落標題、空值標記，以及從相鄰網頁區塊誤抓進來的文字。
4. 使用可重現的雙語詞典把可辨識的中文值翻成英文候選；研究領域只以乾淨且等長的中英主要欄位作保守的逐項對齊提示。
5. 主要研究領域與研究領域摘要分別清洗及標準化後再取聯集並去重；主要欄位空白時摘要自然成為資料來源，兩者都有內容時也保留摘要提供的新主題。
6. 合併本質相同的名稱。例如 `AI`、`人工智慧` 統一為 `Artificial Intelligence`；`資產訂價`、`Asset Pricing` 統一為 `Asset Pricing`；`國立台灣大學`、`National Taiwan Univ.` 統一為 `National Taiwan University`；`專任副教授`、`Associate Professor` 統一為 `Associate Professor`。
7. 將學歷解析為學位、科系與學校三個部分，並統一輸出成 `Degree, Field, Institution`。
8. 無法可靠解析或只能部分解析的來源值寫入人工覆核佇列，不自行臆測翻譯。
9. 產生各系所覆蓋率、熱門研究領域、職稱與博士畢業學校等描述統計與圖表。

## 結果

| field | faculty_with_standardized_value | faculty_total | faculty_coverage_pct | raw_non_noise_values | raw_unique_values | standardized_values | standardized_unique_values | source_entries_mapped_pct | source_entries_requiring_review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| title | 734 | 741 | 99.1 | 1863 | 230 | 1072 | 31 | 94.8 | 99 |
| education | 530 | 741 | 71.5 | 1528 | 1183 | 900 | 367 | 73.5 | 405 |
| research_interest | 662 | 741 | 89.3 | 1315 | 1220 | 1953 | 170 | 63.3 | 1836 |

教授層級的標準化覆蓋率為：職稱 99.1%、學歷 71.5%、研究領域／興趣 89.3%。人工覆核佇列共有 2,340 個來源項目，主要是尚未能確定對應的學校／科系、過長自由文字或細分研究主題。`ntu-cs-ie` 與 `ntu-ds` 的學歷依官方來源維持空白。

最常見研究領域為 `Artificial Intelligence`（109 人）與 `Machine Learning`（94 人）；最常見職稱是 `Professor`（414 人）；成功辨識的博士學歷中，`National Taiwan University` 最常見（77 人）。

## 輸出檔案

### 標準化資料

- `data/data-preprocessing/faculty_standardized.json`：完整資料；陣列格式分開保留主要研究領域與研究領域摘要原文、各自 canonical 值、聯集候選、其他翻譯候選與結構化學歷。
- `data/data-preprocessing/faculty_standardized.csv`：UTF-8 with BOM 的平面版本；多值欄位以 ` | ` 分隔。
- `data/data-preprocessing/education_standardized_long.csv`：每列一筆標準化學歷。
- `data/data-preprocessing/research_interests_standardized_long.csv`：每列一個標準化研究領域。
- `data/data-preprocessing/titles_standardized_long.csv`：每列一個標準化職稱。
- `data/data-preprocessing/standardization_mapping.csv`：來源值到 canonical 值的稽核軌跡。
- `data/data-preprocessing/manual_review_queue.csv`：無法解析或只能部分解析的來源項目。

### 描述統計

- `analysis/descriptive-stats-after-preprocessing/descriptive-stats-report.md`
- `analysis/descriptive-stats-after-preprocessing/descriptive_stats.json`
- 各欄位／系所的 CSV 摘要與熱門類別表。
- 欄位覆蓋率、研究領域、職稱與博士畢業學校的 PNG 圖表。

## 重現方式

使用指定的 Python 3.12 環境執行 notebook：

```powershell
python -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 scripts/data-preprocessing/1_faculty_data_preprocessing.ipynb
```

## 限制與覆核建議

- 標準化器採保守策略。canonical 值缺失可能代表來源本來沒有資料、資料被網頁污染，或內容太模糊而無法可靠對應。
- 學歷解析以含學位的項目和已知學校別名為主；證書、博士後經歷與敘事型簡歷不視為學位。
- 研究領域會合併明確同義詞，但不強迫把每個細分主題歸到過寬類別。摘要中的防詐聲明等非研究文字會在標準化時排除，原文仍保留供稽核；若要提高召回率，請優先檢視 `manual_review_queue.csv`。
- 各來源網站的結構與完整度差異很大，覆蓋率不可直接解讀為系所或教授排名。
