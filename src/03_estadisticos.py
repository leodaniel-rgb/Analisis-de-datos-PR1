"""Paso 6a: media, mediana y percentiles ponderados, con intervalos de confianza al 95 %.

Metodo (diseno muestral de la ENOE: estratos = est_d_tri, UPM = upm, peso = fac_tri):
  * Medias y proporciones: razon ponderada + varianza por conglomerados ultimos
    (linealizacion de Taylor), el enfoque que INEGI describe para sus precisiones.
  * Percentiles: no tienen formula cerrada simple -> bootstrap reescalado de Rao-Wu
    (remuestreo de UPM dentro de cada estrato, n_h - 1 extracciones).
  * Estratos con una sola UPM (13): se fusionan con el estrato mas cercano de la misma entidad.
  * Los dominios (SLP, grupos) se estiman con TODAS las UPM del diseno, no con submuestras.
Guarda reports/estadisticos.md y data/interim/estadisticos.pkl (usado por 04_graficas.py).
"""
import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

warnings.filterwarnings("ignore")
RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")
engine = create_engine(
    "postgresql+psycopg2://{u}:{p}@{h}:{port}/{d}".format(
        u=os.getenv("PGUSER"), p=os.getenv("PGPASSWORD"), h=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"), d=os.getenv("PGDATABASE"),
    )
)
B, SEMILLA, Z = 500, 20260713, 1.96
PCTS = [0.10, 0.25, 0.50, 0.75, 0.90]
NIV = {1: "Primaria incompleta", 2: "Primaria completa", 3: "Secundaria completa", 4: "Medio superior y superior"}
RAMA = {1: "Construcción", 2: "Industria manufacturera", 3: "Comercio", 4: "Servicios", 5: "Otros", 6: "Agropecuario"}

d = pd.read_sql("SELECT cve_ent, niv_ins, rama, emp_ppal, ingocup_pesos, est_d_tri, upm, fac_tri "
                "FROM clean.ocupados_2026t2", engine)
w = d["fac_tri"].to_numpy(float)
inf = (d["emp_ppal"] == 1).to_numpy(float)
ing = d["ingocup_pesos"].to_numpy(float)
tiene_ing = ~np.isnan(ing)

# --- 1. Estructura del diseno: fusionar estratos con una sola UPM -------------------------------
estrato = d["est_d_tri"].astype(int).to_numpy().copy()
upm_por_est = d.groupby("est_d_tri")["upm"].nunique()
solos = upm_por_est[upm_por_est == 1].index.astype(int).tolist()
ent_est = d.groupby("est_d_tri")["cve_ent"].first()
for s in solos:
    ent = ent_est[s]
    mismos = [e for e in ent_est.index[ent_est == ent] if e != s and e not in solos]
    candidatos = mismos or [e for e in ent_est.index if e != s and e not in solos]
    destino = min(candidatos, key=lambda e: abs(e - s))
    estrato[estrato == s] = destino
print(f"Estratos con una UPM fusionados: {len(solos)}")

psu_codes, psu_unicos = pd.factorize(d["upm"])
P = len(psu_unicos)
h_codes, _ = pd.factorize(estrato)
psu_h = np.zeros(P, dtype=int)
psu_h[psu_codes] = h_codes                      # estrato de cada UPM
H = psu_h.max() + 1
n_h = np.bincount(psu_h, minlength=H).astype(float)
assert (n_h >= 2).all(), "quedan estratos con una sola UPM"
inicio_h = np.concatenate([[0], np.cumsum(n_h)[:-1]]).astype(int)
orden = np.argsort(psu_h, kind="stable")
psu_pos = np.empty(P, dtype=int)
psu_pos[orden] = np.arange(P)                    # posicion de la UPM ordenada por estrato
psu_codes_ord = psu_pos[psu_codes]               # UPM de cada fila en el orden por estrato
psu_h_ord = psu_h[orden]


