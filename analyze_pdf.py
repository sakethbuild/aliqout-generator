import sys
import os

try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf not found. Please install it using 'pip install pypdf'")
    sys.exit(1)

def extract_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    pdf_path = "/Users/sakethvinjamuri/Documents/Dr. Austin's CPS Project/Example Data.pdf"
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
    else:
        content = extract_text(pdf_path)
        print(content)
