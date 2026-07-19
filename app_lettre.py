import streamlit as st
import streamlit.components.v1 as components
import openai

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Générateur de Lettre IA Pro", page_icon="✉️", layout="centered")

# Configuration de la clé API OpenAI (à remplacer par la tienne ou à mettre dans les Secrets Streamlit)
# Idéalement, utilise st.secrets["OPENAI_API_KEY"] sur Streamlit Cloud
OPENAI_API_KEY = "VOTRE_CLE_API_OPENAI_ICI" 
openai.api_key = OPENAI_API_KEY

# CONFIGURATION PAYANTE (STRIPE)
LINK_PAIEMENT_STRIPE = "https://buy.stripe.com/votre_lien_de_paiement_ici"
CODE_SECRET_PREMIUM = "PREMIUM2026"  # Le code secret fourni à tes clients après achat

# Initialisation du compteur de lettres gratuites dans la session
if "lettres_generees" not in st.session_state:
    st.session_state.lettres_generees = 0

# Style CSS Global
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

# --- BARRE LATÉRALE : ZONE PREMIUM ---
st.sidebar.title("💳 Espace Premium")
code_client = st.sidebar.text_input("🔑 Tu as payé ? Entre ton code d'accès :", type="password")

est_premium = (code_client == CODE_SECRET_PREMIUM)

if est_premium:
    st.sidebar.markdown("<span class='premium-badge'>👑 COMPTE PREMIUM ACTIF</span>", unsafe_allow_html=True)
    st.sidebar.success("Accès illimité débloqué ! Merci pour votre confiance.")
else:
    st.sidebar.info(f"⏳ Version d'essai : {1 - st.session_state.lettres_generees}/1 essai gratuit restant.")

st.write("### 📝 Remplis les informations pour l'IA :")

# --- FORMULAIRE DES DONNÉES ---
col1, col2 = st.columns(2)
with col1:
    nom = st.text_input("Ton Prénom & Nom", value="Lucas Martin")
    email = st.text_input("Ton adresse e-mail", value="lucas.martin@example.com")
with col2:
    telephone = st.text_input("Ton numéro de téléphone", value="06 12 34 56 78")
    ville = st.text_input("Ta Ville & Code Postal", value="Lyon 69000")

st.write("---")

# Les deux gros blocs pour nourrir l'IA
poste_vise = st.text_input("🎯 Intitulé du poste visé (ex: Conseiller Bancaire, Développeur Web...)", value="Manager Commercial")
competences_cles = st.text_area("🛠️ Tes principales compétences ou expériences clés (Copie-colle ton CV ici)", 
                                value="- 5 ans d'expérience en vente de services B2B\n- Maîtrise des techniques de négociation et CRM Salesforce\n- Management d'une équipe de 3 personnes\n- Goût du challenge et esprit d'équipe")

offre_emploi = st.text_area("📋 Texte ou description de l'offre d'emploi (Copie-colle l'annonce ici)", 
                             value="Nous recherchons un Manager Commercial H/F dynamique pour développer notre portefeuille de clients. Missions : piloter la stratégie commerciale, encadrer l'équipe de vente, assurer le suivi des KPIs. Profil : Bac+3 minimum, tempérament de chasseur, excellent relationnel.")

# Choix du ton de la lettre
ton = st.selectbox("🎭 Ton de la lettre :", ["Professionnel & Formel 💼", "Dynamique & Enthousiaste 🚀", "Créatif & Audacieux 🎨"])

st.write("---")

# --- VÉRIFICATION DES QUOTAS / PAYWALL ---
bloque_par_paywall = False

if not est_premium and st.session_state.lettres_generees >= 1:
    bloque_par_paywall = True

