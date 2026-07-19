import streamlit as st
import requests

# ==============================================================================
# CONFIGURATION ET LIENS DE PAIEMENT
# ==============================================================================
PAYPAL_LINK = "https://paypal.me/Ayoub212500/4.99EUR"
CODE_SECRET_PREMIUM = "PREMIUM2026"

# Clé API Gemini et URL d'appel direct (v1 stable)
GEMINI_API_KEY = "AQ.Ab8RN6KAJd0t8vxUaN9svqlHC5iYRZoaZt8sdtkcqC_U6kJDzg"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

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
    
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        try:
            return data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return "Erreur dans la structure de la réponse de l'IA."
    else:
        return f"Erreur API ({response.status_code}) : {response.text}"

# Configuration de la page
st.set_page_config(
    page_title="Générateur Pro CV & Lettres",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pour une interface moderne et haut de gamme
st.markdown("""
<style>
    .main-title { font-size: 42px; font-weight: 800; color: #1E293B; text-align: center; margin-bottom: 5px; }
    .subtitle { font-size: 18px; color: #64748B; text-align: center; margin-bottom: 30px; }
    .premium-badge { background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); color: white; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px; display: inline-block; margin-bottom: 10px; }
    .free-badge { background-color: #E2E8F0; color: #475569; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 12px; display: inline-block; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if "generations_count" not in st.session_state:
    st.session_state.generations_count = 0

# DÉTECTION AUTOMATIQUE DU CODE DANS L'URL
params = st.query_params
code_dans_url = params.get("code", "")

is_premium = False
if code_dans_url.strip() == CODE_SECRET_PREMIUM:
    is_premium = True

# BARRE LATÉRALE
st.sidebar.image("https://img.icons8.com/fluent/96/000000/crown.png", width=60)
st.sidebar.title("Espace Premium 👑")

if is_premium:
    st.sidebar.success("👑 ACCÈS PREMIUM ILLIMITÉ ACTIF")
    st.sidebar.write("📊 Utilisation : **Illimitée ♾️**")
else:
    code_saisi = st.sidebar.text_input("Tu as payé ? Entre ton code d'accès :", type="password")
    if code_saisi:
        if code_saisi.strip() == CODE_SECRET_PREMIUM:
            is_premium = True
            st.sidebar.success("👑 ACCÈS PREMIUM ILLIMITÉ ACTIF")
            st.query_params["code"] = CODE_SECRET_PREMIUM
            st.rerun()
        else:
            st.sidebar.error("❌ Code incorrect")

    if not is_premium:
        st.sidebar.info("💡 Mode gratuit actif (Limité à 1 essai global)")
        st.sidebar.write(f"📊 Essai gratuit utilisé : **{st.session_state.generations_count} / 1**")
        st.sidebar.markdown(f"""
        <hr style="margin: 20px 0;">
        <div style="background-color:#FFFBEB; padding:15px; border-radius:10px; border:1px solid #FEF3C7; text-align:center;">
            <span style="font-size:16px; font-weight:bold; color:#B45309;">👑 Devenez Premium</span>
            <p style="font-size:13px; color:#4B5563; margin: 8px 0;">Débloquez l'accès complet en illimité !</p>
            <a href="{PAYPAL_LINK}" target="_blank" style="text-decoration:none;">
                <button style="background-color:#EF4444; color:white; border:none; padding:10px 15px; font-size:14px; font-weight:bold; border-radius:5px; cursor:pointer; width:100%;">Débloquer l'accès (4,99 €)</button>
            </a>
        </div>
        """, unsafe_allow_html=True)

def afficher_paywall():
    st.markdown(f"""
    <div style="background-color:#FEF2F2; padding:30px; border-radius:15px; border:2px solid #F87171; text-align:center; margin-top: 20px;">
        <h2 style="color:#DC2626; margin-top:0;">🛑 Limite de la version gratuite atteinte !</h2>
        <a href="{PAYPAL_LINK}" target="_blank" style="text-decoration:none;">
            <button style="background-color:#DC2626; color:white; border:none; padding:15px 30px; font-size:20px; font-weight:bold; border-radius:8px; cursor:pointer; width: 100%; max-width: 400px;">👉 Débloquer sur PayPal (4,99 €)</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

def peut_generer():
    if is_premium: return True
    if st.session_state.generations_count < 1: return True
    return False

def enregistrer_generation():
    if not is_premium: st.session_state.generations_count += 1

# CORPS PRINCIPAL
st.markdown("<div class='main-title'>Générateur de Candidature Intelligent 🚀</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>L'intelligence artificielle au service de votre réussite professionnelle</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 Lettre de Motivation", "📄 Créateur de CV Pro", "👑 Boite à Outils Premium"])

# ONGLET 1 : LETTRE DE MOTIVATION
with tab1:
    st.subheader("Créez une lettre de motivation percutante")
    col1, col2 = st.columns([1, 1])
    with col1:
        nom_complet = st.text_input("Votre Nom et Prénom", placeholder="Ex: Jean Dupont")
        poste_vise = st.text_input("Poste visé", placeholder="Ex: Conseiller de vente")
        entreprise_cible = st.text_input("Entreprise", placeholder="Ex: Nike")
        competences_cles = st.text_area("Vos compétences clés & points forts", placeholder="Ex: Sens du service client, 2 ans d'expérience...")
        
        ton_lettre = st.selectbox("Style et ton de la lettre", ["Classique / Formel", "Dynamique / Start-up", "Créatif / Audacieux"]) if is_premium else "Classique / Formel"

    with col2:
        if st.button("✨ Générer ma lettre de motivation", use_container_width=True, type="primary"):
            if not nom_complet or not poste_vise or not entreprise_cible:
                st.warning("Veuillez remplir les champs obligatoires.")
            elif not peut_generer():
                afficher_paywall()
            else:
                with st.spinner("Rédaction en cours..."):
                    prompt_lettre = f"Rédige une lettre de motivation pour {nom_complet}, poste de {poste_vise} chez {entreprise_cible}. Forces : {competences_cles}. Style : {ton_lettre}."
                    resultat = generer_texte_gemini(prompt_lettre)
                    st.success("Rédaction terminée ! 🎉")
                    st.text_area("Copiez votre lettre :", resultat, height=450)
                    enregistrer_generation()

# ONGLET 2 : CRÉATEUR DE CV
with tab2:
    st.subheader("Générateur de structure de CV Professionnel")
    col_cv1, col_cv2 = st.columns([1, 1])
    with col_cv1:
        nom_cv = st.text_input("Nom & Prénom (CV)")
        email_cv = st.text_input("Adresse Email")
        tel_cv = st.text_input("Téléphone")
        metier_cv = st.text_input("Titre du CV (Votre métier)")
        experiences_cv = st.text_area("Vos expériences professionnelles")
        etudes_cv = st.text_area("Formations et diplômes")
        competences_cv = st.text_input("Hard & Soft Skills")
        
    with col_cv2:
        if st.button("🛠️ Générer mon CV optimisé", use_container_width=True, type="primary"):
            if not nom_cv or not metier_cv:
                st.warning("Veuillez indiquer au moins votre nom et votre métier.")
            elif not peut_generer():
                afficher_paywall()
            else:
                with st.spinner("Mise en valeur de votre profil..."):
                    prompt_cv = f"Rédige un CV au format Markdown pour {nom_cv}, Métier: {metier_cv}, Email: {email_cv}, Tel: {tel_cv}, Expériences: {experiences_cv}, Études: {etudes_cv}, Compétences: {competences_cv}."
                    resultat = generer_texte_gemini(prompt_cv)
                    st.success("Votre CV est prêt !")
                    st.text_area("Structure du CV :", resultat, height=450)
                    enregistrer_generation()

# ONGLET 3 : OUTILS PREMIUM
with tab3:
    st.subheader("Boîte à outils Premium 👑")
    if not is_premium:
        st.warning("🔒 Cet espace est réservé aux membres Premium.")
    else:
        choix_outil = st.radio("Choisissez un outil Premium :", ["📞 Relance", "👔 Entretien", "💬 LinkedIn"])
        if choix_outil == "📞 Relance":
            rel_ent = st.text_input("Entreprise")
            rel_poste = st.text_input("Poste")
            if st.button("🚀 Créer l'e-mail de relance"):
                res = generer_texte_gemini(f"Rédige un e-mail court de relance pour le poste de {rel_poste} chez {rel_ent}.")
                st.text_area("Message :", res, height=200)
        elif choix_outil == "👔 Entretien":
            prep_poste = st.text_input("Poste")
            prep_ent = st.text_input("Entreprise")
            if st.button("🎯 Préparer mon entretien"):
                res = generer_texte_gemini(f"Donne 3 questions pièges pour un entretien de {prep_poste} chez {prep_ent} avec réponses types.")
                st.write(res)
        elif choix_outil == "💬 LinkedIn":
            link_poste = st.text_input("Poste ciblé")
            link_entreprise = st.text_input("Entreprise")
            if st.button("📲 Rédiger le message LinkedIn"):
                res = generer_texte_gemini(f"Rédige un message court d'approche LinkedIn pour le poste de {link_poste} chez {link_entreprise}.")
                st.text_area("Message :", res, height=200)

st.markdown("<hr><p style='text-align:center; color:#94A3B8; font-size:12px;'>Générateur Pro CV & Lettres de Motivation © 2026.</p>", unsafe_allow_html=True)
