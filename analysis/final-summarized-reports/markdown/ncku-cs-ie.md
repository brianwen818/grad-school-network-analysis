# 成功大學資訊工程學系（`ncku-cs-ie`）研究結果總結報告

所屬分組：資工組（cs）　｜　資料日期：2026-09-09 蒐集、2026-09-10 完成網路分析

> **本報告的資料來源**
> 本專案分三個階段：(1) 資料蒐集（`scripts/data-collection/`）從 14 個系所官網爬取師資的姓名、職稱、學歷與研究領域，中英文分開蒐集後配對；
> (2) 資料預處理（`scripts/data-preprocessing/`）把職稱、學歷、研究領域標準化成英文 canonical 值，並產生描述統計；
> (3) 網路分析（`scripts/network-analysis/current-version/`）建立「教授–研究領域」二分網路，投影成研究領域網路與教授網路，做社群偵測、中心性、虛無模型與敏感度分析。
> 本報告所有數字、表格與圖表都取自 `analysis/` 底下這三個階段的輸出，每張圖表下方都標明出處與建構方式，附錄另有完整清單。
> 「研究集群」指教授網路的 Louvain 社群；「重要老師」依教授在該網路中的 degree（與多少同儕共享領域）與 betweenness（是否位於集群之間的橋梁位置）判定，**不是**學術成就的排名。

## 1. 科系速覽

成大資工系官網列出 62 位教師，研究輪廓以 AI 為主：Artificial Intelligence 17 人、Machine Learning 11 人、Deep Learning 9 人，其次是 Embedded Systems（8 人）、Algorithms 與 Image Processing（各 7 人）。與其他資工系相比，本系的特色是 **Medical Informatics 與 Smart Healthcare（各 5 人）比重高**，反映成大醫學院的鄰近效應；另一特色是 Smart Manufacturing 與 Digital Twins 的出現。研究領域完整率 82.3%，有 11 位未進入網路。博士畢業學校以台大（10 人）、成大（6 人）、清大與交大（各 5 人）為主。

### 1.1 基本資料

| 項目 | 數值 |
| --- | --- |
| 官網師資人數（canonical 紀錄） | 62 |
| 職稱分類（一人可屬多類） | 教師（未細分） 46、專任 7、兼任 4、主管／講座 4、合聘 2 |
| 中英文紀錄配對率 | 100.0% |
| 研究領域完整率（標準化後） | 82.3% |
| 學歷完整率（標準化後） | 80.6% |
| 每位教授平均研究領域數 | 3.05 |
| 進入網路分析的教授數 | 51（11 位因無研究領域排除） |

*出處：`analysis/data-collection/ncku-cs-ie/quality-report.json`（人數、職稱、配對率）、`analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv`（完整率）、`analysis/network-analysis/ncku-cs-ie/network_metrics.json`（進入網路人數）*  
*建構方式：quality-report 由 `scripts/data-collection/collect.py` 在爬取官網後統計 canonical 紀錄的職稱分類與中英配對；coverage 由 `1_faculty_data_preprocessing.ipynb` 計算標準化後有 canonical 值的教師比例。*

### 1.2 主要研究領域

| 排名 | 研究領域（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | Artificial Intelligence | 17 |
| 2 | Machine Learning | 11 |
| 3 | Deep Learning | 9 |
| 4 | Embedded Systems | 8 |
| 5 | Algorithms | 7 |
| 6 | Image Processing | 7 |
| 7 | Computer Vision | 6 |
| 8 | Medical Informatics | 5 |
| 9 | Smart Healthcare | 5 |
| 10 | Multimedia Systems | 5 |
| 11 | Data Mining | 5 |
| 12 | Data Science | 4 |
| 13 | Optimization | 4 |
| 14 | Internet of Things | 4 |
| 15 | Smart Manufacturing | 4 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/research_fields/cs.csv`（`ncku-cs-ie` 欄）*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

![成功大學資訊工程學系 研究領域人數](../descriptive-stats-after-preprocessing/by_department/top_research_fields/ncku-cs-ie.png)

*圖：成功大學資訊工程學系 研究領域人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_research_fields/ncku-cs-ie.png`*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

### 1.3 博士畢業學校

