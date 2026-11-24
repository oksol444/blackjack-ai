"""Proste strategie do porównania z AI.

Stan jak w Gymnasium: (suma gracza, karta krupiera 1-10 gdzie 1 = As, miękki As).
"""

from __future__ import annotations

import random

from blackjack_ai.env import HIT, STAND, State

_rng = random.Random(0)


def random_policy(state: State) -> int:
    return _rng.choice((HIT, STAND))


def dealer_policy(state: State) -> int:
    """Graj jak krupier: dobieraj poniżej 17."""
    total, _, _ = state
    return HIT if total < 17 else STAND


def basic_strategy(state: State) -> int:
    """Strategia podstawowa ograniczona do HIT/STAND (bez double i split)."""
    total, dealer, soft = state
    dealer = 11 if dealer == 1 else dealer  # As krupiera jest najsilniejszy
    if soft:
        if total >= 19:
            return STAND
        if total == 18:
            return STAND if dealer <= 8 else HIT
        return HIT
    if total >= 17:
        return STAND
    if total >= 13:
        return STAND if dealer <= 6 else HIT
    if total == 12:
        return STAND if 4 <= dealer <= 6 else HIT
    return HIT
