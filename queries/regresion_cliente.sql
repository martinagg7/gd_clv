--regresion_cliente.sql:Para cada PVP se obtienen estadísticas como la edad media del cliente, margen bruto medio, coste total y más.
--Se  calcula la tasa media de churn, que luego se analizará para encontrar la mejor regresión que prediga la retención de clientes.
SELECT
    f.PVP,
    COUNT(*) AS Numero_Compras,
    AVG(c.Edad) AS Edad_Media_Cliente,
    AVG(f.Car_Age) AS Edad_Media_Coche,
    AVG(f.Margen_Bruto) AS Margen_Bruto_Medio,
    AVG(f.Margen_eur) AS Margen_Eur_Medio,
    AVG(f.Coste_Total) AS Coste_Total,
    AVG(c.RENTA_MEDIA_ESTIMADA) AS Renta_Media,
    AVG(f.Km_medio_por_revision) AS Km_medio_por_revision,
    AVG(f.Revisiones) AS Revisiones_Medias, 
    AVG(f.COSTE_VENTA_NO_IMPUESTOS) AS Coste_Venta_No_Impuestos_Medio,  
    AVG(f.DIAS_EN_TALLER) AS Dias_En_Taller,
    AVG(CAST(f.Churn AS DECIMAL(10,2))) AS churn_medio --Variable objetivo

    
FROM [dwh_case1].[dbo].[dim_fact] f
JOIN [dwh_case1].[dbo].[dim_cliente] c 
    ON f.Customer_ID = c.Customer_ID
GROUP BY f.PVP
ORDER BY f.PVP;
