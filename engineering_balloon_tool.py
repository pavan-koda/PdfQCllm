import os
import re
import fitz  # PyMuPDF
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

from flask import Flask, request, send_file, render_template_string, url_for
from werkzeug.utils import secure_filename

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Single-file HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Engineering Drawing Ballooning Tool</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f4f9; color: #333; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 90%; max-width: 1000px; margin-top: 2rem; }
        h1 { color: #2c3e50; text-align: center; }
        .upload-area { border: 2px dashed #3498db; padding: 2rem; text-align: center; border-radius: 8px; background: #f8fbff; }
        .btn { background-color: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; font-size: 1rem; }
        .btn:hover { background-color: #2980b9; }
        .preview-container { margin-top: 2rem; height: 700px; border: 1px solid #ddd; }
        iframe { width: 100%; height: 100%; border: none; }
        .stats { text-align: center; margin: 1rem 0; color: #27ae60; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📐 Auto-Ballooning Tool</h1>
        
        {% if not processed_file %}
        <div class="upload-area">
            <form method="post" enctype="multipart/form-data">
                <p>Upload your Engineering Drawing (PDF)</p>
                <input type="file" name="file" accept=".pdf" required>
                <br><br>
                <button type="submit" class="btn">🚀 Upload & Balloon</button>
            </form>
        </div>
        {% else %}
        <div class="stats">✅ Added {{ count }} balloons to {{ filename }}</div>
        
        {% if ai_summary %}
        <div style="background: #e8f6f3; padding: 1rem; border-radius: 5px; margin: 1rem 0; text-align: left; border-left: 5px solid #27ae60;">
            <strong>🤖 Llama Vision Analysis:</strong>
            <p style="white-space: pre-wrap; margin-top: 0.5rem;">{{ ai_summary }}</p>
        </div>
        {% endif %}
        
        <div style="text-align: center;">
            <a href="{{ url_for('download_file', filename=processed_file) }}" class="btn">💾 Download PDF</a>
            <a href="/" class="btn" style="background-color: #95a5a6;">🔄 New File</a>
        </div>

        <div class="preview-container">
            <!-- Browser native PDF preview -->
            <iframe src="{{ url_for('download_file', filename=processed_file) }}#toolbar=0"></iframe>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def is_dimension(text):
    """
    Detects if text is likely an engineering dimension.
    Matches: 10.5, 10.00, Ø10, R5, M6, 45°
    """
    clean_text = text.strip('.,;')
    patterns = [
        r'^\d+\.\d+$',          # Decimals (e.g., 10.5)
        r'^[ØRMr]\d+(\.\d+)?$', # Symbols (e.g., Ø10, R5, M6)
        r'^\d+(\.\d+)?°$'       # Degrees (e.g., 45°)
    ]
    for p in patterns:
        if re.match(p, clean_text):
            return True
    return False

def process_pdf(input_path, output_path):
    doc = fitz.open(input_path)
    balloon_count = 0
    
    for page in doc:
        # Get words with coordinates: (x0, y0, x1, y1, "text", ...)
        words = page.get_text("words")
        
        for w in words:
            text = w[4]
            if is_dimension(text):
                balloon_count += 1
                x1, y0 = w[2], w[1] # Top-right corner of text
                
                # Balloon settings
                center = fitz.Point(x1 + 8, y0 - 2)
                radius = 8
                
                # Draw Red Circle
                page.draw_circle(center, radius, color=(1, 0, 0), fill=(1, 1, 1), width=1)
                
                # Draw Number (Centered)
                text_len = fitz.get_text_length(str(balloon_count), fontsize=8)
                text_pos = fitz.Point(center.x - (text_len/2), center.y + 3)
                page.insert_text(text_pos, str(balloon_count), fontsize=8, color=(1, 0, 0))
                
    doc.save(output_path)
    doc.close()
    return balloon_count

def get_ai_summary(input_path):
    """
    Uses Llama 3.2 Vision to analyze the drawing.
    """
    if not OLLAMA_AVAILABLE:
        return "Ollama library not installed. AI analysis unavailable."
    
    try:
        # Convert first page to image for the LLM
        doc = fitz.open(input_path)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
        img_data = pix.tobytes("png")
        doc.close()
        
        response = ollama.chat(
            model='llama3.2-vision:11b',
            messages=[{
                'role': 'user',
                'content': 'You are an expert mechanical engineer. Analyze this technical drawing. Briefly list the main component shown and describe the key features (holes, flanges, dimensions) you see.',
                'images': [img_data]
            }]
        )
        return response['message']['content']
    except Exception as e:
        return f"AI Analysis could not run (ensure Ollama is running): {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files: return 'No file'
        file = request.files['file']
        if file.filename == '': return 'No file'
        
        if file:
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            output_filename = f"ballooned_{filename}"
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
            
            count = process_pdf(input_path, output_path)
            ai_summary = get_ai_summary(input_path)
            
            return render_template_string(HTML_TEMPLATE, processed_file=output_filename, filename=filename, count=count, ai_summary=ai_summary)
            
    return render_template_string(HTML_TEMPLATE, processed_file=None)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['PROCESSED_FOLDER'], filename))

if __name__ == '__main__':
    print("Starting Balloon Tool on http://0.0.0.0:5001")
    app.run(host='0.0.0.0', debug=True, port=5001)