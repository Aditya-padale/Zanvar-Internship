from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import PyPDF2
import os
import json
from datetime import datetime
import base64
import io
try:
    import google.generativeai as genai
    HAS_GOOGLE_AI = True
except ImportError:
    genai = None
    HAS_GOOGLE_AI = False
    print("Warning: Google AI not available, using fallback mode")

from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from intelligent_data_analyzer import IntelligentDataAnalyzer
from enhanced_smart_analyzer import EnhancedSmartAnalyzer
from super_intelligent_analyzer import SuperIntelligentAnalyzer

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx', 'xls'}

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('generated_charts', exist_ok=True)

# Global analyzer instance
analyzer = None

# Conversation memory to track context
conversation_memory = {
    'last_question': '',
    'last_answer': '',
    'mentioned_parts': [],
    'mentioned_dates': [],
    'mentioned_defects': [],
    'session_context': {},
    'context': {}  # For maintaining current conversation context
}

# Configure Google Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
model = None

if HAS_GOOGLE_AI and api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Google Gemini API configured successfully")
    except Exception as e:
        print(f"Warning: Google API configuration failed: {e}")
else:
    if not HAS_GOOGLE_AI:
        print("Warning: Google AI library not available")
    else:
        print("Warning: GOOGLE_API_KEY not found in environment variables")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def safe_json(obj):
    if isinstance(obj, float) and (pd.isna(obj) or math.isnan(obj)):
        return None
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    if isinstance(obj, dict):
        return {k: safe_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [safe_json(x) for x in obj]
    return str(obj)

def process_csv_file(filepath):
    """Process CSV file and return basic info"""
    try:
        df = pd.read_csv(filepath)
        # Convert pandas data types to JSON serializable format
        data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}
        null_counts = {col: int(count) for col, count in df.isnull().sum().items()}
        numeric_summary = df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {}
        numeric_summary = safe_json(numeric_summary)
        info = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'data_types': data_types,
            'sample_data': df.head().to_dict('records'),
            'null_counts': null_counts,
            'numeric_summary': numeric_summary
        }
        return info
    except Exception as e:
        return {'error': str(e)}

def process_excel_file(filepath):
    """Process Excel file and return basic info"""
    try:
        df = pd.read_excel(filepath)
        # Convert pandas data types to JSON serializable format
        data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}
        null_counts = {col: int(count) for col, count in df.isnull().sum().items()}
        numeric_summary = df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {}
        numeric_summary = safe_json(numeric_summary)
        info = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'data_types': data_types,
            'sample_data': df.head().to_dict('records'),
            'null_counts': null_counts,
            'numeric_summary': numeric_summary
        }
        return info
    except Exception as e:
        return {'error': str(e)}

def process_pdf_file(filepath):
    """Extract text from PDF file"""
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return {'text': text[:1000] + "..." if len(text) > 1000 else text}
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return jsonify({
        "message": "Zanvar Group of Industries - Intelligent Analytics Chatbot API is running!",
        "version": "2.0.0",
        "company": "Zanvar Group of Industries",
        "description": "AI-powered data analysis and visualization platform",
        "capabilities": [
            "Data analysis and insights",
            "Professional chart generation", 
            "Quality control analytics",
            "Statistical calculations",
            "Process improvement recommendations"
        ]
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process file based on type
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension == 'csv':
            file_info = process_csv_file(filepath)
        elif file_extension in ['xlsx', 'xls']:
            file_info = process_excel_file(filepath)
        elif file_extension == 'pdf':
            file_info = process_pdf_file(filepath)
        else:
            file_info = {'message': 'File uploaded successfully'}
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'file_info': file_info
        })
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    uploaded_files = data.get('files', [])
    
    # If no files provided, check for available files in uploads directory
    if not uploaded_files and os.path.exists(UPLOAD_FOLDER):
        available_files = os.listdir(UPLOAD_FOLDER)
        if available_files:
            uploaded_files = available_files
    
    # Process the user query
    response = process_user_query(user_message, uploaded_files)
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

