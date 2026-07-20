import streamlit as st
import requests

# ==============================================================================
# CONFIGURATION ET LIENS DE PAIEMENT
# ==============================================================================
PAYPAL_LINK = "https://paypal.me/Ayoub212500/4.99EUR"
CODE_SECRET_PREMIUM = "PREMIUM2026"
GEMINI_API_KEY = "AQ.Ab8RN6KAJd0t8vxUaN9svqlHC5iYRZoaZt8sdtkcqC_U6kJDzg"

# Fonction robuste avec basculement automatique de modèle pour éviter le 503/404
def generer_texte_gemini(prompt_texte):
    modeles = ["gemini-3-flash-preview", "gemini-1.5-flash"]
    payload = {"contents": [{"parts": [{"text": prompt_texte}]}]}
    headers = {"Content-Type": "application/json"}
    
    for modele in modeles:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modele}:generateContent?key={GEMINI_API_KEY}"
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                data = response.json()
                return data['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            continue
    return "Erreur : Les serveurs sont surchargés. Veuillez réessayer."

# Configuration de la page
st.set_page_config(page_title="Générateur Pro CV & Lettres", page_icon="👑", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .main-title { font-size: 42px; font-weight: 800; color: #1E293B; text-align: center; margin-bottom: 5px; }
    .subtitle { font-size: 18px; color: #64748B; text-align: center; margin-bottom: 30px; }
</style>
""", unsafe_allow_html=True)

# Initialisation
if "generations_count" not in st.session_state: st.session_state.generations_count = 0
params = st.query_params
is_premium = (params.get("code", "") == CODE_SECRET_PREMIUM)

# BARRE LATÉRALE
st.sidebar.title("Espace Premium 👑")
if is_premium:
    st.sidebar.success("👑 ACCÈS PREMIUM ILLIMITÉ ACTIF")
else:
    code_saisi = st.sidebar.text_input("Code d'accès :", type="password")
    if code_saisi and code_saisi.strip() == CODE_SECRET_PREMIUM:
        st.query_params["code"] = CODE_SECRET_PREMIUM
        st.rerun()

def afficher_paywall():
    st.markdown(f"""<div style="background:#FEF2F2; padding:30px; border-radius:15px; border:2px solid #F87171; text-align:center;">
    <h2>🛑 Limite gratuite atteinte !</h2>
    <a href="{PAYPAL_LINK}" target="_blank"><button style="background:#DC2626; color:white; padding:15px; border-radius:8px; border:none; width:100%;">Débloquer (4,99 €)</button></a></div>""", unsafe_allow_html=True)

# CORPS PRINCIPAL
st.markdown("<div class='main-title'>Générateur de Candidature Intelligent 🚀</div>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["📝 Lettre de Motivation", "📄 Créateur de CV Pro", "👑 Boite à Outils Premium"])

with tab1:
    col1, col2 = st.columns(2)
    nom_l = col1.text_input("Nom", key="l_n")
    poste_l = col1.text_input("Poste", key="l_p")
    ent_l = col1.text_input("Entreprise", key="l_e")
    if col1.button("✨ Générer Lettre", type="primary"):
        if st.session_state.generations_count >= 1 and not is_premium: afficher_paywall()
        else:
            res = generer_texte_gemini(f"Lettre pour {nom_l}, {poste_l} chez {ent_l}")
            col2.text_area("Résultat :", res, height=450)
            if not is_premium: st.session_state.generations_count += 1

with tab2:
    col1, col2 = st.columns(2)
    nom_c = col1.text_input("Nom", key="c_n")
    exp_c = col1.text_area("Expériences", key="c_e")
    if col1.button("🛠️ Générer CV", type="primary"):
        if st.session_state.generations_count >= 1 and not is_premium: afficher_paywall()
        else:
            res = generer_texte_gemini(f"CV pour {nom_c}, exp: {exp_c}")
            col2.text_area("Résultat :", res, height=450)
            if not is_premium: st.session_state.generations_count += 1

with tab3:
    if not is_premium: st.warning("🔒 Section réservée.")
    else: st.write("Outils Premium Activés.")

# --- ESPACE DE REMPLISSAGE POUR STRUCTURE LONGUE ---
for i in range(150): st.sidebar.write("")
st.sidebar.info("Application V2026 - Stable")
