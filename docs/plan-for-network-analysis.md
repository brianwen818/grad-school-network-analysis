# 教授－研究領域 網路分析執行計畫

撰寫時間：2026-09-09
狀態：待執行
先前範例：`scripts/network-analysis/previous-examples/`（HKUST FM，兩本 notebook；第三方素材，未隨本專案發布，概念整理見該目錄的 `core-ideas.md`）

## 0. 研究問題

沿用 HKUST FM 範例的核心問題，套用到 14 個台灣研究所：

> **每個校系的教授研究哪些主題，以及教授和研究領域之間形成什麼樣的網路結構。**

在三個層級各回答一次：

| 層級 | 單位 | 數量 |
| --- | --- | --- |
| 系所層級 | 單一 `school_id` | 14 個 |
| 組層級 | `cs` / `ds` / `fin-and-econ` | 3 個 |
| 全體層級 | 全部 14 校系 | 1 個 |

組層級額外回答一個系所層級做不到的問題：**社群結構是被學校決定，還是被研究主題決定？**

### 校系分組

| group | school_id |
| --- | --- |
| `fin-and-econ` | `nccu-fin`、`nccu-mb`、`nthu-qf`、`ntu-econ`、`ntu-fin`、`nycu-info-mag-fin` |
| `ds` | `ncku-stats-ds`、`ntu-comm-engin-ds-network`、`ntu-ds` |
| `cs` | `ncku-cs-ie`、`nthu-cs`、`ntu-cs-ie`、`ntu-im`、`nycu-cs` |

## 1. 資料來源與現況

輸入為 `data/data-preprocessing/` 的預處理成果，**不重跑也不修改**前段流程：

- `faculty_standardized.json`：741 筆，主要使用 `faculty_id`、`school_id`、`professor_name`、`name_en`、`emails`、`research_interests_standardized_en`、`education_structured`、`role_groups`。
- `research_interests_standardized_long.csv`：長表，1,953 列。

### 關鍵基線數字

| 項目 | 數值 |
| --- | --- |
| 教授總數 | 741 |
| 有標準化研究領域者 | 662（89.3%） |
| canonical 研究領域 unique 值 | 170 |
| 每位教授平均領域數 | 2.95（中位數 3、最大 10） |
| 只有 1 人研究的領域 | 16 / 170 |
| 最大領域 `Artificial Intelligence` | 109 人（佔 662 的 16.5%） |
| 跨校重複教授（合聘） | 38 人、79 筆紀錄 |

### 各系所研究領域覆蓋率

| school_id | 教授數 | 有研究領域 | 覆蓋率 |
| --- | ---: | ---: | ---: |
| `nccu-fin` | 23 | 23 | 100.0% |
| `nccu-mb` | 22 | 18 | 81.8% |
| `ncku-cs-ie` | 62 | 51 | 82.3% |
| `ncku-stats-ds` | 47 | 39 | 83.0% |
| `nthu-cs` | 81 | 76 | 93.8% |
| `nthu-qf` | 19 | 17 | 89.5% |
| `ntu-comm-engin-ds-network` | 25 | 25 | 100.0% |
| `ntu-cs-ie` | 90 | 88 | 97.8% |
| `ntu-ds` | 69 | 59 | 85.5% |
| `ntu-econ` | 49 | 44 | 89.8% |
| `ntu-fin` | 43 | 32 | 74.4% |
| `ntu-im` | 31 | 30 | 96.8% |
| `nycu-cs` | 152 | 141 | 92.8% |
| `nycu-info-mag-fin` | 28 | 19 | 67.9% |

覆蓋率差距達 32 個百分點（67.9% ~ 100%）。**所有跨單位比較一律使用密度、平均分支度、modularity 等正規化指標，禁止直接比較節點數或邊數**，且每張比較表必須併列 coverage 欄位。

### 資料注意事項

- `name_zh` 部分紀錄含殘留前綴（例：`": 吳啟銘"`）。去重與顯示一律使用已清理的 `professor_name`。
- `research_interests_standardized_en` 已是「主要研究領域」與「研究領域摘要」的聯集去重結果，直接採用，不再拆分。
- 沒有研究領域的 79 位教授不進入網路，但會在每個單位的 `network_metrics.json` 中明確記錄排除人數。

