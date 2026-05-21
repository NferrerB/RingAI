from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Optional


State = Any
EvaluateFn = Callable[[State], float]
ChildrenFn = Callable[[State], Iterable[State]]
TerminalFn = Callable[[State], bool]


@dataclass(frozen=True)
class SearchResult:
    score: float
    state: State | None = None


def _default_terminal(state: State) -> bool:
    required = {"bronce": 7, "plata": 3, "oro": 1}
    return all(getattr(state, attr, -1) >= target for attr, target in required.items())


def _default_evaluate(state: State) -> float:
    if not all(hasattr(state, attr) for attr in ("bronce", "plata", "oro")):
        return 0.0

    score = float(state.bronce * 10 + state.plata * 40 + state.oro * 100)

    if getattr(state, "bloqueado", False):
        score -= 25.0

    reserva = getattr(state, "reserva", None)
    mano = getattr(state, "mano", None)
    fase = state.fase_actual() if hasattr(state, "fase_actual") else None

    if reserva is not None:
        tipo_reserva = getattr(reserva, "tipo", None)
        score += 12.0 if fase is not None and tipo_reserva == fase else 2.0

    if mano is not None:
        tipo_mano = getattr(mano, "tipo", None)
        score += 6.0 if fase is not None and tipo_mano == fase else 1.0

    mazo = getattr(state, "mazo", None)
    cabeza = getattr(mazo, "cabeza", None) if mazo is not None else None
    if cabeza is None and mano is None and reserva is None:
        score -= 15.0

    return score


def _advance_reserve(state: State) -> None:
    reserva = getattr(state, "reserva", None)
    if reserva is None:
        return

    tipo = getattr(reserva, "tipo", None)
    fase = state.fase_actual() if hasattr(state, "fase_actual") else None

    if tipo == "Bronce" and (fase is None or fase == "Bronce") and getattr(state, "bronce", 0) < 7:
        state.bronce += 1
    elif tipo == "Plata" and (fase is None or fase == "Plata") and getattr(state, "plata", 0) < 3:
        state.plata += 1
    elif tipo == "Oro" and (fase is None or fase == "Oro") and getattr(state, "oro", 0) < 1:
        state.oro += 1

    state.reserva = None


def _default_children(state: State) -> list[State]:
    children: list[State] = []

    if not all(hasattr(state, attr) for attr in ("mano", "reserva", "mazo")):
        return children

    if state.mano is None and getattr(state.mazo, "cabeza", None) is not None:
        child = deepcopy(state)
        child.mano = child.mazo.extraer_del_frente()
        if child.mano is not None:
            children.append(child)

    if state.mano is not None and state.reserva is None:
        child = deepcopy(state)
        child.reserva = child.mano
        child.mano = None
        children.append(child)

    if state.reserva is not None:
        child = deepcopy(state)
        _advance_reserve(child)
        children.append(child)

    return children


class MinimaxAI:
    def __init__(
        self,
        depth: int = 3,
        evaluate_fn: Optional[EvaluateFn] = None,
        children_fn: Optional[ChildrenFn] = None,
        terminal_fn: Optional[TerminalFn] = None,
    ) -> None:
        self.depth = depth
        self.evaluate_fn = evaluate_fn or _default_evaluate
        self.children_fn = children_fn or _default_children
        self.terminal_fn = terminal_fn or _default_terminal

    def choose(self, state: State) -> State | None:
        result = self._minimax(state, self.depth, True, float("-inf"), float("inf"))
        return result.state

    def score(self, state: State) -> float:
        return self.evaluate_fn(state)

    def _minimax(
        self,
        state: State,
        depth: int,
        maximizing_player: bool,
        alpha: float,
        beta: float,
    ) -> SearchResult:
        if depth == 0 or self.terminal_fn(state):
            return SearchResult(self.evaluate_fn(state), state)

        children = list(self.children_fn(state))
        if not children:
            return SearchResult(self.evaluate_fn(state), state)

        if maximizing_player:
            best_score = float("-inf")
            best_state = None

            for child in children:
                result = self._minimax(child, depth - 1, False, alpha, beta)
                if result.score > best_score:
                    best_score = result.score
                    best_state = child
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break

            return SearchResult(best_score, best_state)

        best_score = float("inf")
        best_state = None

        for child in children:
            result = self._minimax(child, depth - 1, True, alpha, beta)
            if result.score < best_score:
                best_score = result.score
                best_state = child
            beta = min(beta, best_score)
            if alpha >= beta:
                break

        return SearchResult(best_score, best_state)


def minimax(state: State, depth: int, maximizing_player: bool) -> float:
    return MinimaxAI(depth=depth)._minimax(state, depth, maximizing_player, float("-inf"), float("inf")).score


def is_terminal(state: State) -> bool:
    return _default_terminal(state)


def evaluate(state: State) -> float:
    return _default_evaluate(state)


def get_children(state: State) -> list[State]:
    return _default_children(state)

