import streamlit as st
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import io

# 1. Configuración de la página Pro Avanzada
st.set_page_config(page_title="DataPulse | Analizador Pro v2.0", page_icon="⚡", layout="wide")

# 2. INYECCIÓN DE CSS AVANZADO (Diseño UI Premium)
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
    
    /* Tarjetas de Alerta */
    .insight-card {
        background-color: #1c1917;
        border-left: 5px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Renderizado del Banner Superior Pro
st.markdown("""
<div class="tech-banner">
    <h1 class="main-title">⚡ DataPulse Analytics Pro v2.0</h1>
    <p style="color: #38bdf8; font-size: 1.2rem; margin-top: 5px; font-weight: 500;">
        <span>●</span> Licencia Corporativa Global Inteligente Activa
    </p>
</div>
""", unsafe_allow_html=True)

# 4. Zona de Carga de Archivos
uploaded_file = st.file_uploader("📂 Arrastra aquí cualquier archivo de Excel (.xlsx) o CSV", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"🎯 Archivo '{uploaded_file.name}' sincronizado con éxito.")
        columnas_reales = list(df.columns)
        
        # Mapeo de columnas inicial en la barra lateral
        st.sidebar.markdown("## 🛠️ Mapeo de Datos Maestro")
        col_producto_elegida = st.sidebar.selectbox("Columna de Clasificación (Texto):", columnas_reales, index=0)
        col_cantidad_elegida = st.sidebar.selectbox("Columna de Volúmenes (Números):", columnas_reales, index=0)
        col_total_elegida = st.sidebar.selectbox("Columna de Valores Métricos (Números):", columnas_reales, index=0)
        
        # --- PROCESAMIENTO Y LIMPIEZA MATEMÁTICA ---
        df_procesado = df.copy()
        df_procesado[col_total_elegida] = pd.to_numeric(df_procesado[col_total_elegida], errors='coerce').fillna(0)
        df_procesado[col_cantidad_elegida] = pd.to_numeric(df_procesado[col_cantidad_elegida], errors='coerce').fillna(0)
        df_procesado[col_producto_elegida] = df_procesado[col_producto_elegida].astype(str).str.strip()
        
        # --- FILTROS DINÁMICOS EN LA BARRA LATERAL ---
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 🔍 Filtros Inteligentes")
        
        categorias_disponibles = sorted(df_procesado[col_producto_elegida].unique())
        categorias_seleccionadas = st.sidebar.multiselect(
            f"Filtrar por {col_producto_elegida}:", 
            options=categorias_disponibles, 
            default=categorias_disponibles
        )
        
        # Aplicar el filtro dinámico al DataFrame en tiempo real
        df_filtrado = df_procesado[df_procesado[col_producto_elegida].isin(categorias_seleccionadas)]
        
        if len(df_filtrado) > 0:
            total_valores = df_filtrado[col_total_elegida].sum()
            total_volumen = df_filtrado[col_cantidad_elegida].sum()
            promedio_calculado = df_filtrado[col_total_elegida].mean()
            
            # Renderizado de Tarjetas KPIs Dinámicas
            st.markdown('### 📈 Panel de Indicadores Clave (Datos Filtrados)')
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric-card"><div class="metric-title">📊 TOTAL: {col_total_elegida.upper()}</div><div class="metric-value">{total_valores:,.2f}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card" style="border-left-color: #3b82f6;"><div class="metric-title">📦 VOLUMEN: {col_cantidad_elegida.upper()}</div><div class="metric-value">{int(total_volumen):,} Uds.</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-card" style="border-left-color: #a855f7;"><div class="metric-title">🛒 PROMEDIO DE: {col_total_elegida.upper()}</div><div class="metric-value">{promedio_calculado:,.2f}</div></div>', unsafe_allow_html=True)
            
            # --- MÓDULO DE TARJETAS DE ALERTA (INSIGHTS AUTOMÁTICOS) ---
            st.markdown("### 🤖 Diagnóstico Inteligente del Sistema")
            col_in1, col_in2 = st.columns(2)
            
            resumen_agrupado = df_filtrado.groupby(col_producto_elegida)[col_cantidad_elegida].sum().sort_values(ascending=False)
            top_elemento = resumen_agrupado.index[0]
            peor_elemento = resumen_agrupado.index[-1]
            
            with col_in1:
                st.markdown(f"""
                <div class="insight-card" style="border-left-color: #10b981;">
                    <b style="color: #10b981;">🔥 MÁXIMO RENDIMIENTO:</b><br>
                    El elemento <b>{top_elemento}</b> registra la mayor actividad con un volumen acumulado de <b>{int(resumen_agrupado.max()):,}</b> unidades.
                </div>
                """, unsafe_allow_html=True)
            with col_in2:
                st.markdown(f"""
                <div class="insight-card" style="border-left-color: #ef4444;">
                    <b style="color: #ef4444;">⚠️ CONTROL REQUERIDO:</b><br>
                    El elemento <b>{peor_elemento}</b> registra el menor desempeño en los datos actuales con solo <b>{int(resumen_agrupado.min()):,}</b> unidades procesadas.
                </div>
                """, unsafe_allow_html=True)
            
            # Renderizado de Gráfico en la Web de Streamlit
            st.markdown("### 🏆 Distribución Gráfica Operativa")
            top_grafico = df_filtrado.groupby(col_producto_elegida)[col_cantidad_elegida].sum().sort_values(ascending=False).head(10)
            st.bar_chart(top_grafico, color="#3b82f6")
            
            # Generar gráfico en memoria RAM para estampar en el PDF
            fig, ax = plt.subplots(figsize=(6, 3))
            top_grafico.plot(kind='bar', ax=ax, color='#3b82f6')
            ax.set_title("Segmentacion Operativa v2.0", fontsize=10, fontweight='bold')
            plt.xticks(rotation=30, ha='right', fontsize=8)
            plt.tight_layout()
            
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png', dpi=150)
            img_buf.seek(0)
            plt.close(fig)

            st.markdown("---")
            st.markdown("### 📄 Centro de Descargas e Informes Oficiales")
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                # --- CONSTRUCCIÓN DEL PDF ---
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(15, 23, 42) 
                pdf.rect(0, 0, 210, 35, 'F')
                pdf.set_font("Helvetica", "B", 20)
                pdf.set_text_color(16, 185, 129) 
                pdf.text(15, 22, "DATAPULSE AUTOMATED REPORT v2.0")
                
                pdf.set_text_color(40, 40, 40)
                pdf.set_font("Helvetica", "B", 12)
                pdf.ln(35)
                pdf.cell(0, 10, "Resumen Tecnico de Analitica Avanzada", ln=True)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(5)
                
                pdf.set_font("Helvetica", "", 11)
                pdf.cell(60, 8, f"Suma Total Evaluada: {total_valores:,.2f}", ln=True)
                pdf.cell(60, 8, f"Registros Procesados: {int(total_volumen):,} unidades", ln=True)
                pdf.cell(60, 8, f"Valor Promedio General: {promedio_calculado:,.2f}", ln=True)
                
                pdf.ln(5)
                pdf.image(img_buf, w=140)
                img_buf.close()
                    
                pdf.y = 265
                pdf.set_font("Helvetica", "I", 8)
                pdf.set_text_color(150, 150, 150)
                pdf.cell(0, 10, "Reporte universal de alto impacto generado mediante DataPulse Core v2.0.", align="C")
                
                pdf_output = bytes(pdf.output())
                st.download_button(
                    label="📥 Exportar Informe Ejecutivo (PDF)",
                    data=pdf_output,
                    file_name="Reporte_DataPulse_Avanzado.pdf",
                    key="btn_pdf_pro_v2",
                    mime="application/pdf"
                )
                
            with col_btn2:
                # --- DESCARGA DE DATOS FILTRADOS EN EXCEL ---
                buffer_excel = io.BytesIO()
                with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
                    df_filtrado.to_excel(writer, index=False, sheet_name='Datos_Limpios')
                
                # --- EXTRAER DATOS COMPLETOS Y SELLAR LA CAJA ---
                excel_data = buffer_excel.getvalue()
                
                st.download_button(
                    label="📥 Descargar Base de Datos Filtrada Excel",
                    data=excel_data,
                    file_name="DataPulse_Datos_Filtrados.xlsx",
                    key="btn_excel_pro_v2",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            
            st.markdown("### 📋 Tabla de Datos Sincronizada")
            st.dataframe(df_filtrado, use_container_width=True)
        else:
            st.warning("⚠️ No hay datos coincidentes con los filtros seleccionados en la barra lateral.")

    except Exception as e:
        st.error(f"Fallo en el motor de renderizado matemático: {e}")

                    