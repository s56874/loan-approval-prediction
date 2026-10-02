import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("model/loan_approval_xgboost.pkl")

# Page
st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦"
)

st.title("🏦 Loan Approval Prediction")
st.write("Enter applicant details below.")

# Inputs
no_of_dependents = st.number_input(
    "Number of Dependents", 0, 10, 2
)

education = st.selectbox(
    "Education",
    ["Graduate", "Not Graduate"]
)

self_employed = st.selectbox(
    "Self Employed",
    ["Yes", "No"]
)

income_annum = st.number_input(
    "Annual Income", min_value=0, value=500000
)

loan_amount = st.number_input(
    "Loan Amount", min_value=0, value=1000000
)

loan_term = st.number_input(
    "Loan Term (Months)", min_value=1, value=12
)

cibil_score = st.number_input(
    "CIBIL Score",
    min_value=300,
    max_value=900,
    value=700
)

residential_assets_value = st.number_input(
    "Residential Assets Value",
    min_value=0,
    value=1000000
)

commercial_assets_value = st.number_input(
    "Commercial Assets Value",
    min_value=0,
    value=500000
)

luxury_assets_value = st.number_input(
    "Luxury Assets Value",
    min_value=0,
    value=500000
)

bank_asset_value = st.number_input(
    "Bank Asset Value",
    min_value=0,
    value=500000
)


# Prediction
if st.button("Predict Loan Status"):

    # Feature engineering
    total_assets_value = (
        residential_assets_value
        + commercial_assets_value
        + luxury_assets_value
        + bank_asset_value
    )

    loan_to_income_ratio = (
        loan_amount / income_annum
        if income_annum > 0 else 0
    )

    # Create input
    data = pd.DataFrame({
        "no_of_dependents": [no_of_dependents],
        "education": [education],
        "self_employed": [self_employed],
        "income_annum": [income_annum],
        "loan_amount": [loan_amount],
        "loan_term": [loan_term],
        "cibil_score": [cibil_score],
        "residential_assets_value": [residential_assets_value],
        "commercial_assets_value": [commercial_assets_value],
        "luxury_assets_value": [luxury_assets_value],
        "bank_asset_value": [bank_asset_value],
        "total_assets_value": [total_assets_value],
        "loan_to_income_ratio": [loan_to_income_ratio]
    })

    # Prediction
    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0]

    # Result
    if prediction == 0:

        st.success("✅ Loan Approved")

        st.image("screenshots/approved.png", width=250)

        st.write(
            f"Approval Probability: **{probability[0] * 100:.2f}%**"
        )

    else:

        st.error("❌ Loan Rejected")

        st.image("screenshots/rejected.png", width=250)

        st.write(
            f"Rejection Probability: **{probability[1] * 100:.2f}%**"
        )
