from dotenv import load_dotenv
import streamlit as st
import os
import pathlib
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Configure Google API key for generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load OpenAI model and get responses
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Define the prompt template
    prompt_template = """
        Analyze the image to determine if it is related to plants or leaves:

        1. If the image shows a plant or leaf:
        - Identify the *botanical name* of the plant species.
        - Provide the *common name* of the plant.
        - Detect any *diseases* affecting the plant or leaf. If no diseases are present, state "*No diseases found*."
        - If a disease is detected, describe the *symptoms* in detail and suggest possible *causes*.
        - Recommend appropriate *treatments or cures* for the disease.

        2. If the image does not show a plant or leaf:
        - Respond with "*No plant identity*."
        """
 
    # Append user input (if any) to the prompt template
    if input_text != "":
        final_prompt = f"{input_text}\n\n{prompt_template}"
    else:
        final_prompt = prompt_template
    
    # Get the model response with both input and image
    response = model.generate_content([final_prompt, image])
    
    return response.text

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")

# User input for the prompt
input_text = st.text_input("Input Prompt (optional): ", key="input")

# File uploader for the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""  # Placeholder for image content

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to submit the form
submit = st.button("Tell me about the image")

# If submit button is clicked
if submit:
    response = get_gemini_response( input_text ,image)
    st.subheader("The Response is")
    st.write(response)