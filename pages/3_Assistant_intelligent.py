import streamlit as st
import json
import unicodedata
from google import genai

st.set_page_config(page_title="KPI Assistant", page_icon="🤖", layout="wide")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(239,68,68,0.12), transparent 35%),
        radial-gradient(circle at top right, rgba(250,204,21,0.18), transparent 30%),
        linear-gradient(135deg, #fff7ed 0%, #fff1f2 45%, #f8fafc 100%);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #b91c1c 0%, #f97316 60%, #facc15 100%);
}

section[data-testid="stSidebar"] * {
    color: white !important;
    font-weight: 600;
}

h1 {
    font-size: 48px !important;
    font-weight: 900 !important;
    background: linear-gradient(90deg, #7f1d1d, #b91c1c, #ea580c, #eab308);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.chat-hero {
    background: linear-gradient(135deg, rgba(185,28,28,0.85), rgba(249,115,22,0.75), rgba(250,204,21,0.55));
    padding: 30px;
    border-radius: 28px;
    box-shadow: 0 25px 65px rgba(185, 28, 28, 0.20);
    margin-bottom: 25px;
}

.chat-bubble {
    background: rgba(255,255,255,0.92);
    padding: 22px 26px;
    border-radius: 24px 24px 24px 6px;
    max-width: 680px;
    font-size: 21px;
    color: #334155;
    box-shadow: 0 18px 45px rgba(15,23,42,0.12);
    position: relative;
}

.chat-bubble::after {
    content: "";
    position: absolute;
    bottom: -14px;
    left: 40px;
    border-width: 14px 14px 0 0;
    border-style: solid;
    border-color: rgba(255,255,255,0.92) transparent transparent transparent;
}

.assistant-avatar {
    width: 82px;
    height: 82px;
    border-radius: 50%;
    background: linear-gradient(135deg, #b91c1c, #f97316, #facc15);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 38px;
    box-shadow: 0 18px 45px rgba(127,29,29,0.25);
    animation: floatBot 3s ease-in-out infinite;
    margin-top: 18px;
}

@keyframes floatBot {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.chat-row {
    display: flex;
    align-items: flex-end;
    gap: 18px;
}

div[data-testid="stAlert"] {
    border-radius: 22px;
    background: rgba(255,255,255,0.70);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 14px 35px rgba(127, 29, 29, 0.12);
    animation: fadeIn 0.5s ease-in-out;
}

div[data-baseweb="select"] > div {
    border-radius: 18px !important;
    background: rgba(255,255,255,0.78) !important;
    border: 1px solid rgba(249,115,22,0.35) !important;
    box-shadow: 0 10px 25px rgba(127,29,29,0.08);
}

input {
    border-radius: 18px !important;
    border: 1px solid rgba(249,115,22,0.45) !important;
    padding: 12px !important;
    background: rgba(255,255,255,0.85) !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 18px 45px rgba(15,23,42,0.10);
    border: 1px solid rgba(255,255,255,0.55);
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

.block-container {
    padding-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Assistant KPI")

st.markdown("""
<div class="chat-hero">
    <div class="chat-row">
        <div class="chat-bubble">
            Bonjour 👋, je suis votre assistant intelligent.<br>
            Je peux vous aider à analyser les KPI, identifier les meilleures campagnes,
            les meilleurs agents, les offres, les canaux et les statuts selon le type de fact.
        </div>
        <div class="assistant-avatar">🤖</div>
    </div>
</div>
""", unsafe_allow_html=True)

if "df" not in st.session_state:
    st.warning("Veuillez d’abord importer un fichier CSV dans la page d’accueil.")
    st.stop()

df = st.session_state["df"]
available_measures = st.session_state["available_measures"]
fact_type = st.session_state.get("fact_type", "unknown")

if not available_measures:
    st.warning("Aucune mesure KPI détectée.")
    st.stop()

st.info(f"Type détecté : **{fact_type}**")

FACT_CONFIG = {
    "fact_ventes": {
        "agent": ["employee_name", "matricule", "agent"],
        "fallback_agent": ["login_createur"],
        "campagne": ["correspondance_campagne_hermes", "nom_campagne", "campaign_id", "campaign_name"],
        "date": ["date_signature", "date", "signature_date"],
        "statut": ["etat_site"],
        "offre": ["nom_offre"],
        "canal": ["canal_2", "canal"],
        "team_leader": ["tl", "team_leader", "team_lead_name"]
    },
    "fact_telephonie_appel": {
        "agent": ["employee_name", "matricule", "id_last_agent", "id_agent"],
        "campagne": ["id_last_campaign", "campaign_name", "campaign_id"],
        "date": ["call_date", "date"],
        "tranche": ["call_tranche", "start_hour"],
        "statut": ["call_status", "id_call_status", "libelle_status"]
    },
    "fact_telephonie_action": {
        "agent": ["employee_name", "matricule", "id_agent"],
        "campagne": ["action_campaign", "campaign_name", "campaign_id"],
        "date": ["action_date", "date"],
        "tranche": ["action_tranche", "action_time_utc"],
        "statut": ["id_action_state", "id_action_state_detail"]
    },
    "fact_codifications": {
        "agent": ["employee_name", "matricule", "id_agent"],
        "campagne": ["campaign_name", "campaign_id"],
        "date": ["appel_date", "form_import_date", "date"],
        "statut": ["libelle_status"],
        "detail": ["libelle_detail"],
        "fichier": ["fichier"]
    },
    "fact_codifications_appels_client": {
        "agent": ["employee_name", "matricule", "id_agent"],
        "campagne": ["campaign_name", "campaign_id"],
        "date": ["appel_date", "form_import_date", "date"],
        "statut": ["libelle_status"],
        "detail": ["libelle_detail"],
        "fichier": ["fichier"]
    },
    "fact_agent_360": {
        "agent": ["employee_name", "matricule", "id_agent"],
        "campagne": ["campaign_name", "campaign_id"],
        "date": ["date", "call_date", "action_date", "appel_date"],
        "tranche": ["tranche", "call_tranche", "action_tranche"],
        "team_leader": ["team_leader", "team_lead_name", "tl"]
    }
}

GLOBAL_DIMENSIONS = {
    "agent": ["employee_name", "agent", "matricule", "id_agent", "id_last_agent"],
    "campagne": ["campaign_name", "campaign_id", "id_last_campaign", "action_campaign", "nom_campagne", "correspondance_campagne_hermes"],
    "date": ["date", "call_date", "action_date", "appel_date", "date_signature", "form_import_date"],
    "statut": ["etat_site", "libelle_status", "call_status", "id_action_state", "id_action_state_detail"],
    "offre": ["nom_offre", "offre"],
    "canal": ["canal_2", "canal"],
    "team_leader": ["tl", "team_leader", "team_lead_name"],
    "tranche": ["call_tranche", "action_tranche", "start_hour", "tranche"],
    "detail": ["libelle_detail"],
    "fichier": ["fichier"]
}


def find_dimension(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def find_dimension_by_type(df, fact_type, dimension_type):
    fact_config = FACT_CONFIG.get(fact_type, {})

    candidates = fact_config.get(dimension_type, [])
    dimension = find_dimension(df, candidates)

    if dimension:
        return dimension

    if dimension_type == "agent":
        fallback = fact_config.get("fallback_agent", [])
        dimension = find_dimension(df, fallback)

        if dimension:
            return dimension

    return find_dimension(df, GLOBAL_DIMENSIONS.get(dimension_type, []))


def get_display_dimension_name(dimension):
    if dimension == "login_createur":
        return "agent"
    return dimension


def clean_dimension_values(dataframe, dimension):
    analysis_df = dataframe[dataframe[dimension].notna()].copy()

    analysis_df = analysis_df[
        analysis_df[dimension].astype(str).str.strip() != ""
    ]

    analysis_df = analysis_df[
        analysis_df[dimension].astype(str).str.lower().str.strip() != "none"
    ]

    analysis_df = analysis_df[
        analysis_df[dimension].astype(str).str.lower().str.strip() != "nan"
    ]

    return analysis_df


def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return text


def detect_action_from_question(question):
    q = normalize_text(question)

    top_keywords = [
        "meilleur",
        "meilleure",
        "plus performant",
        "top",
        "plus grand",
        "genere le plus",
        "genere plus",
        "produit le plus",
        "realise le plus",
        "fait le plus",
        "donne le plus",
        "apporte le plus",
        "a le plus",
        "le plus de",
        "plusieurs ventes"
    ]

    bottom_keywords = [
        "moins performant",
        "moins performante",
        "plus faible",
        "minimum",
        "dernier",
        "derniere",
        "genere le moins",
        "fait le moins",
        "a le moins",
        "le moins de",
        "moins de ventes"
    ]

    total_keywords = [
        "total",
        "combien au total",
        "somme"
    ]

    average_keywords = [
        "moyenne",
        "moyen",
        "average"
    ]

    count_keywords = [
        "nombre de lignes",
        "nombre d'elements",
        "combien de lignes"
    ]

    for keyword in bottom_keywords:
        if keyword in q:
            return "bottom"

    for keyword in top_keywords:
        if keyword in q:
            return "top"

    for keyword in total_keywords:
        if keyword in q:
            return "total"

    for keyword in average_keywords:
        if keyword in q:
            return "average"

    for keyword in count_keywords:
        if keyword in q:
            return "count"

    return None


def detect_dimension_type_from_question(question):
    q = normalize_text(question)

    if "campagne" in q:
        return "campagne"

    if "canal" in q:
        return "canal"

    if "agent" in q or "conseiller" in q or "matricule" in q or "commercial" in q or "login createur" in q:
        return "agent"

    if "offre" in q:
        return "offre"

    if "team leader" in q or "tl" in q or "superviseur" in q:
        return "team_leader"

    if "tranche" in q or "heure" in q:
        return "tranche"

    if "statut" in q or "status" in q or "etat" in q:
        return "statut"

    if "detail" in q or "codification" in q:
        return "detail"

    if "fichier" in q:
        return "fichier"

    if "date" in q or "jour" in q or "mois" in q or "periode" in q:
        return "date"

    return None


def clean_json_response(text):
    text = text.replace("```json", "").replace("```", "").strip()
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text


def ask_gemini(question, metric, columns, fact_type):
    prompt = f"""
Tu es un assistant KPI intelligent pour une application Streamlit.

Type de fact détecté :
{fact_type}

Colonnes disponibles dans le CSV :
{columns}

KPI sélectionné :
{metric}

Question utilisateur :
{question}

Retourne uniquement un JSON valide, sans texte avant ni après.

Format attendu :
{{
  "action": "total" | "top" | "bottom" | "average" | "count" | "unknown",
  "dimension_type": "agent" | "campagne" | "date" | "statut" | "offre" | "canal" | "team_leader" | "tranche" | "detail" | "fichier" | "none",
  "dimension": "nom_colonne_ou_null",
  "answer_text": "réponse courte en français"
}}

Règles :
- Si l'utilisateur demande un total ou combien au total : action = "total".
- Si l'utilisateur demande le meilleur, le plus performant, le top, le plus grand, génère le plus, produit le plus, réalise le plus, fait le plus, donne le plus, apporte le plus, a le plus, le plus de : action = "top".
- Si l'utilisateur demande le moins performant, le plus faible, le minimum, le dernier, génère le moins, fait le moins, a le moins, le moins de : action = "bottom".
- Si l'utilisateur demande une moyenne : action = "average".
- Si l'utilisateur demande le nombre de lignes ou nombre d'éléments : action = "count".
- Si la question contient "campagne", dimension_type = "campagne".
- Si la question contient "canal", dimension_type = "canal".
- Si la question parle d'agent, conseiller, matricule, commercial ou login créateur : dimension_type = "agent".
- Si la question parle de date, jour, mois, période : dimension_type = "date".
- Si la question parle de statut, état, état site : dimension_type = "statut".
- Si la question parle d'offre : dimension_type = "offre".
- Si la question parle de team leader, TL, superviseur : dimension_type = "team_leader".
- Si la question parle de tranche ou heure : dimension_type = "tranche".
- Si la question parle de détail de codification : dimension_type = "detail".
- Si la question parle de fichier : dimension_type = "fichier".
- Pour agent, privilégier toujours employee_name, matricule ou agent avant login_createur.
- La dimension doit être une colonne existante parmi les colonnes disponibles.
- Si tu n'es pas sûr, action = "unknown".
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def local_ai_fallback(question):
    action = detect_action_from_question(question)
    dimension_type = detect_dimension_type_from_question(question)

    return {
        "action": action if action else "unknown",
        "dimension_type": dimension_type if dimension_type else "none",
        "dimension": None,
        "answer_text": "Analyse effectuée avec les règles locales."
    }


metric = st.selectbox("Choisir la mesure KPI", available_measures)
question = st.text_input("Pose une question")

if question:
    thinking_box = st.empty()

    thinking_box.markdown("""
    <div style="
        display:flex;
        align-items:center;
        gap:14px;
        background:rgba(255,255,255,0.78);
        border:1px solid rgba(249,115,22,0.35);
        border-radius:22px;
        padding:18px 22px;
        box-shadow:0 14px 35px rgba(127,29,29,0.12);
        margin-top:18px;
        color:#334155;
        font-size:18px;">
        <div style="
            width:42px;
            height:42px;
            border-radius:50%;
            background:linear-gradient(135deg,#b91c1c,#f97316,#facc15);
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:22px;">🤖</div>
        <div>
            <strong>Assistant KPI réfléchit...</strong><br>
            Analyse de la question selon le type de fact et les colonnes du CSV.
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        ai_response = ask_gemini(question, metric, df.columns.tolist(), fact_type)
        thinking_box.empty()

        ai_response = clean_json_response(ai_response)
        parsed = json.loads(ai_response)

    except Exception:
        thinking_box.empty()
        parsed = local_ai_fallback(question)

    action = parsed.get("action")
    dimension_type = parsed.get("dimension_type")
    dimension = parsed.get("dimension")
    answer_text = parsed.get("answer_text")

    detected_action = detect_action_from_question(question)
    detected_dimension_type = detect_dimension_type_from_question(question)

    if detected_action:
        action = detected_action

    if detected_dimension_type:
        dimension_type = detected_dimension_type
        dimension = find_dimension_by_type(df, fact_type, dimension_type)

    if action == "total":
        total = df[metric].sum()
        st.success(f"Le total de **{metric}** est : **{total:,.2f}**")
        st.info(answer_text)

    elif action == "average":
        moyenne = df[metric].mean()
        st.success(f"La moyenne de **{metric}** est : **{moyenne:,.2f}**")
        st.info(answer_text)

    elif action == "count":
        st.success(f"Le nombre total de lignes dans le fichier est : **{len(df):,}**")
        st.info(answer_text)

    elif action in ["top", "bottom"]:
        if dimension_type == "agent":
            dimension = find_dimension_by_type(df, fact_type, dimension_type)
        elif dimension not in df.columns:
            dimension = find_dimension_by_type(df, fact_type, dimension_type)

        if dimension and dimension in df.columns:
            display_dimension = get_display_dimension_name(dimension)
            ascending_order = action == "bottom"

            analysis_df = clean_dimension_values(df, dimension)

            if analysis_df.empty:
                st.warning("Aucune donnée exploitable après suppression des valeurs vides.")
                st.stop()

            result = (
                analysis_df.groupby(dimension)[metric]
                .sum()
                .reset_index()
                .sort_values(metric, ascending=ascending_order)
                .head(10)
            )

            if dimension == "login_createur":
                result = result.rename(columns={"login_createur": "agent"})
                dimension_for_display = "agent"
            else:
                dimension_for_display = dimension

            best_row = result.iloc[0]
            best_name = best_row[dimension_for_display]
            best_value = best_row[metric]

            if action == "top":
                st.success(
                    f"La meilleure valeur pour **{display_dimension}** est **{best_name}** "
                    f"avec **{best_value:,.2f}** pour **{metric}**."
                )
                st.info(
                    f"Voici ensuite le Top 10 selon **{metric}** par **{display_dimension}**."
                )

            else:
                st.warning(
                    f"La valeur la plus faible pour **{display_dimension}** est **{best_name}** "
                    f"avec **{best_value:,.2f}** pour **{metric}**."
                )
                st.info(
                    f"Voici ensuite les 10 valeurs les plus faibles selon **{metric}** par **{display_dimension}**."
                )

            st.dataframe(result, use_container_width=True)

        else:
            st.warning("Aucune dimension adaptée détectée pour répondre à cette question.")

    else:
        st.write("""
        Je n’ai pas bien compris la question.

        Exemples :
        - Quel est le total ?
        - Quelle est la moyenne ?
        - Quelle est la meilleure campagne ?
        - Quel est l’agent le moins performant ?
        - Quelle est la meilleure offre ?
        - Quel canal a le plus de ventes ?
        - Donne-moi le top 10 par statut.
        """)

else:
    st.info("Exemples : total, moyenne, meilleure campagne, agent le moins performant, meilleure offre, top par canal.")