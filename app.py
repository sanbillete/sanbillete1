import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración Global JDS
st.set_page_config(page_title="JDS | Global Audit", layout="wide", page_icon="⚖️")

# --- BASE DE DATOS DE AFILIADOS (La lista de mando) ---
# Más bien, aquí es donde usted agrega a sus socios o clientes
USERS = {
    "admin": "JDS2026",
    "socio1": "CLAVE01",
    "afiliado_usa": "MIAMI2026"
}

def check_password():
    if "user_authenticated" not in st.session_state:
        st.title("🔐 JDS CONSULTING GROUP | LOGIN")
        user = st.text_input("User / Usuario:")
        password = st.text_input("Password / Contraseña:", type="password")
        
        if st.button("🚀 ENTER / ENTRAR"):
            if user in USERS and USERS[user] == password:
                st.session_state["user_authenticated"] = user
                st.rerun()
            else:
                st.error("❌ Access Denied / Acceso Denegado")
        return False
    return True

if check_password():
    current_user = st.session_state["user_authenticated"]
    
    # Inicializar la bitácora si no existe
    if 'master_log' not in st.session_state:
        st.session_state['master_log'] = []

    st.title(f"⚖️ JDS: Audit Control - User: {current_user.upper()}")
    
    # --- SIDEBAR / BARRA DE CONTROL ---
    st.sidebar.header("🕹️ Command Center")
    presupuesto = st.sidebar.number_input("💰 Personal Budget:", min_value=0.0, value=1000000.0)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎙️ Voice & Photo")
    
    concepto = st.sidebar.text_input("Concept / Concepto:")
    valor = st.sidebar.number_input("Amount / Valor ($):", min_value=0.0)
    foto_recibo = st.sidebar.camera_input("📸 Receipt Photo")

    if st.sidebar.button("✅ RECORD / GRABAR"):
        if concepto and valor > 0:
            ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            registro = {
                "User": current_user, # Marcamos quién hizo el gasto
                "Timestamp": ahora, 
                "Concept": concepto.upper(), 
                "Amount": valor,
                "Photo": "YES ✅" if foto_recibo else "NO ❌"
            }
            st.session_state['master_log'].append(registro)
            st.sidebar.success("Recorded! / ¡Grabado!")
        else:
            st.sidebar.warning("Missing data")

    # --- FILTRO DE PRIVACIDAD (Ingeniería JDS) ---
    # Solo mostramos los gastos del usuario que está logueado
    df_all = pd.DataFrame(st.session_state['master_log'])
    
    if not df_all.empty:
        df_user = df_all[df_all['User'] == current_user]
        total_user = df_user['Amount'].sum()
        saldo_user = presupuesto - total_user

        # Dashboard Visual
        c1, c2, c3 = st.columns(3)
        c1.metric("BUDGET", f"${presupuesto:,.2f}")
        c2.metric("SPENT", f"${total_user:,.2f}", delta=f"-{total_user:,.2f}", delta_color="inverse")
        c3.metric("AVAILABLE", f"${saldo_user:,.2f}")

        st.markdown("---")
        
        col_t, col_g = st.columns([1.2, 0.8])
        with col_t:
            st.subheader("📋 Your Audit Log")
            st.dataframe(df_user, use_container_width=True)
        with col_g:
            st.subheader("📊 Your Analytics")
            chart_data = df_user.groupby("Concept")["Amount"].sum()
            st.bar_chart(chart_data)

    # --- SELLO DE PROTECCIÓN ---
    st.markdown("---")
    st.caption("© 2026 JDS Consulting Group | Global Audit Systems. All rights reserved.")
    st.caption("Cuida la menuda, que la gruesa se cuida sola.")
