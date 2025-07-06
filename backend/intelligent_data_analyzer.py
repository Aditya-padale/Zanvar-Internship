import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os
import plotly.graph_objects as go
import plotly.express as px
import base64
import io
from PIL import Image

class IntelligentDataAnalyzer:
    def __init__(self, file_path):
        """Initialize the analyzer with the data file"""
        self.file_path = file_path
        self.df = None
        self.defect_columns = []
        self.metadata = {}
        self.conversation_memory = {
            'last_question': '',
            'last_answer': '',
            'mentioned_parts': [],
            'mentioned_dates': [],
            'mentioned_defects': [],
            'context': {}
        }
        self.load_and_analyze_data()
    
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
            
            print("✅ Data loaded successfully!")
            print(f"📊 Records: {len(self.df)}")
            print(f"📅 Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
            print(f"🔧 Unique parts: {self.df['Part Name'].nunique()}")
            print(f"❌ Total rejections: {self.df['Total Rej Qty.'].sum()}")
            
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
            'daily_stats': {
                'max_daily_rejection': self.df.groupby('Date')['Total Rej Qty.'].sum().max(),
                'avg_daily_rejection': self.df.groupby('Date')['Total Rej Qty.'].sum().mean()
            }
        }
    
    def answer_question(self, question):
        """Intelligently answer any question about the data"""
        question_lower = question.lower()
        
        # Update conversation memory
        self.conversation_memory['last_question'] = question
        if 'context' not in self.conversation_memory:
            self.conversation_memory['context'] = {}
        
        # Check for contextual follow-up questions
        context_response = self.handle_contextual_questions(question)
        if context_response:
            self.conversation_memory['last_answer'] = context_response
            return context_response
        
        # Machine-related questions
        if 'machine' in question_lower:
            response = self.handle_machine_questions(question)
            self.conversation_memory['last_answer'] = response
            return response
        
        # Part-related questions (check more comprehensively)
        if ('part' in question_lower and ('highest' in question_lower or 'lowest' in question_lower or 'rejection' in question_lower)) or \
           ('which part' in question_lower) or \
           ('part number' in question_lower and 'total' not in question_lower):
            response = self.handle_part_questions(question)
            self.conversation_memory['last_answer'] = response
            return response
        
        # Date-related questions (but not if it's asking about parts on dates)
        if any(word in question_lower for word in ['date', 'day', 'month', 'year', 'when']) and 'part' not in question_lower:
            return self.handle_date_questions(question)
        
        # Rejection reason questions
        if any(word in question_lower for word in ['reason', 'defect', 'burr', 'damage', 'toolmark']) and 'part' not in question_lower:
            return self.handle_defect_questions(question)
        
        # Quantity/count questions
        if any(word in question_lower for word in ['total', 'count', 'number', 'quantity', 'how many']) and 'part' not in question_lower:
            return self.handle_quantity_questions(question)
        
        # Date-specific highest/lowest questions
        if any(word in question_lower for word in ['date', 'day']) and any(word in question_lower for word in ['highest', 'lowest']):
            return self.handle_date_questions(question)
        
        # Defect-specific highest/lowest questions  
        if any(word in question_lower for word in ['reason', 'defect', 'frequent']) and any(word in question_lower for word in ['highest', 'lowest', 'most']):
            return self.handle_defect_questions(question)
        
        # Ratio/percentage questions
        if any(word in question_lower for word in ['ratio', 'percentage', 'rate']):
            return self.handle_ratio_questions(question)
        
        # Trend/analysis questions (fallback for general analysis)
        if any(word in question_lower for word in ['trend', 'analysis', 'chart', 'graph']):
            return self.handle_analysis_questions(question)
        
        # General questions
        response = self.handle_general_questions(question)
        self.conversation_memory['last_answer'] = response
        return response
    
    def handle_contextual_questions(self, question):
        """Handle follow-up questions that depend on conversation context"""
        question_lower = question.lower()
        last_question = self.conversation_memory.get('last_question', '').lower()
        last_answer = self.conversation_memory.get('last_answer', '')
        
        # Look for context clues in follow-up questions
        context_words = ['why', 'how', 'what caused', 'reason', 'because', 'this part', 'that part', 'why this', 'why that']
        
        if any(word in question_lower for word in context_words) and last_answer:
            # Attempt to derive part context from last question or answer if it mentioned a specific part
            part_match = re.search(r'([A-Z][A-Z\s\d-]+\d+(?:-\d+)?)', last_answer) or \
                         re.search(r'part\s+(number|name)\s+([A-Z][A-Z\s\d-]+\d+(?:-\d+)?)', last_question) or \
                         re.search(r'([A-Z]{5,}\s*[A-Z]*\s*\d+(?:-\d+)?)', last_answer)
            
            if part_match:
                part_name = part_match.group(1) if part_match.group(1) else part_match.group(2)
                if part_name:
                    part_name = part_name.strip()
                    self.conversation_memory['context']['current_part'] = part_name
                    
                    # Update conversation memory with extracted part
                    if part_name not in self.conversation_memory['mentioned_parts']:
                        self.conversation_memory['mentioned_parts'].append(part_name)
                    
                    if 'why' in question_lower and ('rejection' in question_lower or 'most' in question_lower or 'this part' in question_lower):
                        return self.analyze_part_rejection_reasons(part_name)
                        
                    if 'how' in question_lower and 'many' in question_lower:
                        return self.get_part_detailed_analysis(part_name)
                        
                    if 'what caused' in question_lower or 'reason' in question_lower:
                        return self.analyze_part_rejection_reasons(part_name)
        
        # Handle pronoun references ("this part", "that part")
        if ('this part' in question_lower or 'that part' in question_lower) and self.conversation_memory.get('context', {}).get('current_part'):
            part_name = self.conversation_memory['context'].get('current_part', '')
            if not part_name:
                return "❌ **Error:** Unable to determine the part in question. Please specify clearly."
            
            if 'rejection' in question_lower or 'defect' in question_lower:
                return self.analyze_part_rejection_reasons(part_name)
        
        return None  # No contextual handling needed
    
    def analyze_part_rejection_reasons(self, part_name):
        """Analyze why a specific part has high rejections"""
        try:
            # Get data for this specific part
            part_data = self.df[self.df['Part Name'].str.contains(part_name, na=False, case=False)]
            
            if len(part_data) == 0:
                return f"❌ **Answer:** No data found for part '{part_name}'."
            
            # Calculate total rejections for this part
            total_rejections = part_data['Total Rej Qty.'].sum()
            
            # Find top defect types for this part
            defect_analysis = []
            for col in self.defect_columns:
                if col in part_data.columns:
                    defect_total = part_data[col].sum()
                    if defect_total > 0:
                        percentage = (defect_total / total_rejections) * 100
                        defect_analysis.append((col, defect_total, percentage))
            
            # Sort by quantity and take top 5
            defect_analysis.sort(key=lambda x: x[1], reverse=True)
            top_defects = defect_analysis[:5]
            
            if not top_defects:
                return f"✅ **Answer:** {part_name} has {total_rejections} total rejections, but specific defect breakdown is not available."
            
            # Calculate frequency (how often this part gets rejected)
            total_inspected = part_data['Inspected Qty.'].sum()
            rejection_rate = (total_rejections / total_inspected * 100) if total_inspected > 0 else 0
            
            # Build comprehensive answer
            answer = f"🔍 **Why {part_name} has the most rejections:**\n\n"
            answer += f"📊 **Overall Impact:**\n"
            answer += f"• Total rejections: {total_rejections:,} parts\n"
            answer += f"• Rejection rate: {rejection_rate:.2f}%\n"
            answer += f"• Data points: {len(part_data)} days\n\n"
            
            answer += f"🎯 **Top Defect Types:**\n"
            for i, (defect, count, percentage) in enumerate(top_defects, 1):
                answer += f"{i}. **{defect}**: {count:,} parts ({percentage:.1f}% of part's rejections)\n"
            
            # Add insights based on defect patterns
            if len(top_defects) >= 2:
                top_two_percentage = sum([x[2] for x in top_defects[:2]])
                if top_two_percentage > 60:
                    answer += f"\n💡 **Key Insight:** Top 2 defects account for {top_two_percentage:.1f}% of rejections - focus on these for maximum impact.\n"
            
            # Check for specific defect patterns
            sizing_defects = [d for d in top_defects if 'size' in d[0].lower()]
            surface_defects = [d for d in top_defects if any(word in d[0].lower() for word in ['burr', 'mark', 'damage', 'scratch'])]
            
            if sizing_defects:
                answer += f"\n⚠️ **Process Issue:** Sizing problems detected - may indicate tool wear or setup issues.\n"
            
            if surface_defects:
                answer += f"\n⚠️ **Quality Issue:** Surface defects detected - may indicate handling or machining problems.\n"
            
            return answer
            
        except Exception as e:
            return f"❌ **Error analyzing part rejections:** {str(e)}"
    
    def get_part_detailed_analysis(self, part_name):
        """Get detailed analysis for a specific part"""
        try:
            part_data = self.df[self.df['Part Name'].str.contains(part_name, na=False, case=False)]
            
            if len(part_data) == 0:
                return f"❌ **Answer:** No data found for part '{part_name}'."
            
            total_rejections = part_data['Total Rej Qty.'].sum()
            total_inspected = part_data['Inspected Qty.'].sum()
            avg_daily_rejections = total_rejections / len(part_data)
            worst_day = part_data.loc[part_data['Total Rej Qty.'].idxmax()]
            
            answer = f"📈 **Detailed Analysis for {part_name}:**\n\n"
            answer += f"• Production days tracked: {len(part_data)}\n"
            answer += f"• Total parts inspected: {total_inspected:,}\n"
            answer += f"• Total rejections: {total_rejections:,}\n"
            answer += f"• Average daily rejections: {avg_daily_rejections:.1f}\n"
            answer += f"• Worst day: {worst_day['Date'].strftime('%Y-%m-%d')} ({worst_day['Total Rej Qty.']:.0f} rejections)\n"
            
            return answer
            
        except Exception as e:
            return f"❌ **Error getting detailed analysis:** {str(e)}"
    
    def handle_machine_questions(self, question):
        """Handle questions about machines"""
        # Extract machine number if present
        machine_match = re.search(r'machine\s*(?:no\.?\s*)?(\d+)', question.lower())
        
        if machine_match:
            machine_num = machine_match.group(1)
            return f"❌ **Answer:** Machine No. {machine_num} is not identified in the data. The dataset tracks rejections by part names/components, not by specific machine numbers."
        
        if 'this month' in question.lower():
            current_month = self.df['Date'].dt.to_period('M').max()
            return f"❌ **Answer:** No machine identifiers found in the data. The dataset only contains part names. Latest available data is for {current_month}."
        
        return "❌ **Answer:** The dataset does not contain machine identifiers. Data is organized by part names/components only."
    
    def handle_part_questions(self, question):
        """Handle questions about specific parts"""
        # Extract part number if present
        part_match = re.search(r'["\']([^"\']+)["\']|(\d{8,})', question)
        
        if part_match:
            part_num = part_match.group(1) or part_match.group(2)
            matching_parts = self.df[self.df['Part Name'].str.contains(part_num, na=False, case=False)]
            
            if len(matching_parts) > 0:
                total_rej = matching_parts['Total Rej Qty.'].sum()
                return f"✅ **Answer:** Part containing '{part_num}' has {total_rej} total rejections."
            else:
                return f"❌ **Answer:** Part number '{part_num}' not found in the data."
        
        # Highest rejections
        if 'highest' in question.lower():
            top_part = self.df.groupby('Part Name')['Total Rej Qty.'].sum().sort_values(ascending=False)
            return f"✅ **Answer:** {top_part.index[0]} with {top_part.iloc[0]} total rejections."
        
        return "❓ **Answer:** Please specify the part number or provide more details about the part."
    
    def handle_date_questions(self, question):
        """Handle date-related questions"""
        # Extract specific date
        date_match = re.search(r'(\d{1,2})[st|nd|rd|th]*\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})', question.lower())
        
        if date_match:
            day = int(date_match.group(1))
            month_name = date_match.group(2)
            year = int(date_match.group(3))
            
            month_map = {
                'january': 1, 'february': 2, 'march': 3, 'april': 4,
                'may': 5, 'june': 6, 'july': 7, 'august': 8,
                'september': 9, 'october': 10, 'november': 11, 'december': 12
            }
            
            try:
                target_date = datetime(year, month_map[month_name], day)
                date_data = self.df[self.df['Date'].dt.date == target_date.date()]
                
                if len(date_data) > 0:
                    total_rej = date_data['Total Rej Qty.'].sum()
                    parts = date_data['Part Name'].unique()
                    return f"✅ **Answer:** {total_rej} rejections on {target_date.strftime('%B %d, %Y')}. Parts involved: {', '.join(parts[:3])}{'...' if len(parts) > 3 else ''}"
                else:
                    return f"❌ **Answer:** No data found for {target_date.strftime('%B %d, %Y')}."
            except:
                return "❌ **Answer:** Invalid date format."
        
        # Month-based questions
        month_match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})', question.lower())
        
        if month_match:
            month_name = month_match.group(1)
            year = int(month_match.group(2))
            
            month_map = {
                'january': 1, 'february': 2, 'march': 3, 'april': 4,
                'may': 5, 'june': 6, 'july': 7, 'august': 8,
                'september': 9, 'october': 10, 'november': 11, 'december': 12
            }
            
            month_num = month_map[month_name]
            month_data = self.df[(self.df['Date'].dt.month == month_num) & (self.df['Date'].dt.year == year)]
            
            if len(month_data) > 0:
                total_rej = month_data['Total Rej Qty.'].sum()
                return f"✅ **Answer:** {total_rej} rejections in {month_name.title()} {year}."
            else:
                return f"❌ **Answer:** No data available for {month_name.title()} {year}."
        
        # Highest rejection date
        if 'highest' in question.lower():
            daily_rejections = self.df.groupby('Date')['Total Rej Qty.'].sum().sort_values(ascending=False)
            top_date = daily_rejections.index[0]
            return f"✅ **Answer:** {top_date.strftime('%Y-%m-%d')} with {daily_rejections.iloc[0]} rejections."
        
        return "❓ **Answer:** Please specify the date or time period you're asking about."
    
    def handle_defect_questions(self, question):
        """Handle questions about defects/rejection reasons"""
        question_lower = question.lower()
        
        # Check if this is a chart/graph request first
        if any(word in question_lower for word in ['chart', 'graph', 'plot', 'draw', 'create', 'show', 'visualize']):
            return self.generate_intelligent_chart(question)
        
        # Handle top N rejection reasons
        if any(phrase in question_lower for phrase in ['top', 'highest', 'most', 'frequent']):
            # Check if asking for specific number (top 5, top 10, etc.)
            import re
            number_match = re.search(r'top\s*(\d+)', question_lower)
            count = int(number_match.group(1)) if number_match else 5
            
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
            
            # Format the response
            answer = f"🎯 **Top {len(sorted_defects)} Rejection Reasons:**\n\n"
            
            for i, (defect_type, count) in enumerate(sorted_defects, 1):
                percentage = (count / total_rejections) * 100
                answer += f"{i}. **{defect_type}**: {count:,} parts ({percentage:.1f}%)\n"
            
            # Add summary statistics
            answer += f"\n📊 **Summary:**\n"
            answer += f"• Total defect categories: {len(self.defect_columns)}\n"
            answer += f"• Active defect types: {len(defect_totals)}\n"
            answer += f"• Total rejections: {total_rejections:,} parts\n"
            
            # Add insight about top defects contribution
            top_3_percentage = sum([x[1] for x in sorted_defects[:3]]) / total_rejections * 100
            answer += f"• Top 3 defects account for: {top_3_percentage:.1f}% of all rejections\n"
            
            return answer
        
        # Extract specific defect type
        defect_keywords = ['burr', 'damage', 'toolmark', 'oversize', 'undersize', 'drilling', 'milling', 'boring']
        
        found_defect = None
        for keyword in defect_keywords:
            if keyword in question_lower:
                # Find matching columns
                matching_cols = [col for col in self.defect_columns if keyword.lower() in col.lower()]
                if matching_cols:
                    found_defect = matching_cols[0]
                    break
        
        if found_defect:
            total_defects = self.df[found_defect].sum()
            return f"✅ **Answer:** {total_defects} parts rejected due to '{found_defect}' defect."
        
        # List all defect types
        if 'list' in question_lower or 'all' in question_lower:
            active_defects = [col for col in self.defect_columns if self.df[col].sum() > 0]
            return f"✅ **Answer:** Available active defect types ({len(active_defects)} total): {', '.join(active_defects[:10])}{'...' if len(active_defects) > 10 else ''}"
        
        # Default fallback - show top 5 rejection reasons
        return self.handle_defect_questions("top 5 rejection reasons")
    
    def handle_quantity_questions(self, question):
        """Handle quantity-related questions"""
        # Handle specific month questions
        if 'june 2024' in question.lower():
            june_data = self.df[(self.df['Date'].dt.month == 6) & (self.df['Date'].dt.year == 2024)]
            if len(june_data) > 0:
                total_rej = june_data['Total Rej Qty.'].sum()
                return f"✅ **Answer:** {total_rej} rejections in June 2024."
            else:
                return f"❌ **Answer:** No data available for June 2024."
        
        if 'total' in question.lower() and ('rejected' in question.lower() or 'rejection' in question.lower()):
            total_rej = self.df['Total Rej Qty.'].sum()
            return f"✅ **Answer:** Total rejections across all data: {total_rej} parts."
        
        if 'total' in question.lower():
            total_rej = self.df['Total Rej Qty.'].sum()
            return f"✅ **Answer:** Total rejections across all data: {total_rej} parts."
        
        if 'this month' in question.lower():
            current_month = self.df['Date'].dt.to_period('M').max()
            current_data = self.df[self.df['Date'].dt.to_period('M') == current_month]
            total_rej = current_data['Total Rej Qty.'].sum()
            return f"✅ **Answer:** {total_rej} rejections in {current_month} (latest available month)."
        
        return f"✅ **Answer:** Total rejections in dataset: {self.df['Total Rej Qty.'].sum()}"
    
    def handle_analysis_questions(self, question):
        """Handle analysis and trend questions"""
        question_lower = question.lower()
        
        # Chart/Graph generation requests
        if any(word in question_lower for word in ['chart', 'graph', 'plot', 'draw', 'create', 'show']):
            return self.generate_intelligent_chart(question)
        
        if 'trend' in question_lower:
            monthly_trends = self.df.groupby(self.df['Date'].dt.to_period('M'))['Total Rej Qty.'].sum()
            trend_direction = "increasing" if monthly_trends.iloc[-1] > monthly_trends.iloc[0] else "decreasing"
            return f"✅ **Answer:** Rejection trend is {trend_direction}. Latest month: {monthly_trends.iloc[-1]}, First month: {monthly_trends.iloc[0]}"
        
        if 'highest' in question_lower and 'average' in question_lower:
            part_avg = self.df.groupby('Part Name')['Total Rej Qty.'].mean().sort_values(ascending=False)
            return f"✅ **Answer:** {part_avg.index[0]} has the highest average daily rejection: {part_avg.iloc[0]:.2f} parts/day."
        
        return "📈 **Answer:** Analysis capability available. Please specify what type of analysis you need."
    
    def handle_ratio_questions(self, question):
        """Handle ratio and percentage questions"""
        if 'rejection ratio' in question.lower():
            total_inspected = self.df['Inspected Qty.'].sum()
            total_rejected = self.df['Total Rej Qty.'].sum()
            ratio = (total_rejected / total_inspected) * 100 if total_inspected > 0 else 0
            return f"✅ **Answer:** Overall rejection ratio: {ratio:.2f}% ({total_rejected} rejected out of {total_inspected} inspected)."
        
        return "📊 **Answer:** Ratio calculation available. Please specify what ratio you need."
    
    def generate_intelligent_chart(self, question):
        """Generate charts based on intelligent question analysis"""
        question_lower = question.lower()
        
        try:
            # Analyze the question to understand exactly what the user wants
            chart_analysis = self.analyze_chart_request(question)
            
            # Generate appropriate chart based on analysis
            if chart_analysis['data_type'] == 'rejections':
                return self.create_rejection_reasons_chart(question, chart_analysis)
            
            elif chart_analysis['data_type'] == 'trends':
                return self.create_trend_chart(question, chart_analysis)
            
            elif chart_analysis['data_type'] == 'parts':
                return self.create_parts_analysis_chart(question, chart_analysis)
            
            elif chart_analysis['data_type'] == 'defects':
                return self.create_defect_analysis_chart(question, chart_analysis)
            
            elif chart_analysis['data_type'] == 'monthly':
                return self.create_monthly_analysis_chart(question, chart_analysis)
            
            else:
                # Intelligent fallback based on question content
                return self.create_smart_fallback_chart(question)
                
        except Exception as e:
            return f"❌ **Error generating chart:** {str(e)}\n\nLet me try a simpler approach...\n\n" + self.create_basic_chart(question)
    
    def create_rejection_reasons_chart(self, question):
        """Create a chart showing top rejection reasons"""
        try:
            # Extract number if specified (top 5, top 10, etc.)
            import re
            number_match = re.search(r'top\s*(\d+)', question.lower())
            count = int(number_match.group(1)) if number_match else 15
            
            # Get top rejection reasons data
            defect_totals = {}
            for col in self.defect_columns:
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:
                        defect_totals[col] = total
            
            if not defect_totals:
                return "❌ **Error:** No defect data found for chart generation."
            
            # Sort and get top N
            sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:count]
            
            # Create chart data
            defect_names = [item[0] for item in sorted_defects]
            defect_counts = [item[1] for item in sorted_defects]
            
            # Determine chart type from question
            chart_type = 'bar'  # default
            if 'pie' in question.lower():
                chart_type = 'pie'
            elif 'line' in question.lower():
                chart_type = 'line'
            
            if chart_type == 'pie':
                fig = px.pie(
                    values=defect_counts[:10],  # Limit pie chart to top 10 for readability
                    names=defect_names[:10],
                    title=f'Top {min(10, len(defect_names))} Rejection Reasons Distribution'
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    showlegend=True,
                    legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.01)
                )
            else:
                # Bar chart (default)
                fig = px.bar(
                    x=defect_counts,
                    y=defect_names,
                    orientation='h',
                    title=f'Top {len(defect_names)} Rejection Causes',
                    labels={'x': 'Total Rejections', 'y': 'Defect Type'}
                )
                fig.update_layout(
                    height=max(400, len(defect_names) * 25),
                    margin=dict(l=200, r=50, t=80, b=50),
                    yaxis={'categoryorder': 'total ascending'}
                )
            
            # Convert to base64 image
            img_bytes = fig.to_image(format="png", width=1000, height=max(600, len(defect_names) * 25))
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Create response with chart and analysis
            total_rejections = sum(defect_counts)
            top_3_percent = sum(defect_counts[:3]) / total_rejections * 100
            
            response = f"📊 **{chart_type.title()} Chart: Top {len(defect_names)} Rejection Reasons**\n\n"
            response += f"🎯 **Quick Insights:**\n"
            response += f"• Top defect: **{defect_names[0]}** ({defect_counts[0]:,} parts)\n"
            response += f"• Top 3 defects account for {top_3_percent:.1f}% of all rejections\n"
            response += f"• Total categories analyzed: {len(self.defect_columns)}\n\n"
            response += f"📈 **Chart Image:**\n"
            response += f"data:image/png;base64,{img_base64}"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating rejection chart:** {str(e)}"
    
    def create_trend_chart(self, question):
        """Create a trend chart showing rejections over time"""
        try:
            # Group by month for trend analysis
            monthly_data = self.df.groupby(self.df['Date'].dt.to_period('M')).agg({
                'Total Rej Qty.': 'sum',
                'Inspected Qty.': 'sum'
            }).reset_index()
            
            monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()
            monthly_data['Rejection_Rate'] = (monthly_data['Total Rej Qty.'] / monthly_data['Inspected Qty.']) * 100
            
            # Create trend chart
            fig = go.Figure()
            
            # Add rejection quantity line
            fig.add_trace(go.Scatter(
                x=monthly_data['Date'],
                y=monthly_data['Total Rej Qty.'],
                mode='lines+markers',
                name='Total Rejections',
                line=dict(color='red', width=3),
                yaxis='y'
            ))
            
            # Add rejection rate line on secondary y-axis
            fig.add_trace(go.Scatter(
                x=monthly_data['Date'],
                y=monthly_data['Rejection_Rate'],
                mode='lines+markers',
                name='Rejection Rate (%)',
                line=dict(color='orange', width=2),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title='Quality Trends: Rejections Over Time',
                xaxis_title='Month',
                yaxis=dict(title='Total Rejections', side='left'),
                yaxis2=dict(title='Rejection Rate (%)', side='right', overlaying='y'),
                height=500,
                showlegend=True
            )
            
            # Convert to base64
            img_bytes = fig.to_image(format="png", width=1000, height=500)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Analysis
            trend_direction = "improving" if monthly_data['Total Rej Qty.'].iloc[-1] < monthly_data['Total Rej Qty.'].iloc[0] else "worsening"
            latest_rate = monthly_data['Rejection_Rate'].iloc[-1]
            
            response = f"📈 **Trend Analysis Chart**\n\n"
            response += f"🎯 **Key Insights:**\n"
            response += f"• Trend direction: **{trend_direction}**\n"
            response += f"• Latest rejection rate: **{latest_rate:.2f}%**\n"
            response += f"• Data period: {len(monthly_data)} months\n\n"
            response += f"📊 **Chart Image:**\n"
            response += f"data:image/png;base64,{img_base64}"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating trend chart:** {str(e)}"
    
    def analyze_chart_request(self, question):
        """Intelligently analyze what type of chart the user wants"""
        question_lower = question.lower()
        
        analysis = {
            'chart_type': 'bar',  # default
            'data_type': 'rejections',  # default
            'count': 15,  # default
            'time_period': None,
            'specific_part': None,
            'specific_defect': None
        }
        
        # Determine chart type
        if 'pie' in question_lower:
            analysis['chart_type'] = 'pie'
        elif 'line' in question_lower or 'trend' in question_lower:
            analysis['chart_type'] = 'line'
        elif 'bar' in question_lower:
            analysis['chart_type'] = 'bar'
        
        # Determine data type
        if any(word in question_lower for word in ['part', 'component']):
            analysis['data_type'] = 'parts'
        elif any(word in question_lower for word in ['trend', 'time', 'monthly', 'daily', 'over time']):
            analysis['data_type'] = 'trends'
        elif any(word in question_lower for word in ['defect', 'rejection', 'reason', 'cause']):
            analysis['data_type'] = 'rejections'
        elif 'monthly' in question_lower:
            analysis['data_type'] = 'monthly'
        
        # Extract count (top 5, top 10, etc.)
        import re
        number_match = re.search(r'top\s*(\d+)', question_lower)
        if number_match:
            analysis['count'] = int(number_match.group(1))
        
        # Extract time period
        if any(month in question_lower for month in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']):
            analysis['time_period'] = 'monthly'
        
        # Extract specific part
        part_match = re.search(r'part\s+([A-Z][A-Z\s\d-]+)', question_lower)
        if part_match:
            analysis['specific_part'] = part_match.group(1)
        
        # Extract specific defect
        defect_keywords = ['burr', 'damage', 'toolmark', 'oversize', 'undersize', 'drilling', 'milling']
        for keyword in defect_keywords:
            if keyword in question_lower:
                analysis['specific_defect'] = keyword
                break
        
        return analysis
    
    def create_rejection_reasons_chart(self, question, chart_analysis=None):
        """Create a chart showing top rejection reasons based on intelligent analysis"""
        try:
            if chart_analysis is None:
                chart_analysis = self.analyze_chart_request(question)
            
            count = chart_analysis.get('count', 15)
            chart_type = chart_analysis.get('chart_type', 'bar')
            
            # Get top rejection reasons data
            defect_totals = {}
            for col in self.defect_columns:
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:
                        defect_totals[col] = total
            
            if not defect_totals:
                return "❌ **Error:** No defect data found for chart generation."
            
            # Sort and get top N
            sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:count]
            
            # Create chart data
            defect_names = [item[0] for item in sorted_defects]
            defect_counts = [item[1] for item in sorted_defects]
            
            if chart_type == 'pie':
                # Limit pie chart to top 10 for readability
                display_count = min(10, len(defect_names))
                fig = px.pie(
                    values=defect_counts[:display_count],
                    names=defect_names[:display_count],
                    title=f'Top {display_count} Rejection Reasons Distribution'
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    showlegend=True,
                    legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.01)
                )
            else:
                # Bar chart (default)
                fig = px.bar(
                    x=defect_counts,
                    y=defect_names,
                    orientation='h',
                    title=f'Top {len(defect_names)} Rejection Causes',
                    labels={'x': 'Total Rejections', 'y': 'Defect Type'}
                )
                fig.update_layout(
                    height=max(400, len(defect_names) * 25),
                    margin=dict(l=200, r=50, t=80, b=50),
                    yaxis={'categoryorder': 'total ascending'}
                )
            
            # Convert to base64 image
            img_bytes = fig.to_image(format="png", width=1000, height=max(600, len(defect_names) * 25))
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Create response with chart and analysis
            total_rejections = sum(defect_counts)
            top_3_percent = sum(defect_counts[:3]) / total_rejections * 100 if len(defect_counts) >= 3 else 100
            
            response = f"📊 **{chart_type.title()} Chart: Top {len(defect_names)} Rejection Reasons**\n\n"
            response += f"🎯 **Quick Insights:**\n"
            response += f"• Top defect: **{defect_names[0]}** ({defect_counts[0]:,} parts)\n"
            response += f"• Top 3 defects account for {top_3_percent:.1f}% of all rejections\n"
            response += f"• Total categories analyzed: {len(self.defect_columns)}\n\n"
            response += f"📈 **Chart Image:**\n"
            response += f"data:image/png;base64,{img_base64}"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating rejection chart:** {str(e)}"
    
    def create_trend_chart(self, question, chart_analysis=None):
        """Create a trend chart showing rejections over time"""
        try:
            # Group by month for trend analysis
            monthly_data = self.df.groupby(self.df['Date'].dt.to_period('M')).agg({
                'Total Rej Qty.': 'sum',
                'Inspected Qty.': 'sum'
            }).reset_index()
            
            monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()
            monthly_data['Rejection_Rate'] = (monthly_data['Total Rej Qty.'] / monthly_data['Inspected Qty.']) * 100
            
            # Create trend chart
            fig = go.Figure()
            
            # Add rejection quantity line
            fig.add_trace(go.Scatter(
                x=monthly_data['Date'],
                y=monthly_data['Total Rej Qty.'],
                mode='lines+markers',
                name='Total Rejections',
                line=dict(color='red', width=3),
                yaxis='y'
            ))
            
            # Add rejection rate line on secondary y-axis
            fig.add_trace(go.Scatter(
                x=monthly_data['Date'],
                y=monthly_data['Rejection_Rate'],
                mode='lines+markers',
                name='Rejection Rate (%)',
                line=dict(color='orange', width=2),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title='Quality Trends: Rejections Over Time',
                xaxis_title='Month',
                yaxis=dict(title='Total Rejections', side='left'),
                yaxis2=dict(title='Rejection Rate (%)', side='right', overlaying='y'),
                height=500,
                showlegend=True
            )
            
            # Convert to base64
            img_bytes = fig.to_image(format="png", width=1000, height=500)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Analysis
            trend_direction = "improving" if monthly_data['Total Rej Qty.'].iloc[-1] < monthly_data['Total Rej Qty.'].iloc[0] else "worsening"
            latest_rate = monthly_data['Rejection_Rate'].iloc[-1]
            
            response = f"📈 **Trend Analysis Chart**\n\n"
            response += f"🎯 **Key Insights:**\n"
            response += f"• Trend direction: **{trend_direction}**\n"
            response += f"• Latest rejection rate: **{latest_rate:.2f}%**\n"
            response += f"• Data period: {len(monthly_data)} months\n\n"
            response += f"📊 **Chart Image:**\n"
            response += f"data:image/png;base64,{img_base64}"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating trend chart:** {str(e)}"
    
    def create_parts_analysis_chart(self, question, chart_analysis=None):
        """Create a chart analyzing parts performance"""
        try:
            if chart_analysis is None:
                chart_analysis = self.analyze_chart_request(question)
            
            count = chart_analysis.get('count', 15)
            
            # Get top parts with highest rejections
            parts_data = self.df.groupby('Part Name')['Total Rej Qty.'].sum().sort_values(ascending=False)[:count]
            
            # Create horizontal bar chart for better readability
            fig = px.bar(
                x=parts_data.values,
                y=parts_data.index,
                orientation='h',
                title=f'Top {count} Parts by Rejection Count',
                labels={'x': 'Total Rejections', 'y': 'Part Name'}
            )
            
            fig.update_layout(
                height=max(400, count * 30),
                margin=dict(l=200, r=50, t=80, b=50),
                yaxis={'categoryorder': 'total ascending'}
            )
            
            # Convert to base64
            img_bytes = fig.to_image(format="png", width=1000, height=max(400, count * 30))
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Analysis
            total_parts = self.df['Part Name'].nunique()
            top_part_rejections = parts_data.iloc[0]
            
            response = f"🔧 **Parts Analysis Chart**\n\n"
            response += f"🎯 **Key Insights:**\n"
            response += f"• Worst performing part: **{parts_data.index[0]}** ({top_part_rejections:,} rejections)\n"
            response += f"• Total unique parts: {total_parts}\n"
            response += f"• Showing top {count} parts by rejection count\n\n"
            response += f"📊 **Chart Image:**\n"
            response += f"data:image/png;base64,{img_base64}"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating parts chart:** {str(e)}"
    
    def create_defect_analysis_chart(self, question, chart_analysis=None):
        """Create specialized defect analysis chart"""
        return self.create_rejection_reasons_chart(question, chart_analysis)
    
    def create_monthly_analysis_chart(self, question, chart_analysis=None):
        """Create monthly analysis chart"""
        return self.create_trend_chart(question, chart_analysis)
    
    def create_smart_fallback_chart(self, question):
        """Smart fallback when specific chart type can't be determined"""
        # Analyze the question content to make best guess
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['part', 'component']):
            return self.create_parts_analysis_chart(question)
        elif any(word in question_lower for word in ['time', 'trend', 'monthly']):
            return self.create_trend_chart(question)
        else:
            # Default to rejection reasons
            return self.create_rejection_reasons_chart(question)
    
    def create_basic_chart(self, question):
        """Basic chart creation as final fallback"""
        try:
            # Simple bar chart of top 10 rejection reasons
            defect_totals = {}
            for col in self.defect_columns:
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:
                        defect_totals[col] = total
            
            if not defect_totals:
                return "❌ **Error:** No defect data available for chart creation."
            
            sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:10]
            defect_names = [item[0] for item in sorted_defects]
            defect_counts = [item[1] for item in sorted_defects]
            
            fig = px.bar(
                x=defect_counts,
                y=defect_names,
                orientation='h',
                title='Top 10 Rejection Causes (Basic Chart)',
                labels={'x': 'Total Rejections', 'y': 'Defect Type'}
            )
            
            fig.update_layout(
                height=500,
                margin=dict(l=200, r=50, t=80, b=50),
                yaxis={'categoryorder': 'total ascending'}
            )
            
            img_bytes = fig.to_image(format="png", width=800, height=500)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            response = f"📊 **Basic Chart: Top 10 Rejection Causes**\n\n"
            response += f"🎯 **Top Defect:** {defect_names[0]} ({defect_counts[0]:,} parts)\n\n"
            response += f"📈 **Chart Image:**\n"
            response += f"data:image/png;base64,{img_base64}"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating basic chart:** {str(e)}"
    
    def handle_general_questions(self, question):
        """Handle general questions about the dataset"""
        return f"""
📋 **Data Summary:**
• Total records: {self.metadata['total_records']}
• Date range: {self.metadata['date_range']['start'].strftime('%Y-%m-%d')} to {self.metadata['date_range']['end'].strftime('%Y-%m-%d')}
• Unique parts: {self.metadata['unique_parts']}
• Total rejections: {self.metadata['total_rejections']}
• Available months: {', '.join(self.metadata['months_available'])}
• Defect types tracked: {len(self.metadata['defect_types'])}

❓ **Ask me about:**
- Specific dates, parts, or defect types
- Trends and analysis
- Quantities and ratios
- Comparisons between parts or time periods
- Charts and visualizations (bar, pie, line, trend)
"""

# Example usage and testing
def test_analyzer():
    """Test the analyzer with sample questions"""
    analyzer = IntelligentDataAnalyzer('uploads/QUALITY_DAILY_Machining_Rejection.xlsx')
    
    # Test questions
    questions = [
        "What is the total number of rejected parts for each machine this month?",
        "Which part number had the highest number of rejections overall?",
        "Which date had the highest rejection count?",
        "How many rejections were recorded in the month of June 2024?",
        "How many parts were rejected due to Burr on Machine No. 32?",
        "What is the total rejection quantity for part number 30534763?",
        "Show all rejection entries for 15th March 2024",
        "Which rejection reason is the most frequent across all machines?",
        "What is the rejection ratio for the entire dataset?",
        "Is there a trend in rejection quantities over time?"
    ]
    
    print("🤖 INTELLIGENT DATA ANALYZER - TEST RESULTS")
    print("=" * 60)
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. {question}")
        answer = analyzer.answer_question(question)
        print(answer)
        print("-" * 50)

if __name__ == "__main__":
    test_analyzer()
