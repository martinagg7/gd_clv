--Select *  from[DATAEX].[011_tienda]
--select * from [DATAEX].[012_provincia]
--select * from [DATAEX].[013_zona]



--Tabla Geografica:  Hacemos un LEFT JOIN de la tabla tienda con las tablas PROVINCIA y ZONA.

SELECT 
    tienda.[TIENDA_ID],
    tienda.[PROVINCIA_ID],
    tienda.[ZONA_ID],
    tienda.[TIENDA_DESC],
    provincia.[PROV_DESC],
    zona.[ZONA]

FROM [DATAEX].[011_tienda] as tienda
LEFT JOIN [DATAEX].[012_provincia] as provincia 
    ON tienda.PROVINCIA_ID = provincia.PROVINCIA_ID
LEFT JOIN [DATAEX].[013_zona] as zona
    ON tienda.ZONA_ID = zona.ZONA_ID;
 

