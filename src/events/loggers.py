import logging
from typing import Optional

from src.entities.base import Base
from src.entities.hero import HEROES, Hero
from src.entities.mission import MISSIONS, Mission
from src.entities.world import FINAL_TIME, N_MISSIONS

formatter = logging.Formatter("%(message)s")


def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(
        log_file,
        mode="w",
        encoding="utf-8",
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


class FinalEvent:
    def __init__(self) -> None:
        self.logger = setup_logger("final_logger", "logs/final.log")

    def update(self) -> None:
        self.logger.info(f"{FINAL_TIME}: END")

        [self.logger.info(str(HEROES[hero_id])) for hero_id in HEROES]

        missions_done = sum([mission.complete for mission in MISSIONS.values()])
        mean_attempts = (
            sum([mission.attempts for mission in MISSIONS.values()]) / N_MISSIONS
        )

        self.logger.info(
            f"{missions_done}/{N_MISSIONS} DONE ({missions_done / N_MISSIONS:.2%}) MEAN OF {mean_attempts} ATTEMPTS/MISSION"
        )


# class MissionEventLogger:
#     def __init__(self, time: int, mission: Mission) -> None:
#         self.time = time
#         self.mission = mission
#         self.logger = setup_logger("missions_logger", "logs/missions.log")

#     def __str__(self) -> str:
#         exit_str = f"{self.time}: {self.mission.__str__()}"

#         return exit_str

#     def update(self) -> None:
#         self.logger.info(self.__str__())


# class HeroEventLogger:
#     def __init__(self, time: int, hero: Hero, base: Base, action: str) -> None:
#         self.time = time
#         self.hero = hero
#         self.base = base
#         self.action = action
#         self.logger = setup_logger("heroes_logger", "logs/heroes.log")

#     def __str__(self) -> str:
#         exit_str = f"{self.time}: {self.action} {self.hero.__str__()}"

#         return exit_str

#     def update(self) -> None:
#         self.logger.info(self.__str__())


class BaseEventLogger:
    def __init__(self, time: int, base: Base, action: str) -> None:
        self.time = time
        self.base = base
        self.action = action
        self.logger = setup_logger("bases_logger", "logs/bases.log")

    def update(self) -> None:
        self.logger.info(self.__str__())

    def __str__(self) -> str:
        exit_str = f"{self.time}: {self.action} {self.base.__str__()}"

        return exit_str


class ArrivesEventLogger:
    def __init__(self, time: int, hero: Hero, base: Base) -> None:
        self.time = time
        self.hero = hero
        self.base = base

        self.logger = setup_logger("heroes_logger", "logs/heroes.log")

        self.successfull = None

    def update(self, successfull: bool) -> None:
        self.successfull = successfull

        self.logger.info(self.__str__())

    def __str__(self) -> str:
        exit_str = f"{self.time}: ARRIVES {self.hero.__str__()} {self.base.__repr__()}"

        if self.successfull:
            exit_str += " AWAITS"
        else:
            exit_str += " GIVES UP"

        return exit_str


class AwaitsEventLogger:
    def __init__(self, time: int, hero: Hero, base: Base) -> None:
        self.time = time
        self.hero = hero
        self.base = base

        self.logger = setup_logger("heroes_logger", "logs/heroes.log")

    def update(self) -> None:
        self.logger.info(self.__str__())

    def __str__(self) -> str:
        exit_str = f"{self.time}: AWAITS {self.hero.__str__()}"
        exit_str += f" {self.base.__str__()} ({self.base.queue_size})"

        return exit_str


class GivesUpEventLogger:
    def __init__(self, time: int, hero: Hero, base: Base) -> None:
        self.time = time
        self.hero = hero
        self.base = base

        self.logger = setup_logger("heroes_logger", "logs/heroes.log")

    def update(self) -> None:
        self.logger.info(self.__str__())

    def __str__(self) -> str:
        exit_str = super().__str__()
        exit_str += f" {self.base.__str__()}"

        return exit_str


class NotifiesEventLogger:
    def __init__(self, time: int, base: Base) -> None:
        self.time = time
        self.base = base

        self.logger = setup_logger("bases_logger", "logs/bases.log")

        self.heroes = list()

    def update(self, hero_id) -> None:
        self.heroes.append(hero_id)

        self.logger.info(self.__str__())

    def __str__(self) -> str:
        exit_str = f"{self.time}: NOTIFIES GATEKEEPER {self.base.__repr__()}"
        exit_str += f" QUEUE {self.base.queue}"

        for hero_id in self.heroes:
            exit_str += f"\n{self.time}: NOTIFIES GATEKEEPER {self.base.__str__()}"
            exit_str += f" WELCOMES HERO {hero_id}"

        return exit_str


class EntersEventLogger:
    def __init__(self, time: int, hero: Hero, base: Base) -> None:
        self.time = time
        self.hero = hero
        self.base = base
        self.exit_time = None

        self.logger = setup_logger("heroes_logger", "logs/heroes.log")

    def update(self, exit_time: int) -> None:
        self.exit_time = exit_time

        self.logger.info(self.__str__())

    def __str__(self) -> str:
        exit_str = f"{self.time}: ENTERS {self.hero.__str__()} {self.base.__repr__()}"
        exit_str += f" EXITS ({self.exit_time})"

        return exit_str


class ExitsEventLogger:
    def __init__(self, time: int, hero: Hero, base: Base) -> None:
        self.time = time
        self.hero = hero
        self.base = base

        self.logger = setup_logger("heroes_logger", "logs/heroes.log")

    def update(self) -> None:
        self.logger.info(self.__str__())

    def __str__(self) -> str:
        exit_str = f"{self.time}: EXITS {self.hero.__str__()} {self.base.__repr__()}"

        return exit_str


class TravelsEventLogger:
    def __init__(self, time: int, hero: Hero, destination: Base) -> None:
        self.time = time
        self.hero = hero
        self.destination = destination
        self.distance = None
        self.arrival_time = None

        self.logger = setup_logger("heroes_logger", "logs/heroes.log")

    def update(self, distance: int, arrival_time: int) -> None:
        self.distance = distance
        self.arrival_time = arrival_time

        self.logger.info(self.__str__())

    def __str__(self) -> str:
        exit_str = f"{self.time}: TRAVELS {self.hero.__str__()}"
        exit_str += f" {self.destination.__str__()}"
        exit_str += f" DIST {self.distance}"
        exit_str += f" SPEED {self.hero.speed}"
        exit_str += f" ARRIVES {self.arrival_time}"

        return exit_str


class MissionEventLogger:
    def __init__(self, time: int, mission: Mission) -> None:
        self.time = time
        self.mission = mission

        self.first_run = True

        self.base = None
        self.base_skills = None

        self.logger = setup_logger("missions_logger", "logs/missions.log")

    def update(
        self,
        base: Optional[Base] = None,
        base_skills: Optional[list] = None,
    ) -> None:
        self.base = base
        self.base_skills = base_skills

        self.logger.info(self.__str__())

    def __str__(self) -> str:
        exit_str = f"{self.time}: {self.mission.__str__()}"

        if self.first_run:
            exit_str += f" SKILLS REQ: {self.mission.skills}"
            self.first_run = False

        elif self.base and self.mission.complete:
            exit_str += f" COMPLETE {self.base.__str__()} HEROES: {self.base.heroes}"

        elif self.base:
            exit_str += f" SKILLS {self.base.__str__()}: {self.base_skills}"

        else:
            exit_str += f" IMPOSSIBLE"

        return exit_str
