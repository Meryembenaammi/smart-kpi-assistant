import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="ML Predictive Modeling", page_icon="🧠", layout="wide")

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
    position: relative;
}

section[data-testid="stSidebar"] * {
    color: white !important;
    font-weight: 600;
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

section[data-testid="stSidebar"]::after {
    content: "© 2026 Smart KPI Assistant — Tous droits réservés";
    position: absolute;
    bottom: 18px;
    left: 10px;
    right: 10px;
    text-align: center;
    font-size: 12px;
    font-weight: 400;
    color: #111827;
    letter-spacing: 0.3px;
    background: none;
    border: none;
    box-shadow: none;
}

h1 {
    font-size: 52px !important;
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
    background: rgba(255,255,255,0.62);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 14px 35px rgba(127, 29, 29, 0.12);
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
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 28px 70px rgba(127, 29, 29, 0.22);
}

div[data-baseweb="select"] > div {
    border-radius: 18px !important;
    background: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(249,115,22,0.35) !important;
    box-shadow: 0 10px 25px rgba(127,29,29,0.08);
}

div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    border-radius: 18px !important;
}

div[data-testid="stRadio"] {
    background: rgba(255,255,255,0.48);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 16px 20px;
    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 14px 35px rgba(127,29,29,0.08);
}

.stSlider {
    background: rgba(255,255,255,0.42);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 18px 22px;
    border: 1px solid rgba(255,255,255,0.55);
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
    padding-bottom: 4rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 ML Predictive Modeling")

if "df" not in st.session_state:
    st.warning("Veuillez d’abord importer un fichier CSV dans la page d’accueil.")
    st.stop()

df = st.session_state["df"]
fact_type = st.session_state.get("fact_type", "unknown")
available_measures = st.session_state.get("available_measures", [])

st.info(f"Type détecté : **{fact_type}**")

if not available_measures:
    st.warning("Aucune mesure KPI détectée pour entraîner un modèle.")
    st.stop()

st.markdown("""
Cette page permet de tester plusieurs modèles de Machine Learning sur les KPI chargés depuis Looker.
L’objectif est de comparer les performances des modèles et de visualiser les prédictions produites par chaque modèle.
""")

# =========================
# VARIABLES EXPLICATIVES PAR FACT
# =========================

FEATURES_BY_FACT = {
    "fact_ventes": [
        "etat_site",
        "canal_2",
        "nom_offre",
        "login_createur",
        "matricule",
        "agent",
        "tl",
        "nom_campagne",
        "correspondance_campagne_hermes",
        "campaign_id"
    ],

    "fact_telephonie_appel": [
        "matricule",
        "id_last_agent",
        "id_last_campaign",
        "call_tranche",
        "duree_de_communication",
        "duree_totale_attente",
        "dmc",
        "duree_moyenne_attente",
        "duree_moyenne_abandon",
        "call_conversation_duration"
    ],

    "fact_telephonie_action": [
        "matricule",
        "id_agent",
        "action_campaign",
        "action_tranche",
        "duree_de_presence",
        "duree_de_disponibilite",
        "duree_de_post_travail",
        "duree_totale_des_pauses",
        "duree_appels_sortants",
        "duree_appels_entrants",
        "duree_callback",
        "duree_numerotation",
        "duree_saisie_de_numero",
        "duree_appel_manuel",
        "duree_lecture_du_message",
        "duree_mode_recherche"
    ],

    "fact_telephonie_codifications": [
        "id_agent",
        "matricule",
        "campaign_name",
        "fichier",
        "libelle_detail",
        "libelle_status"
    ]
}

LEAKAGE_KEYWORDS = [
    "accord", "absent", "refus", "injoignable", "busy", "repondeur",
    "answering_machine", "faux_numero", "indisponible", "relance",
    "renouvele", "scoring", "wrong_number", "unreachable",
    "codification", "codifications",
    "appels_traites", "appels_abandonnes", "total_recu_projet_ae",
    "ventes_realisees"
]


def is_leakage_feature(col, target):
    if col == target:
        return True

    if target == "nombre_de_codifications":
        return any(k in col for k in LEAKAGE_KEYWORDS)

    if target == "ventes_realisees":
        return col in ["ventes_realisees"]

    if target in ["qs_ae"]:
        return col in ["appels_traites", "appels_abandonnes"]

    if target == "duree_moyenne_attente":
        return col in ["duree_totale_attente", "total_recu_projet_ae"]

    return False


def get_smart_features(df, fact_type, target):
    candidates = FEATURES_BY_FACT.get(fact_type, df.columns.tolist())

    features = []
    for col in candidates:
        if col in df.columns and not is_leakage_feature(col, target):
            features.append(col)

    return features


target = st.selectbox("Choisir le KPI à prédire", available_measures)

st.markdown("### 🧠 Sélection des variables explicatives")

mode_selection = st.radio(
    "Mode de sélection",
    [
        "Auto détecter les meilleures variables",
        "Sélection manuelle"
    ],
    horizontal=True
)

all_possible_features = [
    col for col in df.columns
    if col != target and not is_leakage_feature(col, target)
]

smart_features = get_smart_features(df, fact_type, target)

if mode_selection == "Auto détecter les meilleures variables":
    selected_features = st.multiselect(
        "Variables explicatives proposées automatiquement",
        all_possible_features,
        default=smart_features
    )
else:
    selected_features = st.multiselect(
        "Choisir les variables explicatives",
        all_possible_features,
        default=smart_features[:min(5, len(smart_features))]
    )

if not selected_features:
    st.warning("Veuillez choisir au moins une variable explicative.")
    st.stop()

st.success(f"Variables utilisées : {selected_features}")

# =========================
# PRÉPARATION DATA
# =========================

data_ml = df[selected_features + [target]].copy()
data_ml = data_ml.replace([np.inf, -np.inf], np.nan)
data_ml = data_ml.dropna()

if data_ml.shape[0] < 10:
    st.warning("Pas assez de lignes exploitables pour entraîner un modèle ML.")
    st.stop()

X = data_ml[selected_features]
y = data_ml[target]

numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
categorical_features = X.select_dtypes(exclude=["number"]).columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

test_size = st.slider(
    "Taille du jeu de test",
    min_value=0.10,
    max_value=0.40,
    value=0.20,
    step=0.05
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=test_size,
    random_state=42
)

# =========================
# COMPARAISON DES MODÈLES
# =========================

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree Regressor": DecisionTreeRegressor(random_state=42),
    "Random Forest Regressor": RandomForestRegressor(n_estimators=150, random_state=42),
    "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42),
    "KNN Regressor": KNeighborsRegressor(n_neighbors=5),
    "SVR": SVR()
}

