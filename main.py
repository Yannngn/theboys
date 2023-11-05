import json
import random

from tqdm.auto import tqdm

from src.entities.base import BASES
from src.entities.hero import HEROES
from src.entities.mission import MISSIONS
from src.entities.world import FINAL_TIME
from src.events.events import ArrivesEvent, FutureEventsList, MissionEvent
from src.events.loggers import FinalEvent


def main():
    CLOCK = 0
    fel = FutureEventsList()
    fe = FinalEvent()

    for hero in HEROES.values():
        time = random.randint(0, 4320)
        base = random.choice(list(BASES.values()))

        fel.add(ArrivesEvent(time, hero, base))

    for mission in MISSIONS.values():
        time = random.randint(0, FINAL_TIME)
        fel.add(MissionEvent(time, mission))

    loop = tqdm(range(0, FINAL_TIME))
    while CLOCK < 500:
        fel.update(CLOCK)

        CLOCK += 1

        loop.update()
    loop.close()

    with open("logs/fel.json", "w") as f:
        dict_ = {
            k: [o.__class__.__name__ for o in v] for k, v in fel.event_dict.items()
        }

        json.dump(dict_, f)

    fe.update()


if __name__ == "__main__":
    main()
