# Fuente de datos

| Campo | Valor |
|---|---|
| Encuesta | Encuesta Nacional de Ocupación y Empleo (ENOE), población de 15 años y más |
| Institución | INEGI |
| Periodo | Segundo trimestre de 2026 (abril–junio; la tabla incluye `mes_cal` = 4, 5, 6 y 97) |
| Archivo | `enoe_2026_trim2_csv.zip` |
| URL | https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/microdatos/enoe_2026_trim2_csv.zip |
| Página del programa | https://www.inegi.org.mx/programas/enoe/15ymas/#microdatos |
| Última modificación del archivo (según INEGI) | 25 de agosto de 2026 |
| Fecha de descarga | 2026-10-13 |
| Tamaño | 35,213,597 bytes (33.6 MB) |
| SHA-256 | `020811FA989A3E4E3E0DAAE39B32DF6BB055F3CA59653B76ECC454F9B231D91E` |

## Tablas incluidas en el zip
`ENOE_SDEMT226` (417,128 filas, 115 columnas; se usa esta), `ENOE_COE1T226`, `ENOE_COE2T226`, `ENOE_HOGT226`, `ENOE_VIVT226`.

## Diccionario de datos
El zip de 2026 **no incluye diccionario**. Se usó el diccionario oficial del cuarto trimestre de 2025, que es el más reciente publicado en la Red Nacional de Metadatos de INEGI:
- https://www.inegi.org.mx/rnm/index.php/catalog/1121/data-dictionary/F52?file_name=SDEMT425

Se comprobó que el CSV de 2026 trae 115 columnas y todas las variables que usa este proyecto. Se debe tratar como supuesto que los códigos no cambiaron entre 4T 2025 y 2T 2026.

Códigos verificados en el diccionario: `EMP_PPAL` 1 = empleo informal, 2 = empleo formal, 0 = no aplica; `CLASE2` 1 = población ocupada; `NIV_INS` 1–4 (4 = medio superior y superior), 5 = no especificado; `RAMA` 1 = construcción, 2 = industria manufacturera, 3 = comercio, 4 = servicios, 5 = otros, 6 = agropecuario, 7 = no especificado. Factor de expansión: `FAC_TRI`.

## Reproducir
Los datos crudos no se suben a Git (ver `.gitignore`). Descarga el zip de la URL, verifica el SHA-256 y extrae en `data/raw/enoe_2026_t2/`.
