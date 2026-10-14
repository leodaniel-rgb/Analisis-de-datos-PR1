"""Paso 6b: graficas con matplotlib a partir de data/interim/estadisticos.pkl y la tabla limpia.

Paleta validada (scripts/validate_palette.js del skill dataviz): Nacional = azul #2a78d6,
San Luis Potosi = naranja #eb6834 (par adyacente: CVD dE 24.7, vision normal dE 33.6, contraste >= 3:1).
"""
import os
import warnings
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

warnings.filterwarnings("ignore")
RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "reports" / "figures"
SALIDA.mkdir(parents=True, exist_ok=True)
load_dotenv(RAIZ / ".env")

SUPERFICIE, TINTA, TINTA_2, TINTA_3, REJILLA = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"
AZUL, NARANJA = "#2a78d6", "#eb6834"
FUENTE = "Fuente: INEGI, ENOE 2T 2026 (ocupados de 15+ años); cálculos propios. Barras = IC 95 %."
plt.rcParams.update({
    "font.family": "Segoe UI", "font.size": 10, "text.color": TINTA, "axes.labelcolor": TINTA_2,
    "xtick.color": TINTA_2, "ytick.color": TINTA_2, "axes.edgecolor": REJILLA,
    "figure.facecolor": SUPERFICIE, "axes.facecolor": SUPERFICIE, "savefig.facecolor": SUPERFICIE,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": REJILLA,
    "grid.linewidth": 0.8, "axes.axisbelow": True,
})

est = pd.read_pickle(RAIZ / "data" / "interim" / "estadisticos.pkl")
res, dif = est["res"], est["dif"]
r = res.set_index(["ambito", "tipo", "grupo"])
NIVELES = ["Primaria incompleta", "Primaria completa", "Secundaria completa", "Medio superior y superior"]
SECTORES = ["Agropecuario", "Construcción", "Comercio", "Servicios", "Industria manufacturera"]  # "Otros" se omite (n<100 en SLP)


def titulo(fig, texto, sub):
    fig.text(0.01, 0.965, texto, fontsize=14, fontweight="bold", va="top", color=TINTA)
    fig.text(0.01, 0.915, sub, fontsize=10, va="top", color=TINTA_2)


def pie(fig, extra=""):
    fig.text(0.01, 0.015, FUENTE + (" " + extra if extra else ""), fontsize=8, color=TINTA_3, va="bottom")


def puntos_ic(ax, categorias, tipo, col, lo, hi, fmt, desplazamiento=0.17, etiquetas=True):
    """Dot plot horizontal: un punto por ambito y categoria, con su IC de 95 %."""
    y = np.arange(len(categorias))[::-1]
    for amb, color, dy in [("Nacional", AZUL, +desplazamiento), ("San Luis Potosí", NARANJA, -desplazamiento)]:
        v = np.array([r.loc[(amb, tipo, c), col] for c in categorias])
        a = np.array([r.loc[(amb, tipo, c), lo] for c in categorias])
        b = np.array([r.loc[(amb, tipo, c), hi] for c in categorias])
        ax.hlines(y + dy, a, b, color=color, linewidth=2, zorder=2)
        ax.scatter(v, y + dy, s=64, color=color, edgecolor=SUPERFICIE, linewidth=1.5, zorder=3, label=amb)
        if etiquetas:
            for xi, yi, vi, bi in zip(v, y + dy, v, b):
                ax.text(bi, yi, "  " + fmt(vi), va="center", fontsize=9, color=TINTA)
    ax.set_yticks(y)
    ax.set_yticklabels(categorias)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="y", visible=False)


# ---- Figura 1: informalidad por escolaridad -----------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.6))
puntos_ic(ax, NIVELES, "Escolaridad", "pct_informal", "pct_informal_lo", "pct_informal_hi", lambda v: f"{v:.1f}%")
ax.set_xlim(20, 105)
ax.set_xlabel("% de ocupados en empleo informal")
ax.legend(loc="lower right", frameon=False)
fig.subplots_adjust(top=0.80, bottom=0.14, left=0.2, right=0.95)
titulo(fig, "La informalidad cae con la escolaridad, y SLP sigue el mismo patrón que el país",
       "% de ocupados con empleo informal por nivel de instrucción. SLP y Nacional se solapan en los 4 niveles.")
