# 陽明交通大學資訊工程學系（資訊學院）（`nycu-cs`）研究結果總結報告

所屬分組：資工組（cs）　｜　資料日期：2026-09-09 蒐集、2026-09-10 完成網路分析

> **本報告的資料來源**
> 本專案分三個階段：(1) 資料蒐集（`scripts/data-collection/`）從 14 個系所官網爬取師資的姓名、職稱、學歷與研究領域，中英文分開蒐集後配對；
> (2) 資料預處理（`scripts/data-preprocessing/`）把職稱、學歷、研究領域標準化成英文 canonical 值，並產生描述統計；
> (3) 網路分析（`scripts/network-analysis/current-version/`）建立「教授–研究領域」二分網路，投影成研究領域網路與教授網路，做社群偵測、中心性、虛無模型與敏感度分析。
> 本報告所有數字、表格與圖表都取自 `analysis/` 底下這三個階段的輸出，每張圖表下方都標明出處與建構方式，附錄另有完整清單。
> 「研究集群」指教授網路的 Louvain 社群；「重要老師」依教授在該網路中的 degree（與多少同儕共享領域）與 betweenness（是否位於集群之間的橋梁位置）判定，**不是**學術成就的排名。

## 1. 科系速覽

陽明交大資訊學院官網列出 152 位教師，是 14 個系所中規模最大的單位（含名譽 33 位、講座／主管 29 位）。研究輪廓以 AI 為絕對核心：Artificial Intelligence 35 人、Machine Learning 21 人、Deep Learning 16 人、Computer Vision 15 人、Image Processing 14 人，其次是 Computer Networks、Algorithms、Multimedia Systems（各 12 人）、Internet of Things（11 人）、Embedded Systems（10 人）。研究領域完整率 92.8%，學歷完整率 100%。博士畢業學校以交大本校（29 人）與台大（21 人）最多，其次是 Northwestern 與清大（各 8 人）、Purdue（7 人），是**本校博士比例最高**的系所。

### 1.1 基本資料

| 項目 | 數值 |
| --- | --- |
| 官網師資人數（canonical 紀錄） | 152 |
| 職稱分類（一人可屬多類） | 教師（未細分） 57、專任 41、名譽／退休 33、主管／講座 29、客座 4、合聘 1、專案 1 |
| 中英文紀錄配對率 | 100.0% |
| 研究領域完整率（標準化後） | 92.8% |
| 學歷完整率（標準化後） | 99.3% |
| 每位教授平均研究領域數 | 2.78 |
| 進入網路分析的教授數 | 141（11 位因無研究領域排除） |

*出處：`analysis/data-collection/nycu-cs/quality-report.json`（人數、職稱、配對率）、`analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv`（完整率）、`analysis/network-analysis/nycu-cs/network_metrics.json`（進入網路人數）*  
*建構方式：quality-report 由 `scripts/data-collection/collect.py` 在爬取官網後統計 canonical 紀錄的職稱分類與中英配對；coverage 由 `1_faculty_data_preprocessing.ipynb` 計算標準化後有 canonical 值的教師比例。*

### 1.2 主要研究領域

| 排名 | 研究領域（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | Artificial Intelligence | 35 |
| 2 | Machine Learning | 21 |
| 3 | Deep Learning | 16 |
| 4 | Computer Vision | 15 |
| 5 | Image Processing | 14 |
| 6 | Computer Networks | 12 |
| 7 | Algorithms | 12 |
| 8 | Multimedia Systems | 12 |
| 9 | Internet of Things | 11 |
| 10 | Embedded Systems | 10 |
| 11 | Information Security | 9 |
| 12 | Operating Systems | 9 |
| 13 | Bioinformatics | 9 |
| 14 | Data Mining | 9 |
| 15 | Human-Computer Interaction | 8 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/research_fields/cs.csv`（`nycu-cs` 欄）*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

![陽明交通大學資訊工程學系（資訊學院） 研究領域人數](../descriptive-stats-after-preprocessing/by_department/top_research_fields/nycu-cs.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 研究領域人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_research_fields/nycu-cs.png`*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

### 1.3 博士畢業學校

| 排名 | 博士畢業學校（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | National Chiao Tung University | 29 |
| 2 | National Taiwan University | 21 |
| 3 | Northwestern University | 8 |
| 4 | National Tsing Hua University | 8 |
| 5 | Purdue University | 7 |
| 6 | University of Illinois Urbana-Champaign | 6 |
| 7 | University of Washington | 4 |
| 8 | University of Maryland, College Park | 4 |
| 9 | National Cheng Kung University | 4 |
| 10 | University of California, Los Angeles | 3 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/phd_institutions/cs.csv`（`nycu-cs` 欄）*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

![陽明交通大學資訊工程學系（資訊學院） 博士畢業學校人數](../descriptive-stats-after-preprocessing/by_department/top_phd_institutions/nycu-cs.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 博士畢業學校人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_phd_institutions/nycu-cs.png`*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

