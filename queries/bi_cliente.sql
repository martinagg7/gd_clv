
--bi_cliente.sql:En esta consulta se emplean los datos de la consulta vision_cliente.sql y los coeficientes que hemos obtenido de la regresión lineal para calcular el churn, la retención y el CLV de cada cliente.

-- Declaramos las variables para los coeficientes
DECLARE @b0 FLOAT, @b1 FLOAT, @b2 FLOAT, @b3 FLOAT, @b4 FLOAT;

-- Asignamos los valores de la tabla de Regresion_coeficientes
SELECT 
    @b0 = MAX(CASE WHEN Variable = 'Intercepto' THEN Valor END),
    @b1 = MAX(CASE WHEN Variable = 'PVP' THEN Valor END),
    @b2 = MAX(CASE WHEN Variable = 'Edad_Media_Coche' THEN Valor END),
    @b3 = MAX(CASE WHEN Variable = 'Km_medio_por_revision' THEN Valor END),
    @b4 = MAX(CASE WHEN Variable = 'Revisiones_Medias' THEN Valor END)
FROM [dwh_case1].[dbo].[Regresion_Coeficientes];

-- Calculamos churn, retención y CLV para cada cliente 
SELECT 
	vc.Customer_ID,
    vc.Edad,
    vc.RENTA_MEDIA_ESTIMADA,
    vc.GENERO,
    vc.Fecha_nacimiento,
    vc.STATUS_SOCIAL,
    vc.CODIGO_POSTAL,
    vc.provincia,
    vc.poblacion,
    vc.lat,
    vc.lon,
    vc.Origen_Compra,
    vc.Fue_Lead_Alguna_Vez,
    vc.Numero_Veces_Lead,
    vc.Total_Compras,
    vc.Modelos_Comprados,
    vc.PVP_Total,
    vc.PVP_Medio, -- Regresión lineal
    vc.PVP_Diferencia,
    vc.Dias_Entre_Primera_Ultima_Compra,
    vc.Ultima_Compra,
    vc.Dias_Desde_Ultima_Compra,
    vc.Compra_Finde_O_Festivo,
    vc.Edad_Media_Coche, -- Regresión lineal
    vc.Total_Revisiones, -- Regresión lineal
    vc.Km_Medio_por_Revision, -- Regresión lineal
    vc.Tuvo_Mantenimiento_Gratuito,
    vc.Dias_Medio_En_Taller,
    vc.Total_Quejas,
    vc.Compra_Tienda_Unica,
    vc.Contrato_Seguro_Bateria,
    vc.Coste_Medio_Cliente,
    vc.Margen_Bruto_Medio,
    vc.Margen_eur_Medio,
    vc.Rentabilidad_Relativa,

    -- Calculamos churn medio y lo limitamos entre [0,1](puesto que hay valores negativos)
    GREATEST(0, LEAST(1, (
        @b0 + @b1 * vc.PVP_Medio + @b2 * vc.Edad_Media_Coche 
        + @b3 * vc.Km_Medio_por_Revision + @b4 * vc.Total_Revisiones
    ))) AS churn_medio_estimado,

    -- Calculamos retención y la limitamos entre [0,1]
    GREATEST(0, LEAST(1, (
        1 - (@b0 + @b1 * vc.PVP_Medio + @b2 * vc.Edad_Media_Coche 
        + @b3 * vc.Km_Medio_por_Revision + @b4 * vc.Total_Revisiones)
    ))) AS retencion,


    /**ANOTACIÓN**:
        como hay clientes con retención negativa y hemos limitado el valor entre [0,1], el CLV a 5 años 
        CLV_5_anos=0 cuando la retención es negativa,
    */

    -- CLV a 5 años: Ret^t / (1+i)^t * Margen_eur_Medio
    vc.Margen_eur_Medio * (
        POWER(GREATEST(0, LEAST(1, 1 - (@b0 + @b1 * vc.PVP_Medio + @b2 * vc.Edad_Media_Coche + @b3 * vc.Km_Medio_por_Revision + @b4 * vc.Total_Revisiones))), 1) / POWER(1.07, 1) +
        POWER(GREATEST(0, LEAST(1, 1 - (@b0 + @b1 * vc.PVP_Medio + @b2 * vc.Edad_Media_Coche + @b3 * vc.Km_Medio_por_Revision + @b4 * vc.Total_Revisiones))), 2) / POWER(1.07, 2) +
        POWER(GREATEST(0, LEAST(1, 1 - (@b0 + @b1 * vc.PVP_Medio + @b2 * vc.Edad_Media_Coche + @b3 * vc.Km_Medio_por_Revision + @b4 * vc.Total_Revisiones))), 3) / POWER(1.07, 3) +
        POWER(GREATEST(0, LEAST(1, 1 - (@b0 + @b1 * vc.PVP_Medio + @b2 * vc.Edad_Media_Coche + @b3 * vc.Km_Medio_por_Revision + @b4 * vc.Total_Revisiones))), 4) / POWER(1.07, 4) +
        POWER(GREATEST(0, LEAST(1, 1 - (@b0 + @b1 * vc.PVP_Medio + @b2 * vc.Edad_Media_Coche + @b3 * vc.Km_Medio_por_Revision + @b4 * vc.Total_Revisiones))), 5) / POWER(1.07, 5)
    ) AS CLV_5_anos

FROM dwh_case1.dbo.vision_cliente vc;