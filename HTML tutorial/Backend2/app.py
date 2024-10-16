from flask import Flask, request, jsonify, render_template
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure Google API key for generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Endpoint to handle image and input text
@app.route('/analyze', methods=['GET', 'POST'])
def analyze_image():
    if request.method == 'GET':
        # Render the HTML form when the route is accessed via GET
        return '''
            <html>
                <body>
                    <h1>Plant Disease Analysis</h1>
                    <form method="POST" enctype="multipart/form-data" action="/analyze">
                        <label for="input_text">Input Text:</label>
                        <input type="text" id="input_text" name="input_text"><br><br>
                        <label for="image">Upload Image:</label>
                        <input type="file" id="image" name="image" accept="image/*"><br><br>
                        <button type="submit">Analyze Image</button>
                    </form>
                </body>
            </html>
        '''
    elif request.method == 'POST':
        try:
            # Get the input text and image from the request
            input_text = request.form.get('input_text')
            image_file = request.files['image']

            # Check if an image file was uploaded
            if image_file.filename == '':
                return jsonify({"error": "No selected file"}), 400
            
            # Print input text and image filename for debugging
            print(f"Input Text: {input_text}")
            print(f"Uploaded Image: {image_file.filename}")

            # Open the image using PIL
            image = Image.open(image_file)

            # Process the image and input text with generative AI
            response_text = get_gemini_response(input_text, image)

            # Return the AI response as JSON
            return jsonify({"response": response_text})

        except Exception as e:
            print(f"Error: {str(e)}")  # Print the error for debugging
            return jsonify({"error": str(e)}), 500

# Function to load OpenAI model and get responses
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt_template = """
        Analyze the image to determine if it is related to plants or leaves:

        1. Identify the botanical and common names.
        2. Detect diseases and suggest treatments.
    """

    # Create the prompt based on input_text
    final_prompt = f"{input_text}\n\n{prompt_template}" if input_text else prompt_template
    
    # Generate a response using the model
    response = model.generate_content([final_prompt, image])
    
    return response.text

if __name__ == '__main__':
    app.run(debug=True)