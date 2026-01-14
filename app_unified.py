"""
Unified PDF QA System with Interactive Model Selection
Combines vision-style indexing with flexible model support
Supports: Llama 3.2-Vision, Gemma, Mistral, Phi, and custom Ollama models
"""

from flask import Flask, render_template, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
import os
import pickle
import uuid
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import components
from vision_pdf_processor import VisionPDFProcessor
from vision_qa_engine import VisionQAEngine
from unified_model_selector import select_model_interactive

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create directories
for directory in ['uploads', 'data', 'logs', 'processed_pdfs']:
    os.makedirs(directory, exist_ok=True)

# Global QA engine (initialized after model selection)
qa_engine: Optional[VisionQAEngine] = None
SELECTED_MODEL: Optional[dict] = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def log_performance(session_id, question, answer, response_time, page_info):
    """Log performance metrics with latest entries on top."""
    log_file = Path('logs') / 'unified_performance.txt'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Read existing content
    existing_content = ""
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()

    # Write new entry at top
    log_entry = f"""
{'='*80}
Timestamp: {timestamp}
Session ID: {session_id}
Model: {SELECTED_MODEL['name']} ({SELECTED_MODEL['model_id']})
Question: {question}
Response Time: {response_time:.3f} seconds
Pages Used: {page_info}
Answer Length: {len(answer)} characters
{'='*80}

"""

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(log_entry + existing_content)


@app.route('/')
def index():
    """Landing page with upload form."""
    return render_template('vision_upload.html',
                         model_info=SELECTED_MODEL)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF upload and processing."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files allowed'}), 400

    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")

        # Save file
        file.save(filepath)
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)

        logger.info(f"PDF uploaded: {filepath}")
        logger.info(f"File size: {file_size_mb:.2f} MB")

        # Process PDF with vision
        output_dir = os.path.join('processed_pdfs', session_id)
        os.makedirs(output_dir, exist_ok=True)

        # Get processing options
        dpi = int(request.form.get('dpi', 150))
        extract_images = request.form.get('extract_images', 'true').lower() == 'true'

        logger.info(f"Processing PDF with DPI={dpi}, extract_images={extract_images}")

        processor = VisionPDFProcessor(
            dpi=dpi,
            extract_images=extract_images,
            extract_text=True,
            batch_size=10
        )

        # Process PDF
        start_time = time.time()
        result = processor.process_pdf(filepath, output_dir)
        processing_time = time.time() - start_time

        if not result:
            os.remove(filepath)
            return jsonify({'error': 'Failed to process PDF. Please check the file.'}), 400

        logger.info(f"PDF processed in {processing_time:.2f} seconds")

        # Create ChromaDB collection and ColPali index
        logger.info("Creating vector index...")
        index_start = time.time()

        success = qa_engine.create_collection(
            session_id=session_id,
            page_images=result['page_images'],
            page_texts=result['page_text'],
            metadata=result['metadata']
        )

        index_time = time.time() - index_start

        if not success:
            return jsonify({'error': 'Failed to create search index'}), 500

        logger.info(f"Index created in {index_time:.2f} seconds")

        # Save metadata to session
        metadata = {
            'filename': filename,
            'total_pages': result['metadata']['total_pages'],
            'session_id': session_id,
            'processing_time': processing_time,
            'index_time': index_time,
            'model': SELECTED_MODEL['name']
        }
        session['metadata'] = metadata
        session['session_id'] = session_id
        session['conversation_history'] = []  # Initialize conversation history

        # Cleanup uploaded file
        os.remove(filepath)

        return jsonify({
            'success': True,
            'session_id': session_id,
            'metadata': metadata
        }), 200

    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/qa')
def qa_page():
    """QA chat interface."""
    if 'session_id' not in session:
        return redirect('/')

    return render_template('vision_qa.html',
                         metadata=session.get('metadata'),
                         model_info=SELECTED_MODEL)


