from time import perf_counter

import numpy as np
from numpy.typing import NDArray
from typing import Tuple

from src.plotting import plot_points


# orientation of a trio of points
def orientation(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]) -> bool:
    """
    to determine the orientation, the determinant of the 3x3 matrix, composed of the coordinates of the points, is used
        | a[0] a[1] 1 |
    det=| b[0] b[1] 1 |
        | c[0] c[1] 1 |
    when det = 0, it means that all points lie on the same lines
    when det > 0, it means that they form a clockwise rotation
    when det < 0, it means that they form a counterclockwise rotation
    """
    val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
    if val >= 0:
        return True
    return False


def convex_bucket(points: NDArray) -> NDArray:
    """Complexity: O(n log n)"""
    # sort all points by x-coordinate and if two points have the same x, sort this points by y-coordinate
    points = sorted(points, key=lambda p: (p[0], p[1]))

    # convex bucket algorithm
    clockwise_sorted_ch = [points[0], points[1]]
    for p in points[2:]:
        while len(clockwise_sorted_ch) > 1 and orientation(clockwise_sorted_ch[-2], clockwise_sorted_ch[-1], p):
            clockwise_sorted_ch.pop()
        clockwise_sorted_ch.append(p)

    # avoid cycle
    clockwise_sorted_ch += clockwise_sorted_ch[-2::-1]

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
