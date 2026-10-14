-- 15 consultas sobre clean.ocupados_2026t2 (ENOE 2T 2026, ocupados de 15+ anios).
-- Convenciones:
--   * SLP = cve_ent 24. "Nacional" incluye a SLP (es el total del pais).
--   * Todo total o proporcion usa fac_tri (factor de expansion), nunca count(*) a secas.
--   * Ingreso: solo ingocup_pesos (monto declarado > 0); es NULL en el resto y los
--     promedios lo ignoran, pero el DENOMINADOR ponderado se filtra explicitamente.
--   * "n_muestra" = filas reales de la encuesta; sirve para juzgar si una celda es confiable.
-- Formato: cada consulta empieza con "-- Qnn" para que el runner la separe y la ejecute.

------------------------------------------------------------------------------------------
-- NIVEL 1: filtros y conteos
------------------------------------------------------------------------------------------

-- Q01 | Cuantos ocupados hay en la MUESTRA, a nivel nacional y en SLP?
-- Concepto: WHERE / count(*) FILTER. Responde "de cuantas entrevistas parto", no "cuantas
-- personas hay": para eso se necesita fac_tri (Q02). Una muestra chica = estimaciones inestables.
SELECT count(*)                          AS ocupados_muestra_nacional,
       count(*) FILTER (WHERE cve_ent = 24) AS ocupados_muestra_slp
FROM clean.ocupados_2026t2;

-- Q02 | Cuantas personas ocupadas representa la encuesta, por entidad (las 10 mayores)?
-- Concepto: SUM(fac_tri) + JOIN a catalogo + GROUP BY + ORDER BY + LIMIT.
-- Esta es la forma correcta de "contar poblacion" con una encuesta con factor de expansion.
SELECT e.nombre AS entidad,
       count(*)           AS n_muestra,
       sum(o.fac_tri)     AS poblacion_ocupada
FROM clean.ocupados_2026t2 o
JOIN cat.entidad e USING (cve_ent)
GROUP BY e.nombre
ORDER BY poblacion_ocupada DESC
LIMIT 10;

-- Q03 | Que porcentaje de los ocupados esta en empleo informal, en cada entidad?
-- Concepto: agregacion condicional con FILTER. Tasa = sum(w de informales) / sum(w de todos).
-- emp_ppal = 1 es informal (INEGI, informalidad laboral del trabajo principal).
SELECT e.nombre AS entidad,
       count(*) AS n_muestra,
       round(100.0 * sum(o.fac_tri) FILTER (WHERE o.emp_ppal = 1) / sum(o.fac_tri), 1) AS pct_informal
FROM clean.ocupados_2026t2 o
JOIN cat.entidad e USING (cve_ent)
GROUP BY e.nombre
ORDER BY pct_informal DESC;

-- Q04 | SLP frente al pais: tasa de informalidad ponderada y SIN ponderar.
-- Concepto: UNION ALL para apilar dos "ambitos". La columna pct_sin_ponderar muestra el sesgo
-- de ignorar el factor de expansion (pregunta 3 del proyecto).
SELECT 'San Luis Potosí' AS ambito,
       count(*) AS n_muestra,
       round(100.0 * sum(fac_tri) FILTER (WHERE emp_ppal = 1) / sum(fac_tri), 1) AS pct_informal_ponderado,
       round(100.0 * count(*) FILTER (WHERE emp_ppal = 1) / count(*), 1)         AS pct_sin_ponderar
FROM clean.ocupados_2026t2 WHERE cve_ent = 24
UNION ALL
SELECT 'Nacional', count(*),
       round(100.0 * sum(fac_tri) FILTER (WHERE emp_ppal = 1) / sum(fac_tri), 1),
       round(100.0 * count(*) FILTER (WHERE emp_ppal = 1) / count(*), 1)
FROM clean.ocupados_2026t2;

------------------------------------------------------------------------------------------
-- NIVEL 2: GROUP BY con JOIN (preguntas 1, 2 y 3 del proyecto)
------------------------------------------------------------------------------------------

-- Q05 | Ingreso mensual medio por nivel de instruccion: SLP vs pais (pregunta 1).
-- Concepto: media ponderada = sum(w*x) / sum(w), solo entre quienes tienen ingreso declarado.
-- El CTE "base" duplica las filas de SLP bajo un segundo ambito, asi evitamos escribir
-- la misma consulta dos veces (patron que se repite en Q06-Q15).
WITH base AS (
    SELECT 'Nacional' AS ambito, * FROM clean.ocupados_2026t2
    UNION ALL
    SELECT 'San Luis Potosí', * FROM clean.ocupados_2026t2 WHERE cve_ent = 24
)
SELECT n.nombre AS nivel_instruccion, b.ambito,
       count(*) FILTER (WHERE b.ingocup_pesos IS NOT NULL) AS n_con_ingreso,
       round(sum(b.ingocup_pesos * b.fac_tri)
             / sum(b.fac_tri) FILTER (WHERE b.ingocup_pesos IS NOT NULL)) AS ingreso_medio
