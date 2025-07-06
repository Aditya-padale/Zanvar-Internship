import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import base64
import io
import re
from collections import Counter
import os

try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except ImportError:
    HAS_TEXTBLOB = False
    print("⚠️ TextBlob not available - using basic NLP")

try:
    import nltk
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False
    print("⚠️ NLTK not available - using basic processing")

class EnhancedSmartAnalyzer:
    def __init__(self, file_path):
        """Initialize the enhanced analyzer with better NLP capabilities"""
        self.file_path = file_path
        self.df = None
        self.defect_columns = []
        self.metadata = {}
        self.conversation_context = {
            'last_question': '',
            'last_answer': '',
            'current_focus': None,  # 'parts', 'defects', 'trends', etc.
            'mentioned_entities': [],
            'chart_preferences': {}
        }
        
        # Initialize NLP components
        self.initialize_nlp()
        
        # Load and analyze data
        self.load_and_analyze_data()
        
        # Create semantic understanding patterns
        self.setup_semantic_patterns()
    
    def initialize_nlp(self):
        """Initialize NLP components for better text understanding"""
        try:
            if HAS_NLTK:
                # Download required NLTK data if not present
                import nltk
                try:
                    nltk.download('punkt', quiet=True)
                    nltk.download('stopwords', quiet=True)
                    nltk.download('wordnet', quiet=True)
                    
                    from nltk.corpus import stopwords
                    from nltk.tokenize import word_tokenize
                    from nltk.stem import WordNetLemmatizer
                    
                    self.stop_words = set(stopwords.words('english'))
                    self.lemmatizer = WordNetLemmatizer()
                    print("✅ NLTK components initialized")
                except:
                    self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
                    self.lemmatizer = None
            else:
                self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
                self.lemmatizer = None
                
        except Exception as e:
            print(f"⚠️ NLP initialization warning: {e}")
            # Fallback to basic processing
            self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
            self.lemmatizer = None
    
    def setup_semantic_patterns(self):
        """Setup semantic patterns for better understanding"""
        self.chart_type_patterns = {
            'pie': {
                'keywords': ['pie', 'distribution', 'proportion', 'percentage', 'share', 'breakdown'],
                'phrases': ['pie chart', 'show distribution', 'break down', 'proportion of'],
                'best_for': ['categorical data', 'parts distribution', 'defect distribution']
            },
            'bar': {
                'keywords': ['bar', 'compare', 'comparison', 'ranking', 'top', 'highest', 'lowest'],
                'phrases': ['bar chart', 'compare', 'rank', 'top 10', 'highest', 'lowest'],
                'best_for': ['comparisons', 'rankings', 'categorical analysis']
            },
            'line': {
                'keywords': ['line', 'trend', 'over time', 'timeline', 'progression', 'change'],
                'phrases': ['line chart', 'over time', 'trend analysis', 'time series'],
                'best_for': ['time series', 'trends', 'progression analysis']
            },
            'scatter': {
                'keywords': ['scatter', 'correlation', 'relationship', 'versus', 'vs'],
                'phrases': ['scatter plot', 'correlation', 'relationship between'],
                'best_for': ['correlation analysis', 'relationship analysis']
            }
        }
        
        self.data_focus_patterns = {
            'defects': {
                'keywords': ['defect', 'rejection', 'reason', 'cause', 'problem', 'issue', 'fault'],
                'phrases': ['rejection reasons', 'defect types', 'why rejected', 'causes of'],
                'entities': ['burr', 'damage', 'toolmark', 'oversize', 'undersize']
            },
            'parts': {
                'keywords': ['part', 'component', 'item', 'product', 'piece'],
                'phrases': ['part number', 'which part', 'part analysis', 'component'],
                'entities': []  # Will be populated from data
            },
            'trends': {
                'keywords': ['trend', 'time', 'monthly', 'daily', 'weekly', 'over time', 'progression'],
                'phrases': ['over time', 'trend analysis', 'time series', 'monthly trends'],
                'entities': ['month', 'day', 'week', 'year']
            },
            'performance': {
                'keywords': ['performance', 'quality', 'efficiency', 'rate', 'ratio', 'percentage'],
                'phrases': ['rejection rate', 'quality performance', 'efficiency analysis'],
                'entities': ['rate', 'ratio', 'percentage']
            }
        }
    
    def load_and_analyze_data(self):
        """Load and perform initial analysis of the data"""
        try:
            # Load the file
            if self.file_path.endswith('.xlsx'):
                self.df = pd.read_excel(self.file_path)
            elif self.file_path.endswith('.csv'):
                self.df = pd.read_csv(self.file_path)
            else:
                raise ValueError("Unsupported file format")
            
            # Convert date column
            if 'Date' in self.df.columns:
                self.df['Date'] = pd.to_datetime(self.df['Date'])
            
            # Identify key columns
            self.identify_columns()
            
            # Generate metadata
            self.generate_metadata()
            
            print("✅ Enhanced Data Analyzer loaded successfully!")
            print(f"📊 Records: {len(self.df)}")
            print(f"📅 Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
            print(f"🔧 Unique parts: {self.df['Part Name'].nunique()}")
            print(f"❌ Total rejections: {self.df['Total Rej Qty.'].sum()}")
            print(f"🎯 Defect categories: {len(self.defect_columns)}")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def identify_columns(self):
        """Identify and categorize different types of columns"""
        # Identify defect columns (all columns except basic info)
        basic_cols = ['Unnamed: 0', 'Date', 'Inspected Qty.', 'Part Name', 'Total Rej Qty.']
        self.defect_columns = [col for col in self.df.columns if col not in basic_cols and not col.startswith('Unnamed')]
        
        # Clean up defect columns (remove empty or unnamed columns)
        self.defect_columns = [col for col in self.defect_columns if not pd.isna(col) and col.strip()]
    
    def generate_metadata(self):
        """Generate comprehensive metadata about the dataset"""
        self.metadata = {
            'total_records': len(self.df),
            'date_range': {
                'start': self.df['Date'].min(),
                'end': self.df['Date'].max()
            },
            'unique_parts': self.df['Part Name'].nunique(),
            'part_names': self.df['Part Name'].unique().tolist(),
            'total_rejections': self.df['Total Rej Qty.'].sum(),
            'defect_types': self.defect_columns,
            'months_available': sorted(self.df['Date'].dt.to_period('M').unique().astype(str)),
        }
    
    def get_top_rejection_reasons(self, count=5):
        """Get the top N rejection reasons with detailed analysis"""
        try:
            # Calculate totals for all defect columns
            defect_totals = {}
            for col in self.defect_columns:
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:  # Only include defects that actually occurred
                        defect_totals[col] = total
            
            if not defect_totals:
                return "❌ **Answer:** No defect data found in the dataset."
            
            # Sort by total count and get top N
            sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:count]
            
            if not sorted_defects:
                return "❌ **Answer:** No rejection data available."
            
            # Calculate total rejections for percentage calculation
            total_rejections = sum(defect_totals.values())
            
            # Format the enhanced response
            answer = f"🎯 **Top {len(sorted_defects)} Rejection Reasons (Enhanced Analysis):**\n\n"
            
            for i, (defect_type, count) in enumerate(sorted_defects, 1):
                percentage = (count / total_rejections) * 100
                
                # Add visual indicators for severity
                severity = "🔴" if percentage > 10 else "🟠" if percentage > 5 else "🟡" if percentage > 2 else "🟢"
                
                answer += f"{i}. {severity} **{defect_type}**: {count:,} parts ({percentage:.1f}%)\n"
            
            # Add comprehensive summary statistics
            answer += f"\n📊 **Detailed Summary:**\n"
            answer += f"• Total defect categories tracked: {len(self.defect_columns)}\n"
            answer += f"• Active defect types (with occurrences): {len(defect_totals)}\n"
            answer += f"• Total rejections across all types: {total_rejections:,} parts\n"
            answer += f"• Average rejections per defect type: {total_rejections/len(defect_totals):.1f} parts\n"
            
            # Calculate cumulative impact
            cumulative_percentages = []
            cumulative_sum = 0
            for _, count in sorted_defects:
                cumulative_sum += count
                cumulative_percentages.append((cumulative_sum / total_rejections) * 100)
            
            answer += f"\n🎯 **Impact Analysis:**\n"
            answer += f"• Top 1 defect accounts for: {cumulative_percentages[0]:.1f}% of all rejections\n"
            if len(cumulative_percentages) >= 3:
                answer += f"• Top 3 defects account for: {cumulative_percentages[2]:.1f}% of all rejections\n"
            if len(cumulative_percentages) >= 5:
                answer += f"• Top 5 defects account for: {cumulative_percentages[4]:.1f}% of all rejections\n"
            
            # Add process insights
            answer += f"\n💡 **Process Insights:**\n"
            
            # Categorize defects by type
            sizing_defects = [d for d, _ in sorted_defects if any(word in d[0].lower() for word in ['size', 'oversize', 'undersize', 'u/s', 'o/s'])]
            surface_defects = [d for d, _ in sorted_defects if any(word in d[0].lower() for word in ['damage', 'mark', 'toolmark', 'burr', 'scratch'])]
            machining_defects = [d for d, _ in sorted_defects if any(word in d[0].lower() for word in ['drilling', 'milling', 'boring', 'face', 'cut'])]
            position_defects = [d for d, _ in sorted_defects if any(word in d[0].lower() for word in ['position', 'off', 'pcd', 'symmetry'])]
            
            if sizing_defects:
                sizing_count = sum([count for defect, count in sizing_defects])
                sizing_pct = (sizing_count / total_rejections) * 100
                answer += f"• Sizing Issues: {len(sizing_defects)} types, {sizing_count:,} parts ({sizing_pct:.1f}%) - Check tooling calibration\n"
            
            if surface_defects:
                surface_count = sum([count for defect, count in surface_defects])
                surface_pct = (surface_count / total_rejections) * 100
                answer += f"• Surface Defects: {len(surface_defects)} types, {surface_count:,} parts ({surface_pct:.1f}%) - Review cutting parameters\n"
            
            if machining_defects:
                machining_count = sum([count for defect, count in machining_defects])
                machining_pct = (machining_count / total_rejections) * 100
                answer += f"• Machining Issues: {len(machining_defects)} types, {machining_count:,} parts ({machining_pct:.1f}%) - Check machine condition\n"
            
            if position_defects:
                position_count = sum([count for defect, count in position_defects])
                position_pct = (position_count / total_rejections) * 100
                answer += f"• Positioning Errors: {len(position_defects)} types, {position_count:,} parts ({position_pct:.1f}%) - Verify setup accuracy\n"
            
            # Add recommendations
            answer += f"\n🔧 **Action Recommendations:**\n"
            top_defect = sorted_defects[0]
            answer += f"• **Priority 1:** Address '{top_defect[0]}' immediately ({top_defect[1]:,} parts, {(top_defect[1]/total_rejections)*100:.1f}%)\n"
            
            if len(sorted_defects) >= 2:
                answer += f"• **Priority 2:** Focus on top 3 defects for 80/20 impact\n"
            
            answer += f"• **Process Review:** Implement root cause analysis for defects >5% of total\n"
            answer += f"• **Quality Control:** Enhance inspection for the top {min(3, len(sorted_defects))} defect categories\n"
            
            return answer
            
        except Exception as e:
            return f"❌ **Error analyzing rejection reasons:** {str(e)}"
    
    def analyze_question_semantically(self, question):
        """Analyze question using enhanced semantic understanding"""
        question_lower = question.lower().strip()
        
        # Use TextBlob for basic NLP analysis if available
        analysis = {
            'original_question': question,
            'chart_type': 'auto',  # Will be determined
            'data_focus': 'auto',  # Will be determined
            'specific_count': None,
            'time_period': None,
            'specific_entities': [],
            'question_type': 'unknown',
            'complexity': 'medium'
        }
        
        # Extract specific numbers (top 5, top 10, etc.)
        number_matches = re.findall(r'top\s*(\d+)|first\s*(\d+)|(\d+)\s*most|(\d+)\s*highest', question_lower)
        if number_matches:
            for match in number_matches:
                for num in match:
                    if num:
                        analysis['specific_count'] = int(num)
                        break
                if analysis['specific_count']:
                    break
        
        # Determine chart type preference
        analysis['chart_type'] = self.determine_chart_type(question_lower)
        
        # Determine data focus
        analysis['data_focus'] = self.determine_data_focus(question_lower)
        
        # Determine question type
        analysis['question_type'] = self.determine_question_type(question_lower)
        
        return analysis
    
    def determine_chart_type(self, question_lower):
        """Intelligently determine the best chart type for the question"""
        chart_scores = {}
        
        for chart_type, patterns in self.chart_type_patterns.items():
            score = 0
            
            # Check keywords
            for keyword in patterns['keywords']:
                if keyword in question_lower:
                    score += 2
            
            # Check phrases (higher weight)
            for phrase in patterns['phrases']:
                if phrase in question_lower:
                    score += 3
            
            chart_scores[chart_type] = score
        
        # Contextual logic for chart selection
        if any(word in question_lower for word in ['distribution', 'proportion', 'breakdown', 'share']):
            chart_scores['pie'] += 5
        
        if any(word in question_lower for word in ['compare', 'top', 'highest', 'lowest', 'rank']):
            chart_scores['bar'] += 5
        
        if any(word in question_lower for word in ['trend', 'over time', 'monthly', 'progression']):
            chart_scores['line'] += 5
        
        # Return the chart type with highest score, or 'auto' if no clear preference
        best_chart = max(chart_scores, key=chart_scores.get) if max(chart_scores.values()) > 0 else 'auto'
        return best_chart
    
    def determine_data_focus(self, question_lower):
        """Determine what type of data the user is asking about"""
        focus_scores = {}
        
        for focus_type, patterns in self.data_focus_patterns.items():
            score = 0
            
            # Check keywords
            for keyword in patterns['keywords']:
                if keyword in question_lower:
                    score += 2
            
            # Check phrases
            for phrase in patterns['phrases']:
                if phrase in question_lower:
                    score += 3
            
            focus_scores[focus_type] = score
        
        # Return the focus with highest score
        best_focus = max(focus_scores, key=focus_scores.get) if max(focus_scores.values()) > 0 else 'auto'
        return best_focus
    
    def determine_question_type(self, question_lower):
        """Determine the type of question being asked"""
        question_types = {
            'comparison': ['compare', 'versus', 'vs', 'difference', 'better', 'worse'],
            'ranking': ['top', 'highest', 'lowest', 'best', 'worst', 'rank'],
            'quantity': ['how many', 'count', 'number', 'total', 'sum'],
            'analysis': ['analyze', 'analysis', 'insight', 'pattern', 'trend'],
            'visualization': ['chart', 'graph', 'plot', 'draw', 'show', 'visualize'],
            'specific': ['which', 'what', 'when', 'where', 'who'],
            'temporal': ['when', 'date', 'time', 'month', 'day', 'year']
        }
        
        for q_type, keywords in question_types.items():
            if any(keyword in question_lower for keyword in keywords):
                return q_type
        
        return 'general'
    
    def generate_intelligent_response(self, question):
        """Generate an intelligent response with appropriate charts"""
        # Analyze the question semantically
        analysis = self.analyze_question_semantically(question)
        
        # Route to appropriate handler based on analysis
        if analysis['question_type'] == 'visualization' or any(word in question.lower() for word in ['chart', 'graph', 'plot', 'draw', 'show', 'visualize']):
            return self.create_smart_visualization(question, analysis)
        
        elif analysis['data_focus'] == 'defects':
            return self.handle_defect_analysis(question, analysis)
        
        elif analysis['data_focus'] == 'parts':
            return self.handle_parts_analysis(question, analysis)
        
        elif analysis['data_focus'] == 'trends':
            return self.handle_trend_analysis(question, analysis)
        
        else:
            # Enhanced fallback
            return self.get_top_rejection_reasons(analysis.get('specific_count', 5))
    
    def create_smart_visualization(self, question, analysis):
        """Create smart visualizations based on semantic analysis"""
        try:
            chart_type = analysis['chart_type']
            data_focus = analysis['data_focus']
            count = analysis['specific_count'] or 15
            
            # Smart chart selection logic
            if chart_type == 'auto':
                if data_focus == 'defects':
                    chart_type = 'pie' if 'distribution' in question.lower() else 'bar'
                elif data_focus == 'trends':
                    chart_type = 'line'
                elif data_focus == 'parts':
                    chart_type = 'bar'
                else:
                    chart_type = 'bar'  # Safe default
            
            # Generate appropriate chart
            if chart_type == 'pie':
                return self.create_intelligent_pie_chart(question, analysis, count)
            elif chart_type == 'line':
                return self.create_intelligent_line_chart(question, analysis)
            elif chart_type == 'bar':
                return self.create_intelligent_bar_chart(question, analysis, count)
            else:
                return self.create_intelligent_bar_chart(question, analysis, count)
                
        except Exception as e:
            return f"❌ **Error creating visualization:** {str(e)}\n\nLet me provide a basic analysis instead...\n\n" + self.get_top_rejection_reasons(5)
    
    def create_intelligent_pie_chart(self, question, analysis, count):
        """Create an intelligent pie chart based on context"""
        try:
            # Get defect distribution pie chart
            defect_totals = {}
            for col in self.defect_columns:
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:
                        defect_totals[col] = total
            
            if not defect_totals:
                return "❌ **No defect data available for pie chart.**"
            
            # Sort and get top N
            sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:min(count, 10)]
            
            defect_names = [item[0] for item in sorted_defects]
            defect_counts = [item[1] for item in sorted_defects]
            
            # Create pie chart
            fig = px.pie(
                values=defect_counts,
                names=defect_names,
                title=f'Smart Analysis: Top {len(defect_names)} Rejection Reasons Distribution'
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                showlegend=True,
                legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.01),
                width=1000,
                height=600
            )
            
            # Convert to base64
            img_bytes = fig.to_image(format="png", width=1000, height=600)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Create intelligent response
            total_rejections = sum(defect_counts)
            top_defect_percentage = (defect_counts[0] / total_rejections) * 100
            
            response = f"📊 **Smart Pie Chart Analysis: Rejection Reasons Distribution**\n\n"
            response += f"🎯 **Key Insights:**\n"
            response += f"• **Dominant defect**: {defect_names[0]} ({defect_counts[0]:,} parts, {top_defect_percentage:.1f}%)\n"
            response += f"• **Data coverage**: {len(defect_names)} defect categories\n"
            response += f"• **Total rejections**: {total_rejections:,} parts\n\n"
            
            # Add actionable insights
            if top_defect_percentage > 50:
                response += f"💡 **Critical Insight**: {defect_names[0]} accounts for over {top_defect_percentage:.0f}% of rejections - immediate action required!\n\n"
            elif top_defect_percentage > 30:
                response += f"⚠️ **High Impact**: {defect_names[0]} is the major contributor - prioritize this defect type.\n\n"
            
            response += f"📈 **Generated Chart:**\n"
            response += f"data:image/png;base64,{img_base64}"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating pie chart:** {str(e)}"
    
    def create_intelligent_bar_chart(self, question, analysis, count):
        """Create an intelligent bar chart based on context"""
        try:
            # Create defect ranking bar chart
            defect_totals = {}
            for col in self.defect_columns:
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:
                        defect_totals[col] = total
            
            sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:count]
            defect_names = [item[0] for item in sorted_defects]
            defect_counts = [item[1] for item in sorted_defects]
            
            # Create horizontal bar chart for better readability
            fig = px.bar(
                x=defect_counts,
                y=defect_names,
                orientation='h',
                title=f'Smart Analysis: Top {len(defect_names)} Rejection Causes (Ranked)',
                labels={'x': 'Total Rejections', 'y': 'Defect Type'},
                color=defect_counts,
                color_continuous_scale='Reds'
            )
            
            fig.update_layout(
                height=max(400, len(defect_names) * 30),
                margin=dict(l=250, r=50, t=80, b=50),
                yaxis={'categoryorder': 'total ascending'},
                showlegend=False
            )
            
            img_bytes = fig.to_image(format="png", width=1200, height=max(600, len(defect_names) * 30))
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Generate intelligent insights
            total_rejections = sum(defect_counts)
            top_3_percentage = sum(defect_counts[:3]) / total_rejections * 100
            
            response = f"📊 **Smart Bar Chart Analysis: Rejection Rankings**\n\n"
            response += f"🥇 **Top Defect**: {defect_names[0]} ({defect_counts[0]:,} parts)\n"
            response += f"🎯 **Focus Area**: Top 3 defects = {top_3_percentage:.1f}% of all rejections\n"
            response += f"📈 **Improvement Potential**: Fixing top defect could reduce rejections by {(defect_counts[0]/total_rejections*100):.1f}%\n\n"
            response += f"📊 **Generated Chart:**\n"
            response += f"data:image/png;base64,{img_base64}"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating bar chart:** {str(e)}"
    
    def create_intelligent_line_chart(self, question, analysis):
        """Create an intelligent line chart for trend analysis"""
        try:
            # Create monthly trend analysis
            monthly_data = self.df.groupby(self.df['Date'].dt.to_period('M')).agg({
                'Total Rej Qty.': 'sum',
                'Inspected Qty.': 'sum'
            }).reset_index()
            
            monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()
            monthly_data['Rejection_Rate'] = (monthly_data['Total Rej Qty.'] / monthly_data['Inspected Qty.']) * 100
            
            # Create comprehensive trend chart
            fig = go.Figure()
            
            # Add rejection quantity trend
            fig.add_trace(go.Scatter(
                x=monthly_data['Date'],
                y=monthly_data['Total Rej Qty.'],
                mode='lines+markers',
                name='Total Rejections',
                line=dict(color='red', width=3),
                marker=dict(size=8),
                yaxis='y'
            ))
            
            # Add rejection rate trend on secondary axis
            fig.add_trace(go.Scatter(
                x=monthly_data['Date'],
                y=monthly_data['Rejection_Rate'],
                mode='lines+markers',
                name='Rejection Rate (%)',
                line=dict(color='orange', width=2, dash='dash'),
                marker=dict(size=6),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title='Smart Trend Analysis: Quality Performance Over Time',
                xaxis_title='Month',
                yaxis=dict(title='Total Rejections', side='left'),
                yaxis2=dict(title='Rejection Rate (%)', side='right', overlaying='y'),
                height=600,
                width=1200,
                showlegend=True,
                hovermode='x unified'
            )
            
            img_bytes = fig.to_image(format="png", width=1200, height=600)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Generate trend insights
            latest_rejections = monthly_data['Total Rej Qty.'].iloc[-1]
            first_rejections = monthly_data['Total Rej Qty.'].iloc[0]
            trend_direction = "improving ⬇️" if latest_rejections < first_rejections else "worsening ⬆️"
            
            latest_rate = monthly_data['Rejection_Rate'].iloc[-1]
            avg_rate = monthly_data['Rejection_Rate'].mean()
            
            response = f"📈 **Smart Trend Analysis**\n\n"
            response += f"📊 **Trend Direction**: Quality is {trend_direction}\n"
            response += f"🎯 **Current Status**: {latest_rejections:,} rejections, {latest_rate:.2f}% rate\n"
            response += f"📋 **Benchmark**: Average rate is {avg_rate:.2f}%\n"
            response += f"⏱️ **Analysis Period**: {len(monthly_data)} months\n\n"
            
            if latest_rate > avg_rate * 1.2:
                response += f"🚨 **Alert**: Current rejection rate is {((latest_rate/avg_rate-1)*100):.0f}% above average!\n\n"
            elif latest_rate < avg_rate * 0.8:
                response += f"✅ **Good News**: Current rate is {((1-latest_rate/avg_rate)*100):.0f}% below average!\n\n"
            
            response += f"📈 **Generated Chart:**\n"
            response += f"data:image/png;base64,{img_base64}"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating trend chart:** {str(e)}"
    
    def handle_defect_analysis(self, question, analysis):
        """Handle defect-related questions with smart analysis"""
        if 'chart' in question.lower() or 'graph' in question.lower():
            return self.create_smart_visualization(question, analysis)
        
        # Provide smart defect analysis
        count = analysis['specific_count'] or 5
        return self.get_top_rejection_reasons(count)
    
    def handle_parts_analysis(self, question, analysis):
        """Handle parts-related questions with smart analysis"""
        if 'chart' in question.lower() or 'graph' in question.lower():
            return self.create_smart_visualization(question, analysis)
        
        # Smart parts analysis
        if 'highest' in question.lower():
            top_part = self.df.groupby('Part Name')['Total Rej Qty.'].sum().sort_values(ascending=False)
            return f"🔧 **Highest Rejections**: {top_part.index[0]} with {top_part.iloc[0]:,} total rejections"
        
        return "🔧 **Parts analysis available**. Ask about specific parts or request charts!"
    
    def handle_trend_analysis(self, question, analysis):
        """Handle trend-related questions"""
        if 'chart' in question.lower() or 'graph' in question.lower():
            return self.create_smart_visualization(question, analysis)
        
        # Basic trend analysis
        monthly_trends = self.df.groupby(self.df['Date'].dt.to_period('M'))['Total Rej Qty.'].sum()
        trend_direction = "improving" if monthly_trends.iloc[-1] < monthly_trends.iloc[0] else "declining"
        
        return f"📈 **Trend**: Quality is {trend_direction}. Latest: {monthly_trends.iloc[-1]}, Start: {monthly_trends.iloc[0]}"
    
    def answer_question(self, question):
        """Enhanced question answering with smarter detection"""
        question_lower = question.lower()
        
        # Check for chart/visualization requests first
        if any(word in question_lower for word in ['chart', 'graph', 'plot', 'draw', 'show', 'visualize', 'pie', 'bar', 'line']):
            return self.generate_intelligent_response(question)
        
        # Enhanced pattern matching for rejection reason queries
        rejection_patterns = [
            r'top\s*(\d+)?\s*(rejection|defect|cause)',
            r'(tell|show|list|give)\s*(me\s*)?(top|highest|most)\s*(\d+)?\s*(rejection|defect|reason)',
            r'most\s*(frequent|common)\s*(rejection|defect)',
            r'highest\s*(rejection|defect)',
            r'(rejection|defect)\s*reason',
            r'(why|what)\s*.*(reject|fail)',
        ]
        
        # Check if this is asking for rejection reasons
        is_rejection_query = False
        requested_count = 5  # default
        
        for pattern in rejection_patterns:
            match = re.search(pattern, question_lower)
            if match:
                is_rejection_query = True
                # Try to extract the number if specified
                numbers = re.findall(r'\d+', question_lower)
                if numbers:
                    try:
                        requested_count = int(numbers[0])
                        # Limit to reasonable range
                        requested_count = min(max(requested_count, 1), 20)
                    except:
                        requested_count = 5
                break
        
        if is_rejection_query:
            return self.get_top_rejection_reasons(requested_count)
        
        # Use intelligent response for other questions
        return self.generate_intelligent_response(question)

# Test the enhanced analyzer
def test_enhanced_analyzer():
    """Test the enhanced analyzer with various queries"""
    analyzer = EnhancedSmartAnalyzer('uploads/QUALITY_DAILY_Machining_Rejection.xlsx')
    
    test_queries = [
        "tell top 5 rejection reason",
        "top 10 rejection reasons", 
        "show me the most frequent rejection causes",
        "what are the top 3 defect types",
        "list the highest rejection reasons",
        "most common defects"
    ]
    
    print("\n🧪 Testing Enhanced Analyzer")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        result = analyzer.answer_question(query)
        print(result)
        print("-" * 50)

if __name__ == "__main__":
    test_enhanced_analyzer()