@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle question and return answer."""
    if 'session_id' not in session:
        return jsonify({'error': 'No active session. Please upload a PDF first.'}), 400

    try:
        data = request.json
        question = data.get('question', '').strip()
        use_vision = data.get('use_vision', SELECTED_MODEL.get('vision_support', False))
        top_k = data.get('top_k', 5)

        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400

        session_id = session['session_id']

        # Get conversation history from session (limit to last 5)
        conversation_history = session.get('conversation_history', [])[-5:]

        logger.info(f"Question: {question[:100]}... (use_vision={use_vision}, top_k={top_k}, history_len={len(conversation_history)})")

        # Get answer from QA engine
        start_time = time.time()
        result = qa_engine.answer_question(
            question=question,
            session_id=session_id,
            top_k=top_k,
            use_vision=use_vision,
            use_text_context=True,
            return_images=True,
            conversation_history=conversation_history
        )

        response_time = time.time() - start_time

        # Extract answer and metadata
        if isinstance(result, dict):
            answer = result.get('answer', '')
            images = result.get('images', [])
            page_used = result.get('page')
        else:
            answer = result
            images = []
            page_used = None

        logger.info(f"Answer generated in {response_time:.2f} seconds")

        # Add to conversation history (limit to last 5 exchanges)
        current_timestamp = datetime.now().strftime('%H:%M:%S')
        if 'conversation_history' not in session:
            session['conversation_history'] = []

        session['conversation_history'].append({
            'question': question,
            'answer': answer,
            'page': page_used,
            'timestamp': current_timestamp
        })

        # Keep only last 5 exchanges
        session['conversation_history'] = session['conversation_history'][-5:]

        # Log performance
        log_performance(session_id, question, answer, response_time, page_used)

        return jsonify({
            'success': True,
            'answer': answer,
            'question': question,
            'response_time': round(response_time, 3),
            # Don't send server timestamp - frontend will use client time
            'used_vision': use_vision,
            'images': images,
            'page': page_used
        }), 200

    except Exception as e:
        logger.error(f"Error answering question: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error: {str(e)}'}), 500


@app.route('/reset', methods=['POST'])
def reset_session():
    """Reset current session."""
    session.clear()
    return jsonify({'success': True})


@app.route('/download-log')
def download_log():
    """Download performance log."""
    log_file = Path('logs') / 'unified_performance.txt'

    if not log_file.exists():
        return jsonify({'error': 'No log file found'}), 404

    return send_file(log_file, as_attachment=True, download_name='qa_performance.txt')


@app.route('/data/<session_id>/<filename>')
def serve_page_image(session_id, filename):
    """Serve page images (stored in processed_pdfs directory)."""
    try:
        # Page images are stored in processed_pdfs/{session_id}/page_XXXX.png
        image_path = Path('processed_pdfs') / session_id / filename

        if not image_path.exists():
            logger.error(f"Page image not found: {image_path}")
            return jsonify({'error': 'Page image not found'}), 404

        return send_file(image_path, mimetype='image/png')

    except Exception as e:
        logger.error(f"Error serving page image: {str(e)}")
        return jsonify({'error': f'Error serving page image: {str(e)}'}), 500


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("  UNIFIED PDF QA SYSTEM")
    print("=" * 80)
    print()

    # Interactive model selection
    print("Please select an AI model to use:")
    print()

    model_selection = select_model_interactive()

    if not model_selection:
        print("\n❌ No model selected. Exiting...")
        exit(0)

    model_type, model_id, has_vision = model_selection

    # Store selected model info
    SELECTED_MODEL = {
        'type': model_type,
        'model_id': model_id,
        'name': model_id,
        'vision_support': has_vision
    }

    print("\n" + "=" * 80)
    print("  INITIALIZING QA ENGINE")
    print("=" * 80)
    print(f"Model: {model_id}")
    print(f"Vision Support: {'Yes' if has_vision else 'No'}")
    print()

    # Initialize QA engine with selected model
    try:
        if model_type == 'ollama':
            # Ollama model - use VisionQAEngine with Ollama
            qa_engine = VisionQAEngine(
                model_name=model_id,
                ollama_url="http://localhost:11434",
                use_colpali=True
            )

            if qa_engine and qa_engine._check_ollama_connection():
                print("=" * 80)
                print("  SYSTEM READY")
                print("=" * 80)
                print(f"Model: {model_id}")
                print(f"Model Type: Ollama")
                print(f"Ollama URL: {qa_engine.ollama_url}")
                print(f"Vision Support: {'Enabled' if has_vision else 'Disabled'}")
                print(f"ColPali Enabled: {qa_engine.use_colpali}")
                print("=" * 80)
                print()
                print(f"Starting server at: http://localhost:5000")
                print("Press Ctrl+C to stop")
                print()

                app.run(host='0.0.0.0', port=5000, debug=False)
            else:
                print("\nERROR: Could not connect to Ollama")
                print("Make sure Ollama is running: ollama serve")
                exit(1)

        elif model_type == 'huggingface':
            # HuggingFace model - note that full HF integration requires additional work
            print("\nNOTE: HuggingFace model support is experimental")
            print("The system will attempt to use the model, but functionality may be limited")
            print()

            # For now, we'll use VisionQAEngine but note this needs HF pipeline integration
            qa_engine = VisionQAEngine(
                model_name=model_id,
                ollama_url="http://localhost:11434",  # Won't be used for HF
                use_colpali=True
            )

            print("=" * 80)
            print("  SYSTEM READY (EXPERIMENTAL HF MODE)")
            print("=" * 80)
            print(f"Model: {model_id}")
            print(f"Model Type: HuggingFace")
            print(f"Vision Support: {'Enabled' if has_vision else 'Disabled'}")
            print(f"ColPali Enabled: {qa_engine.use_colpali}")
            print()
            print("WARNING: HuggingFace models require additional setup")
            print("Please ensure you have transformers, torch, and accelerate installed")
            print("=" * 80)
            print()
            print(f"Starting server at: http://localhost:5000")
            print("Press Ctrl+C to stop")
            print()

            app.run(host='0.0.0.0', port=5000, debug=False)

        else:
            print(f"\nERROR: Unknown model type: {model_type}")
            exit(1)

    except Exception as e:
        print(f"\nERROR: Failed to initialize QA engine: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
