import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_health_remark(
    glucose,
    haemoglobin,
    cholesterol,
    risk
):

    prompt = f"""
    Patient Health Data

    Glucose: {glucose}
    Haemoglobin: {haemoglobin}
    Cholesterol: {cholesterol}

    Predicted Risk: {risk}

    Based on the provided health parameters, your current health status requires ongoing attention and monitoring. Adopting healthy lifestyle habits and following medical advice can help improve long-term well-being.
    """

    response = model.generate_content(prompt)

    return response.text