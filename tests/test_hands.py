import random

import pytest

from blackjack_ai.hands import (
    Card,
    Hand,
    all_starting_situations,
    random_situation,
)


@pytest.mark.parametrize(
    "ranks, value, soft",
    [
        (("10", "6"), 16, False),
        (("A", "7"), 18, True),
        (("A", "A"), 12, True),
        (("A", "5", "10"), 16, False),
        (("A", "A", "9"), 21, True),
        (("K", "Q", "J"), 30, False),
    ],
)
def test_value_and_softness(ranks, value, soft):
    hand = Hand.of(*ranks)
    assert hand.value == value
    assert hand.is_soft == soft


def test_blackjack_only_with_two_cards():
    assert Hand.of("A", "K").is_blackjack
    assert not Hand.of("7", "7", "7").is_blackjack


def test_pair_uses_card_value():
    assert Hand.of("10", "K").is_pair
    assert not Hand.of("9", "10").is_pair


def test_bust():
    assert Hand.of("10", "6", "8").is_bust
    assert not Hand.of("10", "A").is_bust


def test_invalid_card():
    with pytest.raises(ValueError):
        Card("1")


def test_state():
    assert Hand.of("A", "6").state(Card("10")) == (17, 10, True)


def test_starting_situations_count():
    assert len(all_starting_situations()) == 550


def test_random_situation_is_reproducible():
    a = random_situation(random.Random(42))
    b = random_situation(random.Random(42))
    assert a == b