## 2. 設計決策（已確認）

| # | 決策 |
| --- | --- |
| D1 | 建立三層 research taxonomy，但 **parent 只作為節點屬性，不注入為節點或邊** |
| D2 | 粒度落差以 **IDF 加權 + parent 折扣（λ）相似度** 解決，λ 預設 0.4，做 0 / 0.3 / 0.5 敏感度分析 |
| D3 | 系所層級不去重；**組層級與全體層級以 `person_id` 去重，研究領域取聯集**，`school_id` 轉為多值屬性 |
| D4 | Taxonomy 由本流程直接建立完成後即往下跑，草案同時輸出供事後稽核 |

### D1 的理由

`Artificial Intelligence` 已佔 662 人中的 109 人。若將 `Deep Learning`(54)、`Computer Vision`(54)、`Natural Language Processing`(22)、`Reinforcement Learning`(12)、`Generative AI`(7) 等 roll-up 成 AI 節點，該節點將涵蓋 250 人以上，professor 投影後 `cs` 組近乎完全圖——這正是「所有經濟系教授都在研究經濟學」的失敗模式。因此 parent 只上色、只作為社群偵測的對照基準，不製造連線。

### D2 的公式

令分析單位內教授集合為 `P`，教授 A 的領域集合為 `K_A`，領域 k 在全體的持有人數為 `n_k`。

**逆頻率權重（以全體 662 位教授計算一次，跨單位共用以保持可比性）**

```
IDF(k) = ln(1 + N_all / n_k)          N_all = 662
```

**教授－教授邊權重**

```
S_exp(A,B) = Σ            IDF(k)                          # 明確共同領域
             k ∈ K_A ∩ K_B

S_inf(A,B) = Σ            max        sqrt( IDF(i)·IDF(j) )   # 同 parent 的不同領域
             p ∈ 共同L2   i ∈ K_A\K_B
                          j ∈ K_B\K_A
                          parent_L2(i) = parent_L2(j) = p

w(A,B) = S_exp(A,B) + λ · S_inf(A,B)          λ = 0.4
```

`S_inf` **每個共同 L2 parent 只取貢獻最大的一組配對**，避免某位教授在同一 parent 下掛多個子領域時權重爆炸。

同時輸出餘弦正規化版本作為邊屬性，供不同規模單位比較：

```
w_cos(A,B) = w(A,B) / sqrt( Σ_{k∈K_A} IDF(k)² · Σ_{k∈K_B} IDF(k)² )
```

**領域－領域邊權重**：共同研究該兩領域的教授人數（原始共現次數），另存 Jaccard 與餘弦正規化值。此處不套用 λ，parent 資訊改以節點屬性表示。

### D3 的理由

38 位教授跨校重複出現，組內分布如下：

| group | 組內跨校重複人數 | 組內紀錄數 |
| --- | ---: | ---: |
| `ds` | 10 | 134 |
| `cs` | 6 | 413 |
| `fin-and-econ` | 1 | 177 |

重疊最重的配對為 `ntu-cs-ie ↔ ntu-ds`（16 人）、`ntu-comm-engin-ds-network ↔ ntu-ds`（9 人）、`ntu-comm-engin-ds-network ↔ ntu-cs-ie`（5 人）。`ds` 組僅 134 筆紀錄卻有 10 位重複教授，若不去重會憑空製造跨校橋接——同一個人跟自己被視為兩位研究主題相同的教授。

**去重規則**

1. `person_id` 優先以正規化 email（小寫、去空白）判定。
2. 無 email 時以 `professor_name`（非空中文名）比對，並要求 `name_en` 正規化後相容或其一為空。
3. 同名但 email 不同 → 視為不同人，寫入 `person_identity_map.csv` 並標記 `status = name_collision_kept_separate` 供人工覆核。
4. 合併後 `research_interests_standardized_en` 取**聯集去重**。教授可能在 A 系與 B 系列出不同的研究領域，聯集才是該教授完整的研究輪廓；同時記錄 `keyword_source_schools` 保留每個領域來自哪一個系所的網頁。
5. `school_ids`、`faculty_ids`、`titles` 轉為多值屬性，`n_appointments` 記錄合聘數。
6. 系所層級一律不去重；同時保留組層級「未去重版本」作為 robustness check。

