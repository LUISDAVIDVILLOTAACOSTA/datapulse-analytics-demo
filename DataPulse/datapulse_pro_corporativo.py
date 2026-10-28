import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import os

st.set_page_config(page_title="DataPulse Pro v2.0", page_icon="⚡", layout="wide")

def load_ui_theme():
    """ Inicializa las hojas de estilo del panel corporativo """
    st.markdown("""
    <style>
        .main { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
        .dp-banner {
            background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
            border: 1px solid #1e293b; padding: 25px; border-radius: 12px; margin-bottom: 25px;
        }
        .dp-title {
            background: linear-gradient(90deg, #10b981, #3b82f6);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-size: 3rem; font-weight: 800; margin: 0;
        }
        .dp-card {
            background-color: #1e293b; border-left: 5px solid #10b981;
            padding: 20px; border-radius: 8px; margin-bottom: 20px;
        }
        .dp-card-meta { color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
        .dp-card-val { color: #f8fafc; font-size: 1.8rem; font-weight: 700; margin-top: 5px; }
        .dp-insight {
            background-color: #1c1917; border-left: 5px solid #f59e0b;
            padding: 15px; border-radius: 6px; margin-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data(show_spinner="Leyendo estructura...")
def load_dataset(file_obj):
    """ Lector optimizado en caché para archivos Excel y CSV """
    try:
        return pd.read_csv(file_obj) if file_obj.name.endswith('.csv') else pd.read_excel(file_obj)
    except Exception as err:
        st.error(f"Error al abrir el archivo: {err}")
        return None


def generate_pdf_report(v_total, q_total, mean_val, img_data):
    """ Compila y genera el reporte ejecutivo en formato PDF corporativo """
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado institucional
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(16, 185, 129)
    pdf.text(15, 22, "DATAPULSE AUTOMATED REPORT v2.0")
    
    # Estructura del cuerpo técnico
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Helvetica", "B", 12)
    pdf.ln(35)
    pdf.cell(0, 10, "Resumen Tecnico de Analitica Avanzada", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Inyección de métricas
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(60, 8, f"Suma Total Evaluada: {v_total:,.2f}", ln=True)
    pdf.cell(60, 8, f"Registros Procesados: {int(q_total):,} unidades", ln=True)
    pdf.cell(60, 8, f"Valor Promedio General: {mean_val:,.2f}", ln=True)
    pdf.ln(5)
    
    # Gestión de persistencia en disco por IO/OS
    ruta_temporal = "temp_grafico_datapulse.png"
    try:
        img_data.seek(0)
        with open(ruta_temporal, "wb") as f_temp:
            f_temp.write(img_data.read())
        img_data.close()
        
        pdf.image(ruta_temporal, w=140)
    except Exception:
        pass
    finally:
        if os.path.exists(ruta_temporal):
            os.remove(ruta_temporal)
            
    # Configuración de pie de página
    pdf.y = 265
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, "Reporte universal de alto impacto generado mediante DataPulse Core v2.0.", align="C")
    
    return pdf.output(dest='S').encode('latin-1')


def export_to_excel(filtered_df):
    """ Empaqueta la tabla filtrada directamente en memoria para descarga """
    buffer_excel = io.BytesIO()
    with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False, sheet_name='Datos_Limpios')
    return buffer_excel.getvalue()


def process_analytics(df, c_prod, c_cant, c_val):
    """ Ejecuta el motor analítico, KPIs, gráficas y descargas empresariales """
    # Normalización de datos numéricos y eliminación de caracteres monetarios
    df[c_val] = pd.to_numeric(df[c_val].astype(str).str.replace('$', '', regex=False).str.strip(), errors='coerce').fillna(0)
    df[c_cant] = pd.to_numeric(df[c_cant].astype(str).str.strip(), errors='coerce').fillna(0)
    df[c_prod] = df[c_prod].astype(str).str.strip()
    
    st.sidebar.markdown("--- \n## 🔍 Filtros Avanzados")
    available_cats = sorted(df[c_prod].unique())
    selected_cats = st.sidebar.multiselect(
        f"Filtrar por {c_prod}:", 
        options=available_cats, 
        default=available_cats
    )
    
    df_filtered = df[df[c_prod].isin(selected_cats)]
    
    if df_filtered.empty:
        st.warning("⚠️ No hay datos coincidentes con los filtros seleccionados en la barra lateral.")
        return

    # Cálculos analíticos de negocio
    v_sum = df_filtered[c_val].sum()
    q_sum = df_filtered[c_cant].sum()
    v_mean = df_filtered[c_val].mean()
    
    # Renderizado del grid de KPIs
    st.markdown('### 📈 Panel de Indicadores Clave (Datos Filtrados)')
    col1, col2, col3 = st.columns(3)
    kpis = [
        (f"Total Acumulado ({c_val})", f"$ {v_sum:,.2f}", "#10b981"),
        (f"Volumen Operativo ({c_cant})", f"{int(q_sum):,} Uds.", "#3b82f6"),
        (f"Promedio Comercial ({c_val})", f"$ {v_mean:,.2f}", "#a855f7")
    ]
    
    for col, (label, value, color) in zip([col1, col2, col3], kpis):
        col.markdown(f"""
        <div class="dp-card" style="border-left-color: {color};">
            <div class="dp-card-meta">{label}</div>
            <div class="dp-card-val">{value}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Diagnóstico inteligente de extremos (INSIGHTS ARREGLADOS CON ÍNDICE EXPLÍCITO)
    st.markdown("### 🤖 Diagnóstico Inteligente de Tendencias")
    grouped_data = df_filtered.groupby(c_prod)[c_cant].sum().sort_values(ascending=False)
    
    # Extracción del primer y último texto string real
    top_item = grouped_data.index[0]
    worst_item = grouped_data.index[-1]
    
    in1, in2 = st.columns(2)
    in1.markdown(f"""
    <div class="dp-insight" style="border-left-color: #10b981;">
        <b style="color: #10b981;">🔥 MÁXIMO DESEMPEÑO:</b><br>
        El registro <b>{top_item}</b> lidera la actividad con un volumen consolidado de <b>{int(grouped_data.max()):,}</b> unidades.
    </div>
    """, unsafe_allow_html=True)
    
    in2.markdown(f"""
    <div class="dp-insight" style="border-left-color: #ef4444;">
        <b style="color: #ef4444;">⚠️ CONTROL REQUERIDO:</b><br>
        El registro <b>{worst_item}</b> muestra el menor desempeño con solo <b>{int(grouped_data.min()):,}</b> unidades procesadas.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🏆 Distribución Gráfica Operativa")
    chart_df = grouped_data.reset_index(name=c_cant).head(10)
    st.bar_chart(chart_df, x=c_prod, y=c_cant, color="#3b82f6")
    
    # Generación en memoria RAM de la figura Matplotlib para el informe
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(chart_df[c_prod], chart_df[c_cant], color='#3b82f6')
    ax.set_title("Segmentacion Operativa v2.0", fontsize=10, fontweight='bold')
    plt.xticks(rotation=30, ha='right', fontsize=8)
    plt.tight_layout()
    
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=150)
    img_buf.seek(0)
    plt.close(fig)
    
    st.markdown("--- \n### 📄 Centro de Informes y Descargas Oficiales")
    c_btn1, c_btn2 = st.columns(2)
    
    with c_btn1:
        pdf_bytes = generate_pdf_report(v_sum, q_sum, v_mean, img_buf)
        st.download_button(
            label="📥 Exportar Informe Ejecutivo (PDF)",
            data=pdf_bytes,
            file_name="Reporte_DataPulse_Avanzado.pdf",
            key="btn_pdf_corporativo_v3",
            mime="application/pdf"
        )
        
    with c_btn2:
        excel_bytes = export_to_excel(df_filtered)
        st.download_button(
            label="📥 Descargar Base de Datos Filtrada Excel",
            data=excel_bytes,
            file_name="DataPulse_Datos_Fltrados.xlsx",
            key="btn_excel_corporativo_v3",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.markdown("### 📋 Tabla de Datos Sincronizada")
    st.dataframe(df_filtered, use_container_width=True)


def main():
    load_ui_theme()
    
    st.markdown("""
    <div class="dp-banner">
        <h1 class="dp-title">⚡ DataPulse Analytics Pro</h1>
        <p style="color: #38bdf8; font-size: 1.1rem; margin-top: 4px; font-weight: 500;">
            <span>●</span> Licencia Corporativa Global Inteligente Activa
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📂 Arrastra aquí cualquier archivo de Excel (.xlsx) o CSV", type=["xlsx", "csv"])
    
    if uploaded_file:
        dataset = load_dataset(uploaded_file)
        if dataset is not None:
            st.success(f"🎯 Sincronización exitosa: {uploaded_file.name}")
            headers = list(dataset.columns)
            
            st.sidebar.markdown("## 🛠️ Configuración Core")
            sel_prod = st.sidebar.selectbox("Columna de Clasificación (Texto):", headers, index=0)
            sel_cant = st.sidebar.selectbox("Columna de Volúmenes (Números):", headers, index=1 if len(headers) > 1 else 0)
            sel_val = st.sidebar.selectbox("Columna de Valores Métricos (Números):", headers, index=2 if len(headers) > 2 else 0)
            
            try:
                process_analytics(dataset, sel_prod, sel_cant, sel_val)
            except Exception as err:
                st.error("Se detectó un problema en el procesamiento interno de los datos:")
                st.code(str(err))
    else:
        st.info("💡 Sistema Pro en espera. Cargue un set de datos corporativo para iniciar el mapeo inteligente.")


if __name__ == '__main__':
    main()
