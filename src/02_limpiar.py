"""Paso 2: limpia raw.enoe_sdemt_2026t2 con pandas y crea clean.ocupados_2026t2.

Una fila = una persona ocupada de 15 anios o mas, con factor de expansion valido.
Cada filtro y cada decision se documenta en reports/limpieza_log.txt.
"""
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")
engine = create_engine(
    "postgresql+psycopg2://{u}:{p}@{h}:{port}/{d}".format(
        u=os.getenv("PGUSER"), p=os.getenv("PGPASSWORD"), h=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"), d=os.getenv("PGDATABASE"),
    )
)

log = []


def anota(msg):
    print(msg)
    log.append(msg)


# --- 1. Leer solo las columnas necesarias (todas llegan como texto) -------------------------
COLS = ["cve_ent", "con", "v_sel", "n_hog", "h_mud", "n_ent", "n_ren", "n_pro_viv", "tipo",
        "upm", "est_d_tri", "t_loc_tri", "c_res", "r_def", "sex", "eda", "clase2", "pos_ocu",
        "rama", "niv_ins", "anios_esc", "ingocup", "ing7c", "hrsocup", "ing_x_hrs",
        "emp_ppal", "tue_ppal", "fac_tri"]
raw = pd.read_sql(f"SELECT {', '.join(COLS)} FROM raw.enoe_sdemt_2026t2", engine)
anota(f"1. Filas en raw: {len(raw):,}")

# --- 2. Tipos: blancos (' ') -> NaN y despues a numerico -----------------------------------
# Las columnas llegan como texto y los 'nulos' son espacios en blanco, no NULL.
NUM = ["eda", "anios_esc", "ingocup", "hrsocup", "ing_x_hrs", "fac_tri"]
for c in NUM:
    raw[c] = pd.to_numeric(raw[c].str.strip().replace("", np.nan), errors="raise")
CAT = [c for c in COLS if c not in NUM]
for c in CAT:
    raw[c] = raw[c].str.strip()

# --- 3. Duplicados: llave unica de persona (+ tipo de muestra) ------------------------------
llave = ["cve_ent", "con", "v_sel", "n_hog", "h_mud", "n_ent", "n_ren", "n_pro_viv", "tipo"]
anota(f"2. Duplicados exactos: {raw.duplicated().sum()} | duplicados por llave de persona: {raw.duplicated(llave).sum()}")
assert not raw.duplicated(llave).any()

# --- 4. Poblacion objetivo: fac_tri > 0, 15+ anios, ocupados --------------------------------
n0 = len(raw)
df = raw[raw["fac_tri"] > 0]
anota(f"3. Con fac_tri > 0 (residentes con entrevista completa): {len(df):,}  (se excluyen {n0 - len(df):,})")
n1 = len(df)
df = df[df["eda"] >= 15]
anota(f"4. De 15 anios o mas: {len(df):,}  (se excluyen {n1 - len(df):,})")
n2 = len(df)
df = df[df["clase2"] == "1"].copy()
anota(f"5. Poblacion ocupada (clase2 = 1): {len(df):,}  (se excluyen {n2 - len(df):,})")
anota(f"   Poblacion ocupada expandida: {df['fac_tri'].sum() / 1e6:.2f} millones (INEGI publica 60.0 millones)")

# --- 5. Codigos de 'no especificado' -> NaN --------------------------------------------------
n99 = (df["anios_esc"] == 99).sum()
df.loc[df["anios_esc"] == 99, "anios_esc"] = np.nan
anota(f"6. anios_esc = 99 (no especificado) -> NULL: {n99:,}")
for col, cod in [("rama", "7"), ("pos_ocu", "5"), ("niv_ins", "5")]:
    n = (df[col] == cod).sum()
    df.loc[df[col] == cod, col] = np.nan
    anota(f"   {col} = {cod} (no especificado) -> NULL: {n:,}")
for col in ["emp_ppal", "tue_ppal"]:
    assert df[col].isin(["1", "2"]).all(), f"{col} trae codigos inesperados en ocupados"

