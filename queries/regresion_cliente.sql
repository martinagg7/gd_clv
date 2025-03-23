SELECT
    f.PVP,
    COUNT(*) AS Numero_Compras,  -- Número de compras por precio (PVP)
    AVG(c.Edad) AS Edad_Media_Cliente,
    AVG(f.Car_Age) AS Edad_Media_Coche,
    AVG(f.Margen_Bruto) AS Margen_Bruto_Medio,
    AVG(f.Margen_eur) AS Margen_Eur_Medio,
    AVG(c.RENTA_MEDIA_ESTIMADA) AS Renta_Media,
    AVG(f.Km_medio_por_revision) AS Km_medio_por_revision,
    AVG(f.DIAS_EN_TALLER) AS Dias_En_Taller,
    AVG(f.Coste_Total) AS Coste_Total,
    AVG(CAST(f.Churn AS DECIMAL(10,2))) AS churn_medio  -- Variable objetivo
FROM [dwh_case1].[dbo].[dim_fact] f
JOIN [dwh_case1].[dbo].[dim_cliente] c 
    ON f.Customer_ID = c.Customer_ID
GROUP BY f.PVP
ORDER BY f.PVP;
