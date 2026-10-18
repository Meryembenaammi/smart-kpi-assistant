import streamlit as st
import plotly.express as px

st.set_page_config(page_title="KPI Overview", page_icon="📈", layout="wide")
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, rgba(239,68,68,0.10), transparent 35%),
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
    border-radius: 20px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.45);
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
    background: rgba(255,255,255,0.70) !important;
    border: 1px solid rgba(249,115,22,0.35) !important;
    box-shadow: 0 10px 25px rgba(127,29,29,0.08);
}

div[data-testid="stMultiSelect"] div {
    border-radius: 16px !important;
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

st.title("📈 Analyse KPI")

if "df" not in st.session_state:
    st.warning("Veuillez d’abord importer un fichier CSV dans la page d’accueil.")
    st.stop()

df = st.session_state["df"]
fact_type = st.session_state["fact_type"]
available_measures = st.session_state["available_measures"]


def get_dimension_options(df, available_measures):
    forbidden_keywords = [
        "duree",
        "temps",
        "taux",
        "appel",
        "appels",
        "vente",
        "ventes",
        "codification",
        "codifications",
        "accord",
        "absent",
        "refus",
        "injoignable",
        "callback",
        "pause",
        "presence",
        "disponibilite"
    ]

    dimensions = []

    for col in df.columns:
        if col in available_measures:
            continue

        if any(k in col for k in forbidden_keywords):
            continue

        dimensions.append(col)

    return dimensions


def find_default_dimension(dimensions):
    preferred = [
        "campaign_name",
        "campaign_id",
        "id_last_campaign",
        "action_campaign",
        "nom_campagne",
        "matricule",
        "agent",
        "employee_name",
        "team_lead_name",
        "tl",
        "id_agent"
    ]

    for col in preferred:
        if col in dimensions:
            return col

    return dimensions[0]


st.info(f"Type détecté : **{fact_type}**")

if not available_measures:
    st.warning("Aucune mesure KPI détectée.")
    st.stop()

dimension_options = get_dimension_options(df, available_measures)

if not dimension_options:
    st.warning("Aucune dimension détectée.")
    st.stop()

selected_measures = st.multiselect(
    "Choisir les mesures KPI",
    available_measures,
    default=available_measures[:4]
)

if selected_measures:
    cols = st.columns(min(len(selected_measures), 4))
    for i, metric in enumerate(selected_measures[:4]):
        cols[i].metric(metric.replace("_", " ").title(), f"{df[metric].sum():,.2f}")

st.subheader("Visualisation dynamique")

default_dimension = find_default_dimension(dimension_options)

dimension = st.selectbox(
    "Analyser par",
    dimension_options,
    index=dimension_options.index(default_dimension)
)

metric = st.selectbox(
    "Mesure KPI",
    available_measures
)

sort_order = st.radio(
    "Ordre de tri",
    ["Descending", "Ascending"],
    horizontal=True
)

ascending_value = sort_order == "Ascending"

# Supprimer les lignes avec dimensions nulles ou vides
analysis_df = df[
    df[dimension].notna()
]

analysis_df = analysis_df[
    analysis_df[dimension].astype(str).str.strip() != ""
]

grouped = (
    analysis_df.groupby(dimension)[metric]
    .sum()
    .reset_index()
    .sort_values(metric, ascending=ascending_value)
    .head(20)
)

# Transformer la dimension en texte pour l'afficher comme catégorie
grouped[dimension] = grouped[dimension].astype(str)

chart_type = st.selectbox(
    "Type de graphique",
    [
        "Bar Chart",
        "Line Chart",
        "Scatter Plot",
        "Area Chart",
        "Pie Chart"
    ]
)

if chart_type == "Bar Chart":
    fig = px.bar(
        grouped,
        x=dimension,
        y=metric,
        color=metric,
        text=metric,
        title=f"{metric} par {dimension} — {sort_order}"
    )

elif chart_type == "Line Chart":
    fig = px.line(
        grouped,
        x=dimension,
        y=metric,
        markers=True,
        title=f"{metric} par {dimension} — {sort_order}"
    )

elif chart_type == "Scatter Plot":
    fig = px.scatter(
        grouped,
        x=dimension,
        y=metric,
        color=metric,
        size=metric,
        title=f"{metric} par {dimension} — {sort_order}"
    )

elif chart_type == "Area Chart":
    fig = px.area(
        grouped,
        x=dimension,
        y=metric,
        title=f"{metric} par {dimension} — {sort_order}"
    )

elif chart_type == "Pie Chart":
    fig = px.pie(
        grouped,
        names=dimension,
        values=metric,
        title=f"Répartition de {metric} par {dimension}"
    )

if chart_type == "Bar Chart":
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")

elif chart_type in ["Line Chart", "Scatter Plot"]:
    fig.update_traces(textposition="top center")

fig.update_layout(
    xaxis_title=dimension,
    yaxis_title=metric,
    xaxis_type="category"
)

st.plotly_chart(fig, use_container_width=True)
st.dataframe(grouped, use_container_width=True)