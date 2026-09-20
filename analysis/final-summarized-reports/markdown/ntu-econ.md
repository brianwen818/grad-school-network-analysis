# 台灣大學經濟學系（`ntu-econ`）研究結果總結報告

所屬分組：財金與經濟組（fin-and-econ）　｜　資料日期：2026-09-09 蒐集、2026-09-10 完成網路分析

> **本報告的資料來源**
> 本專案分三個階段：(1) 資料蒐集（`scripts/data-collection/`）從 14 個系所官網爬取師資的姓名、職稱、學歷與研究領域，中英文分開蒐集後配對；
> (2) 資料預處理（`scripts/data-preprocessing/`）把職稱、學歷、研究領域標準化成英文 canonical 值，並產生描述統計；
> (3) 網路分析（`scripts/network-analysis/current-version/`）建立「教授–研究領域」二分網路，投影成研究領域網路與教授網路，做社群偵測、中心性、虛無模型與敏感度分析。
> 本報告所有數字、表格與圖表都取自 `analysis/` 底下這三個階段的輸出，每張圖表下方都標明出處與建構方式，附錄另有完整清單。
> 「研究集群」指教授網路的 Louvain 社群；「重要老師」依教授在該網路中的 degree（與多少同儕共享領域）與 betweenness（是否位於集群之間的橋梁位置）判定，**不是**學術成就的排名。

## 1. 科系速覽

台大經濟系是 14 個系所中唯一的純經濟學單位，研究輪廓與財金系所明顯不同：最多人研究的是 Macroeconomics（13 人）、Econometrics（11 人）、Labor Economics（10 人），其次是 Monetary Economics 與 Industrial Organization（各 7 人）。官網列出 49 位教師，研究領域完整率 89.8%。博士畢業學校幾乎全部是美國名校：University of Chicago（7 人）、UCLA（6 人）、University of Wisconsin-Madison（6 人）、The Ohio State University（4 人），前十名中沒有任何台灣學校，是 14 個系所中海外博士比例最鮮明的科系。

### 1.1 基本資料

| 項目 | 數值 |
| --- | --- |
| 官網師資人數（canonical 紀錄） | 49 |
| 職稱分類（一人可屬多類） | 教師（未細分） 24、專任 22 |
| 中英文紀錄配對率 | 77.5% |
| 研究領域完整率（標準化後） | 89.8% |
| 學歷完整率（標準化後） | 100.0% |
| 每位教授平均研究領域數 | 2.04 |
| 進入網路分析的教授數 | 44（5 位因無研究領域排除） |

*出處：`analysis/data-collection/ntu-econ/quality-report.json`（人數、職稱、配對率）、`analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv`（完整率）、`analysis/network-analysis/ntu-econ/network_metrics.json`（進入網路人數）*  
*建構方式：quality-report 由 `scripts/data-collection/collect.py` 在爬取官網後統計 canonical 紀錄的職稱分類與中英配對；coverage 由 `1_faculty_data_preprocessing.ipynb` 計算標準化後有 canonical 值的教師比例。*

### 1.2 主要研究領域

| 排名 | 研究領域（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | Macroeconomics | 13 |
| 2 | Econometrics | 11 |
| 3 | Labor Economics | 10 |
| 4 | Monetary Economics | 7 |
| 5 | Industrial Organization | 7 |
| 6 | Political Economy | 6 |
| 7 | Financial Economics | 5 |
| 8 | Microeconomics | 5 |
| 9 | Public Economics | 3 |
| 10 | Game Theory | 3 |
| 11 | Experimental Economics | 3 |
| 12 | Mechanism Design | 3 |
| 13 | Banking and Financial Institutions | 3 |
| 14 | Health Economics | 2 |
| 15 | International Finance | 2 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/research_fields/fin-and-econ.csv`（`ntu-econ` 欄）*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

![台灣大學經濟學系 研究領域人數](../descriptive-stats-after-preprocessing/by_department/top_research_fields/ntu-econ.png)

*圖：台灣大學經濟學系 研究領域人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_research_fields/ntu-econ.png`*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

### 1.3 博士畢業學校

