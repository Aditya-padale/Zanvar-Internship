from flask import jsonify
import os
from datetime import datetime

def handler(request):
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'environment': 'vercel' if os.getenv('VERCEL') else 'local',
        'deployment_id': os.getenv('VERCEL_DEPLOYMENT_ID', 'local'),
        'message': 'Data Analysis API is running'
    })

# For Vercel
def main(request):
    return handler(request)
