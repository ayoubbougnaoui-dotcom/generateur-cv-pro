import streamlit as st
import requests

# ==============================================================================
# CONFIGURATION ET LIENS DE PAIEMENT
# ==============================================================================
PAYPAL_LINK = "https://paypal.me/Ayoub212500/4.99EUR"
CODE_SECRET_PREMIUM = "PREMIUM2026"
GEMINI_API_KEY = "AQ.Ab8RN6KAJd0t8vxUaN9svqlHC5iYRZoaZt8sdtkcqC_U6kJDzg"

# URL mis à jour pour le modèle 2.0-flash disponible en 2026
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def generer_texte_gemini(prompt_texte):
    payload = {"contents": [{"parts": [{"text": prompt_texte}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Erreur API ({response.status_code}) : {response.text}"
    except Exception as e:
        return f"Erreur de connexion : {str(e)}"

# Configuration de la page
st.set_page_config(page_title="Générateur Pro CV & Lettres", page_icon="👑", layout="wide")

# Initialisation session
if "generations_count" not in st.session_state: st.session_state.generations_count = 0
params = st.query_params
is_premium = (params.get("code", "") == CODE_SECRET_PREMIUM)

# BARRE LATÉRALE
st.sidebar.title("Espace Premium 👑")
if is_premium:
    st.sidebar.success("👑 ACCÈS PREMIUM ACTIF")
else:
    code_saisi = st.sidebar.text_input("Code d'accès :", type="password", key="sidebar_code")
    if code_saisi.strip() == CODE_SECRET_PREMIUM:
        st.query_params["code"] = CODE_SECRET_PREMIUM
        st.rerun()

def afficher_paywall():
    st.markdown(f"""
    <div style="background-color:#FEF2F2; padding:20px; border-radius:10px; border:1px solid #F87171; text-align:center;">
        <h3>Limite gratuite atteinte !</h3>
        <a href="{PAYPAL_LINK}" target="_blank">Débloquer en illimité (4,99 €)</a>
    </div>
    """, unsafe_allow_html=True)

# CORPS PRINCIPAL
st.title("Générateur de Candidature Intelligent 🚀")
tab1, tab2, tab3 = st.tabs(["📝 Lettre de Motivation", "📄 Créateur de CV Pro", "👑 Boite à Outils Premium"])

# --- ONGLET 1 ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom Prénom", key="l_nom")
        poste = st.text_input("Poste visé", key="l_poste")
        entreprise = st.text_input("Entreprise", key="l_ent")
        competences = st.text_area("Compétences clés", key="l_comp")
    with col2:
        if st.button("Générer la lettre", key="l_btn"):
            if not is_premium and st.session_state.generations_count >= 1:
                afficher_paywall()
            else:
                res = generer_texte_gemini(f"Rédige une lettre pour {nom}, {poste} chez {entreprise}. Forces: {competences}")
                st.text_area("Résultat :", res, height=400)
                if not is_premium: st.session_state.generations_count += 1

# --- ONGLET 2 ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        nom_cv = st.text_input("Nom (CV)", key="c_nom")
        metier_cv = st.text_input("Titre du CV", key="c_poste")
        exp_cv = st.text_area("Expériences", key="c_exp")
    with col2:
        if st.button("Générer mon CV", key="c_btn"):
            if not is_premium and st.session_state.generations_count >= 1:
                afficher_paywall()
            else:
                res = generer_texte_gemini(f"Rédige un CV en Markdown pour {nom_cv}, {metier_cv}. Exp: {exp_cv}")
                st.text_area("Structure CV :", res, height=400)
                if not is_premium: st.session_state.generations_count += 1

# --- ONGLET 3 ---
with tab3:
    if not is_premium:
        st.warning("🔒 Espace réservé aux membres Premium.")
    else:
        outil = st.radio("Outil Premium :", ["Relance", "Entretien", "LinkedIn"], key="p_radio")
        if outil == "Relance":
            e = st.text_input("Entreprise", key="p_rel_ent")
            if st.button("Générer", key="p_rel_btn"): st.write(generer_texte_gemini(f"Mail de relance pour {e}"))
        elif outil == "Entretien":
            p = st.text_input("Poste", key="p_ent_post")
            if st.button("Générer", key="p_ent_btn"): st.write(generer_texte_gemini(f"Entretien pour {p}"))
        elif outil == "LinkedIn":
            p = st.text_input("Poste", key="p_link_post")
            if st.button("Générer", key="p_link_btn"): st.write(generer_texte_gemini(f"Message LinkedIn pour {p}"))