| 排名 | 博士畢業學校（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | University of Chicago | 7 |
| 2 | University of California, Los Angeles | 6 |
| 3 | University of Wisconsin-Madison | 6 |
| 4 | The Ohio State University | 4 |
| 5 | Pennsylvania State University | 3 |
| 6 | University of Michigan | 2 |
| 7 | Brown University | 2 |
| 8 | Northwestern University | 2 |
| 9 | Duke University | 2 |
| 10 | Texas A&M University | 1 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/phd_institutions/fin-and-econ.csv`（`ntu-econ` 欄）*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

![台灣大學經濟學系 博士畢業學校人數](../descriptive-stats-after-preprocessing/by_department/top_phd_institutions/ntu-econ.png)

*圖：台灣大學經濟學系 博士畢業學校人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_phd_institutions/ntu-econ.png`*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

## 2. 研究領域網路結構

### 2.1 網路指標

| 指標 | 數值 | 說明 |
| --- | --- | --- |
| 二分網路：教授數 / 領域數 / 邊數 | 44 / 28 / 100 | 一條邊 = 一位教授研究一個領域 |
| 二分網路連通元件數 | 2 | 最大元件涵蓋 93.2% 教授 |
| 每位教授平均 / 最多領域數 | 2.27 / 5 |  |
| 研究領域網路：節點 / 邊 | 27 / 68 | 只含至少與一個其他領域共現的領域 |
| 研究領域網路密度 | 0.194 | 實際邊數 ÷ 可能邊數 |
| 研究領域網路平均 degree | 5.04 |  |
| 研究領域網路 modularity Q（Louvain） | 0.441 | 4 個社群；resolution 0.7 / 1.3 時為 3 / 4 個 |
| 領域社群 vs taxonomy L1 一致度 | NMI 0.457 / ARI 0.125 | 1 = 完全一致，0 = 無關 |
| 教授網路：節點 / 邊 | 41 / 391 | 只含最大連通元件 |
| 教授網路密度 | 0.477 |  |
| 教授網路 modularity Q（Louvain） | 0.313 | 3 個集群 |
| 教授集群 vs 主導 L1 一致度 | NMI 0.173 / ARI 0.004 |  |

*出處：`analysis/network-analysis/ntu-econ/network_metrics.json`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

![台灣大學經濟學系 教授–研究領域二分網路](../network-analysis/ntu-econ/figures/01_bipartite_network.png)

*圖：台灣大學經濟學系 教授–研究領域二分網路*  
*出處：`analysis/network-analysis/ntu-econ/figures/01_bipartite_network.png`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。圖中兩類節點以不同顏色區分，節點大小與 degree 成正比；邊數超過 400 時繪圖使用 disparity filter backbone（α = 0.05），指標仍以完整圖計算。*

### 2.2 關鍵研究領域

| 研究領域 | Degree | Degree centrality | Betweenness | PageRank | 教授數 | taxonomy L1 |
| --- | --- | --- | --- | --- | --- | --- |
| Econometrics | 14 | 0.538 | 0.483 | 0.1029 | 11 | Economics & Policy |
| Macroeconomics | 11 | 0.423 | 0.380 | 0.0889 | 13 | Economics & Policy |
| Labor Economics | 8 | 0.308 | 0.109 | 0.0665 | 10 | Economics & Policy |
| Financial Economics | 8 | 0.308 | 0.018 | 0.0521 | 5 | Asset Pricing & Financial Markets |
| Banking and Financial Institutions | 7 | 0.269 | 0.023 | 0.0413 | 3 | Financial Engineering & Risk |
| Time Series Analysis | 6 | 0.231 | 0.002 | 0.0358 | 2 | Statistics & Statistical Methods |
| Political Economy | 6 | 0.231 | 0.088 | 0.0555 | 6 | Economics & Policy |
| Monetary Economics | 6 | 0.231 | 0.315 | 0.0508 | 7 | Economics & Policy |
| Financial Markets | 6 | 0.231 | 0.271 | 0.0409 | 2 | Asset Pricing & Financial Markets |
| Industrial Organization | 6 | 0.231 | 0.203 | 0.0522 | 7 | Economics & Policy |
| Social Network Analysis | 5 | 0.192 | 0.000 | 0.0316 | 2 | Data, Databases & Knowledge Discovery |
| Public Economics | 5 | 0.192 | 0.000 | 0.0269 | 3 | Economics & Policy |