## 3. 執行階段

程式置於 `scripts/network-analysis/current-version/`，四本 notebook 依序執行。

### Stage 1 — `1_build_taxonomy.ipynb`

建立固定的三層研究領域階層。

1. 讀入 170 個 canonical 值與其人數。
2. 以確定性規則 + 人工編定的對照表指派 `parent_l2`、`parent_l1`。L2 約 35~45 個、L1 約 12~16 個。
3. L1 的粒度必須維持「系所內仍具鑑別力」，例如採 `AI & Machine Learning`、`Vision & Multimedia`、`Systems & Architecture`、`Networks & Security`、`Theory & Algorithms`、`Data & Databases`、`Corporate Finance`、`Asset Pricing & Markets`、`Econometrics & Statistics`、`Macro & Policy Economics`、`Information Systems & Management`、`Applied Math & OR` 等，**不得使用 `Computer Science`、`Economics` 這類全系涵蓋的類別**。
4. 每個 canonical 值本身即 L3。`source` 欄位記錄 `explicit`（教授原文寫的層級）或 `inferred`（由 taxonomy 推得的上層）。
5. 輸出 `data/network-analysis/research_taxonomy.csv`，欄位：
   `keyword_en, parent_l2, parent_l1, faculty_count, source, note`
6. 驗證：170 個值全數有 L2 與 L1；無孤兒；每個 L1 至少含 2 個 L2。

此表為**固定資產**，後續分析一律讀取，不動態推斷。

### Stage 2 — `2_build_network_data.ipynb`

對應範例的 Notebook 1，產生網路資料表。**不使用 `pinyin` 與 `googletrans`**——預處理階段已完成確定性雙語標準化，引入即時翻譯會破壞可重現性。

1. 讀 `faculty_standardized.json` 與 `research_taxonomy.csv`。
2. 建立 `person_identity_map.csv`（D3 規則）。
3. 計算全體 IDF 表 `keyword_idf.csv`。
4. 針對 18 個分析單位（14 系所 + 3 組 + 1 全體）各產生三份表：
   - `professor_nodes.csv`：`node_id, professor_name, name_en, school_ids, role_groups, n_keywords, phd_institution, n_appointments`
   - `keyword_nodes.csv`：`keyword_en, parent_l2, parent_l1, n_faculty_in_unit, n_faculty_overall, idf`
   - `prof_keyword_edges.csv`：`node_id, keyword_en, source`
5. 驗證：邊表中的 keyword 全數存在於 taxonomy；系所節點數與 §1 覆蓋率表一致；組層級去重後人數 = 原紀錄數 − 組內重複人數。

### Stage 3 — `3_network_analysis.ipynb`

對應範例的 Notebook 2，對每個分析單位執行同一套流程。

**3.1 Professor–Keyword 二分網路**
- `nx.Graph`，`bipartite=0`（教授）/ `bipartite=1`（領域）。
- 網路層級指標：節點數、邊數、density、degree 分布、連通元件數。
- 找出 largest connected component（LCC），記錄其涵蓋比例。

**3.2 Keyword–Keyword 網路**（由 LCC 投影）
- `nx.bipartite.weighted_projected_graph`，權重為共現人數。
- 中心性：degree、weighted degree(strength)、betweenness（距離 = 1/w）、closeness、eigenvector、PageRank、clustering coefficient。
- 社群偵測：**Louvain**（`nx.community.louvain_communities`，`seed=42`，resolution 掃 0.7 / 1.0 / 1.3），回報 modularity Q。節點數 < 60 時另跑 Girvan–Newman 作為對照。
- **Taxonomy 對齊檢驗**：偵測出的社群 vs `parent_l1` 標籤的 NMI 與 ARI。
- degree 與 betweenness 的 Pearson 相關（沿用範例）。

**3.3 Professor–Professor 網路**（由 LCC 投影）
- 依 D2 公式計算 `w(A,B)`，同時存 `w_cos`。
- 同一套中心性與 Louvain 社群偵測。
- assortativity（依主要 `parent_l1`、依 `role_groups`）。

