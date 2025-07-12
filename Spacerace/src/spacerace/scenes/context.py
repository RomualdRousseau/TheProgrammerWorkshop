import pyray as pr

from spacerace.entities.asteriod import Asteroid
from spacerace.entities.entity import Entity
from spacerace.entities.player import Player


class Context:
    timer: float

    score1: int
    player1: Player

    score2: int
    player2: Player

    asteroids: list[Asteroid]

    entities: list[Entity]

    stream: pr.AudioStream
    stream_freq1: float
    stream_freq2: float
    stream_freq3: float
    stream_time: float

    music: pr.Music
