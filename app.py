import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from coordinator import Coordinator
from tools.file_ops import write_file
import tempfile
import shutil
import json
from flask import Response

app = Flask(__name__, static_folder='static')
CORS(app)

# Ensure the static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

# Initialize Coordinator
# Initialize Coordinator
# Enabling backup by default for better safety, but can be controlled via request data
coordinator = Coordinator(backup_enabled=True)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/process', methods=['POST'])
def process_request():
    data = request.form
    instruction = data.get('instruction', 'analyze this code')
    code_content = data.get('code_content', '')
    history_raw = data.get('history', '[]')
    
    try:
        history = json.loads(history_raw)
    except:
        history = []
    
    # Handle file upload if present
    temp_dir = tempfile.mkdtemp()
    target_path = ""
    
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = file.filename
                target_path = os.path.join(temp_dir, filename)
                file.save(target_path)
        elif code_content:
            # If code is pasted, save it to a temporary file
            target_path = os.path.join(temp_dir, "pasted_code.py")
            write_file(target_path, code_content)
            
        # Execute the request via Coordinator
        dry_run = data.get('dry_run', 'false').lower() == 'true'
        
        report = coordinator.execute_request(target_path, instruction, history=history)
        
        # Read the modified file if refactoring happened
        final_code = ""
        if os.path.exists(target_path):
            with open(target_path, 'r') as f:
                final_code = f.read()
                
        return jsonify({
            "report": report,
            "final_code": final_code,
            "success": True,
            "dry_run": dry_run
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir)

@app.route('/api/stream', methods=['POST'])
def stream_request():
    data = request.form
    instruction = data.get('instruction', 'analyze this code')
    code_content = data.get('code_content', '')
    history_raw = data.get('history', '[]')
    
    try:
        history = json.loads(history_raw)
    except:
        history = []
    
    temp_dir = tempfile.mkdtemp()
    target_path = ""
    
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            target_path = os.path.join(temp_dir, file.filename)
            file.save(target_path)
    elif code_content:
        target_path = os.path.join(temp_dir, "pasted_code.py")
        write_file(target_path, code_content)

    def generate():
        try:
            for part in coordinator.execute_request_stream(target_path, instruction, history=history):
                yield f"data: {json.dumps({'content': part})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