**3.4 虛無模型檢定**
- 以 `nx.double_edge_swap`（保持二分結構與雙邊 degree 序列，`nswap = 10 × |E|`）產生 1,000 個隨機網路。
- 對比觀測值與虛無分布：keyword 網路 density、modularity Q、平均共現次數、professor 網路 clustering coefficient。
- 輸出 z-score 與 empirical p-value。**這一步是讓結論從「一張圖」變成「一個發現」的關鍵。**

**3.5 λ 敏感度與護欄**
- λ ∈ {0, 0.3, 0.4, 0.5} 各跑一次，輸出對照表：density、平均 degree、LCC 佔比、社群數、modularity Q。λ=0 為 baseline。
- **L1 過寬護欄**：任一 `parent_l1` 在該單位覆蓋率 > 50% 即標記 `too_broad`，不得用於該單位的 L1 roll-up 視角，並在報告中揭露。
- 若某 λ 使 density 相對 baseline 增加超過 50%，或 modularity Q 下降超過 0.1，於報告中標示為過度合併。

**3.6 視覺化**

所有圖檔一律存入 `analysis/network-analysis/`，不寫入 `data/`，也不只留在 notebook 輸出中。

**3.6.1 圖中文字語言規則（強制）**

- 圖中所有文字——標題、軸標籤、圖例、社群名稱、研究領域節點標籤、colorbar、註解——**一律使用英文**。
- **唯一例外是教授姓名**：使用 `professor_name`。此欄位在預處理階段已定義為「優先中文、缺中文時退回英文」，因此直接採用即符合規則，不需額外邏輯。入網的 662 位教授中有 **13 位沒有中文名**（`ncku-stats-ds` 7 位、`ntu-econ` 4 位、`nthu-cs` 2 位），這些人在圖中顯示英文姓名。
- 因此中文字型只會用在 professor 節點標籤上。字型以偵測方式取得（`msjh.ttc` → `Microsoft JhengHei` → `sans-serif` fallback），不硬寫絕對路徑；偵測失敗時記錄警告並以 `name_en` 退回。
- 檔名一律使用英文小寫加底線。

**3.6.2 繪圖共同規範**

- **指標一律以完整加權圖計算；backbone 抽取（disparity filter，α=0.05）只用於繪圖。**
- 統一 layout（`spring_layout`，`seed=42`）與統一配色，讓 18 個單位的圖可以並排比較。
- 節點大小對應中心性，邊寬對應權重；節點數 > 80 時只標註 top-15 標籤。
- 圖檔尺寸上限 20×16 吋、`dpi=180`，不沿用範例的 `figsize=(90,80)`。
- 每張圖同時輸出 PNG（報告用）與 GraphML（Gephi 互動探索用）。
- 每張網路圖的 caption 需註明：節點數、邊數、是否套用 backbone、λ 值。

**3.6.3 每個分析單位的圖表清單**

存於 `analysis/network-analysis/<unit>/figures/`：

| 檔名 | 類型 | 內容 |
| --- | --- | --- |
| `01_bipartite_network.png` | 網路圖 | Professor–Keyword 二分網路，兩色區分節點類型 |
| `02_largest_component.png` | 網路圖 | LCC，標註涵蓋比例 |
| `03_keyword_network_degree.png` | 網路圖 | Keyword 網路，節點大小 = degree centrality |
| `04_keyword_network_betweenness.png` | 網路圖 | Keyword 網路，節點大小 = betweenness centrality |
| `05_keyword_network_communities.png` | 網路圖 | Keyword 網路，顏色 = Louvain 社群 |
| `06_keyword_network_by_taxonomy.png` | 網路圖 | Keyword 網路，顏色 = `parent_l1`；與 05 並看即可目視社群是否對齊 taxonomy |
| `07_professor_network_degree.png` | 網路圖 | Professor 網路，節點大小 = degree |
| `08_professor_network_betweenness.png` | 網路圖 | Professor 網路，節點大小 = betweenness |
| `09_professor_network_communities.png` | 網路圖 | Professor 網路，顏色 = Louvain 社群 |
| `10_top_keywords_bar.png` | 長條圖 | 該單位 top-20 研究領域人數 |
| `11_degree_distribution.png` | 分布圖 | Professor 與 Keyword 的 degree 分布（含 log-log 版） |
| `12_centrality_scatter.png` | 散布圖 | degree vs betweenness，附 Pearson r 與 p-value |
| `13_keyword_cooccurrence_heatmap.png` | 熱力圖 | Top-25 研究領域的共現矩陣 |
| `14_community_composition.png` | 堆疊長條 | 各 Louvain 社群的 `parent_l1` 組成 |
| `15_null_model_comparison.png` | 分布圖 | 觀測值 vs 1,000 次虛無模型分布，標出 z-score |
| `16_lambda_sensitivity.png` | 折線圖 | λ ∈ {0, 0.3, 0.4, 0.5} 對 density / modularity / LCC 佔比的影響 |
| `17_taxonomy_sunburst.png` | 階層圖 | 該單位研究領域的 L1 → L2 → L3 分布 |

