import streamlit as st
import pandas as pd
import base64
import unicodedata
import re
st.set_page_config(
    page_title="Smart KPI Assistant",
    page_icon="📊",
    layout="wide"
)

with open("assets/logo-totalenergie.png", "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode()

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, rgba(239,68,68,0.12), transparent 35%),
        radial-gradient(circle at top right, rgba(250,204,21,0.18), transparent 30%),
        linear-gradient(135deg, #fff7ed 0%, #fff1f2 40%, #f8fafc 100%);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #b91c1c 0%, #f97316 60%, #facc15 100%);
}

section[data-testid="stSidebar"] * {
    color: white !important;
    font-weight: 600;
}
section[data-testid="stSidebar"]::before {
    
    display: block;
    margin: 28px 22px 44px 22px;
    padding: 24px 18px;
    text-align: center;
    border-radius: 30px;
    color: white;
    font-weight: 900;
    font-size: 20px;
    letter-spacing: 0.5px;
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.30),
        rgba(255,255,255,0.12)
    );
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.35);
    box-shadow: 0 20px 60px rgba(255,255,255,0.25);
    animation: navGlow 3s ease-in-out infinite;
}
@keyframes navGlow {
    0% {
        transform: translateY(0px);
        box-shadow: 0 16px 35px rgba(255,255,255,0.10);
    }
    50% {
        transform: translateY(-6px);
        box-shadow: 0 24px 55px rgba(255,255,255,0.38);
    }
    100% {
        transform: translateY(0px);
        box-shadow: 0 16px 35px rgba(255,255,255,0.10);
    }
}
            
section[data-testid="stSidebar"] a {
    border-radius: 14px;
    margin: 6px 10px;
    transition: all 0.25s ease;
}

section[data-testid="stSidebar"] a:hover {
    background: rgba(255,255,255,0.22) !important;
    transform: translateX(8px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.18);
}
.hero {
    padding: 34px;
    border-radius: 28px;
    background: linear-gradient(
        135deg,
        rgba(185,28,28,0.65) 0%,
        rgba(239,68,68,0.55) 30%,
        rgba(249,115,22,0.50) 70%,
        rgba(250,204,21,0.45) 100%
    );
    color: white;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.35);
    box-shadow: 0 25px 65px rgba(185, 28, 28, 0.20);
    margin-bottom: 30px;
}

.hero-title {
    display: flex;
    align-items: center;
    gap: 18px;
}

.hero-logo-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.hero-logo-wrapper::before {
    content: "";
    position: absolute;
    width: 170px;
    height: 170px;
    background: radial-gradient(
        circle,
        rgba(255,255,255,1) 0%,
        rgba(255,255,255,0.65) 35%,
        rgba(255,255,255,0.25) 60%,
        transparent 82%
    );
    filter: blur(22px);
    border-radius: 50%;
    z-index: 1;
    animation: glowPulse 3s ease-in-out infinite;
}

.hero-logo {
    height: 95px;
    width: auto;
    position: relative;
    z-index: 2;
    background: transparent;
    filter: drop-shadow(0px 10px 20px rgba(0,0,0,0.25));
    animation: floatLogo 3s ease-in-out infinite;
}

@keyframes glowPulse {
    0% { transform: scale(1); opacity: 0.85; }
    50% { transform: scale(1.25); opacity: 1; }
    100% { transform: scale(1); opacity: 0.85; }
}

