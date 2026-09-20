# 台灣大學資料科學學位學程（`ntu-ds`）研究結果總結報告

所屬分組：資料科學組（ds）　｜　資料日期：2026-09-09 蒐集、2026-09-10 完成網路分析

> **本報告的資料來源**
> 本專案分三個階段：(1) 資料蒐集（`scripts/data-collection/`）從 14 個系所官網爬取師資的姓名、職稱、學歷與研究領域，中英文分開蒐集後配對；
> (2) 資料預處理（`scripts/data-preprocessing/`）把職稱、學歷、研究領域標準化成英文 canonical 值，並產生描述統計；
> (3) 網路分析（`scripts/network-analysis/current-version/`）建立「教授–研究領域」二分網路，投影成研究領域網路與教授網路，做社群偵測、中心性、虛無模型與敏感度分析。
> 本報告所有數字、表格與圖表都取自 `analysis/` 底下這三個階段的輸出，每張圖表下方都標明出處與建構方式，附錄另有完整清單。
> 「研究集群」指教授網路的 Louvain 社群；「重要老師」依教授在該網路中的 degree（與多少同儕共享領域）與 betweenness（是否位於集群之間的橋梁位置）判定，**不是**學術成就的排名。

## 1. 科系速覽

台大資料科學學位學程是一個跨院整合的學程，官網列出 69 位教師，其中「核心師資」多為台大資工、電機、數學、統計與中研院的合聘教授。研究輪廓以 AI 為核心：Machine Learning 與 Artificial Intelligence 各 15 人，Deep Learning 8 人，Multimedia Systems 與 Computer Vision 各 7 人，Data Mining 與 Natural Language Processing 各 6 人；同時也有 Partial Differential Equations（5 人）、Statistics 等數學統計領域，是 ds 組中主題最寬的單位。官網未提供學歷，因此沒有博士畢業學校資料；研究領域完整率 85.5%，英文研究領域完整率只有 23.2%。

### 1.1 基本資料

| 項目 | 數值 |
| --- | --- |
| 官網師資人數（canonical 紀錄） | 69 |
| 職稱分類（一人可屬多類） | 教師（未細分） 23、專任 10、主管／講座 3、合聘 1、專案 1 |
| 中英文紀錄配對率 | 100.0% |
| 研究領域完整率（標準化後） | 85.5% |
| 學歷完整率（標準化後） | 0.0% |
| 每位教授平均研究領域數 | 2.43 |
| 進入網路分析的教授數 | 59（10 位因無研究領域排除） |

*出處：`analysis/data-collection/ntu-ds/quality-report.json`（人數、職稱、配對率）、`analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv`（完整率）、`analysis/network-analysis/ntu-ds/network_metrics.json`（進入網路人數）*  
*建構方式：quality-report 由 `scripts/data-collection/collect.py` 在爬取官網後統計 canonical 紀錄的職稱分類與中英配對；coverage 由 `1_faculty_data_preprocessing.ipynb` 計算標準化後有 canonical 值的教師比例。*

### 1.2 主要研究領域

| 排名 | 研究領域（canonical） | 教授人數 |
| --- | --- | --- |
| 1 | Machine Learning | 15 |
| 2 | Artificial Intelligence | 15 |
| 3 | Deep Learning | 8 |
| 4 | Multimedia Systems | 7 |
| 5 | Computer Vision | 7 |
| 6 | Data Mining | 6 |
| 7 | Natural Language Processing | 6 |
| 8 | Information Security | 5 |
| 9 | Partial Differential Equations | 5 |
| 10 | Optimization | 4 |
| 11 | Internet of Things | 4 |
| 12 | Reinforcement Learning | 4 |
| 13 | Data Science | 4 |
| 14 | Statistics | 4 |
| 15 | Computer Architecture | 3 |

*出處：`analysis/descriptive-stats-after-preprocessing/group_comparison/research_fields/ds.csv`（`ntu-ds` 欄）*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

![台灣大學資料科學學位學程 研究領域人數](../descriptive-stats-after-preprocessing/by_department/top_research_fields/ntu-ds.png)

*圖：台灣大學資料科學學位學程 研究領域人數*  
*出處：`analysis/descriptive-stats-after-preprocessing/by_department/top_research_fields/ntu-ds.png`*  
*建構方式：由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。*

### 1.3 博士畢業學校

官網未提供學歷資料，蒐集系統刻意不從外部網站補資料，因此本系沒有博士畢業學校統計。

## 2. 研究領域網路結構

### 2.1 網路指標

