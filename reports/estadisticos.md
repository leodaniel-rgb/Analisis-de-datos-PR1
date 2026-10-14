# Estadísticos con intervalos de confianza al 95 % (ENOE 2T 2026)

Ingreso: solo ocupados con monto declarado (`ingocup > 0`). Medias y proporciones: varianza por conglomerados últimos (Taylor). Percentiles: bootstrap Rao-Wu con %d réplicas. `n` = observaciones de la muestra; celdas con n < 100 son poco confiables (criterio de este proyecto).

**Cómo leer este reporte**

- Los ingresos se concentran en pocos valores repetidos (p. ej. 8,600 y 12,900). Cuando una mediana cae sobre uno de ellos, su intervalo bootstrap puede reducirse a un solo valor (p. ej. 10,750–10,750): eso **no** es precisión alta, es un efecto de la concentración de valores. Para comparar ingresos se prefiere la **media**, cuyo intervalo no depende de ello.
- Se comparan 11 grupos en 3 indicadores (33 pruebas). Con 95 % de confianza se esperan ~1.6 resultados ✔ por azar; los ✔ con un límite del intervalo muy cerca de 0 deben tomarse con cautela.
- *Resto del país* excluye a San Luis Potosí; así los dos dominios no comparten UPM y la diferencia tiene sentido estadístico. Las tablas por ámbito usan *Nacional* (incluye a SLP, ~2 % de los ocupados).

## Nacional

| Grupo | n con ingreso | Media (IC 95 %) | p25 | Mediana (IC 95 %) | p75 | p90 | % informal (IC 95 %) | Aviso |
|---|---|---|---|---|---|---|---|---|
| Total: Todos | 123546 | 11,047 (10,938–11,155) | 6,450 | 9,460 (9,425–9,460) | 12,900 | 19,350 | 55.1 (54.6–55.6) |  |
| Escolaridad: Primaria incompleta | 8596 | 6,830 (6,630–7,030) | 3,000 | 6,400 (6,020–6,450) | 9,030 | 12,900 | 87.6 (86.7–88.5) |  |
| Escolaridad: Primaria completa | 16867 | 8,476 (8,315–8,638) | 4,300 | 7,740 (7,740–8,000) | 10,750 | 15,050 | 79.1 (78.2–80.0) |  |
| Escolaridad: Secundaria completa | 41493 | 9,741 (9,627–9,855) | 6,020 | 8,600 (8,600–9,000) | 12,169 | 16,000 | 62.9 (62.1–63.6) |  |
| Escolaridad: Medio superior y superior | 56362 | 13,777 (13,579–13,975) | 8,000 | 11,000 (10,800–11,352) | 16,000 | 24,000 | 37.9 (37.3–38.5) |  |
| Sector: Construcción | 11629 | 12,057 (11,836–12,278) | 8,600 | 10,750 (10,750–10,750) | 13,760 | 18,490 | 80.9 (79.8–82.0) |  |
| Sector: Industria manufacturera | 20734 | 11,244 (11,045–11,442) | 7,740 | 10,320 (10,000–10,518) | 12,900 | 17,200 | 36.6 (35.4–37.7) |  |
| Sector: Comercio | 23060 | 9,683 (9,458–9,907) | 5,160 | 8,600 (8,600–8,600) | 12,000 | 16,000 | 59.0 (58.0–59.9) |  |
| Sector: Servicios | 57563 | 12,187 (12,012–12,361) | 6,450 | 10,000 (10,000–10,000) | 15,000 | 21,500 | 48.7 (48.1–49.4) |  |
| Sector: Otros | 1037 | 18,132 (17,047–19,218) | 10,750 | 15,050 (14,000–16,000) | 20,640 | 30,000 | 19.1 (13.6–24.6) |  |
| Sector: Agropecuario | 8982 | 6,834 (6,590–7,078) | 3,225 | 6,450 (6,400–6,450) | 8,600 | 12,040 | 84.8 (83.8–85.9) |  |

## San Luis Potosí

