from typing import Tuple, List, Dict, Any, Optional
import os
from datetime import datetime

def read_user_inputs() -> Tuple[float, float]:
    height_km = float(input("Höhe über Erdoberfläche [km]: ").strip())
    speed_kms = float(input("Startgeschwindigkeit [km/s]: ").strip())
    return height_km, speed_kms

def validate_inputs(height_km: float, speed_kms: float) -> List[str]:
    msgs: List[str] = []
    if height_km < 0:
        msgs.append("FEHLER: Höhe muss ≥ 0 km sein.")
    if speed_kms <= 0:
        msgs.append("FEHLER: Geschwindigkeit muss > 0 km/s sein.")
    if height_km < 120:
        msgs.append("WARNUNG: Höhe < 120 km – Atmosphäre nicht modelliert, Wiedereintritt wahrscheinlich.")
    return msgs

def format_report(result: Dict[str, Any]) -> str:
    lines: List[str] = []
    inp = result["input"]
    lines.append("=== Orbit-Report ===")
    lines.append(f"Eingabe: Höhe {inp['height_km']:.0f} km, v {inp['speed_kms']:.2f} km/s")
    lines.append(f"Typ: {result['type']}")
    lines.append(f"Referenz: v_kreis {result['v_circ_kms']:.2f} km/s, v_flucht {result['v_esc_kms']:.2f} km/s")
    lines.append(f"a: {result['a_km']:.0f} km")
    if result["type"] != "escape":
        lines.append(f"Perigäum: {result['hp_km']:.0f} km   Apogäum: {result['ha_km']:.0f} km")
        lines.append(f"Umlaufzeit: {result['period_min']:.1f} min")
    lines.append(f"Annahmen: {result['assumptions']}")
    return "\n".join(lines)

def ask_yes_no(prompt: str, default: bool = True) -> bool:
    suffix = " [J/n]: " if default else " [j/N]: "
    ans = input(prompt + suffix).strip().lower()
    if ans == "":
        return default
    return ans.startswith("j") or ans in ("y", "yes")

def build_report_filename(height_km: float, speed_kms: float) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    hk = f"{height_km:.0f}"
    vk = f"{speed_kms:.2f}".replace(".", "p")
    return f"run_{ts}_height{hk}km_speed{vk}kms.txt"

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def save_report_text(text: str, folder: str = "data") -> Optional[str]:
    try:
        ensure_dir(folder)
        fname = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        fpath = os.path.join(folder, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(text)
        return fpath
    except Exception as exc:
        print(f"Fehler beim Speichern: {exc}")
        return None

def save_report_with_metadata(text: str, height_km: float, speed_kms: float, folder: str = "data") -> Optional[str]:
    try:
        ensure_dir(folder)
        fname = build_report_filename(height_km, speed_kms)
        fpath = os.path.join(folder, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(text)
        return fpath
    except Exception as exc:
        print(f"Fehler beim Speichern: {exc}")
        return None

def format_hohmann_report(info: dict) -> str:
    lines = []
    lines.append("=== Hohmann-Transfer ===")
    lines.append(f"Von: {info['from_height_km']:.0f} km  →  Nach: {info['to_height_km']:.0f} km")
    lines.append(f"Kreisradien: r1={info['r1_km']:.0f} km, r2={info['r2_km']:.0f} km")
    lines.append(f"Δv1: {info['dv1_ms']:.1f} m/s ({info['dv1_kms']:.3f} km/s)")
    lines.append(f"Δv2: {info['dv2_ms']:.1f} m/s ({info['dv2_kms']:.3f} km/s)")
    lines.append(f"Δv_total: {info['dv_total_ms']:.1f} m/s ({info['dv_total_kms']:.3f} km/s)")
    lines.append(f"Transferzeit: {info['t_min']:.1f} min ({info['t_s']:.0f} s)")
    return "\n".join(lines)
