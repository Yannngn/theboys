from typing import Callable

INITIAL_TIME: int = 0
FINAL_TIME: int = 525_600  # minutes
WORLD_SIZE: int = 20_000  # meters
N_SKILLS: int = 10
N_HEROES: int = N_SKILLS * 5
N_BASES: int = N_HEROES // 6
N_MISSIONS: int = FINAL_TIME // 100


EXECUTION_DICT: dict[int, list[tuple[Callable, tuple]]] = {
    time: list() for time in range(FINAL_TIME)
}
