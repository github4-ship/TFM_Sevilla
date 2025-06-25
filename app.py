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
        body {
            background-color: #0D0D0D;
            color: white;
        }
        .css-1rs6os.edgvbvh3 {
            background-color: #0D0D0D;
        }
    </style>
""", unsafe_allow_html=True)

# =======================
# BLOQUE 4: BARRA LATERAL
# =======================
st.sidebar.title("📊 Navegación")
seccion = st.sidebar.radio("Selecciona una sección:", ["Resumen General", "Clusters", "Detalle por Fan"])

# =======================
# BLOQUE 5: RESUMEN GENERAL
# =======================
if seccion == "Resumen General":
    st.title("📈 Análisis General de la Base de Fans")

    col1, col2 = st.columns(2)
    col1.metric("Total Fans", len(df_fans))
    col2.metric("Gasto Total Medio", f"{df_fans['gasto_total'].mean():.2f} €")

    st.subheader("🎯 Distribución por Cluster")
    fig1 = px.histogram(df_fans, x="cluster_marketing", color="cluster_marketing", title="Distribución de Clusters")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🧠 Interacciones en Redes Sociales")
    fig2 = px.box(df_fans, x="cluster_marketing", y="interacciones_redes", color="cluster_marketing")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🛍️ Gasto Total por Cluster")
    fig3 = px.box(df_fans, x="cluster_marketing", y="gasto_total", color="cluster_marketing")
    st.plotly_chart(fig3, use_container_width=True)

# =======================
# BLOQUE 6: CLUSTERS
# =======================
elif seccion == "Clusters":
    st.title("🔬 Segmentación por Clusters")

    st.dataframe(resumen_clusters)

    st.subheader("💡 Radar Comparativo de Métricas")
    cluster_id = st.selectbox("Selecciona un cluster", resumen_clusters["cluster_marketing"].unique())

    # Asegúrate de que estas métricas existan en el CSV resumen_clusters
    metrics = [col for col in resumen_clusters.columns if col not in ["cluster_marketing"]]
    cluster_vals = resumen_clusters[resumen_clusters["cluster_marketing"] == cluster_id][metrics].values.flatten()
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

    fan_id = st.selectbox("Selecciona un fan_id", df_fans["fan_id"].unique())
    fan = df_fans[df_fans["fan_id"] == fan_id].iloc[0]

    col1, col2 = st.columns(2)
    col1.metric("Gasto Total (€)", round(fan["gasto_total"], 2))
    col2.metric("Cluster", fan["cluster_marketing"])

    st.subheader("⚙️ Métricas Avanzadas")
    st.write({
        "Edad": fan["edad"],
        "Localidad": fan["localidad"],
        "Canal": fan["canal"],
        "Visitas App": fan["visitas_app"],
        "Interacciones en RRSS": fan["interacciones_redes"],
        "Clickrate Newsletter": fan["clickrate_newsletter"],
        "Compras Totales": fan["compras_total"],
        "Participación en Eventos": fan["participacion_eventos"]
    })
