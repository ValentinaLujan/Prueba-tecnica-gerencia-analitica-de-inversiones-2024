-- Crear tablas
CREATE TABLE cat_perfil_riesgo (
    cod_perfil_riesgo VARCHAR(100) PRIMARY KEY,
    perfil_riesgo VARCHAR(50)
);

CREATE TABLE catalogo_activos (
	activo VARCHAR(100),
    cod_activo VARCHAR(100) PRIMARY KEY
);

CREATE TABLE catalogo_banca (
    cod_banca VARCHAR(10) PRIMARY KEY,
    banca VARCHAR(100)
);

CREATE TABLE historico_aba_macroactivos (
    ingestion_year INTEGER,
    ingestion_month INTEGER,
    ingestion_day INTEGER,
    id_sistema_cliente VARCHAR(100) NULL,
    macroactivo VARCHAR(100),
    cod_activo VARCHAR(100) NULL,
    aba DECIMAL(20,10),
    cod_perfil_riesgo VARCHAR(100) NULL,
    cod_banca VARCHAR(100) NULL,
    year VARCHAR(100),
    month VARCHAR(100)
);
