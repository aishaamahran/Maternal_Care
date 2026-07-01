import streamlit as st
import pandas as pd
import joblib
from utils.components import (
    set_page,
    render_navbar,
    render_footer,
    section_header,
    step_pills,
    risk_result_card,
)

# -----------------------------
# Load Model  (unchanged)
# -----------------------------
model = joblib.load("models/maternal_risk_model.pkl")

set_page("Risk Prediction", "📊")
render_navbar(active="Prediction")

section_header(
    "AI Risk Prediction",
    "Pregnancy Risk Prediction",
    "Walk through four quick steps. Your information stays on this session "
    "and is only used to generate the prediction below.",
)

STEPS = ["Personal", "Medical", "Lifestyle", "Result"]

# -----------------------------
# Wizard state
# -----------------------------
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 0

defaults = {
    "age": 25, "gravidity": 1, "parity": 0, "gestational_age": 20,
    "bmi": 24.5, "systolic": 120, "diastolic": 80, "hemoglobin": 12.0,
    "glucose": 90, "anc": 4, "proteinuria": 0, "hiv": 0, "anemia": 0,
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

step_pills(STEPS, st.session_state.wizard_step)


def go_next():
    st.session_state.wizard_step = min(st.session_state.wizard_step + 1, len(STEPS) - 1)


def go_back():
    st.session_state.wizard_step = max(st.session_state.wizard_step - 1, 0)


# -----------------------------
# STEP 0 — Personal Information
# -----------------------------
if st.session_state.wizard_step == 0:
    with st.container(key="glass_step"):
        st.markdown("#### 👤 Personal Information")
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.age = st.number_input(
                "Age (Years)", 15, 60, st.session_state.age
            )
            st.session_state.gravidity = st.number_input(
                "Gravidity", 1, 15, st.session_state.gravidity
            )
        with c2:
            st.session_state.parity = st.number_input(
                "Parity", 0, 10, st.session_state.parity
            )
            st.session_state.gestational_age = st.number_input(
                "Gestational Age (Weeks)", 1, 40, st.session_state.gestational_age
            )

    nav_l, nav_r = st.columns([5, 1])
    with nav_r:
        st.button("Next →", on_click=go_next, use_container_width=True)

# -----------------------------
# STEP 1 — Medical Information
# -----------------------------
elif st.session_state.wizard_step == 1:
    with st.container(key="glass_step"):
        st.markdown("#### 🩺 Medical Information")
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.bmi = st.number_input(
                "BMI", 10.0, 50.0, st.session_state.bmi
            )
            st.session_state.systolic = st.number_input(
                "Systolic BP", 70, 220, st.session_state.systolic
            )
            st.session_state.diastolic = st.number_input(
                "Diastolic BP", 40, 150, st.session_state.diastolic
            )
        with c2:
            st.session_state.hemoglobin = st.number_input(
                "Hemoglobin", 5.0, 20.0, st.session_state.hemoglobin
            )
            st.session_state.glucose = st.number_input(
                "Fasting Glucose", 50, 250, st.session_state.glucose
            )
            st.session_state.anc = st.number_input(
                "ANC Visits", 0, 20, st.session_state.anc
            )

        bp_diff = st.session_state.systolic - st.session_state.diastolic
        st.info(f"Blood Pressure Difference : {bp_diff}")

    nav_l, nav_back, nav_next = st.columns([4, 1, 1])
    with nav_back:
        with st.container(key="ghostbtn3"):
            st.button("← Back", on_click=go_back, use_container_width=True)
    with nav_next:
        st.button("Next →", on_click=go_next, use_container_width=True)

# -----------------------------
# STEP 2 — Lifestyle / Lab Flags
# -----------------------------
elif st.session_state.wizard_step == 2:
    with st.container(key="glass_step"):
        st.markdown("#### 🧬 Lifestyle & Lab Flags")
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.proteinuria = st.selectbox(
                "Proteinuria", [0, 1],
                index=[0, 1].index(st.session_state.proteinuria),
            )
            st.session_state.hiv = st.selectbox(
                "HIV Status", [0, 1],
                index=[0, 1].index(st.session_state.hiv),
            )
        with c2:
            st.session_state.anemia = st.selectbox(
                "Anemia Status", [0, 1, 2, 3],
                index=[0, 1, 2, 3].index(st.session_state.anemia),
                format_func=lambda x: {
                    0: "None", 1: "Mild", 2: "Moderate", 3: "Severe"
                }[x],
            )

    nav_l, nav_back, nav_next = st.columns([4, 1, 1])
    with nav_back:
        with st.container(key="ghostbtn4"):
            st.button("← Back", on_click=go_back, use_container_width=True)
    with nav_next:
        st.button("Predict Risk →", on_click=go_next, use_container_width=True)

# -----------------------------
# STEP 3 — Prediction Result
# -----------------------------
else:
    age = st.session_state.age
    gravidity = st.session_state.gravidity
    parity = st.session_state.parity
    gestational_age = st.session_state.gestational_age
    bmi = st.session_state.bmi
    systolic = st.session_state.systolic
    diastolic = st.session_state.diastolic
    hemoglobin = st.session_state.hemoglobin
    glucose = st.session_state.glucose
    anc = st.session_state.anc
    proteinuria = st.session_state.proteinuria
    hiv = st.session_state.hiv
    anemia = st.session_state.anemia
    bp_diff = systolic - diastolic

    # -----------------------------
    # Prediction  (identical logic/columns to the original app)
    # -----------------------------
    input_data = pd.DataFrame([{
        "age_years": age,
        "gravidity": gravidity,
        "parity": parity,
        "gestational_age_weeks": gestational_age,
        "bmi_pre_pregnancy": bmi,
        "systolic_bp_mmhg": systolic,
        "diastolic_bp_mmhg": diastolic,
        "hemoglobin_gdl": hemoglobin,
        "anemia_status": anemia,
        "fasting_glucose_mgdl": glucose,
        "proteinuria": proteinuria,
        "hiv_status": hiv,
        "anc_visits": anc,
        "bp_diff": bp_diff
    }])

    prediction = model.predict(input_data)[0]

    # Confidence score is purely additive — derived from predict_proba
    # when available. It does not influence the predicted class.
    confidence = None
    try:
        proba = model.predict_proba(input_data)[0]
        confidence = float(proba[prediction]) * 100
    except Exception:
        confidence = None

    risk = {
        0: "🟢 Low Risk",
        1: "🟡 Moderate Risk",
        2: "🔴 High Risk"
    }
    level_key = {0: "low", 1: "medium", 2: "high"}[prediction]

    with st.container(key="glass_step"):
        st.markdown("#### 📋 Prediction Result")

        risk_result_card(
            level=level_key,
            confidence=confidence,
            title=risk[prediction],
            sub="Based on the personal, medical, and lifestyle information you entered.",
        )

        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

        if prediction == 0:
            st.success("""
Continue routine prenatal visits.

Maintain healthy nutrition.

Exercise regularly.

Drink enough water.
""")

        elif prediction == 1:
            st.warning("""
Increase prenatal monitoring.

Track blood pressure.

Follow medical advice.

Maintain healthy weight.
""")

        else:
            st.error("""
Seek immediate medical care.

Monitor blood pressure daily.

Attend all prenatal appointments.

Follow physician recommendations.
""")

    nav_back, nav_restart = st.columns([1, 1])
    with nav_back:
        with st.container(key="ghostbtn5"):
            st.button("← Edit Information", on_click=go_back, use_container_width=True)
    with nav_restart:
        if st.button("Start Over", use_container_width=True):
            st.session_state.wizard_step = 0
            st.rerun()

render_footer()
