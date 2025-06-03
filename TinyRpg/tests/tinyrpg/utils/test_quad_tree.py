import random as rnd


def install_mock():
    rnd.random = lambda: 2


# install_mock()


def test_random():
    assert 0 <= rnd.random() < 1