| 排名 | 博士畢業學校（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | National Taiwan University | 10 |
| 2 | National Cheng Kung University | 6 |
| 3 | National Tsing Hua University | 5 |
| 4 | National Chiao Tung University | 5 |
| 5 | Texas A&M University | 3 |
| 6 | The Ohio State University | 2 |
| 7 | National Central University | 2 |
| 8 | University of Missouri | 2 |
| 9 | University of Florida | 1 |
| 10 | Columbia University | 1 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/phd_institutions/cs.csv`（`ncku-cs-ie` 欄）*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

![成功大學資訊工程學系 博士畢業學校人數](../descriptive-stats-after-preprocessing/by_department/top_phd_institutions/ncku-cs-ie.png)

*圖：成功大學資訊工程學系 博士畢業學校人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_phd_institutions/ncku-cs-ie.png`*  
*建構方式：同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。*

## 2. 研究領域網路結構

### 2.1 網路指標

| 指標 | 數值 | 說明 |
| --- | --- | --- |
| 二分網路：教授數 / 領域數 / 邊數 | 51 / 66 / 189 | 一條邊 = 一位教授研究一個領域 |
| 二分網路連通元件數 | 2 | 最大元件涵蓋 98.0% 教授 |
| 每位教授平均 / 最多領域數 | 3.71 / 9 |  |
| 研究領域網路：節點 / 邊 | 65 / 286 | 只含至少與一個其他領域共現的領域 |
| 研究領域網路密度 | 0.138 | 實際邊數 ÷ 可能邊數 |
| 研究領域網路平均 degree | 8.80 |  |
| 研究領域網路 modularity Q（Louvain） | 0.397 | 7 個社群；resolution 0.7 / 1.3 時為 4 / 6 個 |
| 領域社群 vs taxonomy L1 一致度 | NMI 0.448 / ARI 0.147 | 1 = 完全一致，0 = 無關 |
| 教授網路：節點 / 邊 | 50 / 493 | 只含最大連通元件 |
| 教授網路密度 | 0.402 |  |
| 教授網路 modularity Q（Louvain） | 0.235 | 5 個集群 |
| 教授集群 vs 主導 L1 一致度 | NMI 0.376 / ARI 0.148 |  |

*出處：`analysis/network-analysis/ncku-cs-ie/network_metrics.json`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

![成功大學資訊工程學系 教授–研究領域二分網路](../network-analysis/ncku-cs-ie/figures/01_bipartite_network.png)

*圖：成功大學資訊工程學系 教授–研究領域二分網路*  
*出處：`analysis/network-analysis/ncku-cs-ie/figures/01_bipartite_network.png`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。圖中兩類節點以不同顏色區分，節點大小與 degree 成正比；邊數超過 400 時繪圖使用 disparity filter backbone（α = 0.05），指標仍以完整圖計算。*

### 2.2 關鍵研究領域

| 研究領域 | Degree | Degree centrality | Betweenness | PageRank | 教授數 | taxonomy L1 |
| --- | --- | --- | --- | --- | --- | --- |
| Artificial Intelligence | 37 | 0.578 | 0.391 | 0.0695 | 17 | AI & Machine Learning |
| Machine Learning | 28 | 0.438 | 0.158 | 0.0518 | 11 | AI & Machine Learning |
| Deep Learning | 20 | 0.312 | 0.109 | 0.0400 | 9 | AI & Machine Learning |
| Embedded Systems | 19 | 0.297 | 0.067 | 0.0302 | 8 | Systems, Software & Architecture |
| Algorithms | 18 | 0.281 | 0.144 | 0.0339 | 7 | Theory & Algorithms |
| Computer Vision | 17 | 0.266 | 0.037 | 0.0301 | 6 | Vision, Multimedia & Human-Centered Computing |
| Medical Informatics | 17 | 0.266 | 0.055 | 0.0253 | 5 | Biomedical & Health Informatics |
| Data Science | 17 | 0.266 | 0.054 | 0.0259 | 4 | Data, Databases & Knowledge Discovery |
| Smart Healthcare | 16 | 0.250 | 0.064 | 0.0283 | 5 | Biomedical & Health Informatics |
| Image Processing | 15 | 0.234 | 0.009 | 0.0268 | 7 | Vision, Multimedia & Human-Centered Computing |
| Data Mining | 15 | 0.234 | 0.042 | 0.0273 | 5 | Data, Databases & Knowledge Discovery |
| Optimization | 13 | 0.203 | 0.062 | 0.0224 | 4 | Applied Mathematics & Operations Research |

Betweenness 最高的五個領域：Artificial Intelligence（0.39）、Machine Learning（0.16）、Algorithms（0.14）、Deep Learning（0.11）、Internet of Things（0.10）。Betweenness 高代表該領域位於不同主題群之間的連結位置，是系上跨主題的共同語言。

