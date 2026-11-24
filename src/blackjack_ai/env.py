"""Środowisko gry oparte na bibliotece Gymnasium (Blackjack-v1).

Zasady gry pochodzą w całości z biblioteki:
- nieskończona talia,
- ruchy: STAND (0) i HIT (1),
- krupier dobiera do 17 i stoi na każdym 17,
- blackjack gracza płaci 3:2 (opcja natural=True).

Obserwacja (stan) to krotka: (suma gracza, karta krupiera 1-10 gdzie 1 = As, miękki As).
"""

from __future__ import annotations

import gymnasium as gym

STAND = 0
HIT = 1
ACTIONS = (STAND, HIT)
ACTION_NAMES = {STAND: "S", HIT: "H"}

State = tuple[int, int, bool]


def make_env(num_envs: int, seed: int) -> tuple[gym.vector.VectorEnv, tuple]:
    """Tworzy `num_envs` równoległych stołów i zwraca (środowisko, pierwsze obserwacje).

    Tryb SAME_STEP: gdy rozdanie się kończy, stół od razu rozdaje nowe,
    a krok zwraca nagrodę za zakończone rozdanie i obserwację z nowego.
    """
    envs = gym.make_vec(
        "Blackjack-v1",
        num_envs=num_envs,
        vectorization_mode="sync",
        vector_kwargs={"autoreset_mode": gym.vector.AutoresetMode.SAME_STEP},
        natural=True,
        # Blackjack-v1 domyślnie ma sab=True (zasady z książki Suttona i Barto),
        # które wyłączają wypłatę 3:2 za blackjacka - dlatego wyłączamy to jawnie.
        sab=False,
    )
    obs, _ = envs.reset(seed=seed)
    return envs, obs
