import random
from dataclasses import dataclass, field

from src.entities.world import N_BASES, WORLD_SIZE


@dataclass()
class Base:
    id_: int
    base_size: int
    coords: tuple[int, int]
    queue: list[int] = field(default_factory=list)
    heroes: list[int] = field(default_factory=list)

    def add_to_queue(self, hero_id: int) -> None:
        self.queue.append(hero_id)

    def welcome_hero(self) -> None:
        hero = self.queue.pop(0)
        self.heroes.append(hero)

    def remove(self, hero_id: int) -> None:
        self.heroes.remove(hero_id)

    @property
    def last_hero(self) -> int:
        return self.heroes[-1]

    @property
    def first_hero_in_queue(self) -> int:
        return self.queue[0]

    @property
    def occupants(self) -> int:
        return len(self.heroes)

    @property
    def queue_size(self) -> int:
        return len(self.queue)

    @property
    def has_room(self) -> bool:
        return len(self.heroes) == 0

    def __str__(self) -> str:
        return f"BASE {self.id_}"

    def __repr__(self) -> str:
        return f"BASE {self.id_} ({self.occupants}/{self.base_size})"


def create_base(id_: int) -> Base:
    return Base(
        id_=id_,
        coords=(random.randint(0, WORLD_SIZE), random.randint(0, WORLD_SIZE)),
        base_size=random.randint(3, 10),
    )


BASES: dict[int, Base] = {id_: create_base(id_) for id_ in range(N_BASES)}
