# Resultados de las consultas (ENOE 2T 2026)

## Q01 | Cuantos ocupados hay en la MUESTRA, a nivel nacional y en SLP?

```
 ocupados_muestra_nacional  ocupados_muestra_slp
                    189353                  5343
```

## Q02 | Cuantas personas ocupadas representa la encuesta, por entidad (las 10 mayores)?

```
         entidad  n_muestra  poblacion_ocupada
Estado de México       7867            8102275
Ciudad de México       4760            4873434
         Jalisco       5886            3822914
        Veracruz       7594            3310652
          Puebla       6812            3111161
      Nuevo León       5959            2966006
      Guanajuato       7486            2936908
       Michoacán       5175            2218946
         Chiapas       8467            2218580
          Oaxaca       6395            1936523
```

## Q03 | Que porcentaje de los ocupados esta en empleo informal, en cada entidad?

```
            entidad  n_muestra  pct_informal
             Oaxaca       6395          80.1
           Guerrero       5287          77.6
            Chiapas       8467          76.9
            Hidalgo       4615          72.0
           Tlaxcala       5510          72.0
          Michoacán       5175          71.3
             Puebla       6812          70.3
           Veracruz       7594          69.1
            Morelos       4902          67.2
            Tabasco       5135          66.2
           Campeche       7204          61.4
          Zacatecas       4725          61.2
            Yucatán       5544          59.1
            Nayarit       5912          58.9
            Durango       6025          55.5
   Estado de México       7867          55.3
    San Luis Potosí       5343          54.9
         Guanajuato       7486          54.8
            Sinaloa       4920          49.0
            Jalisco       5886          46.5
             Colima       5203          46.2
   Ciudad de México       4760          45.3
       Quintana Roo       4880          45.0
         Tamaulipas       6934          44.4
             Sonora       4998          43.9
     Aguascalientes       5013          42.5
Baja California Sur       4118          39.6
          Querétaro       5284          39.2
    Baja California       7299          36.2
           Coahuila       7225          35.5
          Chihuahua       6876          35.1
         Nuevo León       5959          34.8
```

## Q04 | SLP frente al pais: tasa de informalidad ponderada y SIN ponderar.

```
         ambito  n_muestra  pct_informal_ponderado  pct_sin_ponderar
San Luis Potosí       5343                    54.9              52.1
       Nacional     189353                    55.1              51.9
```

## Q05 | Ingreso mensual medio por nivel de instruccion: SLP vs pais (pregunta 1).

```
        nivel_instruccion          ambito  n_con_ingreso  ingreso_medio
      Primaria incompleta San Luis Potosí            189         6978.0
      Primaria incompleta        Nacional           8596         6830.0
        Primaria completa San Luis Potosí            448         6770.0
        Primaria completa        Nacional          16867         8476.0
      Secundaria completa San Luis Potosí           1248         8893.0
      Secundaria completa        Nacional          41493         9741.0
Medio superior y superior San Luis Potosí           1300        13634.0
Medio superior y superior        Nacional          56362        13777.0
```

## Q06 | Ingreso mensual medio por sector de actividad: SLP vs pais (pregunta 2).

```
                 sector          ambito  n_con_ingreso  ingreso_medio
           Agropecuario San Luis Potosí            333         5756.0
           Agropecuario        Nacional           8982         6834.0
               Comercio San Luis Potosí            559         9058.0
               Comercio        Nacional          23060         9683.0
           Construcción San Luis Potosí            285        10781.0
           Construcción        Nacional          11629        12057.0
Industria manufacturera San Luis Potosí            649        11746.0
Industria manufacturera        Nacional          20734        11244.0
                  Otros San Luis Potosí             27        11331.0
                  Otros        Nacional           1037        18132.0
              Servicios San Luis Potosí           1328        11584.0
              Servicios        Nacional          57563        12187.0
```

## Q07 | Informalidad por nivel de instruccion: SLP vs pais (pregunta 3).

```
        nivel_instruccion          ambito  n_muestra  pct_informal
      Primaria incompleta San Luis Potosí        370          87.9
      Primaria incompleta        Nacional      12102          87.6
        Primaria completa San Luis Potosí        667          77.3
        Primaria completa        Nacional      23622          79.1
      Secundaria completa San Luis Potosí       1941          61.3
      Secundaria completa        Nacional      59263          62.9
Medio superior y superior San Luis Potosí       2332          36.6
Medio superior y superior        Nacional      93866          37.9
```

## Q08 | Informalidad por sector de actividad: SLP vs pais (pregunta 3).

```
                 sector          ambito  n_muestra  pct_informal
           Agropecuario San Luis Potosí        634          89.4
           Agropecuario        Nacional      14846          84.8
               Comercio San Luis Potosí        940          64.0
               Comercio        Nacional      36509          59.0
           Construcción San Luis Potosí        391          79.7
           Construcción        Nacional      15488          80.9
Industria manufacturera San Luis Potosí       1097          23.3
Industria manufacturera        Nacional      30652          36.6
                  Otros San Luis Potosí         44          25.5
                  Otros        Nacional       1655          19.1
              Servicios San Luis Potosí       2197          49.7
              Servicios        Nacional      88771          48.7
```

## Q09 | En SLP, que sectores tienen al menos 100 observaciones con ingreso y cual es su ingreso medio?