# --- BOUTON DE GÉNÉRATION ---
if bloque_par_paywall:
    st.markdown(f"""
        <div class="paywall-box">
            <h4 style="color: #991B1B; margin-top:0;">🛑 Limite de l'essai gratuit atteinte !</h4>
            <p>Pour générer des lettres de motivation professionnelles à l'infini et décrocher le job de vos rêves, débloquez l'accès complet.</p>
            <a href="{LINK_PAIEMENT_STRIPE}" target="_blank" style="text-decoration: none;">
                <button style="background-color: #EF4444; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%;">
                    💳 Débloquer l'accès Premium à vie (4.99€)
                </button>
            </a>
            <p style="font-size: 12px; color: #64748B; margin-top: 10px;">Paiement 100% sécurisé via Stripe. Le code d'activation s'affichera juste après le paiement.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    if st.button("🚀 Générer ma Lettre de Motivation Personnalisée"):
        if not poste_vise or not competences_cles or not offre_emploi:
            st.error("❌ Veuillez remplir le poste visé, vos compétences et l'offre d'emploi pour nourrir l'IA.")
        elif OPENAI_API_KEY == "VOTRE_CLE_API_OPENAI_ICI":
            st.error("❌ Configuration requise : Vous devez ajouter une clé API OpenAI valide dans le code pour faire fonctionner l'IA.")
        else:
            with st.spinner("🤖 L'intelligence artificielle analyse l'offre et rédige votre lettre sur-mesure..."):
                try:
                    # Construction du prompt pour ChatGPT
                    prompt_IA = f"""
                    Rédige une lettre de motivation professionnelle, percutante et sans fautes d'orthographe en utilisant les informations suivantes.
                    Expéditeur : {nom}, résidant à {ville}, email: {email}, tel: {telephone}.
                    Poste visé : {poste_vise}.
                    Profil et compétences du candidat : {competences_cles}.
                    Description de l'offre d'emploi : {offre_emploi}.
                    Ton à adopter : {ton}.
                    
                    La lettre doit respecter la structure classique française (Coordonnées, objet clair, accroche percutante sur l'entreprise et le besoin, mise en valeur du profil en lien avec le poste, proposition d'entretien, formule de politesse soignée). N'invente pas de fausses entreprises si non mentionnées, utilise des crochets [Nom de l'entreprise] si nécessaire.
                    """

                    # Appel à l'API OpenAI (Modèle gpt-4o-mini, très rapide et économique)
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Tu es un expert en recrutement et en ressources humaines spécialisé dans la rédaction de candidatures à fort impact."},
                            {"role": "user", "content": prompt_IA}
                        ],
                        temperature=0.7
                    )
                    
                    lettre_redigee = response.choices[0].message.content
                    
                    # Augmenter le compteur seulement si l'utilisateur n'est pas premium
                    if not est_premium:
                        st.session_state.lettres_generees += 1
                    
                    st.success("🎉 Votre lettre a été rédigée avec succès !")
                    
                    # --- CODE VISUEL DE LA LETTRE ---
                    lettre_html_preview = f"""
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <style>
                            body {{ font-family: 'Helvetica Neue', Arial, sans-serif; color: #334155; background-color: white; padding: 15px; }}
                            .letter-container {{ max-width: 700px; margin: 0 auto; background-color: #F8FAFC; padding: 40px; border-radius: 8px; border-left: 6px solid #475569; box-shadow: 0 4px 6px rgba(0,0,0,0.05); white-space: pre-line; font-size: 14px; line-height: 1.6; }}
                        </style>
                    </head>
                    <body>
                        <div class="letter-container">
{lettre_redigee}
                        </div>
                    </body>
                    </html>
                    """
                    
                    st.write("### 👁️ Aperçu de votre lettre :")
                    components.html(lettre_html_preview, height=600, scrolling=True)
                    
                    # Bouton de téléchargement direct
                    st.write("### 💾 Téléchargement :")
                    st.download_button(
                        label="📥 Télécharger au format TEXTE (.txt) prêt à copier",
                        data=lettre_redigee,
                        file_name=f"Lettre_Motivation_{nom.replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"⚠️ Une erreur est survenue lors de la génération avec l'IA : {e}")
