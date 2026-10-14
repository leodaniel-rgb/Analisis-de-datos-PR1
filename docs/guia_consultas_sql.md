# Guía: 15 consultas SQL (paso 5)

**Reproducir:**
```bash
.venv\Scripts\python src\ejecutar_sql.py sql/00_catalogos.sql   # crea el esquema cat y verifica integridad
.venv\Scripts\python src\ejecutar_sql.py sql/01_consultas.sql   # corre Q01-Q15 y guarda reports/resultados_consultas.md
```

## Patrones que enseña cada nivel
| Nivel | Consultas | Idea central |
|---|---|---|
| 1. Filtros y conteos | Q01-Q04 | `WHERE`, `COUNT(*) FILTER`, `SUM(fac_tri)`. Contar filas ≠ contar personas. |
| 2. `GROUP BY` + `JOIN` | Q05-Q09 | Media ponderada `SUM(w·x)/SUM(w)`; catálogos con `JOIN`; `HAVING` filtra grupos. |
| 3. CTE | Q10-Q11 | Dividir un problema en pasos con nombre (`WITH`) y razones entre grupos. |
| 4. Ventanas | Q12-Q15 | `RANK`, `SUM() OVER`, `LAG`: calculan sobre un conjunto de filas **sin colapsarlas**. |

## Por qué se hizo así
- **Catálogos (`cat.*`) y `JOIN`:** una sola traducción de códigos a nombres, verificable con las pruebas de integridad (0 claves sin catálogo). Evita `CASE WHEN` repetidos.
- **Truco del CTE `base`:** duplica las filas de SLP como segundo "ámbito" (`UNION ALL`) para comparar SLP con el país en una sola consulta. "Nacional" incluye a SLP.
- **Media ponderada solo con ingreso declarado:** el numerador se calcula solo con `ingocup_pesos`; el denominador se filtra con `FILTER (WHERE ingocup_pesos IS NOT NULL)`. Si no filtras el denominador, la media queda subestimada, y es un error silencioso.
- **Percentiles ponderados a mano (Q13):** `percentile_cont` de SQL ignora el factor de expansión. Se calcula el peso acumulado con `SUM(w) OVER (ORDER BY x)` y se toma el primer valor que alcanza el p % del peso total.

## Cómo se verificó
Se recalcularon en pandas, con código independiente, Q05, Q08, Q13 y Q15: coinciden exactamente. Verificar un resultado con un segundo método es la mejor defensa contra errores de lógica que "corren sin error".

## Lo que dicen los datos (descriptivo, aún sin intervalos de confianza)
- Informalidad: **54.9 % SLP vs 55.1 % nacional** (Q04). La diferencia es mínima; sin intervalo de confianza no se puede afirmar que existe.
- Ingreso medio con primaria completa: **$6,770 SLP vs $8,476 nacional** (razón 0.80, Q10), con n = 448 en SLP. Con medio superior y superior la razón es 0.99.
- Manufactura: **23.3 % de informalidad en SLP vs 36.6 % nacional** (Q08), la mayor diferencia por sector, con n = 1,097 en SLP. También pesa más en SLP: 19.6 % de los ocupados vs 16.3 % (Q15).
- Mediana de ingreso: **$8,600 SLP vs $9,460 nacional** (Q13). SLP ocupa el lugar 18 de 32 en ingreso medio y el 17 en informalidad (Q12).

## Trampas que aparecieron
1. **Concentración de valores (heaping).** Los ingresos más repetidos son 8,600, 12,900, 10,750, 6,450 y 7,740, casi todos múltiplos de 2,150. Por eso la mediana de SLP (8,600) y el p75 de ambos ámbitos (12,900) caen justo en un valor repetido. *Hipótesis, no verificada:* puede venir de cómo se captura o imputa el ingreso. Hay que revisar la metodología de INEGI antes de afirmarlo.
2. **Cobertura desigual del ingreso.** Con monto declarado hay 59.8 % de los ocupados en SLP, frente a 64.9 % a nivel nacional. Si quienes no declaran difieren de quienes sí, la comparación puede estar sesgada.
3. **Celdas pequeñas.** "Otros" en SLP tiene n = 27 con ingreso (Q06) y 10 en la celda formal/informal (Q11). Q09 aplica un umbral de 100 observaciones, que es un criterio de este proyecto, no una norma de INEGI.
4. **Descriptivo no es causal.** Q11 muestra que los formales ganan ~1.7 a 2.1 veces más, pero eso no prueba que formalizarse cause ese ingreso.
5. **Error de muestreo.** Todo número es una estimación. Los intervalos de confianza se calculan con `upm` y `est_d_tri`, que ya están en la tabla. Es el siguiente paso para poder decir "difiere" o "no difiere".

## Tarea para practicar
1. Escribe una consulta que compare la informalidad **por sexo** (usa `cat.sexo`) en SLP y en el país.
2. Calcula el ingreso por hora medio (`ing_x_hrs_pesos`) por sector en SLP. ¿Cambia el orden de los sectores respecto a Q06? ¿Por qué podría cambiar?
3. Cambia el umbral de Q09 de 100 a 300. ¿Qué sectores desaparecen y qué pasa con la conclusión?