def varianza_conglomerados(u):
    """Varianza de un total linealizado u (por fila) con conglomerados ultimos."""
    tot = np.bincount(psu_codes_ord, weights=u, minlength=P)
    media_h = np.bincount(psu_h_ord, weights=tot, minlength=H) / n_h
    desv = tot - media_h[psu_h_ord]
    return float(np.sum(n_h[psu_h_ord] / (n_h[psu_h_ord] - 1) * desv ** 2))


def razon(y, dom):
    """Estimador de razon sum(w*y*dom)/sum(w*dom) y su valor linealizado u por fila."""
    wd = w * dom
    r = np.sum(wd * y) / np.sum(wd)
    u = wd * (y - r) / np.sum(wd)
    return r, u


# --- 2. Dominios ---------------------------------------------------------------------------------
slp = (d["cve_ent"] == 24).to_numpy()
ambitos = {"Nacional": np.ones(len(d), bool), "San Luis Potosí": slp, "Resto del país": ~slp}
grupos = {("Total", "Todos"): np.ones(len(d), bool)}
grupos.update({("Escolaridad", NIV[k]): (d["niv_ins"] == k).to_numpy() for k in NIV})
grupos.update({("Sector", RAMA[k]): (d["rama"] == k).to_numpy() for k in RAMA})
dominios = {(a, t, g): ma & mg for a, ma in ambitos.items() for (t, g), mg in grupos.items()}

# --- 3. Medias y proporciones (Taylor) -----------------------------------------------------------
filas, lin = [], {}
for (a, t, g), m in dominios.items():
    dom_inf = m.astype(float)
    p, u_p = razon(inf, dom_inf)
    dom_ing = (m & tiene_ing).astype(float)
    mu, u_mu = razon(np.nan_to_num(ing), dom_ing)
    lin[(a, t, g)] = (u_p, u_mu)
    se_p, se_mu = np.sqrt(varianza_conglomerados(u_p)), np.sqrt(varianza_conglomerados(u_mu))
    filas.append({
        "ambito": a, "tipo": t, "grupo": g,
        "n_ocupados": int(m.sum()), "poblacion": float(np.sum(w[m])),
        "pct_informal": 100 * p, "pct_informal_ee": 100 * se_p,
        "n_ingreso": int((m & tiene_ing).sum()), "ingreso_medio": mu, "ingreso_medio_ee": se_mu,
    })
res = pd.DataFrame(filas)

# --- 4. Percentiles ponderados: estimacion + bootstrap Rao-Wu ------------------------------------
claves = list(dominios.keys())
idx_orden = {}
for k in claves:
    ii = np.where(dominios[k] & tiene_ing)[0]
    idx_orden[k] = ii[np.argsort(ing[ii], kind="stable")]


def percentiles(pesos):
    out = {}
    for k in claves:
        ii = idx_orden[k]
        if len(ii) == 0:
            out[k] = [np.nan] * len(PCTS)
            continue
        cum = np.cumsum(pesos[ii])
        pos = np.minimum(np.searchsorted(cum, np.array(PCTS) * cum[-1]), len(ii) - 1)
        out[k] = ing[ii][pos].tolist()
    return out


punto = percentiles(w)
rng = np.random.default_rng(SEMILLA)
h_sorteo = np.repeat(np.arange(H), (n_h - 1).astype(int))
factor_h = n_h / (n_h - 1)
boot = {k: np.empty((B, len(PCTS))) for k in claves}
for b in range(B):
    elegida = inicio_h[h_sorteo] + (rng.random(len(h_sorteo)) * n_h[h_sorteo]).astype(int)
    veces = np.bincount(elegida, minlength=P)                    # veces que sale cada UPM (en orden)
    mult = factor_h[psu_h_ord] * veces
    pb = percentiles(w * mult[psu_codes_ord])
    for k in claves:
        boot[k][b] = pb[k]
print(f"Bootstrap Rao-Wu: {B} replicas")

nombres_p = [f"p{int(q * 100)}" for q in PCTS]
for j, nm in enumerate(nombres_p):
    res[nm] = [punto[k][j] for k in claves]
    res[nm + "_lo"] = [np.percentile(boot[k][:, j], 2.5) for k in claves]
    res[nm + "_hi"] = [np.percentile(boot[k][:, j], 97.5) for k in claves]

