# Bookdown maintenance integration — 3 November 2026

The integration preserves the newer upstream Bookdown migration, root Rmd
chapters, Part layout, bs4_book styling, cover and native render workflow. It
adapts the earlier audited repairs from `a8b5e4cf`; obsolete Quarto workflows,
configuration and directory layout are not restored. Historical audit evidence
remains in MAINTENANCE.md and does not stand in for current-format validation.

The upstream Rmd MCTS implementation still failed the actual-source regression:
root visits did not accumulate. The repaired code uses shared nodes, handles
singleton choices and rejects invalid budgets/moves. The current Rmd regression
passes root/child accounting, the forced win, 20 complete bounded games and invalid
inputs. A separate counter confirms that the plotted evaluation runs all 300
seeded games; the upstream hardcoded rate table is replaced. Worked explanations distinguish pure search from AlphaZero training and
avoid unsupported finite-budget performance claims.

Existing upstream bibliography edits are retained; only the two missing audited
entries are added. Source checks now read all configured Bookdown inputs and
bibliographies, validate cross-references/citation keys, and distinguish linked
account handles from citations. New render checks preserve source figures and
stop on execution errors. The R environment chapter follows the current layout. The current-format render
also exposed duplicate Part/appendix markers inherited from the migration:
the dedicated Part inputs remain, and duplicate markers in their first chapters
are removed. An escaped GitHub handle avoids a spurious citation. These bounded
repairs preserve the intended navigation rather than replacing its layout.

The optional download footer resolves chapter filenames from the actual source
link and exposes only artifacts that respond successfully. A mobile-only display
math rule keeps wide equations inside the reading column. The four JavaScript
regressions fail against the old footer and pass against the repaired source.

The complete EPUB exposed raw HTML table/image markup that violated XML syntax.
An EPUB-only filter preserves the table markup and values while dropping empty
style attributes and converting raw images to native image nodes. Strict archive
checks reject invalid XML, duplicate IDs, missing files and missing anchors. A
real-Pandoc regression protects table values, identities and images and verifies
that ordinary HTML is unchanged. Full-book preservation checks compare the
resulting table/image counts and chapter text with the complete unfiltered build.
Bookdown preview output is not a release artifact: it can retain only headings in
chapters outside the selected input. Final artifacts use complete book renders.

Final local qualification used R 4.6.1, Bookdown 0.48, Pandoc 3.12.1 and Node
24.22.1. Complete HTML and EPUB renders finished successfully. All 57 HTML pages
passed 6,134 local file/anchor checks. All 60 EPUB XHTML documents parsed as XML;
9,971 internal XML references resolved, with no duplicate IDs or archive errors.
All 31 tables and 72 images were preserved from the complete unfiltered EPUB;
chapter text changed only in the deliberate cross-reference syntax explanation.
The final EPUB SHA-256 is
`85b9c43ceab7d5b46d1a651050692998f276400e1dec9baceb298935747054e5`.

Real Chromium journeys exercised home-to-chapter navigation, light/dark mode,
and 390-pixel mobile reading. The document width remains 390 pixels; the display
equation scrolls locally. A final mobile figure-width correction reconciles the
upstream full-viewport figure rule with this book's existing margins. Its final
HTML-only style include was copied into all 57 complete rendered heads, checking
that every page body remained unchanged. The available EPUB link downloads the exact hash-verified
archive; absent PDF formats are omitted. The settled search index returns MCTS results and its selection navigates to the
actual section. An immediate first-focus search returned no results in one run;
this inherited asynchronous-index limitation remains recorded separately.
Extracted EPUB front matter,
game tables and the computed MCTS figure were also visually inspected.

Source references passed across 63 configured inputs and 756 labels. The MCTS
regressions, four JavaScript download cases, real-Pandoc EPUB regression and
workflow lint passed. Baseline failures and rejected partial preview artifacts
are retained separately. The source figures and original checkout are unchanged.

The renders reported inherited PDF-device warnings for subscript glyphs in a
Nash-equilibrium export and Pandoc deprecation warnings. They are not presented
as warning-free builds. These checks qualify the observed local HTML/EPUB paths;
they are not EPUB-device certification or confirmation of hosted deployment.
PDF/per-chapter PDF, optional external backends, complete historical lockfile
restoration and live deployment remain separate from these local checks.