```
                 sector  n_con_ingreso  ingreso_medio
Industria manufacturera            649        11746.0
              Servicios           1328        11584.0
           Construcción            285        10781.0
               Comercio            559         9058.0
           Agropecuario            333         5756.0
```

## Q10 | Que fraccion del ingreso nacional medio gana SLP, por nivel de instruccion?

```
        nivel_instruccion  nacional     slp  razon_slp_nacional
      Primaria incompleta    6830.0  6978.0                1.02
        Primaria completa    8476.0  6770.0                0.80
      Secundaria completa    9741.0  8893.0                0.91
Medio superior y superior   13777.0 13634.0                0.99
```

## Q11 | En SLP, cuanto mas ganan los formales que los informales dentro de cada sector?

```
                 sector  ingreso_formal  ingreso_informal  razon_formal_informal  n_minimo_celda
              Servicios         15959.0            7650.0                   2.09             646
           Construcción         18640.0            9135.0                   2.04              50
Industria manufacturera         13407.0            6909.0                   1.94             147
           Agropecuario          9388.0            5206.0                   1.80              47
               Comercio         12411.0            7207.0                   1.72             214
                  Otros         13487.0            7967.0                   1.69              10
```

## Q12 | En que lugar queda SLP entre las 32 entidades en ingreso medio y en informalidad?

```
            entidad  ingreso_medio  lugar_ingreso  pct_informal  lugar_informalidad
Baja California Sur        16016.0              1          39.6                  27
         Nuevo León        15446.0              2          34.8                  32
   Ciudad de México        15052.0              3          45.3                  22
    Baja California        14418.0              4          36.2                  29
          Chihuahua        13753.0              5          35.1                  31
       Quintana Roo        12991.0              6          45.0                  23
             Colima        12927.0              7          46.2                  21
             Sonora        12905.0              8          43.9                  25
           Coahuila        12819.0              9          35.5                  30
     Aguascalientes        12070.0             10          42.5                  26
          Querétaro        11945.0             11          39.2                  28
         Tamaulipas        11778.0             12          44.4                  24
            Sinaloa        11659.0             13          49.0                  19
            Jalisco        11480.0             14          46.5                  20
            Yucatán        10919.0             15          59.1                  13
            Nayarit        10881.0             16          58.9                  14
   Estado de México        10734.0             17          55.3                  16
    San Luis Potosí        10330.0             18          54.9                  17
            Durango        10320.0             19          55.5                  15
         Guanajuato        10208.0             20          54.8                  18
           Campeche        10029.0             21          61.4                  11
          Zacatecas         9991.0             22          61.2                  12
          Michoacán         9294.0             23          71.3                   6
            Hidalgo         9206.0             24          72.0                   5
            Tabasco         8910.0             25          66.2                  10
           Veracruz         8907.0             26          69.1                   8
             Puebla         8739.0             27          70.3                   7
           Tlaxcala         8698.0             28          72.0                   4
            Morelos         8575.0             29          67.2                   9
             Oaxaca         8357.0             30          80.1                   1
           Guerrero         8184.0             31          77.6                   2
            Chiapas         7454.0             32          76.9                   3
```

## Q13 | Percentiles ponderados del ingreso (p25, mediana, p75): SLP vs pais.

```
         ambito    p25  mediana     p75
San Luis Potosí 5160.0   8600.0 12900.0
       Nacional 6450.0   9460.0 12900.0
```

## Q14 | Cuanto sube el ingreso medio al pasar de un grupo de escolaridad al siguiente?

```
         ambito anios_escolaridad     n  ingreso_medio  cambio_pct_vs_tramo_anterior
San Luis Potosí               0-5   188         7009.0                           NaN
San Luis Potosí                 6   366         6649.0                          -5.1
San Luis Potosí               7-8    81         7296.0                           9.7
San Luis Potosí                 9   979         8619.0                          18.1
San Luis Potosí             10-11   230         9529.0                          10.6
San Luis Potosí                12   592        10725.0                          12.5
San Luis Potosí             13-15   155        12292.0                          14.6
San Luis Potosí                16   131        13502.0                           9.8
San Luis Potosí               17+   462        18141.0                          34.4
       Nacional               0-5  8587         6830.0                           NaN
       Nacional                 6 13921         8407.0                          23.1
       Nacional               7-8  2891         8858.0                           5.4
       Nacional                 9 33315         9631.0                           8.7
       Nacional             10-11  6367         9689.0                           0.6
       Nacional                12 27189        10970.0                          13.2
       Nacional             13-15  6244        11632.0                           6.0
       Nacional                16 10890        16389.0                          40.9
       Nacional               17+ 13858        18780.0                          14.6
```

## Q15 | Que parte de los ocupados trabaja en cada sector, en SLP y en el pais?

```
                 sector          ambito  poblacion_ocupada  pct_del_total
           Agropecuario San Luis Potosí             193817           14.7
           Agropecuario        Nacional            6159248           10.3
               Comercio San Luis Potosí             243282           18.4
               Comercio        Nacional           11787987           19.8
           Construcción San Luis Potosí              91985            7.0
           Construcción        Nacional            4841023            8.1
Industria manufacturera San Luis Potosí             259286           19.6
Industria manufacturera        Nacional            9700092           16.3
                  Otros San Luis Potosí              11579            0.9
                  Otros        Nacional             373681            0.6
              Servicios San Luis Potosí             520343           39.4
              Servicios        Nacional           26730972           44.9
```