Betweenness 最高的五個領域：Econometrics（0.48）、Macroeconomics（0.38）、Monetary Economics（0.32）、Financial Markets（0.27）、Industrial Organization（0.20）。Betweenness 高代表該領域位於不同主題群之間的連結位置，是系上跨主題的共同語言。

*出處：`analysis/network-analysis/ntu-econ/keyword_centrality.csv`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。 degree 為相連領域數，betweenness 為經過該節點的最短路徑比例，PageRank 為加權隨機漫步的穩態機率；parent_l1 來自 `1_build_taxonomy.ipynb` 手工編定的三層 taxonomy（170 個 L3、46 個 L2、16 個 L1）。*

![台灣大學經濟學系 研究領域教授人數長條圖](../network-analysis/ntu-econ/figures/10_top_keywords_bar.png)

*圖：台灣大學經濟學系 研究領域教授人數長條圖*  
*出處：`analysis/network-analysis/ntu-econ/figures/10_top_keywords_bar.png`*  
*建構方式：以二分網路中每個領域節點的 degree（研究該領域的教授數）排序繪製。*

### 2.3 研究領域社群

| 社群 | 領域數 | 主要領域（教授人數） | 主要 taxonomy L1（領域數） |
| --- | --- | --- | --- |
| 0 | 8 | Macroeconomics（13）、Monetary Economics（7）、Financial Economics（5）、Banking and Financial Institutions（3）、Time Series Analysis（2）、International Finance（2）、Asset Pricing（1） | Economics & Policy 3、Asset Pricing & Financial Markets 3、Financial Engineering & Risk 1 |
| 1 | 7 | Econometrics（11）、Labor Economics（10）、Social Network Analysis（2）、Health Economics（2）、Statistics（1）、Environmental Economics（1）、Machine Learning（1） | Economics & Policy 4、Data, Databases & Knowledge Discovery 1、Statistics & Statistical Methods 1 |
| 2 | 7 | Industrial Organization（7）、Political Economy（6）、Microeconomics（5）、Public Economics（3）、Game Theory（3）、Mechanism Design（3）、Development Economics（2） | Economics & Policy 5、Applied Mathematics & Operations Research 2 |
| 3 | 5 | Financial Markets（2）、Corporate Finance（1）、Corporate Governance（1）、Investments（1）、Market Microstructure（1） | Asset Pricing & Financial Markets 3、Corporate Finance & Governance 2 |

*出處：`analysis/network-analysis/ntu-econ/keyword_communities.csv`（`community` 欄）、`keyword_centrality.csv`（教授人數）*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。*

![台灣大學經濟學系 研究領域網路的 Louvain 社群](../network-analysis/ntu-econ/figures/05_keyword_network_communities.png)

*圖：台灣大學經濟學系 研究領域網路的 Louvain 社群*  
*出處：`analysis/network-analysis/ntu-econ/figures/05_keyword_network_communities.png`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。節點顏色為社群，大小與 degree 成正比。*

![台灣大學經濟學系 各研究領域社群的 taxonomy L1 組成](../network-analysis/ntu-econ/figures/14_community_composition.png)

*圖：台灣大學經濟學系 各研究領域社群的 taxonomy L1 組成*  
*出處：`analysis/network-analysis/ntu-econ/figures/14_community_composition.png`*  
*建構方式：把每個 Louvain 領域社群內的領域依 taxonomy L1 分類計數，堆疊長條圖。用來檢查資料驅動的社群是否對應人工分類。*

![台灣大學經濟學系 研究領域共現熱圖](../network-analysis/ntu-econ/figures/13_keyword_cooccurrence_heatmap.png)

*圖：台灣大學經濟學系 研究領域共現熱圖*  
*出處：`analysis/network-analysis/ntu-econ/figures/13_keyword_cooccurrence_heatmap.png`*  
*建構方式：取研究領域網路的加權鄰接矩陣（共同研究兩領域的教授人數），依社群排序後繪製熱圖。*

## 3. 主要研究集群與重要老師

教授網路分成 3 個規模相近的集群：總體與貨幣經濟、個體與產業組織、計量與勞動經濟。研究領域網路的 modularity 顯著高於虛無模型（z = 5.7，p = 0.002），是財金與經濟組中主題分工最明確的科系。

