import sys
import os
import json
from pypdf import PdfReader

def extract_text(file_path):
    try:
        if file_path.lower().endswith('.pdf'):
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        else:
            with open(file_path, 'r') as f:
                return f.read()
    except Exception as e:
        return str(e)

def load_prompt(template_path, text):
    with open(template_path, 'r') as f:
        template = f.read()
    return template.replace("{text}", text)

import google.generativeai as genai

# Configure Gemini API
GENAI_API_KEY = "AIzaSyCcTLQvt6hRtWu32833wimZzDMz0voxNqU"
genai.configure(api_key=GENAI_API_KEY)

# Generate Aliquots using Gemini API
def generate_aliquots_with_gemini(text):
    try:
        model = genai.GenerativeModel('gemini-3-pro-preview')
        
        # Load the prompt template
        template_path = "prompt_template.txt"
        if os.path.exists(template_path):
            prompt = load_prompt(template_path, text)
        else:
            # Fallback prompt if template file is missing
            prompt = f"""
            You are a clinician-educator. Convert the following EMR text into structured clinical aliquots for a case presentation.
            Follow the standard VMR format with numbered aliquots (1: Presenting Situation, 2: History, 3: Exam, 4: Labs/Imaging, etc.) and a Final Diagnosis.
            
            Raw Text:
            {text}
            """
            
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating aliquots with Gemini API: {str(e)}"

# Alias for backward compatibility with app.py (or update app.py to use this name)
def simulate_llm_response(text, filename=""):
    return generate_aliquots_with_gemini(text)

def render_markdown(text):
    # The text is already in the desired format
    return text

if __name__ == "__main__":
    # Default to the first case if no argument provided
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = "/Users/sakethvinjamuri/Documents/Dr. Austin's CPS Project/Example Data.pdf"
    
    template_path = "prompt_template.txt"
    
    # 1. Extract Text (Real)
    if os.path.exists(input_path):
        raw_text = extract_text(input_path)
    else:
        print(f"Error: File not found at {input_path}")
        sys.exit(1)

    # 2. Prepare Prompt (Real - for context, though we mock the response)
    # prompt = load_prompt(template_path, raw_text)
    
    # 3. Simulate LLM Response (Mocked)
    response_text = simulate_llm_response(raw_text, filename=input_path)
    
    # 4. Render Output
    markdown_output = render_markdown(response_text)
    
    print(markdown_output)
    
    # Save to file for review (derive filename from input)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_filename = f"{base_name}_aliquots.md"
    
    with open(output_filename, "w") as f:
        f.write(markdown_output)
    print(f"\nOutput saved to {output_filename}")
