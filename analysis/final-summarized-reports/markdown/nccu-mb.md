# 政治大學金融學系（`nccu-mb`）研究結果總結報告

所屬分組：財金與經濟組（fin-and-econ）　｜　資料日期：2026-09-09 蒐集、2026-09-10 完成網路分析

> **本報告的資料來源**
> 本專案分三個階段：(1) 資料蒐集（`scripts/data-collection/`）從 14 個系所官網爬取師資的姓名、職稱、學歷與研究領域，中英文分開蒐集後配對；
> (2) 資料預處理（`scripts/data-preprocessing/`）把職稱、學歷、研究領域標準化成英文 canonical 值，並產生描述統計；
> (3) 網路分析（`scripts/network-analysis/current-version/`）建立「教授–研究領域」二分網路，投影成研究領域網路與教授網路，做社群偵測、中心性、虛無模型與敏感度分析。
> 本報告所有數字、表格與圖表都取自 `analysis/` 底下這三個階段的輸出，每張圖表下方都標明出處與建構方式，附錄另有完整清單。
> 「研究集群」指教授網路的 Louvain 社群；「重要老師」依教授在該網路中的 degree（與多少同儕共享領域）與 betweenness（是否位於集群之間的橋梁位置）判定，**不是**學術成就的排名。

## 1. 科系速覽

政大金融系的研究輪廓以**銀行與金融機構、風險管理、金融工程與精算**為主，是 14 個系所中最偏「銀行／風險」而非「公司理財」的財金科系。官網 22 位師資中專任 17 位、兼任 8 位、名譽 2 位，研究領域完整率 81.8%，有 4 位缺研究領域而未進入網路。Banking and Financial Institutions（6 人）與 Risk Management（5 人）是最多人研究的領域，Econometrics（4 人）與 Asset Pricing（3 人）構成另一條計量軸線。

### 1.1 基本資料

| 項目 | 數值 |
| --- | --- |
| 官網師資人數（canonical 紀錄） | 22 |
| 職稱分類（一人可屬多類） | 專任 17、兼任 8、名譽／退休 2、專案 2 |
| 中英文紀錄配對率 | 100.0% |
| 研究領域完整率（標準化後） | 81.8% |
| 學歷完整率（標準化後） | 90.9% |
| 每位教授平均研究領域數 | 2.00 |
| 進入網路分析的教授數 | 18（4 位因無研究領域排除） |

*出處：`analysis/data-collection/nccu-mb/quality-report.json`（人數、職稱、配對率）、`analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv`（完整率）、`analysis/network-analysis/nccu-mb/network_metrics.json`（進入網路人數）*  
*建構方式：quality-report 由 `scripts/data-collection/collect.py` 在爬取官網後統計 canonical 紀錄的職稱分類與中英配對；coverage 由 `1_faculty_data_preprocessing.ipynb` 計算標準化後有 canonical 值的教師比例。*

### 1.2 主要研究領域

| 排名 | 研究領域（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | Banking and Financial Institutions | 6 |
| 2 | Risk Management | 5 |
| 3 | Econometrics | 4 |
| 4 | Asset Pricing | 3 |
| 5 | Financial Engineering | 3 |
| 6 | Financial Markets | 3 |
| 7 | Financial Derivatives | 2 |
| 8 | Actuarial Science | 2 |
| 9 | International Finance | 2 |
| 10 | Macroeconomics | 1 |
| 11 | Behavioral Finance | 1 |
| 12 | Investments | 1 |
| 13 | Financial Management | 1 |
| 14 | Labor Economics | 1 |
| 15 | Accounting | 1 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/research_fields/fin-and-econ.csv`（`nccu-mb` 欄）*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

![政治大學金融學系 研究領域人數](../descriptive-stats-after-preprocessing/by_department/top_research_fields/nccu-mb.png)

*圖：政治大學金融學系 研究領域人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_research_fields/nccu-mb.png`*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

### 1.3 博士畢業學校

| 排名 | 博士畢業學校（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | National Taiwan University | 2 |
| 2 | National Chengchi University | 2 |
| 3 | University of Chicago | 1 |
| 4 | University of California, Los Angeles | 1 |
| 5 | Harvard University | 1 |
| 6 | Brown University | 1 |
| 7 | Nanyang Technological University | 1 |
| 8 | Stony Brook University | 1 |
| 9 | University of Hong Kong | 1 |
| 10 | University of Minnesota | 1 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/phd_institutions/fin-and-econ.csv`（`nccu-mb` 欄）*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

![政治大學金融學系 博士畢業學校人數](../descriptive-stats-after-preprocessing/by_department/top_phd_institutions/nccu-mb.png)

*圖：政治大學金融學系 博士畢業學校人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_phd_institutions/nccu-mb.png`*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

