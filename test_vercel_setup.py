#!/usr/bin/env python3
"""
Simple test script to verify serverless functions work locally
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from api.serverless_analyzer import ServerlessAnalyzer
import pandas as pd
import tempfile

def test_analyzer():
    """Test the serverless analyzer with sample data"""
    print("Testing ServerlessAnalyzer...")
    
    # Create sample CSV data
    sample_data = {
        'Category': ['A', 'B', 'C', 'A', 'B', 'C', 'A'],
        'Values': [10, 20, 15, 25, 30, 18, 12],
        'Date': pd.date_range('2023-01-01', periods=7)
    }
    
    df = pd.DataFrame(sample_data)
    
    # Save to temporary CSV
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        temp_file = f.name
    
    try:
        # Test analyzer
        analyzer = ServerlessAnalyzer()
        
        # Test data loading
        print("✓ Loading data...")
        success = analyzer.load_data(temp_file, 'csv')
        if not success:
            print("✗ Failed to load data")
            return False
        
        # Test summary
        print("✓ Creating summary...")
        summary = analyzer.get_basic_summary()
        if summary is None:
            print("✗ Failed to create summary")
            return False
        
        print(f"  - Shape: {summary['shape']}")
        print(f"  - Columns: {summary['columns']}")
        
        # Test pie chart
        print("✓ Creating pie chart...")
        pie_chart = analyzer.create_pie_chart('Category')
        if pie_chart is None:
            print("✗ Failed to create pie chart")
            return False
        
        print(f"  - Chart type: {pie_chart['type']}")
        print(f"  - Column: {pie_chart['column']}")
        
        # Test bar chart
        print("✓ Creating bar chart...")
        bar_chart = analyzer.create_bar_chart('Category')
        if bar_chart is None:
            print("✗ Failed to create bar chart")
            return False
        
        print(f"  - Chart type: {bar_chart['type']}")
        
        # Test line chart
        print("✓ Creating line chart...")
        line_chart = analyzer.create_line_chart(None, 'Values')
        if line_chart is None:
            print("✗ Failed to create line chart")
            return False
        
        print(f"  - Chart type: {line_chart['type']}")
        
        print("\n✅ All tests passed! Serverless analyzer is working correctly.")
        return True
        
    finally:
        # Clean up
        os.unlink(temp_file)

def test_api_imports():
    """Test that API modules can be imported"""
    print("Testing API imports...")
    
    try:
        # Test health endpoint
        print("✓ Importing health...")
        import api.health
        
        # Test upload endpoint  
        print("✓ Importing upload...")
        import api.upload
        
        # Test chat endpoint
        print("✓ Importing chat...")
        import api.chat
        
        # Test charts endpoint
        print("✓ Importing charts...")
        import api.charts
        
        print("✅ All API modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Vercel Serverless Setup\n")
    
    # Test imports
    imports_ok = test_api_imports()
    print()
    
    # Test analyzer
    analyzer_ok = test_analyzer()
    
    if imports_ok and analyzer_ok:
        print("\n🎉 All tests passed! Ready for Vercel deployment.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)
