# Faculty Research Networks in Taiwanese Graduate Programmes

[繁體中文版 / Chinese version →](README.md)

A social-network analysis of **741 faculty members across 14 graduate programmes
in Taiwan**, built from public departmental web pages and modelled as a
professor–research-field bipartite network.

> This is a personal student project. It is **not** an official publication of
> any university, and none of the metrics here should be read as a ranking of
> departments or of individual academics. Every e-mail address in the dataset
> has been irreversibly pseudonymised. See [LICENSE-data](LICENSE-data) for the
> full statement.
>
> Code [MIT](LICENSE) · Data and analysis [CC BY 4.0](LICENSE-data) · Collected 2026-09-09

---

## What the project asks

The 14 programmes fall into three groups:

| Group | Programmes |
| --- | --- |
| Computer science (`cs`) | NTU CSIE, NTU IM, NTHU CS, NYCU CS, NCKU CSIE |
| Data science (`ds`) | NTU Data Science, NTU GICE Data Science & Networking, NCKU Statistics |
| Finance and economics (`fin-and-econ`) | NTU Finance, NTU Economics, NCCU Finance, NCCU Money & Banking, NTHU Quantitative Finance, NYCU Information Management & Finance |

Four questions drive the analysis:

1. What does each department actually work on?
2. How do research topics cluster, and who sits at the centre of each cluster?
3. Do clusters form around **schools** or around **research topics**?
4. Is the three-way grouping above supported by the data?

## Headline findings

- **Topic beats institution.** Across every level of aggregation, Louvain
  communities align far better with research topic than with school
  (overall NMI 0.551 vs 0.329; school assortativity ≈ 0 — 0.003 for the `cs`
  group). Faculty are not meaningfully more connected to colleagues at their
  own institution.
- **CS and DS are not separable.** Hierarchical clustering on department ×
  research-field proportion vectors splits finance/economics off first, but all
  eight CS and DS programmes land in a single cluster. Only 13 of the 86 fields
  in the DS group are unique to it.
- **The field distribution is top-heavy.** Artificial Intelligence (109 faculty)
  and Machine Learning (94) dominate overall; Corporate Finance (34) and
  Econometrics (30) lead on the finance side.

Full results, one report per department plus a cross-department comparison:
[`analysis/final-summarized-reports/`](analysis/final-summarized-reports/markdown/).

## Method in brief

```
public faculty pages
   │
   ▼
[1] collection   scripts/data-collection/
   │   one collector.py per department describing that site's structure,
   │   shared logic in collector_core.py; Chinese and English pages are
   │   scraped separately and then paired into one bilingual record
   ▼
[2] preprocessing  scripts/data-preprocessing/
   │   normalise field names ("AI" / "人工智慧" -> Artificial Intelligence) and
   │   institution names; split degrees into degree / field / institution;
   │   anything ambiguous goes to a manual review queue
   ▼
[3] network analysis  scripts/network-analysis/current-version/
       1  a hand-built three-level taxonomy (170 fields -> 46 L2 -> 16 L1)
       2  node and edge tables, with joint appointments de-duplicated
       3  communities, centrality, null models and sensitivity analysis
          for 18 units (14 departments + 3 groups + overall)
       4  cross-school and cross-group comparison
```

The professor–field bipartite graph is projected onto each side. Professor-side
edge weight is `w = S_exp + λ·S_inf`, where `S_exp` is an IDF-weighted sum over
shared fields and `S_inf` a smaller inferred similarity from shared taxonomy
parents (λ = 0.4). Communities come from Louvain (seed 42). Structure is checked
against 1,000 degree-preserving rewirings, and the community structure is stable
across λ ∈ {0, 0.3, 0.4, 0.5}.

"Central" faculty means **position in the shared-field network** (degree,
betweenness). It says nothing about research quality or standing.

## Reproducing

```bash
# 1. collection
python -m pip install -r scripts/data-collection/requirements.txt
python scripts/data-collection/collect.py --school all

# 2. preprocessing and 3. analysis
python -m pip install -r requirements-analysis.txt
python -m jupyter nbconvert --to notebook --execute --inplace \
    scripts/data-preprocessing/1_faculty_data_preprocessing.ipynb
# ...then 2_, and the four notebooks under scripts/network-analysis/current-version/
# in order (notebook 3 is slow: --ExecutePreprocessor.timeout=3600)
```

Python 3.12. Figures label people in Chinese where a CJK font is available and
fall back to `name_en` otherwise.

## Repository layout

| Path | Contents |
| --- | --- |
| [`data/`](data/README.md) | Raw snapshots, standardised dataset, node and edge tables — **field-by-field data dictionary here** |
| `analysis/` | Every output: quality reports, descriptive statistics, network metrics, 474 figures |
| `analysis/final-summarized-reports/` | 14 department reports + 1 cross-department comparison, in Markdown ★ start here |
| [Releases](https://github.com/brianwen818/grad-school-network-analysis/releases/latest) | The same 15 reports as PDFs (~47 MB), kept out of the repository so clones stay small |
| `scripts/` | The crawler and six analysis notebooks |
| `docs/` | Stage-by-stage methodology reports |

## Limitations

- Research fields are self-declared on departmental pages; granularity varies by
  person, and network density partly reflects filling-in habits.
- Field coverage ranges from 67.9% to 100%. Two departments publish no education
  data at all, so that field is 0% for them.
- Departments are not de-duplicated against each other; jointly appointed faculty
  appear in more than one department report. De-duplication happens at the group
  and overall levels only.
- A snapshot of 2026-09-09. Sites change.

## Citation

See [CITATION.cff](CITATION.cff).