*出處：`analysis/network-analysis/ncku-cs-ie/keyword_centrality.csv`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。 degree 為相連領域數，betweenness 為經過該節點的最短路徑比例，PageRank 為加權隨機漫步的穩態機率；parent_l1 來自 `1_build_taxonomy.ipynb` 手工編定的三層 taxonomy（170 個 L3、46 個 L2、16 個 L1）。*

![成功大學資訊工程學系 研究領域教授人數長條圖](../network-analysis/ncku-cs-ie/figures/10_top_keywords_bar.png)

*圖：成功大學資訊工程學系 研究領域教授人數長條圖*  
*出處：`analysis/network-analysis/ncku-cs-ie/figures/10_top_keywords_bar.png`*  
*建構方式：以二分網路中每個領域節點的 degree（研究該領域的教授數）排序繪製。*

### 2.3 研究領域社群

| 社群 | 領域數 | 主要領域（教授人數） | 主要 taxonomy L1（領域數） |
| --- | --- | --- | --- |
| 0 | 12 | Artificial Intelligence（17）、Generative AI（3）、Mobile Computing（2）、Computer Networks（2）、Information Security（2）、Network Security（2）、Big Data Analytics（2） | AI & Machine Learning 3、Networks & Communications 3、Security, Privacy & Cryptography 3 |
| 1 | 11 | Medical Informatics（5）、Data Mining（5）、Multimedia Systems（5）、Databases（4）、Natural Language Processing（2）、Information Retrieval（2）、Wireless Networks（2） | Data, Databases & Knowledge Discovery 4、AI & Machine Learning 3、Networks & Communications 2 |
| 2 | 10 | Deep Learning（9）、Algorithms（7）、Smart Healthcare（5）、Distributed Systems（4）、Parallel Computing（4）、Medical Imaging（3）、Signal Processing（3） | Biomedical & Health Informatics 3、Systems, Software & Architecture 3、Theory & Algorithms 2 |
| 3 | 9 | Machine Learning（11）、Image Processing（7）、Computer Vision（6）、Human-Computer Interaction（4）、Robotics（2）、Augmented Reality（2）、Automation and Control（2） | Vision, Multimedia & Human-Centered Computing 6、Robotics, Control & Smart Manufacturing 2、AI & Machine Learning 1 |
| 4 | 9 | Optimization（4）、Smart Manufacturing（4）、Digital Twins（2）、Digital Transformation（1）、Reinforcement Learning（1）、Cyber-Physical Systems（1）、Real-Time Systems（1） | Systems, Software & Architecture 4、Information Systems & Management 2、Applied Mathematics & Operations Research 1 |
| 5 | 7 | Embedded Systems（8）、Internet of Things（4）、Storage Systems（3）、Operating Systems（2）、Computer Architecture（2）、Edge Computing（1）、Intelligent Transportation Systems（1） | Systems, Software & Architecture 3、Networks & Communications 3、Data, Databases & Knowledge Discovery 1 |
| 6 | 7 | Data Science（4）、Recommender Systems（1）、Social Media Analytics（1）、Social Network Analysis（1）、Trustworthy AI（1）、Data Envelopment Analysis（1）、Operations Research（1） | Data, Databases & Knowledge Discovery 4、Applied Mathematics & Operations Research 2、AI & Machine Learning 1 |

*出處：`analysis/network-analysis/ncku-cs-ie/keyword_communities.csv`（`community` 欄）、`keyword_centrality.csv`（教授人數）*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。*

![成功大學資訊工程學系 研究領域網路的 Louvain 社群](../network-analysis/ncku-cs-ie/figures/05_keyword_network_communities.png)

*圖：成功大學資訊工程學系 研究領域網路的 Louvain 社群*  
*出處：`analysis/network-analysis/ncku-cs-ie/figures/05_keyword_network_communities.png`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。節點顏色為社群，大小與 degree 成正比。*

![成功大學資訊工程學系 各研究領域社群的 taxonomy L1 組成](../network-analysis/ncku-cs-ie/figures/14_community_composition.png)

*圖：成功大學資訊工程學系 各研究領域社群的 taxonomy L1 組成*  
*出處：`analysis/network-analysis/ncku-cs-ie/figures/14_community_composition.png`*  
*建構方式：把每個 Louvain 領域社群內的領域依 taxonomy L1 分類計數，堆疊長條圖。用來檢查資料驅動的社群是否對應人工分類。*

