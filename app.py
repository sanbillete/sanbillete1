import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración SANBILLETE - Nivel Escolta
st.set_page_config(page_title="SANBILLETE | Auditoría Pro", layout="wide", page_icon="💰")

# --- FUNCIÓN DE SEGURIDAD ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 MOTOR SANBILLETE")
        password = st.text_input("Ingrese la Llave de Mando para despegar:", type="password")
        if st.button("🔑 Activar Motor"):
            if password == "admin123": # <--- CAMBIE SU CLAVE AQUÍ
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Llave incorrecta. Acceso denegado.")
        return False
    return True

# --- SOLO SI LA CLAVE ES CORRECTA ARRANCA EL SISTEMA ---
if check_password():
    # Estilo de CSS para tarjetas blancas ejecutivas
    st.markdown("""
        <style>
        .main { background-color: #f5f7f9; }
        .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        </style>
        """, unsafe_allow_html=True)

    st.title("⚖️ SANBILLETE: Control Maestro de Auditoría")
    st.markdown("---")

    if 'gastos_lista' not in st.session_state:
        st.session_state['gastos_lista'] = []

    # --- BARRA LATERAL ---
    st.sidebar.header("🕹️ Centro de Mandos")
    presupuesto_cliente = st.sidebar.number_input("💰 Presupuesto Asignado:", min_value=0.0, value=6000000.0, step=100000.0)

    st.sidebar.markdown("---")
    st.sidebar.subheader("📝 Registro de Gasto")
    concepto = st.sidebar.text_input("Concepto (Ej: Peajes)")
    valor = st.sidebar.number_input("Valor ($)", min_value=0.0, step=100.0)

    if st.sidebar.button("✅ Registrar en Bitácora"):
        if concepto and valor > 0:
            ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            st.session_state['gastos_lista'].append({"Fecha/Hora": ahora, "Concepto": concepto.upper(), "Valor": valor})
            st.sidebar.success("Movimiento Grabado")
        else:
            st.sidebar.warning("Datos incompletos")

    # --- LÓGICA DE DATOS ---
    df_gastos = pd.DataFrame(st.session_state['gastos_lista'])
    total_gastado = df_gastos['Valor'].sum() if not df_gastos.empty else 0.0
    saldo_restante = presupuesto_cliente - total_gastado

    # --- TABLERO EJECUTIVO ---
    c1, c2, c3 = st.columns(3)
    c1.metric("FONDO ASIGNADO", f"${presupuesto_cliente:,.0f}")
    c2.metric("GASTO EJECUTADO", f"${total_gastado:,.0f}", delta=f"-{total_gastado:,.0f}", delta_color="inverse")
    c3.metric("SALDO DISPONIBLE", f"${saldo_restante:,.0f}")

    st.markdown("---")

    if not df_gastos.empty:
        col_tabla, col_grafica = st.columns([1, 1])
        with col_tabla:
            st.subheader("📋 Bitácora Oficial")
            st.dataframe(df_gastos, use_container_width=True)
            csv = df_gastos.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 DESCARGAR AUDITORÍA (CSV)", data=csv, file_name='auditoria_sanbillete.csv', mime='text/csv')
        with col_grafica:
            st.subheader("📊 Análisis de Distribución")
            st.bar_chart(df_gastos.set_index("Concepto")["Valor"])
    else:
        st.info("💡 Sistema blindado. Ingrese el primer reporte de campo.")
    
    if st.sidebar.button("🚪 Cerrar Sesión"):
        del st.session_state["password_correct"]
        st.rerun()
