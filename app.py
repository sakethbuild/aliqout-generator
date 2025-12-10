import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from aliquot_generator import extract_text, simulate_llm_response, render_markdown

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file
            try:
                raw_text = extract_text(filepath)
                
                # Generate aliquots
                # Pass filename to help the mock generator decide which case to use
                response_text = simulate_llm_response(raw_text, filename=filename)
                
                # Render markdown (optional, but good for consistency)
                markdown_output = render_markdown(response_text)
                
                return render_template('result.html', content=markdown_output, filename=filename)
                
            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
            finally:
                # Clean up uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
                    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
