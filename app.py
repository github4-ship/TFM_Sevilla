import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# ========== BLOQUE 1: CARGA DE DATOS ==========
@st.cache_data
def load_data():
    df = pd.read_csv("CSV_Corregido_para_App.csv")
    return df

df_fans = load_data()

# Limpiar campos de texto problemáticos
for col in df_fans.columns:
    if df_fans[col].dtype == object:
        df_fans[col] = df_fans[col].replace("np.int64(.*)", "", regex=True)
        df_fans[col] = df_fans[col].replace("N/A", np.nan)

# ========== BLOQUE 2: CONFIGURACIÓN GENERAL ==========
st.set_page_config(page_title="Fan Value Engine", layout="wide")
st.title("🚀 Fan Value Engine")

st.sidebar.title("🔄 Navegación")
opcion = st.sidebar.radio("Selecciona una sección:", [
    "Resumen General", 
    "Clusters", 
    "Detalle por Fan", 
    "Segmentación avanzada", 
    "Engagement Digital",
    "Despliegue Real del Fan Value Engine"
])

# ========== 1. RESUMEN GENERAL ==========
if opcion == "Resumen General":
    st.header("📊 Distribución por Nivel de Fan")
    fig1 = px.histogram(df_fans, x="cluster_marketing", color="cluster_marketing",
                        color_discrete_sequence=px.colors.qualitative.Set1,
                        title="Distribución de Segmentos")
    st.plotly_chart(fig1, use_container_width=True)

# ========== 2. CLUSTERS ==========
elif opcion == "Clusters":
    st.header("🧠 Visitas a App por Cluster")
    if "visitas_app" in df_fans.columns:
        fig2 = px.box(df_fans, y="visitas_app", color="cluster_marketing",
                     color_discrete_sequence=px.colors.qualitative.Pastel,
                     title="Distribución de Visitas App por Cluster")
        st.plotly_chart(fig2, use_container_width=True)

# ========== 3. DETALLE POR FAN ==========
elif opcion == "Detalle por Fan":
    st.header("👤 Análisis Individual")
    fan_id = st.selectbox("Selecciona un Fan_ID", df_fans["Fan_ID"].unique())
    fan_data = df_fans[df_fans["Fan_ID"] == fan_id].squeeze()

    st.metric("Fan Score", f"{fan_data['Fan_Score']:.2f}")
    st.metric("Nivel", fan_data.get("cluster_marketing", "N/A"))

    st.subheader("⚙️ Métricas Avanzadas")
    cols_advanced = ["edad", "localidad", "canal", "visitas_app", "Interacciones_RRSS", 
                     "clickrate_newsletter", "Compras_Ecommerce", "participacion_eventos", 
                     "Miembro_Programa_Fidelidad", "Gasto_Total_€"]
    dict_metrica = {col: fan_data.get(col, "N/A") for col in cols_advanced}
    st.json(dict_metrica)

# ========== 4. SEGMENTACIÓN AVANZADA ==========
elif opcion == "Segmentación avanzada":
    st.header("📈 Segmentación Avanzada")
    st.markdown("Explora relaciones entre dos métricas para detectar patrones por tipo de fan.")

    col1, col2 = st.columns(2)
    x_axis = col1.selectbox("Variable en eje X", df_fans.columns, index=df_fans.columns.get_loc("Fan_Score"))
    y_axis = col2.selectbox("Variable en eje Y", df_fans.columns, index=df_fans.columns.get_loc("Gasto_Total_€"))

    try:
        fig4 = px.scatter(df_fans, x=x_axis, y=y_axis, color="cluster_marketing",
                          size="Compras_Ecommerce", hover_name="Fan_ID",
                          title=f"Relación entre {x_axis} y {y_axis}",
                          color_discrete_sequence=px.colors.qualitative.Antique)
        st.plotly_chart(fig4, use_container_width=True)
    except Exception as e:
        st.error(f"Error generando el gráfico: {e}")

# ========== 5. ENGAGEMENT DIGITAL ==========
elif opcion == "Engagement Digital":
    st.header("💡 Engagement Digital")
    st.markdown("Análisis de comportamiento y participación digital de los fans.")

    st.subheader("🔍 Correlación entre variables de comportamiento")
    cols_digitales = ["visitas_app", "Interacciones_RRSS", "clickrate_newsletter", "participacion_eventos"]
    corr_matrix = df_fans[cols_digitales].corr()
    fig_corr, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr_matrix, annot=True, cmap="Blues", fmt=".2f", ax=ax)
    st.pyplot(fig_corr)

    st.subheader("📲 Interacciones en RRSS por Cluster")
    if "Interacciones_RRSS" in df_fans.columns:
        fig_rrss = px.box(df_fans, x="cluster_marketing", y="Interacciones_RRSS", color="cluster_marketing",
                          title="Distribución de Interacciones en RRSS")
        st.plotly_chart(fig_rrss, use_container_width=True)

    st.subheader("🎟️ Participación en Eventos por Edad")
    if "participacion_eventos" in df_fans.columns:
        fig_eventos = px.scatter(df_fans, x="edad", y="participacion_eventos", color="cluster_marketing",
                                 title="Relación Edad vs Participación en Eventos")
        st.plotly_chart(fig_eventos, use_container_width=True)

    st.subheader("📧 Clickrate Newsletter vs Fan Score")
    if "clickrate_newsletter" in df_fans.columns:
        fig_news = px.scatter(df_fans, x="Fan_Score", y="clickrate_newsletter", color="cluster_marketing",
                              title="Relación entre Fan Score y Clickrate Newsletter")
        st.plotly_chart(fig_news, use_container_width=True)

# ========== 6. ANEXO IV – PLAN DE DESPLIEGUE ==========
elif opcion == "Despliegue Real del Fan Value Engine":
    

    # Gráfico Gantt
    st.subheader("📆 Calendario de Despliegue")
    despliegue = pd.DataFrame({
        "Fase": ["Integración", "Automatización", "Escalado", "Evaluación"],
        "Inicio": ["2025-07-01", "2025-08-01", "2025-09-01", "2025-10-01"],
        "Fin": ["2025-07-31", "2025-08-31", "2025-09-30", "2025-10-31"]
    })
    despliegue["Inicio"] = pd.to_datetime(despliegue["Inicio"])
    despliegue["Fin"] = pd.to_datetime(despliegue["Fin"])
    fig_gantt = px.timeline(despliegue, x_start="Inicio", x_end="Fin", y="Fase", color="Fase",
                            title="📆 Calendario de Despliegue del Fan Value Engine")
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True)

    # Gráfico Funnel
    st.subheader("🚀 Funnel de Madurez del Despliegue")
    funnel = go.Figure(go.Funnel(
        y = ["Evaluación", "Escalado", "Automatización", "Integración"],
        x = [50, 100, 150, 200],
        textinfo = "value+percent previous"
    ))
    st.plotly_chart(funnel, use_container_width=True)

    # Gráfico Radar
    st.subheader("📊 Radar de KPIs tras Despliegue")
    kpis = pd.DataFrame({
        "KPI": ["Retención", "Conversión", "Satisfacción", "ROI", "Feedback Interno"],
        "Valor": [85, 70, 90, 75, 65]
    })
    fig_radar = px.line_polar(kpis, r="Valor", theta="KPI", line_close=True,
                              title="📊 KPIs del Fan Value Engine")
    fig_radar.update_traces(fill='toself')
    st.plotly_chart(fig_radar, use_container_width=True)
