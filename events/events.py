from dataclasses import dataclass, field

from entities.base import Base
from entities.hero import Hero
from entities.mission import Mission


@dataclass
class Event:
    time: int
    action: str = field(init=False)

    def __str__(self):
        exit_str = f"{self.time}: {self.action}"

        return exit_str


@dataclass
class GlobalEvent:
    time: int
    action: str

    def __str__(self):
        exit_str = f"{self.time}: {self.action}"

        return exit_str


@dataclass
class MissionEvent:
    time: int
    mission: Mission

    def __str__(self):
        exit_str = f"{self.time}: MISSION {self.mission.id_}"

        return exit_str


@dataclass
class HeroEvent(Event):
    time: int
    hero: Hero
    base: Base

    def __str__(self):
        exit_str = super().__str__()
        exit_str += f" HERO {self.hero.id_}"
        exit_str += f" BASE {self.base.id_}"

        return exit_str


@dataclass
class ArrivesEvent(HeroEvent):
    successfull: bool

    def __post_init__(self):
        self.action = "ARRIVES"

    def __str__(self):
        exit_str = super().__str__()
        exit_str += f" ({self.base.occupants}/{self.base.base_size})"

        if self.successfull:
            exit_str += " AWAITS"
        else:
            exit_str += " GIVES UP"

        return exit_str


@dataclass
class AwaitsEvent(HeroEvent):
    def __post_init__(self):
        self.action = "AWAITS"

    def __str__(self):
        exit_str = super().__str__()
        exit_str += f" ({self.base.queue_size})"

        return exit_str


@dataclass
class GivesUpEvent(HeroEvent):
    def __post_init__(self):
        self.action = "GIVES UP"

    def __str__(self):
        exit_str = super().__str__()

        return exit_str


@dataclass
class NotifiesEvent(Event):
    base: Base

    def __post_init__(self):
        self.action = "NOTIFIES GATEKEEPER"

    def __str__(self):
        exit_str = super().__str__()
        exit_str += f" BASE {self.base.id_}"
        exit_str += f" ({self.base.occupants}/{self.base.base_size})"
        exit_str += f" QUEUE {self.base.queue}"

        return exit_str


@dataclass
class GateKeeperEvent(Event):
    base: Base

    def __post_init__(self):
        self.action = "NOTIFIES GATEKEEPER"

    def __str__(self):
        exit_str = super().__str__()
        exit_str += f" BASE {self.base.id_}"
        exit_str += f" WELCOMES HERO {self.base.queue[0].id_}"

        return exit_str


@dataclass
class EntersEvent(HeroEvent):
    exit_time: int

    def __post_init__(self):
        self.action = "ENTERS"

    def __str__(self):
        exit_str = super().__str__()
        exit_str += f" ({self.base.occupants}/{self.base.base_size})"
        exit_str += f" EXITS ({self.exit_time})"

        return exit_str


@dataclass
class ExitsEvent(HeroEvent):
    def __post_init__(self):
        self.action = "EXITS"

    def __str__(self):
        exit_str = super().__str__()
        exit_str += f" ({self.base.occupants}/{self.base.base_size})"

        return exit_str


@dataclass
class TravelsEvent(HeroEvent):
    destination: Base
    distance: int
    arrival_time: int

    def __post_init__(self):
        self.action = "TRAVELS"

    def __str__(self):
        exit_str = super().__str__()
        exit_str += f" BASE {self.destination.id_}"
        exit_str += f" DIST {self.distance}"
        exit_str += f" SPEED {self.hero.speed}"
        exit_str += f" ARRIVES {self.arrival_time}"

        return exit_str


@dataclass
class MissionReqEvent(MissionEvent):
    def __str__(self):
        exit_str = super().__str__()
        exit_str += f" SKILLS REQ: {self.mission.skills}"

        return exit_str


@dataclass
class MissionCheckEvent(MissionEvent):
    base: Base

    def __str__(self):
        exit_str = super().__str__()
        exit_str += f" SKILLS BASE {self.base.id_}: {self.base.skills}"

        return exit_str


@dataclass
class MissionCompleteEvent(MissionEvent):
    base: Base

    def __str__(self):
        exit_str = super().__str__()

        exit_str += f" COMPLETE"
        exit_str += f" BASE {self.base.id_} HEROES: {self.base.heroes}"

        return exit_str


@dataclass
class ImpossibleMissionEvent(MissionEvent):
    def __str__(self):
        exit_str = super().__str__()

        exit_str += f" IMPOSSIBLE"

        return exit_str
