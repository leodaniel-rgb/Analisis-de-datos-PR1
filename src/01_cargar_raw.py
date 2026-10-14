"""Paso 1: carga el CSV SDEMT 2T 2026 tal cual en PostgreSQL (esquema raw).

Todas las columnas van como TEXT: la tabla cruda es una copia fiel de la fuente.
Los tipos y la limpieza se hacen en el paso siguiente (esquema clean).
"""
import csv
import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "raw" / "enoe_2026_t2" / "ENOE_SDEMT226.csv"
ESQUEMA, TABLA = "raw", "enoe_sdemt_2026t2"
FILAS_ESPERADAS = 417_128  # verificado al inspeccionar el archivo

load_dotenv(RAIZ / ".env")

with open(CSV, newline="", encoding="latin-1") as f:
    columnas = next(csv.reader(f))

con = psycopg2.connect(
    host=os.getenv("PGHOST", "localhost"), port=os.getenv("PGPORT", "5432"),
    dbname=os.getenv("PGDATABASE"), user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
)
try:
    with con, con.cursor() as cur:  # una sola transaccion: o carga todo o nada
        cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(ESQUEMA)))
        destino = sql.Identifier(ESQUEMA, TABLA)
        cur.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(destino))
        cur.execute(sql.SQL("CREATE TABLE {} ({})").format(
            destino,
            sql.SQL(", ").join(sql.SQL("{} TEXT").format(sql.Identifier(c)) for c in columnas),
        ))
        with open(CSV, encoding="latin-1") as f:
            cur.copy_expert(
                sql.SQL("COPY {} FROM STDIN WITH (FORMAT csv, HEADER true)").format(destino).as_string(con),
                f,
            )
        cur.execute(sql.SQL("SELECT count(*) FROM {}").format(destino))
        n = cur.fetchone()[0]
        if n != FILAS_ESPERADAS:
            raise RuntimeError(f"Se cargaron {n} filas, se esperaban {FILAS_ESPERADAS}")
    print(f"OK: {ESQUEMA}.{TABLA} con {n} filas y {len(columnas)} columnas")
except Exception as e:
    print("Fallo:", type(e).__name__, "-", str(e).strip().splitlines()[0])
    sys.exit(1)
finally:
    con.close()
