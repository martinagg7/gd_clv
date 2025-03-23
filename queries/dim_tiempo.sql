--Tabla de tiempo
--Con la información de las fechas de las ventas.

SELECT 
    CONVERT(date, Date, 103) AS Date,
    Dia,
    Mes,
    Anno,
    Week,
    CONVERT(date, InicioMes, 103) AS InicioMes,
    Diadelasemana,
    Annomes,
    CONVERT(date, FinMes, 103) AS FinMes,
    Findesemana,
    Festivo,
    Laboral,
    Diadelesemana_desc,
    Mes_desc

FROM DATAEX.[002_date]