# --- 6. Regla de ingresos (acordada): ingocup > 0 es ingreso declarado en pesos --------------
# ing7c: 1-5 rango de salarios minimos, 6 no recibe ingresos, 7 no especificado.
df["tipo_ingreso"] = np.select(
    [df["ingocup"] > 0, df["ing7c"] == "6", df["ing7c"] == "7"],
    ["monto_declarado", "no_recibe", "no_especificado"],
    default="solo_rango",
)
df["ingocup_pesos"] = df["ingocup"].where(df["ingocup"] > 0)
df["ing_x_hrs_pesos"] = df["ing_x_hrs"].where(df["ingocup"] > 0)
w = df.groupby("tipo_ingreso")["fac_tri"].agg(["size", "sum"])
w["pct_muestra"] = 100 * w["size"] / w["size"].sum()
w["pct_ponderado"] = 100 * w["sum"] / w["sum"].sum()
anota("7. Tipo de ingreso (muestra y ponderado):\n" + w.round(1).to_string())

# --- 7. Rangos plausibles ---------------------------------------------------------------------
anota(f"8. hrsocup: min {df['hrsocup'].min():.0f}, max {df['hrsocup'].max():.0f} | "
      f"ingocup_pesos: min {df['ingocup_pesos'].min():.0f}, max {df['ingocup_pesos'].max():.0f}")

# --- 8. Armar tabla final con tipos explicitos ------------------------------------------------
df["id_persona"] = df[llave].agg("-".join, axis=1)
out = pd.DataFrame({
    "id_persona": df["id_persona"],
    "cve_ent": df["cve_ent"].astype(int).astype("int16"),
    "sexo": df["sex"].astype(int).astype("int16"),
    "edad": df["eda"].astype(int).astype("int16"),
    "anios_esc": df["anios_esc"].astype("Int16"),
    "niv_ins": pd.to_numeric(df["niv_ins"]).astype("Int16"),
    "rama": pd.to_numeric(df["rama"]).astype("Int16"),
    "pos_ocu": pd.to_numeric(df["pos_ocu"]).astype("Int16"),
    "emp_ppal": df["emp_ppal"].astype(int).astype("int16"),
    "tue_ppal": df["tue_ppal"].astype(int).astype("int16"),
    "ing7c": df["ing7c"].astype(int).astype("int16"),
    "tipo_ingreso": df["tipo_ingreso"],
    "ingocup_pesos": df["ingocup_pesos"],
    "ing_x_hrs_pesos": df["ing_x_hrs_pesos"],
    "hrsocup": df["hrsocup"].astype(int).astype("int16"),
    "t_loc_tri": df["t_loc_tri"].astype(int).astype("int16"),
    "est_d_tri": df["est_d_tri"].astype(int).astype("int16"),
    "upm": df["upm"],
    "fac_tri": df["fac_tri"].astype(int),
})
assert out["id_persona"].is_unique and out["fac_tri"].gt(0).all()

DDL = """
DROP TABLE IF EXISTS clean.ocupados_2026t2;
CREATE SCHEMA IF NOT EXISTS clean;
CREATE TABLE clean.ocupados_2026t2 (
    id_persona      TEXT PRIMARY KEY,
    cve_ent         SMALLINT NOT NULL CHECK (cve_ent BETWEEN 1 AND 32),
    sexo            SMALLINT NOT NULL CHECK (sexo IN (1, 2)),
    edad            SMALLINT NOT NULL CHECK (edad >= 15),
    anios_esc       SMALLINT,
    niv_ins         SMALLINT,
    rama            SMALLINT,
    pos_ocu         SMALLINT,
    emp_ppal        SMALLINT NOT NULL CHECK (emp_ppal IN (1, 2)),
    tue_ppal        SMALLINT NOT NULL CHECK (tue_ppal IN (1, 2)),
    ing7c           SMALLINT NOT NULL,
    tipo_ingreso    TEXT NOT NULL,
    ingocup_pesos   NUMERIC,
    ing_x_hrs_pesos NUMERIC,
    hrsocup         SMALLINT NOT NULL,
    t_loc_tri       SMALLINT NOT NULL,
    est_d_tri       SMALLINT NOT NULL,
    upm             TEXT NOT NULL,
    fac_tri         INTEGER NOT NULL CHECK (fac_tri > 0)
);
"""
with engine.begin() as con:
    for stmt in DDL.strip().split(";"):
        if stmt.strip():
            con.execute(text(stmt))
    out.to_sql("ocupados_2026t2", con, schema="clean", if_exists="append",
               index=False, method="multi", chunksize=5000)
    n = con.execute(text("SELECT count(*) FROM clean.ocupados_2026t2")).scalar()
assert n == len(out), "la tabla cargada no coincide con el DataFrame"
anota(f"9. clean.ocupados_2026t2 cargada: {n:,} filas, {out.shape[1]} columnas")

(RAIZ / "reports").mkdir(exist_ok=True)
(RAIZ / "reports" / "limpieza_log.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
