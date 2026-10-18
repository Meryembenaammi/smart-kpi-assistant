
# 📊 Smart KPI Assistant

<p align="center">
  <strong>An intelligent analytics application for KPI monitoring, anomaly detection, predictive modeling, and AI-powered data exploration.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--learn-F7931E?logo=scikitlearn&logoColor=white" alt="Machine Learning" />
  <img src="https://img.shields.io/badge/Visualization-Plotly-3F4F75?logo=plotly&logoColor=white" alt="Plotly" />
</p>

---

## 📌 Overview

**Smart KPI Assistant** is an interactive application designed to help users monitor key performance indicators (KPIs), identify unusual patterns, explore predictive models, and interact with data more intuitively.

Built with Python and Streamlit, the application combines business intelligence, data analytics, machine learning, and AI-powered assistance in a single interface.

## ✨ Features

### 📈 KPI Overview
- Explore key performance indicators through interactive dashboards.
- Visualize trends and performance metrics.
- Support data-driven monitoring and analysis.

### 🚨 Anomaly Detection
- Identify unusual patterns in KPI data.
- Apply anomaly detection techniques to highlight potential irregularities.
- Visualize detected anomalies to support further investigation.

### 🤖 Intelligent Assistant
- Explore data through a conversational interface.
- Use Gemini API integration for AI-powered assistance.
- Support natural-language questions about data, depending on the configured data sources and functionality.

### 🧹 Data Quality
- Explore data quality indicators and potential inconsistencies.
- Support data validation and quality analysis.

### 🔮 Predictive Modeling
- Compare machine learning models for KPI prediction.
- Evaluate model performance using metrics such as MAE, RMSE, and R².
- Support predictive analysis and model comparison.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Application | Streamlit |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly |
| Machine Learning | Scikit-learn |
| AI Integration | Gemini API |
| Development Tools | Git, GitHub |

## 📁 Project Structure

```text
smart-kpi-assistant/
├── Page_d_accueil.py
├── pages/
│   ├── 1_KPI_Overview.py
│   ├── 2_Anomaly_Detection.py
│   ├── 3_Assistant_intelligent.py
│   ├── 4_Data_Quality.py
│   └── 5_ML_Predictive_Modeling.py
├── assets/
│   └── logo-totalenergie.png
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Meryembenaammi/smart-kpi-assistant.git
cd smart-kpi-assistant
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

If your application uses the Gemini API, configure your API key securely. Do not commit API keys or passwords to GitHub.

For Streamlit secrets, create a local file at `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

Replace the placeholder with your own key. Keep this file private and excluded from Git.

Make sure the application reads the secret using the same variable name.

### 5. Run the application

```bash
streamlit run Page_d_accueil.py
```

Streamlit will provide a local URL in your terminal, usually:

```text
http://localhost:8501
```

## 📊 Use Cases

- KPI monitoring and business performance analysis.
- Exploratory analysis of operational data.
- Anomaly identification and investigation.
- Comparison of predictive models.
- AI-assisted data exploration.

## 🔐 Security

- Never publish API keys, passwords, access tokens, or confidential datasets.
- Keep `.env` and `.streamlit/secrets.toml` out of version control.
- Use anonymized or synthetic data when sharing demonstrations publicly.

## 🚀 Future Improvements

- Deploy the application to a cloud hosting platform.
- Add automated data ingestion and scheduled refreshes.
- Improve model monitoring and evaluation.
- Expand AI-assisted analytics and natural-language querying.
- Add automated testing and data quality checks.

## 👩‍💻 Author

**Meryem Ben-Aammi**

Data Engineering | Business Intelligence | Big Data & Artificial Intelligence

- GitHub: [@Meryembenaammi](https://github.com/Meryembenaammi)
- LinkedIn: [Connect with me](https://www.linkedin.com/)

---

<p align="center">
  <i>Turning data into insights through analytics, machine learning, and AI.</i>
</p>