def process_user_query(message, files):
    """Process user query and generate appropriate response using intelligent analysis"""
    global analyzer
    message_lower = message.lower()
    
    # Initialize analyzer if we don't have one and there are available data files
    if not analyzer:
        analyzer = initialize_analyzer(files)
    
    # Use Google API for better question understanding if available
    if model and api_key:
        try:
            # Create a comprehensive prompt for understanding the user's intent
            prompt = f"""
            Analyze this user question about data analysis and determine if it requires:
            1. Specific data analysis (like month-wise breakdown, temporal analysis)
            2. Chart/visualization creation
            3. Statistical analysis
            4. General conversation
            
            User question: "{message}"
            
            If the question asks for "every month", "monthly", "month-wise", or similar temporal grouping,
            it should be treated as a temporal analysis request that requires month-by-month breakdown.
            
            Respond with: "DATA_ANALYSIS" if it needs data processing, "VISUALIZATION" if it needs charts, "GENERAL" if it's conversational.
            Also indicate if temporal grouping is needed: "TEMPORAL_YES" or "TEMPORAL_NO"
            
            Format: CATEGORY|TEMPORAL
            """
            
            api_response = model.generate_content(prompt)
            api_understanding = api_response.text.strip().upper()
            
            # Parse the API response
            is_temporal_request = 'TEMPORAL_YES' in api_understanding
            is_data_request = 'DATA_ANALYSIS' in api_understanding or 'VISUALIZATION' in api_understanding
            
            print(f"Google API Understanding: {api_understanding}")
            print(f"Temporal Request: {is_temporal_request}")
            
            # If it's a temporal request, ensure the analyzer handles it properly
            if analyzer and (is_data_request or is_data_question(message)):
                try:
                    intelligent_response = analyzer.answer_question(message)
                    if intelligent_response and not intelligent_response.startswith("❓"):
                        return intelligent_response
                except Exception as e:
                    print(f"Intelligent analyzer error: {e}")
                    return f"❌ **Error processing your data question:** {str(e)}\n\nPlease try rephrasing your question or check if your data file is properly uploaded."
        
        except Exception as e:
            print(f"Google API error in query processing: {e}")
            # Fall back to original logic
    
    # If we have an analyzer and this is a data-related question, use intelligent analysis
    if analyzer and is_data_question(message):
        try:
            intelligent_response = analyzer.answer_question(message)
            if intelligent_response and not intelligent_response.startswith("❓"):
                return intelligent_response
        except Exception as e:
            print(f"Intelligent analyzer error: {e}")
            # Return a helpful error message instead of failing completely
            return f"❌ **Error processing your data question:** {str(e)}\n\nPlease try rephrasing your question or check if your data file is properly uploaded."
    
    # Check for direct chart/graph requests - use intelligent analyzer first
    if any(word in message_lower for word in ['graph', 'chart', 'plot', 'pie', 'line', 'bar', 'visualize', 'visualization', 'draw']):
        if analyzer:
            try:
                intelligent_response = analyzer.answer_question(message)
                if intelligent_response and not intelligent_response.startswith("❓"):
                    return intelligent_response
            except Exception as e:
                print(f"Chart generation error: {e}")
        return create_direct_chart(files, message)
    
    # Check for specific calculation requests
    if any(word in message_lower for word in ['rejection percentage', 'rejection rate', 'calculate rejection']):
        return calculate_rejection_percentage(files, message)
    
    # Get file context only for data-related queries
    file_context = ""
    if files and any(word in message_lower for word in ['data', 'analyze', 'chart', 'graph', 'calculate', 'statistics', 'file', 'upload', 'csv', 'excel']):
        file_context = get_file_context(files)
    
    # Use Google Gemini AI if available, but with robust fallback
    if model and api_key:
        try:
            # Create a conversational prompt
            if file_context:
                prompt = f"""
                You are a helpful AI assistant. A user has asked: "{message}"
                
                Context: {file_context}
                
                Respond naturally and conversationally, like ChatGPT. Keep responses concise and friendly.
                Only mention data analysis capabilities if directly asked about them.
                For casual greetings or general questions, respond normally without mentioning data files.
                """
            else:
                prompt = f"""
                You are a helpful AI assistant. A user has asked: "{message}"
                
                Respond naturally and conversationally, like ChatGPT. Keep it concise and friendly.
                Don't assume they want data analysis unless they specifically ask for it.
                """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Google API error: {e}")
            print("Falling back to intelligent analyzer or built-in responses...")
            # Try intelligent analyzer one more time
            if analyzer and is_data_question(message):
                try:
                    intelligent_response = analyzer.answer_question(message)
                    if intelligent_response and not intelligent_response.startswith("❓"):
                        return intelligent_response
                except:
                    pass
            return get_fallback_response(message, files)
    
    # Fallback keyword-based responses
    if any(word in message_lower for word in ['chart', 'graph', 'plot', 'visualize']):
        if files:
            return generate_chart_response(files)
        else:
            return "I'd be happy to create charts for you! Please upload a CSV or Excel file with your data."
    
    elif any(word in message_lower for word in ['analyze', 'summary', 'statistics']):
        if files:
            return generate_analysis_response(files)
        else:
            return "I can help analyze your data! Please upload a CSV, Excel, or PDF file."
    
    elif 'calculate' in message_lower:
        return "I can help with calculations! What would you like me to calculate?"
    
    else:
        return "I'm here to help with data analysis, calculations, and visualizations. What would you like to do?"

