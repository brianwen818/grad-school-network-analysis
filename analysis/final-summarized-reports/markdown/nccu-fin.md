# 政治大學財務管理學系（`nccu-fin`）研究結果總結報告

所屬分組：財金與經濟組（fin-and-econ）　｜　資料日期：2026-09-09 蒐集、2026-09-10 完成網路分析

> **本報告的資料來源**
> 本專案分三個階段：(1) 資料蒐集（`scripts/data-collection/`）從 14 個系所官網爬取師資的姓名、職稱、學歷與研究領域，中英文分開蒐集後配對；
> (2) 資料預處理（`scripts/data-preprocessing/`）把職稱、學歷、研究領域標準化成英文 canonical 值，並產生描述統計；
> (3) 網路分析（`scripts/network-analysis/current-version/`）建立「教授–研究領域」二分網路，投影成研究領域網路與教授網路，做社群偵測、中心性、虛無模型與敏感度分析。
> 本報告所有數字、表格與圖表都取自 `analysis/` 底下這三個階段的輸出，每張圖表下方都標明出處與建構方式，附錄另有完整清單。
> 「研究集群」指教授網路的 Louvain 社群；「重要老師」依教授在該網路中的 degree（與多少同儕共享領域）與 betweenness（是否位於集群之間的橋梁位置）判定，**不是**學術成就的排名。

## 1. 科系速覽

政大財管系是一個以**公司理財、投資與財務管理**為核心的傳統財金科系。官網 23 位師資中，專任 14 位、兼任 11 位，另有 10 位身兼行政主管職務。研究領域資料完整率 100%，是 14 個系所中資料最齊全的單位之一，因此網路分析結果不受缺漏影響。系上研究主題集中在 Corporate Finance、Financial Management、Investments 與 Risk Management 四個大項，沒有資訊技術或計量方法類的領域，屬於純財務的研究輪廓。

### 1.1 基本資料

| 項目 | 數值 |
| --- | --- |
| 官網師資人數（canonical 紀錄） | 23 |
| 職稱分類（一人可屬多類） | 專任 14、兼任 11、主管／講座 10、名譽／退休 1、教師（未細分） 1 |
| 中英文紀錄配對率 | 100.0% |
| 研究領域完整率（標準化後） | 100.0% |
| 學歷完整率（標準化後） | 95.7% |
| 每位教授平均研究領域數 | 2.70 |
| 進入網路分析的教授數 | 23（0 位因無研究領域排除） |

*出處：`analysis/data-collection/nccu-fin/quality-report.json`（人數、職稱、配對率）、`analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv`（完整率）、`analysis/network-analysis/nccu-fin/network_metrics.json`（進入網路人數）*  
*建構方式：quality-report 由 `scripts/data-collection/collect.py` 在爬取官網後統計 canonical 紀錄的職稱分類與中英配對；coverage 由 `1_faculty_data_preprocessing.ipynb` 計算標準化後有 canonical 值的教師比例。*

### 1.2 主要研究領域

| 排名 | 研究領域（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | Corporate Finance | 9 |
| 2 | Financial Management | 8 |
| 3 | Investments | 6 |
| 4 | Risk Management | 5 |
| 5 | Corporate Governance | 4 |
| 6 | Asset Pricing | 4 |
| 7 | Financial Markets | 3 |
| 8 | International Finance | 3 |
| 9 | Market Microstructure | 3 |
| 10 | Behavioral Finance | 2 |
| 11 | Mergers and Acquisitions | 2 |
| 12 | Real Estate Finance | 1 |
| 13 | Portfolio Management | 1 |
| 14 | Personal Finance | 1 |
| 15 | Interest Rate Modeling | 1 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/research_fields/fin-and-econ.csv`（`nccu-fin` 欄）*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

![政治大學財務管理學系 研究領域人數](../descriptive-stats-after-preprocessing/by_department/top_research_fields/nccu-fin.png)

*圖：政治大學財務管理學系 研究領域人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_research_fields/nccu-fin.png`*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

### 1.3 博士畢業學校