res["pct_informal_lo"] = res["pct_informal"] - Z * res["pct_informal_ee"]
res["pct_informal_hi"] = res["pct_informal"] + Z * res["pct_informal_ee"]
res["ingreso_medio_lo"] = res["ingreso_medio"] - Z * res["ingreso_medio_ee"]
res["ingreso_medio_hi"] = res["ingreso_medio"] + Z * res["ingreso_medio_ee"]
res["cv_ingreso_medio"] = 100 * res["ingreso_medio_ee"] / res["ingreso_medio"]
res["cv_pct_informal"] = res["pct_informal_ee"] / res["pct_informal"] * 100

# --- 5. Diferencias SLP - Resto del pais --------------------------------------------------------
dif = []
for (t, g) in grupos:
    ks, kr = ("San Luis Potosí", t, g), ("Resto del país", t, g)
    (up_s, um_s), (up_r, um_r) = lin[ks], lin[kr]
    r = res.set_index(["ambito", "tipo", "grupo"])
    d_p = r.loc[ks, "pct_informal"] - r.loc[kr, "pct_informal"]
    se_p = 100 * np.sqrt(varianza_conglomerados(up_s - up_r))
    d_mu = r.loc[ks, "ingreso_medio"] - r.loc[kr, "ingreso_medio"]
    se_mu = np.sqrt(varianza_conglomerados(um_s - um_r))
    j = nombres_p.index("p50")
    d_med = punto[ks][j] - punto[kr][j]
    dm_b = boot[ks][:, j] - boot[kr][:, j]
    dif.append({"tipo": t, "grupo": g,
                "dif_pct_informal": d_p, "dif_pct_informal_lo": d_p - Z * se_p, "dif_pct_informal_hi": d_p + Z * se_p,
                "dif_ingreso_medio": d_mu, "dif_ingreso_medio_lo": d_mu - Z * se_mu, "dif_ingreso_medio_hi": d_mu + Z * se_mu,
                "dif_mediana": d_med, "dif_mediana_lo": np.percentile(dm_b, 2.5), "dif_mediana_hi": np.percentile(dm_b, 97.5),
                "n_ingreso_slp": int(r.loc[ks, "n_ingreso"])})
dif = pd.DataFrame(dif)

# --- 6. Verificacion: Taylor vs bootstrap para la media nacional de ingreso ---------------------
k = ("Nacional", "Total", "Todos")
mb = []
rng2 = np.random.default_rng(SEMILLA + 1)
for b in range(200):
    elegida = inicio_h[h_sorteo] + (rng2.random(len(h_sorteo)) * n_h[h_sorteo]).astype(int)
    mult = factor_h[psu_h_ord] * np.bincount(elegida, minlength=P)
    wb = w * mult[psu_codes_ord]
    m = tiene_ing
    mb.append(np.sum(wb[m] * ing[m]) / np.sum(wb[m]))
ee_t = res.loc[(res.ambito == k[0]) & (res.tipo == k[1]), "ingreso_medio_ee"].iloc[0]
print(f"Verificacion EE de la media nacional de ingreso: Taylor {ee_t:.1f} vs bootstrap {np.std(mb, ddof=1):.1f}")

# --- 7. Guardar ----------------------------------------------------------------------------------
(RAIZ / "data" / "interim").mkdir(parents=True, exist_ok=True)
pd.to_pickle({"res": res, "dif": dif, "B": B}, RAIZ / "data" / "interim" / "estadisticos.pkl")


def f0(x):
    return f"{x:,.0f}"


def tabla(df, cols, encabezados):
    out = ["| " + " | ".join(encabezados) + " |", "|" + "|".join(["---"] * len(encabezados)) + "|"]
    out += ["| " + " | ".join(str(c(r)) for c in cols) + " |" for _, r in df.iterrows()]
    return "\n".join(out)