教授網路共 41 位教授、3 個集群（Louvain，Q = 0.313）。以下依集群人數排序；集群編號與圖中的 Community 編號一致。表中 Degree 為與該教授共享研究領域的同儕數，Betweenness 為該教授位於他人最短路徑上的比例（越高越像橋梁）。

![台灣大學經濟學系 教授網路的 Louvain 集群](../network-analysis/ntu-econ/figures/09_professor_network_communities.png)

*圖：台灣大學經濟學系 教授網路的 Louvain 集群*  
*出處：`analysis/network-analysis/ntu-econ/figures/09_professor_network_communities.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

### 3.1 集群 0：總體經濟與貨幣經濟集群（17 人）

- **成員共同研究領域**：Macroeconomics（13 人）、Monetary Economics（7 人）、Labor Economics（3 人）、Financial Economics（3 人）、Financial Markets（2 人）、Econometrics（2 人）、Banking and Financial Institutions（2 人）
- **成員主導 taxonomy L1**：Economics & Policy 12 人、Asset Pricing & Financial Markets 5 人

17 位成員，共享 Macroeconomics（13 人）、Monetary Economics（7 人）與 Financial Economics。梁卓誠、劉育辰的 degree 最高（30）且 betweenness 較高，是集群對外的橋梁；小松利明（Toshiaki Komatsu）與高恩琵同時研究勞動經濟與總體經濟，把此集群連到計量勞動集群。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 梁卓誠 | Cheuk Shing Leung | 專任 | 30 | 0.081 | Macroeconomics、Public Economics |
| 劉育辰 | Yu-Chen Liu | 專任 | 30 | 0.071 | International Economics、Macroeconomics、Monetary Economics |
| Toshiaki Komatsu | Toshiaki Komatsu | 專任 | 30 | 0.008 | Labor Economics、Macroeconomics |
| 小松利明 |  | 教師（未細分） | 30 | 0.008 | Labor Economics、Macroeconomics |
| 高恩琵 | Ko Eunbi | 專任 | 30 | 0.008 | Labor Economics、Macroeconomics |
| 和田健司 | Kenji Wada | 專任 | 27 | 0.096 | Asset Pricing、Econometrics、Financial Economics、Macroeconomics、Time Series Analysis |
| 郭漢豪 | Kwok Hon Ho | 專任 | 24 | 0.027 | Econometrics、Macroeconomics、Social Network Analysis、Statistics |
| 王建強 | Chien-Chiang Wang | 專任 | 19 | 0.144 | Banking and Financial Institutions、Financial Economics、Macroeconomics、Monetary Economics |

其餘成員（9 位，依 degree 排序）：蘇軒立、李怡庭、陳旭昇、廖珮如、蔡宜展、朱玉琦、陳南光、陳虹如、吳儀玲


### 3.2 集群 1：個體、產業組織與政治經濟集群（14 人）

- **成員共同研究領域**：Industrial Organization（7 人）、Political Economy（6 人）、Microeconomics（5 人）、Mechanism Design（3 人）、Game Theory（3 人）、Financial Economics（1 人）、Labor Economics（1 人）
- **成員主導 taxonomy L1**：Economics & Policy 11 人、Applied Mathematics & Operations Research 3 人

14 位成員，共享 Industrial Organization、Political Economy、Microeconomics、Game Theory 與 Mechanism Design，主導 taxonomy 為 Economics & Policy 與 Applied Mathematics & Operations Research。李宗穎（產業組織、健康經濟、計量）與朴聖民（金融經濟、勞動、個體）的 betweenness 最高；羅珮瑜、馮勃翰的研究組合完全相同（賽局、產業組織、政治經濟）。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 李宗穎 | Chung-Ying Lee | 專任 | 28 | 0.104 | Econometrics、Health Economics、Industrial Organization |
| 朴聖民 |  | 教師（未細分） | 27 | 0.121 | Financial Economics、Labor Economics、Microeconomics |
| 羅珮瑜 | Pei-Yu Lo | 專任 | 25 | 0.025 | Game Theory、Industrial Organization、Political Economy |
| 馮勃翰 | Po Han Fong | 專任 | 25 | 0.025 | Game Theory、Industrial Organization、Political Economy |
| 蔡崇聖 | Tsung-Sheng Tsai | 教師（未細分） | 23 | 0.090 | Industrial Organization、Political Economy、Public Economics |
| 江淳芳 | Chun-Fang Chiang | 教師（未細分） | 23 | 0.024 | Microeconomics、Political Economy |
| 陳慶池 | Hing Chi Jimmy Chan | 教師（未細分） | 21 | 0.097 | Game Theory、Mechanism Design、Political Economy |
| 許軒銘 | Shanon Hsuan-Ming Hsu | 專任 | 19 | 0.009 | Development Economics、Political Economy |

其餘成員（6 位，依 degree 排序）：Joonkyo Hong、洪俊教、林明仁、黃景沂、Junrok Park、朴埻錄


### 3.3 集群 2：計量經濟與勞動經濟集群（10 人）

- **成員共同研究領域**：Econometrics（8 人）、Labor Economics（6 人）、Financial Economics（1 人）、Banking and Financial Institutions（1 人）、International Finance（1 人）、Time Series Analysis（1 人）、Environmental Economics（1 人）
- **成員主導 taxonomy L1**：Economics & Policy 8 人、Asset Pricing & Financial Markets 2 人

10 位成員，共享 Econometrics（8 人）與 Labor Economics（6 人）。謝志昇結合計量、健康經濟、勞動與社會網路分析，是集群中心；陳由常、陳冠銘、駱明慶、楊睿中的 degree 並列 24，內部同質性高；楊睿中是系上唯一標記 Machine Learning 的教授。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 謝志昇 | Chih-Sheng Hsieh | 教師（未細分） | 24 | 0.057 | Econometrics、Health Economics、Labor Economics、Social Network Analysis |
| 陳由常 | Yu-Chang Chen | 專任 | 24 | 0.025 | Econometrics、Labor Economics、Public Economics |
| 陳冠銘 | Kuan-Ming Chen | 專任 | 24 | 0.002 | Econometrics、Labor Economics |
| 駱明慶 | Ming-Ching Luoh | 教師（未細分） | 24 | 0.002 | Econometrics、Labor Economics |
| 楊睿中 | Jui-Chung Yang | 專任 | 24 | 0.000 | Econometrics、Environmental Economics、Machine Learning |
| Sungmin Park | Sungmin Park | 專任 | 23 | 0.003 | Financial Economics、Labor Economics |
| 樊家忠 | Elliott Fan | 教師（未細分） | 19 | 0.012 | Development Economics、Labor Economics |
| 何泰寬 | Tai-kuang Ho | 教師（未細分） | 13 | 0.009 | Banking and Financial Institutions、Econometrics、International Finance、Time Series Analysis |

其餘成員（2 位，依 degree 排序）：張勝凱、王泓仁


*集群表出處：`analysis/network-analysis/ntu-econ/professor_communities.csv`（集群歸屬）、`professor_centrality.csv`（degree、betweenness、職稱類別）、`prof_keyword_network.graphml`（成員研究領域，用來統計集群的共同領域）*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 職稱類別為官網職稱的分類，一人可屬多類時取主要類別；「N 個系所」表示該教授也出現在其他系所名單。*

### 3.4 全系的橋接者與樞紐

Betweenness 最高的教授（跨集群的橋梁）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 王建強 | Chien-Chiang Wang | 專任 | 19 | 0.144 | Economics & Policy |
| 朴聖民 |  | 教師（未細分） | 27 | 0.121 | Economics & Policy |
| 李宗穎 | Chung-Ying Lee | 專任 | 28 | 0.104 | Economics & Policy |
| 陳慶池 | Hing Chi Jimmy Chan | 教師（未細分） | 21 | 0.097 | Applied Mathematics & Operations Research |
| 和田健司 | Kenji Wada | 專任 | 27 | 0.096 | Asset Pricing & Financial Markets |
| 蔡崇聖 | Tsung-Sheng Tsai | 教師（未細分） | 23 | 0.090 | Economics & Policy |

Degree 最高的教授（與最多同儕共享領域的樞紐）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 梁卓誠 | Cheuk Shing Leung | 專任 | 30 | 0.081 | Economics & Policy |
| 小松利明 |  | 教師（未細分） | 30 | 0.008 | Economics & Policy |
| Toshiaki Komatsu | Toshiaki Komatsu | 專任 | 30 | 0.008 | Economics & Policy |
| 劉育辰 | Yu-Chen Liu | 專任 | 30 | 0.071 | Economics & Policy |
| 高恩琵 | Ko Eunbi | 專任 | 30 | 0.008 | Economics & Policy |
| 李宗穎 | Chung-Ying Lee | 專任 | 28 | 0.104 | Economics & Policy |

*出處：`analysis/network-analysis/ntu-econ/professor_centrality.csv`*

![台灣大學經濟學系 教授網路（節點大小 = betweenness）](../network-analysis/ntu-econ/figures/08_professor_network_betweenness.png)

*圖：台灣大學經濟學系 教授網路（節點大小 = betweenness）*  
*出處：`analysis/network-analysis/ntu-econ/figures/08_professor_network_betweenness.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。此圖節點大小改為與 betweenness 成正比。*

