import numpy as np

from blackjack_ai.baselines import basic_strategy
from blackjack_ai.env import HIT, STAND, make_env


def test_observation_format():
    envs, obs = make_env(8, seed=0)
    total, dealer, soft = obs
    assert total.shape == (8,)
    assert ((4 <= total) & (total <= 21)).all()
    assert ((1 <= dealer) & (dealer <= 10)).all()  # 1 = As
    assert set(np.unique(soft)) <= {0, 1}
    envs.close()


def test_stand_always_ends_hand():
    envs, _ = make_env(64, seed=1)
    _, reward, terminated, _, _ = envs.step(np.full(64, STAND))
    assert terminated.all()
    assert set(np.unique(reward)) <= {-1.0, 0.0, 1.0, 1.5}
    envs.close()


def test_blackjack_pays_3_to_2():
    envs, _ = make_env(5000, seed=3)
    _, reward, _, _, _ = envs.step(np.full(5000, STAND))
    assert (reward == 1.5).any()
    envs.close()


def test_rewards_are_valid_when_always_hitting():
    envs, _ = make_env(64, seed=2)
    for _ in range(20):
        _, reward, terminated, _, _ = envs.step(np.full(64, HIT))
        assert set(np.unique(reward[terminated])) <= {-1.0}
        assert (reward[~terminated] == 0).all()
    envs.close()


def test_basic_strategy_treats_dealer_ace_as_strong():
    assert basic_strategy((16, 1, False)) == HIT   # 16 vs As
    assert basic_strategy((16, 6, False)) == STAND
    assert basic_strategy((18, 1, True)) == HIT    # miękkie 18 vs As