.hero h2 {
    font-size: 36px;
    font-weight: 900;
    margin: 0;

    /* 🔥 Dégradé inspiré TotalEnergies (plus foncé pour lisibilité) */
    background: linear-gradient(
        90deg,
        #7f1d1d 0%,   /* rouge foncé */
        #b91c1c 25%,  /* rouge */
        #ea580c 50%,  /* orange */
        #f97316 75%,  /* orange clair */
        #eab308 100%  /* jaune */
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    /*  petit effet glow pour lisibilité */
    text-shadow: 0px 2px 10px rgba(0,0,0,0.15);
}

.hero p {
    font-size: 17px;
    margin-top: 18px;
}

@keyframes floatLogo {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

.feature-card {
    background: rgba(255,255,255,0.48);
    backdrop-filter: blur(16px);
    padding: 24px;
    border-radius: 28px;

    /* 🔥 ALIGNEMENT PARFAIT */
    min-height: 310px;
    height: 310px;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 18px 45px rgba(127, 29, 29, 0.13);
    transition: all 0.35s ease;
}
.feature-card h3 {
    min-height: 60px;
}

.feature-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 28px 70px rgba(127, 29, 29, 0.24);
    background: rgba(255,255,255,0.62);
}

.feature-icon {
    font-size: 38px;
    margin-bottom: 10px;
}

.feature-card h3 {
    color: #7f1d1d;
    font-weight: 900;
    font-size: 22px;
}

.feature-card p {
    color: #475569;
    font-size: 15px;
    line-height: 1.55;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 14px 35px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.5);
}

div[data-testid="stFileUploader"] {
    border-radius: 22px;
    border: 2px dashed #f97316;
    padding: 20px;
    background: rgba(255,255,255,0.42);
    backdrop-filter: blur(14px);
}