![台灣大學經濟學系 各集群教授 word cloud（字級 = degree）](../network-analysis/ntu-econ/figures/27_professor_wordcloud_degree_by_community.png)

*圖：台灣大學經濟學系 各集群教授 word cloud（字級 = degree）*  
*出處：`analysis/network-analysis/ntu-econ/figures/27_professor_wordcloud_degree_by_community.png`*  
*建構方式：依 Louvain 集群分塊、同集群同色的教授姓名 word cloud，字級與 degree 成線性正比並設下限。*

另有 3 位教授雖有研究領域，但與其他教授沒有共享任何領域，孤立於最大連通元件之外，不屬於任何集群。

## 4. 結構穩健性檢驗

### 4.1 虛無模型檢定

| 統計量 | 觀測值 | 虛無平均 | 虛無標準差 | z-score | empirical p | p < 0.05 |
| --- | --- | --- | --- | --- | --- | --- |
| 領域網路密度 | 0.1937 | 0.2120 | 0.0142 | -1.28 | 0.174 | 不顯著 |
| 領域網路 modularity Q | 0.4408 | 0.2535 | 0.0326 | 5.75 | 0.002 | 顯著 |
| 領域平均共現次數 | 1.3235 | 1.2862 | 0.0594 | 0.63 | 0.595 | 不顯著 |
| 教授網路 clustering 係數 | 0.7373 | 0.6934 | 0.0314 | 1.40 | 0.168 | 不顯著 |