| 排名 | 博士畢業學校（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | Nanyang Technological University | 2 |
| 2 | Indiana University | 2 |
| 3 | National Taiwan University | 1 |
| 4 | University of Iowa | 1 |
| 5 | Oklahoma State University | 1 |
| 6 | Mississippi State University | 1 |
| 7 | Louisiana State University | 1 |
| 8 | Iowa State University | 1 |
| 9 | Cornell University | 1 |
| 10 | University of Warwick | 1 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/phd_institutions/fin-and-econ.csv`（`nccu-fin` 欄）*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

![政治大學財務管理學系 博士畢業學校人數](../descriptive-stats-after-preprocessing/by_department/top_phd_institutions/nccu-fin.png)

*圖：政治大學財務管理學系 博士畢業學校人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_phd_institutions/nccu-fin.png`*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

## 2. 研究領域網路結構

### 2.1 網路指標

| 指標 | 數值 | 說明 |
| --- | --- | --- |
| 二分網路：教授數 / 領域數 / 邊數 | 23 / 24 / 62 | 一條邊 = 一位教授研究一個領域 |
| 二分網路連通元件數 | 3 | 最大元件涵蓋 91.3% 教授 |
| 每位教授平均 / 最多領域數 | 2.70 / 5 |  |
| 研究領域網路：節點 / 邊 | 22 / 51 | 只含至少與一個其他領域共現的領域 |
| 研究領域網路密度 | 0.221 | 實際邊數 ÷ 可能邊數 |
| 研究領域網路平均 degree | 4.64 |  |
| 研究領域網路 modularity Q（Louvain） | 0.276 | 4 個社群；resolution 0.7 / 1.3 時為 3 / 5 個 |
| 領域社群 vs taxonomy L1 一致度 | NMI 0.353 / ARI 0.124 | 1 = 完全一致，0 = 無關 |
| 教授網路：節點 / 邊 | 21 / 159 | 只含最大連通元件 |
| 教授網路密度 | 0.757 |  |
| 教授網路 modularity Q（Louvain） | 0.123 | 3 個集群 |
| 教授集群 vs 主導 L1 一致度 | NMI 0.458 / ARI 0.287 |  |

*出處：`analysis/network-analysis/nccu-fin/network_metrics.json`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

![政治大學財務管理學系 教授–研究領域二分網路](../network-analysis/nccu-fin/figures/01_bipartite_network.png)

*圖：政治大學財務管理學系 教授–研究領域二分網路*  
*出處：`analysis/network-analysis/nccu-fin/figures/01_bipartite_network.png`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。圖中兩類節點以不同顏色區分，節點大小與 degree 成正比；邊數超過 400 時繪圖使用 disparity filter backbone（α = 0.05），指標仍以完整圖計算。*

### 2.2 關鍵研究領域

| 研究領域 | Degree | Degree centrality | Betweenness | PageRank | 教授數 | taxonomy L1 |
| --- | --- | --- | --- | --- | --- | --- |
| Financial Management | 12 | 0.571 | 0.342 | 0.1188 | 8 | Corporate Finance & Governance |
| Risk Management | 10 | 0.476 | 0.269 | 0.0993 | 5 | Financial Engineering & Risk |
| Corporate Finance | 10 | 0.476 | 0.254 | 0.1081 | 9 | Corporate Finance & Governance |
| Investments | 9 | 0.429 | 0.364 | 0.1014 | 6 | Asset Pricing & Financial Markets |
| Asset Pricing | 6 | 0.286 | 0.186 | 0.0559 | 4 | Asset Pricing & Financial Markets |
| Market Microstructure | 6 | 0.286 | 0.002 | 0.0529 | 3 | Asset Pricing & Financial Markets |
| International Finance | 5 | 0.238 | 0.000 | 0.0528 | 3 | Asset Pricing & Financial Markets |
| Behavioral Finance | 5 | 0.238 | 0.000 | 0.0378 | 2 | Asset Pricing & Financial Markets |
| Entrepreneurship | 4 | 0.190 | 0.000 | 0.0291 | 1 | Information Systems & Management |
| Corporate Governance | 4 | 0.190 | 0.001 | 0.0376 | 4 | Corporate Finance & Governance |
| Financial Markets | 4 | 0.190 | 0.000 | 0.0381 | 3 | Asset Pricing & Financial Markets |
| Banking and Financial Institutions | 4 | 0.190 | 0.000 | 0.0292 | 1 | Financial Engineering & Risk |