## 2. 研究領域網路結構

### 2.1 網路指標

| 指標 | 數值 | 說明 |
| --- | --- | --- |
| 二分網路：教授數 / 領域數 / 邊數 | 18 / 23 / 44 | 一條邊 = 一位教授研究一個領域 |
| 二分網路連通元件數 | 3 | 最大元件涵蓋 88.9% 教授 |
| 每位教授平均 / 最多領域數 | 2.44 / 6 |  |
| 研究領域網路：節點 / 邊 | 19 / 41 | 只含至少與一個其他領域共現的領域 |
| 研究領域網路密度 | 0.240 | 實際邊數 ÷ 可能邊數 |
| 研究領域網路平均 degree | 4.32 |  |
| 研究領域網路 modularity Q（Louvain） | 0.289 | 4 個社群；resolution 0.7 / 1.3 時為 3 / 4 個 |
| 領域社群 vs taxonomy L1 一致度 | NMI 0.500 / ARI 0.286 | 1 = 完全一致，0 = 無關 |
| 教授網路：節點 / 邊 | 16 / 49 | 只含最大連通元件 |
| 教授網路密度 | 0.408 |  |
| 教授網路 modularity Q（Louvain） | 0.226 | 2 個集群 |
| 教授集群 vs 主導 L1 一致度 | NMI 0.483 / ARI 0.388 |  |

*出處：`analysis/network-analysis/nccu-mb/network_metrics.json`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

![政治大學金融學系 教授–研究領域二分網路](../network-analysis/nccu-mb/figures/01_bipartite_network.png)

*圖：政治大學金融學系 教授–研究領域二分網路*  
*出處：`analysis/network-analysis/nccu-mb/figures/01_bipartite_network.png`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。圖中兩類節點以不同顏色區分，節點大小與 degree 成正比；邊數超過 400 時繪圖使用 disparity filter backbone（α = 0.05），指標仍以完整圖計算。*

### 2.2 關鍵研究領域

| 研究領域 | Degree | Degree centrality | Betweenness | PageRank | 教授數 | taxonomy L1 |
| --- | --- | --- | --- | --- | --- | --- |
| Banking and Financial Institutions | 11 | 0.611 | 0.297 | 0.1244 | 6 | Financial Engineering & Risk |
| Risk Management | 10 | 0.556 | 0.277 | 0.1274 | 5 | Financial Engineering & Risk |
| Econometrics | 8 | 0.444 | 0.329 | 0.0791 | 4 | Economics & Policy |
| Financial Engineering | 6 | 0.333 | 0.000 | 0.0695 | 3 | Financial Engineering & Risk |
| Actuarial Science | 6 | 0.333 | 0.017 | 0.0629 | 2 | Financial Engineering & Risk |
| Financial Derivatives | 5 | 0.278 | 0.000 | 0.0533 | 2 | Financial Engineering & Risk |
| International Finance | 5 | 0.278 | 0.142 | 0.0500 | 2 | Asset Pricing & Financial Markets |
| Market Microstructure | 4 | 0.222 | 0.000 | 0.0394 | 1 | Asset Pricing & Financial Markets |
| Financial Markets | 4 | 0.222 | 0.307 | 0.0748 | 3 | Asset Pricing & Financial Markets |
| Corporate Governance | 4 | 0.222 | 0.000 | 0.0394 | 1 | Corporate Finance & Governance |
| Behavioral Finance | 4 | 0.222 | 0.000 | 0.0394 | 1 | Asset Pricing & Financial Markets |
| Asset Pricing | 3 | 0.167 | 0.366 | 0.0407 | 3 | Asset Pricing & Financial Markets |

Betweenness 最高的五個領域：Asset Pricing（0.37）、Econometrics（0.33）、Financial Markets（0.31）、Banking and Financial Institutions（0.30）、Risk Management（0.28）。Betweenness 高代表該領域位於不同主題群之間的連結位置，是系上跨主題的共同語言。

*出處：`analysis/network-analysis/nccu-mb/keyword_centrality.csv`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。 degree 為相連領域數，betweenness 為經過該節點的最短路徑比例，PageRank 為加權隨機漫步的穩態機率；parent_l1 來自 `1_build_taxonomy.ipynb` 手工編定的三層 taxonomy（170 個 L3、46 個 L2、16 個 L1）。*

