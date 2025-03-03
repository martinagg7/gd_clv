select * from [DATAEX].[003_clientes] ORDER BY CODIGO_POSTAL DESC;
select * from [DATAEX].[019_Mosaic] ORDER BY CP DESC
select * from [DATAEX].[005_cp]
select * from [DATAEX].[012_provincia]

select count(DISTINCT CODIGO_POSTAL) AS total_codigos_postales_CLIENTES
FROM [DATAEX].[003_clientes];

select count(DISTINCT CP) AS total_codigos_postales_CP FROM [DATAEX].[005_cp];

select count(DISTINCT CP) AS total_codigos_postales_mosaic FROM [DATAEX].[019_Mosaic];