FROM base b
JOIN cat.nivel_instruccion n USING (niv_ins)
GROUP BY n.orden, n.nombre, b.ambito
ORDER BY n.orden, b.ambito DESC;

-- Q06 | Ingreso mensual medio por sector de actividad: SLP vs pais (pregunta 2).
-- Mismo patron que Q05 con otro catalogo. Ojo: "Otros" y "Agropecuario" pueden tener pocas
-- observaciones en SLP; revisar n_con_ingreso antes de concluir (ver Q09).
WITH base AS (
    SELECT 'Nacional' AS ambito, * FROM clean.ocupados_2026t2
    UNION ALL
    SELECT 'San Luis Potosí', * FROM clean.ocupados_2026t2 WHERE cve_ent = 24
)
SELECT s.nombre AS sector, b.ambito,
       count(*) FILTER (WHERE b.ingocup_pesos IS NOT NULL) AS n_con_ingreso,
       round(sum(b.ingocup_pesos * b.fac_tri)
             / sum(b.fac_tri) FILTER (WHERE b.ingocup_pesos IS NOT NULL)) AS ingreso_medio
FROM base b
JOIN cat.sector s USING (rama)
GROUP BY s.nombre, b.ambito
ORDER BY s.nombre, b.ambito DESC;

-- Q07 | Informalidad por nivel de instruccion: SLP vs pais (pregunta 3).
-- Aqui NO se filtra por ingreso: emp_ppal esta completo para todos los ocupados.
WITH base AS (
    SELECT 'Nacional' AS ambito, * FROM clean.ocupados_2026t2
    UNION ALL
    SELECT 'San Luis Potosí', * FROM clean.ocupados_2026t2 WHERE cve_ent = 24
)
SELECT n.nombre AS nivel_instruccion, b.ambito, count(*) AS n_muestra,
       round(100.0 * sum(b.fac_tri) FILTER (WHERE b.emp_ppal = 1) / sum(b.fac_tri), 1) AS pct_informal
FROM base b
JOIN cat.nivel_instruccion n USING (niv_ins)
GROUP BY n.orden, n.nombre, b.ambito
ORDER BY n.orden, b.ambito DESC;

-- Q08 | Informalidad por sector de actividad: SLP vs pais (pregunta 3).
WITH base AS (
    SELECT 'Nacional' AS ambito, * FROM clean.ocupados_2026t2
    UNION ALL
    SELECT 'San Luis Potosí', * FROM clean.ocupados_2026t2 WHERE cve_ent = 24
)
SELECT s.nombre AS sector, b.ambito, count(*) AS n_muestra,
       round(100.0 * sum(b.fac_tri) FILTER (WHERE b.emp_ppal = 1) / sum(b.fac_tri), 1) AS pct_informal
FROM base b
JOIN cat.sector s USING (rama)
GROUP BY s.nombre, b.ambito
ORDER BY s.nombre, b.ambito DESC;

-- Q09 | En SLP, que sectores tienen al menos 100 observaciones con ingreso y cual es su ingreso medio?
-- Concepto: HAVING filtra GRUPOS (WHERE filtra filas). Buena practica: no reportar celdas con
-- muestra pequena. El umbral de 100 es un criterio practico del proyecto, no una norma de INEGI.
SELECT s.nombre AS sector,
       count(*) AS n_con_ingreso,
       round(sum(o.ingocup_pesos * o.fac_tri) / sum(o.fac_tri)) AS ingreso_medio
FROM clean.ocupados_2026t2 o
JOIN cat.sector s USING (rama)
WHERE o.cve_ent = 24 AND o.ingocup_pesos IS NOT NULL
GROUP BY s.nombre
HAVING count(*) >= 100
ORDER BY ingreso_medio DESC;

------------------------------------------------------------------------------------------
-- NIVEL 3: CTE y comparaciones
------------------------------------------------------------------------------------------

