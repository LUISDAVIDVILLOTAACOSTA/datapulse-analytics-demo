import streamlit as st
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import io

# 1. Configuración de la página con estilo moderno y tema oscuro
st.set_page_config(page_title="DataPulse | Analizador Pro", page_icon="⚡", layout="wide")

# 2. INYECCIÓN DE CSS AVANZADO (Diseño Interfaz Premium)
custom_css = """
<style>
    .main { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Roboto, sans-serif; }
    .tech-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid #1e293b;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    .tech-banner::before {
        content: "";
        position: absolute;
        top: 0; right: 0; bottom: 0; left: 0;
        opacity: 0.15;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://w3.org" width="100" height="100" viewBox="0 0 100 100"><circle cx="10" cy="10" r="2" fill="%2310b981"/><circle cx="60" cy="20" r="3" fill="%233b82f6"/><line x1="10" y1="10" x2="60" y2="20" stroke="%233b82f6" stroke-width="0.5"/></svg>');
        background-size: 150px 150px;
    }
    .main-title {
        background: linear-gradient(90deg, #10b981, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem;
        font-weight: 800;
        margin: 0;
    }
    .metric-card {
        background-color: #1e293b;
        border-left: 5px solid #10b981;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    .metric-title { color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { color: #f8fafc; font-size: 2rem; font-weight: 700; margin-top: 5px; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Renderizado del Banner Superior
st.markdown("""
<div class="tech-banner">
    <h1 class="main-title">⚡ DataPulse Analytics</h1>
    <p style="color: #38bdf8; font-size: 1.2rem; margin-top: 5px; font-weight: 500;">
        <span>●</span> Motor de Procesamiento Flexible Activo
    </p>
</div>
""", unsafe_allow_html=True)

# 4. Zona de Carga de Archivos
uploaded_file = st.file_uploader("📂 Arrastra aquí cualquier archivo de Excel (.xlsx) o CSV", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # Cargar el archivo según su extensión
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"🎯 Archivo '{uploaded_file.name}' sincronizado con éxito.")
        
        # Obtener la lista completa de columnas reales del Excel del usuario
        columnas_reales = list(df.columns)
        
        st.markdown("### 🛠️ Configuración del Mapeo de Datos")
        st.write("Selecciona cuáles son las columnas que deseas analizar de tu archivo:")
        
        col_sel1, col_sel2, col_sel3 = st.columns(3)
        
        with col_sel1:
            col_producto_elegida = st.selectbox("Columna de Clasificación (Ej: Tipo de Servicio o Producto):", columnas_reales, index=0)
            
        with col_sel2:
            col_cantidad_elegida = st.selectbox("Columna de Volúmenes (Ej: Tiempos o Cantidades):", columnas_reales, index=0)
            
        with col_sel3:
            col_total_elegida = st.selectbox("Columna de Valores Métricos (Ej: Tiempos de Resolución o Totales):", columnas_reales, index=0)
            
        st.markdown("---")
        
        # --- PROCESAMIENTO MATEMÁTICO ---
        df_procesado = df.copy()
        df_procesado[col_total_elegida] = pd.to_numeric(df_procesado[col_total_elegida], errors='coerce').fillna(0)
        df_procesado[col_cantidad_elegida] = pd.to_numeric(df_procesado[col_cantidad_elegida], errors='coerce').fillna(0)
        
        total_ingresos = df_procesado[col_total_elegida].sum()
        total_productos = df_procesado[col_cantidad_elegida].sum()
        ticket_promedio = df_procesado[col_total_elegida].mean() if len(df_procesado) > 0 else 0
        
        # Renderizado de Tarjetas KPIs Dinámicas e Inteligentes
        st.markdown('### 📈 Tablero de Control de KPIs')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">📊 TOTAL: {col_total_elegida.upper()}</div><div class="metric-value">{total_ingresos:,.2f}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card" style="border-left-color: #3b82f6;"><div class="metric-title">📦 VOLUMEN: {col_cantidad_elegida.upper()}</div><div class="metric-value">{int(total_productos):,} Uds.</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card" style="border-left-color: #a855f7;"><div class="metric-title">🛒 PROMEDIO DE: {col_total_elegida.upper()}</div><div class="metric-value">{ticket_promedio:,.2f}</div></div>', unsafe_allow_html=True)

        
        # Renderizado de Gráfico en la Web de Streamlit
        st.markdown("### 🏆 Distribución Gráfica de Datos")
        top_productos = df_procesado.groupby(col_producto_elegida)[col_cantidad_elegida].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top_productos, color="#10b981")
        
        # Generar gráfico en memoria RAM para estampar en el PDF corporativo
        fig, ax = plt.subplots(figsize=(6, 3))
        top_productos.plot(kind='bar', ax=ax, color='#10b981')
        ax.set_title("Analisis por Segmentacion de Datos", fontsize=10, fontweight='bold')
        plt.xticks(rotation=30, ha='right', fontsize=8)
        plt.tight_layout()
        
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png', dpi=150)
        img_buf.seek(0)
        plt.close(fig)

        st.markdown("---")
        st.markdown("### 📄 Reporte de Salida")
        
        # --- CONSTRUCCIÓN SÓLIDA DEL DOCUMENTO PDF ---
        pdf = FPDF()
        pdf.add_page()
        
        # Encabezado corporativo oscuro
        pdf.set_fill_color(15, 23, 42) 
        pdf.rect(0, 0, 210, 35, 'F')
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_text_color(16, 185, 129) 
        pdf.text(15, 22, "DATAPULSE AUTOMATED REPORT")
        
        # Datos tabulados del reporte ejecutivo
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Helvetica", "B", 12)
        pdf.ln(35)
        pdf.cell(0, 10, "Resumen Tecnico de Analitica", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(60, 8, f"Suma Total Evaluada: {total_ingresos:,.2f}", ln=True)
        pdf.cell(60, 8, f"Registros / Volumen Procesado: {int(total_productos):,} unidades", ln=True)
        pdf.cell(60, 8, f"Valor Promedio General: {ticket_promedio:,.2f}", ln=True)
        
        # Estampado del gráfico binario dentro del documento PDF
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "Grafico Estadistico de Rendimiento", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.image(img_buf, w=140)
        img_buf.close()
            
        pdf.y = 265
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, "Reporte universal generado mediante DataPulse Core Engine v1.2.", align="C")
        
        # Conversión segura a bytes estándar
        pdf_output = bytes(pdf.output())
        
        st.download_button(
            label="📥 Descargar Documento Ejecutivo Completo (PDF)",
            data=pdf_output,
            file_name="Reporte_DataPulse_Universal.pdf",
            mime="application/pdf"
        )
        
        st.markdown("### 📋 Tabla de Datos Completa")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Fallo en el motor de renderizado matemático: {e}")
else:
    # Estado inicial de espera
    st.info("💡 Panel en espera de origen de datos. Por favor, arrastra tu archivo Excel para activar el análisis computacional.")
    st.markdown("""
    <div style="text-align: center; margin-top: 5px; opacity: 0.3;">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5">
            <path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path>
            <path d="M22 12A10 10 0 0 0 12 2v10z"></path>
        </svg>
        <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 10px;">DataPulse Core Engine v1.2</p>
    </div>
    """, unsafe_allow_html=True)
