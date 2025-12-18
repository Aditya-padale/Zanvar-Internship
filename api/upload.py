import os
import json
import tempfile
import base64
from datetime import datetime

def handler(request):
    """Lightweight file upload handler for Vercel"""
    method = request.get('method') if isinstance(request, dict) else getattr(request, 'method', 'GET')
    
    if method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # For now, just simulate file upload success
        # In a real serverless environment, you'd upload to cloud storage
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
                'message': 'File upload endpoint is working! For full functionality, integrate with cloud storage.',
                'timestamp': datetime.now().isoformat(),
                'note': 'This is a lightweight version optimized for Vercel deployment size limits.'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Upload failed: {str(e)}'})
        }

# For Vercel
def main(event, context):
    return handler(event)
