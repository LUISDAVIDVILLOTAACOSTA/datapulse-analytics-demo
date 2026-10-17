import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

# 1. Configuración de la página Demo
st.set_page_config(page_title="DataPulse | Demo Evaluativa", page_icon="🔒", layout="wide")

# 2. INYECCIÓN DE CSS (Diseño UI con Candado de Bloqueo)
custom_css = """
<style>
    .main { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Roboto, sans-serif; }
    .demo-banner {
        background: linear-gradient(135deg, #451a03 0%, #0f172a 100%);
        border: 1px solid #78350f;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
    .main-title {
        background: linear-gradient(90deg, #ef4444, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
    }
    .lock-alert {
        background-color: #7f1d1d;
        color: #fca5a5;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #b91c1c;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #1e293b;
        border-left: 5px solid #ef4444;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .metric-title { color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; }
    .metric-value { color: #f8fafc; font-size: 1.8rem; font-weight: 700; margin-top: 5px; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Banner Informativo de la Demo Comercial
st.markdown("""
<div class="demo-banner">
    <h1 class="main-title">📊 DataPulse Analytics (Modo Demo)</h1>
    <p style="color: #f59e0b; font-size: 1.1rem; margin-top: 5px; font-weight: 500;">
        🔒 EDICIÓN DEMOSTRATIVA EN VIVO - LICENCIA COMERCIAL RESTRINGIDA
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="lock-alert">🔒 BOTÓN DE DESCARGA EJECUTIVA BLOQUEADO EN MODO EVALUATIVO. ADQUIERA LA LICENCIA COMPLETA PARA EXPORTAR INFORMES CORPORATIVOS.</div>', unsafe_allow_html=True)

# 4. Zona de Carga de Archivos
uploaded_file = st.file_uploader("📂 Carga un archivo de Excel (.xlsx) o CSV de prueba", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"🎯 Archivo evaluativo '{uploaded_file.name}' cargado en la memoria RAM temporal.")
        columnas_reales = list(df.columns)
        
        # Mapeo básico en pantalla central
        st.markdown("### 🛠️ Configuración de Mapeo Básico")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            col_producto_elegida = st.selectbox("Columna Clasificación:", columnas_reales, index=0)
        with col_c2:
            col_cantidad_elegida = st.selectbox("Columna Volúmenes:", columnas_reales, index=0)
        with col_c3:
            col_total_elegida = st.selectbox("Columna Valores Métricos:", columnas_reales, index=0)
        
        # Procesamiento matemático básico
        df_procesado = df.copy()
        df_procesado[col_total_elegida] = pd.to_numeric(df_procesado[col_total_elegida], errors='coerce').fillna(0)
        df_procesado[col_cantidad_elegida] = pd.to_numeric(df_procesado[col_cantidad_elegida], errors='coerce').fillna(0)
        
        total_valores = df_procesado[col_total_elegida].sum()
        total_volumen = df_procesado[col_cantidad_elegida].sum()
        promedio_calculado = df_procesado[col_total_elegida].mean()
        
        # KPIs de la Demo
        st.markdown('### 📈 Muestreo de Indicadores Globales')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">TOTAL ACUMULADO</div><div class="metric-value">{total_valores:,.2f}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">VOLUMEN PROCESADO</div><div class="metric-value">{int(total_volumen):,} Uds.</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">PROMEDIO CALCULADO</div><div class="metric-value">{promedio_calculado:,.2f}</div></div>', unsafe_allow_html=True)
        
        # Gráfica básica estática
        st.markdown("### 🏆 Gráfica de Distribución General")
        top_grafico = df_procesado.groupby(col_producto_elegida)[col_cantidad_elegida].sum().sort_values(ascending=False).head(5)
        st.bar_chart(top_grafico, color="#ef4444")
        
        st.markdown("---")
        st.markdown("### 📄 Centro de Descargas (Bloqueado)")
        
        # Botón bloqueado simulado (El candado comercial)
        st.button("📥 Descargar Documento Ejecutivo Completo (PDF)", disabled=True, help="Función restringida en la versión Demo. Adquiera la Licencia Pro corporativa.")
        st.caption("⚠️ Para desbloquear la exportación automática en PDF con gráficos integrados, las alertas de negocio e informes en Excel, adquiera el paquete comercial completo en Gumroad.")
        
        st.markdown("### 📋 Vista Previa de la Tabla")
        st.dataframe(df_procesado.head(10), use_container_width=True)

    except Exception as e:
        st.error(f"Error en el motor básico: {e}")
else:
    st.info("💡 Modo Demostración Activo. Suba un archivo para evaluar el renderizado básico del panel.")
