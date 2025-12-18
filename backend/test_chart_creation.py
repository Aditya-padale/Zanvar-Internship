#!/usr/bin/env python3
"""
Test script to debug chart creation issues
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64
import os

def test_simple_pie_chart():
    """Test creating a simple pie chart"""
    try:
        # Create sample data
        labels = ['Defect A', 'Defect B', 'Defect C', 'Defect D', 'Defect E']
        values = [40, 30, 20, 15, 10]
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            textinfo='label+percent+value',
            textposition='outside'
        )])
        
        fig.update_layout(
            title='Test Pie Chart',
            width=800,
            height=600
        )
        
        # Try to convert to image
        print("Converting to image...")
        img_bytes = fig.to_image(format="png", width=800, height=600)
        img_base64 = base64.b64encode(img_bytes).decode()
        
        print(f"✅ Image created successfully! Size: {len(img_base64)} characters")
        print(f"Base64 preview (first 100 chars): {img_base64[:100]}...")
        
        # Save to file for testing
        chart_path = os.path.join("generated_charts", "test_pie_chart.png")
        os.makedirs("generated_charts", exist_ok=True)
        
        with open(chart_path, "wb") as f:
            f.write(img_bytes)
        
        print(f"✅ Chart saved to: {chart_path}")
        
        return True, img_base64
        
    except Exception as e:
        print(f"❌ Error creating pie chart: {e}")
        return False, str(e)

def test_with_real_data():
    """Test with actual uploaded data"""
    try:
        # Check available data files
        upload_files = []
        upload_dir = "uploads"
        if os.path.exists(upload_dir):
            upload_files = [f for f in os.listdir(upload_dir) if f.endswith(('.xlsx', '.csv'))]
            print(f"Found upload files: {upload_files}")
        
        if not upload_files:
            print("No data files found in uploads directory")
            return False, "No data"
        
        # Load first Excel file
        data_path = os.path.join(upload_dir, upload_files[0])
        print(f"Loading data from: {data_path}")
        
        df = pd.read_excel(data_path)
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Look for defect columns (columns with numeric data that might represent defects)
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        print(f"Numeric columns: {numeric_cols}")
        
        # Create pie chart from top 5 numeric columns by sum
        defect_totals = {}
        for col in numeric_cols:
            total = df[col].sum()
            if total > 0:
                defect_totals[col] = total
        
        if not defect_totals:
            print("No positive numeric data found for chart creation")
            return False, "No defect data"
        
        # Get top 5
        sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        labels = [item[0] for item in sorted_defects]
        values = [item[1] for item in sorted_defects]
        
        print(f"Chart data - Labels: {labels}, Values: {values}")
        
        # Create chart
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            textinfo='label+percent+value',
            textposition='outside'
        )])
        
        fig.update_layout(
            title=f'Top {len(labels)} Categories from {upload_files[0]}',
            width=800,
            height=600
        )
        
        # Convert to image
        img_bytes = fig.to_image(format="png", width=800, height=600)
        img_base64 = base64.b64encode(img_bytes).decode()
        
        print(f"✅ Real data chart created! Size: {len(img_base64)} characters")
        
        # Save chart
        chart_path = os.path.join("generated_charts", "real_data_pie_chart.png")
        with open(chart_path, "wb") as f:
            f.write(img_bytes)
        
        print(f"✅ Chart saved to: {chart_path}")
        
        return True, img_base64
        
    except Exception as e:
        print(f"❌ Error with real data: {e}")
        import traceback
        traceback.print_exc()
        return False, str(e)

if __name__ == "__main__":
    print("=== Testing Chart Creation ===")
    
    print("\n1. Testing simple pie chart...")
    success1, result1 = test_simple_pie_chart()
    
    print("\n2. Testing with real data...")
    success2, result2 = test_with_real_data()
    
    if success1 and success2:
        print("\n✅ All tests passed! Chart creation is working.")
    else:
        print(f"\n❌ Some tests failed:")
        if not success1:
            print(f"  Simple chart: {result1}")
        if not success2:
            print(f"  Real data: {result2}")
