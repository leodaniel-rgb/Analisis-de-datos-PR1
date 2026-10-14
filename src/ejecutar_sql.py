"""Ejecuta un archivo .sql contra PostgreSQL.

Uso:
    python src/ejecutar_sql.py sql/00_catalogos.sql      # corre el archivo completo
    python src/ejecutar_sql.py sql/01_consultas.sql      # corre cada consulta "-- Qnn" por separado
                                                         # y guarda reports/resultados_consultas.md
"""
import os
import re
import sys
import warnings
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

warnings.filterwarnings("ignore")
RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")
engine = create_engine(
    "postgresql+psycopg2://{u}:{p}@{h}:{port}/{d}".format(
        u=os.getenv("PGUSER"), p=os.getenv("PGPASSWORD"), h=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"), d=os.getenv("PGDATABASE"),
    )
)

ruta = (RAIZ / sys.argv[1]).resolve()
contenido = ruta.read_text(encoding="utf-8")

if "-- Q01" not in contenido:  # script de definicion (catalogos): se ejecuta completo
    with engine.begin() as con:
        con.exec_driver_sql(contenido)
    print(f"OK: {ruta.name} ejecutado")
    # Integridad: toda clave usada en la tabla limpia debe existir en su catalogo.
    checks = {
        "cve_ent": "cat.entidad", "niv_ins": "cat.nivel_instruccion", "rama": "cat.sector",
        "emp_ppal": "cat.formalidad", "sexo": "cat.sexo", "t_loc_tri": "cat.tamano_localidad",
        "pos_ocu": "cat.posicion_ocupacion",
    }
    with engine.connect() as con:
        for col, cat in checks.items():
            n = con.execute(text(
                f"SELECT count(*) FROM clean.ocupados_2026t2 o "
                f"LEFT JOIN {cat} c USING ({col}) WHERE o.{col} IS NOT NULL AND c.{col} IS NULL"
            )).scalar()
            print(f"  integridad {col:10s} -> {cat:25s} claves sin catalogo: {n}")
    sys.exit(0)

# Archivo de consultas: separar por marcadores "-- Qnn | pregunta"
partes = re.split(r"(?m)^-- (Q\d{2}) \|", contenido)
consultas = list(zip(partes[1::2], partes[2::2]))
salida = ["# Resultados de las consultas (ENOE 2T 2026)\n"]
pd.set_option("display.width", 220, "display.max_columns", 30, "display.max_rows", 100)
for clave, cuerpo in consultas:
    lineas = cuerpo.strip().splitlines()
    pregunta = lineas[0].strip()
    # la consulta empieza en la primera linea que no es comentario y llega hasta el ';' final
    inicio = next(i for i, l in enumerate(lineas) if i > 0 and l.strip() and not l.lstrip().startswith("--"))
    sql = "\n".join(lineas[inicio:])
    sql = sql.split("\n------")[0].strip().rstrip(";")
    df = pd.read_sql(text(sql), engine)
    print(f"\n=== {clave} | {pregunta}\n{df.to_string(index=False)}")
    salida.append(f"## {clave} | {pregunta}\n\n```\n{df.to_string(index=False)}\n```\n")

(RAIZ / "reports").mkdir(exist_ok=True)
(RAIZ / "reports" / "resultados_consultas.md").write_text("\n".join(salida), encoding="utf-8")
print(f"\nGuardado reports/resultados_consultas.md ({len(consultas)} consultas)")
