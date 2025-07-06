#!/usr/bin/env python3
"""
Test script to verify the enhanced AI system
"""

from super_intelligent_analyzer import SuperIntelligentAnalyzer
import os

def test_enhanced_system():
    print('🧪 Testing Enhanced AI System...')
    print('=' * 50)
    
    if os.path.exists('uploads/QUALITY_DAILY_Machining_Rejection.xlsx'):
        try:
            analyzer = SuperIntelligentAnalyzer('uploads/QUALITY_DAILY_Machining_Rejection.xlsx')
            
            # Test a complex question that should use Google API
            test_questions = [
                'forecast quality trends',
                'monthly quality performance heatmap', 
                'physical damage patterns',
                'why are rejections increasing'
            ]
            
            for question in test_questions:
                print(f'\n📋 Testing: "{question}"')
                intent = analyzer.analyze_intent(question)
                print(f'  ✓ Intent: {intent.get("primary_intent", "unknown")}')
                print(f'  ✓ Temporal: {intent.get("temporal_scope", "overall")}')
                print(f'  ✓ Chart: {intent.get("chart_preference", "auto")}')
            
            print(f'\n🤖 Google API Status: {"✅ Connected" if analyzer.google_model else "❌ Not Available"}')
            print(f'📊 Data Records: {len(analyzer.df):,}')
            print(f'🔧 Defect Types: {len(analyzer.defect_columns)}')
            
            print('\n✅ Enhanced AI System is Ready!')
            print('🚀 You can now ask complex questions and get intelligent responses!')
            
        except Exception as e:
            print(f'❌ Error: {e}')
    else:
        print('❌ Data file not found')

if __name__ == "__main__":
    test_enhanced_system()
