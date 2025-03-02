-- 📌 Análisis de Fechas en las Tablas 001_Sales y 002_Date

SELECT COUNT(DISTINCT [Sales_Date]) AS Total_Sales_Dates FROM [DATAEX].[001_sales];
SELECT COUNT(DISTINCT [Date]) AS Total_date_dates FROM [DATAEX].[002_date];

SELECT COUNT(DISTINCT [Sales_Date]) AS dates_comunes FROM [DATAEX].[001_sales] INNER JOIN [DATAEX].[002_date] ON [DATAEX].[001_sales].[Sales_Date] = [DATAEX].[002_date].[Date];

-- La tabla 002_Date tiene más fechas que la tabla 001_Sales.
-- Sin embargo, hemos visto que el número de fechas en común entre ambas es 2135.
-- Esto indica que todas las fechas en 001_Sales existen en 002_Date, pero hay fechas adicionales en 002_Date que no tienen ventas asociadas.
-- Debemos evaluar si eliminamos estas fechas que no se corresponden a ninguna venta o si las mantenemos en la base de datos.