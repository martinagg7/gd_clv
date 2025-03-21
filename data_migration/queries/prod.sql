
SELECT 
        --Producto
        producto.Id_Producto
        ,producto.Code_
        ,producto.CATEGORIA_ID
        ,producto.Fuel_ID
        ,producto.TRANSMISION_ID
        ,producto.Kw
        ,producto.Modelo
        ,producto.TIPO_CARROCERIA
        --Categoría
        ,categoria.Equipamiento
        ,categoria.Grade_ID --Especifica el tipo de equipamiento(0-Low/1,2-Mid/3-Mid-High/4-High)
        --Costes
        ,costes.Margen
        ,costes.Costetransporte
        ,costes.Margendistribuidor
        ,costes.GastosMarketing
        ,costes.Mantenimiento_medio
        ,costes.Comisión_Marca
        --Fuel
        ,fuel.FUEL
  FROM [DATAEX].[006_producto] AS producto
    LEFT JOIN [DATAEX].[014_categoría_producto] AS categoria
        ON producto.CATEGORIA_ID = categoria.CATEGORIA_ID
    LEFT JOIN [DATAEX].[007_costes] AS costes
        ON producto.Modelo = costes.Modelo
    LEFT JOIN [DATAEX].[015_fuel] AS fuel
        ON producto.Fuel_ID = fuel.Fuel_ID




  
 