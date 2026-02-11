from __future__ import annotations

from pathlib import Path
import random
import pandas as pd


def generate_gym_habits(n: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = random.Random(seed)

    actividades = ["cardio", "pesas", "piernas", "brazos", "espalda", "full body", "hiit"]
    intensidades = ["baja", "media", "alta"]
    notas_pool = ["", "buena sesion", "muy pesado", "cansado", "dolor leve", "excelente", None]

    base_dates = pd.date_range("2026-01-01", periods=40, freq="D").to_pydatetime().tolist()

    rows = []
    for _ in range(n):
        dt = rng.choice(base_dates)
        actividad = rng.choice(actividades)
        intensidad = rng.choice(intensidades)

        # Duración: a veces numérico, a veces string con espacios
        dur = rng.choice([25, 30, 35, 40, 45, 50, 55, 60, 70, 75])
        duracion_min = str(dur) if rng.random() < 0.25 else dur
        if rng.random() < 0.15:
            duracion_min = f" {duracion_min} "  # espacios

        # Peso: a veces vacío, a veces con "kg"
        peso_val = round(rng.uniform(66, 75), 1)
        if rng.random() < 0.12:
            peso = ""  # missing
        else:
            peso = f"{peso_val}kg" if rng.random() < 0.18 else peso_val

        # Reps/series: más comunes en pesas
        if actividad in {"pesas", "piernas", "brazos", "espalda", "full body"}:
            reps = rng.choice([6, 8, 10, 12, 15, 20])
            series = rng.choice([3, 4, 5])
            # a veces missing
            if rng.random() < 0.08:
                reps = ""
            if rng.random() < 0.08:
                series = ""
        else:
            reps = ""
            series = ""

        # Notas: a veces None o vacío
        notas = rng.choice(notas_pool)

        # Fechas en formatos mixtos intencionales
        fecha_formats = [
            dt.strftime("%Y-%m-%d"),
            dt.strftime("%d/%m/%Y"),
            dt.strftime("%m/%d/%Y"),
            dt.strftime("%Y/%m/%d"),
            dt.strftime("%d-%m-%Y"),
        ]
        fecha = rng.choice(fecha_formats)

        # Strings con espacios intencionales
        if rng.random() < 0.20:
            actividad = f"  {actividad} "

        rows.append(
            {
                "fecha": fecha,
                "actividad": actividad,
                "duracion_min": duracion_min,
                "peso": peso,
                "reps": reps,
                "series": series,
                "intensidad": intensidad,
                "notas": notas,
            }
        )

    df = pd.DataFrame(rows)

    # Duplicados intencionales (2% de filas duplicadas)
    dup_count = max(1, int(0.02 * n))
    df = pd.concat([df, df.sample(dup_count, random_state=seed)], ignore_index=True)

    return df


def save_csv(df: pd.DataFrame, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    df = generate_gym_habits(n=200, seed=42)
    out_path = save_csv(df, "data/raw/gym_habits.csv")
    print(f"CSV generado: {out_path.resolve()}")
    print(df.head(10))
