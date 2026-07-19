import streamlit as st
import google.generativeai as genai

# ==============================================================================
# CONFIGURATION ET LIENS DE PAIEMENT
# ==============================================================================
PAYPAL_LINK = "https://paypal.me/Ayoub212500/4.99EUR"
CODE_SECRET_PREMIUM = "PREMIUM2026"

# Configuration de la clé API Gemini en dur
GEMINI_API_KEY = "AQ.Ab8RN6KAJd0t8vxUaN9svqlHC5iYRZoaZt8sdtkcqC_U6kJDzg"
genai.configure(api_key=GEMINI_API_KEY)

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
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1E293B;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 18px;
        color: #64748B;
        text-align: center;
        margin-bottom: 30px;
    }
    .premium-badge {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .free-badge {
        background-color: #E2E8F0;
        color: #475569;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if "generations_count" not in st.session_state:
    st.session_state.generations_count = 0

# ------------------------------------------------------------------------------
# DÉTECTION AUTOMATIQUE DU CODE DANS L'URL (Pour garder le premium permanent)
# ------------------------------------------------------------------------------
params = st.query_params
code_dans_url = params.get("code", "")

is_premium = False
if code_dans_url.strip() == CODE_SECRET_PREMIUM:
    is_premium = True

# ==============================================================================
# BARRE LATÉRALE - ESPACE PREMIUM & PAIEMENT
# ==============================================================================
st.sidebar.image("https://img.icons8.com/fluent/96/000000/crown.png", width=60)
st.sidebar.title("Espace Premium 👑")

if is_premium:
    st.sidebar.success("👑 ACCÈS PREMIUM ILLIMITÉ ACTIF")
    st.sidebar.write("📊 Utilisation : **Illimitée ♾️**")
    st.sidebar.info("🔗 Ce lien est ton accès permanent. Garde-le bien en favori !")
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
            <p style="font-size:13px; color:#4B5563; margin: 8px 0;">
                Débloquez le créateur de CV, le message LinkedIn, la relance automatique, le choix des tons et les questions d'entretien d'embauche en illimité !
            </p>
            <a href="{PAYPAL_LINK}" target="_blank" style="text-decoration:none;">
                <button style="background-color:#EF4444; color:white; border:none; padding:10px 15px; font-size:14px; font-weight:bold; border-radius:5px; cursor:pointer; width:100%; transition: 0.3s;">
                    Débloquer l'accès (4,99 €)
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# COMPOSANT PAYWALL
# ==============================================================================
def afficher_paywall():
    st.markdown(f"""
    <div style="background-color:#FEF2F2; padding:30px; border-radius:15px; border:2px solid #F87171; text-align:center; margin-top: 20px;">
        <h2 style="color:#DC2626; margin-top:0;">🛑 Limite de la version gratuite atteinte !</h2>
        <p style="font-size:18px; color:#374151; font-weight:500;">
            Vous avez utilisé votre essai gratuit. Pour débloquer l'accès complet et générer vos documents en illimité, rejoignez nos membres Premium.
        </p>
        <div style="margin: 25px 0;">
            <a href="{PAYPAL_LINK}" target="_blank" style="text-decoration:none;">
                <button style="background-color:#DC2626; color:white; border:none; padding:15px 30px; font-size:20px; font-weight:bold; border-radius:8px; cursor:pointer; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); width: 100%; max-width: 400px;">
                    👉 Débloquer sur PayPal (4,99 €)
                </button>
            </a>
        </div>
        <p style="font-size:14px; color:#6B7280;">
            🔒 Paiement sécurisé via PayPal. Une fois le paiement effectué, vous recevrez instantanément votre lien d'accès Premium par e-mail.
        </p>
    </div>
    """, unsafe_allow_html=True)

def peut_generer():
    if is_premium:
        return True
    if st.session_state.generations_count < 1:
        return True
    return False

def enregistrer_generation():
    if not is_premium:
        st.session_state.generations_count += 1

# ==============================================================================
# CORPS PRINCIPAL DE L'APPLICATION
# ==============================================================================
st.markdown("<div class='main-title'>Générateur de Candidature Intelligent 🚀</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>L'intelligence artificielle au service de votre réussite professionnelle</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "📝 Lettre de Motivation", 
    "📄 Créateur de CV Pro", 
    "👑 Boite à Outils Premium"
])

# ------------------------------------------------------------------------------
# ONGLET 1 : LETTRE DE MOTIVATION
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Créez une lettre de motivation percutante")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        nom_complet = st.text_input("Votre Nom et Prénom", placeholder="Ex: Jean Dupont")
        poste_vise = st.text_input("Poste visé", placeholder="Ex: Conseiller de vente")
        entreprise_cible = st.text_input("Entreprise", placeholder="Ex: Nike")
        competences_cles = st.text_area(
            "Vos compétences clés & points forts (séparés par des virgules)", 
            placeholder="Ex: Sens du service client, dynamisme, esprit d'équipe, 2 ans d'expérience dans le prêt-à-porter..."
        )
        
        if is_premium:
            st.markdown("<span class='premium-badge'>👑 OPTION PREMIUM ACTIVE</span>", unsafe_allow_html=True)
            ton_lettre = st.selectbox(
                "Style et ton de la lettre",
                ["Classique / Formel (Recommandé pour grandes entreprises)", 
                 "Dynamique / Start-up (Moderne et percutant)", 
                 "Créatif / Audacieux (Pour vous démarquer)"]
            )
        else:
            st.markdown("<span class='free-badge'>🔒 OPTION PREMIUM BLOQUÉE</span>", unsafe_allow_html=True)
            st.selectbox(
                "Style et ton de la lettre (Passez au Premium pour modifier)",
                ["Classique / Formel (Par défaut)"],
                disabled=True
            )
            ton_lettre = "Classique / Formel"

    with col2:
        st.info("💡 Plus vous donnez de détails sur vos forces, plus la lettre rédigée par l'IA sera personnalisée et convaincante !")
        
        if st.button("✨ Générer ma lettre de motivation", use_container_width=True, type="primary"):
            if not nom_complet or not poste_vise or not entreprise_cible:
                st.warning("Veuillez remplir au moins votre nom, le poste visé et l'entreprise.")
            elif not peut_generer():
                afficher_paywall()
            else:
                with st.spinner("Rédaction de votre lettre personnalisée en cours..."):
                    try:
                        style_instruction = ""
                        if "Dynamique" in ton_lettre:
                            style_instruction = "Utilise un style direct, moderne, énergique et très enthousiaste, tout en restant professionnel. Évite les formules de politesse trop lourdes du XIXe siècle."
                        elif "Créatif" in ton_lettre:
                            style_instruction = "Utilise un style original, captivant, audacieux qui montre une vraie personnalité unique. Débute par une accroche percutante."
                        else:
                            style_instruction = "Utilise des tournures de phrases classiques, hautement professionnelles et polies adaptées au monde de l'entreprise traditionnel."

                        prompt_lettre = f"""
                        Tu es un rédacteur professionnel expert en recrutement.
                        Rédige une lettre de motivation convaincante, percutante et sans fautes d'orthographe.
                        
                        Informations du candidat :
                        - Nom complet : {nom_complet}
                        - Poste visé : {poste_vise}
                        - Entreprise visée : {entreprise_cible}
                        - Compétences et forces : {competences_cles}
                        
                        Style demandé : {style_instruction}
                        
                        La structure de la lettre doit être la suivante :
                        1. En-tête (Informations de contact fictives à remplacer, date du jour)
                        2. Objet de la lettre clair
                        3. Accroche captivante (Le 'Moi')
                        4. Pourquoi cette entreprise spécifique et le lien avec le candidat (Le 'Vous')
                        5. Ce que le candidat apporte à l'équipe (Le 'Nous')
                        6. Appel à l'action pour un entretien et formule de politesse soignée.
                        
                        Rends le texte immédiatement exploitable et chaleureux.
                        """
                        
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(prompt_lettre)
                        st.success("Rédaction terminée avec succès ! 🎉")
                        st.text_area("Copiez votre lettre ci-dessous :", response.text, height=450)
                        enregistrer_generation()
                    except Exception as e:
                        st.error(f"Une erreur est survenue : {e}")

# ------------------------------------------------------------------------------
# ONGLET 2 : CRÉATEUR DE CV PROFESSIONNEL
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Générateur de structure de CV Professionnel")
    col_cv1, col_cv2 = st.columns([1, 1])
    
    with col_cv1:
        nom_cv = st.text_input("Nom & Prénom (CV)", placeholder="Ex: Jean Dupont")
        email_cv = st.text_input("Adresse Email", placeholder="Ex: jean.dupont@email.com")
        tel_cv = st.text_input("Téléphone", placeholder="Ex: 06 12 34 56 78")
        metier_cv = st.text_input("Titre du CV (Votre métier)", placeholder="Ex: Commercial Terrain / Vendeur")
        
        experiences_cv = st.text_area(
            "Vos expériences professionnelles (Poste, Entreprise, Dates, Missions)", 
            placeholder="Ex: 2022-2024 : Vendeur chez Zara. Conseil client, encaissement, gestion des stocks."
        )
        etudes_cv = st.text_area(
            "Formations et diplômes (Diplôme, École, Année)", 
            placeholder="Ex: 2021 : Bac Pro Métiers du Commerce et de la Vente"
        )
        competences_cv = st.text_input(
            "Hard & Soft Skills (séparés par des virgules)", 
            placeholder="Ex: Relation client, Négociation, Excel, Ponctualité"
        )
        
    with col_cv2:
        st.info("💡 L'IA va transformer vos notes brutes en un CV ultra-professionnel, réécrire vos missions de manière valorisante et structurer le tout proprement.")
        
        if st.button("🛠️ Générer mon CV optimisé", use_container_width=True, type="primary"):
            if not nom_cv or not metier_cv:
                st.warning("Veuillez indiquer au moins votre nom et votre titre de métier.")
            elif not peut_generer():
                afficher_paywall()
            else:
                with st.spinner("Mise en valeur de votre profil par notre IA..."):
                    try:
                        prompt_cv = f"""
                        Tu es un coach en carrière et un concepteur de CV professionnel.
                        À partir des données brutes suivantes, rédige un CV structuré en Markdown.
                        Réécris les expériences pour les rendre extrêmement valorisantes (utilise des verbes d'action, mets en avant les réalisations).
                        
                        Données reçues :
                        - Nom : {nom_cv}
                        - Titre visé : {metier_cv}
                        - Email : {email_cv}
                        - Téléphone : {tel_cv}
                        - Expériences : {experiences_cv}
                        - Études : {etudes_cv}
                        - Compétences : {competences_cv}
                        
                        Structure attendue pour le résultat :
                        1. En-tête centré avec Nom, Métier et Contacts.
                        2. Un court paragraphe d'accroche (profil professionnel) de 3 lignes maximum accrocheur et adapté au métier.
                        3. Section "Expériences Professionnelles" propre avec puces stylisées.
                        4. Section "Formations" bien alignée.
                        5. Section "Compétences" classée par catégories logiques (ex: Compétences techniques, Qualités personnelles).
                        
                        Fais en sorte que le résultat soit clair, percutant et prêt à être copié-collé dans un traitement de texte.
                        """
                        
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(prompt_cv)
                        st.success("Votre CV est prêt ! Copiez le texte ci-dessous :")
                        st.text_area("Structure et textes optimisés du CV :", response.text, height=450)
                        enregistrer_generation()
                    except Exception as e:
                        st.error(f"Une erreur est survenue lors de la création du CV : {e}")

# ------------------------------------------------------------------------------
# ONGLET 3 : OUTILS PREMIUM EXCLUSIFS
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Boîte à outils Premium 👑")
    
    if not is_premium:
        st.warning("🔒 Cet espace est réservé aux membres Premium. Payez une seule fois pour débloquer toutes ces fonctionnalités d'accélération de carrière.")
        
        st.markdown("""
        ### Découvrez ce qui vous attend dans l'espace Premium :
        - 📞 **Le Relanceur Automatique :** Générez des e-mails de relance professionnels pour suivre vos candidatures.
        - 👔 **Simulateur d'Entretien :** Obtenez les 3 questions les plus piégeuses basées sur le poste choisi et leurs réponses types.
        - 💬 **L'Approche Directe LinkedIn :** Convertissez votre profil en un message d'approche privé de 4 à 5 lignes percutant.
        """)
        
        st.markdown(f"""
        <div style="text-align: center; margin-top:20px;">
            <a href="{PAYPAL_LINK}" target="_blank">
                <button style="background-color:#EF4444; color:white; border:none; padding:15px 30px; font-size:18px; font-weight:bold; border-radius:8px; cursor:pointer;">
                    Débloquer l'accès Premium (4,99 €)
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("<span class='premium-badge'>👑 BIENVENUE DANS VOTRE ESPACE PREMIUM</span>", unsafe_allow_html=True)
        
        choix_outil = st.radio(
            "Choisissez un outil Premium à utiliser :",
            ["📞 Relance de candidature (Suivi)", "👔 Préparation à l'entretien", "💬 Message LinkedIn d'approche directe"]
        )
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        if choix_outil == "📞 Relance de candidature (Suivi)":
            st.markdown("#### Générateur d'e-mail de relance professionnel")
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                rel_ent = st.text_input("Nom de l'entreprise postulée", placeholder="Ex: Décathlon")
                rel_poste = st.text_input("Poste concerné", placeholder="Ex: Responsable Rayon")
                rel_temps = st.selectbox("Depuis combien de temps avez-vous postulé ?", ["1 semaine", "2 semaines", "Plus de 2 semaines"])
                rel_ton = st.selectbox("Style de relance", ["Poli & Classique", "Court & Enthousiaste"])
            
            with col_r2:
                if st.button("🚀 Créer l'e-mail de relance", use_container_width=True, type="primary"):
                    with st.spinner("Génération de la relance..."):
                        prompt_rel = f"Rédige un e-mail de relance court, extrêmement courtois et professionnel pour une candidature au poste de {rel_poste} chez {rel_ent} envoyée il y a {rel_temps}. Le style doit être {rel_ton}. Rappelle subtilement la motivation à rejoindre l'équipe sans paraître impatient."
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(prompt_rel)
                        st.success("Votre relance est prête !")
                        st.text_area("Message de relance :", response.text, height=250)

        elif choix_outil == "👔 Préparation à l'entretien":
            st.markdown("#### Anticipateur de questions d'entretien IA")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                prep_poste = st.text_input("Poste pour l'entretien", placeholder="Ex: Vendeur Conseil")
                prep_ent = st.text_input("Entreprise de l'entretien", placeholder="Ex: Zara")
                prep_desc = st.text_area("Description rapide du job (ou compétences attendues)", placeholder="Ex: Accueil, conseil client, réassort, dynamisme demandé.")
            
            with col_p2:
                if st.button("🎯 Préparer mon entretien", use_container_width=True, type="primary"):
                    with st.spinner("Analyse du poste et simulation..."):
                        prompt_prep = f"Tu es un recruteur professionnel pour l'entreprise {prep_ent}. Le candidat passe un entretien pour le poste de {prep_poste}. Compétences clés : {prep_desc}. Sors les 3 questions les plus piégeuses et pertinentes que tu lui poserais spécifiquement pour ce poste, et pour CHAQUE question, donne l'explication de ce que le recruteur cherche à comprendre ainsi que la meilleure réponse type à formuler."
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(prompt_prep)
                        st.success("Fiches de révision d'entretien prêtes !")
                        st.write(response.text)

        elif choix_outil == "💬 Message LinkedIn d'approche directe":
            st.markdown("#### Générateur de message court pour LinkedIn")
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                link_recruteur = st.text_input("Nom du recruteur (si connu)", placeholder="Ex: Sophie Martin (laissez vide si inconnu)")
                link_poste = st.text_input("Poste ciblé", placeholder="Ex: Développeur Web Junior")
                link_entreprise = st.text_input("Entreprise ciblée", placeholder="Ex: Leroy Merlin")
                link_accroche = st.text_input("Votre atout principal en une phrase", placeholder="Ex: Autodidacte passionné avec 3 projets d'application en ligne.")
                
            with col_l2:
                if st.button("📲 Rédiger le message LinkedIn", use_container_width=True, type="primary"):
                    with st.spinner("Synthèse du message direct..."):
                        nom_rec_text = link_recruteur if link_recruteur else "le recruteur"
                        prompt_link = f"Rédige un message de prise de contact direct ultra-court pour LinkedIn (maximum 300 à 400 caractères, idéal pour un message privé d'invitation) destiné à {nom_rec_text} pour exprimer de l'intérêt pour le poste de {link_poste} chez {link_entreprise}. Inclus l'atout suivant : {link_accroche}. Le ton doit être professionnel, percutant et inciter à une brève réponse."
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(prompt_link)
                        st.success("Message LinkedIn rédigé !")
                        st.text_area("Votre message d'approche :", response.text, height=200)

# Pied de page discret
st.markdown("<hr style='margin-top:50px;'><p style='text-align:center; color:#94A3B8; font-size:12px;'>Générateur Pro CV & Lettres de Motivation © 2026. Tous droits réservés.</p>", unsafe_allow_html=True)
