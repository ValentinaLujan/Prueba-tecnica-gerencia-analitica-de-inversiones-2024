-- Query para el portafolio de cada cliente
SELECT 
    h.id_sistema_cliente AS cliente_id,
    COUNT(*) AS total_transacciones,
    SUM(h.aba) AS suma_aba,
    AVG(h.aba) AS promedio_aba
FROM 
    historico_aba_macroactivos h
WHERE 
    h.id_sistema_cliente IS NOT NULL
GROUP BY 
    h.id_sistema_cliente
ORDER BY 
    total_transacciones DESC;

-- Porcentaje de activos y macroactivos para portafolio_cliente
SELECT 
	COALESCE(id_sistema_cliente, 'sin cliente') as id_sistema_cliente, 
    ROUND(COUNT(macroactivo) * 100.0 / (SELECT COUNT(*) FROM historico_aba_macroactivos) , 2) as porcentaje_macro,  
    ROUND(COUNT(cod_activo) * 100.0 / (SELECT COUNT(*) FROM historico_aba_macroactivos), 2) as porcentajea_activo 
FROM 
    historico_aba_macroactivos 
GROUP BY 
    id_sistema_cliente;

-- Query para el portafolio por banca
SELECT 
    h.cod_banca,
    cb.banca,
    COUNT(*) AS total_transacciones,
    SUM(h.aba) AS suma_aba,
    AVG(h.aba) AS promedio_aba
FROM 
    historico_aba_macroactivos h
JOIN 
    catalogo_banca cb ON h.cod_banca = cb.cod_banca
GROUP BY 
    h.cod_banca, cb.banca
ORDER BY 
    total_transacciones DESC;

-- Porcentaje de macroactivos para portafolio_banca
SELECT 
    cb.banca,
    hm.cod_banca, 
    ROUND(COUNT(hm.macroactivo) * 100.0 / (SELECT COUNT(*) FROM historico_aba_macroactivos) , 2) as porcentajeMacro
FROM
    historico_aba_macroactivos hm
JOIN
    catalogo_banca cb ON hm.cod_banca = cb.cod_banca
GROUP BY 
    hm.cod_banca,
    cb.banca;


-- Query para el portafolio por perfil de riesgo
SELECT 
    h.cod_perfil_riesgo,
    p.perfil_riesgo,
    COUNT(*) AS total_transacciones,
    SUM(h.aba) AS suma_aba,
    AVG(h.aba) AS promedio_aba
FROM 
    historico_aba_macroactivos h
JOIN 
    cat_perfil_riesgo p ON h.cod_perfil_riesgo = p.cod_perfil_riesgo
GROUP BY 
    h.cod_perfil_riesgo, p.perfil_riesgo
ORDER BY 
    total_transacciones DESC;

-- Porcentaje de macroactivos para portafolio_perfil_riesgo
SELECT 
    cpr.perfil_riesgo,
    hm.cod_perfil_riesgo, 
    ROUND(COUNT(hm.macroactivo) * 100.0 / (SELECT COUNT(*) FROM historico_aba_macroactivos) , 2) as porcentajeMacro
FROM
    historico_aba_macroactivos hm
JOIN
    cat_perfil_riesgo cpr ON hm.cod_perfil_riesgo = cpr.cod_perfil_riesgo
GROUP BY 
    hm.cod_perfil_riesgo,
    cpr.perfil_riesgo;

-- Query para la evolución mes a mes del ABA promedio
-- Declaración de variables para las fechas de inicio y fin
DECLARE @fecha_inicio DATE = '2024-01-01';
DECLARE @fecha_fin DATE = '2024-12-31';

-- Consulta para la evolución mes a mes del ABA promedio del total del portafolio
-- Se deben definir las fechas de inicio y fin, reemplazando '2023-01-01' y '2024-12-31' con las fechas deseadas
-- Estas fechas pueden ser modificadas según sea necesario
SELECT 
    DATE_TRUNC('month', DATE(h.ingestion_year || '-' || h.ingestion_month || '-01')) AS mes,
    AVG(h.aba) AS aba_promedio
FROM 
    historico_aba_macroactivos h
WHERE 
    DATE(ingestion_date) BETWEEN '2023-01-01' AND '2024-12-31'
GROUP BY 
    mes
ORDER BY 
    mes;

-- Query para porcentaje que representa cada activo 
WITH conteo_activos AS (
    SELECT 
        cod_activo,
        COUNT(*) AS total_activos
    FROM 
        historico_aba_macroactivos
    GROUP BY 
        cod_activo
),
total_total_activos AS (
    SELECT 
        SUM(total_activos) AS suma_total_activos
    FROM 
        conteo_activos
)
SELECT 
    c.cod_activo,
    a.activo,
    c.total_activos,
    ROUND((c.total_activos / (SELECT suma_total_activos FROM total_total_activos)) * 100, 2) AS porcentaje_total
FROM 
    conteo_activos c
JOIN 
    catalogo_activos a ON c.cod_activo = a.cod_activo
ORDER BY 
    porcentaje_total DESC;

-- Porcentaje que representa cada macroactivo
WITH conteo_macroactivos AS (
    SELECT 
        macroactivo,
        COUNT(*) AS total_macroactivos
    FROM 
        historico_aba_macroactivos
    GROUP BY 
        macroactivo
),
total_total_macroactivos AS (
    SELECT 
        SUM(total_macroactivos) AS suma_total_macroactivos
    FROM 
        conteo_macroactivos
)
SELECT 
    c.macroactivo,
    c.total_macroactivos,
    ROUND((c.total_macroactivos / (SELECT suma_total_macroactivos FROM total_total_macroactivos)) * 100, 2) AS porcentaje_total
FROM 
    conteo_macroactivos c
ORDER BY 
    porcentaje_total DESC;