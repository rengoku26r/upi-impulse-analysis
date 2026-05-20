import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from textblob import TextBlob
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
import re

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="UPI Impulse Trap v2",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #07111f;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

.block-container {
    padding-top: 2rem;
}

.hero-box {
    background: linear-gradient(135deg,#111827,#1e3a8a);
    padding: 35px;
    border-radius: 25px;
    border: 1px solid #334155;
    margin-bottom: 20px;
}

.metric-card {
    background: linear-gradient(135deg,#111827,#1e293b);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #334155;
    text-align: center;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.25);
}

.insight-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 18px;
    border-left: 5px solid #6366F1;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed",
    "combined_with_clusters.csv"
)

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

with st.spinner("Analyzing behavioral spending patterns..."):
    df = load_data()

# =========================================================
# CLEANUP
# =========================================================

if "respondent_id" in df.columns:
    df = df.drop("respondent_id", axis=1)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("💸 UPI Impulse Trap v2")

st.sidebar.markdown("""
Behavioral intelligence dashboard exploring:

- Interactive Plotly Analytics
- ML Risk Prediction
- Behavioral Personas
- NLP Wordcloud
- Financial Regret Analysis
""")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Overview",
        "Behavioral Analytics",
        "Trigger Intelligence",
        "Financial Risk",
        "Persona Segmentation",
        "NLP Insights",
        "Regret Risk Predictor",
    ]
)

st.sidebar.markdown("---")

gender_filter = st.sidebar.multiselect(
    "Gender",
    df["gender"].dropna().unique()
)

year_filter = st.sidebar.multiselect(
    "College Year",
    df["college_year"].dropna().unique()
)

if gender_filter:
    df = df[df["gender"].isin(gender_filter)]

if year_filter:
    df = df[df["college_year"].isin(year_filter)]

# =========================================================
# COMMON COLORS
# =========================================================

plot_bg = "#07111f"
paper_bg = "#07111f"

def style_fig(fig, title):

    fig.update_layout(
        title=title,
        title_x=0.5,
        template="plotly_dark",
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color="white"),
        height=500,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig

# =========================================================
# GLOBAL ML MODEL
# =========================================================

feature_cols = [
    "avg_weekly_tx",
    "pct_unplanned_avg",
    "impulse_composite_score",
    "regret_frequency",
    "balance_check_habit",
    "ran_out_of_money",
    "hidden_purchase"
]

model_df = df[
    feature_cols + ["high_regret"]
].dropna()

X = model_df[feature_cols]

y = model_df["high_regret"]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_scaled, y)

# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    st.markdown("""
    <div class="hero-box">
        <h1>💸 UPI Impulse Trap</h1>
        <p>
        Behavioral fingerprinting of impulsive digital spending and financial regret
        among Indian college students using ML + NLP.
        </p>
    </div>
    """, unsafe_allow_html=True)

    total_users = len(df)

    high_regret_pct = round(
        df["high_regret"].mean() * 100,
        1
    )

    avg_impulse = round(
        df["impulse_composite_score"].mean(),
        2
    )

    avg_tx = round(
        df["avg_weekly_tx"].mean(),
        1
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{total_users}</h2>
            <p>Total Respondents</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{high_regret_pct}%</h2>
            <p>High Regret Users</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{avg_impulse}</h2>
            <p>Impulse Score</p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{avg_tx}</h2>
            <p>Weekly Transactions</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 📊 Demographic Intelligence")

    col1, col2 = st.columns(2)

    with col1:

        gender_df = (
            df["gender"]
            .value_counts()
            .reset_index()
        )

        gender_df.columns = ["Gender", "Count"]

        fig = px.pie(
            gender_df,
            names="Gender",
            values="Count",
            hole=0.55
        )

        style_fig(fig, "Gender Distribution")

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        year_df = (
            df["college_year"]
            .value_counts()
            .reset_index()
        )

        year_df.columns = ["Year", "Count"]

        fig = px.bar(
            year_df,
            x="Year",
            y="Count",
            text_auto=True,
            color="Count"
        )

        style_fig(fig, "College Year Distribution")

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("## 📱 UPI App Ecosystem")

    upi_df = (
        df["primary_upi_app"]
        .value_counts()
        .reset_index()
    )

    upi_df.columns = ["UPI App", "Users"]

    fig = px.bar(
        upi_df,
        x="UPI App",
        y="Users",
        color="Users",
        text_auto=True
    )

    style_fig(
        fig,
        "Most Used UPI Applications"
    )

    fig.update_layout(
        xaxis_title="UPI Application",
        yaxis_title="Number of Users"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    top_app = upi_df.iloc[0]["UPI App"]

    st.markdown(f"""
    <div class="insight-box">

    <b>Key Insight:</b>

    {top_app} appears to dominate student digital transactions,
    suggesting strong platform preference and ecosystem dependence
    among respondents.

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    <b>Key Insight:</b> Majority of students experience impulsive UPI spending
    during evening and late-night hours, with food delivery emerging as the
    highest regret category.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# BEHAVIORAL ANALYTICS
