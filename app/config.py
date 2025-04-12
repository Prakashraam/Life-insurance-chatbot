import google.generativeai as genai

# Directly assign the Google API key here
GOOGLE_API_KEY = "AIzaSyCclsd_YD_Flnb2O3EYr7cAqGkBKCZVqbc"  # Replace with your actual API key

# Configure Google Gemini API with the API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to handle generating a response asynchronously
async def generate_chat_response(user_input: str) -> str:
    try:
        # Clean input text (strip leading/trailing spaces and replace newline characters)
        cleaned_input = user_input.strip().replace("\n", " ")

        # Generate response from the model
        response =  model.generate_content(cleaned_input)

        # Check if the response is valid
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "Sorry, I couldn't generate a valid response. Please try again."

    except Exception as e:
        # Handle any errors and provide feedback
        return f"Error generating response: {str(e)}"