![成功大學資訊工程學系 研究領域共現熱圖](../network-analysis/ncku-cs-ie/figures/13_keyword_cooccurrence_heatmap.png)

*圖：成功大學資訊工程學系 研究領域共現熱圖*  
*出處：`analysis/network-analysis/ncku-cs-ie/figures/13_keyword_cooccurrence_heatmap.png`*  
*建構方式：取研究領域網路的加權鄰接矩陣（共同研究兩領域的教授人數），依社群排序後繪製熱圖。*

## 3. 主要研究集群與重要老師

教授網路分成 5 個集群：深度學習與視覺、嵌入式與智慧製造、AI 與網路、資料探勘與醫學資訊、演算法與平行計算。研究領域網路密度顯著低於虛無模型（z = -2.2）、modularity 顯著高於（z = 4.4）、平均共現顯著高於（z = 2.3），主題結構明確。Artificial Intelligence 的 betweenness（0.39）遠高於其他領域，是連結各集群的共同語言。

教授網路共 50 位教授、5 個集群（Louvain，Q = 0.235）。以下依集群人數排序；集群編號與圖中的 Community 編號一致。表中 Degree 為與該教授共享研究領域的同儕數，Betweenness 為該教授位於他人最短路徑上的比例（越高越像橋梁）。

![成功大學資訊工程學系 教授網路的 Louvain 集群](../network-analysis/ncku-cs-ie/figures/09_professor_network_communities.png)

