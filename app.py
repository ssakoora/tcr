from flask import Flask, request, render_template, send_file, jsonify, url_for
import os
import tempfile
import uuid
import shutil
from werkzeug.utils import secure_filename
import sys
import numpy as np
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), 'sources'))
from TextWithImage import ImageWithText

try:
    import imageio.v2 as imageio
    IMAGEIO_AVAILABLE = True
except ImportError:
    try:
        import imageio
        IMAGEIO_AVAILABLE = True
    except ImportError:
        IMAGEIO_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            session_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
            file.save(upload_path)
            
            results_dir = os.path.join(app.config['RESULTS_FOLDER'], session_id)
            os.makedirs(results_dir, exist_ok=True)
            
            image_processor = ImageWithText(upload_path)
            character_files = image_processor.extract_characters_to_directory(results_dir)
            
            os.remove(upload_path)
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'character_count': len(character_files),
                'redirect_url': url_for('show_results', session_id=session_id)
            })
            
        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP files.'}), 400

@app.route('/results/<session_id>')
def show_results(session_id):
    results_dir = os.path.join(app.config['RESULTS_FOLDER'], session_id)
    
    if not os.path.exists(results_dir):
        return "Results not found", 404
    
    character_files = []
    for filename in sorted(os.listdir(results_dir)):
        if filename.startswith('char_') and filename.endswith('.gif'):
            character_files.append(filename)
    
    character_frequencies = count_character_frequencies(results_dir, character_files)
    
    return render_template('results.html', 
                         session_id=session_id, 
                         character_files=character_files,
                         character_count=len(character_files),
                         character_frequencies=character_frequencies)

@app.route('/character/<session_id>/<filename>')
def serve_character(session_id, filename):
    results_dir = os.path.join(app.config['RESULTS_FOLDER'], session_id)
    file_path = os.path.join(results_dir, filename)
    
    if os.path.exists(file_path) and filename.startswith('char_') and filename.endswith('.gif'):
        return send_file(file_path, mimetype='image/gif')
    else:
        return "File not found", 404

def load_character_image(filepath):
    """Load a character image file and return as numpy array"""
    if IMAGEIO_AVAILABLE:
        return imageio.imread(filepath)
    elif PIL_AVAILABLE:
        img = Image.open(filepath)
        return np.array(img)
    else:
        raise ImportError("No image reading library available")

def calculate_image_similarity(img1, img2):
    """Calculate similarity between two character images using normalized cross-correlation"""
    if img1.shape != img2.shape:
        return 0.0
    
    img1_norm = img1.astype(np.float32) / 255.0
    img2_norm = img2.astype(np.float32) / 255.0
    
    correlation = np.corrcoef(img1_norm.flatten(), img2_norm.flatten())[0, 1]
    
    if np.isnan(correlation):
        if np.allclose(img1_norm, img2_norm):
            return 1.0
        else:
            return 0.0
    
    return max(0.0, correlation)

def count_character_frequencies(results_dir, character_files):
    """Count how many times each character appears by grouping similar images"""
    if not character_files:
        return {}
    
    images = {}
    for filename in character_files:
        filepath = os.path.join(results_dir, filename)
        try:
            images[filename] = load_character_image(filepath)
        except Exception:
            continue
    
    if not images:
        return {}
    
    similarity_threshold = 0.85  # Adjust this threshold as needed
    character_groups = []
    processed = set()
    
    for filename1, img1 in images.items():
        if filename1 in processed:
            continue
            
        current_group = [filename1]
        processed.add(filename1)
        
        for filename2, img2 in images.items():
            if filename2 in processed:
                continue
                
            similarity = calculate_image_similarity(img1, img2)
            if similarity >= similarity_threshold:
                current_group.append(filename2)
                processed.add(filename2)
        
        character_groups.append(current_group)
    
    frequencies = {}
    for group in character_groups:
        group_size = len(group)
        for filename in group:
            frequencies[filename] = group_size
    
    return frequencies

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
