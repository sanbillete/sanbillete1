import streamlit as st
import pandas as pd

# Configuración SANBILLETE
st.set_page_config(page_title="SANBILLETE - Control Maestro", layout="wide")
st.title("🚀 SANBILLETE: Saneamos su Motor Financiero")

# --- MEMORIA DEL SISTEMA ---
if 'gastos_lista' not in st.session_state:
    st.session_state['gastos_lista'] = []
if 'presupuesto_total' not in st.session_state:
    st.session_state['presupuesto_total'] = 10000.0

# --- BARRA LATERAL (ALIMENTACIÓN) ---
st.sidebar.header("🕹️ Centro de Mandos")
st.sidebar.subheader("Registrar Nuevo Gasto")

concepto = st.sidebar.text_input("¿En qué se la gastó? (Ej: Tinto)")
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
saldo_restante = st.session_state['presupuesto_total'] - total_gastado

# --- TABLERO PRINCIPAL ---
col1, col2, col3 = st.columns(3)
col1.metric("Presupuesto Inicial", f"${st.session_state['presupuesto_total']:,}")
col2.metric("Gastos Acumulados", f"${total_gastado:,}", delta=f"-{total_gastado}", delta_color="inverse")
col3.metric("Munición Restante (Saldo)", f"${saldo_restante:,}")

st.markdown("---")

if not df_gastos.empty:
    st.subheader("📝 Bitácora de Movimientos")
    st.table(df_gastos)
    st.bar_chart(df_gastos.set_index("Concepto"))
else:
    st.info("Socio, el motor está limpio. Empiece a registrar sus tintos y parqueaderos a la izquierda.")
