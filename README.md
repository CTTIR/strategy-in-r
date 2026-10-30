# Strategy in R

**Game Theory, Simulation, and Machine Intelligence — A Quarto Book**

*Strategy in R* is an open-source book covering game theory, computational simulation, AI/ML for strategic interaction, and ethics — implemented end-to-end in R.

**Read online:** [r-heller.github.io/strategy-in-r](https://r-heller.github.io/strategy-in-r/)

## Build

The current local HTML and EPUB checks used R 4.6.1 and Quarto 1.10.19.
The historical `renv.lock` is preserved; a complete restore of that snapshot has
not been qualified on this Mac. To use an existing R library explicitly:

```sh
Rscript --vanilla -e 'install.packages(c("knitr", "rmarkdown", "tidyverse", "here", "glue", "gt", "scales", "patchwork", "igraph", "deSolve", "lpSolve", "reticulate", "Rcpp", "downlit", "xml2", "gtools", "MASS", "nnet"), repos="https://cloud.r-project.org")'
python3 scripts/check-source-refs.py
RENV_CONFIG_AUTOLOADER_ENABLED=false Rscript tests/test-mcts.R
RENV_CONFIG_AUTOLOADER_ENABLED=false quarto render --to html
python3 scripts/check-html-links.py _book html-links.json
RENV_CONFIG_AUTOLOADER_ENABLED=false quarto render --to epub --no-clean
python3 -m http.server 8000 --directory _book
```

Open `http://localhost:8000`. `--no-clean` preserves the HTML when adding EPUB;
otherwise a later format render cleans the output directory. For the frozen
environment route, run `renv::restore()` first and leave the autoloader enabled.
PDF needs a TeX installation and is not locally verified. Hosted CI and deployment
are separate from these local checks.

The Monte Carlo tree search example is a small teaching algorithm, not an
AlphaZero neural-network implementation. Quantitative simulation outcomes are
seed- and budget-specific. Optional external Python integrations and full
scientific correctness of every chapter remain separate validation work.
See [MAINTENANCE.md](MAINTENANCE.md) for findings, evidence and deferred work.

## Structure

| Part | Topic |
|------|-------|
| I | Foundations of Game Theory |
| II | The R Toolkit |
| III | Simulation |
| IV | AI and Machine Learning |
| V | Applications |
| VI | Ethics and the Future |

## License

- **Code:** [MIT](LICENSE)
- **Content:** [CC-BY-SA 4.0](LICENSE-CONTENT)

## Citation

```bibtex
@book{heller2026strategy,
  author    = {Heller, Raban},
  title     = {Strategy in R: Game Theory, Simulation, and Machine Intelligence},
  year      = {2026},
  url       = {https://r-heller.github.io/strategy-in-r/},
  note      = {Quarto book, DOI forthcoming via Zenodo}
}
```

## Author

Raban Heller ([ORCID: 0000-0001-8006-9742](https://orcid.org/0000-0001-8006-9742))
