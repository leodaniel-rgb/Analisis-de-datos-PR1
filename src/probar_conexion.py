import os, sys
from dotenv import load_dotenv
import psycopg2

load_dotenv()
try:
    con = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"), port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"),
        connect_timeout=5)
    cur = con.cursor()
    cur.execute("select current_database(), current_user, version()")
    db, user, ver = cur.fetchone()
    print("Conexion exitosa:", db, "|", user, "|", ver.split(",")[0])
    con.close()
except Exception as e:
    print("Fallo:", type(e).__name__, "-", str(e).strip().splitlines()[0])
    sys.exit(1)