results_models = []
trained_models = {}

predictions_all_models = pd.DataFrame(index=y_test.index)
predictions_all_models["Valeur réelle"] = y_test

for name, model in models.items():
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    try:
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        y_pred = np.array(y_pred)

        if (y >= 0).all():
            y_pred = np.clip(y_pred, 0, None)

        y_pred = np.clip(
            y_pred,
            np.percentile(y_train, 1),
            np.percentile(y_train, 99)
        )

        y_pred_series = pd.Series(y_pred, index=y_test.index)

        mae = mean_absolute_error(y_test, y_pred_series)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred_series))
        r2 = r2_score(y_test, y_pred_series)

        results_models.append({
            "Modèle": name,
            "MAE": mae,
            "RMSE": rmse,
            "R²": r2
        })

        trained_models[name] = {
            "pipeline": pipeline,
            "y_pred": y_pred_series
        }

        predictions_all_models[f"Prédiction - {name}"] = y_pred_series

    except Exception:
        results_models.append({
            "Modèle": name,
            "MAE": np.nan,
            "RMSE": np.nan,
            "R²": np.nan
        })

comparison_df = pd.DataFrame(results_models)
comparison_df_clean = comparison_df.dropna()

if comparison_df_clean.empty:
    st.error("Aucun modèle n’a pu être entraîné avec les variables sélectionnées.")
    st.stop()

st.subheader("📊 Comparaison des modèles")
st.dataframe(comparison_df, use_container_width=True)

fig_compare = px.bar(
    comparison_df_clean,
    x="Modèle",
    y="R²",
    title="Comparaison des modèles selon R²"
)
st.plotly_chart(fig_compare, use_container_width=True)

best_model_row = comparison_df_clean.sort_values(
    by=["R²", "RMSE"],
    ascending=[False, True]
).iloc[0]

best_model_name = best_model_row["Modèle"]
best_y_pred = trained_models[best_model_name]["y_pred"]

st.subheader("🏆 Modèle optimal")

st.success(
    f"Le modèle le plus optimal est **{best_model_name}** "
    f"avec R² = **{best_model_row['R²']:.2f}**, "
    f"MAE = **{best_model_row['MAE']:.2f}**, "
    f"RMSE = **{best_model_row['RMSE']:.2f}**."
)

# =========================
# PERFORMANCE DU MEILLEUR MODÈLE
# =========================

st.subheader("📈 Performance du modèle optimal")

col1, col2, col3 = st.columns(3)
col1.metric("MAE", f"{best_model_row['MAE']:,.2f}")
col2.metric("RMSE", f"{best_model_row['RMSE']:,.2f}")
col3.metric("R²", f"{best_model_row['R²']:,.2f}")

# =========================
# PRÉDICTIONS DE TOUS LES MODÈLES
# =========================

st.subheader("🔮 Prédictions selon chaque modèle")
st.dataframe(predictions_all_models.reset_index(drop=True), use_container_width=True)

# =========================
# CHOISIR UN MODÈLE POUR VISUALISER LA PRÉDICTION
# =========================

st.subheader("📈 Valeurs réelles vs valeurs prédites")

selected_model_name = st.selectbox(
    "Choisir un modèle pour visualiser les prédictions",
    list(trained_models.keys()),
    index=list(trained_models.keys()).index(best_model_name)
)

selected_y_pred = trained_models[selected_model_name]["y_pred"]

results = pd.DataFrame({
    "Valeur réelle": y_test,
    "Valeur prédite": selected_y_pred
}).reset_index(drop=True)

fig = px.scatter(
    results,
    x="Valeur réelle",
    y="Valeur prédite",
    title=f"Comparaison Réel vs Prédit — {target} avec {selected_model_name}"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Résultats détaillés du modèle sélectionné")
st.dataframe(results, use_container_width=True)

# =========================
# IMPORTANCE VARIABLES
# =========================

if selected_model_name in [
    "Random Forest Regressor",
    "Gradient Boosting Regressor"
]:
    best_pipeline = trained_models[selected_model_name]["pipeline"]
    model = best_pipeline.named_steps["model"]
    preprocessor_fitted = best_pipeline.named_steps["preprocessor"]

    feature_names = []

    if numeric_features:
        feature_names.extend(numeric_features)

    if categorical_features:
        cat_names = preprocessor_fitted.named_transformers_["cat"].get_feature_names_out(categorical_features)
        feature_names.extend(cat_names)

    if hasattr(model, "feature_importances_"):
        importances = pd.DataFrame({
            "Variable": feature_names,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=False)

        st.subheader("🔥 Importance des variables")

        fig_imp = px.bar(
            importances.head(15),
            x="Variable",
            y="Importance",
            title=f"Top variables les plus importantes — {selected_model_name}"
        )

        st.plotly_chart(fig_imp, use_container_width=True)
        st.dataframe(importances, use_container_width=True)