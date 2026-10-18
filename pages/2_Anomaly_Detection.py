import streamlit as st
import plotly.express as px
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

st.set_page_config(page_title="Anomaly Detection", page_icon="🚨", layout="wide")
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

h2, h3 {
    color: #7f1d1d !important;
    font-weight: 900 !important;
}

div[data-testid="stAlert"] {
    border-radius: 22px;
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.5);
    box-shadow: 0 14px 35px rgba(127, 29, 29, 0.10);
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.58);
    backdrop-filter: blur(16px);
    border-radius: 26px;
    padding: 24px;
    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 18px 45px rgba(127, 29, 29, 0.12);
    transition: all 0.35s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 28px 70px rgba(127, 29, 29, 0.22);
}

div[data-baseweb="select"] > div {
    border-radius: 18px !important;
    background: rgba(255,255,255,0.72) !important;
    border: 1px solid rgba(249,115,22,0.35) !important;
    box-shadow: 0 10px 25px rgba(127,29,29,0.08);
}

.stPlotlyChart {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(16px);
    border-radius: 28px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 18px 45px rgba(127, 29, 29, 0.10);
}

div[data-testid="stDataFrame"] {
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 18px 45px rgba(15,23,42,0.10);
    border: 1px solid rgba(255,255,255,0.55);
}

.block-container {
    padding-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🚨 Détection d’anomalies")

if "df" not in st.session_state:
    st.warning("Veuillez d’abord importer un fichier CSV dans la page d’accueil.")
    st.stop()

df = st.session_state["df"]
fact_type = st.session_state["fact_type"]
available_measures = st.session_state["available_measures"]

st.info(f"Type détecté : **{fact_type}**")

if not available_measures:
    st.warning("Aucune mesure KPI détectée.")
    st.stop()

preferred_dimensions = [
    "matricule", "id_agent", "employee_name", "team_lead_name",
    "campaign_name", "campaign_id", "id_last_campaign",
    "action_campaign", "nom_campagne"
]

dimension_options = [
    col for col in preferred_dimensions
    if col in df.columns and df[col].nunique() >= 4
]

if not dimension_options:
    dimension_options = [
        col for col in df.columns
        if df[col].nunique() >= 4 and col not in available_measures
    ]

if not dimension_options:
    st.warning("Aucune dimension avec suffisamment de valeurs différentes pour détecter les anomalies.")
    st.stop()

dimension = st.selectbox("Dimension d’analyse", dimension_options)
metric = st.selectbox("KPI à analyser", available_measures)

# Supprimer les lignes où la dimension est vide ou null
analysis_df = df[
    df[dimension].notna()
]

# Supprimer aussi les chaînes vides
analysis_df = analysis_df[
    analysis_df[dimension].astype(str).str.strip() != ""
]

grouped = (
    analysis_df.groupby(dimension)[metric]
    .sum()
    .reset_index()
)

if len(grouped) < 4:
    st.warning("Pas assez de groupes pour détecter les anomalies. Choisis une autre dimension.")
    st.stop()

model = IsolationForest(contamination=0.2, random_state=42)
grouped["anomaly"] = model.fit_predict(grouped[[metric]])
grouped["statut"] = grouped["anomaly"].apply(lambda x: "Anomalie" if x == -1 else "Normal")

mean_value = grouped[metric].mean()
std_value = grouped[metric].std()

# =========================
# LABELS MÉTIER
# =========================

threshold_high = mean_value + 2 * std_value
threshold_low = mean_value - 2 * std_value

grouped["true_label"] = grouped[metric].apply(
    lambda x: -1 if (x > threshold_high or x < threshold_low) else 1
)

# =========================
# MÉTRIQUES DE PERFORMANCE
# =========================

accuracy = accuracy_score(
    grouped["true_label"],
    grouped["anomaly"]
)

precision = precision_score(
    grouped["true_label"],
    grouped["anomaly"],
    pos_label=-1,
    zero_division=0
)

recall = recall_score(
    grouped["true_label"],
    grouped["anomaly"],
    pos_label=-1,
    zero_division=0
)

f1 = f1_score(
    grouped["true_label"],
    grouped["anomaly"],
    pos_label=-1,
    zero_division=0
)

def explain_anomaly(row):
    value = row[metric]
    diff = value - mean_value
    pct_diff = (diff / mean_value * 100) if mean_value != 0 else 0

    if value > mean_value:
        direction = "supérieure"
        interpretation = "valeur exceptionnellement élevée"
    else:
        direction = "inférieure"
        interpretation = "valeur exceptionnellement faible"

    return (
        f"La valeur **{value:,.2f}** pour **{row[dimension]}** est {direction} "
        f"à la moyenne globale (**{mean_value:,.2f}**), avec un écart de "
        f"**{pct_diff:+.2f}%**. Cela peut indiquer une {interpretation} "
        f"par rapport aux autres groupes."
    )

fig = px.scatter(
    grouped,
    x=dimension,
    y=metric,
    color="statut",
    size=metric,
    title=f"Anomalies détectées sur {metric} par {dimension}"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📌 Résumé de l’analyse")
st.write(
    f"L’algorithme compare les valeurs du KPI **{metric}** entre les différents groupes de la dimension "
    f"**{dimension}**. Une anomalie correspond à une valeur très différente du comportement global observé."
)

col1, col2 = st.columns(2)

col1.metric(
    "Moyenne globale",
    f"{mean_value:,.2f}"
)

col2.metric(
    "Écart-type",
    f"{std_value:,.2f}"
)

st.subheader("📈 Performance de détection")

col3, col4, col5, col6 = st.columns(4)

col3.metric(
    "Accuracy",
    f"{accuracy:.2f}"
)

col4.metric(
    "Precision",
    f"{precision:.2f}"
)

col5.metric(
    "Recall",
    f"{recall:.2f}"
)

col6.metric(
    "F1-score",
    f"{f1:.2f}"
)

anomalies = grouped[grouped["statut"] == "Anomalie"].copy()

st.subheader("🚨 Anomalies détectées")

if anomalies.empty:
    st.success("Aucune anomalie significative détectée.")
else:
    for _, row in anomalies.iterrows():
        st.warning(explain_anomaly(row))

    st.dataframe(anomalies, use_container_width=True)

st.subheader("📊 Toutes les valeurs analysées")
st.dataframe(grouped.sort_values(metric, ascending=False), use_container_width=True)