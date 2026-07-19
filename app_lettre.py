import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Générateur de Lettre IA Pro", page_icon="✉️", layout="centered")

# CLÉ API OPENAI CONFIGURÉE
client = OpenAI(api_key="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")

# CONFIGURATION PAYANTE (STRIPE)
LINK_PAIEMENT_STRIPE = "https://buy.stripe.com/votre_lien_de_paiement_ici"
CODE_SECRET_PREMIUM = "PREMIUM2026"

if "lettres_generees" not in st.session_state:
    st.session_state.lettres_generees = 0

st.markdown("""
    <style>
    .main-title { color: #0F172A; font-size: 32px; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .subtitle { color: #64748B; font-size: 18px; text-align: center; margin-bottom: 25px; }
    .paywall-box { background-color: #FEF2F2; border: 2px dashed #EF4444; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }
    .premium-badge { background-color: #F59E0B; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">✨ Générateur de Lettre de Motivation IA</div>', unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Décrochez plus d'entretiens avec une lettre rédigée sur-mesure par l'IA</div>", unsafe_allow_html=True)

st.sidebar.title("💳 Espace Premium")
code_client = st.sidebar.text_input("🔑 Tu as payé ? Entre ton code d'accès :", type="password")
est_premium = (code_client == CODE_SECRET_PREMIUM)

if est_premium:
    st.sidebar.markdown("<span class='premium-badge'>👑 COMPTE PREMIUM ACTIF</span>", unsafe_allow_html=True)
else:
    st.sidebar.info(f"⏳ Version d'essai : {1 - st.session_state.lettres_generees}/1 essai gratuit restant.")

st.write("### 📝 Remplis les informations pour l'IA :")

col1, col2 = st.columns(2)
with col1:
    nom = st.text_input("Ton Prénom & Nom", value="Lucas Martin")
    email = st.text_input("Ton adresse e-mail", value="lucas.martin@example.com")
with col2:
    telephone = st.text_input("Ton numéro de téléphone", value="06 12 34 56 78")
    ville = st.text_input("Ta Ville & Code Postal", value="Lyon 69000")

st.write("---")
poste_vise = st.text_input("🎯 Intitulé du poste visé", value="Manager Commercial")
competences_cles = st.text_area("🛠️ Tes principales compétences (Copie ton CV)", value="- 5 ans d'expérience en vente B2B\n- CRM Salesforce\n- Management d'équipe")
offre_emploi = st.text_area("📋 Description de l'offre d'emploi", value="Nous recherchons un Manager Commercial H/F dynamique. Profil : excellent relationnel, tempérament de chasseur.")
ton = st.selectbox("🎭 Ton de la lettre :", ["Professionnel & Formel 💼", "Dynamique & Enthousiaste 🚀", "Créatif & Audacieux 🎨"])

st.write("---")

bloque_par_paywall = False
if not est_premium and st.session_state.lettres_generees >= 1:
    bloque_par_paywall = True

if bloque_par_paywall:
    st.markdown(f"""
        <div class="paywall-box">
            <h4 style="color: #991B1B; margin-top:0;">🛑 Limite de l'essai gratuit atteinte !</h4>
            <p>Débloquez l'accès complet pour générer des lettres en illimité.</p>
            <a href="{LINK_PAIEMENT_STRIPE}" target="_blank"><button style="background-color: #EF4444; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%;">💳 Débloquer l'accès Premium (4.99€)</button></a>
        </div>
    """, unsafe_allow_html=True)
else:
    if st.button("🚀 Générer ma Lettre de Motivation Personnalisée"):
        if not client:
            st.error("❌ La clé API OpenAI n'est pas configurée.")
        elif not poste_vise or not competences_cles or not offre_emploi:
            st.error("❌ Veuillez remplir tous les champs.")
        else:
            with st.spinner("🤖 Rédaction en cours par l'IA..."):
                try:
                    prompt_IA = f"Rédige une lettre de motivation pour le poste de {poste_vise}. Candidat: {nom}, {ville}. Compétences: {competences_cles}. Offre: {offre_emploi}. Ton: {ton}."
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Tu es un expert en recrutement."},
                            {"role": "user", "content": prompt_IA}
                        ],
                        temperature=0.7
                    )
                    
                    lettre_redigee = response.choices[0].message.content
                    
                    if not est_premium:
                        st.session_state.lettres_generees += 1
                    
                    st.success("🎉 Lettre rédigée !")
                    st.text_area("📋 Copie ta lettre ici :", value=lettre_redigee, height=400)
                    
                except Exception as e:
                    st.error(f"⚠️ Erreur avec l'IA : {e}")
