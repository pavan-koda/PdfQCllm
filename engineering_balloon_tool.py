import os
import re
import fitz  # PyMuPDF
import concurrent.futures
try:
    import ollama
except ImportError:
    print("Ollama library not found. Please run pip install ollama")

from flask import Flask, request, send_file, render_template_string, url_for, redirect
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
        /* Loader */
        .loader-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,0.9); z-index: 1000; flex-direction: column; justify-content: center; align-items: center; }
        .spinner { border: 8px solid #f3f3f3; border-top: 8px solid #3498db; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div id="loader" class="loader-overlay">
        <div class="spinner"></div>
        <h2 style="color: #2c3e50; margin-top: 20px;">🎈 Ballooning & Analyzing...</h2>
        <p>Please wait while we process your drawing.</p>
        <p style="color: #7f8c8d; font-size: 0.9rem;">Check the server terminal for real-time progress.</p>
    </div>

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
    <script>
        document.querySelector('form')?.addEventListener('submit', function() {
            document.getElementById('loader').style.display = 'flex';
        });
    </script>
</body>
</html>
"""

def is_dimension(text, has_nearby_line=False):
    """
    Detects if text is likely an engineering dimension.
    Uses text patterns and proximity to vector lines (arrows).
    """
    clean_text = text.strip('.,;()[]')
    if not clean_text: return False
    
    # Strong patterns: Symbols that definitely indicate dimensions
    strong_patterns = [
        r'^[ØRMr]\d+(\.\d+)?$', # Symbols (e.g., Ø10, R5, M6)
        r'^[M]\d+(?:[xX]\d+(?:\.\d+)?)?$', # Metric threads (e.g. M6, M6x1)
        r'^\d+(\.\d+)?°$',      # Degrees (e.g., 45°)
        r'^\d+(\.\d+)?[xX]$',   # Multipliers (e.g., 2X)
        r'^\d+[\-±]\d+$'        # Tolerances (e.g. 10-0.1)
    ]
    
    # Weak patterns: Numbers (integers/decimals)
    # These are only dimensions if they are near a line/arrow (to avoid page numbers, notes)
    weak_patterns = [
        r'^\d+$',               # Integers (e.g., 10)
        r'^\d+\.\d+$',          # Decimals (e.g., 10.5)
        r'^\d+,\d+$',           # European Decimals (e.g., 10,5)
    ]

    for p in strong_patterns:
        if re.match(p, clean_text, re.IGNORECASE):
            return True
            
    # If the text is near a vector line (arrow), we accept simple numbers
    if has_nearby_line:
        for p in weak_patterns:
            if re.match(p, clean_text, re.IGNORECASE):
                return True
                
    return False

def get_llm_dimensions(page_pixmap):
    """
    Uses Llama 3.2 Vision to identify dimension text visually.
    Returns a set of strings that the model identifies as dimensions.
    """
    try:
        # Convert PyMuPDF pixmap to PNG bytes
        img_data = page_pixmap.tobytes("png")
        
        # Retry loop
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                print(f"    [AI] Sending image to Llama 3.2 Vision (Attempt {attempt}/{max_retries})... This may take several minutes on 4GB GPU.")
                
                # Run AI with a timeout to prevent hanging forever
                def call_ai():
                    return ollama.chat(
                        model='llama3.2-vision:11b',
                        messages=[{
                            'role': 'user',
                            'content': 'Analyze this engineering drawing. List all the dimension values (numbers like 50, 10.5, or codes like M6, R5) that are pointed to by arrows or lines. Return ONLY a JSON-style list of the values found. Example: ["50", "10.5", "M6"]. Do not include title block text.',
                            'images': [img_data]
                        }]
                    )

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(call_ai)
                    response = future.result(timeout=600) # Increased timeout (10 min) for 4GB GPU
                
                content = response['message']['content']
                found_values = set(re.findall(r'[ØRMr]?\d+(?:[.,]\d+)?(?:[xX]\d+)?°?', content))
                print(f"    [AI] Found {len(found_values)} dimensions: {list(found_values)[:5]}...")
                return found_values

            except concurrent.futures.TimeoutError:
                print(f"    [AI] Attempt {attempt} timed out.")
            except Exception as e:
                print(f"    [AI] Attempt {attempt} failed: {e}")
        
        print("    [AI] All attempts failed. Skipping AI analysis.")
        return set()
    except Exception as e:
        print(f"    [AI] Error: {e}")
        return set()

def process_pdf(input_path, output_path):
    doc = fitz.open(input_path)
    balloon_count = 0
    total_pages = len(doc)
    print(f"\nStarting processing for: {os.path.basename(input_path)} ({total_pages} pages)")
    
    for page_num, page in enumerate(doc):
        print(f"--- Processing Page {page_num + 1}/{total_pages} ---")
        # 0. Get LLM Analysis for this page
        # Render page to image for the AI
        pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0)) # 1.0x zoom (faster)
        llm_values = get_llm_dimensions(pix)

        # 1. Analyze Vector Graphics (Lines & Arrows)
        # We get all drawing paths to check for proximity to text
        drawings = page.get_drawings()
        drawing_rects = []
        for path in drawings:
            # Filter: Ignore huge boxes (borders) or tiny specks
            r = path["rect"]
            if r.width < page.rect.width * 0.9 and (r.width > 1 or r.height > 1):
                drawing_rects.append(r)

        # Get words with coordinates: (x0, y0, x1, y1, "text", ...)
        words = page.get_text("words")
        
        for w in words:
            text = w[4]
            
            # 2. Check Proximity to Lines/Arrows
            # Expand word area dynamically based on font size to find touching lines
            # Handles gaps in dimension lines (<--- 50 --->) and angled leaders
            word_rect = fitz.Rect(w[0], w[1], w[2], w[3])
            word_height = word_rect.height
            expansion = max(15, word_height * 2.5)
            search_area = fitz.Rect(word_rect.x0 - expansion, word_rect.y0 - expansion, 
                                    word_rect.x1 + expansion, word_rect.y1 + expansion)
            
            has_line = False
            for dr in drawing_rects:
                if search_area.intersects(dr):
                    has_line = True
                    break
            
            # 3. Decide if it's a dimension
            # Condition A: Strong geometric match (symbol or near line)
            # Condition B: LLM explicitly identified this value as a dimension
            clean_val = text.strip('.,;()[]')
            if is_dimension(text, has_nearby_line=has_line) or (clean_val in llm_values):
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
    print(f"Done! Saved to {output_path}. Total balloons: {balloon_count}\n")
    return balloon_count

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
            
            return redirect(url_for('index', processed_file=output_filename, filename=filename, count=count))
            
    processed_file = request.args.get('processed_file')
    filename = request.args.get('filename')
    count = request.args.get('count')
    return render_template_string(HTML_TEMPLATE, processed_file=processed_file, filename=filename, count=count)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['PROCESSED_FOLDER'], filename))

if __name__ == '__main__':
    print("Starting Balloon Tool on http://0.0.0.0:5001")
    app.run(host='0.0.0.0', debug=True, port=5001)