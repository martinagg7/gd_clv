-- regresion_cliente.sql:datos necesitamos para estimar la variable churn de un cliente

SELECT
  f.Customer_ID,
  AVG(c.Edad) AS Edad_Media_Cliente,
  AVG(f.Car_Age) AS Edad_Media_Coche,
  AVG(f.Margen_Bruto) AS Margen_Bruto_Medio,
  AVG(f.Margen_eur) AS Margen_Eur_Medio,
  AVG(c.RENTA_MEDIA_ESTIMADA) AS Renta_Media,
  AVG(CAST(f.Churn AS DECIMAL(10,2))) AS churn_medio -- Esto sería la variable objetivo
FROM [dwh_case1].[dbo].[dim_fact] f
JOIN [dwh_case1].[dbo].[dim_cliente] c
  ON f.Customer_ID = c.Customer_ID
GROUP BY f.Customer_ID
ORDER BY f.Customer_ID;
