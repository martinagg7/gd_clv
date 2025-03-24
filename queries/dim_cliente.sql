--Tabla Cliente: Con toda la información de los clientes,código postal,zonas renta....
--Se unen las tablas clientes,cp y mosaic.

SELECT 
    --Clientes
    c.Customer_ID,--PK:tabla clientes
    c.Edad,
    c.RENTA_MEDIA_ESTIMADA,
    c.ENCUESTA_ZONA_CLIENTE_VENTA,
    c.ENCUESTA_CLIENTE_ZONA_TALLER,
    c.GENERO,
    c.CODIGO_POSTAL,--FK
    c.Fecha_nacimiento,
    c.STATUS_SOCIAL,

    --Código Postal
    cp.provincia,
    cp.poblacion,
    cp.codigopostalid,
    cp.lat,
    cp.lon,

    --Mosaic
    m.U,
    m.PROV,
    m.PROV_INE,--PENSARME SI ELIMINAR
    m.Max_Mosaic,
    m.Max_Mosaic1,
    m.A,
    m.B,
    m.C,
    m.D,
    m.E,
    m.F,
    m.G,
    m.H,
    m.I,
    m.J,
    m.K,
    m.Max_Mosaic_G,
    m.Max_Mosaic2,
    m.Renta_Media,
    m.F2,
    m.Count,
    m.Mosaic_number,
    m.[Check] 
    
--Joins(Left join desde la tabla clientes a la tabla cp y de la tabla cp a la tabla mosaic)
FROM [DATAEX].[003_clientes] c
LEFT JOIN [DATAEX].[005_cp] cp 
    ON c.CODIGO_POSTAL = cp.CP  -- 1º LEFT JOIN de clientes con al tabla CP
LEFT JOIN [DATAEX].[019_Mosaic] m
    ON cp.CP = CONCAT('CP', CAST(m.CP AS VARCHAR(10))); --2º LEFT JOIN de la tabla CP con la tabla Mosaic
    
