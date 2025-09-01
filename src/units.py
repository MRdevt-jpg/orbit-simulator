from typing import Union

Number = Union[int, float]

def km_to_m(value_km: Number) -> float:
    return float(value_km) * 1000.0

def m_to_km(value_m: Number) -> float:
    return float(value_m) / 1000.0

def s_to_min(value_s: Number) -> float:
    return float(value_s) / 60.0
