import streamlit as st
import requests

# ==============================================================================
# CONFIGURATION
# ==============================================================================
PAYPAL_LINK = "https://paypal.me/Ayoub212500/4.99EUR"
CODE_SECRET_PREMIUM = "PREMIUM2026"
GEMINI_API_KEY = "AQ.Ab8RN6LNBwuyb9WeUt56M8bKOmfq0caxHQfbioCTgfzrmitD4A"

# Utilisation du modèle 1.5-flash avec la syntaxe standard v1beta
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

def generer_texte_gemini(prompt_texte):
    payload = {"contents": [{"parts": [{"text": prompt_texte}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        # Appel API direct
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Erreur API ({response.status_code}) : {response.text}"
    except Exception as e:
        return f"Erreur : {str(e)}"

# Interface Streamlit
st.set_page_config(page_title="Générateur Pro", layout="wide")
st.title("Générateur de Candidature 🚀")

tab1, tab2, tab3 = st.tabs(["Lettre", "CV", "Premium"])

with tab1:
    nom = st.text_input("Nom", key="l_nom")
    poste = st.text_input("Poste", key="l_poste")
    if st.button("Générer lettre", key="l_btn"):
        st.write(generer_texte_gemini(f"Rédige une lettre pour {nom} visant le poste de {poste}"))

with tab2:
    nom_cv = st.text_input("Nom", key="c_nom")
    if st.button("Générer CV", key="c_btn"):
        st.write(generer_texte_gemini(f"Rédige un CV pour {nom_cv}"))

with tab3:
    st.write("Espace Premium")
