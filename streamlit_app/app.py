
#Liberias/Css/Arhivos/Data
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff  
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.cluster import KMeans
import plotly.graph_objects as go

#Archivos leer
file_path = "../data/cliente_bi.csv"
df = pd.read_csv(file_path)
#Estilos
def load_css(file_path="styles.css"):
    with open(file_path, "r") as f:

        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()
color_palette = ["#1F4E79", "#1F77B4", "#4A90E2", "#76A9FA"]

# Barra de navegación para cambiar entre páginas
menu = st.selectbox("Selecciona una sección:", ["Inicio","Análisis CLV","Segmentación Clientes"])
st.markdown("---")

# --------------------------------------------------------------------------------------
#   PESTAÑA 1: INTRODUCCIÓN AL CLV
# --------------------------------------------------------------------------------------
if menu == "Inicio":
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
    

# --------------------------------------------------------------------------------------
# 📌 PESTAÑA 2: ANÁLISIS CLV Y PROYECCIÓN FINANCIERA
# --------------------------------------------------------------------------------------

if menu == "Análisis CLV":
    st.markdown("""
    ## 📊 Análisis de Clientes y Proyección Financiera

    En esta sección analizamos los datos de nuestra empresa para evaluar el comportamiento de los clientes actuales.  
    Hemos calculado tres métricas clave para cada cliente:

    - **% de Retención:** Probabilidad de que el cliente se mantenga fiel a la compañia los próximos años.  
    - **% de Abandono:** Riesgo de que el cliente deje de comprar productos de la marca.  
    - **CLV a 5 Años (€):** Ingresos netos estimados que generará cada cliente en cinco años.  

    Estos valores nos permiten entender qué clientes son más rentables y qué acciones podemos tomar para mejorar la fidelización y rentabilidad futura.
    """)
    def format_number(value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"
        elif value >= 1_000:
            return f"{value / 1_000:.1f}k"
        else:
            return f"{value:,.0f}"
  
    st.markdown("### Métricas Generales</h3>", unsafe_allow_html=True)

    

    # métricas generales
    num_clientes = df.shape[0]
    ganancias_actuales = df["Margen_eur_Medio"].sum()
    costo_medio_cliente = df["Coste_Medio_Cliente"].mean() if "Coste_Medio_Cliente" in df.columns else 0  
    ganancias_futuras = df["CLV_5_anos"].sum()


    col1, col2, col3, col4 = st.columns(4)

    card_style = """
        <style>
            .metric-card {
                background-color: {color};
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                color: white;
                font-size: 18px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .metric-title {
                font-size: 16px;
                font-weight: bold;
            }
            .metric-value {
                font-size: 22px;
                margin-top: 5px;
            }
        </style>
    """

    st.markdown(card_style, unsafe_allow_html=True)

    with col1:
        st.markdown(f"<div class='metric-card' style='background-color:{color_palette[0]};'>"
                    f"<div class='metric-title'>👥 Clientes Totales</div>"
                    f"<div class='metric-value'>{format_number(num_clientes)}</div>"
                    f"</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='metric-card' style='background-color:{color_palette[1]};'>"
                    f"<div class='metric-title'>💰 Ganancias Actuales (€)</div>"
                    f"<div class='metric-value'>{format_number(ganancias_actuales)}</div>"
                    f"</div>", unsafe_allow_html=True)


    with col3:
        st.markdown(f"<div class='metric-card' style='background-color:{color_palette[2]};'>"
                    f"<div class='metric-title'>💸 Costo Medio por Cliente (€)</div>"
                    f"<div class='metric-value'>{format_number(costo_medio_cliente)}</div>"
                    f"</div>", unsafe_allow_html=True)

    with col4:
        st.markdown(f"<div class='metric-card' style='background-color:{color_palette[3]};'>"
                    f"<div class='metric-title'>📈 Ganancias Proyectadas (€)</div>"
                    f"<div class='metric-value'>{format_number(ganancias_futuras)}</div>"
                    f"</div>", unsafe_allow_html=True)
        

        
    st.markdown("### Análisis de la Retención y Churn")
    st.markdown("""
    Para comprender mejor el comportamiento de los clientes, analizamos la distribución de dos métricas clave:
    - **Churn (%)**: Probabilidad de que el cliente deje de comprar.
    - **Retención (%)**: Probabilidad de que el cliente siga comprando en los próximos años.

    El gráfico interactivo muestra la densidad de estas métricas para toda la base de clientes.
    """)

    # Gráficos de densidad
    churn_values = df["churn_medio_estimado"].dropna().values
    retention_values = df["retencion"].dropna().values

    fig = ff.create_distplot(
        [churn_values, retention_values],
        group_labels=["Churn (Abandono)", "Retención"],
        colors=["red", "#1F4E79"],
        show_hist=False
    )

    fig.update_layout(
        title="Distribución de Churn y Retención",
        xaxis_title="Probabilidad",
        yaxis_title="Densidad"
    )


    st.plotly_chart(fig, use_container_width=True)



    # Definir umbral para retención y abandono
    threshold = 0.5
    clientes_retenidos = df[df["retencion"] >= threshold].shape[0]
    clientes_abandono = df[df["churn_medio_estimado"] > threshold].shape[0]

    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; margin-top: -15px;">
        <table style="border-collapse: collapse; text-align: center;">
            <tr>
                <td style="border: 2px solid #1F4E79; padding: 8px; border-radius: 10px; background-color: white;">
                    <span style="color: #1F4E79; font-weight: bold;">🔵 Retenidos</span><br>
                    <span style="font-size: 18px; font-weight: bold;">{}</span>
                </td>
                <td style="border: 2px solid #D62728; padding: 8px; border-radius: 10px; background-color: white; margin-left: 15px;">
                    <span style="color: #D62728; font-weight: bold;">🔴 En Riesgo</span><br>
                    <span style="font-size: 18px; font-weight: bold;">{}</span>
                </td>
            </tr>
        </table>
    </div>
    """.format(clientes_retenidos, clientes_abandono), unsafe_allow_html=True)

    total_clientes = df.shape[0]
    porcentaje_retenidos = (clientes_retenidos / total_clientes) * 100
    porcentaje_abandono = (clientes_abandono / total_clientes) * 100


    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""


    Actualmente, la empresa **retiene el {porcentaje_retenidos:.1f}%** de sus clientes, mientras que **{porcentaje_abandono:.1f}%** están en riesgo de abandono.  
    Es fundamental analizar qué factores influyen en esta retención y qué estrategias de fidelización pueden implementarse para convertir a los clientes en riesgo en compradores recurrentes.  
    """)


    # Sección: Análisis del CLV
    st.markdown("### Análisis del Customer Lifetime Value (CLV)")


    st.markdown("""Hemos calculado el Customer Lifetime Value (CLV) proyectado a 5 años para nuestros  clientes con el objetivo de comprender su rentabilidad futura.

    """)

    # Gráfico de distribución del CLV
    fig_clv = px.histogram(
        df, x="CLV_5_anos", nbins=50, 
        color_discrete_sequence=["#1F4E79"], 
        title="Distribución del CLV"
    )
    fig_clv.update_layout(
        xaxis_title="CLV a 5 años (€)",
        yaxis_title="Frecuencia",
        bargap=0.1
    )
    st.plotly_chart(fig_clv, use_container_width=True)
    st.markdown("""
    ###### Conclusiones del CLV

    - **Distribución sesgada a la derecha:** La mayoría de los clientes presentan un CLV cercano a 0€, con algunos casos que alcanzan valores positivos elevados, lo que indica que pocos clientes generan una rentabilidad significativa.  

    - **Colas largas:** Se observa una proporción de clientes con CLV negativo, lo que significa que generan pérdidas para la empresa, mientras que en el extremo positivo hay clientes altamente rentables que representan una oportunidad de fidelización.  

    - **Pico central en 0€:** La concentración en 0€ sugiere que una gran parte de los clientes no aporta beneficios netos a largo plazo, lo que puede deberse a costos de adquisición altos o una baja frecuencia de compra.  
    """)



    # Cálculo de métricas clave
    max_clv = df["CLV_5_anos"].max()
    min_clv = df["CLV_5_anos"].min()
    mean_clv = df["CLV_5_anos"].mean()
    median_clv = df["CLV_5_anos"].median()
    std_clv = df["CLV_5_anos"].std()
    clv_negativos = (df["CLV_5_anos"] < 0).mean() * 100  # % de clientes con CLV negativo
    clientes_superior_media = df[df["CLV_5_anos"] > mean_clv].shape[0]
    porcentaje_superior_media = (clientes_superior_media / df.shape[0]) * 100

    st.markdown("""
            ##### Métricas Descriptivas CLV    
    <div style="width:50%; margin:auto; font-size: 14px;">
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Métrica</th>
                    <th>Valor (€)</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Máximo CLV</td><td>{:,.2f}</td></tr>
                <tr><td>Mínimo CLV</td><td>{:,.2f}</td></tr>
                <tr><td>Media CLV</td><td>{:,.2f}</td></tr>
                <tr><td>Mediana CLV</td><td>{:,.2f}</td></tr>
                <tr><td>Desviación Estándar</td><td>{:,.2f}</td></tr>
                <tr><td>% CLV Negativo</td><td>{:.2f}%</td></tr>
                <tr><td>% Clientes con CLV > Media</td><td>{:.2f}%</td></tr>
            </tbody>
        </table>
    </div>
    """.format(max_clv, min_clv, mean_clv, median_clv, std_clv, clv_negativos,porcentaje_superior_media), unsafe_allow_html=True)
    st.markdown("""
    **Conclusiones sobre el CLV y proyección futura**

    - De media, la empresa espera ganar 7,270.50€ por cliente en los próximos 5 años, lo que representa una base sólida para la planificación financiera.
    - La mayoría de los clientes tienen un CLV positivo, lo que indica una rentabilidad general favorable.
    - Aunque solo 12.27% de los clientes tienen un CLV negativo, es crucial analizar qué factores llevan a estas pérdidas y cómo evitarlas con estrategias de fidelización.
    """)


    # Clasificación de clientes según su CLV

    clientes_perdida = df[df["CLV_5_anos"] < 0].shape[0]
    clientes_menor_margen = df[(df["CLV_5_anos"] > 0) & (df["CLV_5_anos"] < df["Margen_eur_Medio"])].shape[0]
    clientes_mayor_margen = df[df["CLV_5_anos"] >= df["Margen_eur_Medio"]].shape[0]

    data_clv_categorias = pd.DataFrame({
        "Categoría": ["CLV Negativo (Pérdidas)", "CLV < Margen Actual", "CLV > Margen Actual"],
        "Clientes": [clientes_perdida, clientes_menor_margen, clientes_mayor_margen]
    })



    fig = px.bar(
        data_clv_categorias, x="Categoría", y="Clientes", 
        color="Categoría", color_discrete_sequence=color_palette,
        text="Clientes", title="Distribución de Clientes según su CLV"
    )


    fig.update_layout(
        yaxis_title="Número de Clientes", 
        xaxis_title="", 
        showlegend=False,
        font=dict(size=14)  
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ##### Análisis de la Distribución del CLV

    Para evaluar el impacto del Customer Lifetime Value (CLV), segmentamos a los clientes en tres categorías clave:

    1. **🚨 Clientes con CLV Negativo (Pérdidas):** Representan un riesgo financiero, ya que generan más costes de los ingresos que aportarán en el futuro. Es importante analizar cómo optimizar su rentabilidad.

    2. **🆗 Clientes con CLV Inferior al Margen Actual:** Aunque actualmente generan ingresos positivos, su valor futuro será menor. Esto indica la necesidad de estrategias de fidelización para evitar una disminución en su contribución a la empresa.

    3. **💡 Clientes con CLV Superior al Margen Actual:** Son los clientes más valiosos, ya que generarán más ingresos en el futuro de lo que aportan actualmente. Es fundamental mantener su compromiso y potenciar su lealtad.""")


# --------------------------------------------------------------------------------------
#   PESTAÑA 3: PCA
# --------------------------------------------------------------------------------------

if menu == "Segmentación Clientes":

    st.title("🧑‍🧑‍🧒 Segmentación Clientes")
    st.write("""
    Se aplicó PCA para reducir la dimensionalidad a dos componentes principales y luego K-means para agrupar a los clientes en 6 clusters. Esto permite identificar patrones y diferencias entre los  diferentes clientes de compañia.

    **Nota**:
             
    Cada color en el gráfico representa un **cluster** con **clientes tienen perfiles de compra similares**.
    Estos grupos serán analizados en detalle a continuación para comprender más fondo el comportamiento de cada grupo
    """)



   

    # Archivo con los datos
    file_path = "../client_anlysis/df_final.csv"
    df = pd.read_csv(file_path)

    if {"PC1", "PC2", "Cluster"}.issubset(df.columns):
        
        # Ordenar los clusters correctamente
        df["Cluster"] = pd.Categorical(df["Cluster"], categories=[0, 1, 2, 3, 4, 5], ordered=True)
        centroids = df.groupby("Cluster")[["PC1", "PC2"]].mean().reset_index()

        # Definir colores personalizados para cada cluster
        cluster_colors = ["#1F4E79", "#1F77B4", "#4A90E2", "#76A9FA", "#E74C3C", "#F39C12"]
        
        # Mostrar leyenda manual con colores
        st.markdown("### Identificación de Clusters")
        legend_html = "".join(
            [f"<span style='background-color:{color}; padding:5px 15px; margin:5px; display:inline-block; color:white; border-radius:5px;'>Cluster {i}</span>"
            for i, color in enumerate(cluster_colors)]
        )
        st.markdown(legend_html, unsafe_allow_html=True)

        # Crear gráfico de dispersión
        fig = px.scatter(
            df, x="PC1", y="PC2", color=df["Cluster"].astype(str),
            title="Segmentación de Clientes con Clusters y Centroides",
            labels={"Cluster": "Cluster"},
            opacity=0.7,
            color_discrete_sequence=cluster_colors
        )

    
        # Ajustar diseño
        fig.update_layout(
            autosize=True,
            width=1000,  
            height=800,
            legend_title_text="Clusters"
        )

        # Mostrar gráfico interactivo en Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Cargar el archivo con las métricas por cluster
    # Cargar el archivo con las métricas por cluster
    file_path = "../client_anlysis/df_cluster_comp.csv"  # Ajusta la ruta según sea necesario
    df_cluster_comp = pd.read_csv(file_path)

    # Lista de métricas disponibles
    metricas_disponibles = list(df_cluster_comp.columns[1:])  # Excluir la columna 'Cluster'

    # 🎯 SELECCIÓN DE MÉTRICAS → Ahora está ENCIMA del gráfico
    st.markdown("### Comparación de Métricas entre Clusters")
    metricas_seleccionadas = st.multiselect("Selecciona las métricas a comparar:", metricas_disponibles, default=["CLV_5_anos", "Margen_eur_Medio"])

    # Verificar que haya métricas seleccionadas
    if metricas_seleccionadas:
        # Crear gráfico interactivo
        df_melted = df_cluster_comp.melt(id_vars=["Cluster"], value_vars=metricas_seleccionadas,
                                        var_name="Métrica", value_name="Valor")
        fig = px.bar(df_melted, x="Cluster", y="Valor", color="Métrica", barmode="group",
                    title="Comparación de Métricas entre Clusters",
                    labels={"Valor": "Valor Escalado", "Cluster": "Cluster"},
                    width=800,  # ⬅ Hacemos este gráfico más grande también
                    height=600)  # ⬅ Ajustamos altura

        st.plotly_chart(fig, use_container_width=False)  # ⬅ Evita que el gráfico se haga pequeño

        # Explicación de la visualización
        st.markdown("""
        **Cómo usar este gráfico:**
        - Cada barra representa el valor de una métrica dentro de un cluster.
        - Se pueden seleccionar diferentes métricas arriba del gráfico para comparar aspectos clave de los clientes.
        - Estos valores están normalizados, por lo que no representan valores absolutos, sino diferencias entre clusters.
        """)
    else:
        st.warning("Selecciona al menos una métrica para visualizar la comparación entre clusters.")
    
    st.markdown("### Estrategias a Futuro")
    st.write("""
    Este análisis identifica los clusters según su **Customer Lifetime Value (CLV)** y propone estrategias optimizadas para cada segmento de clientes.
    """)

    # Crear tabla con estilos
    table_html = """
    <style>
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 16px;
        }
        .styled-table th, .styled-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        .styled-table th {
            background-color: #1F4E79;
            color: white;
        }
    </style>

    <table class="styled-table">
        <thead>
            <tr>
                <th>Cluster</th>
                <th>CLV</th>
                <th>Acción Recomendada</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Clusters 2 y 4</b></td>
                <td>Alto</td>
                <td>Fidelización y Upselling</td>
            </tr>
            <tr>
                <td><b>Clusters 1 y 3</b></td>
                <td>Medio</td>
                <td>Incentivar segunda compra</td>
            </tr>
            <tr>
                <td><b>Clusters 0 y 5</b></td>
                <td>Bajo/Negativo</td>
                <td>Reducir costos o reenfocar estrategias</td>
            </tr>
        </tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)

    # Explicación detallada con expanders
    with st.expander("Clusters 2 y 4 → Clientes Premium"):
        st.write("""
        - **Característica:** Generan altos ingresos a largo plazo, tienen un margen positivo y realizan compras recurrentes.
        - **Estrategias:**
        - Programas VIP y recompensas por fidelidad.
        - Cross-selling con productos complementarios.
        - Servicio personalizado y atención prioritaria.
        """)

    with st.expander("Clusters 1 y 3 → Clientes Potenciales"):
        st.write("""
        - **Característica:** Son rentables, pero su CLV es moderado, pueden aumentar su contribución si se estimulan las compras.
        - **Estrategias:**
        - Descuentos progresivos para incentivar recompra.
        - Campañas de retargeting con promociones personalizadas.
        - Ofrecer financiación para compras más grandes.
        """)

    with st.expander("Clusters 0 y 5 → Clientes No Rentables"):
        st.write("""
        - **Característica:** CLV bajo o negativo, generan pocos ingresos y pueden representar costos elevados en mantenimiento.
        - **Estrategias:**
        - Analizar por qué generan pérdidas y reducir costos.
        - Ofertas específicas para mejorar su conversión.
        - Evitar promociones costosas dirigidas a estos clientes.
        """)

    st.success("Objetivo: Aumentar el valor de los clientes potenciales, retener a los clientes premium y optimizar recursos en clientes menos rentables.")