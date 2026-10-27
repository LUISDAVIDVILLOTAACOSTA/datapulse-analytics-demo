import streamlit as st
import pandas as pd

st.set_page_config(page_title="DataPulse BI", page_icon="🔒", layout="wide")

def load_ui_styles():
    """ Define el tema oscuro y los contenedores de la demo """
    st.markdown("""
    <style>
        .main { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
        .dp-hero {
            background: linear-gradient(135deg, #451a03 0%, #0f172a 100%);
            border: 1px solid #78350f; padding: 22px; border-radius: 10px; margin-bottom: 20px;
        }
        .dp-title {
            background: linear-gradient(90deg, #ef4444, #f59e0b);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-size: 2.5rem; font-weight: 800; margin: 0;
        }
        .dp-lock-msg {
            background-color: #7f1d1d; color: #fca5a5; padding: 10px;
            border-radius: 6px; border: 1px solid #b91c1c; font-weight: 600; text-align: center; margin-bottom: 20px;
        }
        .dp-kpi-box {
            background-color: #1e293b; border-left: 4px solid #ef4444;
            padding: 18px; border-radius: 6px; margin-bottom: 15px;
        }
        .dp-kpi-label { color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; }
        .dp-kpi-num { color: #f8fafc; font-size: 1.7rem; font-weight: 700; margin-top: 3px; }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data(show_spinner="Cargando datos...")
def parse_file(file_obj):
    """ Lector de archivos csv y hojas de cálculo excel """
    try:
        return pd.read_csv(file_obj) if file_obj.name.endswith('.csv') else pd.read_excel(file_obj)
    except Exception as err:
        st.error(f"No se pudo procesar el archivo: {err}")
        return None


def draw_analytics(df, cat_col, qty_col, val_col):
    """ Realiza los cálculos financieros y renderiza las vistas """
    # Limpieza express de columnas numéricas
    v_series = pd.to_numeric(df[val_col], errors='coerce').fillna(0)
    q_series = pd.to_numeric(df[qty_col], errors='coerce').fillna(0)
    
    if v_series.isna().all() or q_series.isna().all():
        st.warning("⚠️ Elige columnas con valores numéricos para generar los paneles.")
        return

    df[val_col], df[qty_col] = v_series, q_series
    
    # Renderizado de los bloques KPI
    c1, c2, c3 = st.columns(3)
    metrics = [
        ("Total Acumulado", f"$ {df[val_col].sum():,.2f}"),
        ("Volumen Total", f"{int(df[qty_col].sum()):,} Uds."),
        ("Promedio de Ventas", f"$ {df[val_col].mean():,.2f}")
    ]
    
    for col, (label, val) in zip([c1, c2, c3], metrics):
        col.markdown(f"""
        <div class="dp-kpi-box">
            <div class="dp-kpi-label">{label}</div>
            <div class="dp-kpi-num">{val}</div>
        </div>
        """, unsafe_allow_html=True)
            
    st.markdown("### 🏆 Top 5 Distribución General")
    chart_data = df.groupby(cat_col)[qty_col].sum().sort_values(ascending=False).head(5)
    st.bar_chart(chart_data, color="#ef4444")


def main():
    load_ui_styles()
    
    # Encabezado de la Demo
    st.markdown("""
    <div class="dp-hero">
        <h1 class="dp-title">📊 DataPulse Analytics</h1>
        <p style="color: #f59e0b; font-size: 1rem; margin-top: 4px; font-weight: 500;">🔒 MODO EVALUACIÓN - LICENCIA COMERCIAL RESTRINGIDA</p>
    </div>
    <div class="dp-lock-msg">🔒 FUNCIONES DE EXPORTACIÓN DESACTIVADAS. REQUIERE LICENCIA PRO PARA DESBLOQUEAR REPORTES.</div>
    """, unsafe_allow_html=True)

    uploaded_doc = st.file_uploader("📂 Selecciona un archivo Excel (.xlsx) o CSV de prueba", type=["xlsx", "csv"])

    if uploaded_doc:
        dataset = parse_file(uploaded_doc)
        if dataset is not None:
            st.success(f"🎯 Archivo leído: {uploaded_doc.name}")
            headers = list(dataset.columns)
            
            st.markdown("### 🛠️ Configuración de Dimensiones")
            cx1, cx2, cx3 = st.columns(3)
            sel_cat = cx1.selectbox("Categoría / Producto:", headers, index=0)
            sel_qty = cx2.selectbox("Volumen / Cantidad:", headers, index=0)
            sel_val = cx3.selectbox("Valores / Ingresos:", headers, index=0)
            
            st.markdown("### 📈 Panel de Control")
            draw_analytics(dataset, sel_cat, sel_qty, sel_val)
            
            # Restricciones comerciales de la Demo
            st.markdown("--- \n### 📄 Módulo de Exportación")
            st.button("📥 Descargar Reporte Ejecutivo (PDF)", disabled=True, help="Función bloqueada.")
            st.caption("⚠️ Nota: La descarga automática requiere una clave de activación comercial.")
            
            st.markdown("### 📋 Vista Previa de Datos")
            st.dataframe(dataset.head(10), use_container_width=True)
    else:
        st.info("💡 Sube un set de datos para activar los módulos analíticos.")


if __name__ == '__main__':
    main()
