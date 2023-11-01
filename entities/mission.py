from dataclasses import dataclass


@dataclass()
class Mission:
    id_: int
    coords: tuple[int, int]
    skills: list[int]
    time: int
    complete: bool = False
    attempts: int = 0
