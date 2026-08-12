import streamlit as st
import pandas as pd
import joblib

from src.assistant.gemini_handler import generate_risk_explanation


st.set_page_config(
    page_title="BC Academic Risk Assistant",
    page_icon="🎓",
    layout="wide"
)


# Load model files
model = joblib.load("models/trained_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")


st.title("🎓 BC Student Academic Risk Assistant")

st.write(
    "Enter a student's academic information below to generate "
    "an academic risk prediction and explanation."
)

st.info(
    "This system is a decision-support tool only and does not make "
    "final academic decisions."
)


st.subheader("Student Information")

col1, col2 = st.columns(2)


with col1:
    age = st.number_input(
        "Age",
        min_value=17,
        max_value=28,
        value=21,
        step=1
    )

    gender = st.selectbox(
        "Gender",
        [
            "Female",
            "Male",
            "Non-binary",
            "Prefer not to say"
        ]
    )

    programme = st.selectbox(
        "Programme",
        [
            "Bachelor of Information Technology",
            "Bachelor of Computing",
            "Diploma in Information Technology",
            "Higher Certificate in Information Systems"
        ]
    )


specialisation_options = {
    "Bachelor of Information Technology": [
        "Software Development",
        "Data Science",
        "Cloud Computing",
        "Cybersecurity",
        "Network Engineering"
    ],
    "Bachelor of Computing": [
        "Software Engineering",
        "Artificial Intelligence"
    ],
    "Diploma in Information Technology": [
        "Network Engineering",
        "Software Development",
        "Cybersecurity"
    ],
    "Higher Certificate in Information Systems": [
        "Information Systems",
        "End-User Computing",
        "Systems Support"
    ]
}


with col2:
    specialisation = st.selectbox(
        "Specialisation",
        specialisation_options[programme]
    )

    year_of_study = st.selectbox(
        "Year of Study",
        [
            "First Year",
            "Second Year",
            "Third Year",
            "Fourth Year"
        ]
    )

    registered_modules = st.number_input(
        "Registered Modules",
        min_value=1,
        max_value=10,
        value=6,
        step=1
    )


st.subheader("Academic Performance")

col3, col4 = st.columns(2)


with col3:
    attendance = st.number_input(
        "Attendance (%)",
        min_value=0,
        max_value=100,
        value=75,
        step=1
    )

    assignment_completion = st.number_input(
        "Assignment Completion (%)",
        min_value=0,
        max_value=100,
        value=75,
        step=1
    )

    bc_connect_activity = st.number_input(
        "BC Connect Activity",
        min_value=0,
        value=50,
        step=1
    )

    missed_assessments = st.number_input(
        "Missed Assessments",
        min_value=0,
        value=0,
        step=1
    )

    failed_modules = st.number_input(
        "Failed Modules",
        min_value=0,
        value=0,
        step=1
    )


with col4:
    overall_average = st.number_input(
        "Overall Average (%)",
        min_value=0,
        max_value=100,
        value=65,
        step=1
    )

    midyear_average = st.number_input(
        "Midyear Average (%)",
        min_value=0,
        max_value=100,
        value=65,
        step=1
    )

    test_average = st.number_input(
        "Test Average (%)",
        min_value=0,
        max_value=100,
        value=65,
        step=1
    )

    assignment_average = st.number_input(
        "Assignment Average (%)",
        min_value=0,
        max_value=100,
        value=65,
        step=1
    )

    practical_average = st.number_input(
        "Practical Average (%)",
        min_value=0,
        max_value=100,
        value=65,
        step=1
    )


passed_modules = st.number_input(
    "Passed Modules",
    min_value=0,
    max_value=int(registered_modules),
    value=min(4, int(registered_modules)),
    step=1
)


st.subheader("Ask the Assistant")

user_question = st.text_area(
    "Question",
    value="Why is this student considered at risk?"
)


if st.button("Analyse Student", type="primary"):

    student_data = {
        "age": age,
        "gender": gender,
        "programme": programme,
        "specialisation": specialisation,
        "year_of_study": year_of_study,
        "attendance": attendance,
        "assignment_completion": assignment_completion,
        "bc_connect_activity": bc_connect_activity,
        "missed_assessments": missed_assessments,
        "overall_average": overall_average,
        "midyear_average": midyear_average,
        "test_average": test_average,
        "assignment_average": assignment_average,
        "practical_average": practical_average,
        "failed_modules": failed_modules,
        "registered_modules": registered_modules,
        "passed_modules": passed_modules
    }

    student_df = pd.DataFrame([student_data])

    prediction_encoded = model.predict(student_df)

    prediction_label = label_encoder.inverse_transform(
        prediction_encoded
    )[0]

    st.subheader("Prediction")

    if prediction_label == "High":
        st.error(f"Academic Risk: {prediction_label}")

    elif prediction_label == "Medium":
        st.warning(f"Academic Risk: {prediction_label}")

    else:
        st.success(f"Academic Risk: {prediction_label}")

    with st.spinner("Generating explanation..."):
        explanation = generate_risk_explanation(
            student_data=student_data,
            risk_label=prediction_label,
            user_question=user_question
        )

    st.subheader("AI Explanation")

    st.write(explanation)

    st.caption(
        "This prediction is an early-warning indicator intended "
        "to support staff awareness only."
    )