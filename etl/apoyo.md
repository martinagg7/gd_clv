# 01_Modelo_Dimensional

## Índice
- [Aspectos a tener en cuenta de las tablas para el análisis](#aspectos-a-tener-en-cuenta-de-las-tablas-para-el-análisis)
- [Tratamiento de los nulos](#tratamiento-de-los-nulos)
- [Cálculo del Churn](#cálculo-del-churn)



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


- `QUEJA`
  Se sustituyen los valores nulos por `'NA'`. Esto permite distinguir entre “no se ha quejado” (`'NO'`) y “no se tiene información” (`'NA'`), sin falsear los análisis de quejas.

- `Car_Age`
  Se sustituyen los valores nulos por `0`. Dado que son pocos (459 de 58.049), se considera que no afectarán significativamente a los análisis agregados.

## Cálculo del Churn

La variable **Churn** indica si un cliente ha dejado de realizar revisiones y, por tanto, tiene una alta probabilidad de no volver a comprar.  
Se ha detectado que muchos registros tienen valores `0` en la columna `DIAS_DESDE_ULTIMA_REVISION`, lo que puede generar confusión.  
Para resolverlo, se ha definido la siguiente estrategia:

- **Clientes con más de 401 días sin revisiones** → Se consideran como **Churn (1)**.  
- **Clientes con 0 días desde la última revisión y un coche con más de 1 año** → También se consideran **Churn (1)**, ya que han pasado dos años o más y aún no se han tenido noticias del cliente.
- **Clientes con 0 días desde la última revisión y un coche de menos de 1 año** → Se consideran **activos (0)**, ya que pueden estar en su período inicial de uso.  
- **Todos los demás casos** → Se consideran **activos (0)**.  

En el futuro, sería recomendable analizar en más profundidad los datos y probar otras estrategias para manejar los valores nulos,  
como imputaciones basadas en patrones históricos o modelos predictivos para determinar la mejor opción.  

---
# 02_Vision_Cliente

## Índice
- [Medidas descriptivas del cliente](#medidas-descriptivas-del-cliente)
- [Origen y captación](#origen-y-captación)
- [Comportamiento de compra](#comportamiento-de-compra)
- [Uso y mantenimiento](#uso-y-mantenimiento)
- [Satisfacción y servicio](#satisfacción-y-servicio)
- [Costes y rentabilidad](#costes-y-rentabilidad)
- [Churn y revisiones](#churn-y-revisiones)

## **Medidas descriptivas del cliente**  
Información básica del cliente:  
- **Edad**  
- **Género**  
- **Renta media estimada**  
- **Provincia y ubicación (lat, lon)**  

## **Origen y captación**  
- **Origen_Compra**: Canal de compra (Internet, Tienda o Ambos).  
- **Fue_Lead_Alguna_Vez**: Si fue registrado como lead alguna vez (1 = sí, 0 = no).  
- **Numero_Veces_Lead**: Número de veces que fue lead.  

## **Comportamiento de compra**  
- **Total_Compras**: Cantidad de vehículos comprados.  
- **Modelos_Comprados**: Modelos adquiridos.  
- **PVP_Total**: Suma del precio de venta de todas sus compras.  
- **PVP_Medio**: Precio medio gastado en cada compra.  
- **PVP_Diferencia**: Diferencia entre la compra más cara y la más barata.  
- **Dias_Entre_Primera_Ultima_Compra**: Días entre la primera y la última compra.  
- **Ultima_Compra**: Fecha de la última compra.  
- **Dias_Desde_Ultima_Compra**: Días desde la última compra hasta la fecha de referencia.  
- **Compra_Finde_O_Festivo**: Si alguna compra fue en fin de semana o festivo (1 = sí, 0 = no).  

## **Uso y mantenimiento**  
- **Edad_Media_Coche**: Edad promedio de los coches comprados.  
- **Total_Revisiones**: Cantidad total de revisiones realizadas.  
- **Km_Medio_por_Revision**: Promedio de kilómetros recorridos por revisión.  
- **Tuvo_Mantenimiento_Gratuito**: Si recibió mantenimiento gratuito alguna vez (1 = sí, 0 = no).  
- **Dias_Medio_En_Taller**: Promedio de días en taller por coche.  

## **Satisfacción y servicio**  
- **Total_Quejas**: Número total de quejas registradas.  
- **Compra_Tienda_Unica**: Si todas sus compras fueron en la misma tienda (1 = sí, 0 = no).  
- **Contrato_Seguro_Bateria**: Si alguna vez contrató seguro de batería (1 = sí, 0 = no).  

## **Costes y rentabilidad**  
- **Coste_Medio_Cliente**: Promedio del coste total por compra.  
- **Margen_Bruto_Medio**: Beneficio teórico promedio antes de restar costes.  
- **Margen_Eur_Medio**: Beneficio neto promedio después de restar costes.  
- **Rentabilidad_Relativa**: Relación entre beneficio neto y coste total, calculada como:  
  \[
  \text{Rentabilidad} = \frac{\text{Margen Eur Medio}}{\text{Coste Medio Cliente}}
  \]
  Si el coste es 0, se evita la división para no generar errores.  

## **Churn y revisiones**  
- **Churn_Cliente**: Si el cliente ha dejado de comprar (1 = sí, 0 = no).  
- **Dias_Medios_Desde_Ultima_Revision**: Días promedio desde su última revisión.  