*圖：成功大學資訊工程學系 教授網路的 Louvain 集群*  
*出處：`analysis/network-analysis/ncku-cs-ie/figures/09_professor_network_communities.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

### 3.1 集群 0：深度學習、影像與電腦視覺集群（16 人）

- **成員共同研究領域**：Machine Learning（8 人）、Deep Learning（7 人）、Image Processing（7 人）、Artificial Intelligence（5 人）、Computer Vision（5 人）、Human-Computer Interaction（4 人）、Multimedia Systems（3 人）
- **成員主導 taxonomy L1**：AI & Machine Learning 8 人、Vision, Multimedia & Human-Centered Computing 7 人、Biomedical & Health Informatics 1 人

16 位成員，主導 taxonomy 為 AI & Machine Learning（8 人）與 Vision, Multimedia & Human-Centered Computing（7 人），共享 Machine Learning、Deep Learning、Image Processing、Computer Vision 與 Human-Computer Interaction。洪昌鈺 degree 最高（33，AI、深度學習、影像、醫學影像）；連震杰 betweenness 最高（0.17），研究擴增實境、自動控制、電腦視覺與嵌入式系統，也與成大統計系合聘；詹慧伶（演算法、資料科學、醫學影像）betweenness 次之；李同益為系主任。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 洪昌鈺 |  | 教師（未細分） | 33 | 0.039 | Artificial Intelligence、Deep Learning、Image Processing、Machine Learning、Medical Imaging |
| 李同益 |  | 主管／講座 | 32 | 0.031 | Artificial Intelligence、Computer Graphics、Computer Vision、Deep Learning、Information Security |
| 連震杰（2 個系所） |  | 教師（未細分） | 31 | 0.170 | Augmented Reality、Automation and Control、Computer Vision、Embedded Systems、Human-Computer Interaction |
| 詹慧伶 |  | 專任 | 31 | 0.103 | Algorithms、Data Science、Deep Learning、Machine Learning、Medical Imaging |
| 郭淑美 |  | 教師（未細分） | 31 | 0.012 | Algorithms、Artificial Intelligence、Deep Learning、Image Processing |
| 吳宗憲 |  | 主管／講座 | 29 | 0.024 | Artificial Intelligence、Deep Learning、Human-Computer Interaction、Multimedia Systems |
| 吳明龍 |  | 專任 | 27 | 0.011 | Data Science、Deep Learning、Image Processing、Machine Learning |
| 賀保羅 |  | 教師（未細分） | 26 | 0.003 | Algorithms、Machine Learning、Medical Informatics |

其餘成員（8 位，依 degree 排序）：朱威達、郭紘睿、王士豪、孫永年、程芙茵、許舒涵、蘇文鈺、黃崇明


### 3.2 集群 1：嵌入式系統與智慧製造集群（13 人）

- **成員共同研究領域**：Embedded Systems（7 人）、Storage Systems（3 人）、Optimization（3 人）、Smart Manufacturing（3 人）、Operating Systems（2 人）、Computer Architecture（2 人）、Digital Twins（2 人）
- **成員主導 taxonomy L1**：Systems, Software & Architecture 5 人、AI & Machine Learning 2 人、Data, Databases & Knowledge Discovery 2 人、Vision, Multimedia & Human-Centered Computing 1 人、Networks & Communications 1 人、Robotics, Control & Smart Manufacturing 1 人、Applied Mathematics & Operations Research 1 人

13 位成員，主導 taxonomy 以 Systems, Software & Architecture 為主，共享 Embedded Systems（7 人）、Storage Systems、Optimization、Smart Manufacturing、Operating Systems 與 Digital Twins。郭軒安 degree 最高（32，數位轉型、數位孿生、最佳化、強化學習）；張大緯 betweenness 最高（0.081），研究邊緣運算、物聯網、智慧交通與作業系統；蔡佩璇代表 Cyber-Physical Systems 與智慧製造；陳培殷、梁勝富專注嵌入式系統。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 郭軒安 |  | 專任 | 32 | 0.035 | Algorithms、Digital Transformation、Digital Twins、Optimization、Reinforcement Learning |
| 陳培殷 |  | 教師（未細分） | 25 | 0.000 | Artificial Intelligence、Embedded Systems |
| 梁勝富 |  | 教師（未細分） | 23 | 0.011 | Embedded Systems、Multimedia Systems、Signal Processing |
| 蔡佩璇 |  | 教師（未細分） | 21 | 0.003 | Cyber-Physical Systems、Digital Twins、Real-Time Systems、Smart Healthcare、Smart Manufacturing |
| 張大緯 |  | 教師（未細分） | 19 | 0.081 | Edge Computing、Embedded Systems、Intelligent Transportation Systems、Internet of Things、Operating Systems |
| 涂嘉恒 |  | 教師（未細分） | 16 | 0.045 | Compilers、Embedded Systems、Optimization、Parallel Computing |
| 何建忠 |  | 教師（未細分） | 14 | 0.020 | Embedded Systems、Storage Systems |
| 楊中平 |  | 教師（未細分） | 9 | 0.000 | Embedded Systems |

其餘成員（5 位，依 degree 排序）：黃敬群、梁郁珮、鄭芳田、楊大和、張燕光


### 3.3 集群 2：人工智慧、網路與行動運算集群（10 人）

- **成員共同研究領域**：Artificial Intelligence（9 人）、Generative AI（3 人）、Machine Learning（3 人）、Internet of Things（3 人）、Big Data Analytics（2 人）、Mobile Computing（2 人）、Computer Networks（2 人）
- **成員主導 taxonomy L1**：AI & Machine Learning 7 人、Networks & Communications 1 人、Data, Databases & Knowledge Discovery 1 人、Security, Privacy & Cryptography 1 人

10 位成員，7 位主導 AI & Machine Learning，共享 Artificial Intelligence（9 人）、Generative AI、Internet of Things、Mobile Computing 與 Computer Networks。李政德（與成大統計合聘）與鄭憲宗 degree 並列最高（30）；陳怡君（生成式 AI、電腦視覺）betweenness 最高；蔣榮先結合大數據、資訊檢索與醫學資訊；郭耀煌代表模糊系統與物聯網。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 李政德（2 個系所） |  | 教師（未細分） | 30 | 0.038 | Artificial Intelligence、Data Science、Machine Learning、Natural Language Processing、Recommender Systems |
| 鄭憲宗 |  | 教師（未細分） | 30 | 0.029 | Artificial Intelligence、Computer Networks、Machine Learning、Mobile Computing、Network Security |
| 陳怡君 |  | 教師（未細分） | 29 | 0.052 | Artificial Intelligence、Computer Vision、Generative AI、Machine Learning |
| 郭耀煌 |  | 教師（未細分） | 29 | 0.010 | Artificial Intelligence、Computer Networks、Fuzzy Systems、Internet of Things |
| 蔣榮先 |  | 教師（未細分） | 28 | 0.040 | Artificial Intelligence、Big Data Analytics、Information Retrieval、Medical Informatics、Mobile Computing |
| 陳響亮 |  | 教師（未細分） | 27 | 0.041 | Artificial Intelligence、Big Data Analytics、Internet of Things、Smart Manufacturing |
| 藍崑展 |  | 教師（未細分） | 26 | 0.014 | Artificial Intelligence、Internet of Things、Robotics、Smart Healthcare |
| 李信杰 |  | 專任 | 16 | 0.000 | Artificial Intelligence、Generative AI |

其餘成員（2 位，依 degree 排序）：龔漢威、黃宗立


### 3.4 集群 3：資料探勘、資料庫與醫學資訊集群（6 人）

- **成員共同研究領域**：Data Mining（5 人）、Databases（3 人）、Cloud Computing（2 人）、Medical Informatics（2 人）、Wireless Networks（2 人）、Deep Learning（1 人）、Data Envelopment Analysis（1 人）
- **成員主導 taxonomy L1**：Data, Databases & Knowledge Discovery 3 人、AI & Machine Learning 1 人、Applied Mathematics & Operations Research 1 人、Networks & Communications 1 人

6 位成員，共享 Data Mining（5 人）、Databases、Cloud Computing 與 Medical Informatics。陳朝鈞 betweenness 最高（0.073），研究資料探勘、資料庫、醫學資訊、多媒體與無線網路；張瑞紘（雲端、資料庫、深度學習）degree 相同；盧文祥代表 NLP 與機器翻譯；李家岩（與台大資管合聘，兼任）帶入作業研究與資料包絡分析。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 陳朝鈞 |  | 教師（未細分） | 28 | 0.073 | Data Mining、Databases、Medical Informatics、Multimedia Systems、Wireless Networks |
| 張瑞紘 |  | 專任 | 28 | 0.025 | Cloud Computing、Data Mining、Databases、Deep Learning |
| 盧文祥 |  | 教師（未細分） | 16 | 0.012 | Data Mining、Information Retrieval、Machine Translation、Medical Informatics、Natural Language Processing |
| 莊坤達 |  | 教師（未細分） | 13 | 0.004 | Cloud Computing、Data Mining、Databases |
| 李家岩（2 個系所） |  | 兼任 | 12 | 0.014 | Data Envelopment Analysis、Data Mining、Data Science、Operations Research、Optimization |
| 蘇銓清 |  | 教師（未細分） | 3 | 0.000 | Wireless Networks |

### 3.5 集群 4：演算法與分散式／平行運算集群（5 人）

- **成員共同研究領域**：Distributed Systems（4 人）、Parallel Computing（3 人）、Algorithms（3 人）、Artificial Intelligence（2 人）、Graph Theory（2 人）、Smart Healthcare（2 人）、Software Engineering（1 人）
- **成員主導 taxonomy L1**：AI & Machine Learning 2 人、Systems, Software & Architecture 2 人、Theory & Algorithms 1 人

5 位成員，共享 Distributed Systems、Parallel Computing 與 Algorithms。謝孫源（系主任）degree 34 為全系最高，研究演算法、AI、生物資訊、深度學習與分散式系統，是這個集群通往 AI 集群的橋；李強（AI、資料庫、平行計算）次之；陳奇業結合圖論與智慧醫療；朱治平、蕭宏章專注分散式與平行計算。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 謝孫源 |  | 主管／講座 | 34 | 0.093 | Algorithms、Artificial Intelligence、Bioinformatics、Deep Learning、Distributed Systems |
| 李強 |  | 教師（未細分） | 26 | 0.009 | Artificial Intelligence、Databases、Parallel Computing |
| 陳奇業 |  | 教師（未細分） | 16 | 0.001 | Algorithms、Distributed Systems、Graph Theory、Smart Healthcare |
| 蕭宏章 |  | 教師（未細分） | 9 | 0.002 | Algorithms、Distributed Systems、Parallel Computing |
| 朱治平 |  | 教師（未細分） | 5 | 0.000 | Distributed Systems、Parallel Computing、Software Engineering |

*集群表出處：`analysis/network-analysis/ncku-cs-ie/professor_communities.csv`（集群歸屬）、`professor_centrality.csv`（degree、betweenness、職稱類別）、`prof_keyword_network.graphml`（成員研究領域，用來統計集群的共同領域）*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 職稱類別為官網職稱的分類，一人可屬多類時取主要類別；「N 個系所」表示該教授也出現在其他系所名單。*

### 3.6 全系的橋接者與樞紐

Betweenness 最高的教授（跨集群的橋梁）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 連震杰 |  | 教師（未細分） | 31 | 0.170 | Vision, Multimedia & Human-Centered Computing |
| 詹慧伶 |  | 專任 | 31 | 0.103 | AI & Machine Learning |
| 謝孫源 |  | 主管／講座 | 34 | 0.093 | AI & Machine Learning |
| 張大緯 |  | 教師（未細分） | 19 | 0.081 | Networks & Communications |
| 陳朝鈞 |  | 教師（未細分） | 28 | 0.073 | Data, Databases & Knowledge Discovery |
| 陳怡君 |  | 教師（未細分） | 29 | 0.052 | AI & Machine Learning |

Degree 最高的教授（與最多同儕共享領域的樞紐）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 謝孫源 |  | 主管／講座 | 34 | 0.093 | AI & Machine Learning |
| 洪昌鈺 |  | 教師（未細分） | 33 | 0.039 | AI & Machine Learning |
| 李同益 |  | 主管／講座 | 32 | 0.031 | Vision, Multimedia & Human-Centered Computing |
| 郭軒安 |  | 專任 | 32 | 0.035 | AI & Machine Learning |
| 郭淑美 |  | 教師（未細分） | 31 | 0.012 | AI & Machine Learning |
| 詹慧伶 |  | 專任 | 31 | 0.103 | AI & Machine Learning |

*出處：`analysis/network-analysis/ncku-cs-ie/professor_centrality.csv`*

![成功大學資訊工程學系 教授網路（節點大小 = betweenness）](../network-analysis/ncku-cs-ie/figures/08_professor_network_betweenness.png)

*圖：成功大學資訊工程學系 教授網路（節點大小 = betweenness）*  
*出處：`analysis/network-analysis/ncku-cs-ie/figures/08_professor_network_betweenness.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。此圖節點大小改為與 betweenness 成正比。*

