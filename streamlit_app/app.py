
#Liberias/Css/Arhivos/Data
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


file_path = "../data/bi_cliente.csv"
df = pd.read_csv(file_path)

def load_css(file_path="styles.css"):
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

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

# Matriz de correlación - Sección
st.subheader("📊 Matriz de Correlación - Churn y Variables Seleccionadas")

# Crear un contenedor para la selección de variables
with st.expander("🔹 Selecciona las variables para la matriz de correlación"):
    variables_disponibles = ["Edad_Media_Coche", "PVP_Medio", 'RENTA_MEDIA_ESTIMADA', "churn_medio_estimado","Numero_Veces_Lead","Total_Quejas"]
    variables_seleccionadas = st.multiselect("Elige las variables:", variables_disponibles, default=variables_disponibles)

# Filtrar el dataframe con las variables seleccionadas
df_selected = df[variables_seleccionadas]
for col in df_selected.columns:
    df_selected[col] = pd.to_numeric(df_selected[col], errors="coerce")

# Calcular la matriz de correlación
corr_matrix = df_selected.corr()

# Mostrar la matriz de correlación en la misma sección
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr_matrix, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5, ax=ax)
ax.set_title("Matriz de Correlación - Churn y Variables Seleccionadas")
st.pyplot(fig)