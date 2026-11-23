import random

import pytest

from blackjack_ai.hands import Card, all_starting_situations, make_hand, random_situation


def test_value_and_softness():
    cases = [
        (("10", "6"), 16, False),
        (("A", "7"), 18, True),
        (("A", "A"), 12, True),
        (("A", "5", "10"), 16, False),
        (("A", "A", "9"), 21, True),
        (("K", "Q", "J"), 30, False),
    ]
    for ranks, value, soft in cases:
        hand = make_hand(*ranks)
        assert hand.value() == value
        assert hand.is_soft() == soft


def test_blackjack_only_with_two_cards():
    assert make_hand("A", "K").is_blackjack()
    assert not make_hand("7", "7", "7").is_blackjack()


def test_pair_uses_card_value():
    assert make_hand("10", "K").is_pair()
    assert not make_hand("9", "10").is_pair()


def test_bust():
    assert make_hand("10", "6", "8").is_bust()
    assert not make_hand("10", "A").is_bust()


def test_add_card():
    hand = make_hand("10", "2")
    hand.add(Card("5"))
    assert hand.value() == 17


def test_invalid_card():
    with pytest.raises(ValueError):
        Card("1")


def test_state():
    assert make_hand("A", "6").state(Card("10")) == (17, 10, True)


def test_starting_situations_count():
    assert len(all_starting_situations()) == 550


def test_random_situation_is_reproducible():
    a = random_situation(random.Random(42))
    b = random_situation(random.Random(42))
    assert str(a.player) == str(b.player)
    assert str(a.dealer_card) == str(b.dealer_card)