Betweenness 最高的五個領域：Investments（0.36）、Financial Management（0.34）、Risk Management（0.27）、Corporate Finance（0.25）、Asset Pricing（0.19）。Betweenness 高代表該領域位於不同主題群之間的連結位置，是系上跨主題的共同語言。

*出處：`analysis/network-analysis/nccu-fin/keyword_centrality.csv`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。 degree 為相連領域數，betweenness 為經過該節點的最短路徑比例，PageRank 為加權隨機漫步的穩態機率；parent_l1 來自 `1_build_taxonomy.ipynb` 手工編定的三層 taxonomy（170 個 L3、46 個 L2、16 個 L1）。*

![政治大學財務管理學系 研究領域教授人數長條圖](../network-analysis/nccu-fin/figures/10_top_keywords_bar.png)

*圖：政治大學財務管理學系 研究領域教授人數長條圖*  
*出處：`analysis/network-analysis/nccu-fin/figures/10_top_keywords_bar.png`*  
*建構方式：以二分網路中每個領域節點的 degree（研究該領域的教授數）排序繪製。*

### 2.3 研究領域社群

| 社群 | 領域數 | 主要領域（教授人數） | 主要 taxonomy L1（領域數） |
| --- | --- | --- | --- |
| 0 | 7 | Corporate Finance（9）、Investments（6）、Corporate Governance（4）、Market Microstructure（3）、Mergers and Acquisitions（2）、Banking and Financial Institutions（1）、Institutional Investors（1） | Corporate Finance & Governance 4、Asset Pricing & Financial Markets 2、Financial Engineering & Risk 1 |
| 1 | 6 | Financial Management（8）、International Finance（3）、Entrepreneurship（1）、Business Valuation（1）、Personal Finance（1）、Portfolio Management（1） | Corporate Finance & Governance 2、Asset Pricing & Financial Markets 2、Information Systems & Management 1 |
| 2 | 5 | Asset Pricing（4）、Financial Markets（3）、Behavioral Finance（2）、Econometrics（1）、Financial Derivatives（1） | Asset Pricing & Financial Markets 3、Economics & Policy 1、Financial Engineering & Risk 1 |
| 3 | 4 | Risk Management（5）、Credit Risk（1）、Financial Engineering（1）、Interest Rate Modeling（1） | Financial Engineering & Risk 4 |

*出處：`analysis/network-analysis/nccu-fin/keyword_communities.csv`（`community` 欄）、`keyword_centrality.csv`（教授人數）*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。*

![政治大學財務管理學系 研究領域網路的 Louvain 社群](../network-analysis/nccu-fin/figures/05_keyword_network_communities.png)

*圖：政治大學財務管理學系 研究領域網路的 Louvain 社群*  
*出處：`analysis/network-analysis/nccu-fin/figures/05_keyword_network_communities.png`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。節點顏色為社群，大小與 degree 成正比。*

![政治大學財務管理學系 各研究領域社群的 taxonomy L1 組成](../network-analysis/nccu-fin/figures/14_community_composition.png)

*圖：政治大學財務管理學系 各研究領域社群的 taxonomy L1 組成*  
*出處：`analysis/network-analysis/nccu-fin/figures/14_community_composition.png`*  
*建構方式：把每個 Louvain 領域社群內的領域依 taxonomy L1 分類計數，堆疊長條圖。用來檢查資料驅動的社群是否對應人工分類。*

![政治大學財務管理學系 研究領域共現熱圖](../network-analysis/nccu-fin/figures/13_keyword_cooccurrence_heatmap.png)

*圖：政治大學財務管理學系 研究領域共現熱圖*  
*出處：`analysis/network-analysis/nccu-fin/figures/13_keyword_cooccurrence_heatmap.png`*  
*建構方式：取研究領域網路的加權鄰接矩陣（共同研究兩領域的教授人數），依社群排序後繪製熱圖。*

## 3. 主要研究集群與重要老師

