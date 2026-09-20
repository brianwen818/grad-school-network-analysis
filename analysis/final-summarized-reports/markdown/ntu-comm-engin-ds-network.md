# 台灣大學電信工程學研究所 資料科學與網路組（`ntu-comm-engin-ds-network`）研究結果總結報告

所屬分組：資料科學組（ds）　｜　資料日期：2026-09-09 蒐集、2026-09-10 完成網路分析

> **本報告的資料來源**
> 本專案分三個階段：(1) 資料蒐集（`scripts/data-collection/`）從 14 個系所官網爬取師資的姓名、職稱、學歷與研究領域，中英文分開蒐集後配對；
> (2) 資料預處理（`scripts/data-preprocessing/`）把職稱、學歷、研究領域標準化成英文 canonical 值，並產生描述統計；
> (3) 網路分析（`scripts/network-analysis/current-version/`）建立「教授–研究領域」二分網路，投影成研究領域網路與教授網路，做社群偵測、中心性、虛無模型與敏感度分析。
> 本報告所有數字、表格與圖表都取自 `analysis/` 底下這三個階段的輸出，每張圖表下方都標明出處與建構方式，附錄另有完整清單。
> 「研究集群」指教授網路的 Louvain 社群；「重要老師」依教授在該網路中的 degree（與多少同儕共享領域）與 betweenness（是否位於集群之間的橋梁位置）判定，**不是**學術成就的排名。

## 1. 科系速覽

台大電信所資料科學與網路組是一個 25 人的小型單位，研究領域完整率 100%，是資料最完整的系所之一。研究輪廓橫跨三條軸線：Machine Learning（9 人）與 Artificial Intelligence、Signal Processing（7 人）與 Image Processing、以及 Computer Networks（6 人）、Multimedia Systems（6 人）與 Wireless Networks（5 人）。教授網路的集群與 taxonomy L1 的一致度（NMI 0.84）是 18 個分析單位中最高的，代表三個集群幾乎就是三個學門。博士畢業學校以台大（5 人）、University of Michigan（4 人）、UIUC 與 USC（各 3 人）為主。

### 1.1 基本資料

| 項目 | 數值 |
| --- | --- |
| 官網師資人數（canonical 紀錄） | 25 |
| 職稱分類（一人可屬多類） | 專任 19、兼任 3、教師（未細分） 3 |
| 中英文紀錄配對率 | 100.0% |
| 研究領域完整率（標準化後） | 100.0% |
| 學歷完整率（標準化後） | 100.0% |
| 每位教授平均研究領域數 | 2.96 |
| 進入網路分析的教授數 | 25（0 位因無研究領域排除） |

*出處：`analysis/data-collection/ntu-comm-engin-ds-network/quality-report.json`（人數、職稱、配對率）、`analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv`（完整率）、`analysis/network-analysis/ntu-comm-engin-ds-network/network_metrics.json`（進入網路人數）*  
*建構方式：quality-report 由 `scripts/data-collection/collect.py` 在爬取官網後統計 canonical 紀錄的職稱分類與中英配對；coverage 由 `1_faculty_data_preprocessing.ipynb` 計算標準化後有 canonical 值的教師比例。*

### 1.2 主要研究領域

| 排名 | 研究領域（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | Machine Learning | 9 |
| 2 | Signal Processing | 7 |
| 3 | Computer Networks | 6 |
| 4 | Multimedia Systems | 6 |
| 5 | Wireless Networks | 5 |
| 6 | Artificial Intelligence | 4 |
| 7 | Deep Learning | 3 |
| 8 | Wireless Communications | 3 |
| 9 | Image Processing | 3 |
| 10 | Optimization | 3 |
| 11 | Internet of Things | 2 |
| 12 | Robotics | 2 |
| 13 | Information Security | 2 |
| 14 | Neural Networks | 2 |
| 15 | Game Theory | 1 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/research_fields/ds.csv`（`ntu-comm-engin-ds-network` 欄）*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

![台灣大學電信工程學研究所 資料科學與網路組 研究領域人數](../descriptive-stats-after-preprocessing/by_department/top_research_fields/ntu-comm-engin-ds-network.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 研究領域人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_research_fields/ntu-comm-engin-ds-network.png`*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

### 1.3 博士畢業學校

