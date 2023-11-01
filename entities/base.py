from dataclasses import dataclass, field

from entities.hero import Hero

"""
ID: int >= 0 - identificação única da base
Lotação: int >= 0 - número máximo de heróis
Presentes: list[int >= 0] - conjunto dos IDs dos heróis presentes
Espera: list[int >= 0] - conjunto dos IDs dos heróis na fila de espera
Local: tuple[int, int] - coordenada cartesiana [X, Y >= 0]
"""


@dataclass()
class Base:
    id_: int
    coords: tuple[int, int]
    base_size: int
    queue: list[Hero] = field(default_factory=list)
    heroes: list[Hero] = field(default_factory=list)

    @property
    def skills(self) -> list[int]:
        skills = []
        for hero in self.heroes:
            skills.extend(hero.skills)

        return list(set(skills))

    def add_to_queue(self, hero: Hero) -> None:
        self.queue.append(hero)

    def welcome_hero(self) -> Hero:
        hero = self.queue.pop(0)
        self.heroes.append(hero)

        return hero

    def remove(self, hero: Hero) -> None:
        self.heroes.remove(hero)

    def update_exp(self):
        for hero in self.heroes:
            hero.exp += 1

    @property
    def occupants(self) -> int:
        return len(self.heroes)

    @property
    def queue_size(self) -> int:
        return len(self.queue)

    def has_room(self) -> bool:
        return len(self.heroes) == 0

    def __str__(self):
        return f"{ self.id_}"
