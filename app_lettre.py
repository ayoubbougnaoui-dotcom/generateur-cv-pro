import streamlit as st
import requests

# ==============================================================================
# CONFIGURATION ET CLÉ API (CORRIGÉE)
# ==============================================================================
PAYPAL_LINK = "https://paypal.me/Ayoub212500/4.99EUR"
CODE_SECRET_PREMIUM = "PREMIUM2026"
GEMINI_API_KEY = "AQ.Ab8RN6LNBwuyb9WeUt56M8bKOmfq0caxHQfbioCTgfzrmitD4A"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY

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

# ==============================================================================
# CONFIGURATION DE LA PAGE
# ==============================================================================
st.set_page_config(page_title="Générateur Pro CV & Lettres", page_icon="👑", layout="wide")

# CSS PERSONNALISÉ (Pour restaurer votre interface complète)
st.markdown("""
<style>
    .main-title { font-size: 42px; font-weight: 800; color: #1E293B; text-align: center; margin-bottom: 5px; }
    .subtitle { font-size: 18px; color: #64748B; text-align: center; margin-bottom: 30px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2563EB; color: white; }
</style>
""", unsafe_allow_html=True)

# GESTION SESSION ET PREMIUM
if "generations_count" not in st.session_state: st.session_state.generations_count = 0
params = st.query_params
is_premium = (params.get("code", "") == CODE_SECRET_PREMIUM)

st.sidebar.title("Espace Premium 👑")
if not is_premium:
    code_saisi = st.sidebar.text_input("Code d'accès :", type="password", key="s_code")
    if code_saisi.strip() == CODE_SECRET_PREMIUM:
        st.query_params["code"] = CODE_SECRET_PREMIUM
        st.rerun()
else:
    st.sidebar.success("👑 ACCÈS PREMIUM ACTIF")

def afficher_paywall():
    st.markdown(f"""
    <div style="background-color:#FEF2F2; padding:20px; border-radius:10px; border:1px solid #F87171; text-align:center;">
        <h3 style="color:#DC2626;">Limite gratuite atteinte !</h3>
        <p>Passez en version illimitée pour continuer.</p>
        <a href="{PAYPAL_LINK}" target="_blank">Débloquer (4,99 €)</a>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# INTERFACE PRINCIPALE
# ==============================================================================
st.markdown("<div class='main-title'>Générateur de Candidature Intelligent 🚀</div>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["📝 Lettre de Motivation", "📄 Créateur de CV Pro", "👑 Boite à Outils Premium"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom Prénom", key="l_nom")
        poste = st.text_input("Poste visé", key="l_poste")
        entreprise = st.text_input("Entreprise", key="l_ent")
        competences = st.text_area("Compétences clés", key="l_comp")
    with col2:
        if st.button("✨ Générer ma lettre", key="btn_l"):
            if not is_premium and st.session_state.generations_count >= 1: afficher_paywall()
            else:
                res = generer_texte_gemini(f"Rédige une lettre pour {nom}, {poste} chez {entreprise}. Compétences: {competences}")
                st.text_area("Résultat :", res, height=400)
                if not is_premium: st.session_state.generations_count += 1

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        nom_cv = st.text_input("Nom (CV)", key="c_nom")
        email_cv = st.text_input("Email", key="c_email")
        metier_cv = st.text_input("Titre du CV", key="c_metier")
        exp_cv = st.text_area("Expériences", key="c_exp")
    with col2:
        if st.button("🛠️ Générer mon CV", key="btn_c"):
            if not is_premium and st.session_state.generations_count >= 1: afficher_paywall()
            else:
                res = generer_texte_gemini(f"Rédige un CV en markdown pour {nom_cv}, {metier_cv}. Expériences: {exp_cv}")
                st.text_area("Structure CV :", res, height=400)
                if not is_premium: st.session_state.generations_count += 1

with tab3:
    if not is_premium: 
        st.warning("🔒 Espace réservé aux membres Premium.")
    else:
        outil = st.radio("Outil Premium :", ["Relance", "Entretien", "LinkedIn"], key="p_radio")
        if outil == "Relance":
            e = st.text_input("Entreprise", key="p_rel")
            if st.button("🚀 Créer le mail", key="b_rel"): st.text_area("Message :", generer_texte_gemini(f"Mail de relance pour {e}"))
        elif outil == "Entretien":
            p = st.text_input("Poste", key="p_ent")
            if st.button("🚀 Préparer", key="b_ent"): st.text_area("Conseils :", generer_texte_gemini(f"Questions entretien pour {p}"))
        elif outil == "LinkedIn":
            p = st.text_input("Poste", key="p_link")
            if st.button("🚀 Rédiger", key="b_link"): st.text_area("Message :", generer_texte_gemini(f"Message LinkedIn pour {p}"))

# (Si vous aviez d'autres sections, ajoutez-les ici en respectant le format tab)