## 2. 研究領域網路結構

### 2.1 網路指標

| 指標 | 數值 | 說明 |
| --- | --- | --- |
| 二分網路：教授數 / 領域數 / 邊數 | 141 / 88 / 423 | 一條邊 = 一位教授研究一個領域 |
| 二分網路連通元件數 | 2 | 最大元件涵蓋 99.3% 教授 |
| 每位教授平均 / 最多領域數 | 3.00 / 7 |  |
| 研究領域網路：節點 / 邊 | 87 / 366 | 只含至少與一個其他領域共現的領域 |
| 研究領域網路密度 | 0.098 | 實際邊數 ÷ 可能邊數 |
| 研究領域網路平均 degree | 8.41 |  |
| 研究領域網路 modularity Q（Louvain） | 0.386 | 7 個社群；resolution 0.7 / 1.3 時為 4 / 8 個 |
| 領域社群 vs taxonomy L1 一致度 | NMI 0.484 / ARI 0.206 | 1 = 完全一致，0 = 無關 |
| 教授網路：節點 / 邊 | 140 / 2524 | 只含最大連通元件 |
| 教授網路密度 | 0.259 |  |
| 教授網路 modularity Q（Louvain） | 0.350 | 5 個集群 |
| 教授集群 vs 主導 L1 一致度 | NMI 0.557 / ARI 0.389 |  |

*出處：`analysis/network-analysis/nycu-cs/network_metrics.json`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

