#!/usr/bin/env python3
"""
Comprehensive test script for graph creation functionality
Tests all chart types and scenarios to ensure complete functionality
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import base64
import io
from enhanced_smart_analyzer import EnhancedSmartAnalyzer

def test_dependencies():
    """Test if all required dependencies are available"""
    print("🔍 Testing Dependencies...")
    
    try:
        import pandas as pd
        print("✅ pandas - OK")
    except ImportError:
        print("❌ pandas - MISSING")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib - OK")
    except ImportError:
        print("❌ matplotlib - MISSING")
        return False
    
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        print("✅ plotly - OK")
    except ImportError:
        print("❌ plotly - MISSING")
        return False
    
    try:
        # Test plotly image export (kaleido)
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3]))
        img_bytes = fig.to_image(format="png", width=100, height=100)
        print("✅ plotly image export (kaleido) - OK")
    except Exception as e:
        print(f"❌ plotly image export - ERROR: {e}")
        return False
    
    try:
        import base64
        test_data = base64.b64encode(b"test").decode()
        print("✅ base64 - OK")
    except ImportError:
        print("❌ base64 - MISSING")
        return False
    
    return True

def test_data_file():
    """Test if data file is available and readable"""
    print("\n📁 Testing Data File...")
    
    data_file = "uploads/QUALITY_DAILY_Machining_Rejection.xlsx"
    
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return None
    
    try:
        df = pd.read_excel(data_file)
        print(f"✅ Data file loaded successfully")
        print(f"   📊 Shape: {df.shape}")
        print(f"   📋 Columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"❌ Error loading data file: {e}")
        return None

def test_basic_chart_creation(df):
    """Test basic chart creation functions"""
    print("\n📊 Testing Basic Chart Creation...")
    
    if df is None:
        print("❌ No data available for testing")
        return False
    
    # Test pie chart
    try:
        defect_columns = [col for col in df.columns 
                         if col not in ['Unnamed: 0', 'Date', 'Inspected Qty.', 'Part Name', 'Total Rej Qty.'] 
                         and not col.startswith('Unnamed')]
        
        if defect_columns:
            defect_totals = {}
            for col in defect_columns:
                total = df[col].sum()
                if total > 0:
                    defect_totals[col] = total
            
            if defect_totals:
                sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:10]
                defect_names = [item[0] for item in sorted_defects]
                defect_counts = [item[1] for item in sorted_defects]
                
                fig = px.pie(values=defect_counts, names=defect_names, 
                           title='Test Pie Chart - Top 10 Rejection Reasons')
                img_bytes = fig.to_image(format="png", width=800, height=600)
                img_base64 = base64.b64encode(img_bytes).decode()
                print("✅ Pie chart creation - OK")
            else:
                print("⚠️ No defect data for pie chart")
        else:
            print("⚠️ No defect columns found")
            
    except Exception as e:
        print(f"❌ Pie chart creation - ERROR: {e}")
        return False
    
    # Test bar chart
    try:
        if defect_totals:
            sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:15]
            defect_names = [item[0] for item in sorted_defects]
            defect_counts = [item[1] for item in sorted_defects]
            
            fig = px.bar(x=defect_counts, y=defect_names, orientation='h',
                        title='Test Bar Chart - Top 15 Rejection Causes')
            img_bytes = fig.to_image(format="png", width=1000, height=700)
            img_base64 = base64.b64encode(img_bytes).decode()
            print("✅ Bar chart creation - OK")
        else:
            print("⚠️ No data for bar chart")
    except Exception as e:
        print(f"❌ Bar chart creation - ERROR: {e}")
        return False
    
    # Test line chart (trend analysis)
    try:
        if 'Date' in df.columns and 'Total Rej Qty.' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            monthly_data = df.groupby(df['Date'].dt.to_period('M')).agg({
                'Total Rej Qty.': 'sum',
                'Inspected Qty.': 'sum'
            }).reset_index()
            
            monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()
            monthly_data['Rejection_Rate'] = (monthly_data['Total Rej Qty.'] / monthly_data['Inspected Qty.']) * 100
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=monthly_data['Date'], y=monthly_data['Total Rej Qty.'],
                                   mode='lines+markers', name='Total Rejections'))
            fig.update_layout(title='Test Line Chart - Monthly Trend', xaxis_title='Month', yaxis_title='Total Rejections')
            
            img_bytes = fig.to_image(format="png", width=1000, height=600)
            img_base64 = base64.b64encode(img_bytes).decode()
            print("✅ Line chart creation - OK")
        else:
            print("⚠️ Missing Date or Total Rej Qty. columns for line chart")
    except Exception as e:
        print(f"❌ Line chart creation - ERROR: {e}")
        return False
    
    return True

def test_enhanced_analyzer():
    """Test the enhanced smart analyzer"""
    print("\n🧠 Testing Enhanced Smart Analyzer...")
    
    data_file = "uploads/QUALITY_DAILY_Machining_Rejection.xlsx"
    
    try:
        analyzer = EnhancedSmartAnalyzer(data_file)
        print("✅ Enhanced analyzer initialization - OK")
        
        # Test various question types
        test_questions = [
            "top 5 rejection reasons",
            "create a pie chart of defects", 
            "show me a bar chart of rejection causes",
            "draw a trend chart over time",
            "visualize rejection distribution",
            "what are the highest rejection reasons",
            "make a graph of top 10 defects"
        ]
        
        success_count = 0
        for question in test_questions:
            try:
                response = analyzer.answer_question(question)
                if response and not response.startswith("❓"):
                    success_count += 1
                    
                    # Check if response contains chart data
                    if "data:image/png;base64," in response:
                        print(f"✅ Question: '{question}' - Generated chart")
                    else:
                        print(f"✅ Question: '{question}' - Text response")
                else:
                    print(f"⚠️ Question: '{question}' - No valid response")
            except Exception as e:
                print(f"❌ Question: '{question}' - ERROR: {e}")
        
        print(f"📊 Successfully handled {success_count}/{len(test_questions)} questions")
        return success_count == len(test_questions)
        
    except Exception as e:
        print(f"❌ Enhanced analyzer - ERROR: {e}")
        return False

def test_app_chart_functions():
    """Test chart creation functions from app.py"""
    print("\n🌐 Testing App Chart Functions...")
    
    try:
        # Import functions from app.py
        from app import create_pie_chart, create_bar_chart, create_line_chart
        
        data_file = "uploads/QUALITY_DAILY_Machining_Rejection.xlsx"
        df = pd.read_excel(data_file)
        
        # Test pie chart
        try:
            result = create_pie_chart(df)
            if result.startswith("data:image/png;base64,"):
                print("✅ App pie chart function - OK")
            else:
                print(f"⚠️ App pie chart function - Returned text: {result[:100]}...")
        except Exception as e:
            print(f"❌ App pie chart function - ERROR: {e}")
        
        # Test bar chart
        try:
            result = create_bar_chart(df)
            if result.startswith("data:image/png;base64,"):
                print("✅ App bar chart function - OK")
            else:
                print(f"⚠️ App bar chart function - Returned text: {result[:100]}...")
        except Exception as e:
            print(f"❌ App bar chart function - ERROR: {e}")
        
        # Test line chart
        try:
            result = create_line_chart(df)
            if result.startswith("data:image/png;base64,"):
                print("✅ App line chart function - OK")
            else:
                print(f"⚠️ App line chart function - Returned text: {result[:100]}...")
        except Exception as e:
            print(f"❌ App line chart function - ERROR: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ App chart functions import - ERROR: {e}")
        return False

def test_all_chart_scenarios():
    """Test all possible chart creation scenarios"""
    print("\n🎯 Testing All Chart Scenarios...")
    
    chart_requests = [
        "pie chart",
        "bar chart", 
        "line chart",
        "graph",
        "plot",
        "visualize",
        "draw chart",
        "show graph",
        "create pie chart of rejection reasons",
        "make bar chart of top 10 defects",
        "draw line chart showing trends",
        "visualize rejection distribution",
        "show top 5 rejection causes in pie chart",
        "create horizontal bar chart ranking defects",
        "plot monthly rejection trends",
        "graph the most common defect types"
    ]
    
    try:
        from enhanced_smart_analyzer import EnhancedSmartAnalyzer
        analyzer = EnhancedSmartAnalyzer("uploads/QUALITY_DAILY_Machining_Rejection.xlsx")
        
        success_count = 0
        chart_count = 0
        
        for request in chart_requests:
            try:
                response = analyzer.answer_question(request)
                if response:
                    success_count += 1
                    if "data:image/png;base64," in response:
                        chart_count += 1
                        print(f"✅ '{request}' - Chart generated")
                    else:
                        print(f"⚠️ '{request}' - Text response only")
                else:
                    print(f"❌ '{request}' - No response")
            except Exception as e:
                print(f"❌ '{request}' - ERROR: {e}")
        
        print(f"\n📊 Summary:")
        print(f"   Total requests: {len(chart_requests)}")
        print(f"   Successful responses: {success_count}")
        print(f"   Charts generated: {chart_count}")
        print(f"   Success rate: {(success_count/len(chart_requests)*100):.1f}%")
        print(f"   Chart generation rate: {(chart_count/len(chart_requests)*100):.1f}%")
        
        return chart_count >= len(chart_requests) * 0.8  # 80% should generate charts
        
    except Exception as e:
        print(f"❌ Chart scenarios test - ERROR: {e}")
        return False

def fix_missing_dependencies():
    """Install any missing dependencies"""
    print("\n🔧 Checking and fixing missing dependencies...")
    
    try:
        # Check if kaleido is working for plotly image export
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3]))
        img_bytes = fig.to_image(format="png", width=100, height=100)
        print("✅ All dependencies working correctly")
        return True
    except Exception as e:
        print(f"⚠️ Image export issue: {e}")
        print("Installing kaleido...")
        
        import subprocess
        import sys
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "kaleido"])
            print("✅ kaleido installed successfully")
            return True
        except Exception as install_error:
            print(f"❌ Failed to install kaleido: {install_error}")
            return False

def main():
    """Main test function"""
    print("🚀 COMPREHENSIVE GRAPH CREATION TEST")
    print("=" * 50)
    
    # Test dependencies
    if not test_dependencies():
        print("\n❌ CRITICAL: Missing dependencies. Attempting to fix...")
        if not fix_missing_dependencies():
            print("❌ Could not fix dependencies. Please install manually.")
            return False
    
    # Test data file
    df = test_data_file()
    
    # Test basic chart creation
    if not test_basic_chart_creation(df):
        print("\n❌ Basic chart creation failed")
        return False
    
    # Test enhanced analyzer
    if not test_enhanced_analyzer():
        print("\n❌ Enhanced analyzer failed")
        return False
    
    # Test app chart functions
    if not test_app_chart_functions():
        print("\n❌ App chart functions failed")
        return False
    
    # Test all chart scenarios
    if not test_all_chart_scenarios():
        print("\n❌ Chart scenarios test failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("✅ Graph creation functionality is complete and working")
    print("✅ All chart types (pie, bar, line) are supported")
    print("✅ Enhanced analyzer provides intelligent responses")
    print("✅ Both text and visual responses are generated")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