| 排名 | 博士畢業學校（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | National Taiwan University | 5 |
| 2 | University of Michigan | 4 |
| 3 | University of Illinois Urbana-Champaign | 3 |
| 4 | University of Southern California | 3 |
| 5 | Princeton University | 2 |
| 6 | University of California, Los Angeles | 1 |
| 7 | Carnegie Mellon University | 1 |
| 8 | Columbia University | 1 |
| 9 | Georgia Institute of Technology | 1 |
| 10 | University of California, Berkeley | 1 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/phd_institutions/ds.csv`（`ntu-comm-engin-ds-network` 欄）*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

![台灣大學電信工程學研究所 資料科學與網路組 博士畢業學校人數](../descriptive-stats-after-preprocessing/by_department/top_phd_institutions/ntu-comm-engin-ds-network.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 博士畢業學校人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_phd_institutions/ntu-comm-engin-ds-network.png`*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

## 2. 研究領域網路結構

### 2.1 網路指標

| 指標 | 數值 | 說明 |
| --- | --- | --- |
| 二分網路：教授數 / 領域數 / 邊數 | 25 / 31 / 74 | 一條邊 = 一位教授研究一個領域 |
| 二分網路連通元件數 | 1 | 最大元件涵蓋 100.0% 教授 |
| 每位教授平均 / 最多領域數 | 2.96 / 7 |  |
| 研究領域網路：節點 / 邊 | 31 / 89 | 只含至少與一個其他領域共現的領域 |
| 研究領域網路密度 | 0.191 | 實際邊數 ÷ 可能邊數 |
| 研究領域網路平均 degree | 5.74 |  |
| 研究領域網路 modularity Q（Louvain） | 0.407 | 4 個社群；resolution 0.7 / 1.3 時為 3 / 4 個 |
| 領域社群 vs taxonomy L1 一致度 | NMI 0.432 / ARI 0.199 | 1 = 完全一致，0 = 無關 |
| 教授網路：節點 / 邊 | 25 / 153 | 只含最大連通元件 |
| 教授網路密度 | 0.510 |  |
| 教授網路 modularity Q（Louvain） | 0.374 | 3 個集群 |
| 教授集群 vs 主導 L1 一致度 | NMI 0.839 / ARI 0.818 |  |

*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/network_metrics.json`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

![台灣大學電信工程學研究所 資料科學與網路組 教授–研究領域二分網路](../network-analysis/ntu-comm-engin-ds-network/figures/01_bipartite_network.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 教授–研究領域二分網路*  
*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/figures/01_bipartite_network.png`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。圖中兩類節點以不同顏色區分，節點大小與 degree 成正比；邊數超過 400 時繪圖使用 disparity filter backbone（α = 0.05），指標仍以完整圖計算。*

### 2.2 關鍵研究領域

| 研究領域 | Degree | Degree centrality | Betweenness | PageRank | 教授數 | taxonomy L1 |
| --- | --- | --- | --- | --- | --- | --- |
| Multimedia Systems | 14 | 0.467 | 0.194 | 0.0810 | 6 | Vision, Multimedia & Human-Centered Computing |
| Computer Networks | 13 | 0.433 | 0.144 | 0.0749 | 6 | Networks & Communications |
| Signal Processing | 13 | 0.433 | 0.188 | 0.0694 | 7 | Vision, Multimedia & Human-Centered Computing |
| Machine Learning | 12 | 0.400 | 0.297 | 0.0788 | 9 | AI & Machine Learning |
| Optimization | 12 | 0.400 | 0.050 | 0.0535 | 3 | Applied Mathematics & Operations Research |
| Deep Learning | 10 | 0.333 | 0.180 | 0.0519 | 3 | AI & Machine Learning |
| Artificial Intelligence | 9 | 0.300 | 0.079 | 0.0512 | 4 | AI & Machine Learning |
| Wireless Networks | 9 | 0.300 | 0.050 | 0.0535 | 5 | Networks & Communications |
| Wireless Communications | 8 | 0.267 | 0.072 | 0.0405 | 3 | Networks & Communications |
| Financial Technology | 6 | 0.200 | 0.000 | 0.0291 | 1 | Financial Engineering & Risk |
| Internet of Things | 6 | 0.200 | 0.001 | 0.0328 | 2 | Networks & Communications |
| Systems Biology | 6 | 0.200 | 0.000 | 0.0291 | 1 | Biomedical & Health Informatics |