def get_file_context(files):
    """Get context information about uploaded files"""
    context = "Available files and their structure:\n"
    
    # Get all available files from uploads directory
    available_files = os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
    
    # If no files provided in request, use all available files
    if not files:
        files = available_files
    
    for file in files:
        try:
            # Try exact filename first
            filepath = os.path.join(UPLOAD_FOLDER, file)
            
            # If file doesn't exist, try to find similar names
            if not os.path.exists(filepath):
                # Look for files with similar names (handle spaces vs underscores)
                possible_files = [
                    f for f in available_files 
                    if f.lower().replace(' ', '_').replace('-', '_') == file.lower().replace(' ', '_').replace('-', '_')
                    or file.lower().replace(' ', '_').replace('-', '_') in f.lower().replace(' ', '_').replace('-', '_')
                ]
                if possible_files:
                    file = possible_files[0]
                    filepath = os.path.join(UPLOAD_FOLDER, file)
            
            if os.path.exists(filepath):
                if file.endswith('.csv'):
                    df = pd.read_csv(filepath)
                    context += f"\n- {file}: CSV with {df.shape[0]} rows, {df.shape[1]} columns\n"
                    context += f"  Columns: {', '.join(df.columns.tolist())}\n"
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    if numeric_cols:
                        context += f"  Numeric columns: {', '.join(numeric_cols)}\n"
                    
                    # Add sample data for better context
                    sample_data = df.head(3).to_dict('records')
                    context += f"  Sample data: {sample_data}\n"
                    
                elif file.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(filepath)
                    context += f"\n- {file}: Excel with {df.shape[0]} rows, {df.shape[1]} columns\n"
                    context += f"  Columns: {', '.join(df.columns.tolist())}\n"
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    if numeric_cols:
                        context += f"  Numeric columns: {', '.join(numeric_cols)}\n"
                    
                    # Add sample data for better context
                    sample_data = df.head(3).to_dict('records')
                    context += f"  Sample data: {sample_data}\n"
                    
                elif file.endswith('.pdf'):
                    context += f"\n- {file}: PDF document\n"
                else:
                    context += f"\n- {file}: Image file\n"
            else:
                context += f"\n- {file}: File not found in uploads directory\n"
                
        except Exception as e:
            context += f"\n- {file}: Error reading file - {str(e)}\n"
    
    # If no files were processed, list all available files
    if "Error reading file" in context or "File not found" in context:
        context += f"\nAvailable files in uploads directory: {', '.join(available_files)}\n"
    
    return context

