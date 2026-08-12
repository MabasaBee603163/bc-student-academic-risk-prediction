# Role 3 – Frontend Integration

This document describes the completed frontend implementation for the BC Student Academic Risk Prediction system.

The frontend was developed using **Streamlit** and connects the user interface to both the trained machine-learning model and the Gemini conversational layer.

## 1. Frontend Location

The frontend application is located in:

`app.py`

The application allows staff users to enter student information, generate an academic-risk prediction, ask a question about the result, and receive a plain-English explanation.

The frontend can be started using:

```bash
python -m streamlit run app.py
```

The application normally opens at:

`http://localhost:8501`

## 2. Student Input Interface

The frontend provides input controls for the student information required by the machine-learning model.

The supported inputs include:

* Age
* Gender
* Programme
* Specialisation
* Year of Study
* Attendance
* Assignment Completion
* BC Connect Activity
* Missed Assessments
* Overall Average
* Midyear Average
* Test Average
* Assignment Average
* Practical Average
* Failed Modules
* Registered Modules
* Passed Modules

Programme and specialisation are selected using dropdown menus, while numeric academic values are entered using number input fields.

## 3. Machine-Learning Integration

The frontend loads the trained model and label encoder from:

```text
models/trained_model.pkl
models/label_encoder.pkl
```

The student information entered through the interface is converted into a Pandas DataFrame and passed to the trained model.

Example:

```python
student_df = pd.DataFrame([student_data])

prediction_encoded = model.predict(student_df)

prediction_label = label_encoder.inverse_transform(
    prediction_encoded
)[0]
```

The prediction is returned as one of the following values:

* Low
* Medium
* High

The frontend then displays the predicted academic-risk level to the user.

## 4. Gemini Conversational Integration

The AI integration logic is located in:

`src/assistant/gemini_handler.py`

The frontend imports the following function:

```python
from src.assistant.gemini_handler import generate_risk_explanation
```

After the machine-learning model produces a prediction, the frontend passes the student data, the predicted risk label, and the user's question to the Gemini conversational layer.

```python
ai_response = generate_risk_explanation(
    student_data=student_data,
    risk_label=prediction_label,
    user_question=user_question
)
```

Gemini then returns a plain-English explanation that is displayed in the frontend.

The machine-learning model produces the actual risk prediction. Gemini is only responsible for explaining that prediction using the supplied student information.

## 5. API Key Setup

The Gemini API key is stored securely in a local `.env` file in the root directory of the project.

The file contains:

```text
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is excluded from GitHub through `.gitignore` so that the API key is not committed to the repository.

The Gemini handler uses `python-dotenv` to load the API key into the local environment.

## 6. User Interaction Flow

The completed frontend follows this process:

```text
Staff User
    ↓
Enter Student Information
    ↓
Streamlit Frontend
    ↓
Machine-Learning Model
    ↓
Low / Medium / High Prediction
    ↓
User Question
    ↓
Gemini Conversational Layer
    ↓
Plain-English Explanation
    ↓
Displayed to Staff User
```

This provides an end-to-end interface for using both the trained model and the conversational AI layer.

## 7. Decision-Support Warning

The frontend clearly informs users that the system is intended as a decision-support tool only.

The prediction should be treated as an early-warning indicator that can support staff awareness and further review.

It must not be treated as a final academic judgement or official decision about a student.

## 8. Role 3 Contribution

**Justin Cloete – Role 3: Frontend Integration**

Role 3 was responsible for:

* Developing the Streamlit web interface.
* Creating the student information and academic performance input fields.
* Connecting the frontend to the trained machine-learning model.
* Displaying Low, Medium, and High academic-risk predictions.
* Connecting the frontend to the Gemini conversational layer.
* Allowing staff users to enter natural-language questions.
* Displaying Gemini-generated explanations.
* Adding decision-support warnings.
* Adding the required Streamlit and Gemini dependencies.
* Testing the complete frontend workflow.