教授網路的 Louvain 社群偵測找出 3 個集群，正好對應「財務管理與投資」、「資產訂價與市場」、「公司理財與治理」三條主軸。因為系上領域數少（24 個）、教授之間共享領域的比例很高，教授網路密度達 0.757，接近完全圖，三個集群之間的界線其實相當模糊，集群劃分應視為傾向而非硬性分組。

教授網路共 21 位教授、3 個集群（Louvain，Q = 0.123）。以下依集群人數排序；集群編號與圖中的 Community 編號一致。表中 Degree 為與該教授共享研究領域的同儕數，Betweenness 為該教授位於他人最短路徑上的比例（越高越像橋梁）。

![政治大學財務管理學系 教授網路的 Louvain 集群](../network-analysis/nccu-fin/figures/09_professor_network_communities.png)

*圖：政治大學財務管理學系 教授網路的 Louvain 集群*  
*出處：`analysis/network-analysis/nccu-fin/figures/09_professor_network_communities.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

### 3.1 集群 0：財務管理與投資集群（8 人）

- **成員共同研究領域**：Financial Management（8 人）、Investments（3 人）、International Finance（3 人）、Risk Management（2 人）、Financial Markets（2 人）、Business Valuation（1 人）、Personal Finance（1 人）
- **成員主導 taxonomy L1**：Asset Pricing & Financial Markets 5 人、Corporate Finance & Governance 3 人

以 Financial Management 為共同語言（8 人全部有此領域），延伸到 Investments 與 International Finance。周行一、周冠男、張元晨的 betweenness 較高，是把此集群連到其他集群的橋梁；吳啟銘、湛可南則專注於財務管理與投資。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 周行一 | : HSING-YI CHOW | 主管／講座 | 19 | 0.097 | Entrepreneurship、Financial Management、International Finance、Investments、Risk Management |
| 周冠男 | : ROBIN K. CHOU | 專任 | 18 | 0.116 | Behavioral Finance、Financial Management、Investments、Market Microstructure |
| 吳啟銘 | : CHI-MING WU | 專任 | 18 | 0.000 | Business Valuation、Financial Management、Personal Finance、Portfolio Management |
| 湛可南 | : KONAN CHAN | 專任 | 18 | 0.000 | Financial Management、Investments |
| 張元晨 | : YUAN-CHEN CHANG | 專任 | 17 | 0.179 | Corporate Governance、Financial Management、International Finance |
| 顏錫銘 | : SIMON H . YEN | 主管／講座 | 17 | 0.013 | Financial Management、International Finance、Risk Management |
| 屠美亞 | : MIA TWU | 主管／講座 | 16 | 0.021 | Corporate Finance、Financial Management、Financial Markets |
| 林炯垚 | : JOUNG-YOL LIN | 主管／講座 | 16 | 0.000 | Financial Management、Financial Markets |

### 3.2 集群 1：資產訂價、市場微結構與風險集群（8 人）

- **成員共同研究領域**：Corporate Finance（4 人）、Asset Pricing（4 人）、Risk Management（3 人）、Investments（3 人）、Market Microstructure（2 人）、Credit Risk（1 人）、Financial Engineering（1 人）
- **成員主導 taxonomy L1**：Asset Pricing & Financial Markets 7 人、Financial Engineering & Risk 1 人

成員的主導 taxonomy 多為 Asset Pricing & Financial Markets，共享 Corporate Finance、Asset Pricing、Risk Management 與 Market Microstructure。李志宏與林基煌 degree 最高（各 19），陳鴻毅同時跨資產訂價與公司理財，是這個集群通往公司理財集群的橋。林則君為合聘教授，同時出現在兩個系所的名單。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 李志宏 | : JIE-HAUN LEE | 主管／講座 | 19 | 0.098 | Banking and Financial Institutions、Corporate Finance、Investments、Market Microstructure、Risk Management |
| 林基煌 | : CHI-HUANG LIN | 主管／講座 | 19 | 0.014 | Corporate Finance、Investments、Risk Management |
| 陳鴻毅 | : HONG-YI CHEN | 專任 | 18 | 0.114 | Asset Pricing、Corporate Finance、Investments |
| 黃群仰 | : CHUAN YANG HWANG | 主管／講座 | 16 | 0.000 | Corporate Finance、Market Microstructure |
| 林則君（2 個系所） |  | 主管／講座 | 14 | 0.053 | Asset Pricing、Behavioral Finance、Financial Markets |
| 謝沛霖 | : Pei-Lin Hsieh | 專任 | 10 | 0.000 | Asset Pricing、Financial Derivatives |
| 盧敬植 | : CHING-CHIH LU | 專任 | 9 | 0.000 | Asset Pricing、Econometrics |
| 岳夢蘭 | : MENG-LAN YUEH | 專任 | 5 | 0.000 | Credit Risk、Financial Engineering、Interest Rate Modeling、Risk Management |

### 3.3 集群 2：公司理財與公司治理集群（5 人）

- **成員共同研究領域**：Corporate Finance（4 人）、Corporate Governance（3 人）、Mergers and Acquisitions（2 人）、Institutional Investors（1 人）
- **成員主導 taxonomy L1**：Corporate Finance & Governance 5 人

五位成員全部以 Corporate Finance & Governance 為主導領域，共享 Corporate Finance、Corporate Governance 與 Mergers and Acquisitions。邱健嘉、黃嘉威、車倫周、陳嬿如四人 degree 相同（16），內部同質性極高；陳虹伶只有 Corporate Governance 一個領域，位於集群邊緣。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 邱健嘉 | : Jian-Jia Chiou | 專任 | 16 | 0.013 | Corporate Finance、Corporate Governance、Institutional Investors |
| 黃嘉威 | : CHIA-WEI HUANG | 教師（未細分） | 16 | 0.003 | Corporate Finance、Corporate Governance |
| 車倫周 | : Yun Ju Cha | 專任 | 16 | 0.000 | Corporate Finance、Mergers and Acquisitions |
| 陳嬿如 | : YENN-RU CHEN | 專任 | 16 | 0.000 | Corporate Finance、Mergers and Acquisitions |
| 陳虹伶 |  | 專任 | 5 | 0.000 | Corporate Governance |

*集群表出處：`analysis/network-analysis/nccu-fin/professor_communities.csv`（集群歸屬）、`professor_centrality.csv`（degree、betweenness、職稱類別）、`prof_keyword_network.graphml`（成員研究領域，用來統計集群的共同領域）*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 職稱類別為官網職稱的分類，一人可屬多類時取主要類別；「N 個系所」表示該教授也出現在其他系所名單。*

### 3.4 全系的橋接者與樞紐

Betweenness 最高的教授（跨集群的橋梁）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 張元晨 | : YUAN-CHEN CHANG | 專任 | 17 | 0.179 | Corporate Finance & Governance |
| 周冠男 | : ROBIN K. CHOU | 專任 | 18 | 0.116 | Asset Pricing & Financial Markets |
| 陳鴻毅 | : HONG-YI CHEN | 專任 | 18 | 0.114 | Asset Pricing & Financial Markets |
| 李志宏 | : JIE-HAUN LEE | 主管／講座 | 19 | 0.098 | Asset Pricing & Financial Markets |
| 周行一 | : HSING-YI CHOW | 主管／講座 | 19 | 0.097 | Asset Pricing & Financial Markets |
| 林則君 |  | 主管／講座 | 14 | 0.053 | Asset Pricing & Financial Markets |

Degree 最高的教授（與最多同儕共享領域的樞紐）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 李志宏 | : JIE-HAUN LEE | 主管／講座 | 19 | 0.098 | Asset Pricing & Financial Markets |
| 林基煌 | : CHI-HUANG LIN | 主管／講座 | 19 | 0.014 | Asset Pricing & Financial Markets |
| 周行一 | : HSING-YI CHOW | 主管／講座 | 19 | 0.097 | Asset Pricing & Financial Markets |
| 吳啟銘 | : CHI-MING WU | 專任 | 18 | 0.000 | Corporate Finance & Governance |
| 陳鴻毅 | : HONG-YI CHEN | 專任 | 18 | 0.114 | Asset Pricing & Financial Markets |
| 周冠男 | : ROBIN K. CHOU | 專任 | 18 | 0.116 | Asset Pricing & Financial Markets |

*出處：`analysis/network-analysis/nccu-fin/professor_centrality.csv`*

![政治大學財務管理學系 教授網路（節點大小 = betweenness）](../network-analysis/nccu-fin/figures/08_professor_network_betweenness.png)

*圖：政治大學財務管理學系 教授網路（節點大小 = betweenness）*  
*出處：`analysis/network-analysis/nccu-fin/figures/08_professor_network_betweenness.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。此圖節點大小改為與 betweenness 成正比。*

