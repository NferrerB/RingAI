from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Optional, Iterable

from aima3.games import Game
from Player import Jugador

State = Any
EvaluateFn = Callable[[State], float]
ChildrenFn = Callable[[State], Iterable[State]]
TerminalFn = Callable[[State], bool]


class IA(Jugador):
    """Clase IA que hereda de Jugador e implementa estrategia con alphabeta_search."""
    
    def __init__(self, nombre="IA"):
        super().__init__(nombre)


def alphabeta_cutoff_search(state: State, game: Game, d: int = 4, cutoff_test: Optional[Callable[[State, int], bool]] = None, eval_fn: Optional[EvaluateFn] = None) -> State:
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    player = game.to_move(state)

    def max_value(state: State, alpha: float, beta: float, depth: int) -> float:
        if cutoff_test is not None and cutoff_test(state, depth):
            return eval_fn(state)
        v = float("-inf")
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state: State, alpha: float, beta: float, depth: int) -> float:
        if cutoff_test is not None and cutoff_test(state, depth):
            return eval_fn(state)
        v = float("inf")
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    best_score = float("-inf")
    beta = float("inf")
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


