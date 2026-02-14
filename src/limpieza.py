from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

import pandas as pd


@dataclass(frozen=True)
class LimpiezaReporte:
    filas_iniciales: int
    filas_finales: int
    columnas_iniciales: int
    columnas_finales: int
    nulos_antes: int
    nulos_despues: int


def normalizar_nombres_columnas(columns: Iterable[str]) -> list[str]:
    return [
        str(c)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        for c in columns
    ]


def recortar_texto(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    obj_cols = out.select_dtypes(include=["object"]).columns
    for c in obj_cols:
        out[c] = out[c].astype(str).str.strip()
    return out


def convertir_numericos(df: pd.DataFrame, cols: Optional[Iterable[str]] = None) -> pd.DataFrame:
    out = df.copy()
    target_cols = list(cols) if cols is not None else out.columns.tolist()
    for c in target_cols:
        if c in out.columns:
            if out[c].dtype == "object":
                s = (
                    out[c]
                    .astype(str)
                    .str.replace(".", "", regex=False)   # separador miles típico
                    .str.replace(",", ".", regex=False)  # decimal típico
                )
                out[c] = pd.to_numeric(s, errors="ignore")
    return out


def quitar_filas_vacias(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(how="all").copy()


def imputacion_simple(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Numéricas: imputar con mediana
    - Categóricas: imputar con moda (o 'desconocido' si no hay moda)
    """
    out = df.copy()

    num_cols = out.select_dtypes(include=["number"]).columns
    for c in num_cols:
        if out[c].isna().any():
            out[c] = out[c].fillna(out[c].median())

    obj_cols = out.select_dtypes(include=["object"]).columns
    for c in obj_cols:
        if out[c].isna().any():
            moda = out[c].mode(dropna=True)
            fill = moda.iloc[0] if len(moda) else "desconocido"
            out[c] = out[c].fillna(fill)

    return out


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().copy()


def limpiar_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, LimpiezaReporte]:
    filas_i, cols_i = df.shape
    nulos_i = int(df.isna().sum().sum())

    out = df.copy()
    out.columns = normalizar_nombres_columnas(out.columns)
    out = quitar_filas_vacias(out)
    out = recortar_texto(out)
    out = convertir_numericos(out)          # intenta convertir strings numéricas
    out = imputacion_simple(out)
    out = eliminar_duplicados(out)

    filas_f, cols_f = out.shape
    nulos_f = int(out.isna().sum().sum())

    rep = LimpiezaReporte(
        filas_iniciales=filas_i,
        filas_finales=filas_f,
        columnas_iniciales=cols_i,
        columnas_finales=cols_f,
        nulos_antes=nulos_i,
        nulos_despues=nulos_f,
    )
    return out, rep
