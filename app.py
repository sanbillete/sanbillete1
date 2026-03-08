import streamlit as st
import pandas as pd

# Configuración SANBILLETE
st.set_page_config(page_title="SANBILLETE - Control Maestro", layout="wide")
st.title("🚀 SANBILLETE: Saneamos su Motor Financiero")

# --- MEMORIA DEL SISTEMA ---
if 'gastos_lista' not in st.session_state:
    st.session_state['gastos_lista'] = []

# --- BARRA LATERAL (CONTROL DEL CLIENTE) ---
st.sidebar.header("🕹️ Centro de Mandos")

# EL CLIENTE DEFINE SU PODER
presupuesto_cliente = st.sidebar.number_input("💰 Defina su Presupuesto Total:", min_value=0.0, value=6000000.0, step=100000.0)

st.sidebar.markdown("---")
st.sidebar.subheader("Registrar Nuevo Gasto")
concepto = st.sidebar.text_input("¿En qué se la gastó? (Ej: Parqueadero)")
valor = st.sidebar.number_input("¿Cuánto le costó?", min_value=0.0, step=500.0)

if st.sidebar.button("💸 ¡Registrar Gasto!"):
    if concepto and valor > 0:
        st.session_state['gastos_lista'].append({"Concepto": concepto, "Valor": valor})
        st.sidebar.success(f"¡{concepto} registrado!")
    else:
        st.sidebar.error("Socio, ponga el nombre y el valor.")

# --- CÁLCULOS EN VIVO ---
df_gastos = pd.DataFrame(st.session_state['gastos_lista'])
total_gastado = df_gastos['Valor'].sum() if not df_gastos.empty else 0.0
saldo_restante = presupuesto_cliente - total_gastado

# --- TABLERO PRINCIPAL ---
col1, col2, col3 = st.columns(3)
col1.metric("Presupuesto de Misión", f"${presupuesto_cliente:,.0f}")
col2.metric("Gastos Acumulados", f"${total_gastado:,.0f}", delta=f"-{total_gastado:,.0f}", delta_color="inverse")
col3.metric("Munición Restante (Saldo)", f"${saldo_restante:,.0f}")

st.markdown("---")

if not df_gastos.empty:
    st.subheader("📝 Bitácora de Movimientos")
    st.table(df_gastos)
    
    # BOTÓN DE DESCARGA (La Joya de la Corona)
    csv = df_gastos.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte de Gastos (CSV)",
        data=csv,
        file_name='reporte_sanbillete.csv',
        mime='text/csv',
    )
    
    st.bar_chart(df_gastos.set_index("Concepto"))
else:
    st.info("Socio, el motor está limpio. Defina su presupuesto y empiece a registrar gastos a la izquierda.")
