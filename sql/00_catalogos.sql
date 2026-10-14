-- Catalogos (tablas de referencia) para los JOIN del paso 5.
-- Fuente de los codigos: diccionario de datos SDEMT de INEGI (RNM, catalogo 1121, 4T 2025).
-- Una tabla de catalogo evita repetir CASE WHEN en cada consulta y se une con JOIN por su clave.

CREATE SCHEMA IF NOT EXISTS cat;

DROP TABLE IF EXISTS cat.entidad, cat.nivel_instruccion, cat.sector, cat.formalidad,
                     cat.sexo, cat.tamano_localidad, cat.posicion_ocupacion CASCADE;

CREATE TABLE cat.entidad (cve_ent SMALLINT PRIMARY KEY, nombre TEXT NOT NULL);
INSERT INTO cat.entidad VALUES
 (1,'Aguascalientes'),(2,'Baja California'),(3,'Baja California Sur'),(4,'Campeche'),
 (5,'Coahuila'),(6,'Colima'),(7,'Chiapas'),(8,'Chihuahua'),(9,'Ciudad de México'),
 (10,'Durango'),(11,'Guanajuato'),(12,'Guerrero'),(13,'Hidalgo'),(14,'Jalisco'),
 (15,'Estado de México'),(16,'Michoacán'),(17,'Morelos'),(18,'Nayarit'),(19,'Nuevo León'),
 (20,'Oaxaca'),(21,'Puebla'),(22,'Querétaro'),(23,'Quintana Roo'),(24,'San Luis Potosí'),
 (25,'Sinaloa'),(26,'Sonora'),(27,'Tabasco'),(28,'Tamaulipas'),(29,'Tlaxcala'),
 (30,'Veracruz'),(31,'Yucatán'),(32,'Zacatecas');

-- niv_ins: el 5 (no especificado) ya es NULL en la tabla limpia, por eso no se lista.
CREATE TABLE cat.nivel_instruccion (niv_ins SMALLINT PRIMARY KEY, nombre TEXT NOT NULL, orden SMALLINT NOT NULL);
INSERT INTO cat.nivel_instruccion VALUES
 (1,'Primaria incompleta',1),(2,'Primaria completa',2),(3,'Secundaria completa',3),
 (4,'Medio superior y superior',4);

-- rama: el 7 (no especificado) ya es NULL en la tabla limpia.
CREATE TABLE cat.sector (rama SMALLINT PRIMARY KEY, nombre TEXT NOT NULL);
INSERT INTO cat.sector VALUES
 (1,'Construcción'),(2,'Industria manufacturera'),(3,'Comercio'),(4,'Servicios'),
 (5,'Otros'),(6,'Agropecuario');

CREATE TABLE cat.formalidad (emp_ppal SMALLINT PRIMARY KEY, nombre TEXT NOT NULL);
INSERT INTO cat.formalidad VALUES (1,'Empleo informal'),(2,'Empleo formal');

CREATE TABLE cat.sexo (sexo SMALLINT PRIMARY KEY, nombre TEXT NOT NULL);
INSERT INTO cat.sexo VALUES (1,'Hombre'),(2,'Mujer');

CREATE TABLE cat.tamano_localidad (t_loc_tri SMALLINT PRIMARY KEY, nombre TEXT NOT NULL);
INSERT INTO cat.tamano_localidad VALUES
 (1,'Más de 100,000 habitantes'),(2,'15,000 a 99,999'),(3,'2,500 a 14,999'),(4,'Menos de 2,500');

CREATE TABLE cat.posicion_ocupacion (pos_ocu SMALLINT PRIMARY KEY, nombre TEXT NOT NULL);
INSERT INTO cat.posicion_ocupacion VALUES
 (1,'Subordinados y remunerados'),(2,'Empleadores'),(3,'Cuenta propia'),(4,'Sin pago');

-- Integridad: toda clave de clean.ocupados_2026t2 (salvo NULL) debe existir en su catalogo.
-- Si alguna de estas consultas devuelve filas, hay un codigo sin traducir.
-- (Se ejecutan como verificacion en el runner.)
