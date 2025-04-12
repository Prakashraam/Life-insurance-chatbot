import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env and API key
load_dotenv()
genai.configure(api_key="AIzaSyBDGLIRgM745CMm3Lhfs782jKSoaDRvRBI")

# Test the model
def test_model():
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content("Tell me a fun fact about life insurance.")
        print("✅ Gemini Response:\n", response.text)
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    test_model()

# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# load_dotenv()
# genai.configure(api_key="AIzaSyBDGLIRgM745CMm3Lhfs782jKSoaDRvRBI")

# def list_models():
#     models = genai.list_models()
#     for model in models:
#         print(f"{model.name} | Supported methods: {model.supported_generation_methods}")

# if __name__ == "__main__":
#     list_models()
