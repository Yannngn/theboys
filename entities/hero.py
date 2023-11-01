from dataclasses import dataclass


@dataclass()
class Hero:
    id_: int
    patience: int
    speed: int
    skills: list[int]
    time: int
    exp: int = 0

    def __repr__(self):
        return f"{self.id_}"

    def __str__(self):
        return f"HERO {self.id_} PAT {self.patience} SPEED {self.patience} EXP {self.exp} SKILLS {self.skills}"
