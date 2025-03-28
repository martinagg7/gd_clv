
#Liberias/Css/Arhivos/Data
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px  


file_path = "../data/cliente_bi.csv"
df = pd.read_csv(file_path)

def load_css(file_path="styles.css"):
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()
color_palette = ["#1F4E79", "#1F77B4", "#4A90E2", "#76A9FA"]
# ---Pestaña 1: Explicación del CLV--

st.title("🔍 Customer Lifetime Value (CLV)")

## Introducción al Proyecto
st.write("""
En este proyecto, analizamos datos de una empresa automovilística para estudiar el valor de los clientes a futuro. Nuestro objetivo es calcular el CLV (Customer Lifetime Value) a 5 años y evaluar cómo contribuyen los clientes a la rentabilidad de la empresa.

El **Customer Lifetime Value (CLV)** es una métrica que estima los ingresos netos que un cliente generará durante su relación con la empresa. Comprender esta métrica permite optimizar estrategias de fidelización y segmentación de clientes.

 - Un CLV alto indica que un cliente genera muchos ingresos y es rentable
 - CLV bajo o negativo puede significar que el cliente no genera ganancias o incluso que la empresa esta perdiendo dinero con él.
""")

## Cálculo del CLV a 5 Años
st.subheader("Fórmula del CLV a 5 años")
st.latex(r"""
CLV_{5\_anos} = Margen\_eur\_Medio \times \sum_{t=1}^{5} \frac{ Retención^t }{(1+i)^t}
""")

st.write("""
Donde:
- **Retención** → Probabilidad de que el cliente continúe comprando en el tiempo.
- **Margen_eur_Medio** →Beneficio neto por cliente, calculado como la diferencia entre los ingresos generados por el cliente y los costes asociados a su adquisición y mantenimiento.
- **i = 7%** → Tasa de descuento aplicada para ajustar el valor del dinero en el tiempo.


""")

## Conclusiones Clave
st.subheader("Conclusiones Clave")

data = {
    "Cliente": ["A", "B", "C", "D"],
    "Margen(€)": [1000, 500, 700, -300],
    "Retención(%)": [0.95, 0.50, 0.00, 0.75],
    "CLV 1 Año (€)": [950, 250, 0, -225],
    "Explicación": [
        "Cliente muy rentable",
        "Cliente rentable pero con menor fidelidad",
        "No genera beneficios a futuro",
        "Genera pérdidas"
    ]
}

df_escenarios = pd.DataFrame(data)

st.markdown(df_escenarios.to_html(index=False), unsafe_allow_html=True)


st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("**Relevancia de la Retención**", unsafe_allow_html=True)

st.write("""
         
 **Alta Retención:** Un cliente con alta retención seguirá siendo rentable a largo plazo, incluso si su margen es moderado.

**Retención 0:** Si la retención es cero, el cliente dejará de generar ingresos en el futuro, sin importar su margen actual.

**Retención Alta pero Margen Negativo:** Cuando la retención es alta pero el margen es negativo, el cliente continuará generando pérdidas con el tiempo.
""")

st.markdown("""
### Análisis de la Influencia de las Variables en la Tasa de Abandono (Churn)

Para predecir la probabilidad  de abandono por cliente, analizamos qué variables tienen mayor influencia sobre esta. Esto lo representamos a través de una **matriz de correlación**, la cual muestra cómo cada variable se relaciona con el Churn .  

💡 Para este análisis, te sugerimos probar con las variables: **Edad_Media_Coche, PVP_Medio, RENTA_MEDIA_ESTIMADA, Km_Medio_por_Revision**.  

""")
#Para adaptar matriz
with st.expander("Selecciona las variables para la matriz de correlación"):
    variables_disponibles = ["Edad_Media_Coche", "PVP_Medio", 'RENTA_MEDIA_ESTIMADA',"Numero_Veces_Lead","Total_Quejas",'Km_Medio_por_Revision',"churn_medio_estimado"]
    variables_seleccionadas = st.multiselect("Elige las variables:", variables_disponibles, default=variables_disponibles)

df_selected = df[variables_seleccionadas]
for col in df_selected.columns:
    df_selected[col] = pd.to_numeric(df_selected[col], errors="coerce")

# Calcular la matriz de correlación
corr_matrix = df_selected.corr()
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr_matrix, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

st.markdown("<br><br>", unsafe_allow_html=True)

# Intepretación Matriz Correlación
st.markdown("""
#### Interpretación de la Matriz de Correlación
""")

data_corr = {
    "Variable": ["Edad_Media_Coche", "PVP_Medio", "RENTA_MEDIA_ESTIMADA", "Km_Medio_por_Revision"],
    "Coeficiente": [0.47, -0.14, -0.21, -0.52],
    "Interpretación": [
        "Mayor antigüedad del coche, mayor probabilidad de abandono.",
        "Precio medio más alto, menor churn, pero relación débil.",
        "Mayor renta, menor tasa de abandono.",
        "Más kilómetros por revisión, menor churn, clientes comprometidos."
    ]
}

