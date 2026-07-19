import streamlit as st
import requests

# ==============================================================================
# CONFIGURATION ET LIENS DE PAIEMENT
# ==============================================================================
PAYPAL_LINK = "https://paypal.me/Ayoub212500/4.99EUR"
CODE_SECRET_PREMIUM = "PREMIUM2026"

# Clé API Gemini
GEMINI_API_KEY = "AQ.Ab8RN6KAJd0t8vxUaN9svqlHC5iYRZoaZt8sdtkcqC_U6kJDzg"

# URL avec -latest pour assurer la compatibilité du modèle
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

# Fonction d'appel direct à l'API via requêtes HTTP
def generer_texte_gemini(prompt_texte):
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_texte}
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Erreur API ({response.status_code}) : {response.text}"
    except Exception as e:
        return f"Erreur de connexion : {str(e)}"

# Configuration de la page
st.set_page_config(
    page_title="Générateur Pro CV & Lettres",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title { font-size: 42px; font-weight: 800; color: #1E293B; text-align: center; margin-bottom: 5px; }
    .subtitle { font-size: 18px; color: #64748B; text-align: center; margin-bottom: 30px; }
</style>
""", unsafe_allow_html=True)

if "generations_count" not in st.session_state:
    st.session_state.generations_count = 0

params = st.query_params
code_dans_url = params.get("code", "")
is_premium = (code_dans_url.strip() == CODE_SECRET_PREMIUM)

# BARRE LATÉRALE
st.sidebar.title("Espace Premium 👑")
if is_premium:
    st.sidebar.success("👑 ACCÈS PREMIUM ACTIF")
else:
    code_saisi = st.sidebar.text_input("Code d'accès :", type="password")
    if code_saisi.strip() == CODE_SECRET_PREMIUM:
        st.query_params["code"] = CODE_SECRET_PREMIUM
        st.rerun()

def afficher_paywall():
    st.markdown(f"""
    <div style="background-color:#FEF2F2; padding:20px; border-radius:10px; border:1px solid #F87171; text-align:center;">
        <h3 style="color:#DC2626;">Limite atteinte !</h3>
        <a href="{PAYPAL_LINK}" target="_blank">Débloquer en illimité (4,99 €)</a>
    </div>
    """, unsafe_allow_html=True)

# CORPS PRINCIPAL
st.markdown("<div class='main-title'>Générateur de Candidature 🚀</div>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["📝 Lettre de Motivation", "📄 Créateur de CV Pro", "👑 Premium"])

with tab1:
    nom = st.text_input("Nom Prénom")
    poste = st.text_input("Poste visé")
    entreprise = st.text_input("Entreprise")
    if st.button("Générer la lettre"):
        if not is_premium and st.session_state.generations_count >= 1:
            afficher_paywall()
        else:
            res = generer_texte_gemini(f"Rédige une lettre de motivation pour {nom}, {poste} chez {entreprise}.")
            st.text_area("Résultat :", res, height=400)
            if not is_premium: st.session_state.generations_count += 1

with tab2:
    st.write("Remplissez les infos pour le CV.")
    # Ajoutez ici les champs CV si nécessaire

with tab3:
    st.write("Outils avancés pour abonnés.")
