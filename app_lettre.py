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

st.set_page_config(page_title="Générateur Pro CV & Lettres", page_icon="👑", layout="wide")

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
st.markdown("<div style='font-size: 42px; font-weight: 800; color: #1E293B; text-align: center;'>Générateur de Candidature Intelligent 🚀</div>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["📝 Lettre de Motivation", "📄 Créateur de CV Pro", "👑 Boite à Outils Premium"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom & Prénom", key="nom_lettre")
        poste = st.text_input("Poste visé", key="poste_lettre")
        entreprise = st.text_input("Entreprise", key="ent_lettre")
        competences = st.text_area("Vos compétences clés", key="comp_lettre")
        ton = st.selectbox("Style", ["Classique / Formel", "Dynamique / Start-up", "Créatif"], key="ton_lettre")
    with col2:
        if st.button("✨ Générer ma lettre", key="btn_lettre"):
            if not is_premium and st.session_state.generations_count >= 1: afficher_paywall()
            else:
                res = generer_texte_gemini(f"Rédige une lettre pour {nom}, {poste} chez {entreprise}. Compétences: {competences}. Style: {ton}")
                st.text_area("Résultat :", res, height=400)
                if not is_premium: st.session_state.generations_count += 1

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        nom_cv = st.text_input("Nom (CV)", key="nom_cv")
        email_cv = st.text_input("Email", key="email_cv")
        tel_cv = st.text_input("Téléphone", key="tel_cv")
        metier_cv = st.text_input("Titre du CV", key="metier_cv")
        exp_cv = st.text_area("Expériences", key="exp_cv")
    with col2:
        if st.button("🛠️ Générer mon CV", key="btn_cv"):
            if not is_premium and st.session_state.generations_count >= 1: afficher_paywall()
            else:
                res = generer_texte_gemini(f"CV markdown pour {nom_cv}, {metier_cv}. Exp: {exp_cv}")
                st.text_area("Structure CV :", res, height=400)
                if not is_premium: st.session_state.generations_count += 1

with tab3:
    if not is_premium: st.warning("🔒 Espace réservé aux membres Premium.")
    else:
        outil = st.radio("Choisissez un outil :", ["📞 Relance", "👔 Entretien", "💬 LinkedIn"], key="outil_radio")
        if outil == "📞 Relance":
            e_r = st.text_input("Entreprise", key="ent_rel")
            p_r = st.text_input("Poste", key="post_rel")
            if st.button("🚀 Créer le mail", key="btn_rel"): st.text_area("Message :", generer_texte_gemini(f"Mail de relance pour {p_r} chez {e_r}"))
        elif outil == "👔 Entretien":
            p_e = st.text_input("Poste", key="post_ent")
            e_e = st.text_input("Entreprise", key="ent_ent")
            if st.button("🎯 Préparer l'entretien", key="btn_ent"): st.write(generer_texte_gemini(f"Questions pièges pour entretien {p_e} chez {e_e}"))
        elif outil == "💬 LinkedIn":
            p_l = st.text_input("Poste", key="post_link")
            e_l = st.text_input("Entreprise", key="ent_link")
            if st.button("📲 Rédiger le message", key="btn_link"): st.text_area("Message :", generer_texte_gemini(f"Message LinkedIn pour {p_l} chez {e_l}"))