| 指標 | 數值 | 說明 |
| --- | --- | --- |
| 二分網路：教授數 / 領域數 / 邊數 | 59 / 63 / 168 | 一條邊 = 一位教授研究一個領域 |
| 二分網路連通元件數 | 9 | 最大元件涵蓋 79.7% 教授 |
| 每位教授平均 / 最多領域數 | 2.85 / 8 |  |
| 研究領域網路：節點 / 邊 | 50 / 177 | 只含至少與一個其他領域共現的領域 |
| 研究領域網路密度 | 0.144 | 實際邊數 ÷ 可能邊數 |
| 研究領域網路平均 degree | 7.08 |  |
| 研究領域網路 modularity Q（Louvain） | 0.371 | 5 個社群；resolution 0.7 / 1.3 時為 5 / 7 個 |
| 領域社群 vs taxonomy L1 一致度 | NMI 0.505 / ARI 0.226 | 1 = 完全一致，0 = 無關 |
| 教授網路：節點 / 邊 | 47 / 419 | 只含最大連通元件 |
| 教授網路密度 | 0.388 |  |
| 教授網路 modularity Q（Louvain） | 0.222 | 6 個集群 |
| 教授集群 vs 主導 L1 一致度 | NMI 0.649 / ARI 0.362 |  |

*出處：`analysis/network-analysis/ntu-ds/network_metrics.json`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

![台灣大學資料科學學位學程 教授–研究領域二分網路](../network-analysis/ntu-ds/figures/01_bipartite_network.png)

*圖：台灣大學資料科學學位學程 教授–研究領域二分網路*  
*出處：`analysis/network-analysis/ntu-ds/figures/01_bipartite_network.png`*  
*建構方式：由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。圖中兩類節點以不同顏色區分，節點大小與 degree 成正比；邊數超過 400 時繪圖使用 disparity filter backbone（α = 0.05），指標仍以完整圖計算。*

### 2.2 關鍵研究領域

| 研究領域 | Degree | Degree centrality | Betweenness | PageRank | 教授數 | taxonomy L1 |
| --- | --- | --- | --- | --- | --- | --- |
| Artificial Intelligence | 24 | 0.490 | 0.280 | 0.0756 | 15 | AI & Machine Learning |
| Computer Vision | 20 | 0.408 | 0.305 | 0.0593 | 7 | Vision, Multimedia & Human-Centered Computing |
| Machine Learning | 20 | 0.408 | 0.343 | 0.0763 | 15 | AI & Machine Learning |
| Multimedia Systems | 17 | 0.347 | 0.199 | 0.0480 | 7 | Vision, Multimedia & Human-Centered Computing |
| Deep Learning | 17 | 0.347 | 0.065 | 0.0507 | 8 | AI & Machine Learning |
| Reinforcement Learning | 13 | 0.265 | 0.024 | 0.0328 | 4 | AI & Machine Learning |
| Optimization | 12 | 0.245 | 0.074 | 0.0302 | 4 | Applied Mathematics & Operations Research |
| Data Science | 11 | 0.224 | 0.057 | 0.0284 | 4 | Data, Databases & Knowledge Discovery |
| Internet of Things | 11 | 0.224 | 0.026 | 0.0276 | 4 | Networks & Communications |
| Financial Technology | 11 | 0.224 | 0.005 | 0.0257 | 3 | Financial Engineering & Risk |
| Parallel Computing | 10 | 0.204 | 0.050 | 0.0256 | 3 | Systems, Software & Architecture |
| Data Mining | 9 | 0.184 | 0.006 | 0.0274 | 6 | Data, Databases & Knowledge Discovery |

Betweenness 最高的五個領域：Machine Learning（0.34）、Computer Vision（0.30）、Artificial Intelligence（0.28）、Multimedia Systems（0.20）、Statistics（0.09）。Betweenness 高代表該領域位於不同主題群之間的連結位置，是系上跨主題的共同語言。

*出處：`analysis/network-analysis/ntu-ds/keyword_centrality.csv`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。 degree 為相連領域數，betweenness 為經過該節點的最短路徑比例，PageRank 為加權隨機漫步的穩態機率；parent_l1 來自 `1_build_taxonomy.ipynb` 手工編定的三層 taxonomy（170 個 L3、46 個 L2、16 個 L1）。*

![台灣大學資料科學學位學程 研究領域教授人數長條圖](../network-analysis/ntu-ds/figures/10_top_keywords_bar.png)

*圖：台灣大學資料科學學位學程 研究領域教授人數長條圖*  
*出處：`analysis/network-analysis/ntu-ds/figures/10_top_keywords_bar.png`*  
*建構方式：以二分網路中每個領域節點的 degree（研究該領域的教授數）排序繪製。*

### 2.3 研究領域社群

