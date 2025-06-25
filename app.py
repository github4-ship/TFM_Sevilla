# =======================
# BLOQUE 1: LIBRERÍAS
# =======================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# =======================
# BLOQUE 2: CARGA DE DATOS
# =======================
@st.cache_data
def cargar_datos():
    df = pd.read_csv("fans_con_score_y_cluster.csv")
    resumen = pd.read_csv("resumen_clusters.csv")
    return df, resumen

df_fans, resumen_clusters = cargar_datos()

# =======================
# BLOQUE 3: ESTILO GENERAL
# =======================
st.set_page_config(page_title="Fan Value Engine", layout="wide")
st.markdown("""
    <style>
        body { background-color: #0D0D0D; color: white; }
        .css-1rs6os.edgvbvh3 { background-color: #0D0D0D; }
    </style>
""", unsafe_allow_html=True)

# =======================
# BLOQUE 4: BARRA LATERAL
# =======================
st.sidebar.title("📊 Navegación")
seccion = st.sidebar.radio("Selecciona una sección:", [
    "Resumen General",
    "Clusters",
    "Detalle por Fan",
    "Segmentación avanzada"  # Nuevo apartado
])

# =======================
# BLOQUE 5: RESUMEN GENERAL
# =======================
if seccion == "Resumen General":
    st.title("📈 Análisis General de la Base de Fans")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Fans", len(df_fans))
    col2.metric("Fan Score Medio", round(df_fans["Fan_Score"].mean(), 2))
    col3.metric("Prob. Media de Churn", f'{df_fans["Prob_Churn"].mean():.2%}')

    st.subheader("🎯 Distribución por Nivel de Fan")
    fig1 = px.histogram(df_fans, x="Nivel_Fan", color="Nivel_Fan", title="Distribución de Segmentos")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🧠 Engagement Digital (GA4)")
    fig2 = px.box(df_fans, x="Nivel_Fan", y="Engagement_GA4", color="Nivel_Fan")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🛍️ Gasto Total por Nivel de Fan")
    fig3 = px.box(df_fans, x="Nivel_Fan", y="Gasto_Total_€", color="Nivel_Fan")
    st.plotly_chart(fig3, use_container_width=True)

# =======================
# BLOQUE 6: CLUSTERS
# =======================
elif seccion == "Clusters":
    st.title("🔬 Segmentación por Clusters")

    st.dataframe(resumen_clusters)

    st.subheader("💡 Radar Comparativo de Métricas")

    cluster_id = st.selectbox("Selecciona un cluster", resumen_clusters["Cluster"].unique())
    metrics = ["Fan_Score", "Frecuencia_Visitas_Web", "Interacciones_RRSS",
               "Compras_Ecommerce", "Gasto_Total_€", "Miembro_Programa_Fidelidad"]

    cluster_vals = resumen_clusters[resumen_clusters["Cluster"] == cluster_id][metrics].values.flatten()
    max_vals = resumen_clusters[metrics].max().values
    norm_vals = cluster_vals / max_vals

    fig_radar = go.Figure(data=go.Scatterpolar(
        r=norm_vals,
        theta=metrics,
        fill='toself',
        name=f'Cluster {cluster_id}',
        line=dict(color='#00F5A0')
    ))
    fig_radar.update_layout(polar=dict(bgcolor="#0D0D0D"), showlegend=False)
    st.plotly_chart(fig_radar, use_container_width=True)

# =======================
# BLOQUE 7: DETALLE INDIVIDUAL
# =======================
elif seccion == "Detalle por Fan":
    st.title("👤 Análisis Individual")

    fan_id = st.selectbox("Selecciona un Fan_ID", df_fans["Fan_ID"].unique())
    fan = df_fans[df_fans["Fan_ID"] == fan_id].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Fan Score", round(fan["Fan_Score"], 2))
    col2.metric("Nivel", fan["Nivel_Fan"])
    col3.metric("Cluster", fan["Cluster"])

    st.subheader("⚙️ Métricas Avanzadas")
    st.json({
        "Edad": fan["Edad"],
        "Localidad": fan["Localidad"],
        "Canal": fan["Canal"],
        "Visitas App": fan["Frecuencia_Visitas_Web"],
        "Interacciones en RRSS": fan["Interacciones_RRSS"],
        "Clickrate Newsletter": fan["Clickrate_Newsletter"],
        "Compras Totales": fan["Compras_Ecommerce"],
        "Participación en Eventos": fan["Participacion_Eventos"]
    })

# =======================
# BLOQUE 8: SEGMENTACIÓN AVANZADA (nuevo)
# =======================
elif seccion == "Segmentación avanzada":
    st.title("🎯 Segmentación Avanzada")

    st.write("Explora relaciones entre dos métricas para detectar patrones por tipo de fan.")

    col_x, col_y = st.columns(2)
    metricas_disp = df_fans.select_dtypes(include=["float", "int"]).columns.tolist()

    x_axis = col_x.selectbox("Variable en eje X", metricas_disp, index=metricas_disp.index("Fan_Score"))
    y_axis = col_y.selectbox("Variable en eje Y", metricas_disp, index=metricas_disp.index("Gasto_Total_€"))

    fig4 = px.scatter(df_fans, x=x_axis, y=y_axis, color="Nivel_Fan",
                      size="Compras_Ecommerce", hover_name="Fan_ID",
                      title=f"Relación entre {x_axis} y {y_axis}",
                      color_discrete_sequence=px.colors.qualitative.Antique)

    st.plotly_chart(fig4, use_container_width=True)

# =======================
# FIN
# =======================
