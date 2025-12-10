# Clinical Aliquot Generator

A Flask-based web application that uses Google's Gemini 3.0 API to convert unstructured EMR text into structured clinical aliquots for case presentations.

## Features
- **Upload Interface**: Drag-and-drop support for `.txt` and `.pdf` files.
- **AI-Powered**: Uses `gemini-3-pro-preview` to analyze clinical text.
- **Structured Output**: Generates sequential aliquots (History, Exam, Labs, etc.) following VMR standards.
- **Copy-Ready**: Outputs clean Markdown formatted for easy sharing.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install flask google-generativeai pypdf
    ```

2.  **Configure API Key:**
    Update `aliquot_generator.py` with your Gemini API key:
    ```python
    GENAI_API_KEY = "YOUR_API_KEY"
    ```

3.  **Run the Application:**
    ```bash
    python3 app.py
    ```

4.  **Access:**
    Open `http://127.0.0.1:5000` in your browser.

## Project Structure
- `app.py`: Flask backend server.
- `aliquot_generator.py`: Core logic for text extraction and Gemini API interaction.
- `prompt_template.txt`: The system prompt used to guide the AI's generation.
- `templates/`: HTML files for the web interface.
