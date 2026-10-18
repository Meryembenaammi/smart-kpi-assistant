import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Quality", page_icon="📋", layout="wide")
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

div[data-testid="stAlert"] {
    border-radius: 22px;
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 14px 35px rgba(127, 29, 29, 0.12);
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

st.title("📋 Data Quality")

if "df" not in st.session_state:
    st.warning("Veuillez d’abord importer un fichier CSV dans la page d’accueil.")
    st.stop()

df = st.session_state["df"]
numeric_columns = st.session_state.get("numeric_columns", df.select_dtypes(include="number").columns.tolist())
fact_type = st.session_state["fact_type"]

col1, col2, col3 = st.columns(3)
col1.metric("Nombre de lignes", df.shape[0])
col2.metric("Nombre de colonnes", df.shape[1])
col3.metric("Colonnes numériques", len(numeric_columns))

st.info(f"Type détecté : **{fact_type}**")

st.markdown("### Valeurs nulles et valeurs vides")

empty_values = ["", " ", "null", "NULL", "None", "none", "N/A", "n/a", "NA", "na", "-", "--"]

null_counts = []

for col in df.columns:
    valeurs_nulles = df[col].isna().sum()
    valeurs_vides = df[col].astype(str).str.strip().isin(empty_values).sum()

    null_counts.append({
        "colonne": col,
        "valeurs_nulles": valeurs_nulles,
        "valeurs_vides": valeurs_vides,
        "total_nulles_ou_vides": valeurs_nulles + valeurs_vides
    })

nulls = pd.DataFrame(null_counts)
nulls = nulls.sort_values("total_nulles_ou_vides", ascending=False)

# =========================
# METRICS DATA QUALITY
# =========================

total_cells = df.shape[0] * df.shape[1]

total_missing = nulls["total_nulles_ou_vides"].sum()

missing_rate = (
    (total_missing / total_cells) * 100
    if total_cells > 0 else 0
)

completeness_rate = 100 - missing_rate

col4, col5, col6 = st.columns(3)

col4.metric(
    "Valeurs nulles/vides",
    int(total_missing)
)

col5.metric(
    "Taux de valeurs manquantes",
    f"{missing_rate:.2f}%"
)

col6.metric(
    "Taux de complétude",
    f"{completeness_rate:.2f}%"
)

st.dataframe(nulls, use_container_width=True)

fig = px.bar(
    nulls.head(20),
    x="colonne",
    y="total_nulles_ou_vides",
    title="Top colonnes avec valeurs nulles ou vides",
    text="total_nulles_ou_vides"
)

fig.update_traces(textposition="outside")
fig.update_layout(
    xaxis_title="Colonne",
    yaxis_title="Valeurs nulles ou vides"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### Colonnes disponibles")
st.write(df.columns.tolist())

st.markdown("### Aperçu des données")
st.dataframe(df.head(30), use_container_width=True)