| 社群 | 領域數 | 主要領域（教授人數） | 主要 taxonomy L1（領域數） |
| --- | --- | --- | --- |
| 0 | 14 | Multimedia Systems（7）、Internet of Things（4）、Signal Processing（3）、Wireless Networks（2）、Mobile Computing（2）、Information Retrieval（2）、Web Mining（2） | Networks & Communications 6、Data, Databases & Knowledge Discovery 3、Vision, Multimedia & Human-Centered Computing 2 |
| 1 | 11 | Artificial Intelligence（15）、Machine Learning（15）、Data Mining（6）、Natural Language Processing（6）、Information Security（5）、Big Data Analytics（3）、Game Theory（1） | AI & Machine Learning 4、Data, Databases & Knowledge Discovery 3、Security, Privacy & Cryptography 2 |
| 2 | 9 | Reinforcement Learning（4）、Parallel Computing（3）、Computer Architecture（3）、Automation and Control（3）、Electronic Design Automation（3）、Robotics（2）、Embedded Systems（2） | Systems, Software & Architecture 6、Robotics, Control & Smart Manufacturing 2、AI & Machine Learning 1 |
| 3 | 8 | Optimization（4）、Data Science（4）、Financial Technology（3）、Smart Healthcare（3）、Digital Transformation（1）、Systems Biology（1）、Generative AI（1） | Applied Mathematics & Operations Research 2、Biomedical & Health Informatics 2、Data, Databases & Knowledge Discovery 1 |
| 4 | 8 | Deep Learning（8）、Computer Vision（7）、Statistics（4）、Bayesian Statistics（2）、Causal Inference（2）、Image Processing（1）、Medical Imaging（1） | Statistics & Statistical Methods 4、Vision, Multimedia & Human-Centered Computing 2、AI & Machine Learning 1 |

*出處：`analysis/network-analysis/ntu-ds/keyword_communities.csv`（`community` 欄）、`keyword_centrality.csv`（教授人數）*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。*

![台灣大學資料科學學位學程 研究領域網路的 Louvain 社群](../network-analysis/ntu-ds/figures/05_keyword_network_communities.png)

*圖：台灣大學資料科學學位學程 研究領域網路的 Louvain 社群*  
*出處：`analysis/network-analysis/ntu-ds/figures/05_keyword_network_communities.png`*  
*建構方式：研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。節點顏色為社群，大小與 degree 成正比。*

![台灣大學資料科學學位學程 各研究領域社群的 taxonomy L1 組成](../network-analysis/ntu-ds/figures/14_community_composition.png)

*圖：台灣大學資料科學學位學程 各研究領域社群的 taxonomy L1 組成*  
*出處：`analysis/network-analysis/ntu-ds/figures/14_community_composition.png`*  
*建構方式：把每個 Louvain 領域社群內的領域依 taxonomy L1 分類計數，堆疊長條圖。用來檢查資料驅動的社群是否對應人工分類。*

![台灣大學資料科學學位學程 研究領域共現熱圖](../network-analysis/ntu-ds/figures/13_keyword_cooccurrence_heatmap.png)

*圖：台灣大學資料科學學位學程 研究領域共現熱圖*  
*出處：`analysis/network-analysis/ntu-ds/figures/13_keyword_cooccurrence_heatmap.png`*  
*建構方式：取研究領域網路的加權鄰接矩陣（共同研究兩領域的教授人數），依社群排序後繪製熱圖。*

## 3. 主要研究集群與重要老師

教授網路分成 6 個集群，但有 12 位教授因研究領域與他人不重疊而孤立（最大連通元件只涵蓋 79.7% 的教授，二分網路有 9 個連通元件），是 14 個系所中最零散的。研究領域網路的密度顯著低於虛無模型（z = -2.5）、modularity（z = 3.1）與平均共現（z = 2.8）顯著高於虛無模型，代表主題結構明確但分散。

教授網路共 47 位教授、6 個集群（Louvain，Q = 0.222）。以下依集群人數排序；集群編號與圖中的 Community 編號一致。表中 Degree 為與該教授共享研究領域的同儕數，Betweenness 為該教授位於他人最短路徑上的比例（越高越像橋梁）。

![台灣大學資料科學學位學程 教授網路的 Louvain 集群](../network-analysis/ntu-ds/figures/09_professor_network_communities.png)

