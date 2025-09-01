from typing import Literal, Dict, Any
from constant import MU, R_EARTH
from units import km_to_m, m_to_km, s_to_min
from orbit_core import (
    circular_velocity, escape_velocity,
    semi_major_axis_from_visviva, specific_angular_momentum_tangential,
    eccentricity_from_a_h_mu, periapsis_apapsis, period_from_a,
    hohmann_delta_v, hohmann_transfer_time
)

OrbitType = Literal["circle", "ellipse_high", "ellipse_low", "escape"]

def classify_orbit(v_ms: float, v_circ_ms: float, v_esc_ms: float, eps: float = 0.01) -> OrbitType:
    rel = abs(v_ms - v_circ_ms) / v_circ_ms
    if rel <= eps:
        return "circle"
    if v_ms < v_circ_ms:
        return "ellipse_high"
    if v_ms < v_esc_ms:
        return "ellipse_low"
    return "escape"

def compute_orbit_at_radius(height_km: float, speed_kms: float) -> Dict[str, Any]:
    r_m = R_EARTH + km_to_m(height_km)
    v_ms = speed_kms * 1000.0
    v_circ = circular_velocity(MU, r_m)
    v_esc = escape_velocity(MU, r_m)
    otype: OrbitType = classify_orbit(v_ms, v_circ, v_esc)
    a_m = semi_major_axis_from_visviva(MU, r_m, v_ms)

    result: Dict[str, Any] = {
        "input": {"height_km": height_km, "speed_kms": speed_kms},
        "type": otype,
        "r_m": r_m, "r_km": m_to_km(r_m),
        "v_ms": v_ms, "v_kms": speed_kms,
        "v_circ_ms": v_circ, "v_circ_kms": v_circ/1000.0,
        "v_esc_ms": v_esc, "v_esc_kms": v_esc/1000.0,
        "a_m": a_m, "a_km": m_to_km(a_m),
        "assumptions": "Zentralgravitation; keine Atmosphäre/J2"
    }

    if otype == "escape":
        return result

    h = specific_angular_momentum_tangential(r_m, v_ms)
    e = eccentricity_from_a_h_mu(a_m, h, MU)
    rp_m, ra_m = periapsis_apapsis(a_m, e)
    T_s = period_from_a(MU, a_m)

    result.update({
        "e": e,
        "rp_m": rp_m, "ra_m": ra_m,
        "rp_km": m_to_km(rp_m), "ra_km": m_to_km(ra_m),
        "hp_km": m_to_km(rp_m - R_EARTH),
        "ha_km": m_to_km(ra_m - R_EARTH),
        "period_s": T_s, "period_min": s_to_min(T_s)
    })
    return result

def build_orbit_points_from_result(result: dict, num_points: int = 720):
    if result["type"] == "escape":
        return None
    from visualize import orbit_points
    return orbit_points(result["a_m"], result["e"], num_points=num_points)

def build_transfer_ellipse_points(height_from_km: float, height_to_km: float, num_points: int = 720):
    from visualize import orbit_points
    r1 = R_EARTH + km_to_m(height_from_km)
    r2 = R_EARTH + km_to_m(height_to_km)
    a_t_m = 0.5 * (r1 + r2)
    e_t = abs(r2 - r1) / (r1 + r2)
    return orbit_points(a_t_m, e_t, num_points=num_points)

def compute_hohmann_between_circles(height_from_km: float, height_to_km: float) -> dict:
    r1 = R_EARTH + km_to_m(height_from_km)
    r2 = R_EARTH + km_to_m(height_to_km)
    dv1, dv2, dv_total = hohmann_delta_v(MU, r1, r2)
    t = hohmann_transfer_time(MU, r1, r2)
    return {
        "from_height_km": height_from_km,
        "to_height_km": height_to_km,
        "r1_km": m_to_km(r1),
        "r2_km": m_to_km(r2),
        "dv1_ms": dv1, "dv2_ms": dv2, "dv_total_ms": dv_total,
        "dv1_kms": dv1/1000.0, "dv2_kms": dv2/1000.0, "dv_total_kms": dv_total/1000.0,
        "t_s": t, "t_min": s_to_min(t)
    }