pie(fig)
fig.savefig(SALIDA / "01_informalidad_por_escolaridad.png", dpi=150)
plt.close(fig)

# ---- Figura 2: ingreso medio por escolaridad ----------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.6))
puntos_ic(ax, NIVELES, "Escolaridad", "ingreso_medio", "ingreso_medio_lo", "ingreso_medio_hi", lambda v: f"${v:,.0f}")
ax.set_xlim(4500, 16500)
ax.set_xlabel("Ingreso mensual medio, pesos (ocupados con monto declarado)")
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.legend(loc="upper right", frameon=False)
fig.subplots_adjust(top=0.80, bottom=0.14, left=0.2, right=0.95)
titulo(fig, "Con primaria completa, SLP gana menos que el resto del país; con medio superior no hay diferencia clara",
       "Ingreso mensual medio por nivel de instrucción. Un intervalo más ancho en SLP refleja su muestra más pequeña.")
pie(fig, "Solo ocupados con monto declarado (65 % de los ocupados).")
fig.savefig(SALIDA / "02_ingreso_medio_por_escolaridad.png", dpi=150)
plt.close(fig)

# ---- Figura 3: distribucion del ingreso ---------------------------------------------------------
engine = create_engine("postgresql+psycopg2://{u}:{p}@{h}:{port}/{d}".format(
    u=os.getenv("PGUSER"), p=os.getenv("PGPASSWORD"), h=os.getenv("PGHOST", "localhost"),
    port=os.getenv("PGPORT", "5432"), d=os.getenv("PGDATABASE")))
d = pd.read_sql("SELECT cve_ent, ingocup_pesos, fac_tri FROM clean.ocupados_2026t2 WHERE ingocup_pesos IS NOT NULL", engine)
TOPE = 30000
bins = np.arange(0, TOPE + 2000, 2000)
fig, ax = plt.subplots(figsize=(10, 5.6))
for amb, color, sub in [("Nacional", AZUL, d), ("San Luis Potosí", NARANJA, d[d.cve_ent == 24])]:
    x = np.minimum(sub.ingocup_pesos.to_numpy(), TOPE - 1)
    h, _ = np.histogram(x, bins=bins, weights=sub.fac_tri.to_numpy())
    pct = 100 * h / h.sum()
    ax.stairs(pct, bins, color=color, linewidth=2, label=amb, baseline=None)
    med = r.loc[(amb, "Total", "Todos"), "p50"]
    ax.axvline(med, color=color, linewidth=1.2, linestyle=(0, (4, 3)))
    ax.text(med + (150 if amb == "Nacional" else -150), 17.4 if amb == "Nacional" else 18.6,
            f"Mediana {amb.replace('San Luis Potosí', 'SLP')}: \\${med:,.0f}", color=TINTA, fontsize=9,
            ha="left" if amb == "Nacional" else "right")
ax.set_xlim(0, TOPE)
ax.set_ylim(0, 20)
ax.set_xlabel("Ingreso mensual, pesos (tramos de \\$2,000; el último agrupa \\$28,000 o más)")
ax.annotate("\\$28,000\no más\n(acumulado)", xy=(29000, 4.1), xytext=(25200, 8.2), fontsize=9, color=TINTA_2,
            arrowprops=dict(arrowstyle="-", color=TINTA_3, linewidth=1), ha="center")
ax.set_ylabel("% de los ocupados")
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
ax.legend(loc="upper right", frameon=False)
fig.subplots_adjust(top=0.80, bottom=0.14, left=0.08, right=0.97)
titulo(fig, "El ingreso de SLP se concentra en tramos más bajos que el del país",
       "Distribución ponderada del ingreso mensual. Línea punteada = mediana (cae sobre valores muy repetidos, ver nota).")
fig.text(0.01, 0.045, "Nota: los ingresos se concentran en valores como \\$8,600 y \\$12,900, por lo que la mediana es sensible a ello.",
         fontsize=8, color=TINTA_3, va="bottom")
fig.text(0.01, 0.015, "Fuente: INEGI, ENOE 2T 2026 (ocupados de 15+ años con monto de ingreso declarado); cálculos propios.",
         fontsize=8, color=TINTA_3, va="bottom")
fig.savefig(SALIDA / "03_distribucion_ingreso.png", dpi=150)
plt.close(fig)

