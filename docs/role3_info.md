

# Role 3 Handoff: AI Conversational Layer Integration

This document outlines how to connect the front-end user interface to the AI conversational layer configured for our Academic Support System.

## 1. The Code Location
The AI integration logic is located in `src/assistant/gemini_handler.py`. 

This file contains the `generate_risk_explanation` function. It takes the raw student data, the machine learning model's prediction, and the user's typed question, and sends them to the Gemini API to generate a plain-English explanation.

## 2. API Key Setup (Crucial)
To make the AI function work on your local machine, you need the Google AI Studio API key. The script is designed to look for it securely in your local environment.

1.  Get the API key from the WhatsApp group description.
2.  Create a new file named exactly `.env` in the root directory of the project.
3.  Open the `.env` file and paste this exact line, replacing the placeholder with the real key:
    `GEMINI_API_KEY=paste_the_key_here`
4.  Save the file. It will be ignored by GitHub (thanks to `.gitignore`), keeping the key secure.

## 3. How to Use the Function
Since the underlying model and the AI handler are both Python-based, you should wrap the interface using a Python web framework (like Streamlit or Flask). 

Here is how you import and call the function in your front-end logic:

```python
# Import the function from the assistant folder
from src.assistant.gemini_handler import generate_risk_explanation

# Example usage when a user clicks "Submit" on the UI:
ai_response = generate_risk_explanation(
    student_data=current_student_metrics, # Pass the variables from the UI/Dataset
    risk_label=model_prediction,          # "Low", "Medium", or "High" (From Role 1's model)
    user_question=user_input_text         # The string typed by the user in your UI
)

# Display ai_response on the web page