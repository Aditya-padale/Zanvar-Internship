#!/usr/bin/env python3
"""
Test the actual analyzer to make sure chart creation works in the real system
"""
import sys
import os
sys.path.append('.')

from super_intelligent_analyzer import SuperIntelligentAnalyzer
import pandas as pd

def test_analyzer_chart_creation():
    """Test the actual analyzer with chart creation"""
    try:
        # Initialize analyzer with data path
        data_path = "uploads/QUALITY_DAILY_Machining_Rejection.xlsx"
        if not os.path.exists(data_path):
            print(f"❌ Data file not found: {data_path}")
            return False
        
        print(f"Initializing analyzer with data from: {data_path}")
        analyzer = SuperIntelligentAnalyzer(data_path)
        
        # Test various chart queries
        test_queries = [
            "create a pie chart of top 5 defects",
            "make a pie chart showing the top rejection reasons",
            "show me a pie chart of the main defect types",
            "create pie chart for defect analysis",
            "pie chart of top 5 rejection categories"
        ]
        
        print(f"Testing {len(test_queries)} different chart queries...")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- Test {i}: '{query}' ---")
            
            try:
                result = analyzer.answer_question(query)
                
                # Check if result contains chart (base64 image)
                if "data:image/png;base64," in result:
                    print(f"✅ Chart created successfully! Response length: {len(result)} characters")
                    
                    # Extract base64 part for verification
                    base64_start = result.find("data:image/png;base64,") + len("data:image/png;base64,")
                    base64_data = result[base64_start:base64_start+100]  # First 100 chars
                    print(f"   Base64 preview: {base64_data}...")
                else:
                    print(f"❌ No chart found in response")
                    print(f"   Response preview: {result[:200]}...")
                    
            except Exception as e:
                print(f"❌ Error with query: {e}")
                import traceback
                traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing analyzer: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Testing Actual Analyzer Chart Creation ===")
    success = test_analyzer_chart_creation()
    
    if success:
        print("\n✅ Analyzer chart creation test completed!")
    else:
        print("\n❌ Analyzer test failed!")
