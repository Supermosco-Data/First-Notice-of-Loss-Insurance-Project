import streamlit as st
import pandas as pd
from overview import customer_overview
from visualization import (
    plot_claim_amount_histograms,
    plot_weather_traffic,
    plot_monthly_claim_trend,
    plot_claim_type_totals,
    plot_claim_type_means,
)
from prediction import fnol_prediction
from Retrain_machine import show_retraining_ui


st.markdown(
    """
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="font-weight: 700;">💼 FNOL Insurance Analytics</h1>
        <h4 style="margin-top: 0; font-weight: 500;">
            Claims Intelligence and First Notice of Loss Dashboard
        </h4>
    </div>
    """,
    unsafe_allow_html=True
)


st.set_page_config(
    page_title="FNOL Insurance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_claims_data():
    return pd.read_csv("Data\claims_policy_merged_cleaned.csv")


df_final = load_claims_data()

if "page" not in st.session_state:
    st.session_state.page = "overview"


st.sidebar.title("FNOL Dashboard")
st.sidebar.markdown("---")

if st.sidebar.button("Customer Claim Overview", use_container_width=True):
    st.session_state.page = "overview"

if st.sidebar.button("Visualizations", use_container_width=True):
    st.session_state.page = "visuals"

if st.sidebar.button("Prediction", use_container_width=True):
    st.session_state.page = "prediction"

if st.sidebar.button("Retraining", use_container_width=True):
    st.session_state.page = "retraining"



# Main page Router
if st.session_state.page == "overview":
    customer_overview(df_final)

elif st.session_state.page == "visuals":
    st.title("📈 Claim Visualizations")

    plot_claim_amount_histograms(df_final)
    plot_weather_traffic(df_final)
    plot_monthly_claim_trend(df_final)
    plot_claim_type_totals(df_final)
    plot_claim_type_means(df_final)

elif st.session_state.page == "prediction":
    fnol_prediction(df_final)

elif st.session_state.page == "retraining":
    show_retraining_ui()


