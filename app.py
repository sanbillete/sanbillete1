import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración SANBILLETE
st.set_page_config(page_title="SANBILLETE - Control Maestro", layout="wide")
st.title("🚀 SANBILLETE: Saneamos su Motor Financiero")

# --- MEMORIA DEL SISTEMA ---
if 'gastos_lista' not in st.session_state:
    st.session_state['gastos_lista'] = []

# --- BARRA LATERAL (CENTRO DE MANDOS) ---
st.sidebar.header("🕹️ Centro de Mandos")
presupuesto_cliente = st.sidebar.number_input("💰 Presupuesto Asignado:", min_value=0.0, value=6000000.0, step=100000.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Registrar Nuevo Gasto")
concepto = st.sidebar.text_input("¿En qué se la gastó?")
valor = st.sidebar.number_input("¿Cuánto costó?", min_value=0.0, step=500.0)

if st.sidebar.button("💸 ¡Registrar Gasto!"):
    if concepto and valor > 0:
        # AQUÍ ESTÁ EL RELOJ AUTOMÁTICO
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state['gastos_lista'].append({"Fecha/Hora": ahora, "Concepto": concepto, "Valor": valor})
        st.sidebar.success(f"¡Registrado con éxito!")
    else:
        st.sidebar.error("Socio, llene los datos.")

# --- CÁLCULOS ---
df_gastos = pd.DataFrame(st.session_state['gastos_lista'])
total_gastado = df_gastos['Valor'].sum() if not df_gastos.empty else 0.0
saldo_restante = presupuesto_cliente - total_gastado

# --- TABLERO PRINCIPAL ---
col1, col2, col3 = st.columns(3)
col1.metric("Presupuesto de Misión", f"${presupuesto_cliente:,.0f}")
col2.metric("Gastos Acumulados", f"${total_gastado:,.0f}", delta=f"-{total_gastado:,.0f}", delta_color="inverse")
col3.metric("Munición Restante", f"${saldo_restante:,.0f}")

st.markdown("---")

if not df_gastos.empty:
    st.subheader("📝 Bitácora de Movimientos (Con Hora Exacta)")
    # Mostramos la tabla con la hora para el jefe
    st.table(df_gastos)
    
    csv = df_gastos.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte para el Jefe (CSV)",
        data=csv,
        file_name='reporte_caja_menor.csv',
        mime='text/csv',
    )
    
    st.bar_chart(df_gastos.set_index("Concepto")["Valor"])
else:
    st.info("Esperando el primer reporte del mensajero...")