![政治大學財務管理學系 各集群教授 word cloud（字級 = degree）](../network-analysis/nccu-fin/figures/27_professor_wordcloud_degree_by_community.png)

*圖：政治大學財務管理學系 各集群教授 word cloud（字級 = degree）*  
*出處：`analysis/network-analysis/nccu-fin/figures/27_professor_wordcloud_degree_by_community.png`*  
*建構方式：依 Louvain 集群分塊、同集群同色的教授姓名 word cloud，字級與 degree 成線性正比並設下限。*

另有 2 位教授雖有研究領域，但與其他教授沒有共享任何領域，孤立於最大連通元件之外，不屬於任何集群。

## 4. 結構穩健性檢驗

### 4.1 虛無模型檢定

| 統計量 | 觀測值 | 虛無平均 | 虛無標準差 | z-score | empirical p | p < 0.05 |
| --- | --- | --- | --- | --- | --- | --- |
| 領域網路密度 | 0.2208 | 0.2351 | 0.0120 | -1.19 | 0.284 | 不顯著 |
| 領域網路 modularity Q | 0.2541 | 0.2587 | 0.0390 | -0.12 | 0.965 | 不顯著 |
| 領域平均共現次數 | 1.3137 | 1.2536 | 0.0575 | 1.05 | 0.374 | 不顯著 |
| 教授網路 clustering 係數 | 0.7807 | 0.7195 | 0.0348 | 1.76 | 0.070 | 不顯著 |

