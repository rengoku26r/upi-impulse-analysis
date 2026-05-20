import streamlit as st
import pandas as pd
import os

import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

st.set_page_config(page_title="UPI Impulse Analysis", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "data", "processed", "combined_with_clusters.csv")
FIG_DIR = os.path.join(BASE_DIR, "..", "reports", "figures")

df = pd.read_csv(DATA_PATH)

if "respondent_id" in df.columns:
    df = df.drop("respondent_id", axis=1)

def load_plot(name):
    return os.path.join(FIG_DIR, name)

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Spending Behaviour", "Trigger Analysis", "ML Results"]
)

gender_filter = st.sidebar.multiselect(
    "Filter by Gender",
    df["gender"].dropna().unique()
)

if gender_filter:
    df = df[df["gender"].isin(gender_filter)]

year_filter = st.sidebar.multiselect(
    "Filter by College Year",
    df["college_year"].dropna().unique()
)

if year_filter:
    df = df[df["college_year"].isin(year_filter)]

if page == "Overview":
    st.title("UPI Impulse Spending Analysis")

    col1, col2, col3, col4 = st.columns(4)

    total = len(df)
    regret_pct = round(df["high_regret"].mean() * 100, 1)

    time_cols = {
        "flag_morning": "Morning",
        "flag_afternoon": "Afternoon",
        "flag_evening": "Evening",
        "flag_latenight": "Late Night",
        "flag_postmidnight": "Post Midnight"
    }

    top_time = max(time_cols, key=lambda x: df[x].mean())
    top_time = time_cols[top_time]

    cat_cols = [
        "cat_food_delivery","cat_grocery","cat_online_shopping",
        "cat_subscriptions","cat_gaming","cat_gadgets",
        "cat_offline_cafe","cat_other"
    ]

    top_cat = max(cat_cols, key=lambda x: df[x].sum())
    top_cat = top_cat.replace("cat_", "").replace("_", " ").title()

    col1.metric("Total Respondents", total)
    col2.metric("High Regret %", f"{regret_pct}%")
    col3.metric("Top Impulse Time", top_time)
    col4.metric("Top Regret Category", top_cat)

    st.markdown("Most users spend impulsively during evening and regret food-related purchases most frequently.")

    colA, colB = st.columns(2)

    with colA:
        st.image(load_plot("plot_01_demographics.png"), use_container_width=True)

    with colB:
        st.image(load_plot("plot_12_upi_distribution.png"), use_container_width=True)

elif page == "Spending Behaviour":
    st.title("Spending Behaviour")

    st.markdown("Majority users fall in mid-budget range and moderate transaction frequency.")

    c1, c2 = st.columns(2)

    with c1:
        st.image(load_plot("plot_02_budget_distribution.png"), use_container_width=True)
        st.image(load_plot("plot_04_impulse_time.png"), use_container_width=True)

    with c2:
        st.image(load_plot("plot_03_transaction_frequency.png"), use_container_width=True)
        st.image(load_plot("plot_05_unplanned_distribution.png"), use_container_width=True)

    st.image(load_plot("plot_06_regret_frequency.png"), use_container_width=True)

elif page == "Trigger Analysis":
    st.title("Trigger Analysis")

    st.markdown("Late night behaviour, emotional triggers and convenience play a key role in impulsive spending.")

    c1, c2 = st.columns(2)

    with c1:
        st.image(load_plot("plot_09_trigger_heatmap.png"), use_container_width=True)
        st.image(load_plot("plot_10_correlation_heatmap.png"), use_container_width=True)

    with c2:
        st.image(load_plot("plot_07_regret_categories.png"), use_container_width=True)
        st.image(load_plot("plot_14_wordcloud.png"), use_container_width=True)

    st.image(load_plot("plot_15_nlp_trigger_tags.png"), use_container_width=True)

elif page == "ML Results":
    st.title("Machine Learning Results")

    col1, col2 = st.columns(2)
    col1.metric("Model Accuracy", "0.62")
    col2.metric("F1 Score", "0.73")

    st.markdown("High impulsive spenders show strong late-night activity and poor financial control.")

    st.image(load_plot("plot_17_cluster_pca.png"), use_container_width=True)

    st.subheader("Cluster Profiles")

    numeric_df = df.select_dtypes(include="number")

    cluster_profile = df.groupby("cluster_name")[numeric_df.columns].mean().round(2)

    st.dataframe(cluster_profile, use_container_width=True)

    st.image(load_plot("plot_18_feature_importance.png"), use_container_width=True)