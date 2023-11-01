from math import sqrt


def cartesian_distance(coords_1, coords_2):
    x1, y1 = coords_1
    x2, y2 = coords_2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
