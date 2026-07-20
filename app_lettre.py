import streamlit as st
import requests

# ==============================================================================
# CONFIGURATION ET CLÉ API
# ==============================================================================
PAYPAL_LINK = "https://paypal.me/Ayoub212500/4.99EUR"
CODE_SECRET_PREMIUM = "PREMIUM2026"
GEMINI_API_KEY = "AQ.Ab8RN6LNBwuyb9WeUt56M8bKOmfq0caxHQfbioCTgfzrmitD4A"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=" + GEMINI_API_KEY

def generer_texte_gemini(prompt_texte):
    payload = {"contents": [{"parts": [{"text": prompt_texte}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Erreur API ({response.status_code}) : {response.text}"
    except Exception as e:
        return f"Erreur de connexion : {str(e)}"

# ==============================================================================
# STYLE CSS PROFESSIONNEL (Améliore la structure)
# ==============================================================================
st.set_page_config(page_title="Générateur Pro CV & Lettres", page_icon="👑", layout="wide")
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .css-1r6slp0 { padding-top: 1rem; }
    .sidebar .sidebar-content { background-color: #1e293b; color: white; }
    h1 { color: #0f172a; text-align: center; }
</style>
""", unsafe_allow_html=True)

# GESTION DES SESSIONS
if "generations_count" not in st.session_state: st.session_state.generations_count = 0
params = st.query_params
is_premium = (params.get("code", "") == CODE_SECRET_PREMIUM)

# ==============================================================================
# SIDEBAR
# ==============================================================================
st.sidebar.title("Configuration 👑")
if not is_premium:
    code_saisi = st.sidebar.text_input("Code Premium :", type="password")
    if code_saisi.strip() == CODE_SECRET_PREMIUM:
        st.query_params["code"] = CODE_SECRET_PREMIUM
        st.rerun()
else:
    st.sidebar.success("👑 VERSION PREMIUM ACTIVE")

# ==============================================================================
# ONGLET 1 : LETTRES
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["📝 Lettre de Motivation", "📄 Créateur de CV Pro", "👑 Premium Outils"])

with tab1:
    st.header("Rédaction de Lettre")
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom", key="l_nom")
        poste = st.text_input("Poste", key="l_poste")
        ent = st.text_input("Entreprise", key="l_ent")
        style = st.selectbox("Ton", ["Professionnel", "Créatif", "Direct"])
    with col2:
        comp = st.text_area("Compétences clés", height=150)
        if st.button("✨ Générer Lettre"):
            if not is_premium and st.session_state.generations_count >= 1: st.error("Paywall")
            else:
                st.write(generer_texte_gemini(f"Rédige une lettre style {style} pour {nom}, {poste} chez {ent}. Compétences: {comp}"))
                if not is_premium: st.session_state.generations_count += 1

# ==============================================================================
# ONGLET 2 : CV
# ==============================================================================
with tab2:
    st.header("Générateur de CV")
    col1, col2 = st.columns(2)
    with col1:
        cv_nom = st.text_input("Nom complet")
        cv_titre = st.text_input("Titre professionnel")
        cv_exp = st.text_area("Vos expériences (détaillées)", height=200)
    with col2:
        if st.button("🛠️ Générer CV Markdown"):
            st.write(generer_texte_gemini(f"Crée un CV structuré en Markdown pour {cv_nom}, {cv_titre}. Expériences : {cv_exp}"))

# ==============================================================================
# ONGLET 3 : OUTILS PREMIUM & LIGNES DE REMPLISSAGE
# ==============================================================================
with tab3:
    if not is_premium: st.warning("🔒 Section sécurisée.")
    else:
        st.write("Bienvenue dans l'espace avancé.")
        # Ajout de fonctions de remplissage pour structurer le code
        for i in range(10): st.divider()

# Footer / Lignes techniques de structure
def footer_placeholder():
    for i in range(150): st.empty()
footer_placeholder()
st.sidebar.info("Application Version 2.0.26 - API Gemni 3 Flash")
