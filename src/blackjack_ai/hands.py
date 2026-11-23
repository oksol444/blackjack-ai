import random

from gymnasium.envs.toy_text import blackjack

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["Pik", "Kier", "Karo", "Trefl"]

# 10, J, Q, K mają tę samą wartość
DISTINCT_RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


class Card:
    def __init__(self, rank, suit="Pik"):
        if rank not in RANKS:
            raise ValueError("Nieznana ranga: " + str(rank))
        if suit not in SUITS:
            raise ValueError("Nieznany kolor: " + str(suit))
        self.rank = rank
        self.suit = suit

    # As = 1, figury = 10
    def value(self):
        if self.rank == "A":
            return 1
        if self.rank in ["J", "Q", "K"]:
            return 10
        return int(self.rank)

    def __str__(self):
        return self.rank + self.suit


class Hand:
    def __init__(self, cards):
        self.cards = cards

    def values(self):
        values = []
        for card in self.cards:
            values.append(card.value())
        return values

    def value(self):
        return blackjack.sum_hand(self.values())

    # As liczony jako 11
    def is_soft(self):
        return blackjack.usable_ace(self.values())

    def is_pair(self):
        return len(self.cards) == 2 and self.cards[0].value() == self.cards[1].value()

    def is_blackjack(self):
        return blackjack.is_natural(self.values())

    def is_bust(self):
        return blackjack.is_bust(self.values())

    def add(self, card):
        self.cards.append(card)

    # (suma gracza, karta krupiera, miękki As)
    def state(self, dealer_card):
        return (self.value(), dealer_card.value(), self.is_soft())

    def __str__(self):
        names = []
        for card in self.cards:
            names.append(str(card))
        kind = "miękka" if self.is_soft() else "twarda"
        return " ".join(names) + " = " + str(self.value()) + " (" + kind + ")"


def make_hand(*ranks):
    cards = []
    for i in range(len(ranks)):
        cards.append(Card(ranks[i], SUITS[i % 4]))
    return Hand(cards)


class Situation:
    def __init__(self, player, dealer_card, description):
        self.player = player
        self.dealer_card = dealer_card
        self.description = description

    def state(self):
        return self.player.state(self.dealer_card)


# 55 rąk x 10 kart krupiera = 550
def all_starting_situations():
    situations = []
    for i in range(len(DISTINCT_RANKS)):
        for j in range(i, len(DISTINCT_RANKS)):
            r1 = DISTINCT_RANKS[i]
            r2 = DISTINCT_RANKS[j]
            for dealer in DISTINCT_RANKS:
                hand = make_hand(r1, r2)
                situations.append(Situation(hand, Card(dealer, "Kier"), r1 + "+" + r2 + " vs " + dealer))
    return situations


def random_situation(rng=None):
    if rng is None:
        rng = random.Random()
    cards = []
    for _ in range(3):
        cards.append(Card(rng.choice(RANKS), rng.choice(SUITS)))
    return Situation(Hand([cards[0], cards[1]]), cards[2], "losowa")


if __name__ == "__main__":
    print("Wszystkich sytuacji startowych:", len(all_starting_situations()))