*出處：`analysis/network-analysis/ntu-econ/null_model_test.csv`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 密度顯著偏低而 modularity、共現顯著偏高，代表領域共現集中在少數主題群，不是均勻分布。*

![台灣大學經濟學系 觀測值 vs 虛無模型分布](../network-analysis/ntu-econ/figures/15_null_model_comparison.png)

*圖：台灣大學經濟學系 觀測值 vs 虛無模型分布*  
*出處：`analysis/network-analysis/ntu-econ/figures/15_null_model_comparison.png`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。*

### 4.2 λ 敏感度

| λ | 邊數 | 密度 | Q | 集群數 | 密度相對 baseline | Q 下降 | 過度合併 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 242 | 0.295 | 0.391 | 3 | +0% | 0.000 | 否 |
| 0.3 | 391 | 0.477 | 0.327 | 3 | +62% | 0.064 | 是 |
| 0.4 | 391 | 0.477 | 0.313 | 3 | +62% | 0.078 | 是 |
| 0.5 | 391 | 0.477 | 0.300 | 3 | +62% | 0.091 | 是 |

*出處：`analysis/network-analysis/ntu-econ/lambda_sensitivity.csv`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

![台灣大學經濟學系 λ 敏感度](../network-analysis/ntu-econ/figures/16_lambda_sensitivity.png)

*圖：台灣大學經濟學系 λ 敏感度*  
*出處：`analysis/network-analysis/ntu-econ/figures/16_lambda_sensitivity.png`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

### 4.3 taxonomy L1 覆蓋護欄

| taxonomy L1 | 教授數 | 覆蓋率 | flag |
| --- | --- | --- | --- |
| Economics & Policy | 38 | 92.7% | too_broad |
| Asset Pricing & Financial Markets | 9 | 22.0% | ok |
| Applied Mathematics & Operations Research | 5 | 12.2% | ok |
| Financial Engineering & Risk | 3 | 7.3% | ok |
| Statistics & Statistical Methods | 3 | 7.3% | ok |
| Data, Databases & Knowledge Discovery | 2 | 4.9% | ok |
| AI & Machine Learning | 1 | 2.4% | ok |
| Corporate Finance & Governance | 1 | 2.4% | ok |