*出處：`analysis/network-analysis/nccu-fin/null_model_test.csv`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 密度顯著偏低而 modularity、共現顯著偏高，代表領域共現集中在少數主題群，不是均勻分布。*

![政治大學財務管理學系 觀測值 vs 虛無模型分布](../network-analysis/nccu-fin/figures/15_null_model_comparison.png)

*圖：政治大學財務管理學系 觀測值 vs 虛無模型分布*  
*出處：`analysis/network-analysis/nccu-fin/figures/15_null_model_comparison.png`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。*

### 4.2 λ 敏感度

| λ | 邊數 | 密度 | Q | 集群數 | 密度相對 baseline | Q 下降 | 過度合併 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 94 | 0.448 | 0.247 | 3 | +0% | 0.000 | 否 |
| 0.3 | 159 | 0.757 | 0.142 | 4 | +69% | 0.105 | 是 |
| 0.4 | 159 | 0.757 | 0.123 | 3 | +69% | 0.124 | 是 |
| 0.5 | 159 | 0.757 | 0.129 | 3 | +69% | 0.118 | 是 |

*出處：`analysis/network-analysis/nccu-fin/lambda_sensitivity.csv`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

![政治大學財務管理學系 λ 敏感度](../network-analysis/nccu-fin/figures/16_lambda_sensitivity.png)

*圖：政治大學財務管理學系 λ 敏感度*  
*出處：`analysis/network-analysis/nccu-fin/figures/16_lambda_sensitivity.png`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

### 4.3 taxonomy L1 覆蓋護欄

| taxonomy L1 | 教授數 | 覆蓋率 | flag |
| --- | --- | --- | --- |
| Corporate Finance & Governance | 17 | 81.0% | too_broad |
| Asset Pricing & Financial Markets | 15 | 71.4% | too_broad |
| Financial Engineering & Risk | 7 | 33.3% | ok |
| Economics & Policy | 1 | 4.8% | ok |
| Information Systems & Management | 1 | 4.8% | ok |

