--Tabla Fact: Con toda la información de las ventas.
--Se unen las tablas sales,forma_pago,logistica,origen_venta,revisiones,cac,edad y costes.

SELECT  

    --Sales
    S.CODE,--PK:tabla sales
    S.Code_,
    S.Customer_ID,--FK
    S.Id_Producto,--FK
    S.TIENDA_ID,--FK
    S.MOTIVO_VENTA_ID,--FK
    S.FORMA_PAGO_ID,--FK
    CONVERT(DATE, S.Sales_Date, 103) AS Sales_Date,
    S.PVP,
    S.SEGURO_BATERIA_LARGO_PLAZO,
    S.MANTENIMIENTO_GRATUITO,
    CONVERT(DATE, FIN_GARANTIA, 103) AS FIN_GARANTIA,
    S.COSTE_VENTA_NO_IMPUESTOS,
    S.IMPUESTOS,
    S.EXTENSION_GARANTIA,
    CONVERT(DATE, S.BASE_DATE, 103) AS BASE_DATE,
    S.EN_GARANTIA,

    --Forma_pago
    FP.FORMA_PAGO, 
    FP.FORMA_PAGO_GRUPO,

    --Logistica
    L.Fue_Lead,
    L.Lead_compra,
    L.t_prod_date,
    L.t_logist_days,
    L.t_stock_dates,
    CONVERT(DATE, L.Prod_date, 103) AS Prod_date,
    CONVERT(DATE, L.Logistic_date, 103) AS Logistic_date,
    L.Origen_Compra_ID,--FK:tabla origen_venta

    --0rigen_venta
    OV.Origen,

    --Revisiones
    R.Revisiones,
    R.Km_medio_por_revision,
    R.km_ultima_revision,
    --Como la variable dias_desde_ultima_revision estaba en formato varchat y con puntos, se ha tenido que hacer un cast a INT
    TRY_CAST(REPLACE(R.DIAS_DESDE_ULTIMA_REVISION, '.', '') AS INT) as DIAS_DESDE_ULTIMA_REVISION,
    --Fecha Ultima Revision
    CASE 
        WHEN R.DATE_UTIMA_REV IS NULL 
            OR LTRIM(RTRIM(R.DATE_UTIMA_REV)) = ''--Si la fecha es nula o vacía,ponemos Null en vez de 1900-01-01
        THEN NULL
        ELSE CONVERT(DATE, R.DATE_UTIMA_REV, 103)
    END AS Fecha_Ultima_Revision,


    --CAC
    C.DIAS_EN_TALLER,
    C.DIAS_DESDE_LA_ULTIMA_ENTRADA_TALLER,
    C.QUEJA,

    --Edad Coche
    E.Car_Age,


--MÉTRICAS:

    -- Margen_Bruto   
    ROUND(S.PVP * (COST.Margen / 100) * (1 - S.IMPUESTOS / 100), 2) AS Margen_Bruto,
    
    --Margen_Eur
    ROUND(S.PVP * (COST.Margen)*0.01 * (1 - S.IMPUESTOS / 100) - S.COSTE_VENTA_NO_IMPUESTOS - (COST.Margendistribuidor*0.01 + COST.GastosMarketing*0.01-COST.Comisión_Marca*0.01) * S.PVP * (1 - S.IMPUESTOS / 100) - COST.Costetransporte, 2) AS Margen_eur

    --Coste Venta
    ,ROUND(S.COSTE_VENTA_NO_IMPUESTOS +((COST.Margendistribuidor * 0.01 + COST.GastosMarketing * 0.01 - COST.Comisión_Marca * 0.01) * S.PVP * (1 - S.IMPUESTOS / 100)) +COST.Costetransporte,2
    ) AS Coste_Total


    --Variable Churn(1:dias_desde_ultima_revision >401, 0 :caso contrario)
    ,CASE
        WHEN TRY_CAST(REPLACE(R.DIAS_DESDE_ULTIMA_REVISION, '.', '') AS INT) > 401 THEN 1
        ELSE 0
    END AS Churn
   
--Joins para la tabla fact(siempre left join sales con las demás tablas para no perder información)
FROM [DATAEX].[001_sales] S
LEFT JOIN [DATAEX].[010_forma_pago] FP 
    ON S.FORMA_PAGO_ID = FP.FORMA_PAGO_ID
LEFT JOIN [DATAEX].[017_logist] L 
    ON S.CODE = L.CODE
LEFT JOIN [DATAEX].[016_origen_venta] OV 
    ON L.Origen_Compra_ID = OV.Origen_Compra_ID --Join entre la tabla logistica y origen_venta
LEFT JOIN [DATAEX].[004_rev] R 
    ON S.CODE = R.CODE
LEFT JOIN [DATAEX].[008_cac] C 
    ON S.CODE = C.CODE
LEFT JOIN [DATAEX].[018_edad] E 
    ON S.CODE = E.CODE
LEFT JOIN [DATAEX].[009_motivo_venta] MV 
    ON S.MOTIVO_VENTA_ID = MV.MOTIVO_VENTA_ID
LEFT JOIN [DATAEX].[006_producto] P 

--Joins para las métricas
    ON S.Id_Producto = P.Id_Producto
LEFT JOIN [DATAEX].[007_COSTES] COST 
    ON P.Modelo = COST.Modelo

oRDER BY  Customer_ID
;