# =========================================================

elif page == "Behavioral Analytics":

    st.title("🧠 Behavioral Analytics")

    time_cols = {
        "flag_morning": "Morning",
        "flag_afternoon": "Afternoon",
        "flag_evening": "Evening",
        "flag_latenight": "Late Night",
        "flag_postmidnight": "Post Midnight"
    }

    time_df = pd.DataFrame({
        "Time": list(time_cols.values()),
        "Count": [df[col].sum() for col in time_cols.keys()]
    })

    fig = px.bar(
        time_df,
        x="Count",
        y="Time",
        orientation="h",
        color="Count",
        text_auto=True
    )

    style_fig(fig, "Impulse Purchase Timing")

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            df,
            x="avg_weekly_tx",
            nbins=15
        )

        style_fig(fig, "Weekly Transaction Distribution")

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.histogram(
            df,
            x="pct_unplanned_avg",
            nbins=10
        )

        style_fig(fig, "Unplanned Purchase Distribution")

        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TRIGGER INTELLIGENCE
# =========================================================

elif page == "Trigger Intelligence":

    st.title("🔥 Trigger Intelligence")

    trigger_cols = {
        "trigger_boredom": "Boredom",
        "trigger_fomo": "FOMO",
        "trigger_latenight": "Late Night",
        "trigger_cashback": "Cashback",
        "trigger_stress_relief": "Stress Relief",
        "trigger_scarcity_notif": "Scarcity",
        "trigger_cart_abandon": "Cart Reminder",
        "trigger_exam_season": "Exam Stress"
    }

    trigger_df = pd.DataFrame({
        "Trigger": list(trigger_cols.values()),
        "Average Score": [
            df[col].mean()
            for col in trigger_cols.keys()
        ]
    })

    fig = px.bar(
        trigger_df,
        x="Average Score",
        y="Trigger",
        orientation="h",
        color="Average Score",
        text_auto=".2f"
    )

    style_fig(fig, "Behavioral Trigger Scores")

    st.plotly_chart(fig, use_container_width=True)

    corr_cols = [
        "avg_weekly_tx",
        "pct_unplanned_avg",
        "impulse_composite_score",
        "regret_frequency",
        "regret_intensity"
    ]

    corr = df[corr_cols].corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto"
    )

    style_fig(fig, "Behavioral Correlation Matrix")

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# FINANCIAL RISK
# =========================================================

