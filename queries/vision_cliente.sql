-- vision_cliente.sql: Consulta que devuelve un conjunto de métricas descriptivas y agregadas por cliente,

SELECT 
--MEDIDAS DESCRIPTIVAS POR CLIENTE
  c.Customer_ID,
  c.Edad,
  c.RENTA_MEDIA_ESTIMADA,
  c.GENERO,
  c.Fecha_nacimiento,
  c.STATUS_SOCIAL,
  c.CODIGO_POSTAL,
  c.provincia,
  c.poblacion,
  c.lat,
  c.lon,

--MÉTRICAS AGREGRADAS POR CLIENTE(Calculadas a través fact)


--1. ORIGEN Y CAPTACION
  -- origen_compra:canal principal de compra (internet, tienda, ambos o desconocido)
  CASE 
    WHEN COUNT(DISTINCT f.Origen) = 2 THEN 'Ambos'
    WHEN MIN(f.Origen) = 'Internet' THEN 'Internet'
    WHEN MIN(f.Origen) = 'Tienda' THEN 'Tienda'
    ELSE 'Desconocido'
  END AS Origen_Compra,

  -- fue_lead_alguna_vez:indica si el cliente fue registrado como lead (1=si, 0=no)
  MAX(f.Fue_Lead) AS Fue_Lead_Alguna_Vez,

  -- numero_veces_lead:número total de veces que fue registrado como lead
  SUM(f.Fue_Lead) AS Numero_Veces_Lead,


 -- 2.COMPORTAMIENTO DE COMPRA
  -- total_compras:número de vehiculos adquiridos
  COUNT(f.Customer_ID) AS Total_Compras,

  -- pvp_total: cantidad total gastada  en compras
  SUM(f.PVP) AS PVP_Total,

  -- pvp_medio: precio promedio gastado por compra
  AVG(f.PVP) AS PVP_Medio,

  -- pvp_diferencia: diferencia entre la compra más cara y la más barata (si hay más de una)
  CASE 
    WHEN COUNT(f.Customer_ID) > 1 THEN MAX(f.PVP) - MIN(f.PVP)
    ELSE 0 
  END AS PVP_Diferencia,

  -- dias_entre_primera_ultima_compra:días entre la primera y la última compra

    DATEDIFF(
        DAY,
        MIN(f.Sales_Date),
        MAX(f.Sales_Date)
    ) AS Dias_Entre_Primera_Ultima_Compra,

    -- dias_desde_ultima_compra:días desde la última compra
    DATEDIFF(
        DAY,
        MAX(f.Sales_Date),
        GETDATE()
    ) AS Dias_Desde_Ultima_Compra,

  -- compra_finde_o_festivo:indica si se realizó alguna compra en fines de semana o festivos (1=si, 0=no)
  CASE 
    WHEN SUM(CASE WHEN t.FinDeSemana = 'VERDADERO' OR t.Festivo = 'VERDADERO' THEN 1 ELSE 0 END) > 0
      THEN 1 ELSE 0 
  END AS Compra_Finde_O_Festivo,


 --3.USO Y MANTENIMIENTO
  -- edad_media_coche: promedio de edad de todos los coches del cliente
	 AVG(f.Car_Age) AS Edad_Media_Coche,
	
  -- total_revisiones:total de revisiones o mantenimientos realizados
  SUM(f.Revisiones) AS Total_Revisiones,

  -- km_medio_por_revision:promedio de km recorridos por cada revisión
  AVG(f.Km_medio_por_revision) AS Km_Medio_por_Revision,

  -- tuvo_mantenimiento_gratuito indica si se recibió mantenimiento gratuito (1=si, 0=no)
  CASE 
    WHEN MAX(f.MANTENIMIENTO_GRATUITO) = 4 THEN 1 
    ELSE 0 
  END AS Tuvo_Mantenimiento_Gratuito,

    -- dias_medio_en_taller: días promedio los coches de un cliente estuvieron en el taller
  AVG(f.DIAS_EN_TALLER) AS Dias_Medio_En_Taller,

 --4. SATISFACCION Y SERVICIO
  -- total_quejas:número total de quejas registradas(Las sumamos porque como hay muchos valores null convertidos a 0,podríamos estar sesgando el resultado)
  SUM(CASE WHEN f.QUEJA = 'SI' THEN 1 ELSE 0 END) AS Total_Quejas,

  -- compra_tienda_unica:indica si el cliente siempre ha comprado en la misma tienda (1=si 0=no)
  CASE 
    WHEN COUNT(DISTINCT f.TIENDA_ID) = 1 THEN 1  
    ELSE 0 
  END AS Compra_Tienda_Unica,

  -- contrato_seguro_bateria:indica si se ha contratado alguna vez el seguro de batería (1=si 0=no)
  CASE 
    WHEN MAX(CASE WHEN f.SEGURO_BATERIA_LARGO_PLAZO = 'SI' THEN 1 ELSE 0 END) = 1 THEN 1
    ELSE 0 
  END AS Contrato_Seguro_Bateria,

    -- COSTES Y RENTABILIDAD
  -- coste_medio_cliente:coste total medio por compra
  AVG(f.Coste_Total) AS Coste_Medio_Cliente,

  -- margen_bruto_medio:beneficio teórico promedio (sin costes reales)
  AVG(f.Margen_Bruto) AS Margen_Bruto_Medio,

  -- margen_eur_medio beneficio neto promedio (restándole los costes reales)
  AVG(f.Margen_eur) AS Margen_eur_Medio,

  -- rentabilidad_relativa: euros ganados netos por cada euro invertido en costes
  AVG(f.Margen_eur) / NULLIF(AVG(f.Coste_Total), 0) AS Rentabilidad_Relativa , 

 --4.CHURN Y RETENCION
	  AVG(CAST(f.Churn AS DECIMAL(10,2))) AS churn_medio,
	 AVG(f.DIAS_DESDE_ULTIMA_REVISION) AS Dias_Medios_Desde_Ultima_Revision


FROM [dwh_case1].[dbo].[dim_cliente] c
LEFT JOIN [dwh_case1].[dbo].[dim_fact] f
  ON c.Customer_ID = f.Customer_ID
--LEFT JOIN fact_table con Tiempo (Para comprobar si las fehchas de venta son en festivos,findes,días laborales..)
LEFT JOIN [dwh_case1].[dbo].[dim_tiempo] t
  ON f.Sales_Date = t.Date

GROUP BY 
  c.Customer_ID,
  c.Edad,
  c.RENTA_MEDIA_ESTIMADA,
  c.GENERO,
  c.Fecha_nacimiento,
  c.STATUS_SOCIAL,
  c.CODIGO_POSTAL,
  c.provincia,
  c.poblacion,
  c.lat,
  c.lon
;