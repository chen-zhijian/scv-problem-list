# Problem statistics

Generated from [the LaTeX source](papers/src/scv-problem-list.tex) by [`scripts/count_problems.py`](scripts/count_problems.py).

## Counting convention

Each independently numbered `problem` environment counts as one problem. Subquestions within one environment are not split. Multiple source labels attached to one problem do not increase the count. References in remarks and TeX comments are excluded. Explicit problem-counter assignments preserve the identifiers of entries moved between categories.

Status categories follow the manuscript: closed problems have been resolved affirmatively or negatively; partial-results problems have substantial known cases or weaker results; wide-open problems have a central question that remains largely unresolved. The statistics describe the manuscript's classification and do not independently reassess the literature.

## By resolution status

| Status | Count | Share |
| --- | ---: | ---: |
| Closed | 36 | 25.90% |
| Partial results | 52 | 37.41% |
| Wide-open | 51 | 36.69% |
| **Total** | **139** | **100%** |

The two unresolved categories together contain **103** problems.

## By subject and status

| Section | Subject | Closed | Partial results | Wide-open | Total |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | Stein geometry and holomorphic embeddings | 6 | 9 | 6 | 21 |
| 2 | L² theory and CR geometry | 9 | 12 | 11 | 32 |
| 3 | Function theory and pluripotential theory | 3 | 8 | 13 | 24 |
| 4 | Holomorphic mappings and hyperbolicity | 1 | 6 | 4 | 11 |
| 5 | Complex dynamics and foliations | 9 | 11 | 14 | 34 |
| 6 | Complex geometry and algebraic cycles | 5 | 4 | 1 | 10 |
| 7 | Period maps and arithmetic geometry | 3 | 2 | 2 | 7 |
| **Total** | | **36** | **52** | **51** | **139** |

## Problem-number ranges

| Section | Closed | Partial results | Wide-open |
| --- | --- | --- | --- |
| 1 | 1.1–1.6 | 1.7–1.15 | 1.16–1.21 |
| 2 | 2.1–2.9 | 2.10–2.21 | 2.22–2.32 |
| 3 | 3.1–3.3 | 3.4–3.11 | 3.12–3.24 |
| 4 | 4.1 | 4.2–4.7 | 4.8–4.11 |
| 5 | 5.1–5.9 | 5.10–5.20 | 5.21–5.34 |
| 6 | 6.1–6.5 | 6.6–6.9 | 6.10 |
| 7 | 7.1–7.3 | 7.4–7.5 | 7.6–7.7 |

## Refresh or verify

From the repository root:

```sh
python scripts/count_problems.py
python scripts/count_problems.py --check
```

The first command refreshes this file, `data/problem-counts.json`, and the marked statistics block in `README.md`. The second checks them without writing. No TeX installation is required for either command.