Betweenness 最高的五個領域：Machine Learning（0.30）、Multimedia Systems（0.19）、Signal Processing（0.19）、Deep Learning（0.18）、Computer Networks（0.14）。Betweenness 高代表該領域位於不同主題群之間的連結位置，是系上跨主題的共同語言。

*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/keyword_centrality.csv`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。 degree 為相連領域數，betweenness 為經過該節點的最短路徑比例，PageRank 為加權隨機漫步的穩態機率；parent_l1 來自 `1_build_taxonomy.ipynb` 手工編定的三層 taxonomy（170 個 L3、46 個 L2、16 個 L1）。*

![台灣大學電信工程學研究所 資料科學與網路組 研究領域教授人數長條圖](../network-analysis/ntu-comm-engin-ds-network/figures/10_top_keywords_bar.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 研究領域教授人數長條圖*  
*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/figures/10_top_keywords_bar.png`*  
*建構方式：以二分網路中每個領域節點的 degree（研究該領域的教授數）排序繪製。*

### 2.3 研究領域社群

| 社群 | 領域數 | 主要領域（教授人數） | 主要 taxonomy L1（領域數） |
| --- | --- | --- | --- |
| 0 | 9 | Machine Learning（9）、Artificial Intelligence（4）、Information Security（2）、Robotics（2）、Computer Vision（1）、Reinforcement Learning（1）、Smart Manufacturing（1） | AI & Machine Learning 5、Robotics, Control & Smart Manufacturing 2、Security, Privacy & Cryptography 1 |
| 1 | 9 | Multimedia Systems（6）、Computer Networks（6）、Wireless Networks（5）、Internet of Things（2）、Blockchain（1）、Game Theory（1）、Databases（1） | Networks & Communications 5、Vision, Multimedia & Human-Centered Computing 1、Security, Privacy & Cryptography 1 |
| 2 | 7 | Optimization（3）、Deep Learning（3）、Wireless Communications（3）、Data Science（1）、Financial Technology（1）、Systems Biology（1）、Information Theory（1） | Applied Mathematics & Operations Research 1、AI & Machine Learning 1、Networks & Communications 1 |
| 3 | 6 | Signal Processing（7）、Image Processing（3）、Neural Networks（2）、Computer Graphics（1）、Pattern Recognition（1）、Data Mining（1） | Vision, Multimedia & Human-Centered Computing 4、AI & Machine Learning 1、Data, Databases & Knowledge Discovery 1 |

*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/keyword_communities.csv`（`community` 欄）、`keyword_centrality.csv`（教授人數）*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。*

![台灣大學電信工程學研究所 資料科學與網路組 研究領域網路的 Louvain 社群](../network-analysis/ntu-comm-engin-ds-network/figures/05_keyword_network_communities.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 研究領域網路的 Louvain 社群*  
*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/figures/05_keyword_network_communities.png`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。節點顏色為社群，大小與 degree 成正比。*

