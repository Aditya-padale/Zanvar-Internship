import os
import json
from datetime import datetime

def handler(request):
    """Simple health check for Vercel"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'environment': 'vercel' if os.getenv('VERCEL') else 'local',
            'deployment_id': os.getenv('VERCEL_DEPLOYMENT_ID', 'local'),
            'message': 'Lightweight Data Analysis API is running',
            'version': '2.0-serverless'
        })
    }

# For Vercel
def main(event, context):
    return handler(event)
