import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración Global Pro
st.set_page_config(page_title="SANBILLETE | Auditoría Pro", layout="wide", page_icon="💰")

# --- SEGURIDAD ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 ACCESS CONTROL / CONTROL DE ACCESO")
        password = st.text_input("Llave de Mando / Access Key:", type="password")
        if st.button("🔑 ACTIVATE MOTOR / ACTIVAR"):
            if password == "SANBILLETE2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Invalid Key / Llave Incorrecta")
        return False
    return True

if check_password():
    # Estilo de tarjetas blancas ejecutivas
    st.markdown("""
        <style>
        .main { background-color: #f5f7f9; }
        .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 5px solid #004d99; }
        </style>
        """, unsafe_allow_html=True)

    st.title("⚖️ SANBILLETE: Global Audit Control")
    
    if 'gastos_lista' not in st.session_state:
        st.session_state['gastos_lista'] = []

    # --- SIDEBAR / BARRA LATERAL ---
    st.sidebar.header("🕹️ Command Center")
    presupuesto = st.sidebar.number_input("💰 Budget / Presupuesto:", min_value=0.0, value=6000000.0)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎙️ Voice & Photo / Voz y Foto")
    
    # Entradas de Datos
    concepto = st.sidebar.text_input("Concept / Concepto:")
    valor = st.sidebar.number_input("Amount / Valor ($):", min_value=0.0)
    
    # MÁS BIEN AQUÍ ACTIVAMOS EL LENTE:
    foto_recibo = st.sidebar.camera_input("📸 Take Receipt Photo / Foto del Recibo")

    if st.sidebar.button("✅ RECORD / GRABAR TODO"):
        if concepto and valor > 0:
            ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Registramos si tiene foto o no para la auditoría
            registro = {
                "Timestamp": ahora, 
                "Concept": concepto.upper(), 
                "Amount": valor,
                "Photo Evidence": "YES ✅" if foto_recibo else "NO ❌"
            }
            st.session_state['gastos_lista'].append(registro)
            st.sidebar.success("Recorded with Evidence / Grabado con Éxito")
        else:
            st.sidebar.warning("Missing data / Faltan datos")

    # --- TABLERO EJECUTIVO ---
    df = pd.DataFrame(st.session_state['gastos_lista'])
    total = df['Amount'].sum() if not df.empty else 0.0
    saldo = presupuesto - total

    c1, c2, c3 = st.columns(3)
    c1.metric("ASSIGNED BUDGET / PRESUPUESTO", f"${presupuesto:,.2f}")
    c2.metric("TOTAL SPENT / GASTADO", f"${total:,.2f}", delta=f"-{total:,.2f}", delta_color="inverse")
    c3.metric("AVAILABLE / DISPONIBLE", f"${saldo:,.2f}")

    st.markdown("---")

    if not df.empty:
        st.subheader("📋 Audit Log / Bitácora de Auditoría")
        st.dataframe(df, use_container_width=True)
        
        # Más bien entregue el Excel limpio
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DOWNLOAD REPORT / DESCARGAR EXCEL", data=csv, file_name='sanbillete_audit.csv', mime='text/csv')