-- Q10 | Que fraccion del ingreso nacional medio gana SLP, por nivel de instruccion?
-- Concepto: dos CTE (uno por ambito) unidos por JOIN; razon SLP / Nacional.
-- Ratio < 1 significa que SLP queda por debajo del promedio nacional en ese nivel.
WITH nacional AS (
    SELECT niv_ins, sum(ingocup_pesos * fac_tri) / sum(fac_tri) AS ingreso_medio
    FROM clean.ocupados_2026t2 WHERE ingocup_pesos IS NOT NULL AND niv_ins IS NOT NULL
    GROUP BY niv_ins
), slp AS (
    SELECT niv_ins, sum(ingocup_pesos * fac_tri) / sum(fac_tri) AS ingreso_medio
    FROM clean.ocupados_2026t2 WHERE cve_ent = 24 AND ingocup_pesos IS NOT NULL AND niv_ins IS NOT NULL
    GROUP BY niv_ins
)
SELECT n.nombre AS nivel_instruccion,
       round(nac.ingreso_medio) AS nacional,
       round(slp.ingreso_medio) AS slp,
       round(slp.ingreso_medio / nac.ingreso_medio, 2) AS razon_slp_nacional
FROM nacional nac
JOIN slp USING (niv_ins)
JOIN cat.nivel_instruccion n USING (niv_ins)
ORDER BY n.orden;

-- Q11 | En SLP, cuanto mas ganan los formales que los informales dentro de cada sector?
-- Concepto: CTE con agregacion + pivote con FILTER sobre el resultado (formal vs informal en
-- columnas). Importante: es una comparacion descriptiva; no prueba que la formalidad CAUSE
-- el mayor ingreso (los trabajos formales difieren en escolaridad, tamano de empresa, etc.).
WITH por_grupo AS (
    SELECT rama, emp_ppal,
           count(*) AS n,
           sum(ingocup_pesos * fac_tri) / sum(fac_tri) AS ingreso_medio
    FROM clean.ocupados_2026t2
    WHERE cve_ent = 24 AND ingocup_pesos IS NOT NULL AND rama IS NOT NULL
    GROUP BY rama, emp_ppal
)
SELECT s.nombre AS sector,
       round(max(ingreso_medio) FILTER (WHERE emp_ppal = 2)) AS ingreso_formal,
       round(max(ingreso_medio) FILTER (WHERE emp_ppal = 1)) AS ingreso_informal,
       round(max(ingreso_medio) FILTER (WHERE emp_ppal = 2)
           / max(ingreso_medio) FILTER (WHERE emp_ppal = 1), 2) AS razon_formal_informal,
       min(n) AS n_minimo_celda
FROM por_grupo g
JOIN cat.sector s USING (rama)
GROUP BY s.nombre
ORDER BY razon_formal_informal DESC;

------------------------------------------------------------------------------------------
-- NIVEL 4: funciones de ventana
------------------------------------------------------------------------------------------

-- Q12 | En que lugar queda SLP entre las 32 entidades en ingreso medio y en informalidad?
-- Concepto: RANK() OVER (ORDER BY ...). Una ventana calcula sobre un conjunto de filas SIN
-- colapsarlas (a diferencia de GROUP BY). Ranking 1 = mayor ingreso / mayor informalidad.
WITH por_entidad AS (
    SELECT cve_ent,
           sum(ingocup_pesos * fac_tri) / sum(fac_tri) FILTER (WHERE ingocup_pesos IS NOT NULL) AS ingreso_medio,
           100.0 * sum(fac_tri) FILTER (WHERE emp_ppal = 1) / sum(fac_tri) AS pct_informal
    FROM clean.ocupados_2026t2
    GROUP BY cve_ent
)
SELECT e.nombre AS entidad,
       round(p.ingreso_medio) AS ingreso_medio,
       rank() OVER (ORDER BY p.ingreso_medio DESC) AS lugar_ingreso,
       round(p.pct_informal, 1) AS pct_informal,
       rank() OVER (ORDER BY p.pct_informal DESC)  AS lugar_informalidad
FROM por_entidad p
JOIN cat.entidad e USING (cve_ent)
ORDER BY lugar_ingreso;