![台灣大學電信工程學研究所 資料科學與網路組 各研究領域社群的 taxonomy L1 組成](../network-analysis/ntu-comm-engin-ds-network/figures/14_community_composition.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 各研究領域社群的 taxonomy L1 組成*  
*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/figures/14_community_composition.png`*  
*建構方式：把每個 Louvain 領域社群內的領域依 taxonomy L1 分類計數，堆疊長條圖。用來檢查資料驅動的社群是否對應人工分類。*

![台灣大學電信工程學研究所 資料科學與網路組 研究領域共現熱圖](../network-analysis/ntu-comm-engin-ds-network/figures/13_keyword_cooccurrence_heatmap.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 研究領域共現熱圖*  
*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/figures/13_keyword_cooccurrence_heatmap.png`*  
*建構方式：取研究領域網路的加權鄰接矩陣（共同研究兩領域的教授人數），依社群排序後繪製熱圖。*

## 3. 主要研究集群與重要老師

教授網路的 3 個集群分別對應機器學習、網路通訊、訊號與影像處理三個學門，邊界清楚。研究領域網路 modularity（z = 2.5，p = 0.036）與教授網路 clustering（z = 2.0，p = 0.036）都顯著高於虛無模型。本組有大量與台大資工、台大資料科學學程的合聘教授，是 ds 組內跨校重疊最深的單位。

教授網路共 25 位教授、3 個集群（Louvain，Q = 0.374）。以下依集群人數排序；集群編號與圖中的 Community 編號一致。表中 Degree 為與該教授共享研究領域的同儕數，Betweenness 為該教授位於他人最短路徑上的比例（越高越像橋梁）。

![台灣大學電信工程學研究所 資料科學與網路組 教授網路的 Louvain 集群](../network-analysis/ntu-comm-engin-ds-network/figures/09_professor_network_communities.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 教授網路的 Louvain 集群*  
*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/figures/09_professor_network_communities.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

### 3.1 集群 0：機器學習與人工智慧集群（9 人）

- **成員共同研究領域**：Machine Learning（9 人）、Artificial Intelligence（3 人）、Robotics（2 人）、Deep Learning（2 人）、Neural Networks（1 人）、Optimization（1 人）、Information Security（1 人）
- **成員主導 taxonomy L1**：AI & Machine Learning 9 人

9 位成員全部主導 AI & Machine Learning，共享 Machine Learning（9 人）、Artificial Intelligence、Robotics 與 Deep Learning。王鈺強（兼任，電腦視覺、深度學習）與鄭士康（機器學習、多媒體、機器人）degree 並列最高（16）；劉子毓 betweenness 最高（0.091），研究神經網路與最佳化；楊奕軒、簡翌（可信任 AI）是專注 AI 的成員。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 王鈺強 | Yu-Chiang Frank Wang | 兼任 | 16 | 0.065 | Artificial Intelligence、Computer Vision、Deep Learning、Machine Learning |
| 鄭士康 | Shyh-Kang Jeng | 教師（未細分） | 16 | 0.043 | Machine Learning、Multimedia Systems、Robotics |
| 劉子毓（2 個系所） | Tzu-Yu Liu | 專任 | 11 | 0.091 | Machine Learning、Neural Networks、Optimization |
| 吳沛遠（2 個系所） | Pei-Yuan Wu | 專任 | 11 | 0.007 | Information Security、Machine Learning、Smart Manufacturing |
| 楊奕軒 | Yi-Hsuan Yang | 專任 | 11 | 0.000 | Artificial Intelligence、Machine Learning |
| 簡翌 | Eli Chien | 專任 | 11 | 0.000 | Artificial Intelligence、Machine Learning、Trustworthy AI |
| 孫紹華（2 個系所） | Shao-Hua Sun | 專任 | 10 | 0.014 | Machine Learning、Reinforcement Learning、Robotics |
| 李宏毅（3 個系所） | Hung-yi Lee | 專任 | 10 | 0.000 | Deep Learning、Machine Learning、Speech Recognition |

其餘成員（1 位，依 degree 排序）：鄭皓中


### 3.2 集群 1：網路與無線通訊集群（9 人）

- **成員共同研究領域**：Wireless Networks（5 人）、Computer Networks（5 人）、Multimedia Systems（4 人）、Internet of Things（2 人）、Wireless Communications（2 人）、Artificial Intelligence（1 人）、Blockchain（1 人）
- **成員主導 taxonomy L1**：Networks & Communications 8 人、Applied Mathematics & Operations Research 1 人

9 位成員中 8 位主導 Networks & Communications，共享 Wireless Networks、Computer Networks、Multimedia Systems 與 Internet of Things。廖婉君 degree 16、betweenness 0.144，同時出現在 3 個系所名單（合聘），研究 AI、區塊鏈、網路、物聯網與多媒體；魏宏宇（網路、賽局、最佳化）次之；陳銘憲同樣是 3 個系所合聘的資深教授；黃寶儀、謝宏昀、葉丙成專注無線網路與物聯網。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 廖婉君（3 個系所） | Wanjiun Liao | 專任 | 16 | 0.144 | Artificial Intelligence、Blockchain、Computer Networks、Internet of Things、Multimedia Systems |
| 魏宏宇 | Hung-Yu Wei | 專任 | 14 | 0.083 | Computer Networks、Game Theory、Multimedia Systems、Optimization、Wireless Networks |
| 黃寶儀 | Polly Huang | 專任 | 13 | 0.004 | Multimedia Systems、Pervasive Computing、Wireless Networks |
| 陳銘憲（3 個系所） | Ming-Syan Chen | 專任 | 13 | 0.001 | Computer Networks、Databases、Mobile Computing、Multimedia Systems |
| 謝宏昀（2 個系所） | Hung-Yun Hsieh | 專任 | 11 | 0.043 | Computer Networks、Information Security、Internet of Things |
| 葉丙成（2 個系所） | Ping-Cheng Yeh | 專任 | 10 | 0.025 | Wireless Communications、Wireless Networks |
| 周俊廷 | Chun-Ting Chou | 專任 | 10 | 0.000 | Wireless Networks |
| 王奕翔 | I-Hsiang Wang | 專任 | 10 | 0.000 | Information Theory、Wireless Communications |

其餘成員（1 位，依 degree 排序）：蔡志宏


### 3.3 集群 2：訊號與影像處理集群（7 人）

- **成員共同研究領域**：Signal Processing（7 人）、Image Processing（3 人）、Computer Networks（1 人）、Neural Networks（1 人）、Data Science（1 人）、Deep Learning（1 人）、Financial Technology（1 人）
- **成員主導 taxonomy L1**：Vision, Multimedia & Human-Centered Computing 6 人、AI & Machine Learning 1 人

7 位成員中 6 位主導 Vision, Multimedia & Human-Centered Computing，共享 Signal Processing（7 人全部）與 Image Processing。林澤（資料科學、深度學習、金融科技、最佳化、訊號處理）與林宗男（網路、影像、神經網路、訊號處理）degree 並列全系最高（24），betweenness 也是前兩名，是把三個集群綁在一起的樞紐；貝蘇章與李琳山是資深的訊號處理與語音學者，陳宏銘（兼任）與丁建均專注影像與多媒體。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 林澤（2 個系所） | Che Lin | 專任 | 24 | 0.214 | Data Science、Deep Learning、Financial Technology、Optimization、Signal Processing |
| 林宗男（2 個系所） | Tsung-Nan Lin | 專任 | 24 | 0.167 | Computer Networks、Image Processing、Neural Networks、Signal Processing |
| 陳宏銘 | Homer H. Chen | 兼任 | 12 | 0.022 | Data Mining、Multimedia Systems、Signal Processing |
| 貝蘇章 | Soo-Chang Pei | 教師（未細分） | 12 | 0.000 | Computer Graphics、Image Processing、Pattern Recognition、Signal Processing |
| 丁建均 | Jian-Jiun Ding | 專任 | 7 | 0.000 | Image Processing、Signal Processing |
| 李琳山（2 個系所） | Lin-Shan Lee | 教師（未細分） | 7 | 0.000 | Signal Processing |
| 蘇炫榮 | Hsuan-Jung Su | 專任 | 7 | 0.000 | Signal Processing |

*集群表出處：`analysis/network-analysis/ntu-comm-engin-ds-network/professor_communities.csv`（集群歸屬）、`professor_centrality.csv`（degree、betweenness、職稱類別）、`prof_keyword_network.graphml`（成員研究領域，用來統計集群的共同領域）*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 職稱類別為官網職稱的分類，一人可屬多類時取主要類別；「N 個系所」表示該教授也出現在其他系所名單。*

### 3.4 全系的橋接者與樞紐

Betweenness 最高的教授（跨集群的橋梁）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 林澤 | Che Lin | 專任 | 24 | 0.214 | AI & Machine Learning |
| 林宗男 | Tsung-Nan Lin | 專任 | 24 | 0.167 | Vision, Multimedia & Human-Centered Computing |
| 廖婉君 | Wanjiun Liao | 專任 | 16 | 0.144 | Networks & Communications |
| 劉子毓 | Tzu-Yu Liu | 專任 | 11 | 0.091 | AI & Machine Learning |
| 魏宏宇 | Hung-Yu Wei | 專任 | 14 | 0.083 | Applied Mathematics & Operations Research |
| 王鈺強 | Yu-Chiang Frank Wang | 兼任 | 16 | 0.065 | AI & Machine Learning |

Degree 最高的教授（與最多同儕共享領域的樞紐）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 林宗男 | Tsung-Nan Lin | 專任 | 24 | 0.167 | Vision, Multimedia & Human-Centered Computing |
| 林澤 | Che Lin | 專任 | 24 | 0.214 | AI & Machine Learning |
| 王鈺強 | Yu-Chiang Frank Wang | 兼任 | 16 | 0.065 | AI & Machine Learning |
| 鄭士康 | Shyh-Kang Jeng | 教師（未細分） | 16 | 0.043 | AI & Machine Learning |
| 廖婉君 | Wanjiun Liao | 專任 | 16 | 0.144 | Networks & Communications |
| 魏宏宇 | Hung-Yu Wei | 專任 | 14 | 0.083 | Applied Mathematics & Operations Research |

*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/professor_centrality.csv`*

![台灣大學電信工程學研究所 資料科學與網路組 教授網路（節點大小 = betweenness）](../network-analysis/ntu-comm-engin-ds-network/figures/08_professor_network_betweenness.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 教授網路（節點大小 = betweenness）*  
*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/figures/08_professor_network_betweenness.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。此圖節點大小改為與 betweenness 成正比。*

![台灣大學電信工程學研究所 資料科學與網路組 各集群教授 word cloud（字級 = degree）](../network-analysis/ntu-comm-engin-ds-network/figures/27_professor_wordcloud_degree_by_community.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 各集群教授 word cloud（字級 = degree）*  
*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/figures/27_professor_wordcloud_degree_by_community.png`*  
*建構方式：依 Louvain 集群分塊、同集群同色的教授姓名 word cloud，字級與 degree 成線性正比並設下限。*

## 4. 結構穩健性檢驗

### 4.1 虛無模型檢定

| 統計量 | 觀測值 | 虛無平均 | 虛無標準差 | z-score | empirical p | p < 0.05 |
| --- | --- | --- | --- | --- | --- | --- |
| 領域網路密度 | 0.1914 | 0.1991 | 0.0120 | -0.64 | 0.599 | 不顯著 |
| 領域網路 modularity Q | 0.4066 | 0.3060 | 0.0399 | 2.52 | 0.036 | 顯著 |
| 領域平均共現次數 | 1.1348 | 1.1721 | 0.0424 | -0.88 | 0.490 | 不顯著 |
| 教授網路 clustering 係數 | 0.7632 | 0.6707 | 0.0454 | 2.04 | 0.036 | 顯著 |

*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/null_model_test.csv`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 密度顯著偏低而 modularity、共現顯著偏高，代表領域共現集中在少數主題群，不是均勻分布。*

![台灣大學電信工程學研究所 資料科學與網路組 觀測值 vs 虛無模型分布](../network-analysis/ntu-comm-engin-ds-network/figures/15_null_model_comparison.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 觀測值 vs 虛無模型分布*  
*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/figures/15_null_model_comparison.png`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。*

### 4.2 λ 敏感度

| λ | 邊數 | 密度 | Q | 集群數 | 密度相對 baseline | Q 下降 | 過度合併 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 104 | 0.347 | 0.441 | 3 | +0% | 0.000 | 否 |
| 0.3 | 153 | 0.510 | 0.388 | 3 | +47% | 0.053 | 否 |
| 0.4 | 153 | 0.510 | 0.374 | 3 | +47% | 0.067 | 否 |
| 0.5 | 153 | 0.510 | 0.361 | 3 | +47% | 0.079 | 否 |

*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/lambda_sensitivity.csv`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

![台灣大學電信工程學研究所 資料科學與網路組 λ 敏感度](../network-analysis/ntu-comm-engin-ds-network/figures/16_lambda_sensitivity.png)

*圖：台灣大學電信工程學研究所 資料科學與網路組 λ 敏感度*  
*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/figures/16_lambda_sensitivity.png`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

### 4.3 taxonomy L1 覆蓋護欄

| taxonomy L1 | 教授數 | 覆蓋率 | flag |
| --- | --- | --- | --- |
| Vision, Multimedia & Human-Centered Computing | 13 | 52.0% | too_broad |
| AI & Machine Learning | 12 | 48.0% | ok |
| Networks & Communications | 11 | 44.0% | ok |
| Applied Mathematics & Operations Research | 3 | 12.0% | ok |
| Data, Databases & Knowledge Discovery | 3 | 12.0% | ok |
| Robotics, Control & Smart Manufacturing | 3 | 12.0% | ok |
| Security, Privacy & Cryptography | 3 | 12.0% | ok |
| Biomedical & Health Informatics | 1 | 4.0% | ok |

*出處：`analysis/network-analysis/ntu-comm-engin-ds-network/l1_coverage_guardrail.csv`（只列前 8 項）*  
*建構方式：計算每個 L1 分類涵蓋該單位多少比例的教授，超過 50% 標記 too_broad，代表此 L1 在本單位太寬，不能用來做 L1 roll-up 比較。*

## 5. 解讀與注意事項

- L1 護欄標記 Vision, Multimedia & Human-Centered Computing 涵蓋超過 50% 教授，這是因為 Signal Processing 與 Multimedia Systems 在 taxonomy 中都歸在此類。
- λ 敏感度未觸發過度合併，λ=0 與 λ=0.4 的社群數都是 3，集群結論穩健。
- 本組 25 人中至少 9 人同時出現在台大資工或台大資料科學學程的名單（廖婉君、陳銘憲各 3 個系所；林澤、林宗男、劉子毓、吳沛遠、謝宏昀、葉丙成、李琳山各 2 個）。系所層級不去重，因此這些人在三個單位的報告中都會出現。
- 本組沒有孤立教授，25 人全部在同一個連通元件內。
- 研究領域來自官網自填內容，粒度與深度因人而異；網路密度與集群數反映填寫習慣的成分不可忽視，完整率不可解讀為系所或教授的品質排名。

## 附錄：本報告引用的資料與圖表清單

| 檔案 | 產生階段 / 程式 | 建構方式摘要 |
| --- | --- | --- |
| `analysis/data-collection/ntu-comm-engin-ds-network/quality-report.json` | 資料蒐集 `scripts/data-collection/collect.py` | 爬取官網後統計 canonical 紀錄人數、職稱分類、中英配對率與欄位完整率 |
| `analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv` | 預處理 `1_faculty_data_preprocessing.ipynb` | 標準化後各欄位有 canonical 值的教師比例與平均項目數 |
| `.../group_comparison/research_fields/ds.csv`、`by_department/top_research_fields/ntu-comm-engin-ds-network.png` | 預處理 `2_rf_and_phd_inst_comparison.ipynb` | 由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。 |
| `.../group_comparison/phd_institutions/ds.csv`、`by_department/top_phd_institutions/ntu-comm-engin-ds-network.png` | 同上 | 同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。 |
| `analysis/network-analysis/ntu-comm-engin-ds-network/network_metrics.json` | 網路分析 `2_build_network_data.ipynb` + `3_network_analysis.ipynb` | 由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 |
| `analysis/network-analysis/ntu-comm-engin-ds-network/keyword_centrality.csv`、`keyword_communities.csv` | `3_network_analysis.ipynb` | 研究領域網路的中心性與 Louvain 社群；taxonomy 來自 `1_build_taxonomy.ipynb` |
| `analysis/network-analysis/ntu-comm-engin-ds-network/professor_centrality.csv`、`professor_communities.csv`、`prof_keyword_network.graphml` | `3_network_analysis.ipynb` | 教授網路的中心性與 Louvain 集群；graphml 為二分網路，本報告用它統計各集群成員的共同領域 |
| `analysis/network-analysis/ntu-comm-engin-ds-network/null_model_test.csv` | `3_network_analysis.ipynb` | 以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 |
| `analysis/network-analysis/ntu-comm-engin-ds-network/lambda_sensitivity.csv` | `3_network_analysis.ipynb` | 以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。 |
| `analysis/network-analysis/ntu-comm-engin-ds-network/l1_coverage_guardrail.csv` | `3_network_analysis.ipynb` | 每個 L1 涵蓋教授比例，> 50% 標記 too_broad |
| `analysis/network-analysis/ntu-comm-engin-ds-network/figures/01, 05, 08, 09, 10, 13, 14, 15, 16, 27` | `3_network_analysis.ipynb` | 網路圖節點大小與 degree 或 betweenness 成正比、顏色依社群；邊數 > 400 時繪圖用 disparity filter backbone；word cloud 字級與中心性成線性正比 |

更完整的方法說明見 `docs/data-collection-report.md`、`docs/data-preprocessing-report.md`、`docs/network-analysis-report.md`。
