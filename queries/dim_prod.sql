--Tabla Producto: Con toda la información de los productos.
--Se unen las tablas producto,categoría,costes y fuel.

SELECT 
        --Producto
        producto.Id_Producto--PK
        ,producto.Code_
        ,producto.CATEGORIA_ID--FK
        ,producto.Fuel_ID--FK
        ,producto.TRANSMISION_ID
        ,producto.Kw
        ,producto.Modelo--FK
        ,producto.TIPO_CARROCERIA

        --Categoría
        ,categoria.Equipamiento
        ,categoria.Grade_ID 

        --Costes
        ,costes.Margen
        ,costes.Costetransporte
        ,costes.Margendistribuidor
        ,costes.GastosMarketing
        ,costes.Mantenimiento_medio
        ,costes.Comisión_Marca
        
        --Fuel
        ,fuel.FUEL

--Joins(Left join de la tabla producto con las las tablas categoría, costes y fuel)
  FROM [DATAEX].[006_producto] AS producto
    LEFT JOIN [DATAEX].[014_categoría_producto] AS categoria
        ON producto.CATEGORIA_ID = categoria.CATEGORIA_ID
    LEFT JOIN [DATAEX].[007_costes] AS costes
        ON producto.Modelo = costes.Modelo
    LEFT JOIN [DATAEX].[015_fuel] AS fuel
        ON producto.Fuel_ID = fuel.Fuel_ID




  
 