-- Q13 | Percentiles ponderados del ingreso (p25, mediana, p75): SLP vs pais.
-- Concepto: percentil PONDERADO = primer valor cuyo peso acumulado alcanza p * peso total.
-- sum(w) OVER (ORDER BY x) es el peso acumulado; sum(w) OVER () el total del ambito.
-- percentile_cont() de SQL ignora fac_tri, por eso no se usa aqui. La mediana resiste valores
-- extremos mejor que la media (hay ingresos muy bajos y muy altos).
WITH base AS (
    SELECT 'Nacional' AS ambito, ingocup_pesos, fac_tri FROM clean.ocupados_2026t2 WHERE ingocup_pesos IS NOT NULL
    UNION ALL
    SELECT 'San Luis Potosí', ingocup_pesos, fac_tri FROM clean.ocupados_2026t2
    WHERE cve_ent = 24 AND ingocup_pesos IS NOT NULL
), valores AS (                       -- un renglon por ingreso distinto (evita empates)
    SELECT ambito, ingocup_pesos, sum(fac_tri) AS w
    FROM base GROUP BY ambito, ingocup_pesos
), acumulado AS (
    SELECT ambito, ingocup_pesos,
           sum(w) OVER (PARTITION BY ambito ORDER BY ingocup_pesos) AS w_acum,
           sum(w) OVER (PARTITION BY ambito)                         AS w_total
    FROM valores
)
SELECT ambito,
       min(ingocup_pesos) FILTER (WHERE w_acum >= 0.25 * w_total) AS p25,
       min(ingocup_pesos) FILTER (WHERE w_acum >= 0.50 * w_total) AS mediana,
       min(ingocup_pesos) FILTER (WHERE w_acum >= 0.75 * w_total) AS p75
FROM acumulado
GROUP BY ambito
ORDER BY ambito DESC;

-- Q14 | Cuanto sube el ingreso medio al pasar de un grupo de escolaridad al siguiente?
-- Concepto: LAG() trae el valor de la fila anterior dentro de la ventana; sirve para
-- calcular cambios entre grupos consecutivos. Se agrupan los anios de escolaridad en tramos
-- porque por anio la muestra de SLP seria muy pequena. Los tramos son decision del proyecto.
WITH base AS (
    SELECT 'Nacional' AS ambito, * FROM clean.ocupados_2026t2
    UNION ALL
    SELECT 'San Luis Potosí', * FROM clean.ocupados_2026t2 WHERE cve_ent = 24
), tramos AS (
    SELECT ambito,
           CASE WHEN anios_esc <= 5  THEN 1 WHEN anios_esc = 6   THEN 2 WHEN anios_esc <= 8  THEN 3
                WHEN anios_esc = 9   THEN 4 WHEN anios_esc <= 11 THEN 5 WHEN anios_esc = 12  THEN 6
                WHEN anios_esc <= 15 THEN 7 WHEN anios_esc = 16  THEN 8 ELSE 9 END AS orden,
           CASE WHEN anios_esc <= 5  THEN '0-5'  WHEN anios_esc = 6   THEN '6'    WHEN anios_esc <= 8  THEN '7-8'
                WHEN anios_esc = 9   THEN '9'    WHEN anios_esc <= 11 THEN '10-11' WHEN anios_esc = 12 THEN '12'
                WHEN anios_esc <= 15 THEN '13-15' WHEN anios_esc = 16 THEN '16'    ELSE '17+' END AS anios,
           ingocup_pesos, fac_tri
    FROM base WHERE anios_esc IS NOT NULL AND ingocup_pesos IS NOT NULL
), medias AS (
    SELECT ambito, orden, anios, count(*) AS n,
           sum(ingocup_pesos * fac_tri) / sum(fac_tri) AS ingreso_medio
    FROM tramos GROUP BY ambito, orden, anios
)
SELECT ambito, anios AS anios_escolaridad, n, round(ingreso_medio) AS ingreso_medio,
       round(100.0 * (ingreso_medio / lag(ingreso_medio) OVER (PARTITION BY ambito ORDER BY orden) - 1), 1)
           AS cambio_pct_vs_tramo_anterior
FROM medias
ORDER BY ambito DESC, orden;

-- Q15 | Que parte de los ocupados trabaja en cada sector, en SLP y en el pais?
-- Concepto: sum(...) OVER (PARTITION BY ambito) como denominador SIN subconsulta extra.
-- Combina GROUP BY (cuenta por sector) con una ventana (total del ambito) en una sola pasada.
WITH base AS (
    SELECT 'Nacional' AS ambito, * FROM clean.ocupados_2026t2
    UNION ALL
    SELECT 'San Luis Potosí', * FROM clean.ocupados_2026t2 WHERE cve_ent = 24
)
SELECT s.nombre AS sector, b.ambito,
       sum(b.fac_tri) AS poblacion_ocupada,
       round(100.0 * sum(b.fac_tri) / sum(sum(b.fac_tri)) OVER (PARTITION BY b.ambito), 1) AS pct_del_total
FROM base b
JOIN cat.sector s USING (rama)
GROUP BY s.nombre, b.ambito
ORDER BY s.nombre, b.ambito DESC;
