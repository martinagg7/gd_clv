--SELECT * FROM [DATAEX].[006_producto] 
--SELECT * FROM [DATAEX].[014_categoría_producto] 
--SELECT * FROM [DATAEX].[007_costes]
--SELECT * FROM [DATAEX].[015_fuel]


SELECT producto.[CATEGORIA_ID]
        ,producto.[Fuel_ID]
        ,producto.[Id_Producto]
        ,producto.[TRANSMISION_ID]
        ,categoria.[CATEGORIA_ID]
        ,producto.[Kw]
        ,producto.[Code_]
        ,producto.[Modelo]
        ,producto.[TIPO_CARROCERIA]
        ,categoria.[Equipamiento]
        ,costes.[Margen]
        ,costes.[Costetransporte]
        ,costes.[Margendistribuidor]
        ,costes.[GastosMarketing]
        ,costes.[Mantenimiento_medio]
        ,costes.[Comisión_Marca]
        ,fuel.[FUEL]
  FROM [DATAEX].[006_producto] AS producto
    LEFT JOIN [DATAEX].[014_categoría_producto] AS categoria
        ON producto.CATEGORIA_ID = categoria.CATEGORIA_ID
    LEFT JOIN [DATAEX].[007_costes] AS costes
        ON producto.Modelo = costes.Modelo
    LEFT JOIN [DATAEX].[015_fuel] AS fuel
        ON producto.Fuel_ID = fuel.Fuel_ID




  
 