def initialize_analyzer(files):
    """Initialize the intelligent analyzer with the first available data file"""
    try:
        available_files = os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
        
        # Look for Excel or CSV files
        for file in available_files:
            if file.endswith(('.xlsx', '.xls', '.csv')):
                filepath = os.path.join(UPLOAD_FOLDER, file)
                if os.path.exists(filepath):
                    print(f"Initializing Super Intelligent Analyzer with: {file}")
                    # Try super intelligent analyzer first, fallback to enhanced if needed
                    try:
                        return SuperIntelligentAnalyzer(filepath)
                    except Exception as e:
                        print(f"Super intelligent analyzer failed, trying enhanced: {e}")
                        try:
                            return EnhancedSmartAnalyzer(filepath)
                        except Exception as e2:
                            print(f"Enhanced analyzer failed, using regular: {e2}")
                            return IntelligentDataAnalyzer(filepath)
        
        return None
    except Exception as e:
        print(f"Error initializing analyzer: {e}")
        return None

def is_data_question(message):
    """Check if the message is asking for data analysis"""
    data_keywords = [
        'part', 'rejection', 'defect', 'total', 'highest', 'lowest', 'count',
        'quantity', 'date', 'when', 'which', 'how many', 'what is', 'machine',
        'burr', 'damage', 'toolmark', 'ratio', 'percentage', 'trend', 'analysis',
        'statistics', 'calculate', 'sum', 'average', 'maximum', 'minimum',
        'top', 'reason', 'reasons', 'frequent', 'most', 'common', 'why', 'causes'
    ]
    
    # Specific patterns that clearly indicate data questions
    data_patterns = [
        r'top\s+\d+', r'\d+\s+rejection', r'rejection\s+reason',
        r'tell\s+top', r'show\s+top', r'list\s+top',
        r'most\s+frequent', r'highest\s+rejection', r'common\s+defect'
    ]
    
    message_lower = message.lower()
    
    # Check for pattern matches
    import re
    for pattern in data_patterns:
        if re.search(pattern, message_lower):
            return True
    
    # Check for keyword matches
    return any(keyword in message_lower for keyword in data_keywords)

def get_fallback_response(message, files):
    """Fallback responses when AI is not available"""
    global analyzer
    message_lower = message.lower()
    
    # Try to use the intelligent analyzer first if it's available
    if analyzer:
        try:
            intelligent_response = analyzer.answer_question(message)
            if intelligent_response and not intelligent_response.startswith("❓"):
                return intelligent_response
        except Exception as e:
            print(f"Analyzer error in fallback: {e}")
    
    # Data-specific questions with built-in responses
    if any(word in message_lower for word in ['part', 'highest', 'rejection']):
        return get_data_driven_response(message, files)
    
    elif any(word in message_lower for word in ['machine learning', 'ml', 'artificial intelligence', 'ai']):
        return "Machine learning is a branch of artificial intelligence (AI) that focuses on building applications that can learn from data and improve their accuracy over time without being programmed to do so. I can help you analyze data, create visualizations, and perform statistical calculations. Feel free to upload your data files!"
    
    elif any(word in message_lower for word in ['chart', 'graph', 'plot', 'visualize']):
        if files:
            return generate_chart_response(files)
        else:
            return "I'd be happy to create charts for you! Please upload a CSV or Excel file with your data."
    
    elif any(word in message_lower for word in ['analyze', 'summary', 'statistics']):
        if files:
            return generate_analysis_response(files)
        else:
            return "I can help analyze your data! Please upload a CSV, Excel, or PDF file."
    
    elif 'calculate' in message_lower:
        return "I can help with calculations! What would you like me to calculate?"
    
    elif any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your analytics assistant. I can help you analyze data, create charts, perform calculations, and answer questions about data science topics. Upload your files and ask me anything!"
    
    else:
        return "I'm here to help with data analysis, calculations, and visualizations. You can ask me about data science concepts, upload files for analysis, or request charts and calculations. What would you like to do?"

def create_direct_chart(files, message):
    """Create charts directly in response to user queries"""
    try:
        for file in files:
            if file.endswith(('.csv', '.xlsx', '.xls')):
                filepath = os.path.join(UPLOAD_FOLDER, file)
                if file.endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)

                # Determine chart type from the message
                if 'pie' in message:
                    return create_pie_chart(df)
                elif 'line' in message:
                    return create_line_chart(df)
                elif 'bar' in message or 'column' in message:
                    return create_bar_chart(df)

                # Default to a bar chart if not specified
                return create_bar_chart(df)

        return "Error: No valid data files found to create a chart"
    except Exception as e:
        return f"Error: {str(e)}"

