import streamlit as st
import pandas as pd
import numpy as np
from models import load_model


def fnol_prediction(df_final):
    st.title("🎰 FNOL Claim Preduction")
    st.markdown("### Predict ultimate amount based on incident details")

    kpi_1, kpi_2 = st.columns(2)

    with kpi_1:
        st.subheader("📟 Enter the Claim Details")

        with st.form("prediction_form"):
            kpi_1a, kpi_1b = st.columns(2)

            with kpi_1a:
                claim_type = st.selectbox(
                    "Claim Type",
                    options=df_final["Claim_Type"].unique()
                )

                estimated_claim = st.number_input(
                    "Estimated_Claim_Amount ($)",
                    min_value=0,
                    value=1500,
                    step=100
                )

                traffic_conditionm = st.selectbox(
                    "Traffic_Condition",
                    options=df_final["Traffic_Condition"].unique()
                )

                weather_condition = st.selectbox(
                    "Weather Condition",
                    options=df_final["Weather_Condition"].unique()
                )

            with kpi_1b:
                vehicle_type = st.selectbox(
                    "Vehicle_Type",
                    options=df_final["Vehicle_Type"].unique()
                )

                vehicle_year = st.number_input(
                    "Vehicle Year",
                    min_value=1900,
                    max_value=2024,
                    value=2022
                )

                driver_age = st.number_input(
                    "Driver Age",
                    min_value=18,
                    max_value=90,
                    value=30
                )

                license_age = st.number_input(
                    "Years of Experience",
                    min_value=0,
                    max_value=60,
                    value=10
                )

            predict_button = st.form_submit_button(
                "Predict Ultimate Claim Amount",
                use_container_width=True
            )


        with kpi_2:
            st.header("⬆️ Input Summary")
            st.info( f"""
            **Selected Parameter :**
               
            - Claim Type: {claim_type}
                
            -  Vehicle Type: {vehicle_type}  
                
            -  Traffic: {traffic_conditionm}  
            
            -  Weather: {weather_condition}  

            - Driver Age: {driver_age}  

            - Years of Experience: {license_age}  

            - Vehicle Year: {vehicle_year}  

            - Estimated Claim: ${estimated_claim:,.2f}
            """
        )


    if predict_button:
        st.markdown("---")
        st.subheader("📊 Prediction Results")

        try:
            model, feature_columns = load_model()

            input_data = pd.DataFrame({
                "Claim_Type": [str(claim_type)],
                "Estimated_Claim_Amount": [estimated_claim],
                "Traffic_Condition": [str(traffic_conditionm)],
                "Weather_Condition": [str(weather_condition)],
                "Vehicle_Type": [str(vehicle_type)],
                "Vehicle_Year": [vehicle_year],
                "Driver_Age": [driver_age],
                "Years_of_Experience": [license_age]
            })

            input_encoded = pd.get_dummies(input_data, drop_first=False)
            input_encoded = input_encoded.reindex(
                columns=feature_columns,
                fill_value=0
            )

            with st.spinner("Making prediction"):
                prediction = model.predict(input_encoded)
                predicted_amount = np.expm1(prediction[0])

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Estimated Claim Amount",
                    f"${estimated_claim:,.2f}"
                )

            with col2:
                st.metric(
                    "Predicted Ultimate Amount",
                    f"${predicted_amount:,.2f}",
                    f"${predicted_amount - estimated_claim:,.2f}"
                )

            with col3:
                variance = (
                    (predicted_amount - estimated_claim)
                    / estimated_claim
                ) * 100
                st.metric(
                    "Variance",
                    f"{variance:,.2f}%"
                )
            st.success("✅ Prediction completed successfully")

            if predicted_amount > estimated_claim:
                st.warning(
                    " :warning: Predicted amount is higher than the estimate"
                )
            else:
                st.info(
                    " :light bulb: Predicted amount is within or below the estimate"
                )

        except Exception as e:
            st.error(f":cross mark: Error making prediction: {e}")
            st.info(
                "Check that the model and feature columns load correctly"
            )