md = ["# Estadísticos con intervalos de confianza al 95 % (ENOE 2T 2026)\n",
      "Ingreso: solo ocupados con monto declarado (`ingocup > 0`). Medias y proporciones: varianza por conglomerados "
      "últimos (Taylor). Percentiles: bootstrap Rao-Wu con %d réplicas. `n` = observaciones de la muestra; "
      "celdas con n < 100 son poco confiables (criterio de este proyecto).\n",
      "**Cómo leer este reporte**\n",
      "- Los ingresos se concentran en pocos valores repetidos (p. ej. 8,600 y 12,900). Cuando una mediana cae sobre uno de "
      "ellos, su intervalo bootstrap puede reducirse a un solo valor (p. ej. 10,750–10,750): eso **no** es precisión alta, "
      "es un efecto de la concentración de valores. Para comparar ingresos se prefiere la **media**, cuyo intervalo no depende de ello.",
      "- Se comparan 11 grupos en 3 indicadores (33 pruebas). Con 95 % de confianza se esperan ~1.6 resultados ✔ por azar; "
      "los ✔ con un límite del intervalo muy cerca de 0 deben tomarse con cautela.",
      "- *Resto del país* excluye a San Luis Potosí; así los dos dominios no comparten UPM y la diferencia tiene sentido estadístico. "
      "Las tablas por ámbito usan *Nacional* (incluye a SLP, ~2 % de los ocupados).\n"]
for amb in ["Nacional", "San Luis Potosí"]:
    sub = res[res.ambito == amb]
    md.append(f"## {amb}\n")
    md.append(tabla(sub, [
        lambda r: f"{r.tipo}: {r.grupo}", lambda r: r.n_ingreso,
        lambda r: f"{f0(r.ingreso_medio)} ({f0(r.ingreso_medio_lo)}–{f0(r.ingreso_medio_hi)})",
        lambda r: f"{f0(r.p25)}", lambda r: f"{f0(r.p50)} ({f0(r.p50_lo)}–{f0(r.p50_hi)})", lambda r: f"{f0(r.p75)}",
        lambda r: f"{f0(r.p90)}",
        lambda r: f"{r.pct_informal:.1f} ({r.pct_informal_lo:.1f}–{r.pct_informal_hi:.1f})",
        lambda r: ("⚠ n<100" if r.n_ingreso < 100 else "")],
        ["Grupo", "n con ingreso", "Media (IC 95 %)", "p25", "Mediana (IC 95 %)", "p75", "p90", "% informal (IC 95 %)", "Aviso"]) + "\n")
md.append("## Diferencia San Luis Potosí − Resto del país (IC 95 %)\n")
md.append("Una diferencia es estadísticamente distinguible de cero solo si su intervalo no contiene 0 (✔).\n")
sig = lambda lo, hi: "✔" if (lo > 0 or hi < 0) else "—"
md.append(tabla(dif, [
    lambda r: f"{r.tipo}: {r.grupo}", lambda r: r.n_ingreso_slp,
    lambda r: f"{r.dif_pct_informal:+.1f} ({r.dif_pct_informal_lo:+.1f} a {r.dif_pct_informal_hi:+.1f}) {sig(r.dif_pct_informal_lo, r.dif_pct_informal_hi)}",
    lambda r: f"{r.dif_ingreso_medio:+,.0f} ({r.dif_ingreso_medio_lo:+,.0f} a {r.dif_ingreso_medio_hi:+,.0f}) {sig(r.dif_ingreso_medio_lo, r.dif_ingreso_medio_hi)}",
    lambda r: f"{r.dif_mediana:+,.0f} ({r.dif_mediana_lo:+,.0f} a {r.dif_mediana_hi:+,.0f}) {sig(r.dif_mediana_lo, r.dif_mediana_hi)}"],
    ["Grupo", "n con ingreso SLP", "Dif. % informal (pts)", "Dif. ingreso medio ($)", "Dif. mediana ($)"]) + "\n")
(RAIZ / "reports").mkdir(exist_ok=True)
(RAIZ / "reports" / "estadisticos.md").write_text("\n".join(md), encoding="utf-8")
print("Guardado reports/estadisticos.md")