組層級單位另加：

| 檔名 | 類型 | 內容 |
| --- | --- | --- |
| `18_professor_network_by_school.png` | 網路圖 | Professor 網路，顏色 = `school_id`，直接看出跨校混合程度 |
| `19_cross_school_edges.png` | 熱力圖 | 校 × 校的連結強度矩陣 |
| `20_joint_appointment_highlight.png` | 網路圖 | 標出合聘教授（`n_appointments > 1`）的位置 |

### Stage 4 — `4_group_and_cross_comparison.ipynb`

**4.1 跨校橋接分析（組層級專屬）**
- professor 節點帶 `school_ids` 屬性。
- 跨校邊佔比、**E-I index**、依 `school_id` 的 assortativity。
- 跨校 betweenness 排名 → 各組的跨校 broker 教授清單。
- **Louvain 社群 vs `school_id` 分割的 NMI / ARI** → 回答「社群結構由學校決定或由研究主題決定」。
- 合聘教授（`n_appointments > 1`）單獨列出，因其必然為跨校節點，須避免與「研究主題造成的跨校連結」混淆。

**4.2 組間與系所間比較**
- 統一比較表：density、mean degree、LCC 佔比、modularity Q、社群數、平均 clustering coefficient、領域集中度（entropy 與 Gini）、跨校邊比例、coverage。
- 三組研究領域重疊分析：各組獨有領域、跨組共享領域。
- 所有比較圖表併列 coverage，避免把資料完整度誤讀為結構差異。

**4.3 跨單位視覺化**

存於 `analysis/network-analysis/comparison/figures/`，語言規則同 §3.6.1：

| 檔名 | 類型 | 內容 |
| --- | --- | --- |
| `01_metrics_by_school.png` | 分組長條圖 | 14 系所的 density / mean degree / modularity 並列，附 coverage 副軸 |
| `02_metrics_by_group.png` | 分組長條圖 | 3 組的同一組指標 |
| `03_small_multiples_keyword_networks.png` | 小倍數網格 | 14 系所的 keyword 網路縮圖，同 layout 同配色，一眼比較結構 |
| `04_small_multiples_professor_networks.png` | 小倍數網格 | 14 系所的 professor 網路縮圖 |
| `05_school_keyword_heatmap.png` | 熱力圖 | 校系 × Top-40 研究領域，值為人數比例，附階層式聚類樹 |
| `06_school_similarity_dendrogram.png` | 樹狀圖 | 以研究領域向量的餘弦相似度做階層分群，檢驗資料驅動的分群是否重現 cs / ds / fin-and-econ |
| `07_group_field_overlap.png` | 韋恩／UpSet 圖 | 三組研究領域的獨有與共享情形 |
| `08_cross_school_bridging.png` | 分組長條圖 | 三組的 E-I index、跨校邊比例、school assortativity |
| `09_community_vs_school_alignment.png` | 長條圖 | 三組的 NMI / ARI（Louvain 社群 vs school 分割） |
| `10_taxonomy_alignment.png` | 長條圖 | 18 個單位的社群 vs `parent_l1` 對齊度 |
| `11_coverage_vs_density.png` | 散布圖 | coverage 對 density 的關係，用來檢查結構差異是否只是資料完整度造成 |
| `12_top_brokers.png` | 水平長條圖 | 各組跨校 betweenness 前 15 名教授（此圖的教授姓名為中文） |

第 6 與第 11 張是驗證性圖表：前者檢驗人為分組是否有資料支持，後者檢驗結論是否被資料完整度污染。

