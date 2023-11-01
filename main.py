import random

from entities.world import BASES, EXECUTION_DICT, FINAL_TIME, HEROES, MISSIONS
from events.functional import arrives, do_mission, ends


def main():
    CLOCK = 0
    for hero in HEROES.values():
        base = random.choice(list(BASES.values()))

        EXECUTION_DICT[hero.time].append((arrives, (hero, base, hero.time)))

    for mission in MISSIONS.values():
        EXECUTION_DICT[mission.time].append((do_mission, (mission, mission.time)))

    while CLOCK < FINAL_TIME:
        func_list = EXECUTION_DICT[CLOCK]
        for func, args in func_list:
            outputs = func(*args)

            if isinstance(outputs, tuple):
                new_time, func, args = outputs

                if new_time < FINAL_TIME:
                    EXECUTION_DICT[new_time].append((func, args))

            elif isinstance(outputs, list):
                for new_call in outputs:
                    new_time, func, args = new_call

                    if new_time < FINAL_TIME:
                        EXECUTION_DICT[new_time].append((func, args))

        CLOCK += 1

    ends(FINAL_TIME)


if __name__ == "__main__":
    main()