![政治大學金融學系 研究領域教授人數長條圖](../network-analysis/nccu-mb/figures/10_top_keywords_bar.png)

*圖：政治大學金融學系 研究領域教授人數長條圖*  
*出處：`analysis/network-analysis/nccu-mb/figures/10_top_keywords_bar.png`*  
*建構方式：以二分網路中每個領域節點的 degree（研究該領域的教授數）排序繪製。*

### 2.3 研究領域社群

| 社群 | 領域數 | 主要領域（教授人數） | 主要 taxonomy L1（領域數） |
| --- | --- | --- | --- |
| 0 | 6 | Banking and Financial Institutions（6）、Behavioral Finance（1）、Corporate Governance（1）、Market Microstructure（1）、Financial Management（1）、Investments（1） | Asset Pricing & Financial Markets 3、Corporate Finance & Governance 2、Financial Engineering & Risk 1 |
| 1 | 5 | Risk Management（5）、Financial Engineering（3）、Actuarial Science（2）、Financial Derivatives（2）、Sustainable Finance（1） | Financial Engineering & Risk 5 |
| 2 | 4 | Econometrics（4）、Asset Pricing（3）、International Finance（2）、Labor Economics（1） | Economics & Policy 2、Asset Pricing & Financial Markets 2 |
| 3 | 4 | Financial Markets（3）、Accounting（1）、Machine Learning（1）、Macroeconomics（1） | Asset Pricing & Financial Markets 1、Corporate Finance & Governance 1、AI & Machine Learning 1 |

*出處：`analysis/network-analysis/nccu-mb/keyword_communities.csv`（`community` 欄）、`keyword_centrality.csv`（教授人數）*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。*

![政治大學金融學系 研究領域網路的 Louvain 社群](../network-analysis/nccu-mb/figures/05_keyword_network_communities.png)

*圖：政治大學金融學系 研究領域網路的 Louvain 社群*  
*出處：`analysis/network-analysis/nccu-mb/figures/05_keyword_network_communities.png`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。節點顏色為社群，大小與 degree 成正比。*

![政治大學金融學系 各研究領域社群的 taxonomy L1 組成](../network-analysis/nccu-mb/figures/14_community_composition.png)

*圖：政治大學金融學系 各研究領域社群的 taxonomy L1 組成*  
*出處：`analysis/network-analysis/nccu-mb/figures/14_community_composition.png`*  
*建構方式：把每個 Louvain 領域社群內的領域依 taxonomy L1 分類計數，堆疊長條圖。用來檢查資料驅動的社群是否對應人工分類。*

![政治大學金融學系 研究領域共現熱圖](../network-analysis/nccu-mb/figures/13_keyword_cooccurrence_heatmap.png)

*圖：政治大學金融學系 研究領域共現熱圖*  
*出處：`analysis/network-analysis/nccu-mb/figures/13_keyword_cooccurrence_heatmap.png`*  
*建構方式：取研究領域網路的加權鄰接矩陣（共同研究兩領域的教授人數），依社群排序後繪製熱圖。*

## 3. 主要研究集群與重要老師

教授網路只分出 2 個集群，一邊是銀行、風險與金融工程，另一邊是資產訂價與計量經濟。教授網路 clustering 係數顯著高於虛無模型（z = 2.6，p = 0.004），代表教授之間傾向形成緊密的小圈子，而不是均勻連接。

教授網路共 16 位教授、2 個集群（Louvain，Q = 0.226）。以下依集群人數排序；集群編號與圖中的 Community 編號一致。表中 Degree 為與該教授共享研究領域的同儕數，Betweenness 為該教授位於他人最短路徑上的比例（越高越像橋梁）。

![政治大學金融學系 教授網路的 Louvain 集群](../network-analysis/nccu-mb/figures/09_professor_network_communities.png)

