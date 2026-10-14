# Guía: carga y limpieza (pasos 3 y 4)

Cómo reproducirlo: `python src/01_cargar_raw.py` y luego `python src/02_limpiar.py`. El resumen de cada filtro queda en `reports/limpieza_log.txt`.

## 1. Dos capas: `raw` y `clean`
- **Qué:** `raw.enoe_sdemt_2026t2` es una copia fiel del CSV (todo TEXT). `clean.ocupados_2026t2` es la tabla de análisis, con tipos y reglas.
- **Por qué:** si descubres un error de limpieza, vuelves a correr el script desde `raw` sin volver a descargar. Además cualquiera puede auditar qué se cambió. Es la práctica habitual de separar "dato original" de "dato transformado" (ELT en bodegas de datos).
- **Cómo se hizo:** `COPY` de PostgreSQL en una sola transacción (rápido y atómico) y comprobación de que las filas cargadas son las esperadas.

## 2. Los nulos no siempre son NULL
- En `raw` hay **0 `NULL`**, pero columnas como `eda` o `sex` traen 9,305 **espacios en blanco**. Si conviertes a número sin tratarlos, falla (nos pasó) o, peor, se cuelan como valores.
- Además hay **códigos que significan "nulo"**: `0` = "no aplica", `99` en `anios_esc`, `7` en `rama`, `5` en `niv_ins`. Se descubren **leyendo el diccionario**, no los datos.
- **Reproducir:** `pd.to_numeric(col.str.strip().replace("", np.nan))` y luego recodificar los códigos "no especificado" a `NaN`.

## 3. Duplicados: la llave importa
- Una llave mal armada produce "duplicados" falsos: con `cd_a` salieron 56,657; con `cve_ent` 12,453; añadiendo `tipo` o `n_pro_viv`, **cero**. Antes de borrar filas, prueba de qué campos depende la unicidad.
- La llave quedó como: `cve_ent, con, v_sel, n_hog, h_mud, n_ent, n_ren, n_pro_viv, tipo`. Se verifica con un `assert` y se impone con `PRIMARY KEY`.
- Pendiente de documentar: qué significa exactamente `tipo` (el diccionario lo llama "tipo de muestra").

## 4. Población objetivo
- `fac_tri` ya vale 0 para ausentes definitivos y entrevistas incompletas, así que `fac_tri > 0` identifica a los residentes válidos (10,021 filas fuera).
- Luego: edad ≥ 15 (la publicación oficial usa 15+, aunque el diccionario menciona 12+) y `clase2 = 1` (ocupados).
- **Reconciliación con la fuente oficial:** 60.04 millones de ocupados expandidos frente a los 60.0 millones publicados por INEGI. Compara siempre tu total contra una cifra oficial antes de analizar.

## 5. Factor de expansión (`fac_tri`)
- Cada persona de la muestra representa a `fac_tri` personas de la población. Las **proporciones y totales** se estiman con la suma de `fac_tri`, no contando filas.
- Efecto real aquí: informalidad (15+) **55.1 % ponderada** frente a **51.9 % sin ponderar**. Sin ponderar subestimarías la informalidad porque la muestra no es proporcional a la población.
- Los intervalos de confianza requieren el diseño muestral (`upm`, `est_d_tri`), que se conservaron en la tabla. Una media ponderada no trae su error estándar "gratis".

## 6. Regla de ingresos
- `ingocup = 0` en 66,289 ocupados, pero con significados distintos según `ing7c`. La tabla limpia deja `tipo_ingreso`: `monto_declarado`, `solo_rango`, `no_recibe`, `no_especificado`.
- Se analizan ingresos solo con `ingocup > 0` (monto declarado). Cobertura: 65.2 % de la muestra y 64.9 % de la población ocupada ponderada; el resto se reporta como limitación.
- El motivo por el que existen ceros con rango declarado es **inferencia nuestra**, no está en el diccionario consultado.

## 7. Qué mirar después
- `ingocup_pesos` mínimo 17 pesos al mes y `hrsocup` mínimo 0: valores extremos. Para ingresos usaremos mediana y percentiles, que resisten extremos mejor que la media.