![陽明交通大學資訊工程學系（資訊學院） 教授–研究領域二分網路](../network-analysis/nycu-cs/figures/01_bipartite_network.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 教授–研究領域二分網路*  
*出處：`analysis/network-analysis/nycu-cs/figures/01_bipartite_network.png`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。圖中兩類節點以不同顏色區分，節點大小與 degree 成正比；邊數超過 400 時繪圖使用 disparity filter backbone（α = 0.05），指標仍以完整圖計算。*

### 2.2 關鍵研究領域

| 研究領域 | Degree | Degree centrality | Betweenness | PageRank | 教授數 | taxonomy L1 |
| --- | --- | --- | --- | --- | --- | --- |
| Artificial Intelligence | 43 | 0.500 | 0.596 | 0.0710 | 35 | AI & Machine Learning |
| Machine Learning | 33 | 0.384 | 0.161 | 0.0453 | 21 | AI & Machine Learning |
| Deep Learning | 28 | 0.326 | 0.145 | 0.0420 | 16 | AI & Machine Learning |
| Computer Networks | 22 | 0.256 | 0.046 | 0.0223 | 12 | Networks & Communications |
| Internet of Things | 21 | 0.244 | 0.054 | 0.0243 | 11 | Networks & Communications |
| Algorithms | 19 | 0.221 | 0.057 | 0.0234 | 12 | Theory & Algorithms |
| Multimedia Systems | 18 | 0.209 | 0.079 | 0.0206 | 12 | Vision, Multimedia & Human-Centered Computing |
| Data Mining | 18 | 0.209 | 0.150 | 0.0255 | 9 | Data, Databases & Knowledge Discovery |
| Computer Vision | 18 | 0.209 | 0.068 | 0.0334 | 15 | Vision, Multimedia & Human-Centered Computing |
| Information Security | 17 | 0.198 | 0.071 | 0.0215 | 9 | Security, Privacy & Cryptography |
| Image Processing | 17 | 0.198 | 0.093 | 0.0324 | 14 | Vision, Multimedia & Human-Centered Computing |
| Big Data Analytics | 15 | 0.174 | 0.001 | 0.0177 | 6 | Data, Databases & Knowledge Discovery |

Betweenness 最高的五個領域：Artificial Intelligence（0.60）、Machine Learning（0.16）、Data Mining（0.15）、Deep Learning（0.15）、Image Processing（0.09）。Betweenness 高代表該領域位於不同主題群之間的連結位置，是系上跨主題的共同語言。

*出處：`analysis/network-analysis/nycu-cs/keyword_centrality.csv`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。 degree 為相連領域數，betweenness 為經過該節點的最短路徑比例，PageRank 為加權隨機漫步的穩態機率；parent_l1 來自 `1_build_taxonomy.ipynb` 手工編定的三層 taxonomy（170 個 L3、46 個 L2、16 個 L1）。*

![陽明交通大學資訊工程學系（資訊學院） 研究領域教授人數長條圖](../network-analysis/nycu-cs/figures/10_top_keywords_bar.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 研究領域教授人數長條圖*  
*出處：`analysis/network-analysis/nycu-cs/figures/10_top_keywords_bar.png`*  
*建構方式：以二分網路中每個領域節點的 degree（研究該領域的教授數）排序繪製。*

### 2.3 研究領域社群

| 社群 | 領域數 | 主要領域（教授人數） | 主要 taxonomy L1（領域數） |
| --- | --- | --- | --- |
| 0 | 24 | Computer Networks（12）、Algorithms（12）、Internet of Things（11）、Information Security（9）、Optimization（7）、Wireless Networks（7）、Mobile Computing（7） | Networks & Communications 7、Theory & Algorithms 5、Security, Privacy & Cryptography 4 |
| 1 | 14 | Artificial Intelligence（35）、Data Mining（9）、Big Data Analytics（6）、Medical Informatics（4）、Smart Healthcare（4）、Reinforcement Learning（2）、Time Series Analysis（2） | Data, Databases & Knowledge Discovery 4、AI & Machine Learning 3、Biomedical & Health Informatics 2 |
| 2 | 13 | Machine Learning（21）、Deep Learning（16）、Computer Vision（15）、Image Processing（14）、Multimedia Systems（12）、Pattern Recognition（8）、Signal Processing（6） | Vision, Multimedia & Human-Centered Computing 6、AI & Machine Learning 4、Biomedical & Health Informatics 1 |
| 3 | 13 | Bioinformatics（9）、Statistics（6）、Biostatistics（3）、Scientific Computing（3）、Statistical Inference（2）、Systems Biology（2）、Causal Inference（1） | Statistics & Statistical Methods 7、Biomedical & Health Informatics 4、Applied Mathematics & Operations Research 1 |
| 4 | 10 | Embedded Systems（10）、Operating Systems（9）、Computer Architecture（8）、Parallel Computing（7）、Systems Security（5）、Compilers（5）、Storage Systems（3） | Systems, Software & Architecture 7、Security, Privacy & Cryptography 1、Data, Databases & Knowledge Discovery 1 |
| 5 | 7 | Human-Computer Interaction（8）、Computer Graphics（7）、Virtual Reality（6）、Robotics（5）、Augmented Reality（4）、Information Visualization（1）、Social Media Analytics（1） | Vision, Multimedia & Human-Centered Computing 5、Robotics, Control & Smart Manufacturing 1、Data, Databases & Knowledge Discovery 1 |
| 6 | 6 | Databases（5）、Information Retrieval（4）、Natural Language Processing（3）、Privacy-Preserving Computing（2）、Web Mining（1）、Computational Linguistics（1） | Data, Databases & Knowledge Discovery 3、AI & Machine Learning 2、Security, Privacy & Cryptography 1 |

*出處：`analysis/network-analysis/nycu-cs/keyword_communities.csv`（`community` 欄）、`keyword_centrality.csv`（教授人數）*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。*

![陽明交通大學資訊工程學系（資訊學院） 研究領域網路的 Louvain 社群](../network-analysis/nycu-cs/figures/05_keyword_network_communities.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 研究領域網路的 Louvain 社群*  
*出處：`analysis/network-analysis/nycu-cs/figures/05_keyword_network_communities.png`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。節點顏色為社群，大小與 degree 成正比。*

![陽明交通大學資訊工程學系（資訊學院） 各研究領域社群的 taxonomy L1 組成](../network-analysis/nycu-cs/figures/14_community_composition.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 各研究領域社群的 taxonomy L1 組成*  
*出處：`analysis/network-analysis/nycu-cs/figures/14_community_composition.png`*  
*建構方式：把每個 Louvain 領域社群內的領域依 taxonomy L1 分類計數，堆疊長條圖。用來檢查資料驅動的社群是否對應人工分類。*

![陽明交通大學資訊工程學系（資訊學院） 研究領域共現熱圖](../network-analysis/nycu-cs/figures/13_keyword_cooccurrence_heatmap.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 研究領域共現熱圖*  
*出處：`analysis/network-analysis/nycu-cs/figures/13_keyword_cooccurrence_heatmap.png`*  
*建構方式：取研究領域網路的加權鄰接矩陣（共同研究兩領域的教授人數），依社群排序後繪製熱圖。*

## 3. 主要研究集群與重要老師

教授網路分成 5 個集群，其中「網路與系統」集群就有 51 人。四個虛無模型統計量全部高度顯著（密度 z = -7.7、modularity z = 10.0、平均共現 z = 13.3、教授 clustering z = 4.8），是 14 個系所中主題結構最強的單位。Artificial Intelligence 的 betweenness（0.60）遠高於其他領域，是整個學院的共同樞紐。

教授網路共 140 位教授、5 個集群（Louvain，Q = 0.350）。以下依集群人數排序；集群編號與圖中的 Community 編號一致。表中 Degree 為與該教授共享研究領域的同儕數，Betweenness 為該教授位於他人最短路徑上的比例（越高越像橋梁）。

![陽明交通大學資訊工程學系（資訊學院） 教授網路的 Louvain 集群](../network-analysis/nycu-cs/figures/09_professor_network_communities.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 教授網路的 Louvain 集群*  
*出處：`analysis/network-analysis/nycu-cs/figures/09_professor_network_communities.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

### 3.1 集群 0：網路、系統與嵌入式集群（51 人）

- **成員共同研究領域**：Computer Networks（10 人）、Operating Systems（9 人）、Embedded Systems（9 人）、Internet of Things（8 人）、Computer Architecture（7 人）、Wireless Networks（7 人）、Multimedia Systems（7 人）
- **成員主導 taxonomy L1**：Networks & Communications 21 人、Systems, Software & Architecture 18 人、AI & Machine Learning 3 人、Security, Privacy & Cryptography 3 人、Data, Databases & Knowledge Discovery 3 人、Information Systems & Management 2 人、Theory & Algorithms 1 人

51 位成員，主導 taxonomy 為 Networks & Communications（21）與 Systems, Software & Architecture（18），共享 Computer Networks、Operating Systems、Embedded Systems、Internet of Things、Computer Architecture 與 Wireless Networks。王協源 degree 73（數位孿生、邊緣運算、物聯網、網路安全）為集群最高；蔡文錦、林政寬（分散式系統、圖論、無線網路）、吳俊峯（架構、作業系統、儲存系統）、謝秉均（強化學習、最佳化、無線網路）是主要成員。這個集群人數多、主題寬，在較高 resolution 下會分成網路與系統兩群。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 王協源 | Shie-Yuan Wang | 教師（未細分） | 73 | 0.022 | Digital Twins、Edge Computing、Internet of Things、Machine Learning、Network Security |
| 蔡文錦 | W. J. Tsai | 專任 | 65 | 0.004 | Embedded Systems、Machine Learning、Multimedia Systems |
| 林政寬 | Cheng-Kuan Lin | 專任 | 63 | 0.011 | Artificial Intelligence、Distributed Systems、Graph Theory、Wireless Networks |
| 吳俊峯 | Chun-Feng Wu | 專任 | 59 | 0.031 | Artificial Intelligence、Computer Architecture、Operating Systems、Storage Systems |
| 謝秉均 | Ping-Chun Hsieh | 專任 | 57 | 0.012 | Bayesian Statistics、Optimization、Reinforcement Learning、Wireless Networks |
| 蔡文能 | Wen-Nung Tsai | 名譽／退休 | 52 | 0.035 | Computer Networks、Mobile Computing、Network Security、Operating Systems |
| 單智君 | Jean Jyh-Jiun Shann | 專任 | 52 | 0.030 | Compilers、Computer Architecture、Embedded Systems、Information Retrieval、Parallel Computing |
| 王國禎 | Kuo-Chen Wang | 名譽／退休 | 50 | 0.049 | Big Data Analytics、Cloud Computing、Computer Networks、Internet of Things、Mobile Computing |

其餘成員（43 位，依 degree 排序）：張瑞川、蕭旭峰、黃俊穎、許富皓、曹孝櫟、李素瑛、林寶樹、杜宏章、鍾崇斌、陳耀宗、蔡淳仁、楊武、陳志成、蔡孟勳、陳秋媛、黃廷祿、李奇育、游逸平、吳育松、嚴力行、陳添福、陳逸萍、陳碩漢、鍾乾癸、楊啟瑞、李毅郎、蔡中川、黃世昆、趙禧綠、曾建超、陳健、張立平、林一平、張明峰、陳正、王豐堅、陳昌居、張庭榕、曾憲雄、袁賢銘、黃國安、謝志鴻、千本倖生


### 3.2 集群 1：人工智慧與資料探勘集群（36 人）

- **成員共同研究領域**：Artificial Intelligence（30 人）、Data Mining（9 人）、Machine Learning（8 人）、Deep Learning（6 人）、Information Security（5 人）、Smart Healthcare（4 人）、Big Data Analytics（4 人）
- **成員主導 taxonomy L1**：AI & Machine Learning 28 人、Data, Databases & Knowledge Discovery 5 人、Security, Privacy & Cryptography 1 人、Information Systems & Management 1 人、Biomedical & Health Informatics 1 人

36 位成員，28 位主導 AI & Machine Learning，共享 Artificial Intelligence（30 人）、Data Mining、Machine Learning、Deep Learning、Information Security 與 Smart Healthcare。李宗夷 degree 75 為全系最高（演算法、AI、大數據、生物資訊、資料探勘）；吳凱強（AI、EDA、資安）次之；廖弘源與曾煜棋（講座教授）、傅心家（名譽）是資深核心；集群內多位教授研究智慧醫療與醫學資訊。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 李宗夷 | Tzong-Yi Lee | 教師（未細分） | 75 | 0.075 | Algorithms、Artificial Intelligence、Big Data Analytics、Bioinformatics、Data Mining |
| 吳凱強 | Kai-Chiang Wu | 教師（未細分） | 72 | 0.026 | Artificial Intelligence、Automation and Control、Deep Learning、Electronic Design Automation、Information Security |
| 廖弘源 | Mark Liao | 主管／講座 | 69 | 0.003 | Artificial Intelligence、Machine Learning、Multimedia Systems |
| 傅心家 | Hsin-Chia Fu | 名譽／退休 | 69 | 0.001 | Artificial Intelligence、Multimedia Systems、Neural Networks |
| 曾煜棋 | Yu-Chee Tseng | 主管／講座 | 67 | 0.011 | Artificial Intelligence、Internet of Things、Machine Learning |
| 魏佑霖 | Yu-Lin Wei | 專任 | 67 | 0.010 | Artificial Intelligence、Generative AI、Internet of Things、Signal Processing |
| 楊博凱 | Po-Kai Yang | 專任 | 66 | 0.038 | Artificial Intelligence、Deep Learning、Human-Computer Interaction、Smart Healthcare、Time Series Analysis |
| 游家牧（2 個系所） | Chia-Mu Yu | 專任 | 66 | 0.022 | Artificial Intelligence、Cryptography、Deep Learning、Information Security |

其餘成員（28 位，依 degree 排序）：胡毓志、陳奕廷、林寰鐸、丁羅邦芸、葉國暉、顏安孜、彭文志、黃泰一、吳毅成、蒙以亨、謝續平、彭文孝、曾意儒、林得勝、曾新穆、余孝先、顏羽君、范俊逸、葉宗泰、梁伯嵩、何信瑩、白培霖 Pai, Pei-Lin、李嘉晃、林盈達、黃俊龍、俞士綸、梁婷、古倫維


### 3.3 集群 2：電腦視覺、影像與人機互動集群（31 人）

- **成員共同研究領域**：Image Processing（14 人）、Computer Vision（13 人）、Deep Learning（10 人）、Machine Learning（9 人）、Pattern Recognition（8 人）、Virtual Reality（6 人）、Human-Computer Interaction（6 人）
- **成員主導 taxonomy L1**：Vision, Multimedia & Human-Centered Computing 20 人、AI & Machine Learning 10 人、Biomedical & Health Informatics 1 人

31 位成員，20 位主導 Vision, Multimedia & Human-Centered Computing，共享 Image Processing、Computer Vision、Deep Learning、Machine Learning、Pattern Recognition、Virtual Reality 與 Human-Computer Interaction。黃春融 degree 75、betweenness 0.11 為全系最高（AI、電腦視覺、深度學習、影像、醫學影像）；洪瑞鴻（生物資訊、影像、平行計算）betweenness 次之；林彥宇、蔡文祥（講座教授）是視覺與影像的資深核心；集群內也包含 VR／AR 與電腦圖學的教授。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 黃春融 | Chun-Rong Huang | 教師（未細分） | 75 | 0.110 | Artificial Intelligence、Computer Vision、Deep Learning、Image Processing、Medical Imaging |
| 洪瑞鴻 | Jui-Hung Hung | 教師（未細分） | 69 | 0.100 | Algorithms、Bioinformatics、Deep Learning、Image Processing、Parallel Computing |
| 林彥宇 | Yen-Yu Lin | 主管／講座 | 63 | 0.005 | Artificial Intelligence、Computer Vision、Deep Learning、Machine Learning |
| 陳昱芝 | Yu-Chih Chen | 專任 | 63 | 0.003 | Artificial Intelligence、Computer Vision、Deep Learning、Image Processing |
| 蔡文祥 | Wen-Hsiang Tsai | 主管／講座 | 58 | 0.015 | Computer Vision、Image Processing、Information Security、Neural Networks、Pattern Recognition |
| 黃敬群 | Ching-Chun Huang | 教師（未細分） | 57 | 0.063 | Augmented Reality、Deep Learning、Image Processing、Machine Learning、Medical Imaging |
| 范倫達 | Lan-Da Van | 教師（未細分） | 56 | 0.003 | Algorithms、Machine Learning、Signal Processing |
| 魏群樹 | Chun-Shu Wei | 專任 | 54 | 0.000 | Brain-Computer Interfaces、Machine Learning、Signal Processing |

其餘成員（23 位，依 degree 排序）：黃正能、易志偉、邱維辰、黃國源、王才沛、劉育綸、林文杰、林奕成、陳冠文、孫春在、簡仁宗、陳稔、林正中、陳永昇、黃世強、莊榮宏、施仁忠、莊仁輝、陳玲慧、王邦任、詹力韋、王昱舜、張永儒


### 3.4 集群 3：生物資訊與統計集群（12 人）

- **成員共同研究領域**：Bioinformatics（6 人）、Statistics（5 人）、Biostatistics（3 人）、Systems Biology（2 人）、Scientific Computing（2 人）、Statistical Inference（2 人）、Change Point Analysis（1 人）
- **成員主導 taxonomy L1**：Statistics & Statistical Methods 5 人、Biomedical & Health Informatics 4 人、Applied Mathematics & Operations Research 2 人、AI & Machine Learning 1 人

12 位成員，主導 taxonomy 為 Statistics（5）與 Biomedical & Health Informatics（4），共享 Bioinformatics（6 人）、Statistics、Biostatistics、Systems Biology 與 Scientific Computing。荊宇泰 degree 41 為集群最高（生物資訊、機器學習）；王秀瑛（工業統計）、黃冠華（生物統計）、盧鴻興（科學計算）、洪慧念（統計推論）是統計所背景的成員。這個集群與其他集群的連結較稀疏。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 荊宇泰 | Yu-Tai Ching | 教師（未細分） | 41 | 0.000 | Bioinformatics、Machine Learning |
| 王秀瑛 | Hsiu-Ying Wang | 教師（未細分） | 15 | 0.011 | Bioinformatics、Industrial Statistics、Statistics |
| 黃冠華 | GUAN-HUA HUANG | 教師（未細分） | 10 | 0.014 | Bioinformatics、Biostatistics |
| 盧鴻興 | Henry Horng-Shing Lu | 教師（未細分） | 10 | 0.006 | Bioinformatics、Scientific Computing |
| 洪慧念 | HUEI-NIAN HONG | 教師（未細分） | 9 | 0.013 | Scientific Computing、Statistical Inference |
| 高竹嵐 | Chu-Lan Kao | 專任 | 9 | 0.000 | Change Point Analysis、Statistics |
| 林峻宇 | Chun-Yu Lin | 專任 | 8 | 0.000 | Bioinformatics、Systems Biology |
| 楊進木 | Jinn-Moon Yang | 教師（未細分） | 8 | 0.000 | Bioinformatics、Systems Biology |

其餘成員（4 位，依 degree 排序）：林聖軒、王維菁、陳志榮、蕭子健


### 3.5 集群 4：理論、演算法與密碼學集群（10 人）

- **成員共同研究領域**：Algorithms（6 人）、Optimization（4 人）、Cryptography（4 人）、Theory of Computation（4 人）、Coding Theory（3 人）、Computational Complexity（2 人）、Privacy-Preserving Computing（1 人）
- **成員主導 taxonomy L1**：Theory & Algorithms 5 人、Security, Privacy & Cryptography 2 人、Applied Mathematics & Operations Research 2 人、AI & Machine Learning 1 人

10 位成員，5 位主導 Theory & Algorithms，共享 Algorithms、Optimization、Cryptography、Theory of Computation 與 Coding Theory。蔡錫鈞 degree 65、betweenness 0.053 為集群最高（演算法、編碼理論、計算複雜度、網路、密碼學）；陳穎平（講座教授，演化計算、最佳化）次之；曾文貴代表密碼學與資安；陳榮傑、譚建民為名譽教授。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 蔡錫鈞 | Shi-Chun Tsai | 教師（未細分） | 65 | 0.053 | Algorithms、Coding Theory、Computational Complexity、Computer Networks、Cryptography |
| 陳穎平 | Ying-Ping Chen | 主管／講座 | 47 | 0.006 | Algorithms、Evolutionary Computation、Optimization |
| 曾文貴 | Wen-Guey Tzeng | 教師（未細分） | 30 | 0.026 | Computational Complexity、Cryptography、Information Security、Network Security、Theory of Computation |
| 陳榮傑 | Rong-Jaye Chen | 名譽／退休 | 19 | 0.001 | Algorithms、Coding Theory、Cryptography、Theory of Computation |
| 譚建民 | Jimmy J.M. Tan | 名譽／退休 | 18 | 0.004 | Algorithms、Graph Theory、Optimization |
| 高孟駿 | Mong-Jen Kao | 教師（未細分） | 17 | 0.000 | Algorithms、Optimization |
| 謝旻錚 | Min-Zheng Shieh | 專任 | 14 | 0.000 | Coding Theory、Theory of Computation |
| 黃問泙 | Wen-Ping Hwang | 名譽／退休 | 13 | 0.000 | Algorithms |

其餘成員（2 位，依 degree 排序）：王偉豪、蔣兆凱


*集群表出處：`analysis/network-analysis/nycu-cs/professor_communities.csv`（集群歸屬）、`professor_centrality.csv`（degree、betweenness、職稱類別）、`prof_keyword_network.graphml`（成員研究領域，用來統計集群的共同領域）*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 職稱類別為官網職稱的分類，一人可屬多類時取主要類別；「N 個系所」表示該教授也出現在其他系所名單。*

### 3.6 全系的橋接者與樞紐

Betweenness 最高的教授（跨集群的橋梁）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 黃春融 | Chun-Rong Huang | 教師（未細分） | 75 | 0.110 | Vision, Multimedia & Human-Centered Computing |
| 洪瑞鴻 | Jui-Hung Hung | 教師（未細分） | 69 | 0.100 | AI & Machine Learning |
| 李宗夷 | Tzong-Yi Lee | 教師（未細分） | 75 | 0.075 | AI & Machine Learning |
| 黃敬群 | Ching-Chun Huang | 教師（未細分） | 57 | 0.063 | Vision, Multimedia & Human-Centered Computing |
| 蔡錫鈞 | Shi-Chun Tsai | 教師（未細分） | 65 | 0.053 | Theory & Algorithms |
| 王國禎 | Kuo-Chen Wang | 名譽／退休 | 50 | 0.049 | Networks & Communications |

Degree 最高的教授（與最多同儕共享領域的樞紐）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 黃春融 | Chun-Rong Huang | 教師（未細分） | 75 | 0.110 | Vision, Multimedia & Human-Centered Computing |
| 李宗夷 | Tzong-Yi Lee | 教師（未細分） | 75 | 0.075 | AI & Machine Learning |
| 王協源 | Shie-Yuan Wang | 教師（未細分） | 73 | 0.022 | Networks & Communications |
| 吳凱強 | Kai-Chiang Wu | 教師（未細分） | 72 | 0.026 | AI & Machine Learning |
| 傅心家 | Hsin-Chia Fu | 名譽／退休 | 69 | 0.001 | AI & Machine Learning |
| 洪瑞鴻 | Jui-Hung Hung | 教師（未細分） | 69 | 0.100 | AI & Machine Learning |

*出處：`analysis/network-analysis/nycu-cs/professor_centrality.csv`*

![陽明交通大學資訊工程學系（資訊學院） 教授網路（節點大小 = betweenness）](../network-analysis/nycu-cs/figures/08_professor_network_betweenness.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 教授網路（節點大小 = betweenness）*  
*出處：`analysis/network-analysis/nycu-cs/figures/08_professor_network_betweenness.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。此圖節點大小改為與 betweenness 成正比。*

![陽明交通大學資訊工程學系（資訊學院） 各集群教授 word cloud（字級 = degree）](../network-analysis/nycu-cs/figures/27_professor_wordcloud_degree_by_community.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 各集群教授 word cloud（字級 = degree）*  
*出處：`analysis/network-analysis/nycu-cs/figures/27_professor_wordcloud_degree_by_community.png`*  
*建構方式：依 Louvain 集群分塊、同集群同色的教授姓名 word cloud，字級與 degree 成線性正比並設下限。*

另有 1 位教授雖有研究領域，但與其他教授沒有共享任何領域，孤立於最大連通元件之外，不屬於任何集群。

## 4. 結構穩健性檢驗

### 4.1 虛無模型檢定

| 統計量 | 觀測值 | 虛無平均 | 虛無標準差 | z-score | empirical p | p < 0.05 |
| --- | --- | --- | --- | --- | --- | --- |
| 領域網路密度 | 0.0978 | 0.1224 | 0.0032 | -7.71 | 0.002 | 顯著 |
| 領域網路 modularity Q | 0.3879 | 0.2509 | 0.0137 | 10.03 | 0.002 | 顯著 |
| 領域平均共現次數 | 1.4945 | 1.2205 | 0.0206 | 13.31 | 0.002 | 顯著 |
| 教授網路 clustering 係數 | 0.6764 | 0.6164 | 0.0124 | 4.83 | 0.002 | 顯著 |

*出處：`analysis/network-analysis/nycu-cs/null_model_test.csv`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 密度顯著偏低而 modularity、共現顯著偏高，代表領域共現集中在少數主題群，不是均勻分布。*

![陽明交通大學資訊工程學系（資訊學院） 觀測值 vs 虛無模型分布](../network-analysis/nycu-cs/figures/15_null_model_comparison.png)

*圖：陽明交通大學資訊工程學系（資訊學院） 觀測值 vs 虛無模型分布*  
*出處：`analysis/network-analysis/nycu-cs/figures/15_null_model_comparison.png`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。*

### 4.2 λ 敏感度

| λ | 邊數 | 密度 | Q | 集群數 | 密度相對 baseline | Q 下降 | 過度合併 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 1662 | 0.171 | 0.388 | 6 | +0% | 0.000 | 否 |
| 0.3 | 2524 | 0.259 | 0.359 | 5 | +52% | 0.029 | 是 |
| 0.4 | 2524 | 0.259 | 0.350 | 5 | +52% | 0.038 | 是 |
| 0.5 | 2524 | 0.259 | 0.349 | 5 | +52% | 0.039 | 是 |

*出處：`analysis/network-analysis/nycu-cs/lambda_sensitivity.csv`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

![陽明交通大學資訊工程學系（資訊學院） λ 敏感度](../network-analysis/nycu-cs/figures/16_lambda_sensitivity.png)

*圖：陽明交通大學資訊工程學系（資訊學院） λ 敏感度*  
*出處：`analysis/network-analysis/nycu-cs/figures/16_lambda_sensitivity.png`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

### 4.3 taxonomy L1 覆蓋護欄

| taxonomy L1 | 教授數 | 覆蓋率 | flag |
| --- | --- | --- | --- |
| AI & Machine Learning | 57 | 40.7% | ok |
| Vision, Multimedia & Human-Centered Computing | 43 | 30.7% | ok |
| Systems, Software & Architecture | 36 | 25.7% | ok |
| Networks & Communications | 34 | 24.3% | ok |
| Data, Databases & Knowledge Discovery | 24 | 17.1% | ok |
| Biomedical & Health Informatics | 21 | 15.0% | ok |
| Security, Privacy & Cryptography | 20 | 14.3% | ok |
| Theory & Algorithms | 15 | 10.7% | ok |

*出處：`analysis/network-analysis/nycu-cs/l1_coverage_guardrail.csv`（只列前 8 項）*  
*建構方式：計算每個 L1 分類涵蓋該單位多少比例的教授，超過 50% 標記 too_broad，代表此 L1 在本單位太寬，不能用來做 L1 roll-up 比較。*

## 5. 解讀與注意事項

- 152 位師資中 33 位為名譽教授、29 位有講座或主管職稱，多數有研究領域並進入網路，集群反映的是包含資深師資的學院整體樣貌。
- λ 在 0.3、0.4、0.5 都觸發過度合併護欄（密度由 0.171 增至 0.259）。λ=0 的 baseline 有 6 個社群，λ=0.4 減為 5 個，差異在於大型集群的細分；細部解讀應以 λ=0 為準。
- 沒有任何 L1 被標記為過寬；AI & Machine Learning 雖然人數最多，但仍低於 50%。
- 只有 1 位教授孤立於教授網路之外，另有 11 位因官網未填研究領域而排除。
- 研究領域網路有 7 個社群，比教授網路多 2 個：「HCI／Graphics／VR／Robotics」與「Databases／IR／NLP」在領域層級自成一群，但在教授層級併入視覺與 AI 集群。
- 研究領域來自官網自填內容，粒度與深度因人而異；網路密度與集群數反映填寫習慣的成分不可忽視，完整率不可解讀為系所或教授的品質排名。

## 附錄：本報告引用的資料與圖表清單

| 檔案 | 產生階段 / 程式 | 建構方式摘要 |
| --- | --- | --- |
| `analysis/data-collection/nycu-cs/quality-report.json` | 資料蒐集 `scripts/data-collection/collect.py` | 爬取官網後統計 canonical 紀錄人數、職稱分類、中英配對率與欄位完整率 |
| `analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv` | 預處理 `1_faculty_data_preprocessing.ipynb` | 標準化後各欄位有 canonical 值的教師比例與平均項目數 |
| `.../group_comparison/research_fields/cs.csv`、`by_department/top_research_fields/nycu-cs.png` | 預處理 `2_rf_and_phd_inst_comparison.ipynb` | 由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。 |
| `.../group_comparison/phd_institutions/cs.csv`、`by_department/top_phd_institutions/nycu-cs.png` | 同上 | 同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。 |
| `analysis/network-analysis/nycu-cs/network_metrics.json` | 網路分析 `2_build_network_data.ipynb` + `3_network_analysis.ipynb` | 由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 |
| `analysis/network-analysis/nycu-cs/keyword_centrality.csv`、`keyword_communities.csv` | `3_network_analysis.ipynb` | 研究領域網路的中心性與 Louvain 社群；taxonomy 來自 `1_build_taxonomy.ipynb` |
| `analysis/network-analysis/nycu-cs/professor_centrality.csv`、`professor_communities.csv`、`prof_keyword_network.graphml` | `3_network_analysis.ipynb` | 教授網路的中心性與 Louvain 集群；graphml 為二分網路，本報告用它統計各集群成員的共同領域 |
| `analysis/network-analysis/nycu-cs/null_model_test.csv` | `3_network_analysis.ipynb` | 以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 |
| `analysis/network-analysis/nycu-cs/lambda_sensitivity.csv` | `3_network_analysis.ipynb` | 以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。 |
| `analysis/network-analysis/nycu-cs/l1_coverage_guardrail.csv` | `3_network_analysis.ipynb` | 每個 L1 涵蓋教授比例，> 50% 標記 too_broad |
| `analysis/network-analysis/nycu-cs/figures/01, 05, 08, 09, 10, 13, 14, 15, 16, 27` | `3_network_analysis.ipynb` | 網路圖節點大小與 degree 或 betweenness 成正比、顏色依社群；邊數 > 400 時繪圖用 disparity filter backbone；word cloud 字級與中心性成線性正比 |

更完整的方法說明見 `docs/data-collection-report.md`、`docs/data-preprocessing-report.md`、`docs/network-analysis-report.md`。