div[data-testid="stDataFrame"] {
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

div[data-testid="stAlert"] {
    border-radius: 18px;
}
            
/* FOOTER SIDEBAR */

/* 🔥 BADGE TEXTE SIMPLE */
/* 🔥 FOOTER STYLE ONCF */
/* 🔥 FOOTER STYLE SIMPLE (PAS GRAS) */
section[data-testid="stSidebar"]::after {
    content: "© 2026 Smart KPI Assistant — Tous droits réservés";

    position: absolute;
    bottom: 18px;
    left: 10px;
    right: 10px;

    text-align: center;

    font-size: 12px;
    font-weight: 400; 

    color: #111827; /* noir élégant */

    letter-spacing: 0.3px;

    background: none;
    border: none;
    box-shadow: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero">
    <div class="hero-title">
        <div class="hero-logo-wrapper">
            <img src="data:image/png;base64,{encoded_logo}" class="hero-logo" />
        </div>
        <h2>Smart KPI Assistant — TotalEnergies</h2>
    </div>
    <p>
        Analyse intelligente des KPI issus de Looker dans le cadre de la migration
        du use case TotalEnergies vers une architecture Data Lakehouse (GCP).
    </p>
</div>
""", unsafe_allow_html=True)

col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <h3>Analyse KPI</h3>
        <p>
            Visualiser les indicateurs clés issus des exports Looker
            et analyser les performances par dimension métier.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🚨</div>
        <h3>Détection d’anomalies</h3>
        <p>
            Identifier automatiquement les valeurs atypiques dans les KPI
            afin de faciliter la recette et la validation des données.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h3>Assistant intelligent</h3>
        <p>
            Interroger les données chargées et obtenir rapidement
            des réponses simples sur les KPI, les agents et les campagnes.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_d:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📋</div>
        <h3>Data Quality</h3>
        <p>
            Contrôler la qualité des données, identifier les valeurs nulles
            et vérifier les colonnes disponibles dans les exports Looker.
        </p>
    </div>
    """, unsafe_allow_html=True)

MEASURES_BY_FACT = {
    "fact_ventes": [
        "ventes_realisees"
    ],

    "fact_telephonie_appel": [
        "total_recu_projet_ae",
        "appels_clotures",
        "appels_debordes",
        "appels_ignores",
        "appels_svi",
        "appels_abandonnes",
        "appels_traites",
        "duree_de_communication",
        "duree_totale_attente",
        "dmc",
        "duree_moyenne_attente",
        "duree_moyenne_abandon",
        "call_conversation_duration",
        "qs_ae"
    ],

    "fact_telephonie_action": [
        "temps_de_pause",
        "temps_de_pause_break",
        "temps_de_pause_formation",
        "temps_entretien_rh",
        "temps_de_pause_dej",
        "temps_de_pause_bug",
        "temps_de_pause_saisie",
        "temps_de_pause_brief",
        "duree_de_traitement_hors_post_travail",
        "duree_de_presence",
        "duree_totale_des_pauses",
        "duree_de_disponibilite",
        "duree_de_post_travail",
        "duree_appels_sortants",
        "duree_appels_entrants",
        "duree_callback",
        "duree_numerotation",
        "duree_saisie_de_numero",
        "duree_appel_manuel",
        "duree_lecture_du_message",
        "duree_mode_recherche",
        "taux_occupation_sans_dispo",
        "taux_occupation_avec_dispo",
        "taux_de_disponibilite",
        "taux_post_travail",
        "taux_de_pause_totale",
        "taux_pause",
        "taux_pause_break",
        "taux_pause_brief",
        "taux_pause_bug",
        "taux_pause_dejeuner",
        "taux_pause_entretien_rh",
        "taux_pause_formation"
    ],

    "fact_telephonie_codifications": [
    "nombre_de_codifications",
    "absent",
    "accord",
    "answering_machine",
    "busy",
    "call_abandoned_after_hold_time",
    "call_back_disable",
    "cessation_d_activite",
    "changement_de_fournisseur",
    "deja_client_chez_nous",
    "envoie_contrat_par_courrier",
    "envoie_contrat_par_mail",
    "faux_numero",
    "gere_par_un_autre_equipe",
    "gere_par_un_courtier",
    "hors_cible",
    "indisponible",
    "injoignable",
    "no_more_callback_rules",
    "not_qualified",
    "numero_errone",
    "pod_sensible_contacte",
    "polluants",
    "rappel_personnel",
    "refus",
    "refus_de_dialogue",
    "refus_de_renouvellement",
    "relance",
    "relance_pas_disponible_immediatement",
    "renouvele",
    "renouvele_par_une_autre_equipe",
    "repondeur",
    "repondeur_system",
    "scoring_ko_contacte",
    "unreachable_limit",
    "wrong_number_system",

    "absent_a_rappeler_suite_a_propale_envoye",
    "auto_entrepreneur_sans_local_pro",
    "barrage_secretaire",
    "detail_cessation_d_activite",
    "detail_changement_de_fournisseur",
    "changement_du_type_de_contrat",
    "client_sensible_non_deblocable",
    "communication_avec_le_commercial",
    "communication_avec_le_service_client",
    "compteur_de_chantier",
    "contrat_en_cours_via_un_autre_service",
    "declare_ne_pas_avoir_complete_de_formulaire",
    "deja_client",
    "deja_contacte_par_total_energie",
    "doublon_dossier",
    "dual",
    "duree_d_engagement",
    "ejp_tempo",
    "eld",
    "en_attente_document_info_manquante",
    "engage_a_plus_de_6_mois",
    "engage_plus_d_un_an",
    "detail_faux_numero",
    "formulaire_vide",
    "gestion_des_factures",
    "grands_comptes",
    "impaye",
    "injoignable_permanent_agent",
    "mauvais_echos_te_mauvaise_experience",
    "meilleure_proposition",
    "mono",
    "detail_no_more_callback_rules",
    "particulier_sans_activite_professionnelle",
    "pas_decisionnaire_pas_titulaire",
    "pas_decisionnaire_pas_titulaire_pas_mandate",
    "pod_sensible",
    "pris_dans_les_charges",
    "prix_trop_eleve",
    "professionnel_interesse_a_titre_particulier",
    "raccroche_client",
    "rappel_perso_finalisation_contrat",
    "detail_refus_de_dialogue",
    "satisfait_de_son_fournisseur_actuel",
    "scoring_ko",
    "service_client_part_pro",
    "siret_non_retourne",
    "stop_tel",
    "trop_cher_ne_voit_pas_les_economies",
    "veut_voir_un_commercial",
    "veut_reflechir_statuts_fc05_fc30"
]
}


def clean_columns(df):

    new_columns = []

    for col in df.columns:

        col = str(col).strip().lower()

        # Supprimer les accents
        col = unicodedata.normalize("NFD", col)
        col = "".join(
            c for c in col
            if unicodedata.category(c) != "Mn"
        )

        # Remplacer caractères spéciaux
        col = col.replace(" ", "_")
        col = col.replace("-", "_")
        col = col.replace("'", "_")
        col = col.replace("’", "_")
        col = col.replace("/", "_")

        # Supprimer doubles underscores
        col = re.sub(r"_+", "_", col)

        # Nettoyer début/fin
        col = col.strip("_")

        # Corrections spécifiques Looker
        col = col.replace("d_abandon", "abandon")
        col = col.replace("d_attente", "attente")
        col = col.replace("d_communication", "de_communication")

        new_columns.append(col)

    df.columns = new_columns

    return df

def simplify_looker_columns(df):
    prefixes = [
        "fact_telephonie_appel_",
        "fact_telephonie_action_",
        "fact_telephonie_codifications_",
        "fact_ventes_",
        "telephonie_appel_",
        "telephonie_action_",
        "telephonie_codifications_",
        "téléphonie_appel_",
        "téléphonie_action_",
        "téléphonie_codifications_",
        "ventes_totalenergies_",
        "dimension_employee_",
        "dimensions_communes_"
    ]

    new_cols = {}

    for col in df.columns:
        new_col = col
        for prefix in prefixes:
            if new_col.startswith(prefix):
                new_col = new_col.replace(prefix, "")
        new_cols[col] = new_col

    return df.rename(columns=new_cols)


def detect_fact_type(columns, filename=""):
    cols = " ".join(columns).lower()
    filename = filename.lower()

    if "fact_ventes" in filename or "ventes_realisees" in cols:
        return "fact_ventes"

    if (
        "fact_telephonie_appel" in filename
        or "appels_traites" in cols
        or "total_recu_projet_ae" in cols
        or "appels_abandonnes" in cols
    ):
        return "fact_telephonie_appel"

    if (
        "fact_telephonie_action" in filename
        or "duree_de_presence" in cols
        or "temps_de_pause" in cols
        or "duree_de_disponibilite" in cols
        or "duree_totale_des_pauses" in cols
        or "duree_de_post_travail" in cols
    ):
        return "fact_telephonie_action"

    if (
        "fact_telephonie_codifications" in filename
        or "nombre_de_codifications" in cols
        or "libelle_status" in cols
        or "accord" in cols
    ):
        return "fact_telephonie_codifications"

    return "unknown"


def convert_numeric(df):
    numeric_columns = []

    for col in df.columns:
        series = df[col].astype(str).str.strip()

        # Corriger les pourcentages : "99.97%" -> 99.97
        series = series.str.replace("%", "", regex=False)

        # Corriger les virgules décimales : "99,97" -> "99.97"
        series = series.str.replace(",", ".", regex=False)

        converted = pd.to_numeric(series, errors="coerce")

        if converted.notna().sum() > 0:
            df[col] = converted
            numeric_columns.append(col)

    return df, numeric_columns


def get_available_measures(df, fact_type, numeric_columns):
    expected = MEASURES_BY_FACT.get(fact_type, [])

    return [
        col for col in expected
        if col in df.columns and col in numeric_columns
    ]


uploaded_file = st.file_uploader("📤 Importer un fichier CSV Looker", type=["csv"])

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)
    except:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, sep=";")

    df = df.loc[:, ~df.columns.str.contains("^unnamed", case=False)]
    df = clean_columns(df)
    df = simplify_looker_columns(df)

    fact_type = detect_fact_type(df.columns, uploaded_file.name)
    df, numeric_columns = convert_numeric(df)
    measures = get_available_measures(df, fact_type, numeric_columns)

    st.session_state["df"] = df
    st.session_state["fact_type"] = fact_type
    st.session_state["available_measures"] = measures

    st.success(f"✅ Fichier chargé — Type détecté : {fact_type}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Lignes", df.shape[0])
    col2.metric("Colonnes", df.shape[1])
    col3.metric("KPI détectés", len(measures))

    st.subheader("📊 KPI disponibles")
    st.write(measures)

    st.subheader("📋 Aperçu complet")
    st.caption(f"Nombre total de lignes affichées : {df.shape[0]}")
    st.dataframe(df, use_container_width=True)

    st.info("Maintenant, utilise le menu à gauche pour accéder aux analyses.")

else:
    st.info("Importe d’abord un fichier CSV Looker pour activer les pages d’analyse.")