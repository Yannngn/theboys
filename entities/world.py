import random
from typing import Callable

from entities.base import Base
from entities.hero import Hero
from entities.mission import Mission

INITIAL_TIME: int = 0
FINAL_TIME: int = 525_600  # minutes
WORLD_SIZE: int = 20_000  # meters
SKILLS_LEN: int = 10
HEROES_LEN: int = SKILLS_LEN * 5
BASES_LEN: int = HEROES_LEN // 6
MISSIONS_LEN: int = FINAL_TIME // 100

HEROES: dict[int, Hero] = {
    id_: Hero(
        id_=id_,
        patience=random.randint(0, 100),
        speed=random.randint(50, 5000),
        skills=random.sample(range(SKILLS_LEN), k=random.randint(1, 3)),
        time=random.randint(0, 4320),
    )
    for id_ in range(HEROES_LEN)
}

BASES: dict[int, Base] = {
    id_: Base(
        id_=id_,
        coords=(random.randint(0, WORLD_SIZE), random.randint(0, WORLD_SIZE)),
        base_size=random.randint(3, 10),
    )
    for id_ in range(BASES_LEN)
}

MISSIONS: dict[int, Mission] = {
    id_: Mission(
        id_=id_,
        time=random.randint(0, FINAL_TIME),
        coords=(random.randint(0, WORLD_SIZE), random.randint(0, WORLD_SIZE)),
        skills=sorted(
            random.sample(range(SKILLS_LEN), k=random.randint(6, SKILLS_LEN))
        ),
    )
    for id_ in range(MISSIONS_LEN)
}


EXECUTION_DICT: dict[int, list[tuple[Callable, tuple]]] = {
    time: list() for time in range(FINAL_TIME)
}