![成功大學資訊工程學系 各集群教授 word cloud（字級 = degree）](../network-analysis/ncku-cs-ie/figures/27_professor_wordcloud_degree_by_community.png)

*圖：成功大學資訊工程學系 各集群教授 word cloud（字級 = degree）*  
*出處：`analysis/network-analysis/ncku-cs-ie/figures/27_professor_wordcloud_degree_by_community.png`*  
*建構方式：依 Louvain 集群分塊、同集群同色的教授姓名 word cloud，字級與 degree 成線性正比並設下限。*

另有 1 位教授雖有研究領域，但與其他教授沒有共享任何領域，孤立於最大連通元件之外，不屬於任何集群。

## 4. 結構穩健性檢驗

### 4.1 虛無模型檢定

| 統計量 | 觀測值 | 虛無平均 | 虛無標準差 | z-score | empirical p | p < 0.05 |
| --- | --- | --- | --- | --- | --- | --- |
| 領域網路密度 | 0.1375 | 0.1468 | 0.0042 | -2.21 | 0.014 | 顯著 |
| 領域網路 modularity Q | 0.3973 | 0.3029 | 0.0213 | 4.43 | 0.002 | 顯著 |
| 領域平均共現次數 | 1.2238 | 1.1695 | 0.0235 | 2.31 | 0.046 | 顯著 |
| 教授網路 clustering 係數 | 0.6537 | 0.6404 | 0.0257 | 0.52 | 0.587 | 不顯著 |

