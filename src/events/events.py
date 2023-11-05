import random
from typing import Self

from src.entities.base import BASES, Base
from src.entities.hero import HEROES, Hero
from src.entities.mission import Mission
from src.entities.world import N_BASES
from src.events.loggers import (
    ArrivesEventLogger,
    AwaitsEventLogger,
    EntersEventLogger,
    GivesUpEventLogger,
    MissionEventLogger,
    NotifiesEventLogger,
    TravelsEventLogger,
)
from src.events.utils import cartesian_distance


class Event:
    def __init__(self, time: int) -> None:
        self.time = time
        self.logger = None

    def __call__(self) -> Self:
        ...

    def __str__(self) -> str:
        return str(self.logger)


class FutureEventsList:
    def __init__(self) -> None:
        self.event_dict: dict[int, list] = {}

    def add(self, event: Event) -> None:
        self.event_dict.setdefault(event.time, list())
        self.event_dict[event.time].append(event)

    def update(self, now: int) -> None:
        for event in self.event_dict.get(now, []):
            output = event()
            print(event.__str__())

            if isinstance(output, list):
                for child_event in output:
                    self.add(child_event)

            elif isinstance(output, Event):
                self.add(output)

        # if now > 0:
        #     self.event_dict.pop(now - 1, None)


class ArrivesEvent(Event):
    def __init__(self, time: int, hero: Hero, base: Base) -> None:
        super().__init__(time)
        self.hero = hero
        self.base = base

        self.logger = ArrivesEventLogger(time, hero, base)

    def __call__(self) -> Event:
        self.hero.base_id = self.base.id_

        if self.base.has_room and self.base.queue_size == 0:
            wait = True
        else:
            wait = self.hero.patience > (10 * self.base.queue_size)

        self.logger.update(wait)

        if wait:
            return AwaitsEvent(self.time, self.hero, self.base)

        return GivesUpEvent(self.time, self.hero, self.base)

    def __str__(self) -> str:
        return str(self.logger)


class AwaitsEvent(Event):
    def __init__(self, time: int, hero: Hero, base: Base) -> None:
        super().__init__(time)
        self.hero = hero
        self.base = base

        self.logger = AwaitsEventLogger(time, hero, base)

    def __call__(self) -> Event:
        self.base.add_to_queue(self.hero.id_)

        self.logger.update()

        return NotifiesEvent(self.time, self.base)

    def __str__(self) -> str:
        return str(self.logger)


class GivesUpEvent(Event):
    def __init__(self, time: int, hero: Hero, base: Base) -> None:
        super().__init__(time)
        self.hero = hero
        self.base = base

        self.logger = GivesUpEventLogger(time, hero, base)

    def __call__(self) -> Event:
        possible_bases = [d for d in range(N_BASES) if d != self.base.id_]
        dest_id = random.choice(possible_bases)
        destination = BASES[dest_id]

        self.logger.update()

        return TravelsEvent(self.time, self.hero, destination)

    def __str__(self) -> str:
        return str(self.logger)


class NotifiesEvent(Event):
    def __init__(self, time: int, base: Base) -> None:
        super().__init__(time)
        self.base = base

        self.logger = NotifiesEventLogger(time, base)

    def __call__(self) -> list[Event]:
        output = []

        while self.base.has_room and self.base.queue_size > 0:
            self.base.welcome_hero()
            hero_id = self.base.last_hero

            self.logger.update(hero_id)

            hero = HEROES[hero_id]

            output.append(EntersEvent(self.time, hero, self.base))

        return output

    def __str__(self) -> str:
        return str(self.logger)


class TravelsEvent(Event):
    def __init__(self, time: int, hero: Hero, destination: Base) -> None:
        super().__init__(time)
        self.hero = hero
        self.destination = destination

        self.logger = TravelsEventLogger(time, hero, destination)

    def __call__(self) -> Event:
        assert self.hero.base_id is not None

        current_base = BASES[self.hero.base_id]

        distance = cartesian_distance(current_base.coords, self.destination.coords)

        travel_time = distance // self.hero.speed
        arrival_time = self.time + travel_time

        self.logger.update(distance, arrival_time)

        return ArrivesEvent(arrival_time, self.hero, self.destination)


class EntersEvent(Event):
    def __init__(self, time: int, hero: Hero, base: Base) -> None:
        super().__init__(time)
        self.hero = hero
        self.base = base

        self.logger = EntersEventLogger(time, hero, base)

    def __call__(self) -> Event:
        time_to_exit = 15 + self.hero.patience * random.randint(1, 20)
        exit_time = self.time + time_to_exit

        self.logger.update(exit_time)

        return ExitsEvent(exit_time, self.hero, self.base)


class ExitsEvent(Event):
    def __init__(self, time: int, hero: Hero, base: Base) -> None:
        super().__init__(time)
        self.hero = hero
        self.base = base

    def __call__(self) -> list[Event]:
        output = []
        self.base.remove(self.hero.id_)

        possible_bases = [dest for dest in range(N_BASES) if dest != self.base.id_]
        dest_id = random.choice(possible_bases)
        destination = BASES[dest_id]

        output.append(TravelsEvent(self.time, self.hero, destination))
        output.append(NotifiesEvent(self.time, self.base))

        return output


class MissionEvent(Event):
    def __init__(self, time: int, mission: Mission) -> None:
        super().__init__(time)
        self.mission = mission

        self.logger = MissionEventLogger(time, mission)

    def __call__(self) -> Event | None:
        self.logger.update()
        self.mission.attempts += 1

        distances = {
            id_: cartesian_distance(base.coords, self.mission.coords)
            for id_, base in BASES.items()
        }

        distances = dict(sorted(distances.items(), key=lambda x: x[1]))

        for id_ in distances:
            base = BASES[id_]
            base_skills = [
                skill for hero_id in base.heroes for skill in HEROES[hero_id].skills
            ]
            base_skills = list(set(base_skills))

            self.logger.update(base, base_skills)

            if all([skill in base_skills for skill in self.mission.skills]):
                self.mission.complete = True

                [HEROES[hero_id].add_exp() for hero_id in base.heroes]

                self.logger.update(base, base_skills)

                return

        self.logger.update()

        return MissionEvent(self.time + 24 * 60, self.mission)