def create_pie_chart(df):
    """Create a pie chart from numerical data in the dataframe"""
    try:
        # For quality data, create pie chart of rejection reasons
        if 'Total Rej Qty.' in df.columns:
            # Get defect columns (excluding basic info columns)
            defect_columns = [col for col in df.columns 
                            if col not in ['Unnamed: 0', 'Date', 'Inspected Qty.', 'Part Name', 'Total Rej Qty.'] 
                            and not col.startswith('Unnamed')
                            and df[col].sum() > 0]
            
            if defect_columns:
                # Create pie chart data for defect types
                defect_data = []
                for col in defect_columns:
                    total = df[col].sum()
                    if total > 0:
                        defect_data.append({'Defect_Type': col, 'Count': total})
                
                if defect_data:
                    # Take top 10 defect types
                    defect_df = pd.DataFrame(defect_data).nlargest(10, 'Count')
                    fig = px.pie(defect_df, values='Count', names='Defect_Type', 
                               title='Top 10 Rejection Reasons Distribution')
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    return save_figure_as_base64(fig)
        
        # For general data, try to create a meaningful pie chart
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            # If there's a categorical column, group by it
            categorical_cols = df.select_dtypes(include=['object', 'string']).columns
            
            if len(categorical_cols) > 0 and len(df) > 1:
                # Group by first categorical column
                cat_col = categorical_cols[0]
                num_col = numeric_cols[0]
                
                # Aggregate data by category
                grouped_data = df.groupby(cat_col)[num_col].sum().nlargest(10)
                
                if not grouped_data.empty:
                    pie_data = pd.DataFrame({
                        'Category': grouped_data.index,
                        'Value': grouped_data.values
                    })
                    fig = px.pie(pie_data, values='Value', names='Category', 
                               title=f'Distribution of {num_col} by {cat_col}')
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    return save_figure_as_base64(fig)
            
            # If no categorical data, create a simple value distribution
            if len(df) > 1:
                # Create bins for the numeric data
                num_col = numeric_cols[0]
                df_clean = df[df[num_col].notna()].copy()
                
                if len(df_clean) > 0:
                    # Create value ranges
                    df_clean['Value_Range'] = pd.cut(df_clean[num_col], bins=5, precision=1)
                    range_counts = df_clean['Value_Range'].value_counts()
                    
                    if not range_counts.empty:
                        pie_data = pd.DataFrame({
                            'Range': range_counts.index.astype(str),
                            'Count': range_counts.values
                        })
                        fig = px.pie(pie_data, values='Count', names='Range', 
                                   title=f'Distribution of {num_col} Values')
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        return save_figure_as_base64(fig)
        
        return "Unable to create a meaningful pie chart from the available data. Pie charts work best with categorical data or defect type distributions."
    
    except Exception as e:
        return f"Error creating pie chart: {str(e)}"

def create_line_chart(df):
    """Create a line chart from numerical data in the dataframe"""
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        # Use date column if available, otherwise use index
        if 'Date' in df.columns:
            fig = px.line(df.head(50), x='Date', y=numeric_cols[0], title=f"Line Chart of {numeric_cols[0]} Over Time")
        else:
            fig = px.line(df.head(50), y=numeric_cols[0], title=f"Line Chart of {numeric_cols[0]}")
        return save_figure_as_base64(fig)
    return "No suitable numeric data found for a line chart."

def create_bar_chart(df):
    """Create a bar chart from numerical data in the dataframe"""
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        # For quality data, show top defect types
        if 'Total Rej Qty.' in df.columns:
            # Create bar chart of top rejection causes
            defect_columns = [col for col in df.columns 
                            if col not in ['Unnamed: 0', 'Date', 'Inspected Qty.', 'Part Name', 'Total Rej Qty.'] 
                            and df[col].sum() > 0]
            
            defect_data = []
            for col in defect_columns:
                total = df[col].sum()
                if total > 0:
                    defect_data.append({'Defect Type': col, 'Total Count': total})
            
            if defect_data:
                defect_df = pd.DataFrame(defect_data).nlargest(15, 'Total Count')
                fig = px.bar(defect_df, x='Defect Type', y='Total Count', 
                           title='Top 15 Rejection Causes',
                           labels={'Defect Type': 'Defect Type', 'Total Count': 'Total Rejections'})
                fig.update_layout(xaxis_tickangle=45)
                return save_figure_as_base64(fig)
        
        # Default bar chart
        fig = px.bar(df.head(20), y=numeric_cols[0], title=f"Bar Chart of {numeric_cols[0]}")
        return save_figure_as_base64(fig)
    return "No suitable numeric data found for a bar chart."

