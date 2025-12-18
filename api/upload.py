import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
import pandas as pd
import os
import json
from datetime import datetime
import tempfile
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our analyzer classes
try:
    from backend.intelligent_data_analyzer import IntelligentDataAnalyzer
    from backend.enhanced_smart_analyzer import EnhancedSmartAnalyzer
    from backend.super_intelligent_analyzer import SuperIntelligentAnalyzer
except ImportError:
    # Fallback for Vercel deployment
    try:
        import intelligent_data_analyzer
        import enhanced_smart_analyzer
        import super_intelligent_analyzer
        IntelligentDataAnalyzer = intelligent_data_analyzer.IntelligentDataAnalyzer
        EnhancedSmartAnalyzer = enhanced_smart_analyzer.EnhancedSmartAnalyzer
        SuperIntelligentAnalyzer = super_intelligent_analyzer.SuperIntelligentAnalyzer
    except ImportError:
        print("Warning: Could not import analyzer classes")
        IntelligentDataAnalyzer = None
        EnhancedSmartAnalyzer = None
        SuperIntelligentAnalyzer = None

app = Flask(__name__)

# Configuration
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_csv_file(filepath):
    """Process CSV file and return basic info"""
    try:
        df = pd.read_csv(filepath)
        return {
            'type': 'csv',
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'head': df.head().to_dict('records'),
            'summary': df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {}
        }
    except Exception as e:
        return {'error': f'Error processing CSV: {str(e)}'}

def process_excel_file(filepath):
    """Process Excel file and return basic info"""
    try:
        df = pd.read_excel(filepath)
        return {
            'type': 'excel',
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'head': df.head().to_dict('records'),
            'summary': df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {}
        }
    except Exception as e:
        return {'error': f'Error processing Excel: {str(e)}'}

def handler(request):
    if request.method != 'POST':
        return jsonify({'error': 'Method not allowed'}), 405
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_filepath = temp_file.name
        
        try:
            # Process file based on extension
            file_ext = file.filename.rsplit('.', 1)[1].lower()
            
            if file_ext == 'csv':
                result = process_csv_file(temp_filepath)
            elif file_ext in ['xlsx', 'xls']:
                result = process_excel_file(temp_filepath)
            else:
                result = {'error': 'Unsupported file type for processing'}
            
            # Clean up
            os.unlink(temp_filepath)
            
            if 'error' in result:
                return jsonify(result), 400
            
            # Store file info in response
            result['filename'] = secure_filename(file.filename)
            result['upload_time'] = datetime.now().isoformat()
            
            return jsonify({
                'success': True,
                'message': 'File uploaded and processed successfully',
                'file_info': result
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_filepath):
                os.unlink(temp_filepath)
            raise e
            
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

# For Vercel
def main(request):
    return handler(request)
