import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="SANBILLETE - Control Maestro", layout="wide")

# Título Principal
st.title("🚀 SANBILLETE: Saneamos su Motor Financiero")
st.markdown("---")

# Barra lateral para navegación
st.sidebar.header("Menú de Operaciones")
opcion = st.sidebar.selectbox("Seleccione una función", ["Tablero Principal", "Carga de Datos", "Reportes"])

# Contenido Principal
if opcion == "Tablero Principal":
    st.subheader("📊 Estado de la Misión")
    
    # Métricas en columnas
    col1, col2, col3 = st.columns(3)
    col1.metric("Presupuesto", "$10,000", "+5%")
    col2.metric("Gastos Operativos", "$4,500", "-2%")
    col3.metric("Margen de Victoria", "55%", "¡Excelente!")

    st.markdown("---")
    
    # GRÁFICAS VISUALES
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("### 📈 Tendencia de Gastos")
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Nómina', 'Servicios', 'Marketing'])
        st.line_chart(chart_data)
        
    with col_b:
        st.write("### 📊 Distribución de Inversión")
        progreso_data = pd.DataFrame({'Categoría': ['Inversión', 'Reserva', 'Gastos'], 'Valor': [40, 30, 30]})
        st.bar_chart(progreso_data.set_index('Categoría'))

    st.info("El motor SANBILLETE está operando a máxima potencia. ¡Listo para el despegue!")

elif opcion == "Carga de Datos":
    st.subheader("📥 Ingreso de Artillería (Datos)")
    archivo = st.file_uploader("Suba su archivo de Excel o CSV", type=["xlsx", "csv"])
    if archivo:
        st.success("¡Munición cargada con éxito!")

else:
    st.subheader("📑 Reportes del Cuartel")
    st.write("Generando informes estratégicos para la toma de decisiones.")