*圖：台灣大學資料科學學位學程 教授網路的 Louvain 集群*  
*出處：`analysis/network-analysis/ntu-ds/figures/09_professor_network_communities.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。*

### 3.1 集群 0：人工智慧與深度學習集群（11 人）

- **成員共同研究領域**：Artificial Intelligence（10 人）、Machine Learning（6 人）、Deep Learning（4 人）、Financial Technology（3 人）、Information Security（3 人）、Computer Vision（2 人）、Multimedia Systems（2 人）
- **成員主導 taxonomy L1**：AI & Machine Learning 11 人

11 位成員全部主導 AI & Machine Learning，共享 Artificial Intelligence（10 人）、Machine Learning、Deep Learning、Financial Technology 與 Information Security。林澤 degree 最高（31）且 betweenness 最高（0.099），與電信所合聘；鄭文皇（電腦視覺、金融科技、數位轉型）與台大資工合聘；孫紹華（強化學習、機器人）、陳駿丞（電腦視覺、資安）、連云暄（生成式 AI）是主要成員。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 林澤（2 個系所） | Lin, Che | 教師（未細分） | 31 | 0.099 | Artificial Intelligence、Data Science、Deep Learning、Financial Technology、Optimization |
| 鄭文皇（2 個系所） | Cheng, Wen-Huang | 教師（未細分） | 30 | 0.058 | Artificial Intelligence、Computer Vision、Digital Transformation、Financial Technology、Machine Learning |
| 林仁俊 | Lin, Jen-Chun | — | 28 | 0.002 | Artificial Intelligence、Machine Learning、Multimedia Systems |
| 孫紹華（2 個系所） | Sun, Shao-Hua | 專任 | 27 | 0.075 | Artificial Intelligence、Machine Learning、Reinforcement Learning、Robotics |
| 陳駿丞 | Chen, Jun-Cheng | — | 27 | 0.032 | Artificial Intelligence、Computer Vision、Deep Learning、Information Security |
| 連云暄 | Lien, Yun-Hsuan | — | 25 | 0.006 | Artificial Intelligence、Financial Technology、Generative AI、Reinforcement Learning |
| 修丕承 | Hsiu, Pi-Cheng | — | 25 | 0.000 | Artificial Intelligence、Deep Learning |
| 劉子毓（2 個系所） | Liu, Tzu-Yu | 專任 | 25 | 0.000 | Artificial Intelligence、Bioinformatics、Machine Learning |

其餘成員（3 位，依 degree 排序）：吳廸融、林宗男、謝宏昀


### 3.2 集群 1：多媒體、電腦視覺與物聯網集群（9 人）

- **成員共同研究領域**：Multimedia Systems（5 人）、Internet of Things（4 人）、Signal Processing（2 人）、Wireless Communications（2 人）、Big Data Analytics（2 人）、Computer Vision（2 人）、Deep Learning（2 人）
- **成員主導 taxonomy L1**：Networks & Communications 5 人、Vision, Multimedia & Human-Centered Computing 2 人、Data, Databases & Knowledge Discovery 2 人

9 位成員，主導 taxonomy 混合 Networks & Communications、Vision 與 Data，共享 Multimedia Systems、Internet of Things、Signal Processing 與 Computer Vision。陳祝嵩 degree 30、betweenness 0.118 為集群最高，研究電腦視覺、深度學習與影像處理；王建堯（電腦視覺、多媒體）次之；巫芳璟、王志宇、陳伶志代表物聯網與行動運算軸線；鄭卜壬代表資訊檢索與網路探勘。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 陳祝嵩（2 個系所） | Chen, Chu-Song | 教師（未細分） | 30 | 0.118 | Big Data Analytics、Computer Vision、Deep Learning、Image Processing、Machine Learning |
| 王建堯 | Wang, Chien Yao | — | 25 | 0.086 | Computer Vision、Deep Learning、Machine Learning、Multimedia Systems、Signal Processing |
| 巫芳璟（2 個系所） | Wu, Fang-Jing | 專任 | 19 | 0.012 | Artificial Intelligence、Internet of Things、Mobile Computing、Pervasive Computing、Privacy-Preserving Computing |
| 鄭卜壬（2 個系所） | Cheng, Pu-Jen | 教師（未細分） | 17 | 0.024 | Databases、Information Retrieval、Multimedia Systems、Web Mining |
| 王志宇 | Wang, Chih-Yu | — | 16 | 0.028 | Data Science、Internet of Things、Wireless Communications |
| 陳伶志 | Chen, Ling-Jyh | — | 15 | 0.000 | Big Data Analytics、Internet of Things |
| 張佑榕 | Chang, Ronald Y. | — | 11 | 0.003 | Signal Processing、Wireless Communications |
| 廖婉君（3 個系所） | Liao, Wanjiun | 主管／講座 | 10 | 0.007 | Blockchain、Computer Networks、Internet of Things、Multimedia Systems、Wireless Networks |

其餘成員（1 位，依 degree 排序）：黃彥男


### 3.3 集群 2：資料探勘與最佳化集群（8 人）

- **成員共同研究領域**：Data Mining（5 人）、Machine Learning（5 人）、Smart Healthcare（3 人）、Data Science（2 人）、Optimization（2 人）、Game Theory（1 人）、Information Security（1 人）
- **成員主導 taxonomy L1**：AI & Machine Learning 4 人、Biomedical & Health Informatics 2 人、Data, Databases & Knowledge Discovery 1 人、Applied Mathematics & Operations Research 1 人

8 位成員，共享 Data Mining（5 人）、Machine Learning、Smart Healthcare、Data Science 與 Optimization。葉彌妍 degree 30 為集群最高，李育杰（資料探勘、最佳化）、陳尚澤（賽局、資安、機器學習）、王釧茹是核心；陳銘憲為 3 個系所合聘的資深教授；王偉仲帶入科學計算與智慧醫療，betweenness 最高（0.077）。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 葉彌妍 | Yeh, Mi-Yen | — | 30 | 0.043 | Artificial Intelligence、Big Data Analytics、Data Mining、Machine Learning |
| 李育杰 | Lee, Yuh-Jye | — | 27 | 0.039 | Data Mining、Data Science、Machine Learning、Optimization |
| 陳尚澤（2 個系所） | Chen, Shang-Tse | 專任 | 27 | 0.025 | Data Mining、Game Theory、Information Security、Machine Learning |
| 陳銘憲（3 個系所） | Chen, Ming-Syan | 主管／講座 | 26 | 0.000 | Data Mining、Machine Learning |
| 王釧茹 | Wang, Chuan-Ju | — | 26 | 0.000 | Data Mining、Machine Learning |
| 王偉仲 | Wei-Chung Wang | 教師（未細分） | 16 | 0.077 | Data Science、Optimization、Scientific Computing、Smart Healthcare |
| 陳君厚 | Chun-Houh Chen | — | 3 | 0.000 | Smart Healthcare |
| 楊欣洲（2 個系所） | Hsin-Chou Yang | — | 3 | 0.000 | Smart Healthcare |

### 3.4 集群 3：系統、架構與電子設計自動化集群（7 人）

- **成員共同研究領域**：Automation and Control（3 人）、Electronic Design Automation（3 人）、Computer Architecture（3 人）、Parallel Computing（3 人）、Embedded Systems（2 人）、Compilers（1 人）、Optimization（1 人）
- **成員主導 taxonomy L1**：Systems, Software & Architecture 5 人、Robotics, Control & Smart Manufacturing 2 人

7 位成員，5 位主導 Systems, Software & Architecture，共享 Automation and Control、Electronic Design Automation、Computer Architecture 與 Parallel Computing。李濬屹 degree 28、betweenness 0.203 為全系最高，研究自動化、計算機架構、電腦視覺與數位孿生，是這個系統集群連到 AI 集群的唯一強橋；洪士灝（架構、嵌入式、平行計算）次之；張耀文、江介宏代表 EDA。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 李濬屹（2 個系所） | Lee, Chun-Yi | 教師（未細分） | 28 | 0.203 | Automation and Control、Computer Architecture、Computer Vision、Digital Twins、Electronic Design Automation |
| 洪士灝（2 個系所） | Hung, Shih-Hao | 教師（未細分） | 9 | 0.071 | Computer Architecture、Embedded Systems、Optimization、Parallel Computing |
| 張耀文（2 個系所） | Chang, Yao-Wen | 教師（未細分） | 5 | 0.000 | Automation and Control、Electronic Design Automation |
| 江介宏 | Jiang, Jie-Hong Roland | 教師（未細分） | 5 | 0.000 | Automation and Control、Electronic Design Automation |
| 鄭湘筠 | Cheng, Hsiang-Yun | — | 4 | 0.000 | Computer Architecture |
| 張原豪（2 個系所） | Chang, Yuan-Hao | 教師（未細分） | 2 | 0.000 | Embedded Systems |
| 洪鼎詠（2 個系所） | Hong, Ding-Yong | — | 2 | 0.000 | Compilers、Parallel Computing |

### 3.5 集群 4：自然語言處理集群（7 人）

- **成員共同研究領域**：Natural Language Processing（6 人）、Artificial Intelligence（3 人）、Information Retrieval（1 人）、Web Mining（1 人）、Computational Linguistics（1 人）、Data Mining（1 人）、Social Network Analysis（1 人）
- **成員主導 taxonomy L1**：AI & Machine Learning 6 人、Data, Databases & Knowledge Discovery 1 人

7 位成員，6 位主導 AI & Machine Learning，共享 Natural Language Processing（6 人）與 Artificial Intelligence。林守德（AI、資料探勘、NLP、社會網路分析）degree 27 為集群最高，馬偉雲次之；陳縕儂、古倫維、陳信希是 NLP 與資訊檢索的核心；曹昱代表語音訊號處理。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 林守德（2 個系所） | Lin, Shou-De | 教師（未細分） | 27 | 0.042 | Artificial Intelligence、Data Mining、Natural Language Processing、Social Network Analysis |
| 馬偉雲 | Ma, Wei-Yun | — | 26 | 0.041 | Deep Learning、Machine Learning、Natural Language Processing |
| 陳縕儂（2 個系所） | Chen, Yun-Nung | 教師（未細分） | 18 | 0.001 | Artificial Intelligence、Natural Language Processing |
| 古倫維（2 個系所） | Ku, Lun-Wei | — | 18 | 0.001 | Artificial Intelligence、Computational Linguistics、Natural Language Processing |
| 陳信希（2 個系所） | Chen, Hsin-Hsi | 主管／講座 | 17 | 0.008 | Information Retrieval、Natural Language Processing、Web Mining |
| 曹昱 | Tsao, Yu | — | 14 | 0.001 | Signal Processing、Speech Recognition |
| 黃瀚萱 | Huang, Hen-Hsen | — | 6 | 0.000 | Natural Language Processing |

### 3.6 集群 5：統計與因果推論集群（5 人）

- **成員共同研究領域**：Statistics（4 人）、Bayesian Statistics（2 人）、Computer Vision（2 人）、Causal Inference（2 人）、Deep Learning（1 人）、Medical Imaging（1 人）、Multivariate Analysis（1 人）
- **成員主導 taxonomy L1**：Statistics & Statistical Methods 4 人、AI & Machine Learning 1 人

5 位成員，共享 Statistics、Bayesian Statistics、Causal Inference。楊鈞澔（貝氏統計、電腦視覺、深度學習、醫學影像）degree 28，吳沛遠（電腦視覺、資安、強化學習、統計）betweenness 0.112，兩人是統計集群連到 AI 集群的橋；柏嘉偲、黃名鉞、顏佐榕是純統計成員。

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 研究領域（最多列 5 項） |
| --- | --- | --- | --- | --- | --- |
| 楊鈞澔 | Chun-Hao Yang | 專任 | 28 | 0.047 | Bayesian Statistics、Computer Vision、Deep Learning、Medical Imaging、Statistics |
| 吳沛遠（2 個系所） | Wu, Pei-Yuan | 專任 | 26 | 0.112 | Computer Vision、Information Security、Machine Learning、Reinforcement Learning、Statistics |
| 柏嘉偲 | Gaspard Bernard | — | 4 | 0.043 | Causal Inference、Multivariate Analysis、Statistics |
| 黃名鉞 | Ming-Yueh Huang | — | 4 | 0.000 | Causal Inference |
| 顏佐榕 | Tso-Jung Yen | — | 4 | 0.000 | Bayesian Statistics、Statistics |

*集群表出處：`analysis/network-analysis/ntu-ds/professor_communities.csv`（集群歸屬）、`professor_centrality.csv`（degree、betweenness、職稱類別）、`prof_keyword_network.graphml`（成員研究領域，用來統計集群的共同領域）*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 職稱類別為官網職稱的分類，一人可屬多類時取主要類別；「N 個系所」表示該教授也出現在其他系所名單。*

### 3.7 全系的橋接者與樞紐

Betweenness 最高的教授（跨集群的橋梁）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 李濬屹 | Lee, Chun-Yi | 教師（未細分） | 28 | 0.203 | Systems, Software & Architecture |
| 陳祝嵩 | Chen, Chu-Song | 教師（未細分） | 30 | 0.118 | Vision, Multimedia & Human-Centered Computing |
| 吳沛遠 | Wu, Pei-Yuan | 專任 | 26 | 0.112 | AI & Machine Learning |
| 林澤 | Lin, Che | 教師（未細分） | 31 | 0.099 | AI & Machine Learning |
| 王建堯 | Wang, Chien Yao | — | 25 | 0.086 | Vision, Multimedia & Human-Centered Computing |
| 王偉仲 | Wei-Chung Wang | 教師（未細分） | 16 | 0.077 | Applied Mathematics & Operations Research |

Degree 最高的教授（與最多同儕共享領域的樞紐）：

| 姓名 | 英文名 | 職稱類別 | Degree | Betweenness | 主導 L1 |
| --- | --- | --- | --- | --- | --- |
| 林澤 | Lin, Che | 教師（未細分） | 31 | 0.099 | AI & Machine Learning |
| 鄭文皇 | Cheng, Wen-Huang | 教師（未細分） | 30 | 0.058 | AI & Machine Learning |
| 葉彌妍 | Yeh, Mi-Yen | — | 30 | 0.043 | AI & Machine Learning |
| 陳祝嵩 | Chen, Chu-Song | 教師（未細分） | 30 | 0.118 | Vision, Multimedia & Human-Centered Computing |
| 李濬屹 | Lee, Chun-Yi | 教師（未細分） | 28 | 0.203 | Systems, Software & Architecture |
| 楊鈞澔 | Chun-Hao Yang | 專任 | 28 | 0.047 | Statistics & Statistical Methods |

*出處：`analysis/network-analysis/ntu-ds/professor_centrality.csv`*

![台灣大學資料科學學位學程 教授網路（節點大小 = betweenness）](../network-analysis/ntu-ds/figures/08_professor_network_betweenness.png)

*圖：台灣大學資料科學學位學程 教授網路（節點大小 = betweenness）*  
*出處：`analysis/network-analysis/ntu-ds/figures/08_professor_network_betweenness.png`*  
*建構方式：教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。此圖節點大小改為與 betweenness 成正比。*

![台灣大學資料科學學位學程 各集群教授 word cloud（字級 = degree）](../network-analysis/ntu-ds/figures/27_professor_wordcloud_degree_by_community.png)

*圖：台灣大學資料科學學位學程 各集群教授 word cloud（字級 = degree）*  
*出處：`analysis/network-analysis/ntu-ds/figures/27_professor_wordcloud_degree_by_community.png`*  
*建構方式：依 Louvain 集群分塊、同集群同色的教授姓名 word cloud，字級與 degree 成線性正比並設下限。*

另有 12 位教授雖有研究領域，但與其他教授沒有共享任何領域，孤立於最大連通元件之外，不屬於任何集群。

## 4. 結構穩健性檢驗

### 4.1 虛無模型檢定

| 統計量 | 觀測值 | 虛無平均 | 虛無標準差 | z-score | empirical p | p < 0.05 |
| --- | --- | --- | --- | --- | --- | --- |
| 領域網路密度 | 0.1445 | 0.1600 | 0.0061 | -2.53 | 0.016 | 顯著 |
| 領域網路 modularity Q | 0.3714 | 0.2919 | 0.0254 | 3.13 | 0.010 | 顯著 |
| 領域平均共現次數 | 1.2938 | 1.2035 | 0.0318 | 2.84 | 0.024 | 顯著 |
| 教授網路 clustering 係數 | 0.7068 | 0.6775 | 0.0280 | 1.04 | 0.332 | 不顯著 |

*出處：`analysis/network-analysis/ntu-ds/null_model_test.csv`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 密度顯著偏低而 modularity、共現顯著偏高，代表領域共現集中在少數主題群，不是均勻分布。*

![台灣大學資料科學學位學程 觀測值 vs 虛無模型分布](../network-analysis/ntu-ds/figures/15_null_model_comparison.png)

*圖：台灣大學資料科學學位學程 觀測值 vs 虛無模型分布*  
*出處：`analysis/network-analysis/ntu-ds/figures/15_null_model_comparison.png`*  
*建構方式：以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。*

### 4.2 λ 敏感度

| λ | 邊數 | 密度 | Q | 集群數 | 密度相對 baseline | Q 下降 | 過度合併 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.0 | 302 | 0.279 | 0.248 | 6 | +0% | 0.000 | 否 |
| 0.3 | 419 | 0.388 | 0.224 | 6 | +39% | 0.024 | 否 |
| 0.4 | 419 | 0.388 | 0.222 | 6 | +39% | 0.026 | 否 |
| 0.5 | 419 | 0.388 | 0.219 | 6 | +39% | 0.029 | 否 |

*出處：`analysis/network-analysis/ntu-ds/lambda_sensitivity.csv`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

![台灣大學資料科學學位學程 λ 敏感度](../network-analysis/ntu-ds/figures/16_lambda_sensitivity.png)

*圖：台灣大學資料科學學位學程 λ 敏感度*  
*出處：`analysis/network-analysis/ntu-ds/figures/16_lambda_sensitivity.png`*  
*建構方式：以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。*

### 4.3 taxonomy L1 覆蓋護欄

| taxonomy L1 | 教授數 | 覆蓋率 | flag |
| --- | --- | --- | --- |
| AI & Machine Learning | 29 | 61.7% | too_broad |
| Data, Databases & Knowledge Discovery | 13 | 27.7% | ok |
| Vision, Multimedia & Human-Centered Computing | 13 | 27.7% | ok |
| Security, Privacy & Cryptography | 7 | 14.9% | ok |
| Systems, Software & Architecture | 7 | 14.9% | ok |
| Biomedical & Health Informatics | 6 | 12.8% | ok |
| Networks & Communications | 6 | 12.8% | ok |
| Applied Mathematics & Operations Research | 5 | 10.6% | ok |

*出處：`analysis/network-analysis/ntu-ds/l1_coverage_guardrail.csv`（只列前 8 項）*  
*建構方式：計算每個 L1 分類涵蓋該單位多少比例的教授，超過 50% 標記 too_broad，代表此 L1 在本單位太寬，不能用來做 L1 roll-up 比較。*

## 5. 解讀與注意事項

- 12 位教授孤立於教授網路之外（例如只研究 Partial Differential Equations、Algebraic Geometry 等數學主題的教師），這些人不會出現在任何集群中；另有 10 位因官網未填研究領域而排除。
- 官網未提供學歷，本報告沒有博士畢業學校的資料。
- L1 護欄標記 AI & Machine Learning 涵蓋超過 50% 教授。
- λ 敏感度未觸發過度合併，λ=0 與 λ=0.4 的社群數都是 6，集群結論穩健。
- 官網英文姓名格式為「Lin, Che」，與其他系所不同；本學程多數核心師資同時出現在台大資工、電信所的名單中，系所層級不去重。
- 研究領域來自官網自填內容，粒度與深度因人而異；網路密度與集群數反映填寫習慣的成分不可忽視，完整率不可解讀為系所或教授的品質排名。

## 附錄：本報告引用的資料與圖表清單

| 檔案 | 產生階段 / 程式 | 建構方式摘要 |
| --- | --- | --- |
| `analysis/data-collection/ntu-ds/quality-report.json` | 資料蒐集 `scripts/data-collection/collect.py` | 爬取官網後統計 canonical 紀錄人數、職稱分類、中英配對率與欄位完整率 |
| `analysis/descriptive-stats-after-preprocessing/coverage_by_school.csv` | 預處理 `1_faculty_data_preprocessing.ipynb` | 標準化後各欄位有 canonical 值的教師比例與平均項目數 |
| `.../group_comparison/research_fields/ds.csv`、`by_department/top_research_fields/ntu-ds.png` | 預處理 `2_rf_and_phd_inst_comparison.ipynb` | 由 `scripts/data-preprocessing/2_rf_and_phd_inst_comparison.ipynb` 產生。研究領域為官網「主要研究領域」與「研究領域摘要」分別清洗、以雙語詞典標準化成英文 canonical 值後取聯集；計數為具有該領域的不重複教師人數，不做 Top-N 截斷。 |
| `.../group_comparison/phd_institutions/ds.csv`、`by_department/top_phd_institutions/ntu-ds.png` | 同上 | 同一 notebook。學歷先被 `1_faculty_data_preprocessing.ipynb` 解析成「學位、科系、學校」三部分，取學位為博士的項目，學校名稱以別名表對應為英文 canonical 值；計數為不重複教師人數。 |
| `analysis/network-analysis/ntu-ds/network_metrics.json` | 網路分析 `2_build_network_data.ipynb` + `3_network_analysis.ipynb` | 由 `2_build_network_data.ipynb` 從 `faculty_standardized.json` 建立教授–研究領域二分網路：教授與研究領域各為一類節點，教授的標準化研究領域包含某領域即連一條邊。研究領域網路是二分網路的單邊投影：兩個領域若被同一位教授研究就相連，邊權為共同研究兩領域的教授人數。社群以 Louvain（seed = 42，resolution 1.0）偵測，指標以完整加權圖計算。教授網路是二分網路的另一邊投影：兩位教授共享研究領域就相連，邊權 w = S_exp + λ·S_inf；S_exp 為共享領域的 IDF 加權和（IDF 以全體 662 位教授計算一次），S_inf 為共享 taxonomy 上層分類的推論相似度，λ = 0.4。社群以 Louvain（seed = 42，resolution 1.0）偵測，節點大小與 degree 成正比。 |
| `analysis/network-analysis/ntu-ds/keyword_centrality.csv`、`keyword_communities.csv` | `3_network_analysis.ipynb` | 研究領域網路的中心性與 Louvain 社群；taxonomy 來自 `1_build_taxonomy.ipynb` |
| `analysis/network-analysis/ntu-ds/professor_centrality.csv`、`professor_communities.csv`、`prof_keyword_network.graphml` | `3_network_analysis.ipynb` | 教授網路的中心性與 Louvain 集群；graphml 為二分網路，本報告用它統計各集群成員的共同領域 |
| `analysis/network-analysis/ntu-ds/null_model_test.csv` | `3_network_analysis.ipynb` | 以保持二分結構與雙邊 degree 序列的 double edge swap（nswap = 10 × 邊數）產生 1,000 個隨機網路，比較觀測值與虛無分布，輸出 z-score 與雙尾 empirical p-value。 |
| `analysis/network-analysis/ntu-ds/lambda_sensitivity.csv` | `3_network_analysis.ipynb` | 以 λ ∈ {0, 0.3, 0.4, 0.5} 各建一次教授網路，λ = 0 為 baseline；密度較 baseline 增加超過 50% 或 Q 下降超過 0.1 即標記為過度合併。 |
| `analysis/network-analysis/ntu-ds/l1_coverage_guardrail.csv` | `3_network_analysis.ipynb` | 每個 L1 涵蓋教授比例，> 50% 標記 too_broad |
| `analysis/network-analysis/ntu-ds/figures/01, 05, 08, 09, 10, 13, 14, 15, 16, 27` | `3_network_analysis.ipynb` | 網路圖節點大小與 degree 或 betweenness 成正比、顏色依社群；邊數 > 400 時繪圖用 disparity filter backbone；word cloud 字級與中心性成線性正比 |

更完整的方法說明見 `docs/data-collection-report.md`、`docs/data-preprocessing-report.md`、`docs/network-analysis-report.md`。
