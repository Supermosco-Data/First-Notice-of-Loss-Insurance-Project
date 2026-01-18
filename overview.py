# overview.py

import streamlit as st
import pandas as pd


def customer_overview(df_final: pd.DataFrame):
    # --------------------------------------------------
    # Page Header
    # --------------------------------------------------
    st.title("📊 FNOL Customer & Claims Insights")

    st.markdown(
        """
        This dashboard provides a **high-level summary of insurance claims activity**
        derived from First Notice of Loss (FNOL) data.  
        It highlights claim severity, driver demographics, and environmental conditions
        associated with reported claims.
        """
    )

    # --------------------------------------------------
    # KPI SECTION
    # --------------------------------------------------
    st.subheader("📌 Claims Summary Metrics")

    kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)

    with kpi_1:
        st.metric(
            "Minimum Claim Cost",
            f"${df_final['Ultimate_Claim_Amount'].min():,.2f}"
        )

    with kpi_2:
        st.metric(
            "Maximum Claim Cost",
            f"${df_final['Ultimate_Claim_Amount'].max():,.2f}"
        )

    with kpi_3:
        st.metric(
            "Youngest Driver",
            f"{df_final['Driver_Age'].min()} yrs"
        )

    with kpi_4:
        st.metric(
            "Oldest Driver",
            f"{df_final['Driver_Age'].max()} yrs"
        )

    st.divider()

    # --------------------------------------------------
    # CLAIM CATEGORY ANALYSIS
    # --------------------------------------------------
    st.subheader("📂 Claim Category Breakdown")

    claim_summary = (
        df_final
        .groupby("Claim_Type")
        .agg(
            Estimated_Total=("Estimated_Claim_Amount", "sum"),
            Estimated_Average=("Estimated_Claim_Amount", "mean"),
            Number_of_Claims=("Estimated_Claim_Amount", "count"),
            Ultimate_Total=("Ultimate_Claim_Amount", "sum"),
            Ultimate_Average=("Ultimate_Claim_Amount", "mean")
        )
        .round(2)
        .reset_index()
    )

    st.dataframe(
        claim_summary,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # INSIGHT PANEL
    # --------------------------------------------------
    st.subheader("🔍 Key Observations")

    left, right = st.columns(2)

    highest_cost = claim_summary.loc[
        claim_summary["Ultimate_Total"].idxmax()
    ]
    lowest_cost = claim_summary.loc[
        claim_summary["Ultimate_Total"].idxmin()
    ]

    with left:
        st.info(
            f"""
            **Most Expensive Claim Type**  
            {highest_cost['Claim_Type']}  
            Total Cost: ${highest_cost['Ultimate_Total']:,.2f}
            """
        )

    with right:
        st.warning(
            f"""
            **Least Expensive Claim Type**  
            {lowest_cost['Claim_Type']}  
            Total Cost: ${lowest_cost['Ultimate_Total']:,.2f}
            """
        )

    st.success(
        f"✅ Total Claims Reviewed: {claim_summary['Number_of_Claims'].sum():,}"
    )

    st.divider()

    # --------------------------------------------------
    # ENVIRONMENTAL CONDITIONS
    # --------------------------------------------------
    st.subheader("🌦️ Driving Environment Overview")

    env_1, env_2 = st.columns(2)

    with env_1:
        st.markdown("**Traffic Conditions at Time of Claim**")
        traffic_df = (
            df_final["Traffic_Condition"]
            .value_counts()
            .reset_index()
            .rename(columns={
                "index": "Traffic Condition",
                "Traffic_Condition": "Occurrences"
            })
        )
        st.dataframe(
            traffic_df,
            use_container_width=True,
            hide_index=True
        )

    with env_2:
        st.markdown("**Weather Conditions at Time of Claim**")
        weather_df = (
            df_final["Weather_Condition"]
            .value_counts()
            .reset_index()
            .rename(columns={
                "index": "Weather Condition",
                "Weather_Condition": "Occurrences"
            })
        )
        st.dataframe(
            weather_df,
            use_container_width=True,
            hide_index=True
        )





