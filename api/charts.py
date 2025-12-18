import os
import json
from datetime import datetime

def handler(request):
    """Lightweight chart creation endpoint for Vercel"""
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
            data = json.loads(request.get('body', '{}'))
        
        if not data:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No data provided'})
            }
        
        chart_type = data.get('chart_type', 'pie')
        
        # For now, return a placeholder response
        # In production, you'd integrate with a chart generation service
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
                'message': f'Chart generation endpoint is working! Requested chart type: {chart_type}',
                'timestamp': datetime.now().isoformat(),
                'note': 'This is a lightweight version. For full chart generation, consider using external services like QuickChart or Chart.js on the frontend.',
                'suggestion': 'Implement chart generation in the frontend using Chart.js or integrate with cloud-based chart APIs.'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Chart creation failed: {str(e)}'})
        }

# For Vercel
def main(event, context):
    return handler(event)
