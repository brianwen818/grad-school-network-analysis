> **關於這兩本 notebook**：`1. HKUST_FM.ipynb` 與 `2. HKUST_FM.ipynb` 是第三方的參考範例，
> 不是本專案的作品，也沒有附帶授權，因此**不隨本專案發布**。下面是它們的概念整理，
> 本專案實際使用的實作在 [`../current-version/`](../current-version/)。

---

這兩個 notebook 是前後相接的。可以把它理解成：

Notebook 1：整理資料 --> Notebook 2：做網路分析
### 1. `1. HKUST_FM.ipynb`
主要是在做 **資料前處理 + 建立網路分析需要的資料表**。

它做了：

- 讀入 HKUST Finance / FM 的教授資料。
- 使用 `pinyin` 處理中文文字。
- 使用 Google Translate 做中英文翻譯。
- 整理出「教授－研究關鍵字」的對應關係。
- 建立三份資料：
  - Professor Nodelist：教授節點表
  - Keyword Nodelist：研究關鍵字節點表
  - Professor–Keyword Edgelist：教授與關鍵字之間的連線
- 最後輸出成 Excel。

核心概念就是：

```text
教授 A ── Financial Data Analysis
       └─ Asset Pricing

教授 B ── Asset Pricing
       └─ Machine Learning
```

所以 Notebook 1 本身**沒有做很複雜的分析**，主要是在把原始資料整理成「Network Analysis 可以使用的格式」。

---

### 2. `2. HKUST_FM.ipynb`
這份才是真正進行 **Social Network Analysis / Network Analysis（網路分析）**。

首先讀入 Notebook 1 產生的三份 Excel，建立一個：

\[
\boxed{\text{Professor} \leftrightarrow \text{Keyword}}
\]

的 **二分網路（Bipartite Network）**。

例如：

```text
Professor A ───── Asset Pricing
      │
      └────────── Machine Learning

Professor B ───── Asset Pricing
```

然後主要做四件事：

1. **建立並畫出 Professor–Keyword network**
   - 教授是一類節點
   - Keyword 是另一類節點
   - 教授研究某個 keyword，就連一條線。

2. **找 Largest Connected Component**
   - 找出整個網路中最大的連通群。
   - 也就是彼此可以透過教授/關鍵字間接連起來的最大群體。

3. **建立 Keyword–Keyword Network**
   
   如果兩個 keywords 被同一位教授研究，就讓它們產生連結：

   ```text
   Professor A
      ↓
   Asset Pricing
   Machine Learning

   ↓ 投影

   Asset Pricing ─── Machine Learning
   ```

   然後分析：
   - **Degree Centrality**：哪些研究主題跟最多其他主題有關。
   - **Betweenness Centrality**：哪些研究主題扮演不同領域之間的橋樑。
   - **Girvan–Newman Community Detection**：把研究主題分成幾個研究群組。

4. **建立 Professor–Professor Network**
   
   如果兩位教授研究相同 keyword，就把教授連起來：

   ```text
   Professor A ── Asset Pricing ── Professor B

   ↓ 投影

   Professor A ───────── Professor B
   ```

   同樣分析：
   - Degree Centrality
   - Betweenness Centrality
   - Community Detection

---

## 最簡單的總結

這兩份 Notebook 合起來是在研究：

> **HKUST FM 的教授研究哪些主題，以及教授和研究領域之間形成什麼樣的網路結構。**

整體流程就是：

```text
原始教授資料
        ↓
Notebook 1
資料清理 / 翻譯
        ↓
Professor
Keyword
Professor-Keyword 關係
        ↓
Notebook 2
建立 Professor-Keyword Network
        ↓
    ┌───────────────┐
    ↓               ↓
Keyword Network   Professor Network
    ↓               ↓
中心性分析         中心性分析
社群分析           社群分析
```

所以一句話區分：

**Notebook 1 = 把資料整理成網路。**

**Notebook 2 = 分析這個網路，找重要教授、重要研究主題，以及研究群體。**