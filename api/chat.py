import os
import json
from datetime import datetime

try:
    import google.generativeai as genai
    HAS_GOOGLE_AI = True
except ImportError:
    genai = None
    HAS_GOOGLE_AI = False

# Conversation memory to track context
conversation_memory = {
    'last_question': '',
    'last_answer': '',
    'mentioned_parts': [],
    'uploaded_files': []
}

def is_data_question(message):
    """Check if the message is asking for data analysis or charts"""
    data_keywords = [
        'chart', 'graph', 'plot', 'visualize', 'analyze', 'data', 'statistics',
        'trend', 'pattern', 'correlation', 'distribution', 'summary', 'insight',
        'bar chart', 'line chart', 'pie chart', 'histogram', 'scatter plot',
        'show me', 'create', 'generate', 'make a', 'draw'
    ]
    
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in data_keywords)

def get_fallback_response(message, files):
    """Provide fallback responses when Google AI is not available"""
    
    message_lower = message.lower()
    
    # Chart/visualization requests
    if any(word in message_lower for word in ['chart', 'graph', 'plot', 'visualize']):
        if files:
            return {
                'response': "I can help you create charts from your uploaded data. However, Google AI is currently not available, so I'm providing a basic response. To create specific charts, please specify:\n\n1. **Chart type**: pie chart, bar chart, line chart, etc.\n2. **Which columns** to use from your data\n3. **Any specific filtering** you want\n\nFor example: 'Create a pie chart showing the distribution of categories' or 'Make a line chart of sales over time'.",
                'chart_suggestions': [
                    "Pie chart for categorical data distribution",
                    "Bar chart for comparing categories", 
                    "Line chart for trends over time",
                    "Scatter plot for relationships between variables"
                ]
            }
        else:
            return {
                'response': "To create charts, please first upload a data file (CSV or Excel). I can then help you visualize your data with various chart types like pie charts, bar charts, line charts, and more."
            }
    
    # Data analysis requests
    elif any(word in message_lower for word in ['analyze', 'analysis', 'insights', 'summary']):
        if files:
            return {
                'response': "I can help analyze your uploaded data. While Google AI is not available for advanced insights, I can provide:\n\n• **Basic statistics** (mean, median, mode)\n• **Data summary** (row/column counts, data types)\n• **Missing value analysis**\n• **Simple visualizations**\n\nPlease be more specific about what aspect of the data you'd like to analyze."
            }
        else:
            return {
                'response': "To analyze data, please upload a data file (CSV or Excel) first. I can then provide statistical summaries, identify patterns, and create visualizations based on your data."
            }
    
    # Greeting/general conversation
    elif any(word in message_lower for word in ['hello', 'hi', 'help', 'what can you do']):
        return {
            'response': "Hello! I'm your data analysis assistant. I can help you:\n\n📊 **Upload and analyze data** (CSV, Excel files)\n📈 **Create various charts** (pie, bar, line, scatter plots)\n🔍 **Provide data insights** and statistical summaries\n💡 **Answer questions** about your data\n\nTo get started, upload a data file and ask me questions like:\n• 'Show me a summary of the data'\n• 'Create a pie chart of categories'\n• 'What are the trends in this data?'\n\nWhat would you like to do today?"
        }
    
    # Default response
    else:
        return {
            'response': f"I understand you're asking: '{message}'\n\nI'm a data analysis assistant, and I work best with data files and specific requests for analysis or visualization. Here's how I can help:\n\n🔤 **For general questions**: I can provide information about data analysis concepts\n📊 **For data work**: Upload a CSV/Excel file and ask for charts, summaries, or insights\n📈 **For visualizations**: Request specific chart types with your uploaded data\n\nGoogle AI services are currently unavailable, so responses are limited. Please upload data files for the best experience!"
        }

def process_user_query(message, files):
    """Process user query with enhanced context awareness"""
    
    # Update conversation memory
    conversation_memory['last_question'] = message
    
    # Check if it's a data analysis question
    if is_data_question(message):
        if not files:
            return get_fallback_response(message, files)
    
    # Use Google AI if available
    if HAS_GOOGLE_AI and os.getenv('GOOGLE_API_KEY'):
        try:
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            model = genai.GenerativeModel('gemini-pro')
            
            # Create context from uploaded files
            context = get_file_context(files)
            
            # Enhanced prompt with conversation memory
            prompt = f"""
            You are an intelligent data analysis assistant. 
            
            User's question: {message}
            
            Context from uploaded files:
            {context}
            
            Previous conversation:
            Last question: {conversation_memory.get('last_question', 'None')}
            Last answer: {conversation_memory.get('last_answer', 'None')}
            
            Please provide a helpful, accurate response. If the user is asking for data analysis or charts, 
            guide them on what's possible with their uploaded data. Be conversational and helpful.
            """
            
            response = model.generate_content(prompt)
            answer = response.text
            
            # Update memory
            conversation_memory['last_answer'] = answer
            
            return {'response': answer}
            
        except Exception as e:
            print(f"Google AI error: {str(e)}")
            return get_fallback_response(message, files)
    else:
        return get_fallback_response(message, files)

def get_file_context(files):
    """Generate context string from uploaded files"""
    if not files:
        return "No files uploaded yet."
    
    context_parts = []
    for file_info in files:
        if isinstance(file_info, dict):
            file_type = file_info.get('type', 'unknown')
            shape = file_info.get('shape', [0, 0])
            columns = file_info.get('columns', [])
            
            context_parts.append(f"""
            File Type: {file_type}
            Dimensions: {shape[0]} rows, {shape[1]} columns
            Columns: {', '.join(columns[:10])}{'...' if len(columns) > 10 else ''}
            """)
    
    return '\n'.join(context_parts) if context_parts else "File information not available."

def handler(request):
    """Lightweight chat handler for Vercel"""
    method = request.get('method') if isinstance(request, dict) else getattr(request, 'method', 'GET')
    
    if method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse request body
        if hasattr(request, 'get_json'):
            data = request.get_json()
        else:
            # Handle Vercel's event format
            body = request.get('body', '{}') if isinstance(request, dict) else '{}'
            data = json.loads(body)
        
        if not data or 'message' not in data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No message provided'})
            }
        
        message = data['message']
        files = data.get('files', [])
        
        # Process the query
        result = process_user_query(message, files)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'success': True,
                'response': result['response'],
                'timestamp': datetime.now().isoformat()
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Chat processing failed: {str(e)}'})
        }

# For Vercel
def main(event, context):
    return handler(event)
