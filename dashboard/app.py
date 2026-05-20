import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

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
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed",
    "combined_with_clusters.csv"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    if "respondent_id" in df.columns:
        df = df.drop("respondent_id", axis=1)

    return df

df = load_data()

# =========================================================
# THEME + CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #07111f;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    .metric-card {
        background: linear-gradient(135deg,#111827,#1e293b);
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #334155;
        text-align:center;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.2);
    }

    .hero {
        background: linear-gradient(135deg,#111827,#1e3a8a);
        padding: 35px;
        border-radius: 25px;
        margin-bottom: 20px;
        border: 1px solid #334155;
    }

    .small-text {
        color: #94a3b8;
        font-size: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("💸 UPI Impulse Trap v2")

st.sidebar.markdown(
    """
Behavioral analytics dashboard exploring:

- Impulsive UPI spending
- Financial regret
- Psychological triggers
- ML-based personas
"""
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Behavioral Analytics",
        "Trigger Intelligence",
        "Financial Risk",
        "Persona Segmentation",
        "NLP Intelligence"
    ]
)

# =========================================================
# FILTERS
# =========================================================

st.sidebar.markdown("---")

gender_filter = st.sidebar.multiselect(
    "Gender",
    df["gender"].dropna().unique()
)

year_filter = st.sidebar.multiselect(
    "College Year",
    df["college_year"].dropna().unique()
)

income_filter = st.sidebar.multiselect(
    "Income Source",
    df["income_source"].dropna().unique()
)

if gender_filter:
    df = df[df["gender"].isin(gender_filter)]

if year_filter:
    df = df[df["college_year"].isin(year_filter)]

if income_filter:
    df = df[df["income_source"].isin(income_filter)]

# =========================================================
# KPI VALUES
# =========================================================

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

# =========================================================
# COMMON CHART CONFIG
# =========================================================

plot_bg = "#07111f"
paper_bg = "#07111f"
font_color = "white"

def update_layout(fig):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font=dict(color=font_color),
        margin=dict(l=20, r=20, t=60, b=20),
        title_x=0.5,
        height=500
    )

    return fig

# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    st.markdown(
        """
        <div class="hero">
            <h1>💸 UPI Impulse Trap</h1>
            <p class="small-text">
            Behavioral fingerprinting of impulsive digital spending patterns
            and financial regret among Indian college students.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>{total_users}</h3>
                <p>Total Respondents</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>{high_regret_pct}%</h3>
                <p>High Regret Users</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>{avg_impulse}</h3>
                <p>Impulse Score</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>{avg_tx}</h3>
                <p>Weekly Transactions</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 📊 Demographic Landscape")

    col1, col2 = st.columns(2)

    with col1:

        gender_data = (
            df["gender"]
            .value_counts()
            .reset_index()
        )

        gender_data.columns = ["Gender", "Count"]

        fig = px.pie(
            gender_data,
            names="Gender",
            values="Count",
            hole=0.6
        )

        update_layout(fig)

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        year_data = (
            df["college_year"]
            .value_counts()
            .reset_index()
        )

        year_data.columns = ["Year", "Count"]

        fig = px.bar(
            year_data,
            x="Year",
            y="Count",
            text_auto=True
        )

        update_layout(fig)

        st.plotly_chart(fig, use_container_width=True)

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
        "Count": [
            df[col].sum()
            for col in time_cols.keys()
        ]
    })

    fig = px.bar(
        time_df,
        x="Count",
        y="Time",
        orientation="h",
        text_auto=True,
        color="Count"
    )

    update_layout(fig)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## 💳 Spending Pattern")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            df,
            x="avg_weekly_tx",
            nbins=20
        )

        update_layout(fig)

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.histogram(
            df,
            x="pct_unplanned_avg",
            nbins=10
        )

        update_layout(fig)

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
        "Score": [
            df[col].mean()
            for col in trigger_cols.keys()
        ]
    })

    trigger_df = trigger_df.sort_values(
        by="Score",
        ascending=True
    )

    fig = px.bar(
        trigger_df,
        x="Score",
        y="Trigger",
        orientation="h",
        text_auto=".2f",
        color="Score"
    )

    update_layout(fig)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## 📈 Behavioral Correlation Matrix")

    corr_cols = [
        "avg_weekly_tx",
        "pct_unplanned_avg",
        "impulse_composite_score",
        "regret_frequency",
        "regret_intensity",
        "balance_check_habit",
        "ran_out_of_money",
        "hidden_purchase"
    ]

    corr = df[corr_cols].corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto"
    )

    update_layout(fig)

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# FINANCIAL RISK
# =========================================================

elif page == "Financial Risk":

    st.title("⚠️ Financial Risk Intelligence")

    col1, col2 = st.columns(2)

    with col1:

        regret_counts = (
            df["high_regret"]
            .map({
                0: "Low Regret",
                1: "High Regret"
            })
            .value_counts()
            .reset_index()
        )

        regret_counts.columns = ["Group", "Count"]

        fig = px.pie(
            regret_counts,
            names="Group",
            values="Count",
            hole=0.55
        )

        update_layout(fig)

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.box(
            df,
            x="high_regret",
            y="avg_weekly_tx",
            color="high_regret"
        )

        update_layout(fig)

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("## 📊 Regret Intensity Distribution")

    fig = px.histogram(
        df,
        x="regret_intensity",
        nbins=10,
        color="high_regret"
    )

    update_layout(fig)

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# PERSONA SEGMENTATION
# =========================================================

elif page == "Persona Segmentation":

    st.title("🧬 Persona Segmentation")

    if "cluster_name" in df.columns:

        cluster_counts = (
            df["cluster_name"]
            .value_counts()
            .reset_index()
        )

        cluster_counts.columns = ["Cluster", "Count"]

        fig = px.treemap(
            cluster_counts,
            path=["Cluster"],
            values="Count",
            color="Count"
        )

        update_layout(fig)

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("## 📌 Cluster Profile")

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

        compare_col = st.selectbox(
            "Compare Feature",
            [
                "avg_weekly_tx",
                "impulse_composite_score",
                "regret_intensity",
                "pct_unplanned_avg"
            ]
        )

        compare_df = (
            df.groupby("cluster_name")[compare_col]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            compare_df,
            x="cluster_name",
            y=compare_col,
            color="cluster_name",
            text_auto=".2f"
        )

        update_layout(fig)

        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# NLP INTELLIGENCE
# =========================================================

elif page == "NLP Intelligence":

    st.title("📝 NLP Intelligence")

    if "regret_description" in df.columns:

        text_df = df[
            df["regret_description"].notna()
        ]

        st.metric(
            "Total Text Responses",
            len(text_df)
        )

        if len(text_df) > 0:

            sample_text = np.random.choice(
                text_df["regret_description"]
            )

            st.markdown("## 💬 Random Regret Description")

            st.info(sample_text)

    st.markdown("## 🧠 NLP Insights")

    st.success(
        """
        Key patterns discovered from text analysis:

        • Food delivery dominates regret narratives  
        • Stress and boredom are dominant emotional triggers  
        • Late-night purchases show strongest regret association  
        • Emotional spending > social pressure spending  
        """
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "UPI Impulse Trap v2 • Built with Streamlit + Plotly + ML + NLP"
)

st.caption(
    "Developed by Rajnish • IIT Bhilai • DSAI"
)