df_corr = pd.DataFrame(data_corr)
table_html = df_corr.to_html(index=False, classes="styled-table")
st.markdown(table_html, unsafe_allow_html=True)

# Análisis a fondo variable + influyentes
variables_importantes = ["Edad_Media_Coche", "PVP_Medio", "RENTA_MEDIA_ESTIMADA", "Km_Medio_por_Revision"]

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("#### Distribución de Variables Clave")

col1, col2 = st.columns(2)


for i, variable in enumerate(variables_importantes):
    # Ajustar bins en Km_Medio_por_Revision
    bins = 30 if variable != "Km_Medio_por_Revision" else 50  # Aumentar bins para mejor distribución
    
    fig = px.histogram(
        df, x=variable, nbins=bins, 
        color_discrete_sequence=[color_palette[i]], 
        title=f"Distribución de {variable}"
    )
    
    if variable in ["RENTA_MEDIA_ESTIMADA", "Km_Medio_por_Revision"]:
        fig.update_xaxes(tickformat=",")  

    fig.update_layout(
        xaxis_title=variable,
        yaxis_title="Frecuencia",
        bargap=0.1
    )
    if i % 2 == 0:
        with col1:
            st.plotly_chart(fig, use_container_width=True)
    else:
        with col2:
            st.plotly_chart(fig, use_container_width=True)

# Asegurar que las variables sean numéricas
df["churn_medio_estimado"] = pd.to_numeric(df["churn_medio_estimado"], errors="coerce")
df["retencion"] = pd.to_numeric(df["retencion"], errors="coerce")
df["CLV_5_anos"] = pd.to_numeric(df["CLV_5_anos"], errors="coerce")
df["Margen_eur_Medio"] = pd.to_numeric(df["Margen_eur_Medio"], errors="coerce")

### 📌 1️⃣ Scatter Plot Interactivo - Distribución de Churn ###
import plotly.figure_factory as ff
import streamlit as st

st.subheader("📊 Distribución de Churn - Estimación de Densidad (KDE Interactivo)")

# Extraer datos
churn_values = df["churn_medio_estimado"].dropna().values  # Aseguramos que no haya nulos

# Crear KDE con Plotly
fig_kde = ff.create_distplot(
    [churn_values], 
    group_labels=["Churn Estimado"], 
    show_hist=False,  # No queremos histogramas, solo la curva KDE
    colors=["#1F4E79"]
)

# Ajustar título y ejes
fig_kde.update_layout(
    title="Distribución de Churn en Clientes",
    xaxis_title="Churn Estimado",
    yaxis_title="Densidad"
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig_kde)

### 📌 2️⃣ Gráfico de Barras - Clientes Retenidos vs. En Riesgo ###
st.subheader("📊 Segmentación de Clientes según Churn")

# Calcular la cantidad de clientes retenidos y en riesgo
retenidos = df[df["churn_medio_estimado"] <= 0.5].shape[0]
riesgo = df[df["churn_medio_estimado"] > 0.5].shape[0]

fig_barras_churn = px.bar(
    x=["Clientes Retenidos", "Clientes en Riesgo"], 
    y=[retenidos, riesgo],
    color=["Clientes Retenidos", "Clientes en Riesgo"],
    color_discrete_map={"Clientes Retenidos": "#1F4E79", "Clientes en Riesgo": "#D62728"}
)
fig_barras_churn.update_layout(title="Comparación de Clientes según Churn", xaxis_title="", yaxis_title="Cantidad de Clientes")
st.plotly_chart(fig_barras_churn)

### 📌 3️⃣ Gráfico de Barras - Clasificación de Clientes según CLV ###
st.subheader("📊 Clasificación de Clientes según CLV")

# Clasificar clientes según su CLV
clientes_perdida = df[df["CLV_5_anos"] < 0].shape[0]
clientes_equilibrio = df[(df["CLV_5_anos"] >= 0) & (df["CLV_5_anos"] <= df["Margen_eur_Medio"])].shape[0]
clientes_rentables = df[df["CLV_5_anos"] > df["Margen_eur_Medio"]].shape[0]

fig_barras_clv = px.bar(
    x=["Clientes en Pérdida", "Clientes en Equilibrio", "Clientes Rentables"], 
    y=[clientes_perdida, clientes_equilibrio, clientes_rentables],
    color=["Clientes en Pérdida", "Clientes en Equilibrio", "Clientes Rentables"],
    color_discrete_map={
        "Clientes en Pérdida": "#D62728",  
        "Clientes en Equilibrio": "#FFB800",  
        "Clientes Rentables": "#1F4E79"
    }
)
fig_barras_clv.update_layout(title="Clasificación de Clientes según CLV", xaxis_title="", yaxis_title="Cantidad de Clientes")
st.plotly_chart(fig_barras_clv)
