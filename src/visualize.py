import math
from typing import List, Tuple
from constant import R_EARTH
from units import m_to_km

Point = Tuple[float, float]

def earth_circle_points(num_points: int = 360) -> List[Point]:
    R_km = m_to_km(R_EARTH)
    pts: List[Point] = []
    for i in range(num_points):
        theta = 2.0 * math.pi * (i / num_points)
        x = R_km * math.cos(theta)
        y = R_km * math.sin(theta)
        pts.append((x, y))
    return pts

def orbit_points(a_m: float, e: float, num_points: int = 720) -> List[Point]:
    a_km = m_to_km(a_m)
    pts: List[Point] = []
    e = max(0.0, min(e, 0.999999))
    for i in range(num_points):
        theta = 2.0 * math.pi * (i / num_points)
        denom = 1.0 + e * math.cos(theta)
        if abs(denom) < 1e-12:
            continue
        r_km = a_km * (1.0 - e * e) / denom
        x = r_km * math.cos(theta)
        y = r_km * math.sin(theta)
        pts.append((x, y))
    return pts

def plot_orbit(points_orbit: list[tuple[float, float]],
               points_earth: list[tuple[float, float]],
               title: str = "Orbit (km)",
               save_path: str | None = None) -> None:
    import matplotlib.pyplot as plt

    xs_o = [p[0] for p in points_orbit]
    ys_o = [p[1] for p in points_orbit]
    xs_e = [p[0] for p in points_earth]
    ys_e = [p[1] for p in points_earth]

    plt.figure()
    plt.plot(xs_e, ys_e, label="Erde")
    plt.plot(xs_o, ys_o, label="Orbit")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel("x (km)")
    plt.ylabel("y (km)")
    plt.title(title)
    plt.legend()
    plt.grid(True)

    import os
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=160, bbox_inches="tight")
        print(f"[DEBUG] Gespeichert unter: {os.path.abspath(save_path)}")
    else:
        plt.show()

    plt.close()

def plot_orbit_with_transfer(points_orbit: list[tuple[float, float]],
                             points_transfer: list[tuple[float, float]],
                             points_earth: list[tuple[float, float]],
                             title: str = "Orbit + Transfer (km)",
                             save_path: str | None = None) -> None:
    import matplotlib.pyplot as plt

    xs_e = [p[0] for p in points_earth]
    ys_e = [p[1] for p in points_earth]
    xs_o = [p[0] for p in points_orbit]
    ys_o = [p[1] for p in points_orbit]
    xs_t = [p[0] for p in points_transfer]
    ys_t = [p[1] for p in points_transfer]

    plt.figure()
    plt.plot(xs_e, ys_e, label="Erde")
    plt.plot(xs_o, ys_o, label="Ausgangsorbit")
    plt.plot(xs_t, ys_t, label="Transferellipse")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("x (km)")
    plt.ylabel("y (km)")
    plt.title(title)
    plt.legend()
    plt.grid(True)

    import os

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=160, bbox_inches="tight")
        print(f"[DEBUG] Gespeichert unter: {os.path.abspath(save_path)}")
    else:
        plt.show()

    plt.close()