def save_figure_as_base64(fig):
    """Convert figure to base64 string for direct display"""
    try:
        # Convert to image bytes
        img_bytes = fig.to_image(format="png", width=800, height=600)
        # Convert to base64
        img_base64 = base64.b64encode(img_bytes).decode()
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        return f"Error generating chart: {str(e)}"

def calculate_rejection_percentage(files, user_message):
    """Calculate rejection percentage from uploaded files"""
    try:
        for file in files:
            if file.endswith(('.csv', '.xlsx', '.xls')):
                filepath = os.path.join(UPLOAD_FOLDER, file)
                if not os.path.exists(filepath):
                    continue
                    
                if file.endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)
                
                # Look for specific columns in the quality data
                rejection_col = None
                inspected_col = None
                
                # Find the exact column names
                for col in df.columns:
                    if 'Total Rej Qty.' in col:
                        rejection_col = col
                    elif 'Inspected Qty.' in col:
                        inspected_col = col
                
                if rejection_col and inspected_col:
                    total_rejected = df[rejection_col].sum()
                    total_inspected = df[inspected_col].sum()
                    
                    if total_inspected > 0:
                        rejection_percentage = (total_rejected / total_inspected) * 100
                        
                        # Additional analysis
                        avg_daily_rejected = total_rejected / len(df)
                        avg_daily_inspected = total_inspected / len(df)
                        max_daily_rejection = df[rejection_col].max()
                        min_daily_rejection = df[rejection_col].min()
                        
                        # Find top rejection types (excluding main columns)
                        defect_columns = [col for col in df.columns if col not in ['Unnamed: 0', 'Date', 'Inspected Qty.', 'Part Name', 'Total Rej Qty.'] and df[col].sum() > 0]
                        top_defects = []
                        for col in defect_columns:
                            defect_total = df[col].sum()
                            if defect_total > 0:
                                defect_percentage = (defect_total / total_rejected) * 100
                                top_defects.append((col, defect_total, defect_percentage))
                        
                        # Sort by quantity and take top 5
                        top_defects.sort(key=lambda x: x[1], reverse=True)
                        top_defects = top_defects[:5]
                        
                        analysis = f"""
🔍 **Quality Analysis for {file}**

📊 **Overall Rejection Percentage:**
• Total Rejected: {total_rejected:,} units
• Total Inspected: {total_inspected:,} units
• **Overall Rejection Rate: {rejection_percentage:.2f}%**

📈 **Daily Performance Metrics:**
• Data covers {len(df)} days
• Average daily rejections: {avg_daily_rejected:.1f} units
• Average daily inspections: {avg_daily_inspected:.1f} units
• Highest daily rejection: {max_daily_rejection} units
• Lowest daily rejection: {min_daily_rejection} units

🎯 **Top Rejection Causes:**"""
                        
                        for i, (defect, quantity, percentage) in enumerate(top_defects, 1):
                            analysis += f"\n{i}. {defect}: {quantity} units ({percentage:.1f}% of total rejections)"
                        
                        analysis += f"""

💡 **Quality Assessment:**
• Target rejection rate: < 2-5%
• Current performance: {rejection_percentage:.2f}% - {'⚠️ Needs improvement' if rejection_percentage > 5 else '✅ Within acceptable range'}
• Quality level: {'Poor' if rejection_percentage > 10 else 'Fair' if rejection_percentage > 5 else 'Good' if rejection_percentage > 2 else 'Excellent'}

📋 **Recommendations:**
• Focus on top {min(3, len(top_defects))} defect types for maximum impact
• Implement root cause analysis for high-frequency defects
• Consider process improvements for defects > 1% of total rejections"""
                        
                        return analysis
                
                # If no specific columns found, provide general guidance
                return f"""
                Found data file: {file} with {len(df)} rows and columns: {', '.join(df.columns.tolist())}
                
                To calculate rejection percentage, I need columns that indicate:
                1. Rejected/defective quantities
                2. Total produced quantities
                
                Please ensure your data has columns like 'Rejected', 'Defects', 'Total', 'Produced', etc.
                """
        
        return "No suitable data files found for rejection percentage calculation."
    
    except Exception as e:
        return f"Error calculating rejection percentage: {str(e)}"

