# Some problems in complex variables

**Zhijian Chen** · Survey and problem collection  
**Updated manuscript:** 25 October 2026 · 37 pages

[Read the survey](papers/scv-problem-list.pdf) · [LaTeX source](papers/src/scv-problem-list.tex) · [Problem statistics](statistics.md) · [Personal website](https://chen-zhijian.github.io/)

## Overview

This survey collects problems in several complex variables and complex geometry, organizes them by subject and degree of resolution, and brings together overlapping formulations from the literature. Established results are accompanied by proof sketches; partial results specify their hypotheses; remarks are attributed to their sources.

The principal starting points, as recorded in the manuscript's bibliography, are the problem lists of Buzzard, Fornæss, Gavosto, and Krantz (1995) and Fornæss and Sibony (2001), Zhou's survey (2019), and Siu's Tianyuan conference report (2025). The manuscript contains the full references and the precise formulations to which its classifications apply.

## Problems at a glance

<!-- problem-counts:start -->

**139 numbered problems across 7 subject areas:** 36 closed, 52 with partial results, and 51 wide-open.

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

<!-- problem-counts:end -->

Each independently numbered **Problem** is counted once. Several subquestions within one numbered entry remain one entry; multiple source labels attached to a consolidated problem do not increase the count. The classifications follow the current manuscript:

- **Closed:** completely resolved, with either an affirmative or a negative answer.
- **Partial results:** significant special cases or weaker forms are known, while the full formulation remains open.
- **Wide-open:** the central question remains largely unresolved, although related results or proposed approaches may exist.

See [the detailed statistics](statistics.md) for the subject-by-status table and numbering ranges. [Machine-readable counts](data/problem-counts.json) are generated from the LaTeX source.

## Substantive updates — 25 October 2026

Compared with the former manuscript, all **139 problem statements are retained**. Answers and remarks are updated for seven entries:

- **1.14 — Oka–Grauert principle:** adds An–Du–Guo–Wang–Xie’s results on rationally connected projective manifolds and hypersurface complements, with credit to OpenAI’s K3 work. The broader problem remains partially resolved.
- **4.8 — Jacobian conjecture:** adds Tao’s account and formal verification of the Claude-assisted counterexample in $\mathbb C^3$. The survey’s question in $\mathbb C^2$ remains open.
- **6.1 — Kodaira embedding:** adds Du–Xie, OpenAI, and Liu–Wan counterexamples to distinct vector-bundle positivity claims, explaining why they do not settle Hartshorne splitting.
- **6.3 — Invariance of plurigenera:** adds Kähler and logarithmic extensions by Li–Păun–Wang–Zhou and Liu–Wan, with the stated hypotheses and Liu–Wan’s AI-use disclosure.
- **6.5 (formerly 6.7) — Complex structure on $S^6$:** moves from partial results to closed in the survey, with a proof outline, credit to Claude, Alpöge, and Engel, and Viaclovsky’s non-biholomorphic families demonstrating nonuniqueness.
- **6.8 — Analytic uniruledness and canonical fibrations:** adds Ou’s compact Kähler criterion, Du–Guo–Xie’s analytic Fano result, and the combined OpenAI Iitaka/abundance claim. The companion Iitaka theorem supplies the abundance paper’s assumption; independent specialist verification of those AI-generated proofs was not located in the sources checked. The full problem remains partially resolved.
- **6.9 — Hodge conjecture:** moves from wide-open to partial results, adding the reported CM-abelian case, van Hoften–Sempliner’s variant proof, Milne’s assessment, and AI attribution. The general conjecture remains open.

The classifications change from **35 closed / 52 with partial results / 52 wide-open** to **36 / 52 / 51**, with **139 problems across 7 subjects** throughout. The current section-by-section counts appear above. The $S^6$ move also renumbers Hartshorne’s problem from 6.5 to 6.6 and Hermitian-symmetric-space rigidity from 6.6 to 6.7, without changing their content.

The bibliography grows from **137 to 155 entries**. Original papers, precise hypotheses, mathematicians’ remarks, and disclosed AI contributions are documented in the [manuscript](papers/scv-problem-list.pdf); recent preprint claims are identified as such.

## Files

| Path | Contents |
| --- | --- |
| `papers/scv-problem-list.pdf` | Current PDF; the stable manuscript link used by the homepage |
| `papers/src/scv-problem-list.tex` | Self-contained LaTeX source, including the bibliography |
| `statistics.md` | Problem counts by subject, resolution status, and numbering range |
| `data/problem-counts.json` | Machine-readable problem counts |
| `data/initial-import.json` | Hashes and original filenames for the initial author-supplied files |
| `scripts/count_problems.py` | Regenerate or check the problem statistics |
| `scripts/build.py` | Rebuild the PDF with an existing local LaTeX installation |
| `.github/workflows/validate.yml` | Lightweight validation of the recorded statistics |

The initial import preserved the supplied source and PDF byte for byte. Their filenames were normalized for stable links. The initial PDF's title, author, seven sections, and all 139 problem numbers were checked against the source.

## Update the manuscript

Edit `papers/src/scv-problem-list.tex`, then run the following commands from the repository root with Python 3 and a TeX installation providing `latexmk` and pdfLaTeX:

```bash
python scripts/build.py
python scripts/count_problems.py --check
```

The build uses `latexmk` to complete the necessary LaTeX passes, keeps auxiliary files under `build/`, and updates the published PDF only after compilation succeeds. The source uses `\date{\today}`, so a rebuilt PDF displays its build date. Review the rebuilt PDF before committing the source, PDF, and regenerated statistics together.

To refresh the statistics without rebuilding the manuscript:

```bash
python scripts/count_problems.py
```

The GitHub validation workflow checks the statistics with Python. It does not install a TeX distribution or rebuild the PDF; PDF compilation remains a separate local step.

## Homepage link

The [personal homepage](https://chen-zhijian.github.io/) links to `papers/scv-problem-list.pdf` in this repository. Keep that path stable when updating the paper. The homepage's main survey link reaches this repository; its direct PDF link serves a synchronized copy from the website repository. Update that copy and its `papers/manifest.json` provenance when publishing a revised PDF.

If the title, author credit, problem counts, or summary changes, update the corresponding project entry in [`chen-zhijian.github.io`](https://github.com/chen-zhijian/chen-zhijian.github.io) as well.