*出處：`analysis/network-analysis/ncku-cs-ie/null_model_test.csv`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 密度顯著偏低而 modularity、共現顯著偏高，代表領域共現集中在少數主題群，不是均勻分布。*

![成功大學資訊工程學系 觀測值 vs 虛無模型分布](../network-analysis/ncku-cs-ie/figures/15_null_model_comparison.png)

*圖：成功大學資訊工程學系 觀測值 vs 虛無模型分布*  
*出處：`analysis/network-analysis/ncku-cs-ie/figures/15_null_model_comparison.png`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。*

### 4.2 λ 敏感度

| λ | 邊數 | 密度 | Q | 集群數 | 密度相對 baseline | Q 下降 | 過度合併 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 354 | 0.289 | 0.291 | 5 | +0% | 0.000 | 否 |
| 0.3 | 493 | 0.402 | 0.238 | 5 | +39% | 0.053 | 否 |
| 0.4 | 493 | 0.402 | 0.235 | 5 | +39% | 0.056 | 否 |
| 0.5 | 493 | 0.402 | 0.220 | 5 | +39% | 0.071 | 否 |

*出處：`analysis/network-analysis/ncku-cs-ie/lambda_sensitivity.csv`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

![成功大學資訊工程學系 λ 敏感度](../network-analysis/ncku-cs-ie/figures/16_lambda_sensitivity.png)

*圖：成功大學資訊工程學系 λ 敏感度*  
*出處：`analysis/network-analysis/ncku-cs-ie/figures/16_lambda_sensitivity.png`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

### 4.3 taxonomy L1 覆蓋護欄

