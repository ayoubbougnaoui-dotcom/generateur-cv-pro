import streamlit as st
import requests

# ==============================================================================
# CONFIGURATION
# ==============================================================================
PAYPAL_LINK = "https://paypal.me/Ayoub212500/4.99EUR"
CODE_SECRET_PREMIUM = "PREMIUM2026"
GEMINI_API_KEY = "AQ.Ab8RN6KAJd0t8vxUaN9svqlHC5iYRZoaZt8sdtkcqC_U6kJDzg"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

def generer_texte_gemini(prompt_texte):
    payload = {"contents": [{"parts": [{"text": prompt_texte}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Erreur API ({response.status_code}) : {response.text}"
    except Exception as e:
        return f"Erreur : {str(e)}"

# Configuration page
st.set_page_config(page_title="Générateur Pro CV & Lettres", page_icon="👑", layout="wide")

# CSS complet
st.markdown("""
<style>
    .main-title { font-size: 42px; font-weight: 800; color: #1E293B; text-align: center; margin-bottom: 5px; }
    .subtitle { font-size: 18px; color: #64748B; text-align: center; margin-bottom: 30px; }
</style>
""", unsafe_allow_html=True)

# Session et Premium
if "generations_count" not in st.session_state: st.session_state.generations_count = 0
params = st.query_params
is_premium = (params.get("code", "") == CODE_SECRET_PREMIUM)

st.sidebar.title("Espace Premium 👑")
if not is_premium:
    code_saisi = st.sidebar.text_input("Code d'accès :", type="password")
    if code_saisi == CODE_SECRET_PREMIUM:
        st.query_params["code"] = CODE_SECRET_PREMIUM
        st.rerun()
else:
    st.sidebar.success("👑 ACCÈS PREMIUM ACTIF")

def afficher_paywall():
    st.markdown(f"""<div style="background:#FEF2F2; padding:20px; border:2px solid #F87171; text-align:center;">
    <h3>Limite gratuite atteinte !</h3>
    <a href="{PAYPAL_LINK}" target="_blank">Débloquer en illimité (4,99 €)</a></div>""", unsafe_allow_html=True)

# Interface
st.markdown("<div class='main-title'>Générateur de Candidature Intelligent 🚀</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>L'intelligence artificielle au service de votre réussite professionnelle</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Lettre de Motivation", "📄 Créateur de CV Pro", "👑 Boite à Outils Premium"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom & Prénom")
        poste = st.text_input("Poste visé")
        entreprise = st.text_input("Entreprise")
        competences = st.text_area("Vos compétences clés")
        ton = st.selectbox("Style", ["Classique / Formel", "Dynamique / Start-up", "Créatif"]) if is_premium else "Classique / Formel"
    with col2:
        if st.button("✨ Générer ma lettre"):
            if not is_premium and st.session_state.generations_count >= 1: afficher_paywall()
            else:
                res = generer_texte_gemini(f"Rédige une lettre pour {nom}, {poste} chez {entreprise}. Compétences: {competences}. Style: {ton}")
                st.text_area("Résultat :", res, height=400)
                if not is_premium: st.session_state.generations_count += 1

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        nom_cv = st.text_input("Nom (CV)")
        email_cv = st.text_input("Email")
        tel_cv = st.text_input("Téléphone")
        metier_cv = st.text_input("Titre du CV")
        exp_cv = st.text_area("Expériences")
        etudes_cv = st.text_area("Formations")
        skills_cv = st.text_input("Skills")
    with col2:
        if st.button("🛠️ Générer mon CV"):
            if not is_premium and st.session_state.generations_count >= 1: afficher_paywall()
            else:
                res = generer_texte_gemini(f"CV markdown pour {nom_cv}, {metier_cv}. Exp: {exp_cv}, Etudes: {etudes_cv}, Skills: {skills_cv}")
                st.text_area("Structure CV :", res, height=400)
                if not is_premium: st.session_state.generations_count += 1

with tab3:
    if not is_premium: st.warning("🔒 Espace réservé aux membres Premium.")
    else:
        outil = st.radio("Choisissez un outil :", ["📞 Relance", "👔 Entretien", "💬 LinkedIn"])
        if outil == "📞 Relance":
            e = st.text_input("Entreprise")
            p = st.text_input("Poste")
            if st.button("🚀 Créer le mail"): st.text_area("Message :", generer_texte_gemini(f"Mail de relance pour {p} chez {e}"))
        elif outil == "👔 Entretien":
            p = st.text_input("Poste")
            e = st.text_input("Entreprise")
            if st.button("🎯 Préparer l'entretien"): st.write(generer_texte_gemini(f"Questions pièges pour entretien {p} chez {e}"))
        elif outil == "💬 LinkedIn":
            p = st.text_input("Poste")
            e = st.text_input("Entreprise")
            if st.button("📲 Rédiger le message"): st.text_area("Message :", generer_texte_gemini(f"Message LinkedIn pour {p} chez {e}"))