*出處：`analysis/network-analysis/nccu-fin/l1_coverage_guardrail.csv`（只列前 8 項）*  
*建構方式：計算每個 L1 分類涵蓋該單位多少比例的教授，超過 50% 標記 too_broad，代表此 L1 在本單位太寬，不能用來做 L1 roll-up 比較。*

## 5. 解讀與注意事項

- λ 敏感度檢定在 0.3、0.4、0.5 三個 λ 都觸發過度合併護欄：加入推論連結後密度由 0.448 增至 0.757、Q 由 0.247 降到 0.123。本報告的集群仍沿用 λ=0.4 的正式輸出，但解讀應以 λ=0 的 baseline（3 個社群）為準；兩者社群數相同，所以集群結論不受影響。
- L1 護欄標記 Corporate Finance & Governance 與 Asset Pricing & Financial Markets 兩個上層分類各涵蓋超過 50% 教授，因此不能用 L1 roll-up 視角來比較本系內部結構。
- 虛無模型四個統計量都未達顯著（p 介於 0.07 到 0.97），代表以 24 個領域、23 位教授的規模，領域共現結構與隨機重排差異不大。這是小網路的正常現象，不代表系上沒有主題結構。
- 有 2 位教授不在最大連通元件中（沒有與其他人共享任何領域），因此未出現在教授網路的集群裡。
- 博士畢業學校相當分散（Nanyang Technological University 與 Indiana University 各 2 人，其餘各 1 人），沒有單一主要來源學校。
- 研究領域來自官網自填內容，粒度與深度因人而異；網路密度與集群數反映填寫習慣的成分不可忽視，完整率不可解讀為系所或教授的品質排名。

## 附錄：本報告引用的資料與圖表清單

| 檔案 | 產生階段 / 程式 | 建構方式摘要 |
| --- | --- | --- |
| `analysis/data-collection/nccu-fin/quality-report.json` | 資料蒐集 `scripts/data-collection/collect.py` | 爬取官網後統計 canonical 紀錄人數、職稱分類、中英配對率與欄位完整率 |
| `analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv` | 預處理 `1_faculty_data_preprocessing.ipynb` | 標準化後各欄位有 canonical 值的教師比例與平均項目數 |
| `.../group_comparison/research_fields/fin-and-econ.csv`、`by_department/top_research_fields/nccu-fin.png` | 預處理 `2_rf_and_phd_inst_comparison.ipynb` | 由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。 |
| `.../group_comparison/phd_institutions/fin-and-econ.csv`、`by_department/top_phd_institutions/nccu-fin.png` | 同上 | 同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。 |
| `analysis/network-analysis/nccu-fin/network_metrics.json` | 網路分析 `2_build_network_data.ipynb` + `3_network_analysis.ipynb` | 由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 |
| `analysis/network-analysis/nccu-fin/keyword_centrality.csv`、`keyword_communities.csv` | `3_network_analysis.ipynb` | 研究領域網路的中心性與 Louvain 社群；taxonomy 來自 `1_build_taxonomy.ipynb` |
| `analysis/network-analysis/nccu-fin/professor_centrality.csv`、`professor_communities.csv`、`prof_keyword_network.graphml` | `3_network_analysis.ipynb` | 教授網路的中心性與 Louvain 集群；graphml 為二分網路，本報告用它統計各集群成員的共同領域 |
| `analysis/network-analysis/nccu-fin/null_model_test.csv` | `3_network_analysis.ipynb` | 以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 |
| `analysis/network-analysis/nccu-fin/lambda_sensitivity.csv` | `3_network_analysis.ipynb` | 以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。 |
| `analysis/network-analysis/nccu-fin/l1_coverage_guardrail.csv` | `3_network_analysis.ipynb` | 每個 L1 涵蓋教授比例，> 50% 標記 too_broad |
| `analysis/network-analysis/nccu-fin/figures/01, 05, 08, 09, 10, 13, 14, 15, 16, 27` | `3_network_analysis.ipynb` | 網路圖節點大小與 degree 或 betweenness 成正比、顏色依社群；邊數 > 400 時繪圖用 disparity filter backbone；word cloud 字級與中心性成線性正比 |

更完整的方法說明見 `docs/data-collection-report.md`、`docs/data-preprocessing-report.md`、`docs/network-analysis-report.md`。
