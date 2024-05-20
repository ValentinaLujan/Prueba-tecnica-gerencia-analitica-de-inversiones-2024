-- INGESTION_YEAR
SELECT 
    MAX(ingestion_year) AS max_ingestion_year, -- se verifica que sea coherente
    MIN(ingestion_year) AS min_ingestion_year -- se verifica que sea coherente
FROM 
    historico_aba_macroactivos;

-- INGESTION_MONTH
SELECT 
    MAX(ingestion_month) AS max_ingestion_month, -- se verifica que sea coherente
    MIN(ingestion_month) AS min_ingestion_month -- se verifica que sea coherente
FROM 
    historico_aba_macroactivos;

-- INGESTION_DAY
SELECT 
    MAX(ingestion_day) AS max_ingestion_day, -- No se verifica que sea coherente
    MIN(ingestion_day) AS min_ingestion_day -- se verifica que sea coherente
FROM 
    historico_aba_macroactivos;
-- convertir a Null aquellos valores que no se encuentren entre 1 y 31 
UPDATE historico_aba_macroactivos
SET ingestion_day = CASE
    WHEN ingestion_day < 1 OR ingestion_day > 31 THEN NULL
    ELSE ingestion_day
END;
-- arreglar algunas columnas que estan desplazadas
UPDATE historico_aba_macroactivos
SET 
    month = year,
    year = cod_banca,
    cod_banca = cod_perfil_riesgo,
    cod_perfil_riesgo = aba,
    cod_activo = macroactivo,
    macroactivo = id_sistema_cliente,
    id_sistema_cliente = NULL 
WHERE
    id_sistema_cliente IN ('100FICs', '100Renta Fija', '100Renta Variable');


-- ID_SISTEMA_CLIENTE
-- Convertir de notación científica a decimal
UPDATE historico_aba_macroactivos
SET id_sistema_cliente = CAST(id_sistema_cliente AS NUMERIC)
WHERE id_sistema_cliente ~* '^[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?$';

-- MACROACTIVO
-- Convertir a Null los valores numericos
UPDATE historico_aba_macroactivos
SET macroactivo = NULL
WHERE macroactivo ~ '^\d+(\.\d+)?$';
-- Quitarle el 100 del inicio a aquellos registros que fueron desplazados anteriormente
UPDATE historico_aba_macroactivos
SET macroactivo = SUBSTRING(macroactivo FROM 4)
WHERE macroactivo LIKE '100%';

-- COD_ACTIVO
-- Eliminar un 0 de aquellos registros que tienen 5 digitos 
UPDATE historico_aba_macroactivos
SET cod_activo = 
    CASE 
        WHEN length(cod_activo) = 5 THEN 
            substr(cod_activo, 1, 1) || substr(cod_activo, 3)
        ELSE
            cod_activo
    END
WHERE length(cod_activo) = 5;
-- convertir Null los registros en la columna cod_activo que no coinciden con los
-- que estan en la tabla catalogo_activos
UPDATE historico_aba_macroactivos
SET cod_activo = NULL
WHERE cod_activo NOT IN (
    SELECT cod_activo FROM catalogo_activos
);

-- convertir la columna cod_activo a una clave foranea que referencie a la 
-- columna cod_activo de la tabla catalogo_activos
ALTER TABLE historico_aba_macroactivos
ADD CONSTRAINT fk_cod_activo
FOREIGN KEY (cod_activo)
REFERENCES catalogo_activos (cod_activo);

-- ABA
UPDATE historico_aba_macroactivos
SET aba = NULL
WHERE NOT aba::text ~ '^\d+(\.\d+)?$';

-- COD_PERFIL_RIESGO
-- Eliminar un 0 de aquellos registros que tienen 5 digitos 
UPDATE historico_aba_macroactivos
SET cod_perfil_riesgo = 
    CASE 
        WHEN length(cod_perfil_riesgo) = 5 THEN 
            substring(cod_perfil_riesgo from 1 for 1) || substring(cod_perfil_riesgo from 3)
        ELSE
            cod_perfil_riesgo
    END
WHERE length(cod_perfil_riesgo) = 5;

-- cambiar por Null los registros en la columna cod_perfil_riesgo que no coinciden con los
-- que estan en la tabla cat_perfil_riesgo
UPDATE historico_aba_macroactivos
SET cod_perfil_riesgo = NULL
WHERE cod_perfil_riesgo NOT IN (
    SELECT cod_perfil_riesgo FROM cat_perfil_riesgo
);

-- convertir la columna cod_perfil_riesgo a una clave foranea que referencie a la 
-- columna cod_perfil_riesgo de la tabla cat_perfil_riesgo
ALTER TABLE historico_aba_macroactivos
ADD CONSTRAINT fk_cod_perfil_riesgo
FOREIGN KEY (cod_perfil_riesgo)
REFERENCES cat_perfil_riesgo (cod_perfil_riesgo);

-- COD_BANCA
-- Eliminar un 0 de aquellos registros que tienen 5 digitos 
UPDATE historico_aba_macroactivos
SET cod_banca = 
    CASE 
        WHEN length(cod_banca) = 5 THEN 
            substring(cod_banca from 1 for 1) || substring(cod_banca from 3)
        ELSE
            cod_banca
    END
WHERE length(cod_banca) = 5;
-- cambiar por Null los registros en la columna cod_banca que no coinciden con los
-- que estan en la tabla catalogo_banca
UPDATE historico_aba_macroactivos
SET cod_banca = NULL
WHERE cod_banca NOT IN (
    SELECT cod_banca FROM catalogo_banca
);

-- convertir la columna cod_banca a una clave foranea que referencie a la 
-- columna cod_banca de la tabla catalogo_banca
ALTER TABLE historico_aba_macroactivos
ADD CONSTRAINT fk_cod_banca
FOREIGN KEY (cod_banca)
REFERENCES catalogo_banca (cod_banca);

-- YEAR 
-- convertir a Null aquellos valores que no sean numericos
UPDATE historico_aba_macroactivos
SET 
    cod_banca = CASE 
                    WHEN year ~ '^\d+$' THEN cod_banca
                    ELSE year
                END,
    year = CASE 
                WHEN year ~ '^\d+$' THEN year
                ELSE NULL
            END;
-- verificar que los valores numericos sean coherentes 
SELECT 
    MAX(year) AS max_year, 
    MIN(year) AS min_year 
FROM 
    historico_aba_macroactivos;
-- asignar el valor de ingestion_year a year en caso de que el valor sea nulo
UPDATE historico_aba_macroactivos
SET year = ingestion_year
WHERE year IS NULL;

-- MONTH 
-- Convertir a NULL aquellos valores que no sean numéricos
-- Si son numéricos, convertirlos a enteros
UPDATE historico_aba_macroactivos
SET 
    month = CASE 
                WHEN month ~ '^\d+$' THEN CAST(month AS INTEGER)
                ELSE NULL
            END;
-- asignar el valor de ingestion_month a month en caso de que el valor sea nulo
UPDATE historico_aba_macroactivos
SET month = ingestion_month
WHERE month IS NULL;


-- FECHA
-- Crear una nueva columna que relacione las columnas ingestion_year, ingestion_month e 
-- ingestion_day para obtener una fecha completa 
ALTER TABLE historico_aba_macroactivos
ADD COLUMN ingestion_date DATE;

UPDATE historico_aba_macroactivos
SET ingestion_date = TO_DATE(
    ingestion_year || '-' ||
    LPAD(ingestion_month::TEXT, 2, '0') || '-' ||
    LPAD(ingestion_day::TEXT, 2, '0'),
    'YYYY-MM-DD'
);