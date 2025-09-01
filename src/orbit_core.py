import math

def circular_velocity(mu: float, r_m: float) -> float:
    return math.sqrt(mu / r_m)

def escape_velocity(mu: float, r_m: float) -> float:
    return math.sqrt(2.0 * mu / r_m)

def semi_major_axis_from_visviva(mu: float, r_m: float, v_ms: float) -> float:
    inv_a = (2.0 / r_m) - (v_ms * v_ms) / mu
    return 1.0 / inv_a if inv_a != 0.0 else float("inf")

def specific_angular_momentum_tangential(r_m: float, v_ms: float) -> float:
    return r_m * v_ms

def eccentricity_from_a_h_mu(a_m: float, h: float, mu: float) -> float:
    val = 1.0 - (h * h) / (a_m * mu)
    val = max(val, 0.0)
    return math.sqrt(val)

def periapsis_apapsis(a_m: float, e: float) -> tuple[float, float]:
    rp = a_m * (1.0 - e)
    ra = a_m * (1.0 + e)
    return rp, ra

def period_from_a(mu: float, a_m: float) -> float:
    return 2.0 * math.pi * math.sqrt((a_m ** 3) / mu)

def hohmann_delta_v(mu: float, r1_m: float, r2_m: float) -> tuple[float, float, float]:
    v1_c = math.sqrt(mu / r1_m)
    v2_c = math.sqrt(mu / r2_m)
    a_t = 0.5 * (r1_m + r2_m)
    v_p = math.sqrt(mu * (2.0 / r1_m - 1.0 / a_t))
    v_a = math.sqrt(mu * (2.0 / r2_m - 1.0 / a_t))
    dv1 = abs(v_p - v1_c)
    dv2 = abs(v2_c - v_a)
    return dv1, dv2, dv1 + dv2

def hohmann_transfer_time(mu: float, r1_m: float, r2_m: float) -> float:
    a_t = 0.5 * (r1_m + r2_m)
    return math.pi * math.sqrt((a_t ** 3) / mu)
