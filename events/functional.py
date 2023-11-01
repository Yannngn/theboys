import random
from typing import Callable

from entities.base import Base
from entities.hero import Hero
from entities.mission import Mission
from entities.world import BASES, BASES_LEN, FINAL_TIME, HEROES, MISSIONS, MISSIONS_LEN
from events.events import (
    ArrivesEvent,
    AwaitsEvent,
    EntersEvent,
    ExitsEvent,
    GateKeeperEvent,
    GivesUpEvent,
    GlobalEvent,
    ImpossibleMissionEvent,
    MissionCheckEvent,
    MissionCompleteEvent,
    MissionReqEvent,
    NotifiesEvent,
    TravelsEvent,
)
from events.loggers import setup_logger
from events.utils import cartesian_distance

heroes_logger = setup_logger("heroes_logger", "logs/heroes.log")
bases_logger = setup_logger("bases_logger", "logs/bases.log")
missions_logger = setup_logger("missions_logger", "logs/missions.log")
final_logger = setup_logger("final_logger", "logs/final.log")


def arrives(hero: Hero, base: Base, time: int):
    if base.has_room and base.queue_size == 0:
        can_wait = True
    else:
        can_wait = hero.patience > (10 * base.queue_size)

    heroes_logger.info(ArrivesEvent(hero=hero, base=base, time=time, successfull=True))

    if can_wait:
        awaits(hero, base, time)
    else:
        gives_up(hero, base, time)


def awaits(hero: Hero, base: Base, time: int):
    base.add_to_queue(hero)

    heroes_logger.info(AwaitsEvent(hero=hero, base=base, time=time))

    notifies(base, time)


def gives_up(hero: Hero, base: Base, time: int):
    heroes_logger.info(GivesUpEvent(time, hero=hero, base=base))

    new_base_id = random.choice(
        list(range(base.id_)) + list(range(base.id_, BASES_LEN))
    )

    new_base = BASES[new_base_id]

    travels(hero, base, new_base, time)


def notifies(base: Base, time: int):
    bases_logger.info(NotifiesEvent(base=base, time=time))

    while base.base_size - base.occupants > 0 and base.queue_size > 0:
        bases_logger.info(GateKeeperEvent(base=base, time=time))
        base.welcome_hero()


def enters(hero: Hero, base: Base, time: int):
    time_in_base = 15 + hero.patience * random.randint(1, 20)
    exit_time = time + time_in_base

    heroes_logger.info(EntersEvent(time, hero=hero, base=base, exit_time=exit_time))

    exits(hero, base, exit_time)


def exits(hero: Hero, base: Base, time: int):
    base.remove(hero.id_)

    heroes_logger.info(ExitsEvent(time, hero=hero, base=base))

    new_base_id = random.choice(
        list(range(base.id_)) + list(range(base.id_, BASES_LEN))
    )

    new_base = BASES[new_base_id]

    travels(hero, base, new_base, time)
    notifies(base, time)


def travels(
    hero: Hero, base: Base, destination: Base, time: int
) -> tuple[int, Callable, tuple]:
    distance = int(cartesian_distance(base.coords, destination.coords))
    travel_time = distance // hero.speed
    arrival_time = time + travel_time

    heroes_logger.info(
        TravelsEvent(
            hero=hero,
            base=base,
            time=time,
            destination=destination,
            distance=distance,
            arrival_time=arrival_time,
        )
    )

    return (arrival_time, arrives, (hero, destination, arrival_time))


def do_mission(mission: Mission, time: int) -> tuple[int, Callable, tuple] | None:
    missions_logger.info(MissionReqEvent(time, mission))
    mission.attempts += 1

    distances = {
        id_: cartesian_distance(base.coords, mission.coords)
        for id_, base in BASES.items()
    }

    distances = dict(sorted(distances.items(), key=lambda x: x[1]))

    for id_ in distances:
        base = BASES[id_]

        missions_logger.info(MissionCheckEvent(time, mission, base))

        if all([ms in base.skills for ms in mission.skills]):
            mission.complete = True

            missions_logger.info(MissionCompleteEvent(time, mission, base))

            base.update_exp()

            return

    missions_logger.info(ImpossibleMissionEvent(time, mission))
    new_time = time + 24 * 60

    if new_time >= FINAL_TIME:
        return

    return (new_time, do_mission, (mission, new_time))


def ends(time: int):
    final_logger.info(GlobalEvent(time, "END"))
    for hero in HEROES.values():
        final_logger.info(f"{hero.__str__()}")

    missions_done = sum([mission.complete for mission in MISSIONS.values()])
    mean_attempts = (
        sum([mission.attempts for mission in MISSIONS.values()]) / MISSIONS_LEN
    )

    final_logger.info(
        f"{missions_done}/{MISSIONS_LEN} DONE ({missions_done / MISSIONS_LEN:.2%}) MEAN {mean_attempts} ATTEMPTS/MISSION"
    )