*圖：政治大學金融學系 教授網路的 Louvain 集群*  
*出處：`analysis/network-analysis/nccu-mb/figures/09_professor_network_communities.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

### 3.1 集群 0：銀行、風險管理與金融工程集群（9 人）

- **成員共同研究領域**：Banking and Financial Institutions（6 人）、Risk Management（5 人）、Financial Engineering（3 人）、Actuarial Science（2 人）、Financial Derivatives（2 人）、International Finance（1 人）、Financial Management（1 人）
- **成員主導 taxonomy L1**：Financial Engineering & Risk 7 人、Asset Pricing & Financial Markets 2 人

9 位成員中 7 位的主導 taxonomy 為 Financial Engineering & Risk，共享 Banking and Financial Institutions、Risk Management、Financial Engineering、Actuarial Science 與 Financial Derivatives。林士貴的 betweenness（0.348）在全系最高，同時跨精算、銀行、計量與衍生性商品，是把兩個集群連在一起的關鍵人物；林靖庭與廖四郎（兼任）也是重要橋梁，李桐豪、楊曉文則位於集群核心。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 林士貴 | : SHIH-KUEI LIN | 專任 | 11 | 0.348 | Actuarial Science、Banking and Financial Institutions、Econometrics、Financial Derivatives、Financial Engineering |
| 林靖庭 | : CHING-TING LIN | 專任 | 11 | 0.133 | Banking and Financial Institutions、Behavioral Finance、Corporate Governance、Market Microstructure、Risk Management |
| 李桐豪 | : THOMAS LEE | 專任 | 10 | 0.000 | Banking and Financial Institutions、Financial Management、Investments |
| 廖四郎 | : SZU-LANG LIAO | 兼任 | 9 | 0.157 | Banking and Financial Institutions、Financial Engineering、International Finance、Risk Management |
| 楊曉文 | : SHEAUWEN YANG | 專任 | 7 | 0.000 | Actuarial Science、Risk Management、Sustainable Finance |
| 殷乃平 | : NORMAN YIN | 專任 | 6 | 0.000 | Banking and Financial Institutions |
| 陳韋達 |  | 專任 | 6 | 0.000 | Banking and Financial Institutions |
| 陳威光 | : WEI-KUANG CHEN | 專任 | 5 | 0.000 | Financial Derivatives、Risk Management |

其餘成員（1 位，依 degree 排序）：江彌修


### 3.2 集群 1：資產訂價、金融市場與計量集群（7 人）

- **成員共同研究領域**：Financial Markets（3 人）、Asset Pricing（3 人）、Econometrics（3 人）、Macroeconomics（1 人）、International Finance（1 人）、Accounting（1 人）、Machine Learning（1 人）
- **成員主導 taxonomy L1**：Asset Pricing & Financial Markets 4 人、Economics & Policy 2 人、AI & Machine Learning 1 人

共享 Financial Markets、Asset Pricing 與 Econometrics，另含 Macroeconomics、Accounting 等領域。林建秀是集群中心（degree 8、betweenness 0.219），詹育儒次之；羅秉政是系上唯一標記 Machine Learning 的教授，朱浩民為名譽教授。這個集群的內部連結明顯比集群 0 稀疏，成員的研究主題彼此重疊較少。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 林建秀 | : CHIEN-HSIU LIN | 專任 | 8 | 0.219 | Asset Pricing、Econometrics、International Finance |
| 詹育儒 | : Yu-Ju Chan | 專任 | 6 | 0.076 | Asset Pricing、Financial Markets |
| 羅秉政 |  | 專任 | 4 | 0.010 | Accounting、Financial Markets、Machine Learning |
| 朱浩民 | : HAU-MIN CHU | 名譽／退休 | 3 | 0.000 | Financial Markets、Macroeconomics |
| 金帛春 | : BAEK-CHUN KIM | 專任 | 3 | 0.000 | Asset Pricing |
| 陳正暉 | : Zheng-Hui Chen | 專任 | 3 | 0.000 | Econometrics |
| 黃台心 | : TAI-HSIN HUANG | 專任 | 3 | 0.000 | Econometrics、Labor Economics |

*集群表出處：`analysis/network-analysis/nccu-mb/professor_communities.csv`（集群歸屬）、`professor_centrality.csv`（degree、betweenness、職稱類別）、`prof_keyword_network.graphml`（成員研究領域，用來統計集群的共同領域）*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 職稱類別為官網職稱的分類，一人可屬多類時取主要類別；「N 個系所」表示該教授也出現在其他系所名單。*

### 3.3 全系的橋接者與樞紐

Betweenness 最高的教授（跨集群的橋梁）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 林士貴 | : SHIH-KUEI LIN | 專任 | 11 | 0.348 | Financial Engineering & Risk |
| 林建秀 | : CHIEN-HSIU LIN | 專任 | 8 | 0.219 | Asset Pricing & Financial Markets |
| 廖四郎 | : SZU-LANG LIAO | 兼任 | 9 | 0.157 | Financial Engineering & Risk |
| 林靖庭 | : CHING-TING LIN | 專任 | 11 | 0.133 | Asset Pricing & Financial Markets |
| 詹育儒 | : Yu-Ju Chan | 專任 | 6 | 0.076 | Asset Pricing & Financial Markets |
| 羅秉政 |  | 專任 | 4 | 0.010 | AI & Machine Learning |

Degree 最高的教授（與最多同儕共享領域的樞紐）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 林士貴 | : SHIH-KUEI LIN | 專任 | 11 | 0.348 | Financial Engineering & Risk |
| 林靖庭 | : CHING-TING LIN | 專任 | 11 | 0.133 | Asset Pricing & Financial Markets |
| 李桐豪 | : THOMAS LEE | 專任 | 10 | 0.000 | Asset Pricing & Financial Markets |
| 廖四郎 | : SZU-LANG LIAO | 兼任 | 9 | 0.157 | Financial Engineering & Risk |
| 林建秀 | : CHIEN-HSIU LIN | 專任 | 8 | 0.219 | Asset Pricing & Financial Markets |
| 楊曉文 | : SHEAUWEN YANG | 專任 | 7 | 0.000 | Financial Engineering & Risk |

*出處：`analysis/network-analysis/nccu-mb/professor_centrality.csv`*

![政治大學金融學系 教授網路（節點大小 = betweenness）](../network-analysis/nccu-mb/figures/08_professor_network_betweenness.png)

*圖：政治大學金融學系 教授網路（節點大小 = betweenness）*  
*出處：`analysis/network-analysis/nccu-mb/figures/08_professor_network_betweenness.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。此圖節點大小改為與 betweenness 成正比。*

