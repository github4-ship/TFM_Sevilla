# app_CON_Radar.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("CSV_Corregido_para_App.csv")
    return df

df_fans = load_data()

# Correcciones de tipo
for col in df_fans.columns:
    if df_fans[col].dtype == object:
        df_fans[col] = df_fans[col].replace("np.int64(.*)", "", regex=True)
        df_fans[col] = df_fans[col].replace("N/A", np.nan)

# Convertir numéricos donde aplique
numericas = ["Fan_Score", "visitas_app", "Interacciones_RRSS", "Compras_Ecommerce", "Gasto_Total_€"]
for col in numericas:
    df_fans[col] = pd.to_numeric(df_fans[col], errors="coerce")

# Configuración de página
st.set_page_config(page_title="Segmentación Avanzada", layout="wide")
st.title("Segementación Avanzada")

# Sidebar navegación
st.sidebar.title("🔄 Navegación")
opcion = st.sidebar.radio("Selecciona una sección:", [
    "Resumen General", "Clusters", "Detalle por Fan", "Segmentación avanzada"])

# 1. Resumen General
if opcion == "Resumen General":
    st.header("🔹 Distribución por Nivel de Fan")
    fig1 = px.histogram(df_fans, x="cluster_marketing", color="cluster_marketing",
                        color_discrete_sequence=px.colors.qualitative.Set1,
                        labels={"cluster_marketing": "Nivel_Fan"},
                        title="Distribución de Segmentos")
    st.plotly_chart(fig1, use_container_width=True)

# 2. Clusters
elif opcion == "Clusters":
    st.header("🧠 Engagement Digital (GA4)")
    if "visitas_app" in df_fans.columns:
        fig2 = px.box(df_fans, y="visitas_app", color="cluster_marketing",
                     color_discrete_sequence=px.colors.qualitative.Pastel,
                     title="Distribución de Visitas App por Cluster")
        st.plotly_chart(fig2, use_container_width=True)

# 3. Detalle por Fan
elif opcion == "Detalle por Fan":
    st.header(":busts_in_silhouette: Análisis Individual")
    fan_id = st.selectbox("Selecciona un Fan_ID", df_fans["Fan_ID"].unique())
    fan_data = df_fans[df_fans["Fan_ID"] == fan_id].squeeze()

    st.metric("Fan Score", f"{fan_data['Fan_Score']:.2f}")
    st.metric("Nivel", fan_data.get("cluster_marketing", "N/A"))

    st.subheader(":gear: Métricas Avanzadas")
    cols_advanced = ["edad", "localidad", "canal", "visitas_app", "Interacciones_RRSS", 
                     "clickrate_newsletter", "Compras_Ecommerce", "participacion_eventos", 
                     "Miembro_Programa_Fidelidad", "Gasto_Total_€"]
    dict_metrica = {col: fan_data.get(col, "N/A") for col in cols_advanced}
    st.json(dict_metrica)

    # ➕ Añadir radar chart
    st.subheader("📊 Perfil Comparado (Radar)")
    radar_cols = ["Fan_Score", "visitas_app", "Interacciones_RRSS", "Compras_Ecommerce", "Gasto_Total_€"]
    valores_fan = fan_data[radar_cols].values.astype(float)

    if not np.isnan(valores_fan).any():
        maximos = df_fans[radar_cols].max()
        normales = valores_fan / maximos

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=normales,
            theta=radar_cols,
            fill='toself',
            name=f"Fan {fan_id}",
            line_color='gold'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], showticklabels=False),
            ),
            showlegend=False,
            template="plotly_dark",
            height=400
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.warning("Datos insuficientes para mostrar radar.")

# 4. Segmentación avanzada
elif opcion == "Segmentación avanzada":
    st.header(":dart: Segmentación Avanzada")
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