| taxonomy L1 | 教授數 | 覆蓋率 | flag |
| --- | --- | --- | --- |
| AI & Machine Learning | 28 | 56.0% | too_broad |
| Systems, Software & Architecture | 17 | 34.0% | ok |
| Vision, Multimedia & Human-Centered Computing | 17 | 34.0% | ok |
| Data, Databases & Knowledge Discovery | 14 | 28.0% | ok |
| Biomedical & Health Informatics | 11 | 22.0% | ok |
| Networks & Communications | 10 | 20.0% | ok |
| Theory & Algorithms | 7 | 14.0% | ok |
| Robotics, Control & Smart Manufacturing | 6 | 12.0% | ok |

*出處：`analysis/network-analysis/ncku-cs-ie/l1_coverage_guardrail.csv`（只列前 8 項）*  
*建構方式：計算每個 L1 分類涵蓋該單位多少比例的教授，超過 50% 標記 too_broad，代表此 L1 在本單位太寬，不能用來做 L1 roll-up 比較。*

## 5. 解讀與注意事項

- 官網英文姓名欄位多被抓成「dept. CSIE」（頁面模板文字），因此本系多數教授在資料中沒有正確的英文姓名；圖表以中文顯示，不受影響。
- 11 位教授因官網未填研究領域而未進入網路，另有 1 位孤立。
- L1 護欄標記 AI & Machine Learning 涵蓋超過 50% 教授。
- λ 敏感度未觸發過度合併，λ=0 與 λ=0.4 的社群數都是 5，集群結論穩健。
- 研究領域網路有 7 個社群，比教授網路多 2 個；「Optimization／Smart Manufacturing／Digital Twins」與「Data Science／Recommender Systems」在領域層級自成一群，但在教授層級併入其他集群。
- 研究領域來自官網自填內容，粒度與深度因人而異；網路密度與集群數反映填寫習慣的成分不可忽視，完整率不可解讀為系所或教授的品質排名。

## 附錄：本報告引用的資料與圖表清單

| 檔案 | 產生階段 / 程式 | 建構方式摘要 |
| --- | --- | --- |
| `analysis/data-collection/ncku-cs-ie/quality-report.json` | 資料蒐集 `scripts/data-collection/collect.py` | 爬取官網後統計 canonical 紀錄人數、職稱分類、中英配對率與欄位完整率 |
| `analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv` | 預處理 `1_faculty_data_preprocessing.ipynb` | 標準化後各欄位有 canonical 值的教師比例與平均項目數 |
| `.../group_comparison/research_fields/cs.csv`、`by_department/top_research_fields/ncku-cs-ie.png` | 預處理 `2_rf_and_phd_inst_comparison.ipynb` | 由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。 |
| `.../group_comparison/phd_institutions/cs.csv`、`by_department/top_phd_institutions/ncku-cs-ie.png` | 同上 | 同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。 |
| `analysis/network-analysis/ncku-cs-ie/network_metrics.json` | 網路分析 `2_build_network_data.ipynb` + `3_network_analysis.ipynb` | 由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 |
| `analysis/network-analysis/ncku-cs-ie/keyword_centrality.csv`、`keyword_communities.csv` | `3_network_analysis.ipynb` | 研究領域網路的中心性與 Louvain 社群；taxonomy 來自 `1_build_taxonomy.ipynb` |
| `analysis/network-analysis/ncku-cs-ie/professor_centrality.csv`、`professor_communities.csv`、`prof_keyword_network.graphml` | `3_network_analysis.ipynb` | 教授網路的中心性與 Louvain 集群；graphml 為二分網路，本報告用它統計各集群成員的共同領域 |
| `analysis/network-analysis/ncku-cs-ie/null_model_test.csv` | `3_network_analysis.ipynb` | 以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 |
| `analysis/network-analysis/ncku-cs-ie/lambda_sensitivity.csv` | `3_network_analysis.ipynb` | 以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。 |
| `analysis/network-analysis/ncku-cs-ie/l1_coverage_guardrail.csv` | `3_network_analysis.ipynb` | 每個 L1 涵蓋教授比例，> 50% 標記 too_broad |
| `analysis/network-analysis/ncku-cs-ie/figures/01, 05, 08, 09, 10, 13, 14, 15, 16, 27` | `3_network_analysis.ipynb` | 網路圖節點大小與 degree 或 betweenness 成正比、顏色依社群；邊數 > 400 時繪圖用 disparity filter backbone；word cloud 字級與中心性成線性正比 |

更完整的方法說明見 `docs/data-collection-report.md`、`docs/data-preprocessing-report.md`、`docs/network-analysis-report.md`。