**4.4 綜合報告**
- 產生 `docs/network-analysis-report.md`，格式對齊既有三份報告，內嵌上述圖檔的相對路徑連結。

## 4. 輸出檔案

### 程式
```
scripts/network-analysis/current-version/
  1_build_taxonomy.ipynb
  2_build_network_data.ipynb
  3_network_analysis.ipynb
  4_group_and_cross_comparison.ipynb
```

### 資料 `data/network-analysis/`
```
research_taxonomy.csv          # 170 個領域的三層階層（固定資產）
keyword_idf.csv                # 全體 IDF 權重
person_identity_map.csv        # 跨校去重對照與待覆核清單
by-school/<school_id>/         # 14 個
  professor_nodes.csv
  keyword_nodes.csv
  prof_keyword_edges.csv
by-group/<group>/              # 3 個（去重後）
  professor_nodes.csv
  keyword_nodes.csv
  prof_keyword_edges.csv
  professor_nodes_nodedup.csv  # robustness check 用
overall/                       # 1 個（去重後）
  professor_nodes.csv
  keyword_nodes.csv
  prof_keyword_edges.csv
```

### 分析 `analysis/network-analysis/`
**所有 PNG 圖檔一律存於此樹下，不存到 `data/`。**

```
<school_id>/                   # 14 個目錄（已存在，目前為空）
  prof_keyword_network.graphml
  keyword_network.graphml
  professor_network.graphml
  keyword_centrality.csv
  professor_centrality.csv
  keyword_communities.csv
  professor_communities.csv
  network_metrics.json         # 含排除人數與 coverage
  null_model_test.csv
  lambda_sensitivity.csv
  figures/                     # §3.6.3 的 01~17 共 17 張
    01_bipartite_network.png
    ...
    17_taxonomy_sunburst.png
<group>/                       # 3 個目錄，內容同上，另加
  cross_school_bridging.csv
  figures/                     # 01~17 再加組層級專屬的 18~20
    18_professor_network_by_school.png
    19_cross_school_edges.png
    20_joint_appointment_highlight.png
overall/                       # 內容同組層級
comparison/                    # 已存在
  school_metrics_comparison.csv
  group_metrics_comparison.csv
  cross_school_bridging_summary.csv
  taxonomy_alignment.csv
  lambda_sensitivity_summary.csv
  figures/                     # §4.3 的 01~12 共 12 張
    01_metrics_by_school.png
    ...
    12_top_brokers.png
```

圖檔總量約 **14×17 + 4×20 + 12 = 330 張**。

### 報告 `docs/`
```
network-analysis-report.md
```

## 5. 相對於原範例的改善

| # | 原範例做法 | 本計畫做法 | 理由 |
| --- | --- | --- | --- |
| 1 | `pinyin` + `googletrans` 即時翻譯 | 完全移除 | 預處理已完成確定性標準化；即時翻譯不可重現、需連網、會被限流 |
| 2 | Excel 進出 | CSV + GraphML | GraphML 可直接進 Gephi |
| 3 | `bipartite.projected_graph`（無權重） | 加權投影 + IDF + λ | 無權重投影在 152 人的 `nycu-cs` 近乎完全圖，看不出結構 |
| 4 | Girvan–Newman，手動指定 n=3 | Louvain 為主，回報 modularity Q；GN 僅小圖對照 | GN 為 O(m²n)；社群數不應手動猜測 |
| 5 | 僅 degree / betweenness | 加 eigenvector、PageRank、strength、clustering、assortativity 與網路層級指標 | 跨單位比較需要正規化的網路層級指標 |
| 6 | 無虛無模型 | degree-preserving 二分虛無模型 × 1,000 | 才能主張結構超出隨機 |
| 7 | `figsize=(90,80)`、`font_size=1000`、全部標籤 | backbone + top-15 標籤 + 固定 seed + 上限 20×16 吋 | 原圖實務上無法開啟與閱讀 |
| 8 | 硬寫 `C:\Windows\Fonts\msjh.ttc` | 字型偵測與 fallback | 可攜性 |
| 9 | 未處理缺漏 | 每單位明列 coverage 與排除人數 | 覆蓋率 67.9%~100%，直接比原始數量會得出錯誤結論 |
| 10 | 結果散在 notebook 輸出 | 標準化 `metrics` / `nodes` / `edges` CSV | 才能做 18 個單位的橫向比較 |
| 11 | 未處理合聘重複 | 組層級 `person_id` 去重、領域取聯集 | 38 位跨校重複教授會憑空製造跨校橋接 |
| 12 | 只有網路圖，且圖檔散落 | 每單位 17~20 張、comparison 12 張的完整圖表清單，統一存於 `analysis/network-analysis/` | 網路圖之外還需要分布圖、熱力圖、虛無模型對照、λ 敏感度等診斷圖，否則結論無從檢驗 |
| 13 | 圖中混用中英文 | 除教授姓名外一律英文，並以程式掃描驗證 | 圖表需可直接放入英文報告與投影片 |

