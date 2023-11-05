import random
from dataclasses import dataclass

from src.entities.world import N_HEROES, N_SKILLS


@dataclass()
class Hero:
    id_: int
    skills: list[int]
    patience: int
    speed: int
    exp: int = 0
    base_id: int | None = None

    def add_exp(self) -> None:
        self.exp += 1

    def __str__(self) -> str:
        return f"HERO {self.id_}"

    def __repr__(self) -> str:
        return f"HERO {self.id_} PAT {self.patience} SPEED {self.patience} EXP {self.exp} SKILLS {self.skills}"


def create_hero(id_: int) -> Hero:
    return Hero(
        id_=id_,
        patience=random.randint(0, 100),
        speed=random.randint(50, 5000),
        skills=random.sample(range(N_SKILLS), k=random.randint(1, 3)),
    )


HEROES: dict[int, Hero] = {id_: create_hero(id_) for id_ in range(N_HEROES)}
