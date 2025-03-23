
--Tabla Geografica:Con la información geográfica de las tiendas.
--Se unen las tablas tienda,provincia y zona.

SELECT 
    --Tienda
    tienda.TIENDA_ID,--PK
    tienda.PROVINCIA_ID,--FK
    tienda.ZONA_ID,--FK
    tienda.TIENDA_DESC,

    --Provincia
    provincia.PROV_DESC,

    --Zona
    zona.ZONA

--Joins(Left join de la tabla Tienda con las las tablas Provincia y Zona)
FROM [DATAEX].[011_tienda] as tienda
LEFT JOIN [DATAEX].[012_provincia] as provincia 
    ON tienda.PROVINCIA_ID = provincia.PROVINCIA_ID
LEFT JOIN [DATAEX].[013_zona] as zona
    ON tienda.ZONA_ID = zona.ZONA_ID;
 

