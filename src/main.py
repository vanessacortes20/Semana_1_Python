from __future__ import annotations

from pathlib import Path
import pandas as pd

from limpieza import limpiar_dataset


BASE_DIR = Path(__file__).resolve().parents[1]  # raíz del repo
RAW_PATH = BASE_DIR / "data" / "raw" / "ocupacion_y_desempleo.csv"
OUT_PATH = BASE_DIR / "data" / "processed" / "ocupacion_y_desempleo_limpio.csv"


def cargar_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")

    # Intento robusto de lectura (por si viene en latin-1)
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")


def main() -> None:
    df = cargar_csv(RAW_PATH)
    df_limpio, rep = limpiar_dataset(df)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_limpio.to_csv(OUT_PATH, index=False)

    print("OK - Dataset limpio guardado en:", OUT_PATH)
    print(rep)


if __name__ == "__main__":
    main()
