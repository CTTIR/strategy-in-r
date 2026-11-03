# Exercise the actual teaching implementation, not a separately copied engine.
suppressPackageStartupMessages({library(tibble); library(dplyr)})
args <- commandArgs(trailingOnly = TRUE)
x <- readLines(if (length(args)) args[[1L]] else '27-self-play-alphazero.Rmd')
chunks <- c('ttt-engine', 'mcts-core', 'mcts-run-function')
for (label in chunks) {
  starts <- grep(paste0('^```\\{r,? *', label, '[,}]'), x)
  stopifnot(length(starts) == 1L)
  first <- starts + 1L
  last <- first + which(x[first:length(x)] == '```')[1L] - 2L
  eval(parse(text=x[first:last]))
}
set.seed(42)
r <- mcts_search(ttt_new(), 300)
stopifnot(r$root$visits == 300L, sum(r$stats$visits) == 300L,
          length(r$root$children) == 9L, r$best_move %in% 1:9,
          any(vapply(r$root$children, function(n) length(n$children) > 0L, logical(1))))
# The singleton is square 9: sample(9, 1) would incorrectly sample 1:9.
last <- c(1L,-1L,1L,1L,-1L,-1L,-1L,1L,0L)
for (seed in 1:30) {
  set.seed(seed)
  stopifnot(mcts_rollout(last) == 0L, mcts_search(last, 10)$best_move == 9L)
}
# Tactical verification is independent of the search estimates.
win <- c(1L,1L,0L,-1L,-1L,0L,0L,0L,0L)
set.seed(42)
stopifnot(mcts_search(win, 1000)$best_move == 3L)
# Complete games must add exactly one mark each ply and end within nine plies.
for (seed in 1:20) {
  set.seed(seed); b <- ttt_new(); ply <- 0L
  while (is.na(ttt_winner(b))) {
    moves <- ttt_moves(b); player <- ttt_current_player(b)
    move <- if (player == 1L) mcts_search(b, 25)$best_move else moves[sample.int(length(moves),1)]
    b <- ttt_play(b, move, player); ply <- ply + 1L
    stopifnot(sum(b != 0) == ply, ply <= 9L)
  }
  stopifnot(ttt_winner(b) %in% -1:1)
}
for (n in list(0, NA_real_, Inf, 1.5, .Machine$integer.max+1))
  stopifnot(inherits(try(mcts_search(ttt_new(), n), silent=TRUE), 'try-error'))
stopifnot(inherits(try(ttt_play(ttt_new(), integer(), 1L), silent=TRUE),'try-error'),
          inherits(try(mcts_search(rep(1L,9)), silent=TRUE),'try-error'))
cat('Root/child mutation, singleton moves, tactical win, 20 complete games and invalid inputs passed\n')
# The plotted evaluation must execute actual games, rather than use an invented
# rate table. Count starts independently of the chapter's reported outcomes.
starts <- grep('^```\\{r,? *self-play-simulation[,}]', x)
stopifnot(length(starts) == 1L)
first <- starts + 1L
last <- first + which(x[first:length(x)] == '```')[1L] - 2L
original_new <- ttt_new
game_starts <- 0L
ttt_new <- function() {
  game_starts <<- game_starts + 1L
  original_new()
}
eval(parse(text = x[first:last]))
ttt_new <- original_new
stopifnot(game_starts == n_games * length(iteration_levels),
          identical(self_play_results$iterations, iteration_levels),
          all(is.finite(self_play_results$win_rate)),
          all(self_play_results$win_rate >= 0),
          all(self_play_results$draw_rate >= 0),
          all(self_play_results$win_rate + self_play_results$draw_rate <= 1))
cat('Actual plotted evaluation ran', game_starts, 'seeded games\n')
print(self_play_results)
