# visualization.py
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


def plot_claim_amount_histograms(df_final):
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))

    sns.histplot(data=df_final, x="Estimated_Claim_Amount", bins=30, kde=True, ax=axes[0, 0])
    axes[0, 0].set_title("Distribution of Estimated Claim Amount")
    axes[0, 0].set_xlabel("Estimated Claim Amount")

    sns.histplot( data=df_final, x="Ultimate_Claim_Amount", bins=20,kde=True, color="blue", ax=axes[0, 1])
    axes[0, 1].set_title("Distribution of Ultimate Claim Amount")
    axes[0, 1].set_xlabel("Ultimate Claim Amount")

    sns.histplot(data=df_final, x="Driver_Age", bins=30, kde=True, color="green", ax=axes[0, 2])
    axes[0, 2].set_title("Distribution of Driver Age")

    sns.histplot(data=df_final,x="Years_of_Experience",bins=30,kde=True,color="lightgreen",ax=axes[1, 0])
    axes[1, 0].set_title("Distribution of Years of Experience")
    axes[1, 0].set_xlabel("Years of Experience")

    sns.histplot(data=df_final,x="Fnol_Delay_Date",bins=30,kde=True,color="lightblue",ax=axes[1, 1])
    axes[1, 1].set_title("Distribution of FNOL Delay")
    axes[1, 1].set_xlabel("FNOL Delay")

    sns.histplot(data=df_final, x="Settlement_Duration",bins=30,kde=True,color="red",ax=axes[1, 2])
    axes[1, 2].set_title("Distribution of Settlement Duration")
    axes[1, 2].set_xlabel("Settlement Duration")

    plt.tight_layout()
    st.pyplot(fig)

# Weather and Traffic distribution
def plot_weather_traffic(df_final):
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))

    df_final["Weather_Condition"].value_counts().plot(kind="bar", ax=ax[0])
    ax[0].set_title("Weather Condition")
    ax[0].set_xlabel("Weather")
    ax[0].set_ylabel("Count")

    df_final["Traffic_Condition"].value_counts().plot(kind="bar", ax=ax[1])
    ax[1].set_title("Traffic Condition")
    ax[1].set_xlabel("Traffic")
    ax[1].set_ylabel("Count")
    st.pyplot(fig)

# Monrthly accident and claims trend
def plot_monthly_claim_trend(df_final):
    data = df_final.copy()

    data["Accident_Date"] = pd.to_datetime(
        data["Accident_Date"],
        errors="coerce"
    )

    data = data.dropna(subset=["Accident_Date"])

    data["Accident_YearMonth"] = (
        data["Accident_Date"].dt.strftime("%Y-%m")
    )

    monthly_claims = (
        data.groupby("Accident_YearMonth")
        .size()
    )

    fig, ax = plt.subplots(figsize=(20, 10))

    ax.plot(
        monthly_claims.index.astype(str),
        monthly_claims.values,
        marker="o",
        linewidth=1.5
    )

    ax.set_title("Monthly Trends Across the Years")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Claims")

    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

# Total claim amount by claim types
def plot_claim_type_totals(df_final):
    data = (
        df_final.groupby("Claim_Type")
        .agg(
            Estimated_Claim_Amount=("Estimated_Claim_Amount", "sum"),
            Ultimate_Claim_Amount=("Ultimate_Claim_Amount", "sum")
        )
        .sort_values("Ultimate_Claim_Amount", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(14, 5))
    data.plot(kind="bar", ax=ax)
    ax.set_title("Claim Amount by Claim Type")
    ax.set_xlabel("Claim Type")
    ax.set_ylabel("Amount")
    st.pyplot(fig)

# Average claim amount by claim types
def plot_claim_type_means(df_final):
    data = (
        df_final.groupby("Claim_Type")
        .agg(
            Estimated_Claim_Amount=("Estimated_Claim_Amount", "mean"),
            Ultimate_Claim_Amount=("Ultimate_Claim_Amount", "mean")
        )
        .sort_values("Ultimate_Claim_Amount", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(14, 5))
    data.plot(kind="bar", ax=ax)
    ax.set_title("Average Claim Amount by Claim Type")
    ax.set_xlabel("Claim Type")
    ax.set_ylabel("Amount")
    st.pyplot(fig)




