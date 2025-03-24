# 01_Modelo_Dimensional

## Índice

- [Tratamiento de los nulos](#tratamiento-de-los-nulos)

## Tratamiento de los nulos

Para asegurar la consistencia del modelo y evitar errores durante el análisis, se han aplicado las siguientes decisiones de tratamiento de valores nulos, diferenciando por tabla y columna:

**Tabla `cliente`**

- Mosaic_U y Max_Mosaic  
  Se sustituyen los valores nulos por `0`. Al observar la tabla, se ha detectado que muchos clientes ya tienen estas columnas con valor 0, lo que indica que probablemente la empresa ha utilizado este valor como marcador de "sin información". Por tanto, se sigue esta misma lógica.

- Renta_Media (de Mosaic) 
  Se sustituye también por `0`, siguiendo el mismo razonamiento anterior. Muchos clientes ya aparecen con renta media 0, lo cual refuerza la idea de que se ha utilizado como valor por defecto ante la falta de datos.

- Lat y Lon (latitud y longitud)  
  Se dejan como `NA` para evitar errores de interpretación visual en herramientas como Power BI. Reemplazarlos por 0 podría ubicar incorrectamente a un cliente en coordenadas reales (0,0), lo que puede distorsionar el análisis geográfico.



**Tabla `fact`**

- Fecha_Ultima_Revision, DIAS_EN_TALLER y DIAS_DESDE_LA_ULTIMA_ENTRADA_TALLER
  Se sustituyen por `0` siguiendo la misma lógica que con `Km_medio_por_revision`. Si el cliente no ha pasado por el taller, se interpreta como cero días o sin revisión.

- QUEJA 
  Se sustituye por `0` para evitar valores nulos en el modelo. En la consulta `vision_cliente` solo vamos a contar el número de quejas por cliente, por lo que este reemplazo no sesga la información, ya que un nulo se puede considerar como ausencia de queja.

- Car_Age 
  Aunque hay 459 valores nulos sobre 58.049 registros, se sustituyen por `0`, ya que la cantidad es relativamente pequeña y no supondrá un impacto significativo en las métricas agregadas.