elif page == "Financial Risk":

    st.title("⚠️ Financial Risk Intelligence")

    risk_df = (
        df["high_regret"]
        .map({
            0: "Low Risk",
            1: "High Risk"
        })
        .value_counts()
        .reset_index()
    )

    risk_df.columns = ["Risk", "Count"]

    fig = px.pie(
        risk_df,
        names="Risk",
        values="Count",
        hole=0.6
    )

    style_fig(fig, "Financial Regret Risk Distribution")

    st.plotly_chart(fig, use_container_width=True)

    fig = px.box(
        df,
        x="high_regret",
        y="avg_weekly_tx",
        color="high_regret"
    )

    style_fig(fig, "Weekly Transactions vs Regret Risk")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## 🧠 Most Important Risk Factors")

    importance_df = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": model.feature_importances_
    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=True
    )

    fig = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        text_auto=".3f",
        color="Importance"
    )

    style_fig(
        fig,
        "Random Forest Feature Importance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("""
    <div class="insight-box">
    <b>Interpretation:</b>

    Features with higher importance contribute more strongly to predicting
    high financial regret. Impulse score, unplanned spending percentage,
    and financial stress indicators dominate the model.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# PERSONA SEGMENTATION
# =========================================================

elif page == "Persona Segmentation":

    st.title("🧬 Persona Segmentation")

    cluster_df = (
        df["cluster_name"]
        .value_counts()
        .reset_index()
    )

    cluster_df.columns = ["Cluster", "Count"]

    fig = px.treemap(
        cluster_df,
        path=["Cluster"],
        values="Count",
        color="Count"
    )

    style_fig(fig, "Behavioral Personas")

    st.plotly_chart(fig, use_container_width=True)

    numeric_df = df.select_dtypes(include="number")

    cluster_profile = (
        df.groupby("cluster_name")[numeric_df.columns]
        .mean()
        .round(2)
    )

    st.dataframe(
        cluster_profile,
        use_container_width=True
    )

# =========================================================
# NLP INSIGHTS
# =========================================================

elif page == "NLP Insights":

    st.title("📝 NLP Insights")

    if "regret_description" in df.columns:

        text_df = df[
            df["regret_description"].notna()
        ]

        st.metric(
            "Total Text Responses",
            len(text_df)
        )

        combined_text = " ".join(
            text_df["regret_description"]
            .astype(str)
            .tolist()
        )

        if len(combined_text) > 10:

            wordcloud = WordCloud(
                width=1200,
                height=600,
                background_color="black",
                colormap="viridis"
            ).generate(combined_text)

            fig, ax = plt.subplots(figsize=(15, 7))

            ax.imshow(wordcloud, interpolation="bilinear")

            ax.axis("off")

            st.pyplot(fig)

            stop_words = set(stopwords.words("english"))

            custom_stopwords = {
                "upi",
                "purchase",
                "money",
                "buy",
                "bought",
                "spent",
                "spending"
            }

            stop_words.update(custom_stopwords)

            clean_words = re.findall(
                r'\b[a-zA-Z]{3,}\b',
                combined_text.lower()
            )
            filtered_words = [
                word
                for word in clean_words
                if word not in stop_words
            ]

            common_words = Counter(clean_words).most_common(5)

            word_df = pd.DataFrame(
                common_words,
                columns=["Word", "Frequency"]
            )

            st.markdown("## 🔥 Most Common Regret Words")

            st.dataframe(
                word_df,
                use_container_width=True
            )

            st.markdown("""
            <div class="insight-box">

            <b>Interpretation:</b>

            Frequently occurring words represent dominant regret themes
            among students. Terms related to food delivery, stress,
            boredom, and online shopping appear repeatedly.

            </div>
            """, unsafe_allow_html=True)

        else:

            st.warning(
                "Not enough text responses available."
            )

    else:

        st.error(
            "regret_description column not found."
        )

# =========================================================
# REGRET RISK PREDICTOR
# =========================================================

elif page == "Regret Risk Predictor":

    st.title("🤖 Financial Regret Predictor")

    st.markdown("### Enter User Behavioral Features")

    avg_tx = st.slider(
        "Weekly Transactions",
        1,
        40,
        10
    )

    unplanned = st.slider(
        "Unplanned Purchase %",
        0,
        100,
        40
    )

    impulse = st.slider(
        "Impulse Score",
        1.0,
        5.0,
        2.0
    )

    regret_freq = st.slider(
        "Regret Frequency",
        0,
        4,
        1
    )

    balance = st.slider(
        "Balance Checking Habit",
        0,
        3,
        2
    )

    money = st.slider(
        "Ran Out of Money",
        0,
        3,
        1
    )

    hidden = st.slider(
        "Hidden Purchases",
        0,
        2,
        0
    )

    if st.button("Predict Financial Risk"):

        sample = np.array([[
            avg_tx,
            unplanned,
            impulse,
            regret_freq,
            balance,
            money,
            hidden
        ]])

        sample_scaled = scaler.transform(sample)

        pred = model.predict(sample_scaled)[0]

        prob = model.predict_proba(sample_scaled)[0][1]

        if pred == 1:

            st.error(
                f"⚠️ High Financial Regret Risk ({round(prob*100,1)}%)"
            )

        else:

            st.success(
                f"✅ Low Financial Regret Risk ({round((1-prob)*100,1)}%)"
            )

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                title={"text": "Regret Risk Score"},
                gauge={
                    "axis": {"range": [0, 100]}
                }
            )
        )

        style_fig(fig, "ML Risk Prediction")

        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption("""
UPI Impulse Trap v2 • Behavioral Analytics Dashboard
""")

st.caption("""
Built with Streamlit + Plotly + NLP + Machine Learning
""")

st.caption("""
Developed by Rajnish • IIT Bhilai • DSAI
""")