"""Ręce do gry w blackjacka

Wartości rąk liczą funkcje z biblioteki Gymnasium (te same, których używa
środowisko Blackjack-v1), więc zasady są wszędzie identyczne
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from itertools import combinations_with_replacement

from gymnasium.envs.toy_text.blackjack import is_bust, is_natural, sum_hand, usable_ace

RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
SUITS = ("Pik", "Kier", "Karo", "Trefl")

# Rangi o różnych wartościach (10, J, Q, K liczą się tak samo -> wystarczy "10")
DISTINCT_RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10")


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str = "Pik"

    def __post_init__(self) -> None:
        if self.rank not in RANKS:
            raise ValueError(f"Nieznana ranga karty: {self.rank!r}")
        if self.suit not in SUITS:
            raise ValueError(f"Nieznany kolor karty: {self.suit!r}")

    @property
    def value(self) -> int:
        """Wartość karty jak w Gymnasium: As = 1 (Hand sam liczy go jako 11, gdy się da)"""
        if self.rank == "A":
            return 1
        if self.rank in ("J", "Q", "K"):
            return 10
        return int(self.rank)

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


@dataclass(frozen=True)
class Hand:
    cards: tuple[Card, ...]

    @classmethod
    def of(cls, *ranks: str) -> Hand:
        return cls(tuple(Card(r, SUITS[i % 4]) for i, r in enumerate(ranks)))

    def _values(self) -> list[int]:
        return [c.value for c in self.cards]

    @property
    def value(self) -> int:
        return sum_hand(self._values())

    @property
    def is_soft(self) -> bool:
        """Miękka ręka: As liczony jako 11 bez przekroczenia 21"""
        return usable_ace(self._values())

    @property
    def is_pair(self) -> bool:
        """Para do splitu (dwie karty o tej samej wartości, np. K+10)"""
        return len(self.cards) == 2 and self.cards[0].value == self.cards[1].value

    @property
    def is_blackjack(self) -> bool:
        return is_natural(self._values())

    @property
    def is_bust(self) -> bool:
        return is_bust(self._values())

    def add(self, card: Card) -> Hand:
        return Hand(self.cards + (card,))

    def state(self, dealer_upcard: Card) -> tuple[int, int, bool]:
        """Stan dla AI, jak obserwacja Gymnasium: (suma gracza, karta krupiera 1-10, miękki As)"""
        return self.value, dealer_upcard.value, self.is_soft

    def __str__(self) -> str:
        kind = "miękka" if self.is_soft else "twarda"
        return f"{' '.join(map(str, self.cards))} = {self.value} ({kind})"


@dataclass(frozen=True)
class Situation:
    """Przykładowa sytuacja: ręka gracza + odkryta karta krupiera"""

    player: Hand
    dealer_upcard: Card
    description: str

    @property
    def state(self) -> tuple[int, int, bool]:
        return self.player.state(self.dealer_upcard)


def all_starting_situations() -> list[Situation]:
    """Wszystkie rozróżnialne startowe sytuacje: 55 rąk x 10 kart krupiera = 550"""
    situations = []
    for r1, r2 in combinations_with_replacement(DISTINCT_RANKS, 2):
        hand = Hand.of(r1, r2)
        for dealer in DISTINCT_RANKS:
            situations.append(Situation(hand, Card(dealer, "Kier"), f"{r1}+{r2} vs {dealer}"))
    return situations


def random_situation(rng: random.Random | None = None) -> Situation:
    """Losowa sytuacja startowa, z prawdopodobieństwami jak przy prawdziwej talii"""
    rng = rng or random
    c1, c2, dealer = (Card(rng.choice(RANKS), rng.choice(SUITS)) for _ in range(3))
    return Situation(Hand((c1, c2)), dealer, "losowa")


if __name__ == "__main__":
    print(f"Wszystkich sytuacji startowych: {len(all_starting_situations())}")
