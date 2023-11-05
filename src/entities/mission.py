import random
from dataclasses import dataclass

from src.entities.world import FINAL_TIME, N_MISSIONS, N_SKILLS, WORLD_SIZE


@dataclass()
class Mission:
    id_: int
    coords: tuple[int, int]
    skills: list[int]
    time: int
    complete: bool = False
    attempts: int = 0

    def __str__(self) -> str:
        return f"MISSION {self.id_}"


def create_mission(id_: int) -> Mission:
    return Mission(
        id_=id_,
        time=random.randint(0, FINAL_TIME),
        coords=(random.randint(0, WORLD_SIZE), random.randint(0, WORLD_SIZE)),
        skills=sorted(random.sample(range(N_SKILLS), k=random.randint(6, N_SKILLS))),
    )


MISSIONS: dict[int, Mission] = {id_: create_mission(id_) for id_ in range(N_MISSIONS)}