![政治大學金融學系 各集群教授 word cloud（字級 = degree）](../network-analysis/nccu-mb/figures/27_professor_wordcloud_degree_by_community.png)

*圖：政治大學金融學系 各集群教授 word cloud（字級 = degree）*  
*出處：`analysis/network-analysis/nccu-mb/figures/27_professor_wordcloud_degree_by_community.png`*  
*建構方式：依 Louvain 集群分塊、同集群同色的教授姓名 word cloud，字級與 degree 成線性正比並設下限。*

另有 2 位教授雖有研究領域，但與其他教授沒有共享任何領域，孤立於最大連通元件之外，不屬於任何集群。

## 4. 結構穩健性檢驗

### 4.1 虛無模型檢定

| 統計量 | 觀測值 | 虛無平均 | 虛無標準差 | z-score | empirical p | p < 0.05 |
| --- | --- | --- | --- | --- | --- | --- |
| 領域網路密度 | 0.2398 | 0.2759 | 0.0253 | -1.43 | 0.144 | 不顯著 |
| 領域網路 modularity Q | 0.2886 | 0.2959 | 0.0590 | -0.12 | 0.949 | 不顯著 |
| 領域平均共現次數 | 1.1463 | 1.1292 | 0.0552 | 0.31 | 0.865 | 不顯著 |
| 教授網路 clustering 係數 | 0.8261 | 0.6496 | 0.0668 | 2.64 | 0.004 | 顯著 |

*出處：`analysis/network-analysis/nccu-mb/null_model_test.csv`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 密度顯著偏低而 modularity、共現顯著偏高，代表領域共現集中在少數主題群，不是均勻分布。*

![政治大學金融學系 觀測值 vs 虛無模型分布](../network-analysis/nccu-mb/figures/15_null_model_comparison.png)

*圖：政治大學金融學系 觀測值 vs 虛無模型分布*  
*出處：`analysis/network-analysis/nccu-mb/figures/15_null_model_comparison.png`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。*

### 4.2 λ 敏感度

| λ | 邊數 | 密度 | Q | 集群數 | 密度相對 baseline | Q 下降 | 過度合併 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 37 | 0.308 | 0.285 | 2 | +0% | 0.000 | 否 |
| 0.3 | 49 | 0.408 | 0.239 | 2 | +32% | 0.046 | 否 |
| 0.4 | 49 | 0.408 | 0.226 | 2 | +32% | 0.059 | 否 |
| 0.5 | 49 | 0.408 | 0.215 | 3 | +32% | 0.071 | 否 |

*出處：`analysis/network-analysis/nccu-mb/lambda_sensitivity.csv`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

![政治大學金融學系 λ 敏感度](../network-analysis/nccu-mb/figures/16_lambda_sensitivity.png)

*圖：政治大學金融學系 λ 敏感度*  
*出處：`analysis/network-analysis/nccu-mb/figures/16_lambda_sensitivity.png`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