*出處：`analysis/network-analysis/ntu-econ/l1_coverage_guardrail.csv`（只列前 8 項）*  
*建構方式：計算每個 L1 分類涵蓋該單位多少比例的教授，超過 50% 標記 too_broad，代表此 L1 在本單位太寬，不能用來做 L1 roll-up 比較。*

## 5. 解讀與注意事項

- 中英文官網名單不完全相同（配對率 77.5%），有 4 位教授沒有中文姓名，另有少數教授以中文與英文各留一筆紀錄（例如 Toshiaki Komatsu 與小松利明），在教授網路中會成為兩個節點；解讀集群人數時要注意這一點。
- L1 護欄標記 Economics & Policy 涵蓋超過 50% 教授，這是純經濟系的必然結果，L1 視角在本系無法區分內部結構。
- λ 在 0.3、0.4、0.5 都觸發過度合併護欄（密度由 0.295 增至 0.477、Q 降 0.06 至 0.09）。λ=0 的 baseline 同樣是 3 個社群，集群結論穩健，但集群之間的緊密度應以 baseline 為準。
- Econometrics 的 betweenness（0.48）是全系最高，它同時被總體、個體與勞動三群教授使用，是整個系的共同方法語言。
- 有 3 位教授不在最大連通元件中。
- 研究領域來自官網自填內容，粒度與深度因人而異；網路密度與集群數反映填寫習慣的成分不可忽視，完整率不可解讀為系所或教授的品質排名。

## 附錄：本報告引用的資料與圖表清單

| 檔案 | 產生階段 / 程式 | 建構方式摘要 |
| --- | --- | --- |
| `analysis/data-collection/ntu-econ/quality-report.json` | 資料蒐集 `scripts/data-collection/collect.py` | 爬取官網後統計 canonical 紀錄人數、職稱分類、中英配對率與欄位完整率 |
| `analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv` | 預處理 `1_faculty_data_preprocessing.ipynb` | 標準化後各欄位有 canonical 值的教師比例與平均項目數 |
| `.../group_comparison/research_fields/fin-and-econ.csv`、`by_department/top_research_fields/ntu-econ.png` | 預處理 `2_rf_and_phd_inst_comparison.ipynb` | 由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。 |
| `.../group_comparison/phd_institutions/fin-and-econ.csv`、`by_department/top_phd_institutions/ntu-econ.png` | 同上 | 同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。 |
| `analysis/network-analysis/ntu-econ/network_metrics.json` | 網路分析 `2_build_network_data.ipynb` + `3_network_analysis.ipynb` | 由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 |
| `analysis/network-analysis/ntu-econ/keyword_centrality.csv`、`keyword_communities.csv` | `3_network_analysis.ipynb` | 研究領域網路的中心性與 Louvain 社群；taxonomy 來自 `1_build_taxonomy.ipynb` |
| `analysis/network-analysis/ntu-econ/professor_centrality.csv`、`professor_communities.csv`、`prof_keyword_network.graphml` | `3_network_analysis.ipynb` | 教授網路的中心性與 Louvain 集群；graphml 為二分網路，本報告用它統計各集群成員的共同領域 |
| `analysis/network-analysis/ntu-econ/null_model_test.csv` | `3_network_analysis.ipynb` | 以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 |
| `analysis/network-analysis/ntu-econ/lambda_sensitivity.csv` | `3_network_analysis.ipynb` | 以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。 |
| `analysis/network-analysis/ntu-econ/l1_coverage_guardrail.csv` | `3_network_analysis.ipynb` | 每個 L1 涵蓋教授比例，> 50% 標記 too_broad |
| `analysis/network-analysis/ntu-econ/figures/01, 05, 08, 09, 10, 13, 14, 15, 16, 27` | `3_network_analysis.ipynb` | 網路圖節點大小與 degree 或 betweenness 成正比、顏色依社群；邊數 > 400 時繪圖用 disparity filter backbone；word cloud 字級與中心性成線性正比 |

更完整的方法說明見 `docs/data-collection-report.md`、`docs/data-preprocessing-report.md`、`docs/network-analysis-report.md`。
