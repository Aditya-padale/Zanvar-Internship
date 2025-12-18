import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for serverless
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import base64
import os
from datetime import datetime

class ServerlessAnalyzer:
    """Simplified analyzer for serverless deployment"""
    
    def __init__(self):
        self.data = None
        self.file_info = None
    
    def load_data(self, file_path, file_type='csv'):
        """Load data from file"""
        try:
            if file_type == 'csv':
                self.data = pd.read_csv(file_path)
            elif file_type in ['xlsx', 'xls']:
                self.data = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            self.file_info = {
                'shape': self.data.shape,
                'columns': self.data.columns.tolist(),
                'dtypes': self.data.dtypes.astype(str).to_dict()
            }
            return True
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def create_pie_chart(self, column=None):
        """Create a pie chart from categorical data"""
        if self.data is None:
            return None
        
        try:
            if column is None:
                # Auto-select first categorical column
                categorical_cols = self.data.select_dtypes(include=['object']).columns
                if len(categorical_cols) == 0:
                    return None
                column = categorical_cols[0]
            
            # Get value counts
            value_counts = self.data[column].value_counts().head(10)  # Limit to top 10
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(10, 8))
            wedges, texts, autotexts = ax.pie(value_counts.values, 
                                             labels=value_counts.index,
                                             autopct='%1.1f%%',
                                             startangle=90)
            
            ax.set_title(f'Distribution of {column}', fontsize=14, fontweight='bold')
            
            # Convert to base64
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
            return {
                'type': 'pie',
                'data': img_base64,
                'column': column,
                'summary': f"Pie chart showing distribution of {column} with {len(value_counts)} categories"
            }
            
        except Exception as e:
            print(f"Error creating pie chart: {str(e)}")
            return None
    
    def create_bar_chart(self, column=None):
        """Create a bar chart from categorical data"""
        if self.data is None:
            return None
        
        try:
            if column is None:
                # Auto-select first categorical column
                categorical_cols = self.data.select_dtypes(include=['object']).columns
                if len(categorical_cols) == 0:
                    return None
                column = categorical_cols[0]
            
            # Get value counts
            value_counts = self.data[column].value_counts().head(15)  # Limit to top 15
            
            # Create bar chart
            fig, ax = plt.subplots(figsize=(12, 8))
            bars = ax.bar(range(len(value_counts)), value_counts.values)
            
            # Customize
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
            ax.set_ylabel('Count')
            ax.set_title(f'Distribution of {column}', fontsize=14, fontweight='bold')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Convert to base64
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
            return {
                'type': 'bar',
                'data': img_base64,
                'column': column,
                'summary': f"Bar chart showing distribution of {column} with {len(value_counts)} categories"
            }
            
        except Exception as e:
            print(f"Error creating bar chart: {str(e)}")
            return None
    
    def create_line_chart(self, x_col=None, y_col=None):
        """Create a line chart for numerical data over time/sequence"""
        if self.data is None:
            return None
        
        try:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) == 0:
                return None
            
            if y_col is None:
                y_col = numeric_cols[0]
            
            if x_col is None:
                # Use index or first numeric column
                x_data = range(len(self.data))
                x_label = 'Index'
            else:
                x_data = self.data[x_col]
                x_label = x_col
            
            y_data = self.data[y_col]
            
            # Create line chart
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.plot(x_data, y_data, linewidth=2, marker='o', markersize=4)
            
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_col)
            ax.set_title(f'{y_col} over {x_label}', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Convert to base64
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close()
            
            return {
                'type': 'line',
                'data': img_base64,
                'x_column': x_label,
                'y_column': y_col,
                'summary': f"Line chart showing {y_col} trend"
            }
            
        except Exception as e:
            print(f"Error creating line chart: {str(e)}")
            return None
    
    def get_basic_summary(self):
        """Get basic data summary"""
        if self.data is None:
            return None
        
        try:
            summary = {
                'shape': self.data.shape,
                'columns': self.data.columns.tolist(),
                'dtypes': self.data.dtypes.astype(str).to_dict(),
                'missing_values': self.data.isnull().sum().to_dict(),
                'numeric_summary': {}
            }
            
            # Add numeric summary if numeric columns exist
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                summary['numeric_summary'] = self.data[numeric_cols].describe().to_dict()
            
            return summary
            
        except Exception as e:
            print(f"Error creating summary: {str(e)}")
            return None
