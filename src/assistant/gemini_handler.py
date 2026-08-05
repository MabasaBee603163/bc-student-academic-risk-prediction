import os
from google import genai

def generate_risk_explanation(student_data, risk_label, user_question):
    # Initialize the client. It automatically looks for GEMINI_API_KEY in your .env or system variables.
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    # Configuration settings from your export
    generation_config = {
        'temperature': 1, 
        'max_output_tokens': 65536,
        'top_p': 0.95,
        'thinking_level': 'high',
    }

    # Wrapped in triple quotes (""") to prevent apostrophes from breaking the code
    system_instruction = """You are an AI academic support assistant for staff at Belgium Campus ITversity. Your purpose is to explain a machine learning model's academic risk prediction based purely on the provided student data.

Strict Rules of Operation:
Advisory Only: Always treat the model's output as an early-warning indicator to support staff awareness. It is never a final academic decision.

No Hallucinations: Do not invent student history, grades, incidents, or metrics that are not explicitly provided in the prompt.

Terminology: Never claim the model "failed" or "will exclude" a student.

Context: Treat the student's programme and specialisation as context, but focus on the key predictors (e.g., attendance, assignment completion, midyear average, missed assessments, and failed modules) to explain the risk.

Required Response Format:
- State the predicted risk (Low, Medium, or High).
- Highlight 2 to 4 concrete input signals from the data that justify the prediction.
- Conclude with a brief reminder that this is a support tool, not an official academic judgement."""

    # This dynamically builds the exact prompt using the variables passed from the front-end
    dynamic_prompt = f"""
    The machine learning model has evaluated a student and generated the following prediction:
    Predicted Risk Label: {risk_label}

    Here is the student's academic data:
    {student_data}

    Staff Member Question: "{user_question}"
    """

    # Triggering the API call using your specific preview model and structured interaction
    interaction = client.interactions.create(
        model='models/gemini-3-flash-preview',
        input=dynamic_prompt,
        system_instruction=system_instruction,
        generation_config=generation_config,
    )

    # Returns the actual text response to be sent back to Role 3's front-end
    return interaction.steps[-1].text