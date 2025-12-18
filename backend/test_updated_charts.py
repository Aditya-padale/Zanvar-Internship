#!/usr/bin/env python3
"""
Test the updated chart generation with file saving
"""
import sys
import os
sys.path.append('.')

from super_intelligent_analyzer import SuperIntelligentAnalyzer

def test_updated_chart():
    """Test the updated chart generation"""
    try:
        # Initialize analyzer with data path
        data_path = "uploads/QUALITY_DAILY_Machining_Rejection.xlsx"
        if not os.path.exists(data_path):
            print(f"❌ Data file not found: {data_path}")
            return False
        
        print(f"Initializing analyzer with data from: {data_path}")
        analyzer = SuperIntelligentAnalyzer(data_path)
        
        # Test pie chart creation
        query = "create a pie chart of top 5 defects"
        print(f"\n--- Testing: '{query}' ---")
        
        result = analyzer.answer_question(query)
        
        # Check if result contains chart (base64 image)
        if "data:image/png;base64," in result:
            print(f"✅ Chart created successfully!")
            
            # Check if HTML img tag is present
            if '<img src="data:image/png;base64,' in result:
                print(f"✅ HTML img tag found!")
            else:
                print(f"❌ HTML img tag not found")
            
            # Check if markdown image is present
            if '![Pie Chart](data:image/png;base64,' in result:
                print(f"✅ Markdown image found!")
            else:
                print(f"❌ Markdown image not found")
            
            # Check if file was saved
            generated_charts_dir = "generated_charts"
            if os.path.exists(generated_charts_dir):
                files = [f for f in os.listdir(generated_charts_dir) if f.startswith('pie_chart_') and f.endswith('.png')]
                if files:
                    print(f"✅ Chart file saved: {files[-1]}")
                else:
                    print(f"❌ No chart files found in {generated_charts_dir}")
            else:
                print(f"❌ Directory {generated_charts_dir} not found")
                
            # Print a sample of the response
            print(f"\nResponse sample (first 300 chars):")
            print(result[:300] + "...")
            
        else:
            print(f"❌ No chart found in response")
            print(f"Response preview: {result[:200]}...")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Testing Updated Chart Generation ===")
    success = test_updated_chart()
    
    if success:
        print("\n✅ Updated chart generation test completed!")
    else:
        print("\n❌ Test failed!")
