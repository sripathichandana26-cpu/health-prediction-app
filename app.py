import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
import database
from gemini_helper import generate_health_remark

database.create_table()

st.set_page_config(
    page_title="Health Prediction App",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Health Prediction Application")

st.write("Enter patient details and predict health risk.")

with st.form("patient_form"):

    full_name = st.text_input("Full Name")

    dob = st.date_input(
        "Date of Birth",
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )

    email = st.text_input("Email Address")

    glucose = st.number_input(
        "Glucose",
        min_value=0.0,
        step=0.1
    )

    haemoglobin = st.number_input(
        "Haemoglobin",
        min_value=0.0,
        step=0.1
    )

    cholesterol = st.number_input(
        "Cholesterol",
        min_value=0.0,
        step=0.1
    )

    submit = st.form_submit_button("Predict & Save")

if submit:

    if not full_name.strip():
        st.error("Please enter Full Name")

    elif "@" not in email:
        st.error("Please enter a valid Email Address")

    else:

        risk_score = 0

        if glucose > 180:
            risk_score += 2
        elif glucose > 120:
            risk_score += 1

        if cholesterol > 240:
            risk_score += 2
        elif cholesterol > 200:
            risk_score += 1

        if haemoglobin < 12:
            risk_score += 1

        if risk_score >= 4:
            risk = "High Risk"

        elif risk_score >= 2:
            risk = "Medium Risk"

        else:
            risk = "Low Risk"

        remarks = generate_health_remark(
            glucose,
            haemoglobin,
            cholesterol,
            risk
        )

        database.add_patient(
            full_name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        )

        st.success("Patient data saved successfully!")

        st.info(remarks)

st.divider()

st.subheader("📋 Saved Patient Records")

conn = sqlite3.connect("patients.db")

query = """
SELECT
id,
full_name,
dob,
email,
glucose,
haemoglobin,
cholesterol,
remarks
FROM patients
"""

df = pd.read_sql_query(query, conn)

conn.close()

st.dataframe(df, use_container_width=True)

st.divider()

st.subheader("📊 Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Patients", len(df))

with col2:
    high_risk_count = len(
        df[df["remarks"].str.contains("high", case=False, na=False)]
    ) if not df.empty else 0

    st.metric(
        "High Risk Patients",
        high_risk_count
    )

with col3:
    st.metric(
        "Total Records",
        len(df)
    )