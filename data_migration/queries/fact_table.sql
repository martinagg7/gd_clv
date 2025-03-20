SELECT 
    S.CODE,
    S.Sales_Date,
    S.Customer_ID,
    S.Id_Producto,
    S.PVP,
    S.MOTIVO_VENTA_ID,
    MV.MOTIVO_VENTA,
    S.FORMA_PAGO_ID,
    FP.FORMA_PAGO, 
    FP.FORMA_PAGO_GRUPO,
    S.SEGURO_BATERIA_LARGO_PLAZO,
    S.MANTENIMIENTO_GRATUITO,
    S.FIN_GARANTIA,
    S.COSTE_VENTA_NO_IMPUESTOS,
    S.IMPUESTOS,
    S.TIENDA_ID,
    S.Code_,
    S.EXTENSION_GARANTIA,
    S.BASE_DATE,
    S.EN_GARANTIA,  
    L.Fue_Lead,
    L.Lead_compra,
    L.Origen_Compra_ID,
    OV.Origen,  
    L.t_prod_date,
    L.t_logist_days,
    L.t_stock_dates,
    L.Prod_date,
    L.Logistic_date,
    R.Revisiones,
    R.Km_medio_por_revision,
    R.km_ultima_revision,
    R.DIAS_DESDE_ULTIMA_REVISION,
    R.DATE_UTIMA_REV,
    C.DIAS_EN_TALLER,
    C.DIAS_DESDE_LA_ULTIMA_ENTRADA_TALLER,
    C.QUEJA,
    E.Car_Age,
    -- Margen_Bruto 
    COST.Margen,  
    ROUND(S.PVP * (COST.Margen / 100) * (1 - S.IMPUESTOS / 100), 2) AS Margen_Bruto,
    --Margen_Eur
    COST.Margendistribuidor,
    COST.GastosMarketing,
    COST.Comisión_Marca,
    COST.Costetransporte,
    ROUND(
        S.PVP * (COST.Margen * 0.01) * (1 - S.IMPUESTOS / 100) - S.COSTE_VENTA_NO_IMPUESTOS - 
        (COST.Margendistribuidor * 0.01 + COST.GastosMarketing * 0.01 - COST.Comisión_Marca * S.PVP * (1 - S.IMPUESTOS / 100)) - COST.Costetransporte, 
        2
    ) AS Margen_Eur

FROM [DATAEX].[001_sales] S
LEFT JOIN [DATAEX].[010_forma_pago] FP 
    ON S.FORMA_PAGO_ID = FP.FORMA_PAGO_ID
LEFT JOIN [DATAEX].[017_logist] L 
    ON S.CODE = L.CODE
LEFT JOIN [DATAEX].[016_origen_venta] OV 
    ON L.Origen_Compra_ID = OV.Origen_Compra_ID
LEFT JOIN [DATAEX].[004_rev] R 
    ON S.CODE = R.CODE
LEFT JOIN [DATAEX].[008_cac] C 
    ON S.CODE = C.CODE
LEFT JOIN [DATAEX].[018_edad] E 
    ON S.CODE = E.CODE
LEFT JOIN [DATAEX].[009_motivo_venta] MV 
    ON S.MOTIVO_VENTA_ID = MV.MOTIVO_VENTA_ID
LEFT JOIN [DATAEX].[006_producto] P 
    ON S.Id_Producto = P.Id_Producto
LEFT JOIN [DATAEX].[007_COSTES] COST 
    ON P.Modelo = COST.Modelo;