### 4.3 taxonomy L1 覆蓋護欄

| taxonomy L1 | 教授數 | 覆蓋率 | flag |
| --- | --- | --- | --- |
| Financial Engineering & Risk | 9 | 56.2% | too_broad |
| Asset Pricing & Financial Markets | 8 | 50.0% | ok |
| Economics & Policy | 5 | 31.2% | ok |
| Corporate Finance & Governance | 3 | 18.8% | ok |
| AI & Machine Learning | 1 | 6.2% | ok |

*出處：`analysis/network-analysis/nccu-mb/l1_coverage_guardrail.csv`（只列前 8 項）*  
*建構方式：計算每個 L1 分類涵蓋該單位多少比例的教授，超過 50% 標記 too_broad，代表此 L1 在本單位太寬，不能用來做 L1 roll-up 比較。*

## 5. 解讀與注意事項

- L1 護欄標記 Financial Engineering & Risk 涵蓋超過 50% 教授，L1 roll-up 視角在本系不適用。
- λ 敏感度沒有觸發過度合併，λ=0 與 λ=0.4 的社群數都是 2，集群結論穩健。
- 研究領域網路的密度與 modularity 都與虛無模型無顯著差異；只有教授網路的 clustering 顯著。以 19 個領域、18 位教授的規模，這代表主題結構是「小圈子式」而非「模組式」。
- 有 2 位教授不在最大連通元件中，另有 4 位因官網未填研究領域而排除，因此教授網路只有 16 個節點。
- 博士畢業學校分散，台大與政大各 2 人，其餘為美國各校各 1 人。
- 研究領域來自官網自填內容，粒度與深度因人而異；網路密度與集群數反映填寫習慣的成分不可忽視，完整率不可解讀為系所或教授的品質排名。

## 附錄：本報告引用的資料與圖表清單

| 檔案 | 產生階段 / 程式 | 建構方式摘要 |
| --- | --- | --- |
| `analysis/data-collection/nccu-mb/quality-report.json` | 資料蒐集 `scripts/data-collection/collect.py` | 爬取官網後統計 canonical 紀錄人數、職稱分類、中英配對率與欄位完整率 |
| `analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv` | 預處理 `1_faculty_data_preprocessing.ipynb` | 標準化後各欄位有 canonical 值的教師比例與平均項目數 |
| `.../group_comparison/research_fields/fin-and-econ.csv`、`by_department/top_research_fields/nccu-mb.png` | 預處理 `2_rf_and_phd_inst_comparison.ipynb` | 由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。 |
| `.../group_comparison/phd_institutions/fin-and-econ.csv`、`by_department/top_phd_institutions/nccu-mb.png` | 同上 | 同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。 |
| `analysis/network-analysis/nccu-mb/network_metrics.json` | 網路分析 `2_build_network_data.ipynb` + `3_network_analysis.ipynb` | 由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 |
| `analysis/network-analysis/nccu-mb/keyword_centrality.csv`、`keyword_communities.csv` | `3_network_analysis.ipynb` | 研究領域網路的中心性與 Louvain 社群；taxonomy 來自 `1_build_taxonomy.ipynb` |
| `analysis/network-analysis/nccu-mb/professor_centrality.csv`、`professor_communities.csv`、`prof_keyword_network.graphml` | `3_network_analysis.ipynb` | 教授網路的中心性與 Louvain 集群；graphml 為二分網路，本報告用它統計各集群成員的共同領域 |
| `analysis/network-analysis/nccu-mb/null_model_test.csv` | `3_network_analysis.ipynb` | 以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 |
| `analysis/network-analysis/nccu-mb/lambda_sensitivity.csv` | `3_network_analysis.ipynb` | 以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。 |
| `analysis/network-analysis/nccu-mb/l1_coverage_guardrail.csv` | `3_network_analysis.ipynb` | 每個 L1 涵蓋教授比例，> 50% 標記 too_broad |
| `analysis/network-analysis/nccu-mb/figures/01, 05, 08, 09, 10, 13, 14, 15, 16, 27` | `3_network_analysis.ipynb` | 網路圖節點大小與 degree 或 betweenness 成正比、顏色依社群；邊數 > 400 時繪圖用 disparity filter backbone；word cloud 字級與中心性成線性正比 |

更完整的方法說明見 `docs/data-collection-report.md`、`docs/data-preprocessing-report.md`、`docs/network-analysis-report.md`。
