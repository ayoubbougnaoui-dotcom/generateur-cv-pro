import streamlit as st

# 1. Configuration de la page du site
st.set_page_config(page_title="Générateur de CV Professionnel", page_icon="💼", layout="centered")

st.title("💼 Créateur de CV Professionnel en Ligne")
st.subheader("Génère un CV complet, structuré et prêt à l'emploi !")

st.markdown("---")

st.write("### 📝 Remplis les différentes sections de ton CV :")

# --- SECTION 1 : INFORMATIONS PERSONNELLES ---
with st.expander("👤 1. Informations Personnelles & Contact", expanded=True):
    nom = st.text_input("Nom complet (Prénom & Nom)", placeholder="Ex: Ayoub Bougnaoui")
    titre_pro = st.text_input("Titre du CV / Métier recherché", placeholder="Ex: Développeur Python Fullstack")
    email = st.text_input("Adresse e-mail", placeholder="Ex: ayoub@example.com")
    telephone = st.text_input("Numéro de téléphone", placeholder="Ex: 06 12 34 56 78")
    ville = st.text_input("Ville & Code Postal", placeholder="Ex: Paris 75001")
    linkedin = st.text_input("Lien LinkedIn ou GitHub (Optionnel)", placeholder="Ex: github.com/ayoub")

# --- SECTION 2 : ACCROCHE ---
with st.expander("📝 2. À propos de moi (Accroche)", expanded=False):
    accroche = st.text_area(
        "Présente ton profil en quelques phrases percutantes :",
        placeholder="Ex: Développeur passionné par Python et les technologies web, je recherche une opportunité pour mettre mes compétences en création d'applications au service de projets innovants..."
    )

# --- SECTION 3 : EXPÉRIENCES ---
with st.expander("🏢 3. Expériences Professionnelles", expanded=False):
    st.write("#### Dernière expérience majeure")
    exp1_poste = st.text_input("Intitulé du poste", placeholder="Ex: Développeur Stagiaire")
    exp1_entreprise = st.text_input("Entreprise ou Organisation", placeholder="Ex: Tech Solutions")
    exp1_dates = st.text_input("Période (Dates)", placeholder="Ex: Janvier 2026 - Présent")
    exp1_missions = st.text_area("Missions et réalisations (une par ligne)", placeholder="Ex: - Développement d'une application web avec Streamlit\n- Optimisation de scripts Python\n- Travail en équipe agile")

# --- SECTION 4 : FORMATIONS ---
with st.expander("🎓 4. Formations & Diplômes", expanded=False):
    st.write("#### Dernier diplôme ou formation")
    diplome = st.text_input("Nom du diplôme / Titre de la formation", placeholder="Ex: Développeur Logiciel / Concepteur Python")
    ecole = st.text_input("Établissement / École", placeholder="Ex: OpenClassrooms / Université")
    formation_dates = st.text_input("Période / Année d'obtention", placeholder="Ex: 2025 - 2026")

# --- SECTION 5 : COMPÉTENCES & LANGUES ---
with st.expander("🛠️ 5. Compétences, Langues & Intérêts", expanded=False):
    competences = st.text_input("Compétences techniques (séparées par des virgules)", placeholder="Ex: Python, Streamlit, Git, HTML/CSS, SQL")
    langues = st.text_input("Langues parlées (et niveau)", placeholder="Ex: Français (Langue maternelle), Anglais (Intermédiaire)")
    interets = st.text_input("Centres d'intérêt", placeholder="Ex: Programmation, Nouvelles technologies, Football, Voyage")

st.markdown("---")

# 3. BOUTON DE GÉNÉRATION
if st.button("✨ Générer et Prévisualiser mon CV"):
    if not nom or not titre_pro or not email:
        st.error("❌ Les champs 'Nom complet', 'Titre du CV' et 'Adresse e-mail' sont obligatoires pour générer le document.")
    else:
        st.success("🎉 Votre CV a été généré avec succès !")

        # Construction de la mise en page textuelle du CV complet
        cv_final = f"""========================================================================
{nom.upper()}
{titre_pro.upper()}
========================================================================

📌 CONTACT
------------------------------------------------------------------------
📍 Adresse : {ville if ville else 'Non spécifiée'}
📞 Tél     : {telephone if telephone else 'Non spécifié'}
📧 E-mail  : {email}
🔗 Liens   : {linkedin if linkedin else 'Non spécifié'}

📖 PROFIL
------------------------------------------------------------------------
{accroche if accroche else 'Développeur motivé et rigoureux.'}

💼 EXPÉRIENCES PROFESSIONNELLES
------------------------------------------------------------------------
{exp1_dates} | {exp1_poste} chez {exp1_entreprise}
{exp1_missions if exp1_missions else '- Réalisation de projets informatiques.'}

🎓 FORMATION
------------------------------------------------------------------------
{formation_dates} | {diplome}
🏢 {ecole}

🛠️ COMPÉTENCES TECHNIQUES
------------------------------------------------------------------------
{competences if competences else 'Python, Programmation informatique'}

🗣️ LANGUES
------------------------------------------------------------------------
{langues if langues else 'Français'}

⚽ CENTRES D'INTÉRÊT
------------------------------------------------------------------------
{interets if interets else 'Informatique, Veille technologique'}

========================================================================
Généré automatiquement via l'application CV Python de {nom}
"""

        # Affichage de l'aperçu dynamique sur le site
        st.write("### 👁️ Aperçu de ton CV Complet :")
        st.code(cv_final, language="text")

        # Bouton de téléchargement direct
        st.download_button(
            label="💾 Télécharger mon CV au format (.txt)",
            data=cv_final,
            file_name=f"CV_{nom.replace(' ', '_')}.txt",
            mime="text/plain"
        )
