import streamlit as st
import pandas as pd

# Configuración del portal
st.set_page_config(page_title="DataPulse | BI", page_icon="🔒", layout="wide")

# Estilos de la interfaz (Estructura de clases limpia)
st.markdown("""
<style>
    .main { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
    .dp-banner {
        background: linear-gradient(135deg, #451a03 0%, #0f172a 100%);
        border: 1px solid #78350f; padding: 25px; border-radius: 12px; margin-bottom: 25px;
    }
    .dp-main-title {
        background: linear-gradient(90deg, #ef4444, #f59e0b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 2.8rem; font-weight: 800; margin: 0;
    }
    .dp-alert-lock {
        background-color: #7f1d1d; color: #fca5a5; padding: 12px;
        border-radius: 8px; border: 1px solid #b91c1c; font-weight: bold; text-align: center; margin-bottom: 20px;
    }
    .dp-card {
        background-color: #1e293b; border-left: 5px solid #ef4444;
        padding: 20px; border-radius: 8px; margin-bottom: 20px;
    }
    .dp-card-meta { color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; }
    .dp-card-val { color: #f8fafc; font-size: 1.8rem; font-weight: 700; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# Sección estática del Header Comercial
st.markdown("""
<div class="dp-banner">
    <h1 class="dp-main-title">📊 DataPulse Analytics</h1>
    <p style="color: #f59e0b; font-size: 1.1rem; margin-top: 5px; font-weight: 500;">🔒 EDICIÓN DEMO - LICENCIA RESTRINGIDA</p>
</div>
<div class="dp-alert-lock">🔒 BOTÓN DE DESCARGA DESACTIVADO. ADQUIERA LA LICENCIA COMPLETA PARA EXPORTAR INFORMES.</div>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="Analizando estructura del archivo...")
def load_dataset(file):
    """Manejador de ingesta de datos para formatos Excel y CSV."""
    try:
        return pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
    except Exception as err:
        st.error(f"Error crítico al leer el archivo: {err}")
        return None


def render_dashboard(df, c_prod, c_cant, c_val):
    """Procesa la analítica del negocio y genera los componentes visuales."""
    # Intentar conversión y contar cuántos datos válidos quedan
    s_val = pd.to_numeric(df[c_val], errors='coerce')
    s_cant = pd.to_numeric(df[c_cant], errors='coerce')
    
    # Validación humana de calidad de datos
    if s_val.isna().all() or s_cant.isna().all():
        st.warning("⚠️ Las columnas seleccionadas no contienen datos numéricos válidos para generar cálculos.")
        return

    df[c_val] = s_val.fillna(0)
    df[c_cant] = s_cant.fillna(0)
    
    # Grid de KPIs principales con formato monetario formal
    col1, col2, col3 = st.columns(3)
    kpis = [
        ("Total Acumulado", f"$ {df[c_val].sum():,.2f}"),
        ("Volumen Total", f"{int(df[c_cant].sum()):,} Uds."),
        ("Promedio General", f"$ {df[c_val].mean():,.2f}")
    ]
    
    for col, (title, value) in zip([col1, col2, col3], kpis):
        with col:
            st.markdown(f"""
            <div class="dp-card">
                <div class="dp-card-meta">{title.upper()}</div>
                <div class="dp-card-val">{value}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("### 🏆 Top 5 Distribución General")
    
    # Preparación de datos limpia para la gráfica
    chart_df = df[[c_prod, c_cant]].dropna()
    chart_df = chart_df.groupby(c_prod).sum()
    top_5 = chart_df.sort_values(by=c_cant, ascending=False).head(5)
    
    st.bar_chart(top_5, y=c_cant, color="#ef4444")


def main():
    """Flujo principal de la aplicación."""
    src_file = st.file_uploader("📂 Cargue un archivo Excel (.xlsx) o CSV de prueba", type=["xlsx", "csv"])

    if src_file:
        data = load_dataset(src_file)
        if data is not None:
            st.success(f"🎯 Mapeo exitoso: {src_file.name}")
            cols = list(data.columns)
            
            st.markdown("### 🛠️ Configuración de Dimensiones")
            cx1, cx2, cx3 = st.columns(3)
            with cx1: sel_prod = st.selectbox("Categoría (Clasificación):", cols, index=0)
            with cx2: sel_cant = st.selectbox("Volumen (Cantidades):", cols, index=0)
            with cx3: sel_val = st.selectbox("Métrica (Valores Financieros):", cols, index=0)
            
            st.markdown("### 📈 Panel de Control")
            render_dashboard(data, sel_prod, sel_cant, sel_val)
            
            # Módulo de bloqueo comercial
            st.markdown("--- \n### 📄 Módulo de Exportación")
            st.button("📥 Descargar Reporte Ejecutivo (PDF)", disabled=True, help="Función restringida.")
            st.caption("⚠️ Nota: La descarga automática requiere una licencia de distribución comercial activa.")
            
            st.markdown("### 📋 Vista Previa de Datos")
            st.dataframe(data.head(10), use_container_width=True)
    else:
        st.info("💡 Interfaz en modo de evaluación. Cargue un set de datos para activar los módulos analíticos.")


if __name__ == '__main__':
    main()
