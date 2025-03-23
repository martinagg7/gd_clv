# Análisis de Clientes con PCA y Segmentación

## 1. Objetivo del análisis

El objetivo de este análisis es aplicar técnicas de reducción de dimensionalidad mediante PCA para simplificar la representación de clientes.
Posteriormente, se busca segmentar a los clientes en grupos en función de su comportamiento, características y rentabilidad, facilitando la toma de decisiones estratégicas (marketing, fidelización, retención, etc.).

---

## 2. Preparación de los datos

### 2.1 Fuente y origen de los datos

Los datos provinienen de nuestro modelo dimensional:

- `dim_cliente`: contiene atributos personales y socioeconómicos de los clientes.
- `dim_fact`: contiene datos de compras, revisiones, costes, márgenes, etc.
- `dim_tiempo`: permite identificar fechas especiales (festivos, fines de semana, etc.).
- `dim_producto`: nos da información sobre el el vehícullo de cad cliente.



### 2.2 Construcción de la tabla de análisis

Se generó una consulta SQL (`vision_cliente.sql`) que consolida por cada cliente:

- Datos reprentativos de los clientes(edad, renta estimada, género, ubicación...).
- Métricas de comportamiento de compra (número de compras, gasto total, días desde la última compra...).
- Indicadores de uso y mantenimiento del vehículo (número de revisiones, días en taller...).
- Medidas de rentabilidad (costes, márgenes...).
- Señales de fidelidad, quejas y retención.

---

## 3. Selección de variables

### 3.1 Criterios para la selección

Para aplicar correctamente PCA, se seleccionaron únicamente variables numéricas continuas o discretas que:

- Aportan valor descriptivo del comportamiento del cliente.
- No son identificadores ni variables categóricas (como nombres o códigos).
- No están altamente correlacionadas con otras ya incluidas.
- No presentan una gran cantidad de valores nulos o ceros por defecto.
- No representan etiquetas o resultados del cliente (como `churn`, que se usa más adelante para análisis, no como input).

### 3.2 Variables incluidas en el PCA

| Variable                             | Justificación |
|-------------------------------------|----------------|
| `Edad`                              | Variable demográfica clave. |
| `RENTA_MEDIA_ESTIMADA`             | Refleja poder adquisitivo aproximado. |
| `Numero_Veces_Lead`                | Muestra interés previo en la marca. |
| `Total_Compras`                    | Indica nivel de actividad. |
| `PVP_Total`                        | Muestra el gasto total. |
| `Dias_Desde_Ultima_Compra`         | Refleja si está activo o inactivo. |
| `Edad_Media_Coche`                | Indica tipo de vehículos adquiridos. |
| `Total_Revisiones`                 | Refleja uso de postventa. |
| `Dias_Medio_En_Taller`             | Información sobre mantenimiento. |
| `Coste_Medio_Cliente`              | Costo medio de cada cliente. |
| `Margen_Bruto_Medio`               | Rentabilidad estimada sin costes. |
| `Margen_eur_Medio`                 | Rentabilidad real. |
| `Dias_Medios_Desde_Ultima_Revision`| Actividad en servicios de mantenimiento. |

### 3.3 Variables descartadas o dudosas

| Variable                        | Motivo de descarte |
|--------------------------------|---------------------|
| `PVP_Medio`                    | Redundante con total y número de compras. |
| `PVP_Diferencia`               | Valor 0 para una compra, poco informativa. |
| `Dias_Entre_Primera_Ultima_Compra` | Redundante con número de compras. |
| `Km_Medio_por_Revision`        | Muchos ceros por ausencia de revisiones. |
| `Total_Quejas`                 | Muchos valores nulos convertidos a 0. |
| `Rentabilidad_Relativa`        | Derivada de variables ya incluidas. |
| `churn_medio`                  | Variable resultado, no explicativa. |

---

## 4. Aplicación del PCA

En esta sección se describe el preprocesamiento, escalado de variables y cálculo de componentes principales. *(A desarrollar una vez se realice el código)*.