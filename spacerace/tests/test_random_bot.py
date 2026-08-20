"""Story 8: RandomBot InputSource determinism and behavior."""

from spacerace.core.input import InputCommand
from spacerace.game.random_bot import RandomBot


def test_bot_never_confirms() -> None:
    bot = RandomBot(seed=42)

    for _ in range(100):
        command = bot.poll(dt=0.01)
        assert command.confirm is False


def test_bot_is_deterministic_with_same_seed_and_dt() -> None:
    bot_a = RandomBot(seed=42)
    bot_b = RandomBot(seed=42)
    dts = [0.05, 0.05, 0.05, 0.05, 0.1, 0.1]

    for dt in dts:
        assert bot_a.poll(dt) == bot_b.poll(dt)


def test_bot_returns_input_command() -> None:
    bot = RandomBot(seed=0)

    command = bot.poll(dt=1.0)

    assert isinstance(command, InputCommand)
