-- 📌 Análisis de Fechas en las Tablas 001_Sales y 002_Date
SELECT COUNT(DISTINCT [Sales_Date]) AS Total_Sales_Dates FROM [DATAEX].[001_sales];
SELECT COUNT(DISTINCT [Date]) AS Total_date_dates FROM [DATAEX].[002_date];

SELECT COUNT(DISTINCT [Sales_Date]) AS dates_comunes FROM [DATAEX].[001_sales] INNER JOIN [DATAEX].[002_date] ON [DATAEX].[001_sales].[Sales_Date] = [DATAEX].[002_date].[Date];

-- La tabla 002_Date tiene más fechas que la tabla 001_Sales.
-- Sin embargo, hemos visto que el número de fechas en común entre ambas es 2135.
-- Esto indica que todas las fechas en 001_Sales existen en 002_Date, pero hay fechas adicionales en 002_Date que no tienen ventas asociadas.
-- Debemos evaluar si eliminamos estas fechas que no se corresponden a ninguna venta o si las mantenemos en la base de datos.

-- 📌 Análisis de Clientes en las Tablas 001_Sales y 003_Cliente
SELECT COUNT(DISTINCT Customer_ID ) AS total_clientes_ventas FROM [DATAEX].[001_sales];
SELECT COUNT(DISTINCT Customer_ID) AS total_clientes FROM [DATAEX].[003_clientes] ;
--Ambas tablas tienen la misma cantidad de clientes,44053.

-- 📌 Análisis de revisiones
SELECT s.code, COUNT(r.code) AS total_revisiones
FROM [DATAEX].[001_sales] s
INNER JOIN [DATAEX].[004_rev] r ON s.code = r.code
GROUP BY s.code
ORDER BY total_revisiones DESC;

SELECT COUNT(*) AS total_ventas
FROM [DATAEX].[001_Sales];

SELECT COUNT(*) AS total_revisiones
FROM [DATAEX].[004_rev];

--Cada venta tiene un regsitros asociado en la tabla 004_rev.

--- 📌 Análisis de Códigos Postales en la Tabla 003_Clientes
SELECT CODIGO_POSTAL, COUNT(*) AS TOTAL_CLIENTES
FROM [DATAEX].[003_clientes]
GROUP BY CODIGO_POSTAL
ORDER BY TOTAL_CLIENTES DESC;
--Varios clientes tienen el mismo código postal.

SELECT COUNT(DISTINCT CODIGO_POSTAL) AS total_codigos_postales_CLIENTES
FROM [DATAEX].[003_clientes];

SELECT COUNT(DISTINCT CP) AS total_codigos_postales_CP FROM [DATAEX].[005_cp];
--Hay mas codigos postales distitnos en la tabla 005_cp que en la tabla 003_clientes.



-- 📌 Análisis de Productos en las Tablas 001_Sales y 006_Producto
--Para cada producto, cuántas veces fue vendido
SELECT Id_Producto ,COUNT(*) AS TOTAL_VENTAS
FROM [DATAEX].[001_sales]
GROUP BY Id_Producto
ORDER BY TOTAL_VENTAS DESC;
--Para comprobar si hya proudcuto sin ventas.
SELECT COUNT(DISTINCT Id_Producto) AS total_productos_ventas
FROM [DATAEX].[001_sales];

SELECT COUNT(DISTINCT Id_Producto) AS total_productos
FROM [DATAEX].[006_producto]

-- 📌 Análisis de Quejas en las Tablas 001_Sales y 008_CAC

SELECT * FROM [DATAEX].[001_sales]
SELECT * FROM [DATAEX].[008_cac]


SELECT count(DISTINCT CODE) FROM [DATAEX].[001_sales] as codigos_ventas
SELECT count(DISTINCT CODE) FROM [DATAEX].[008_cac] as codigos_cac

SELECT s.CODE, COUNT(c.CODE) AS total_quejas
FROM [DATAEX].[001_sales] s
LEFT JOIN [DATAEX].[008_cac] c ON s.CODE = c.CODE
GROUP BY s.CODE
ORDER BY total_quejas desc;
--Cada queja esta asociada a una venta y cada venta esta asociada a una queja, peor hay ventas que no tienen quejas asociadas.

-- 📌 Análisis de Edad en las Tablas 001_Sales y 018_Edad
SELECT * FROM [DATAEX].[018_edad]
SELECT COUNT(DISTINCT CODE ) FROM [DATAEX].[018_edad] as codigos_edad
SELECT COUNT(DISTINCT CODE) FROM [DATAEX].[001_sales] as codigos_ventas

SELECT COUNT(*) AS coches_sin_edad
FROM [DATAEX].[001_sales] s
LEFT JOIN [DATAEX].[018_edad] c ON s.code = c.code
WHERE c.code IS NULL;

-- hay 559 coches sin edad

-- 📌 Análisis de Provincias en las Tablas 003_Clientes y 012_Provincia
select * from [DATAEX].[003_clientes] ORDER BY CODIGO_POSTAL DESC;
select * from [DATAEX].[019_Mosaic] ORDER BY CP DESC
select * from [DATAEX].[005_cp]
select * from [DATAEX].[012_provincia]

select count(DISTINCT CODIGO_POSTAL) AS total_codigos_postales_CLIENTES
FROM [DATAEX].[003_clientes];

select count(DISTINCT CP) AS total_codigos_postales_CP FROM [DATAEX].[005_cp];

select count(DISTINCT CP) AS total_codigos_postales_mosaic FROM [DATAEX].[019_Mosaic];

--Hay menos coidfos postales en mosci que en clientes 