| Grupo | n con ingreso | Media (IC 95 %) | p25 | Mediana (IC 95 %) | p75 | p90 | % informal (IC 95 %) | Aviso |
|---|---|---|---|---|---|---|---|---|
| Total: Todos | 3197 | 10,330 (9,935–10,725) | 5,160 | 8,600 (8,600–9,030) | 12,900 | 18,060 | 54.9 (52.4–57.3) |  |
| Escolaridad: Primaria incompleta | 189 | 6,978 (5,918–8,038) | 2,580 | 6,450 (5,160–7,740) | 9,030 | 12,040 | 87.9 (83.1–92.8) |  |
| Escolaridad: Primaria completa | 448 | 6,770 (6,320–7,219) | 3,440 | 6,450 (6,450–7,525) | 9,030 | 12,040 | 77.3 (73.7–80.8) |  |
| Escolaridad: Secundaria completa | 1248 | 8,893 (8,466–9,320) | 5,160 | 8,600 (8,000–8,600) | 10,750 | 15,050 | 61.3 (57.5–65.0) |  |
| Escolaridad: Medio superior y superior | 1300 | 13,634 (12,867–14,401) | 8,000 | 10,750 (10,750–11,610) | 16,500 | 24,000 | 36.6 (34.1–39.2) |  |
| Sector: Construcción | 285 | 10,781 (9,588–11,974) | 6,450 | 9,460 (8,600–10,750) | 12,900 | 19,350 | 79.7 (73.8–85.7) |  |
| Sector: Industria manufacturera | 649 | 11,746 (10,976–12,516) | 8,170 | 10,320 (9,890–10,750) | 13,330 | 20,000 | 23.3 (19.4–27.1) |  |
| Sector: Comercio | 559 | 9,058 (8,190–9,926) | 4,300 | 8,370 (7,740–8,600) | 11,000 | 15,050 | 64.0 (59.5–68.6) |  |
| Sector: Servicios | 1328 | 11,584 (10,963–12,206) | 6,000 | 9,890 (9,030–10,000) | 15,000 | 21,500 | 49.7 (47.1–52.2) |  |
| Sector: Otros | 27 | 11,331 (9,114–13,548) | 8,000 | 10,000 (8,000–12,040) | 12,040 | 16,000 | 25.5 (8.1–42.9) | ⚠ n<100 |
| Sector: Agropecuario | 333 | 5,756 (5,084–6,427) | 3,225 | 5,375 (4,300–6,450) | 7,740 | 9,030 | 89.4 (85.7–93.0) |  |

## Diferencia San Luis Potosí − Resto del país (IC 95 %)

Una diferencia es estadísticamente distinguible de cero solo si su intervalo no contiene 0 (✔).

| Grupo | n con ingreso SLP | Dif. % informal (pts) | Dif. ingreso medio ($) | Dif. mediana ($) |
|---|---|---|---|---|
| Total: Todos | 3197 | -0.2 (-2.7 a +2.3) — | -732 (-1,142 a -322) ✔ | -860 (-860 a -430) ✔ |
| Escolaridad: Primaria incompleta | 189 | +0.3 (-4.6 a +5.3) — | +150 (-929 a +1,230) — | +50 (-1,290 a +1,720) — |
| Escolaridad: Primaria completa | 448 | -1.8 (-5.5 a +1.8) — | -1,741 (-2,219 a -1,262) ✔ | -1,290 (-1,550 a -215) ✔ |
| Escolaridad: Secundaria completa | 1248 | -1.7 (-5.5 a +2.2) — | -869 (-1,311 a -426) ✔ | +0 (-830 a +0) — |
| Escolaridad: Medio superior y superior | 1300 | -1.3 (-4.0 a +1.3) — | -146 (-939 a +647) — | -250 (-610 a +610) — |
| Sector: Construcción | 285 | -1.2 (-7.3 a +4.9) — | -1,299 (-2,513 a -86) ✔ | -1,290 (-2,150 a +0) — |
| Sector: Industria manufacturera | 649 | -13.7 (-17.7 a -9.7) ✔ | +514 (-282 a +1,310) — | +0 (-467 a +633) — |
| Sector: Comercio | 559 | +5.2 (+0.5 a +9.8) ✔ | -637 (-1,534 a +260) — | -230 (-860 a +0) — |
| Sector: Servicios | 1328 | +0.9 (-1.7 a +3.6) — | -614 (-1,260 a +33) — | -110 (-970 a +0) — |
| Sector: Otros | 27 | +6.6 (-11.7 a +24.9) — | -7,000 (-9,485 a -4,516) ✔ | -5,050 (-8,600 a -3,010) ✔ |
| Sector: Agropecuario | 333 | +4.7 (+0.9 a +8.5) ✔ | -1,109 (-1,825 a -392) ✔ | -1,075 (-2,150 a +0) — |
