# Maintenance record — 30 October 2026

## Purpose, strategy and acceptance

This is an executable teaching book on game theory, simulation and machine
learning in R. The current milestone prioritizes runnable examples, defensible
worked explanations, complete citations and usable HTML/EPUB navigation. It does
not add a neural training framework or claim independent validation of every
scientific statement. Original figures and the historical environment lock are
preserved; newly rendered figure exports go to `_generated/figures/`.

Milestones: (1) repair the confirmed MCTS failure and protect actual chapter code;
(2) render every configured chapter with errors fatal; (3) repair citation/section
references, check links and exercise reading; (4) document installation and
format limits. All four local milestones passed. PDF, optional external Python
integrations, full historical lock restoration and hosted deployment remain
separate work, rather than being represented as tested.

## Material findings and implemented changes

- High — `part-4-ai-ml/27-self-play-alphazero.qmd`: list-valued tree nodes were
  copied, so visits did not propagate to the root and complete games could fail
  to advance. Use explicitly shared environment nodes; handle singleton action
  sampling, terminal positions and invalid budgets/moves. Regression tests load
  the functions actually printed in the chapter, check 300 root visits, tactical
  choices and 20 complete games of at most nine plies.
- High — the worked winning move and accompanying quantitative claims disagreed
  with the implementation. Correct the position/labels, remove unsupported
  universal win-rate assertions, distinguish pure MCTS from neural AlphaZero and
  cite the actual 2017 AlphaZero paper (https://arxiv.org/abs/1712.01815).
- Medium — missing bibliography keys and seven unresolved section references
  produced incomplete navigation and attribution. Add verified primary-source
  entries, fix section anchors, remove references to absent cover/favicon files,
  and add source and rendered-link gates to CI.
- Medium — chapter figure generation wrote over tracked illustrations. Direct
  new export files to a separate ignored directory and retain historical images.
- Medium — independent format renders clean Quarto's output directory by default.
  Document `--no-clean` when adding a second format; verify both coexist.

## Observed verification

R 4.6.1, Quarto 1.10.19, macOS ARM64:

- All 48 configured inputs rendered to HTML with execution errors fatal. Final
  distribution render completed in 509.55 seconds.
- EPUB render passed in 233.13 seconds; ZIP CRC, required EPUB mimetype, 127 members and 50 XHTML
  resources verified. HTML and EPUB coexist in `_book/`.
- Source gate: 48 inputs, 88 labels, 67 bibliography entries; no unresolved local
  section/citation keys. Rendered gate: 20,213 local references across 48 pages,
  zero broken targets/anchors.
- MCTS regression script passed. Chromium navigation to the self-play chapter,
  chapter content, unresolved-reference absence and 390-pixel reading passed;
  desktop/mobile screenshots retained and inspected.
- Visual inspection then revealed that duplicate YAML/body titles also advanced
  the chapter counter twice. Removed the redundant YAML title while preserving
  its full wording and the explicit chapter anchor in the H1, across chapters
  and the template. Both formats passed full renders after this finding; browser checks confirm one
  chapter H1 with the full title and working navigation on mobile.


Exact commands, logs, primary-source bibliography notes and artifacts are in the
local portfolio evidence directory's `strategy-in-r/` subdirectory. No remote CI,
PDF, deployment or external scientific acceptance is claimed.

## First use and next release action

Follow the exact dependency/install/render/serve commands in README.md. Quarto,
R, Python 3 and a C++ toolchain for Rcpp are required. Read `_book/index.html`
through the documented local HTTP server, or use `_book/Strategy-in-R.epub`.

Before publishing, review the changed examples and bibliography, run the prepared
CI on the chosen commit, and decide whether to qualify PDF with TeX. Longer-term
work should focus on independent scientific review and optional backend examples,
not more chapters without executable evidence.
