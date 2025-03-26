import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar el CSV con todos los datos de los clientes, incluidas las coordenadas PCA y los clusters
df_completo = pd.read_csv("data/clientes_datos_cluster.csv")

# Título de la página
st.title("Análisis de Segmentación de Clientes")

# Mostrar resumen general de los clusters
st.subheader("Resumen general de los clusters")
st.write(f"Total de clientes segmentados: {len(df_completo)}")
st.write("Hemos segmentado a los clientes en **3 clusters** usando PCA y KMeans.")

# Mostrar gráfico PCA con los clusters
st.subheader("Gráfico PCA de los clusters")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_completo, x="PC1", y="PC2", hue="Cluster", palette="Set1", s=100, ax=ax)
ax.set_title("Distribución de Clientes según PCA (PC1 vs PC2)")
st.pyplot(fig)

# Mostrar tabla comparativa entre los clusters
st.subheader("Comparación entre clusters")
df_clusters_comparacion = pd.read_csv("data/clusters_comparacion.csv")  # Cargamos la tabla comparativa
st.dataframe(df_clusters_comparacion)

# Agregar un selectbox para elegir un cluster
cluster_choice = st.selectbox("Selecciona un cluster para analizar:", [0, 1, 2])

# Filtramos el DataFrame para mostrar los clientes del cluster seleccionado
df_cluster_selected = df_completo[df_completo['Cluster'] == cluster_choice]

# Mostrar los datos del cluster seleccionado
st.subheader(f"Análisis del Cluster {cluster_choice}")
st.write(f"Número de clientes en Cluster {cluster_choice}: {len(df_cluster_selected)}")
st.dataframe(df_cluster_selected)  # Mostramos los datos del cluster seleccionado