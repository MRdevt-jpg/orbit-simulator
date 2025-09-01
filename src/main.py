from io_cli import (
    read_user_inputs, validate_inputs, format_report,
    ask_yes_no, save_report_with_metadata, format_hohmann_report
)
from orbit_logic import (
    compute_orbit_at_radius,
    build_orbit_points_from_result,
    build_transfer_ellipse_points,
    compute_hohmann_between_circles
)
from visualize import earth_circle_points, plot_orbit, plot_orbit_with_transfer

def demo_fixed_cases() -> None:
    cases = [
        ("LEO ~400 km, Kreis-nah", 400.0, 7.67),
        ("GEO ~35786 km, Kreis", 35786.0, 3.07),
    ]
    for title, h_km, v_kms in cases:
        print(f"\n--- Demo: {title} ---")
        res = compute_orbit_at_radius(h_km, v_kms)
        print(format_report(res))

def main() -> None:
    demo_fixed_cases()

    print("\n=== Eigener Fall ===")
    height_km, speed_kms = read_user_inputs()

    messages = validate_inputs(height_km, speed_kms)
    for msg in messages:
        print(msg)
    if any(m.startswith("FEHLER") for m in messages):
        print("Abbruch wegen fehlerhafter Eingaben.")
        return

    result = compute_orbit_at_radius(height_km, speed_kms)
    print()
    report = format_report(result)
    print(report)

    if ask_yes_no("Report als Datei in 'data/' speichern?"):
        path = save_report_with_metadata(report, height_km, speed_kms, folder="data")
        if path:
            print(f"✓ Gespeichert: {path}")
        else:
            print("✗ Konnte Report nicht speichern.")

    pts = build_orbit_points_from_result(result, num_points=720)
    if pts is None:
        print("Hinweis: Fluchtbahn – keine Ellipse, daher keine Orbitpunkte.")
        return
    earth_pts = earth_circle_points(360)

    make_plot = input("Orbit als Bild plotten? [J/n]: ").strip().lower()
    if make_plot in ("", "j", "y", "yes"):
        from datetime import datetime
        fname = f"orbit_{int(result['input']['height_km'])}km_{result['type']}_" \
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        out_path = f"data/{fname}"
        plot_orbit(pts, earth_pts, title=f"Orbit – {result['type']}", save_path=out_path)
        print(f"✓ Bild gespeichert: {out_path}")

    add_transfer = input("Hohmann-Transferellipse mitplotten? [j/N]: ").strip().lower()
    if add_transfer in ("j", "y", "yes"):
        try:
            target_h = float(input("Zielhöhe [km]: ").strip())
        except ValueError:
            print("Ungültige Eingabe – kein Transfer-Plot.")
        else:
            trans_pts = build_transfer_ellipse_points(result["input"]["height_km"], target_h, num_points=720)
            from datetime import datetime
            fname = (
                f"orbit_transfer_from{int(result['input']['height_km'])}km"
                f"_to{int(target_h)}km_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            out_path = f"data/{fname}"
            plot_orbit_with_transfer(
                pts, trans_pts, earth_pts,
                title=f"Orbit + Hohmann-Transfer ({result['type']} → Kreis@{int(target_h)} km)",
                save_path=out_path
            )
            print(f"✓ Bild gespeichert: {out_path}")

            ho = compute_hohmann_between_circles(result["input"]["height_km"], target_h)
            print()
            print(format_hohmann_report(ho))

if __name__ == "__main__":
    main()
