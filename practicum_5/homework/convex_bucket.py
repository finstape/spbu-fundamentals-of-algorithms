from time import perf_counter
from functools import cmp_to_key
import numpy as np
from numpy.typing import NDArray
from typing import Tuple

from src.plotting import plot_points


# orientation of a trio of points
def orientation(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]) -> int:
    """
    to determine the orientation, the determinant of the 3x3 matrix, composed of the coordinates of the points, is used
        | a[0] a[1] 1 |
    det=| b[0] b[1] 1 |
        | c[0] c[1] 1 |
    """
    val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
    # when val = 0, it means that all points lie on the same lines
    if val == 0:
        return 0
    # when val > 0, it means that they form a clockwise rotation
    if val > 0:
        return 1
    # when val < 0, it means that they form a counterclockwise rotation
    return 2


# comparison of points for sorting
def comparator(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    val = orientation(p0, a, b)
    if val == 0:
        # choosing a more distant point
        if a[0] + a[1] < b[0] + b[1]:
            # a < b
            return -1
        else:
            # a > b
            return 1
    # a < b
    if val == 2:
        return -1
    # a > b
    return 1


def convex_bucket(points: NDArray) -> NDArray:
    """Complexity: O(n log n)"""
    # find the lowest right point and put it at the top of the list
    points = [(p[0], p[1]) for p in points]
    global p0
    p0 = points[0]
    for p in points:
        if p[0] > p0[0] or (p[0] == p0[0] and p[1] < p0[1]):
            p0 = p
    points.remove(p0)
    points.insert(0, p0)

    # sort the remaining points by polar angle relative to the minimum point
    points = sorted(points, key=cmp_to_key(comparator))

    # convex hull algorithm
    clockwise_sorted_ch = [points[0], points[1], points[2]]
    for i in range(3, len(points)):
        while len(clockwise_sorted_ch) > 1 and orientation(clockwise_sorted_ch[-2], clockwise_sorted_ch[-1],
                                                           points[i]) != 2:
            clockwise_sorted_ch.pop()
        clockwise_sorted_ch.append(points[i])

    return np.array(clockwise_sorted_ch)


if __name__ == "__main__":
    for i in range(1, 11):
        txtpath = f"practicum_5/points_{i}.txt"
        points = np.loadtxt(txtpath)
        print(f"Processing {txtpath}")
        print("-" * 32)
        t_start = perf_counter()
        ch = convex_bucket(points)
        t_end = perf_counter()
        print(f"Elapsed time: {t_end - t_start} sec")
        plot_points(points, convex_hull=ch, markersize=20)
        print()