## 6. 驗證檢查清單

執行完成後必須逐項通過：

- [ ] 170 個 canonical 領域全數對應到 L2 與 L1，無孤兒。
- [ ] 每個 L1 至少包含 2 個 L2；無任一 L1 在全體覆蓋率超過 50%。
- [ ] 各系所節點數與 §1 覆蓋率表一致（例：`nccu-fin` 23 人、`nycu-cs` 141 人）。
- [ ] 組層級去重後人數 = 原紀錄數 − 組內重複人數（`ds` 134−10=124、`cs` 413−6=407、`fin-and-econ` 177−1=176，以實際 email 比對結果為準）。
- [ ] 邊表中所有 keyword 存在於 `research_taxonomy.csv`。
- [ ] λ=0 的結果與純 IDF 加權投影一致。
- [ ] 所有比較表含 coverage 欄位。
- [ ] 每個單位的 `network_metrics.json` 記錄排除人數。
- [ ] GraphML 可被 networkx 重新讀入且節點數相符。
- [ ] `person_identity_map.csv` 中的 `name_collision_kept_separate` 項目已列於報告限制章節。
- [ ] 所有 PNG 圖檔位於 `analysis/network-analysis/` 之下，`data/` 內無任何圖檔。
- [ ] 每個系所單位有 17 張圖、每個組層級與全體單位有 20 張圖、comparison 有 12 張圖，無缺漏。
- [ ] **語言檢查**：逐張確認圖中除教授姓名外無中文字元（以程式掃描每張圖的文字元素清單，非目視）。
- [ ] 無中文名的教授在圖中以 `name_en` 顯示，且已記錄於 `network_metrics.json`。
- [ ] 中文字型偵測成功；若失敗，警告已記錄且教授標籤已退回英文。
- [ ] 所有網路圖 caption 皆註明節點數、邊數、是否套用 backbone、λ 值。

## 7. 限制與注意事項

- 研究領域來自各校官網自填內容，深度與粒度本就不一致。網路密度差異可能反映資料填寫習慣，而非真實研究結構差異。
- `ntu-cs-ie` 與 `ntu-ds` 的學歷欄位為空，因此 PhD institution 相關屬性在這兩系所缺席；相關分析須排除或標註。
- Taxonomy 的 L1/L2 劃分為研究者判斷，不同劃分會影響 λ 項與社群對齊檢驗。`research_taxonomy.csv` 版本控管以確保可稽核與可重現。
- λ 引入的推論連結是研究設計選擇，不是資料本身。所有主要結論須同時檢視 λ=0 的 baseline。
- 覆蓋率不可解讀為系所或教授的品質排名。

## 8. 執行方式

環境已具備所需套件（`networkx 3.6.1` 內建 `louvain_communities`，另有 `pandas 2.2.3`、`numpy 2.3.0`、`scipy 1.16.1`、`matplotlib 3.10.7`、`scikit-learn 1.7.1`），**無須額外安裝**。`pyvis` 未安裝，互動式 HTML 圖列為選配。

```powershell
python -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 scripts/network-analysis/current-version/1_build_taxonomy.ipynb
python -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 scripts/network-analysis/current-version/2_build_network_data.ipynb
python -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 scripts/network-analysis/current-version/3_network_analysis.ipynb
python -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=1800 scripts/network-analysis/current-version/4_group_and_cross_comparison.ipynb
```

Stage 3 的虛無模型檢定（18 單位 × 1,000 次隨機化）為主要耗時來源，逾時設定較長。
