
--Tabla Geografica:Con la información geográfica de las tiendas.
--Se unen las tablas tienda,provincia y zona.

SELECT 
    --Tienda
    tienda.[TIENDA_ID],
    tienda.[PROVINCIA_ID],
    tienda.[ZONA_ID],
    tienda.[TIENDA_DESC],

    --Provincia
    provincia.[PROV_DESC],

    --Zona
    zona.[ZONA]

FROM [DATAEX].[011_tienda] as tienda
LEFT JOIN [DATAEX].[012_provincia] as provincia 
    ON tienda.PROVINCIA_ID = provincia.PROVINCIA_ID
LEFT JOIN [DATAEX].[013_zona] as zona
    ON tienda.ZONA_ID = zona.ZONA_ID;
 

