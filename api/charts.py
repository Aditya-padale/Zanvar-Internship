import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
import tempfile
import pandas as pd
from serverless_analyzer import ServerlessAnalyzer
import json

app = Flask(__name__)

def handler(request):
    if request.method != 'POST':
        return jsonify({'error': 'Method not allowed'}), 405
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        chart_type = data.get('chart_type', 'pie')
        file_data = data.get('file_data')  # Base64 encoded file data
        file_type = data.get('file_type', 'csv')
        column = data.get('column')  # Optional specific column
        
        if not file_data:
            return jsonify({'error': 'No file data provided'}), 400
        
        # Create temporary file from base64 data
        import base64
        try:
            file_content = base64.b64decode(file_data)
        except:
            return jsonify({'error': 'Invalid file data encoding'}), 400
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as temp_file:
            temp_file.write(file_content)
            temp_filepath = temp_file.name
        
        try:
            # Initialize analyzer and load data
            analyzer = ServerlessAnalyzer()
            if not analyzer.load_data(temp_filepath, file_type):
                return jsonify({'error': 'Failed to load data file'}), 400
            
            # Create chart based on type
            chart_result = None
            if chart_type.lower() == 'pie':
                chart_result = analyzer.create_pie_chart(column)
            elif chart_type.lower() == 'bar':
                chart_result = analyzer.create_bar_chart(column)
            elif chart_type.lower() == 'line':
                x_col = data.get('x_column')
                y_col = data.get('y_column', column)
                chart_result = analyzer.create_line_chart(x_col, y_col)
            else:
                return jsonify({'error': f'Unsupported chart type: {chart_type}'}), 400
            
            # Clean up
            os.unlink(temp_filepath)
            
            if chart_result is None:
                return jsonify({'error': 'Failed to create chart'}), 500
            
            return jsonify({
                'success': True,
                'chart': chart_result,
                'data_summary': analyzer.get_basic_summary()
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_filepath):
                os.unlink(temp_filepath)
            raise e
            
    except Exception as e:
        return jsonify({'error': f'Chart creation failed: {str(e)}'}), 500

# For Vercel
def main(request):
    return handler(request)
