# 01_Modelo_Dimensional

## Índice
- [Aspectos a tener en cuenta de las tablas para el análisis](#aspectos-a-tener-en-cuenta-de-las-tablas-para-el-análisis)
- [Tratamiento de los nulos](#tratamiento-de-los-nulos)
- [Cálculo del Churn](#cálculo-del-churn)

## Aspectos a tener en cuenta de las tablas para el análisis

## Aspectos a tener en cuenta de las tablas para el análisis

Existen una serie de variables que pueden dar lugar a confusión durante el análisis si no se interpretan correctamente. Por ello, se ha decidido dejar constancia de estas situaciones para evitar malas interpretaciones de los resultados:

**Tabla `cliente`**

- *RENTAS IGUALES A 0* 
  En algunos registros, tanto la variable `RENTA_MEDIA_ESTIMADA` como `Renta_Media` (proveniente del sistema Mosaic) toman el valor `0`. Este valor no debe interpretarse como que el cliente tiene cero ingresos, sino como falta de información. Se ha optado por mantener el `0` siguiendo la lógica del origen de los datos, ya que muchas veces la empresa ya utilizaba ese valor como marcador por defecto.

**Tabla `fact`**

- *REVISIONES Y KILOMETRAJES EN 0*
  En los casos en que el cliente*no ha realizado ninguna revisión las siguientes variables aparecen con valor `0`:  
  - `Km_medio_por_revision`  
  - `Revisiones`  
  - `Fecha_Ultima_Revision`

  Esto no implica que el cliente tenga revisiones con 0 km, sino que simplemente no ha pasado por el taller.

- *TIEMPO EN TALLER*  
  Las variables:  
  - `DIAS_EN_TALLER`  
  - `DIAS_DESDE_LA_ULTIMA_ENTRADA_TALLER`  
  también toman el valor `0` cuando no hay ninguna entrada registrada en el taller. No significa que el cliente haya estado cero días, sino que directamente no ha tenido actividad relacionada con el taller.




## Tratamiento de los nulos

Para asegurar la consistencia del modelo y evitar errores durante el análisis, se han aplicado las siguientes decisiones de tratamiento de valores nulos, diferenciando por tabla y columna:

**Tabla `cliente`**

- `Mosaic_U y Max_Mosaic`
  Se sustituyen los valores nulos por `0`. Muchos clientes ya tienen estas columnas con valor 0, lo que sugiere que la empresa utiliza ese valor como marcador de “sin información”. Se mantiene esa lógica.

- `Renta_Media (de Mosaic)`
  También se sustituye por `0`. Al igual que en los campos anteriores, se ha observado que la empresa ya representa con 0 los casos sin datos de renta.

- `Lat y Lon (latitud y longitud)`
  Se sustituyen los valores nulos por `'NA'`. Esto evita que Power BI coloque puntos en coordenadas incorrectas como (0,0), lo que podría distorsionar los mapas.

- `provincia y género`
  Se sustituyen los valores vacíos o nulos por `'NA'`. Esto permite tratarlos como categorías distintas y fácilmente filtrables en Power BI, en lugar de aparecer como valores en blanco o errores.



**Tabla `fact`**

- `Fecha_Ultima_Revision`
  Se convierte a formato fecha con `pd.to_datetime`, dejando los valores nulos como `NaT`. Esto facilita su tratamiento posterior en Power BI como fechas desconocidas.

- `DIAS_EN_TALLER` y `DIAS_DESDE_LA_ULTIMA_ENTRADA_TALLER`
  Se sustituyen por `0`. Si el cliente no ha pasado por el taller, se considera como cero días, lo que es coherente con los datos asociados.

- `DIAS_DESDE_ULTIMA_REVISION`
  Se sustituye por `0` cuando coincide con `Revisiones = 0` y `Km_medio_por_revision = 0`, lo que indica que no ha realizado ninguna revisión.

- `QUEJA`
  Se sustituyen los valores nulos por `'NA'`. Esto permite distinguir entre “no se ha quejado” (`'NO'`) y “no se tiene información” (`'NA'`), sin falsear los análisis de quejas.

- `Car_Age`
  Se sustituyen los valores nulos por `0`. Dado que son pocos (459 de 58.049), se considera que no afectarán significativamente a los análisis agregados.

## Cálculo del Churn

Durante el cálculo de la variable **Churn**, se detectó que muchos registros presentaban valores vacíos o nulos en la columna `DIAS_DESDE_ULTIMA_REVISION`. Si estos valores se c