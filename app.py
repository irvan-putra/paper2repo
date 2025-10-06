#!/usr/bin/env python3
"""
Paper2Repo Web Demo
A simple Flask web interface for converting PDFs to code
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import zipfile
import io

# Import our PDF to code converter
from pdf_to_code import DemoPaper2Code

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Global converter instance
converter = DemoPaper2Code()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF upload and conversion"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Please upload a PDF file'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Convert PDF to code
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], Path(filename).stem)
        result_dir = converter.convert_paper(filepath, output_dir)
        
        if result_dir:
            # Read generated files for display
            files = {}
            result_path = Path(result_dir)
            
            for file_path in result_path.iterdir():
                if file_path.is_file() and file_path.suffix in ['.py', '.md', '.txt', '.json']:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        files[file_path.name] = f.read()
            
            return jsonify({
                'success': True,
                'output_dir': result_dir,
                'files': files,
                'message': 'Conversion completed successfully!'
            })
        else:
            return jsonify({'error': 'Conversion failed'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/download/<path:output_dir>')
def download_repo(output_dir):
    """Download generated repository as ZIP"""
    try:
        # Create ZIP file in memory
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            output_path = Path(output_dir)
            for file_path in output_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(output_path)
                    zf.write(file_path, arcname)
        
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            as_attachment=True,
            download_name=f"{Path(output_dir).name}.zip",
            mimetype='application/zip'
        )
        
    except Exception as e:
        return jsonify({'error': f'Error creating download: {str(e)}'}), 500

@app.route('/status')
def status():
    """API status endpoint"""
    return jsonify({
        'status': 'running',
        'aws_enabled': converter.use_aws,
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting Paper2Repo Web Demo...")
    print("📝 Visit http://localhost:5000 to use the interface")
    print("🔧 AWS Bedrock:", "Enabled" if converter.use_aws else "Demo mode (heuristics)")
    app.run(debug=True, host='0.0.0.0', port=5000)