# ---- Figura 4: por sector (dos paneles, sin doble eje) ------------------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5.6), sharey=True)
puntos_ic(a1, SECTORES, "Sector", "pct_informal", "pct_informal_lo", "pct_informal_hi", lambda v: f"{v:.0f}%")
a1.set_xlim(10, 110)
a1.set_xlabel("% de ocupados en empleo informal")
a1.set_title("Informalidad", loc="left", fontsize=11, color=TINTA, fontweight="bold")
puntos_ic(a2, SECTORES, "Sector", "ingreso_medio", "ingreso_medio_lo", "ingreso_medio_hi", lambda v: f"${v/1000:.1f}k")
a2.set_xlim(3500, 16500)
a2.set_xlabel("Ingreso mensual medio, pesos")
a2.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
a2.set_title("Ingreso medio", loc="left", fontsize=11, color=TINTA, fontweight="bold")
h_, l_ = a1.get_legend_handles_labels()
fig.legend(h_, l_, loc="upper right", bbox_to_anchor=(0.97, 0.93), frameon=False, ncol=2)
fig.subplots_adjust(top=0.78, bottom=0.14, left=0.19, right=0.97, wspace=0.12)
titulo(fig, "En manufactura SLP tiene mucha menos informalidad que el país (23 % vs 37 %)",
       "Por sector de actividad. Se omite \"Otros\" (solo 27 observaciones con ingreso en SLP).")
pie(fig)
fig.savefig(SALIDA / "04_sector_informalidad_e_ingreso.png", dpi=150)
plt.close(fig)

# ---- Figura 5: diferencias SLP - resto del pais -------------------------------------------------
orden = [("Total", "Todos")] + [("Escolaridad", n) for n in NIVELES] + [("Sector", s) for s in SECTORES]
etiquetas = ["Todos los ocupados"] + NIVELES + SECTORES
dd = dif.set_index(["tipo", "grupo"]).loc[orden]
fig, axs = plt.subplots(1, 2, figsize=(11, 6.6), sharey=True)
y = np.arange(len(orden))[::-1]
for ax, col, lab, fmt in [(axs[0], "dif_pct_informal", "Diferencia en % de informalidad (puntos porcentuales)", "{:+.1f}"),
                          (axs[1], "dif_ingreso_medio", "Diferencia en ingreso mensual medio (pesos)", "{:+,.0f}")]:
    v, lo, hi = dd[col].to_numpy(), dd[col + "_lo"].to_numpy(), dd[col + "_hi"].to_numpy()
    distinto = (lo > 0) | (hi < 0)
    ax.axvline(0, color=TINTA_2, linewidth=1.2, zorder=1)
    ax.hlines(y, lo, hi, color=np.where(distinto, NARANJA, TINTA_3), linewidth=2, zorder=2)
    ax.scatter(v[distinto], y[distinto], s=64, color=NARANJA, edgecolor=SUPERFICIE, linewidth=1.5, zorder=3,
               label="Intervalo no incluye 0")
    ax.scatter(v[~distinto], y[~distinto], s=64, facecolor=SUPERFICIE, edgecolor=TINTA_3, linewidth=1.8, zorder=3,
               label="Intervalo incluye 0")
    ax.set_xlabel(lab)
    ax.set_yticks(y)
    ax.set_yticklabels(etiquetas)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="y", visible=False)
    for xi, yi, vi, hi_ in zip(v, y, v, hi):
        ax.text(hi_, yi, "  " + fmt.format(vi), va="center", fontsize=9, color=TINTA)
axs[0].set_xlim(-22, 16)
axs[1].set_xlim(-3500, 2400)
axs[1].xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "0" if v == 0 else f"{v:+,.0f}"))
h_, l_ = axs[0].get_legend_handles_labels()
fig.legend(h_, l_, loc="upper right", bbox_to_anchor=(0.97, 0.89), frameon=False, ncol=2)
fig.subplots_adjust(top=0.78, bottom=0.12, left=0.2, right=0.97, wspace=0.1)
titulo(fig, "Solo algunas diferencias entre SLP y el resto del país son claras",
       "SLP menos resto del país (a la derecha de 0, SLP es mayor). Son 33 comparaciones: algún naranja puede ser azar.")
pie(fig, "Se omite \"Otros\".")
fig.savefig(SALIDA / "05_diferencias_slp_vs_resto.png", dpi=150)
plt.close(fig)
print("Figuras guardadas en", SALIDA)
