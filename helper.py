import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Configure the Gemini API with your key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_explanation(topic):
    try:
        # Use Gemini 1.5 Flash model
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content(
            f"Explain this quantum physics concept in simple terms: {topic}"
        )
        return response.text
    except Exception as e:
        return f"Something went wrong: {e}"
