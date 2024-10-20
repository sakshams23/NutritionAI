from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()  # Load environment variables from .env file

# Configure Google API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API key is not set. Check your .env file or environment variables.")
else:
    genai.configure(api_key=api_key)

# Function to load OpenAI model and get response
def get_gemini_response(input_text, image_data, prompt):
    if not input_text or not image_data or not prompt:
        raise ValueError("All parameters (input_text, image_data, and prompt) must be non-empty.")
    
    model = genai.GenerativeModel('gemini-1.5-flash-002')
    response = model.generate_content([input_text, image_data[0], prompt])
    return response.text

# Function to process the uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        # Prepare the image data for the API call
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the MIME type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")

# App UI
st.header("Gemini Application")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

# Define input prompt for the model
input_prompt = """
    You are a nutrition expert. Analyze the food items in the image and calculate the total calories.
    Provide details in the format:

    1. Item 1 - no of calories
    2. Item 2 - no of calories
    ----
    ----
"""

# If submit button is clicked
if submit:
    if not input.strip():
        st.error("Input prompt cannot be empty. Please provide a valid text input.")
    else:
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input, image_data, input_prompt)
            st.subheader("The Response is:")
            st.write(response)
        except FileNotFoundError as e:
            st.error("Please upload an image.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