def get_data_driven_response(message, files):
    """Provide data-driven responses based on available files"""
    global analyzer
    
    try:
        # Initialize analyzer if not already done
        if not analyzer:
            analyzer = initialize_analyzer(files)
        
        if analyzer:
            # Try to get response from intelligent analyzer
            response = analyzer.answer_question(message)
            if response and not response.startswith("❓"):
                return response
        
        # Fallback to basic file analysis
        available_files = os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
        
        if not available_files:
            return "❌ **No data files available.** Please upload a CSV or Excel file to analyze data."
        
        # Try to read the first available data file
        for file in available_files:
            if file.endswith(('.csv', '.xlsx', '.xls')):
                filepath = os.path.join(UPLOAD_FOLDER, file)
                try:
                    if file.endswith('.csv'):
                        df = pd.read_csv(filepath)
                    else:
                        df = pd.read_excel(filepath)
                    
                    # Basic data overview
                    return f"""
📊 **Data Overview from {file}:**
• Rows: {len(df):,}
• Columns: {len(df.columns)}
• Available data: {', '.join(df.columns.tolist()[:5])}{'...' if len(df.columns) > 5 else ''}

💡 **Available Analysis:**
- Upload your data and ask specific questions
- Request charts and visualizations  
- Get statistical summaries
- Analyze trends and patterns

🔍 **Example Questions:**
- "Which part has the highest rejection?"
- "Show me a pie chart of defect types"
- "What's the rejection rate?"
                    """
                except Exception as e:
                    continue
        
        return "❌ **Unable to read data files.** Please ensure you've uploaded valid CSV or Excel files."
        
    except Exception as e:
        return f"❌ **Error:** {str(e)}\n\nPlease try uploading your data file again."

def generate_analysis_response(files):
    """Generate analysis based on uploaded files"""
    try:
        analysis_results = []
        for file in files:
            if file.endswith(('.csv', '.xlsx')):
                filepath = os.path.join(UPLOAD_FOLDER, file)
                if file.endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)
                
                analysis = f"""
                Data Analysis for {file}:
                - Shape: {df.shape[0]} rows, {df.shape[1]} columns
                - Columns: {', '.join(df.columns.tolist())}
                - Missing values: {df.isnull().sum().sum()} total
                """
                
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    analysis += f"\n- Numeric columns summary: {', '.join(numeric_cols)}"
                
                analysis_results.append(analysis)
        
        return '\n\n'.join(analysis_results) if analysis_results else "No analyzable files found."
    except Exception as e:
        return f"Error analyzing data: {str(e)}"

@app.route('/api/generate-chart', methods=['POST'])
def generate_chart():
    data = request.get_json()
    chart_type = data.get('chart_type', 'bar')
    filename = data.get('filename', '')
    column = data.get('column', '')
    
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        # Generate chart based on type
        if chart_type == 'pie':
            fig = px.pie(df.head(10), values=column, title=f"Pie Chart of {column}")
        elif chart_type == 'line':
            fig = px.line(df.head(20), y=column, title=f"Line Chart of {column}")
        else:  # bar chart
            fig = px.bar(df.head(10), y=column, title=f"Bar Chart of {column}")
        
        # Convert to base64 for frontend
        img_bytes = fig.to_image(format="png")
        img_base64 = base64.b64encode(img_bytes).decode()
        
        return jsonify({
            'chart_image': f"data:image/png;base64,{img_base64}",
            'message': f'Generated {chart_type} chart for {column}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
