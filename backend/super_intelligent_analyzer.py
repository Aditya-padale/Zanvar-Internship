"""
Super Intelligent Data Analyzer
Combines advanced NLP, machine learning, and visualization capabilities
to provide ChatGPT-like intelligence for data analysis and graph creation.
"""

import pandas as pd
import numpy as np
import os
import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Core data processing
try:
    import dask.dataframe as dd
    from dask import delayed
    HAS_DASK = True
except ImportError:
    HAS_DASK = False

# Advanced NLP
try:
    import spacy
    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False

try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except ImportError:
    HAS_TEXTBLOB = False

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import WordNetLemmatizer, PorterStemmer
    from nltk.chunk import ne_chunk
    from nltk.tag import pos_tag
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False

# Visualization libraries
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns

try:
    import bokeh.plotting as bk
    from bokeh.models import HoverTool
    HAS_BOKEH = True
except ImportError:
    HAS_BOKEH = False

try:
    import altair as alt
    HAS_ALTAIR = True
except ImportError:
    HAS_ALTAIR = False

# Machine Learning
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge

try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False

# Time series analysis
try:
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsmodels.tsa.arima.model import ARIMA
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False

# Utilities
import base64
import io
from collections import Counter, defaultdict
from loguru import logger
import joblib
from cachetools import TTLCache
from tqdm import tqdm
try:
    import google.generativeai as genai
    HAS_GOOGLE_AI = True
except ImportError:
    genai = None
    HAS_GOOGLE_AI = False

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SuperIntelligentAnalyzer:
    """
    Super Intelligent Data Analyzer with ChatGPT-like capabilities
    """
    
    def __init__(self, file_path: str):
        """Initialize the super intelligent analyzer"""
        self.file_path = file_path
        self.df = None
        self.dask_df = None
        self.nlp_model = None
        self.lemmatizer = None
        self.stemmer = None
        self.ml_models = {}
        self.feature_importance = {}
        self.cache = TTLCache(maxsize=1000, ttl=3600)  # 1 hour cache
        
        # Enhanced metadata
        self.metadata = {
            'data_characteristics': {},
            'statistical_insights': {},
            'ml_insights': {},
            'temporal_patterns': {},
            'anomalies': {},
            'correlations': {},
            'predictions': {}
        }
        
        # Advanced conversation context
        self.conversation_context = {
            'intent_history': [],
            'entity_mentions': {},
            'preference_learning': {
                'chart_types': Counter(),
                'analysis_depth': 'detailed',
                'response_style': 'comprehensive'
            },
            'domain_knowledge': {},
            'user_expertise_level': 'intermediate'
        }
        
        # Initialize Google API
        self._initialize_google_api()
        
        # Initialize components
        self._initialize_nlp()
        self._load_and_analyze_data()
        self._setup_ml_models()
        self._create_knowledge_base()
        
        logger.info("🚀 Super Intelligent Analyzer initialized successfully!")
    
    def _initialize_google_api(self):
        """Initialize Google Gemini API for advanced question understanding"""
        try:
            if not HAS_GOOGLE_AI:
                self.google_model = None
                logger.warning("⚠️ Google AI library not available")
                return
                
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.google_model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("✅ Google Gemini API initialized")
            else:
                self.google_model = None
                logger.warning("⚠️ GOOGLE_API_KEY not found in environment variables")
        except Exception as e:
            logger.warning(f"⚠️ Google API initialization failed: {e}")
            self.google_model = None
    
    def _initialize_nlp(self):
        """Initialize advanced NLP components"""
        logger.info("🧠 Initializing Advanced NLP...")
        
        # SpaCy initialization
        if HAS_SPACY:
            try:
                self.nlp_model = spacy.load("en_core_web_sm")
                logger.info("✅ SpaCy model loaded")
            except OSError:
                try:
                    os.system("python -m spacy download en_core_web_sm")
                    self.nlp_model = spacy.load("en_core_web_sm")
                    logger.info("✅ SpaCy model downloaded and loaded")
                except:
                    logger.warning("⚠️ SpaCy model unavailable")
                    self.nlp_model = None
        
        # NLTK initialization
        if HAS_NLTK:
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('wordnet', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
                nltk.download('maxent_ne_chunker', quiet=True)
                nltk.download('words', quiet=True)
                
                self.stop_words = set(stopwords.words('english'))
                self.lemmatizer = WordNetLemmatizer()
                self.stemmer = PorterStemmer()
                logger.info("✅ NLTK components initialized")
            except:
                logger.warning("⚠️ NLTK initialization failed")
                self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but'])
                self.lemmatizer = None
                self.stemmer = None
    
    def _load_and_analyze_data(self):
        """Load and perform comprehensive data analysis"""
        logger.info("📊 Loading and analyzing data...")
        
        try:
            # Load with pandas
            if self.file_path.endswith('.xlsx'):
                self.df = pd.read_excel(self.file_path)
            elif self.file_path.endswith('.csv'):
                self.df = pd.read_csv(self.file_path)
            else:
                raise ValueError("Unsupported file format")
            
            # Load with Dask for large datasets
            if HAS_DASK and len(self.df) > 10000:
                try:
                    if self.file_path.endswith('.csv'):
                        self.dask_df = dd.read_csv(self.file_path)
                    logger.info("✅ Dask dataframe created for large dataset")
                except:
                    logger.warning("⚠️ Dask loading failed, using pandas only")
            
            # Data preprocessing
            self._preprocess_data()
            
            # Generate comprehensive metadata
            self._generate_comprehensive_metadata()
            
            # Detect anomalies
            self._detect_anomalies()
            
            # Find correlations
            self._analyze_correlations()
            
            logger.info(f"✅ Data analysis complete - {len(self.df)} records processed")
            
        except Exception as e:
            logger.error(f"❌ Data loading failed: {e}")
            raise
    
    def _preprocess_data(self):
        """Advanced data preprocessing"""
        # Convert date columns
        date_columns = [col for col in self.df.columns if 'date' in col.lower()]
        for col in date_columns:
            try:
                self.df[col] = pd.to_datetime(self.df[col])
            except:
                pass
        
        # Identify column types
        self.numeric_columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_columns = self.df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Handle missing values intelligently
        for col in self.numeric_columns:
            if self.df[col].isnull().sum() > 0:
                if self.df[col].isnull().sum() / len(self.df) < 0.1:  # Less than 10% missing
                    self.df[col].fillna(self.df[col].median(), inplace=True)
        
        # Create derived features for quality data
        if 'Total Rej Qty.' in self.df.columns and 'Inspected Qty.' in self.df.columns:
            self.df['Rejection_Rate'] = (self.df['Total Rej Qty.'] / self.df['Inspected Qty.']) * 100
            self.df['Quality_Score'] = 100 - self.df['Rejection_Rate']
            
        # Identify defect columns
        basic_cols = ['Unnamed: 0', 'Date', 'Inspected Qty.', 'Part Name', 'Total Rej Qty.']
        self.defect_columns = [col for col in self.df.columns 
                              if col not in basic_cols and not col.startswith('Unnamed') 
                              and col not in ['Rejection_Rate', 'Quality_Score']]
    
    def _generate_comprehensive_metadata(self):
        """Generate comprehensive metadata about the dataset"""
        self.metadata['data_characteristics'] = {
            'shape': self.df.shape,
            'memory_usage': self.df.memory_usage(deep=True).sum(),
            'null_percentage': (self.df.isnull().sum() / len(self.df) * 100).to_dict(),
            'data_types': self.df.dtypes.astype(str).to_dict(),
            'unique_counts': self.df.nunique().to_dict(),
            'column_categories': {
                'numeric': self.numeric_columns,
                'categorical': self.categorical_columns,
                'datetime': self.datetime_columns,
                'defect_types': self.defect_columns
            }
        }
        
        # Statistical insights
        if self.numeric_columns:
            self.metadata['statistical_insights'] = {
                'descriptive_stats': self.df[self.numeric_columns].describe().to_dict(),
                'skewness': self.df[self.numeric_columns].skew().to_dict(),
                'kurtosis': self.df[self.numeric_columns].kurtosis().to_dict()
            }
        
        # Temporal patterns
        if self.datetime_columns:
            date_col = self.datetime_columns[0]
            self.metadata['temporal_patterns'] = {
                'date_range': {
                    'start': self.df[date_col].min(),
                    'end': self.df[date_col].max(),
                    'span_days': (self.df[date_col].max() - self.df[date_col].min()).days
                },
                'seasonal_patterns': self._detect_seasonality(date_col),
                'trend_direction': self._detect_trend(date_col)
            }
    
    def _detect_anomalies(self):
        """Detect anomalies using multiple methods"""
        anomalies = {}
        
        if len(self.numeric_columns) > 0:
            # Statistical outliers (IQR method)
            for col in self.numeric_columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                if len(outliers) > 0:
                    anomalies[f'{col}_statistical'] = {
                        'count': len(outliers),
                        'percentage': len(outliers) / len(self.df) * 100,
                        'bounds': [lower_bound, upper_bound]
                    }
            
            # ML-based anomaly detection
            try:
                if len(self.numeric_columns) >= 2:
                    isolation_forest = IsolationForest(contamination=0.1, random_state=42)
                    anomaly_scores = isolation_forest.fit_predict(self.df[self.numeric_columns].fillna(0))
                    anomaly_count = np.sum(anomaly_scores == -1)
                    
                    anomalies['ml_based'] = {
                        'count': anomaly_count,
                        'percentage': anomaly_count / len(self.df) * 100,
                        'method': 'Isolation Forest'
                    }
            except:
                pass
        
        self.metadata['anomalies'] = anomalies
    
    def _analyze_correlations(self):
        """Analyze correlations between variables"""
        if len(self.numeric_columns) > 1:
            corr_matrix = self.df[self.numeric_columns].corr()
            
            # Find strong correlations
            strong_correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:  # Strong correlation threshold
                        strong_correlations.append({
                            'variables': [corr_matrix.columns[i], corr_matrix.columns[j]],
                            'correlation': corr_value,
                            'strength': 'very strong' if abs(corr_value) > 0.9 else 'strong'
                        })
            
            self.metadata['correlations'] = {
                'matrix': corr_matrix.to_dict(),
                'strong_correlations': strong_correlations
            }
    
    def _detect_seasonality(self, date_col):
        """Detect seasonal patterns in time series data"""
        if 'Total Rej Qty.' not in self.df.columns:
            return None
        
        try:
            # Resample to monthly data
            monthly_data = self.df.set_index(date_col)['Total Rej Qty.'].resample('M').sum()
            
            if len(monthly_data) > 12:  # Need at least a year of data
                if HAS_STATSMODELS:
                    decomposition = seasonal_decompose(monthly_data, model='additive', period=12)
                    seasonal_strength = np.var(decomposition.seasonal) / np.var(monthly_data)
                    return {
                        'seasonal_strength': seasonal_strength,
                        'has_seasonality': seasonal_strength > 0.1
                    }
            return None
        except:
            return None
    
    def _detect_trend(self, date_col):
        """Detect trend in time series data"""
        if 'Total Rej Qty.' not in self.df.columns:
            return None
        
        try:
            monthly_data = self.df.set_index(date_col)['Total Rej Qty.'].resample('M').sum()
            
            if len(monthly_data) > 3:
                # Simple linear trend
                x = np.arange(len(monthly_data))
                slope, _ = np.polyfit(x, monthly_data.values, 1)
                
                if slope > 0.1:
                    return 'increasing'
                elif slope < -0.1:
                    return 'decreasing'
                else:
                    return 'stable'
            return None
        except:
            return None
    
    def _setup_ml_models(self):
        """Setup machine learning models for predictions and insights"""
        logger.info("🤖 Setting up ML models...")
        
        try:
            # Prepare data for ML
            if 'Total Rej Qty.' in self.df.columns and len(self.numeric_columns) > 1:
                # Feature selection for prediction
                feature_cols = [col for col in self.numeric_columns 
                               if col not in ['Total Rej Qty.', 'Rejection_Rate']]
                
                if len(feature_cols) > 0:
                    X = self.df[feature_cols].fillna(0)
                    y = self.df['Total Rej Qty.'].fillna(0)
                    
                    if len(X) > 10:  # Minimum data requirement
                        X_train, X_test, y_train, y_test = train_test_split(
                            X, y, test_size=0.2, random_state=42
                        )
                        
                        # Random Forest for feature importance
                        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
                        rf_model.fit(X_train, y_train)
                        
                        self.ml_models['random_forest'] = rf_model
                        self.feature_importance = dict(zip(feature_cols, rf_model.feature_importances_))
                        
                        # Model performance
                        y_pred = rf_model.predict(X_test)
                        r2 = r2_score(y_test, y_pred)
                        
                        self.metadata['ml_insights'] = {
                            'model_performance': {'r2_score': r2},
                            'feature_importance': self.feature_importance,
                            'top_features': sorted(self.feature_importance.items(), 
                                                 key=lambda x: x[1], reverse=True)[:5]
                        }
                        
                        logger.info("✅ ML models trained successfully")
        except Exception as e:
            logger.warning(f"⚠️ ML model setup failed: {e}")
    
    def _create_knowledge_base(self):
        """Create a knowledge base for intelligent responses"""
        self.knowledge_base = {
            'chart_recommendations': {
                'comparison': ['bar', 'column', 'radar'],
                'distribution': ['pie', 'donut', 'treemap'],
                'trend': ['line', 'area', 'candlestick'],
                'correlation': ['scatter', 'heatmap', 'bubble'],
                'composition': ['stacked_bar', 'stacked_area', 'waterfall']
            },
            'analysis_templates': {
                'quality_analysis': {
                    'key_metrics': ['rejection_rate', 'defect_distribution', 'trend_analysis'],
                    'insights': ['top_defects', 'improvement_areas', 'process_stability']
                },
                'performance_analysis': {
                    'key_metrics': ['efficiency', 'throughput', 'quality_score'],
                    'insights': ['performance_trends', 'bottlenecks', 'optimization_opportunities']
                }
            },
            'domain_expertise': {
                'manufacturing': {
                    'common_defects': ['burr', 'toolmark', 'oversize', 'undersize', 'damage'],
                    'quality_thresholds': {'excellent': '<1%', 'good': '1-3%', 'poor': '>5%'},
                    'improvement_suggestions': {
                        'high_rejection': 'Focus on process control and tooling',
                        'sizing_issues': 'Check calibration and tool wear',
                        'surface_defects': 'Review cutting parameters and coolant'
                    }
                }
            }
        }
    
    def analyze_intent(self, question: str) -> Dict[str, Any]:
        """Advanced intent analysis using multiple NLP techniques and Google AI"""
        intent_analysis = {
            'original_question': question,
            'primary_intent': 'unknown',
            'secondary_intents': [],
            'entities': [],
            'question_type': 'unknown',
            'complexity': 'medium',
            'chart_preference': 'auto',
            'analysis_depth': 'standard',
            'confidence': 0.0,
            'temporal_scope': 'overall',  # overall, monthly, weekly, daily
            'specific_months': [],
            'grouping_requested': False
        }
        
        question_lower = question.lower().strip()
        
        # SpaCy analysis
        if self.nlp_model:
            doc = self.nlp_model(question)
            
            # Extract entities
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            intent_analysis['entities'] = entities
            
            # Extract key phrases
            key_phrases = [chunk.text for chunk in doc.noun_chunks]
            intent_analysis['key_phrases'] = key_phrases
        
        # NLTK analysis
        if HAS_NLTK:
            try:
                tokens = word_tokenize(question_lower)
                pos_tags = pos_tag(tokens)
                intent_analysis['pos_tags'] = pos_tags
            except Exception as e:
                logger.warning(f"⚠️ NLTK tagging failed: {e}")
                intent_analysis['nlp_error'] = 'tagging_failed'
        
        # Intent classification
        intent_patterns = {
            'visualization': {
                'patterns': [r'chart', r'graph', r'plot', r'visualize', r'draw', r'show.*chart'],
                'confidence_boost': 0.3
            },
            'analysis': {
                'patterns': [r'analyze', r'analysis', r'insight', r'pattern', r'trend'],
                'confidence_boost': 0.2
            },
            'comparison': {
                'patterns': [r'compare', r'versus', r'vs', r'difference', r'better', r'worse'],
                'confidence_boost': 0.25
            },
            'ranking': {
                'patterns': [r'top', r'highest', r'lowest', r'best', r'worst', r'rank'],
                'confidence_boost': 0.3
            },
            'prediction': {
                'patterns': [r'predict', r'forecast', r'future', r'will', r'expect'],
                'confidence_boost': 0.4
            },
            'explanation': {
                'patterns': [r'why', r'how', r'what.*cause', r'reason', r'explain'],
                'confidence_boost': 0.2
            }
        }
        
        intent_scores = {}
        for intent, config in intent_patterns.items():
            score = 0
            for pattern in config['patterns']:
                if re.search(pattern, question_lower):
                    score += config['confidence_boost']
            intent_scores[intent] = score
        
        # Determine primary intent
        if intent_scores:
            primary_intent = max(intent_scores, key=intent_scores.get)
            if intent_scores[primary_intent] > 0:
                intent_analysis['primary_intent'] = primary_intent
                intent_analysis['confidence'] = intent_scores[primary_intent]
        
        # Determine chart preference
        chart_keywords = {
            'pie': ['pie', 'proportion', 'percentage', 'distribution', 'share'],
            'bar': ['bar', 'compare', 'ranking', 'top', 'highest', 'lowest'],
            'line': ['line', 'trend', 'over time', 'timeline', 'progression'],
            'scatter': ['scatter', 'correlation', 'relationship', 'versus'],
            'heatmap': ['heatmap', 'correlation', 'matrix', 'heat map']
        }
        
        for chart_type, keywords in chart_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                intent_analysis['chart_preference'] = chart_type
                break
        
        # Extract numbers for count requests
        numbers = re.findall(r'\d+', question)
        if numbers:
            intent_analysis['requested_count'] = int(numbers[0])
        
        # Detect temporal scope
        temporal_keywords = {
            'monthly': ['month', 'monthly', 'every month', 'each month', 'per month', 'month by month'],
            'weekly': ['week', 'weekly', 'every week', 'each week', 'per week'],
            'daily': ['day', 'daily', 'every day', 'each day', 'per day'],
            'yearly': ['year', 'yearly', 'annually', 'every year']
        }
        
        for scope, keywords in temporal_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                intent_analysis['temporal_scope'] = scope
                intent_analysis['grouping_requested'] = True
                break
        
        # Extract specific months
        month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                      'july', 'august', 'september', 'october', 'november', 'december',
                      'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                      'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        
        for month in month_names:
            if month in question_lower:
                intent_analysis['specific_months'].append(month)
        
        # Use Google API for better understanding if available
        if self.google_model:
            try:
                enhanced_understanding = self._analyze_with_google_api(question)
                if enhanced_understanding:
                    intent_analysis.update(enhanced_understanding)
            except Exception as e:
                logger.warning(f"Google API analysis failed: {e}")
        
        return intent_analysis
    
    def _analyze_with_google_api(self, question: str) -> Dict[str, Any]:
        """Use Google API to enhance question understanding"""
        try:
            if not self.google_model:
                return {}
            
            # Get data context
            columns_info = f"Available data columns: {', '.join(self.df.columns.tolist())}"
            if hasattr(self, 'defect_columns'):
                columns_info += f"\nDefect types: {', '.join(self.defect_columns)}"
            
            prompt = f"""
            Analyze this data analysis question and extract key information:
            
            Question: "{question}"
            Data context: {columns_info}
            
            Please identify:
            1. Primary intent (analysis, visualization, comparison, ranking, prediction, explanation)
            2. Temporal scope (overall, monthly, weekly, daily, specific months)
            3. Whether month-wise or time-based grouping is requested
            4. Specific months mentioned (if any)
            5. Chart type preference (pie, bar, line, etc.)
            6. Requested count/limit for results
            
            Respond in JSON format with these fields:
            {{
                "primary_intent": "string",
                "temporal_scope": "string", 
                "grouping_requested": boolean,
                "specific_months": ["array of month names"],
                "chart_preference": "string",
                "requested_count": number,
                "confidence": number
            }}
            """
            
            response = self.google_model.generate_content(prompt)
            
            # Try to parse JSON response
            try:
                import json
                # Clean the response to extract JSON
                response_text = response.text.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:-3]
                elif response_text.startswith('```'):
                    response_text = response_text[3:-3]
                
                enhanced_understanding = json.loads(response_text)
                logger.info(f"✅ Google API enhanced understanding: {enhanced_understanding}")
                return enhanced_understanding
                
            except json.JSONDecodeError:
                # Fallback to keyword extraction from response
                logger.warning("Failed to parse JSON from Google API, using text analysis")
                enhanced = {}
                text = response.text.lower()
                
                if 'monthly' in text or 'month' in text:
                    enhanced['temporal_scope'] = 'monthly'
                    enhanced['grouping_requested'] = True
                
                if 'pie' in text:
                    enhanced['chart_preference'] = 'pie'
                elif 'bar' in text:
                    enhanced['chart_preference'] = 'bar'
                elif 'line' in text:
                    enhanced['chart_preference'] = 'line'
                
                return enhanced
                
        except Exception as e:
            logger.warning(f"Google API analysis failed: {e}")
            return {}
    
    def generate_intelligent_response(self, question: str) -> str:
        """Generate intelligent responses using Google API first, then NLP extraction"""
        # Step 1: Try Google API for primary response generation
        if self.google_model:
            try:
                # Generate primary response using Google API
                api_response = self._generate_primary_response_with_api(question)
                if api_response and not api_response.startswith("❌"):
                    
                    # Step 2: Use NLP to extract specific data requirements
                    data_requirements = self._extract_data_requirements_with_nlp(question)
                    
                    # Step 3: If data extraction/visualization is needed, enhance with specific data
                    if data_requirements['needs_data_extraction']:
                        enhanced_response = self._enhance_response_with_data(api_response, data_requirements)
                        return enhanced_response
                    
                    return api_response
                    
            except Exception as e:
                logger.error(f"Google API primary response failed: {e}")
        
        # Fallback to traditional routing only if API fails
        intent = self.analyze_intent(question)
        self.conversation_context['intent_history'].append(intent)
        
        if intent['primary_intent'] == 'visualization':
            return self._handle_visualization_request(question, intent)
        elif intent['primary_intent'] == 'ranking':
            return self._handle_ranking_request(question, intent)
        elif intent['primary_intent'] == 'analysis':
            return self._handle_analysis_request(question, intent)
        elif intent['primary_intent'] == 'prediction':
            return self._handle_prediction_request(question, intent)
        elif intent['primary_intent'] == 'explanation':
            return self._handle_explanation_request(question, intent)
        else:
            # Use smart response generation even in fallback
            return self._generate_smart_response_with_api(question)
    
    def _handle_visualization_request(self, question: str, intent: Dict) -> str:
        """Handle visualization requests with intelligent chart selection"""
        try:
            chart_type = intent.get('chart_preference', 'auto')
            count = intent.get('requested_count', 10)
            
            if chart_type == 'auto':
                # Intelligent chart type selection
                if any(word in question.lower() for word in ['distribution', 'proportion', 'breakdown']):
                    chart_type = 'pie'
                elif any(word in question.lower() for word in ['trend', 'over time', 'progression']):
                    chart_type = 'line'
                elif any(word in question.lower() for word in ['compare', 'ranking', 'top']):
                    chart_type = 'bar'
                else:
                    chart_type = 'bar'  # Default
            
            # Generate the appropriate chart
            if chart_type == 'pie':
                return self._create_advanced_pie_chart(question, count)
            elif chart_type == 'line':
                return self._create_advanced_line_chart(question)
            elif chart_type == 'bar':
                return self._create_advanced_bar_chart(question, count)
            elif chart_type == 'heatmap':
                return self._create_correlation_heatmap(question)
            elif chart_type == 'scatter':
                return self._create_scatter_plot(question)
            else:
                return self._create_advanced_bar_chart(question, count)
                
        except Exception as e:
            logger.error(f"Visualization error: {e}")
            return f"❌ **Error creating visualization:** {str(e)}"
    
    def _create_advanced_pie_chart(self, question: str, count: int = 10) -> str:
        """Create advanced interactive pie chart with comprehensive analysis"""
        try:
            # Get defect data
            defect_totals = {}
            for col in self.defect_columns:
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:
                        defect_totals[col] = total
            
            if not defect_totals:
                return "❌ **No defect data available for pie chart analysis.**"
            
            # Sort and get top N
            sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:count]
            defect_names = [item[0] for item in sorted_defects]
            defect_counts = [item[1] for item in sorted_defects]
            
            # Create interactive pie chart
            fig = go.Figure(data=[go.Pie(
                labels=defect_names,
                values=defect_counts,
                hole=0.3,  # Donut style
                textinfo='label+percent+value',
                textposition='outside',
                marker=dict(
                    colors=px.colors.qualitative.Set3,
                    line=dict(color='#000000', width=2)
                ),
                hovertemplate='<b>%{label}</b><br>' +
                             'Count: %{value}<br>' +
                             'Percentage: %{percent}<br>' +
                             '<extra></extra>'
            )])
            
            fig.update_layout(
                title={
                    'text': f'🎯 Smart Analysis: Top {len(defect_names)} Rejection Reasons Distribution',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#2E86AB'}
                },
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                ),
                width=1200,
                height=700,
                margin=dict(l=50, r=200, t=100, b=50)
            )
            
            # Convert to base64
            img_bytes = fig.to_image(format="png", width=1200, height=700)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Generate comprehensive analysis
            total_rejections = sum(defect_counts)
            top_defect_percentage = (defect_counts[0] / total_rejections) * 100
            
            # Calculate cumulative impact
            cumulative_impact = []
            cumulative_sum = 0
            for count in defect_counts:
                cumulative_sum += count
                cumulative_impact.append((cumulative_sum / total_rejections) * 100)
            
            response = f"📊 **Advanced Pie Chart Analysis: Rejection Reasons Distribution**\n\n"
            
            # Key insights with emojis and formatting
            response += f"🎯 **Key Strategic Insights:**\n"
            response += f"• **Primary Issue**: {defect_names[0]} dominates with {defect_counts[0]:,} parts ({top_defect_percentage:.1f}%)\n"
            response += f"• **Data Scope**: Analyzing {len(defect_names)} defect categories from {total_rejections:,} total rejections\n"
            response += f"• **Pareto Analysis**: Top 3 defects account for {cumulative_impact[2]:.1f}% of all rejections\n\n"
            
            # Critical insights based on data
            if top_defect_percentage > 40:
                response += f"🚨 **Critical Alert**: {defect_names[0]} accounts for {top_defect_percentage:.0f}% of rejections - immediate intervention required!\n\n"
            elif top_defect_percentage > 25:
                response += f"⚠️ **High Priority**: {defect_names[0]} is a major contributor - should be primary focus for improvement.\n\n"
            
            # Actionable recommendations
            response += f"💡 **Strategic Recommendations:**\n"
            response += f"• **Immediate Action**: Address {defect_names[0]} for maximum impact ({defect_counts[0]:,} parts)\n"
            response += f"• **80/20 Rule**: Focus on top {min(3, len(defect_names))} defects for {cumulative_impact[min(2, len(cumulative_impact)-1)]:.0f}% improvement\n"
            response += f"• **Resource Allocation**: Prioritize defects contributing >5% of total rejections\n\n"
            
            # Quality assessment
            response += f"📈 **Quality Performance Assessment:**\n"
            avg_defect_count = total_rejections / len(defect_totals)
            response += f"• **Distribution Balance**: {'Concentrated' if top_defect_percentage > 30 else 'Distributed'} rejection pattern\n"
            response += f"• **Process Stability**: {'Unstable' if top_defect_percentage > 50 else 'Needs attention' if top_defect_percentage > 30 else 'Acceptable'}\n"
            response += f"• **Improvement Potential**: Fixing top defect could reduce rejections by {top_defect_percentage:.0f}%\n\n"
            
            response += f"📊 **Interactive Visualization:**\n"
            response += f"![Chart](data:image/png;base64,{img_base64})"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating advanced pie chart:** {str(e)}"
    
    def _create_advanced_bar_chart(self, question: str, count: int = 15) -> str:
        """Create advanced horizontal bar chart with detailed analysis"""
        try:
            # Get defect data
            defect_totals = {}
            for col in self.defect_columns:
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:
                        defect_totals[col] = total
            
            sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:count]
            defect_names = [item[0] for item in sorted_defects]
            defect_counts = [item[1] for item in sorted_defects]
            
            # Create color scale based on values
            colors = px.colors.sample_colorscale("Reds", [n/(max(defect_counts)) for n in defect_counts])
            
            # Create advanced horizontal bar chart
            fig = go.Figure(data=[go.Bar(
                y=defect_names,
                x=defect_counts,
                orientation='h',
                marker=dict(
                    color=colors,
                    line=dict(color='rgba(0,0,0,0.5)', width=1)
                ),
                text=[f'{count:,}' for count in defect_counts],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>' +
                             'Count: %{x:,}<br>' +
                             'Rank: %{customdata}<br>' +
                             '<extra></extra>',
                customdata=list(range(1, len(defect_names) + 1))
            )])
            
            fig.update_layout(
                title={
                    'text': f'🏆 Smart Ranking Analysis: Top {len(defect_names)} Rejection Causes',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#2E86AB'}
                },
                xaxis_title='Total Rejections',
                yaxis_title='Defect Type',
                height=max(500, len(defect_names) * 35),
                width=1200,
                margin=dict(l=300, r=100, t=100, b=50),
                showlegend=False,
                plot_bgcolor='rgba(240,240,240,0.5)',
                xaxis=dict(gridcolor='white', gridwidth=2),
                yaxis=dict(gridcolor='white', gridwidth=2, categoryorder='total ascending')
            )
            
            img_bytes = fig.to_image(format="png", width=1200, height=max(600, len(defect_names) * 35))
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Generate comprehensive analysis
            total_rejections = sum(defect_counts)
            top_3_percentage = sum(defect_counts[:3]) / total_rejections * 100
            
            response = f"📊 **Advanced Bar Chart Analysis: Rejection Rankings & Strategic Insights**\n\n"
            
            # Ranking insights
            response += f"🥇 **Performance Rankings:**\n"
            for i, (name, count) in enumerate(zip(defect_names[:3], defect_counts[:3]), 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                percentage = (count / total_rejections) * 100
                response += f"{medal} **Rank {i}**: {name} - {count:,} parts ({percentage:.1f}%)\n"
            
            response += f"\n🎯 **Strategic Focus Areas:**\n"
            response += f"• **Primary Target**: {defect_names[0]} ({defect_counts[0]:,} parts) - Maximum impact opportunity\n"
            response += f"• **Secondary Targets**: Top 3 combined = {top_3_percentage:.1f}% of all rejections\n"
            response += f"• **Quick Wins**: Address defects with >2% contribution for immediate improvement\n\n"
            
            # Performance gaps analysis
            if len(defect_counts) > 1:
                gap_1_2 = defect_counts[0] - defect_counts[1]
                response += f"📈 **Performance Gap Analysis:**\n"
                response += f"• **Leadership Gap**: #{1} exceeds #{2} by {gap_1_2:,} parts ({(gap_1_2/total_rejections*100):.1f}%)\n"
                response += f"• **Improvement Potential**: Reducing top defect to #{2} level saves {gap_1_2:,} rejections\n\n"
            
            # Categorization and recommendations
            response += f"🔧 **Process Improvement Recommendations:**\n"
            
            # Categorize defects
            sizing_defects = [name for name in defect_names if any(word in name.lower() for word in ['size', 'oversize', 'undersize', 'u/s', 'o/s'])]
            surface_defects = [name for name in defect_names if any(word in name.lower() for word in ['damage', 'mark', 'toolmark', 'burr'])]
            positioning_defects = [name for name in defect_names if any(word in name.lower() for word in ['position', 'off', 'pcd', 'symmetry'])]
            
            if sizing_defects:
                response += f"• **Sizing Issues** ({len(sizing_defects)} types): Review tooling calibration and measurement systems\n"
            if surface_defects:
                response += f"• **Surface Quality** ({len(surface_defects)} types): Optimize cutting parameters and tool condition\n"
            if positioning_defects:
                response += f"• **Positioning Accuracy** ({len(positioning_defects)} types): Check fixture setup and machine calibration\n"
            
            response += f"\n📊 **Interactive Visualization:**\n"
            response += f"![Chart](data:image/png;base64,{img_base64})"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating advanced bar chart:** {str(e)}"
    
    def _create_advanced_line_chart(self, question: str) -> str:
        """Create advanced trend analysis with predictions"""
        try:
            if 'Date' not in self.df.columns or 'Total Rej Qty.' not in self.df.columns:
                return "❌ **Date or rejection quantity data not available for trend analysis.**"
            
            # Prepare monthly data
            monthly_data = self.df.groupby(self.df['Date'].dt.to_period('M')).agg({
                'Total Rej Qty.': 'sum',
                'Inspected Qty.': 'sum'
            }).reset_index()
            
            monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()
            monthly_data['Rejection_Rate'] = (monthly_data['Total Rej Qty.'] / monthly_data['Inspected Qty.']) * 100
            
            # Create advanced multi-axis chart
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Quality Trend Analysis', 'Rejection Rate Performance'),
                vertical_spacing=0.1,
                specs=[[{"secondary_y": True}], [{"secondary_y": False}]]
            )
            
            # Main trend line
            fig.add_trace(
                go.Scatter(
                    x=monthly_data['Date'],
                    y=monthly_data['Total Rej Qty.'],
                    mode='lines+markers',
                    name='Total Rejections',
                    line=dict(color='#e74c3c', width=3),
                    marker=dict(size=8, color='#e74c3c'),
                    hovertemplate='<b>%{x}</b><br>Rejections: %{y:,}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Rejection rate
            fig.add_trace(
                go.Scatter(
                    x=monthly_data['Date'],
                    y=monthly_data['Rejection_Rate'],
                    mode='lines+markers',
                    name='Rejection Rate (%)',
                    line=dict(color='#f39c12', width=2, dash='dash'),
                    marker=dict(size=6, color='#f39c12'),
                    hovertemplate='<b>%{x}</b><br>Rate: %{y:.2f}%<extra></extra>'
                ),
                row=2, col=1
            )
            
            # Add trend line
            if len(monthly_data) > 3:
                x_numeric = np.arange(len(monthly_data))
                z = np.polyfit(x_numeric, monthly_data['Total Rej Qty.'], 1)
                trend_line = np.poly1d(z)(x_numeric)
                
                fig.add_trace(
                    go.Scatter(
                        x=monthly_data['Date'],
                        y=trend_line,
                        mode='lines',
                        name='Trend Line',
                        line=dict(color='#3498db', width=2, dash='dot'),
                        hovertemplate='<b>%{x}</b><br>Trend: %{y:,.0f}<extra></extra>'
                    ),
                    row=1, col=1
                )
            
            fig.update_layout(
                title={
                    'text': '📈 Advanced Quality Trend Analysis with Predictive Insights',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#2E86AB'}
                },
                height=800,
                width=1200,
                showlegend=True,
                hovermode='x unified'
            )
            
            fig.update_xaxes(title_text="Month", row=2, col=1)
            fig.update_yaxes(title_text="Total Rejections", row=1, col=1)
            fig.update_yaxes(title_text="Rejection Rate (%)", row=2, col=1)
            
            img_bytes = fig.to_image(format="png", width=1200, height=800)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Generate comprehensive trend analysis
            latest_rejections = monthly_data['Total Rej Qty.'].iloc[-1]
            first_rejections = monthly_data['Total Rej Qty.'].iloc[0]
            latest_rate = monthly_data['Rejection_Rate'].iloc[-1]
            avg_rate = monthly_data['Rejection_Rate'].mean()
            
            # Calculate trend
            if len(monthly_data) > 3:
                slope = np.polyfit(range(len(monthly_data)), monthly_data['Total Rej Qty.'], 1)[0]
                trend_direction = "📈 Improving (decreasing)" if slope < -10 else "📉 Declining (increasing)" if slope > 10 else "➡️ Stable"
            else:
                trend_direction = "➡️ Insufficient data for trend"
            
            response = f"📈 **Advanced Trend Analysis: Quality Performance Intelligence**\n\n"
            
            # Current status
            response += f"🎯 **Current Quality Status:**\n"
            response += f"• **Latest Performance**: {latest_rejections:,} rejections ({latest_rate:.2f}% rate)\n"
            response += f"• **Trend Direction**: {trend_direction}\n"
            response += f"• **Performance vs Baseline**: {'⬇️ Better' if latest_rejections < first_rejections else '⬆️ Worse'} than initial period\n"
            response += f"• **Analysis Period**: {len(monthly_data)} months of data\n\n"
            
            # Performance assessment
            response += f"📊 **Performance Assessment:**\n"
            if latest_rate > avg_rate * 1.2:
                response += f"🚨 **Alert**: Current rate ({latest_rate:.2f}%) is {((latest_rate/avg_rate-1)*100):.0f}% above average!\n"
            elif latest_rate < avg_rate * 0.8:
                response += f"✅ **Excellent**: Current rate ({latest_rate:.2f}%) is {((1-latest_rate/avg_rate)*100):.0f}% below average!\n"
            else:
                response += f"📊 **Stable**: Current rate ({latest_rate:.2f}%) is within normal range (avg: {avg_rate:.2f}%)\n"
            
            # Statistical insights
            volatility = monthly_data['Rejection_Rate'].std()
            response += f"• **Process Stability**: {'High volatility' if volatility > 2 else 'Moderate volatility' if volatility > 1 else 'Stable process'} (σ={volatility:.2f}%)\n"
            
            # Seasonal analysis
            if len(monthly_data) >= 12:
                monthly_data['Month'] = monthly_data['Date'].dt.month
                seasonal_avg = monthly_data.groupby('Month')['Rejection_Rate'].mean()
                peak_month = seasonal_avg.idxmax()
                best_month = seasonal_avg.idxmin()
                response += f"• **Seasonal Pattern**: Peak in month {peak_month} ({seasonal_avg[peak_month]:.1f}%), best in month {best_month} ({seasonal_avg[best_month]:.1f}%)\n"
            
            response += f"\n🔮 **Predictive Insights:**\n"
            if len(monthly_data) > 6:
                # Simple prediction based on trend
                if abs(slope) > 5:
                    next_month_pred = latest_rejections + slope
                    response += f"• **Next Month Forecast**: ~{max(0, next_month_pred):,.0f} rejections (trend-based)\n"
                
                # Performance targets
                target_reduction = latest_rejections * 0.1  # 10% reduction target
                response += f"• **Improvement Target**: Reduce by {target_reduction:,.0f} rejections (10%) to reach {latest_rejections - target_reduction:,.0f}\n"
            
            response += f"\n💡 **Strategic Recommendations:**\n"
            response += f"• **Process Control**: {'Immediate intervention needed' if latest_rate > avg_rate * 1.5 else 'Maintain current controls'}\n"
            response += f"• **Monitoring Frequency**: {'Daily' if volatility > 2 else 'Weekly'} quality reviews recommended\n"
            response += f"• **Focus Areas**: Target months/periods with consistently higher rejection rates\n\n"
            
            response += f"📈 **Interactive Trend Visualization:**\n"
            response += f"![Chart](data:image/png;base64,{img_base64})"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating advanced trend chart:** {str(e)}"
    
    def answer_question(self, question: str) -> str:
        """Main entry point for answering questions with super intelligence"""
        try:
            # Cache check
            cache_key = f"question_{hash(question.lower())}"
            if cache_key in self.cache:
                logger.info("📋 Returning cached response")
                return self.cache[cache_key]
            
            # Generate intelligent response
            response = self.generate_intelligent_response(question)
            
            # Cache the response
            self.cache[cache_key] = response
            
            # Update user preferences based on successful responses
            if "data:image/png;base64," in response:
                intent = self.analyze_intent(question)
                chart_type = intent.get('chart_preference', 'unknown')
                if chart_type != 'unknown':
                    self.conversation_context['preference_learning']['chart_types'][chart_type] += 1
            
            return response
            
        except Exception as e:
            logger.error(f"Error in answer_question: {e}")
            return f"❌ **I encountered an error while processing your question:** {str(e)}\n\nPlease try rephrasing your question or provide more specific details."
    
    # Additional handler methods would be implemented here...
    def _handle_analysis_request(self, question: str, intent: Dict) -> str:
        """Handle general analysis requests"""
        return self._get_comprehensive_analysis()
    
    def _handle_comparison_request(self, question: str, intent: Dict) -> str:
        """Handle comparison requests"""
        return "🔍 **Comparison analysis available.** Please specify what you'd like to compare (e.g., 'compare rejection rates between parts' or 'compare this month vs last month')."
    
    def _handle_ranking_request(self, question: str, intent: Dict) -> str:
        """Handle ranking requests with temporal scope support"""
        count = intent.get('requested_count', 5)
        temporal_scope = intent.get('temporal_scope', 'overall')
        grouping_requested = intent.get('grouping_requested', False)
        
        if temporal_scope == 'monthly' or grouping_requested:
            return self._get_monthly_rejection_analysis(count)
        else:
            return self._get_top_rejection_reasons(count)
    
    def _handle_prediction_request(self, question: str, intent: Dict) -> str:
        """Handle prediction requests"""
        return self._generate_predictions()
    
    def _handle_explanation_request(self, question: str, intent: Dict) -> str:
        """Handle explanation requests"""
        return self._provide_explanations(question)
    
    def _handle_general_request(self, question: str, intent: Dict) -> str:
        """Handle general requests with Google API fallback"""
        # Try Google API for better understanding first
        if self.google_model:
            try:
                response = self._generate_smart_response_with_api(question)
                if response and not response.startswith("❌"):
                    return response
            except Exception as e:
                logger.warning(f"Google API fallback failed: {e}")
        
        # Fallback to comprehensive analysis only if no specific intent detected
        return self._get_comprehensive_analysis()
    
    def _get_top_rejection_reasons(self, count: int = 5) -> str:
        """Get top rejection reasons with advanced analysis"""
        try:
            defect_totals = {}
            for col in self.defect_columns:
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:
                        defect_totals[col] = total
            
            if not defect_totals:
                return "❌ **No defect data found in the dataset.**"
            
            sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:count]
            total_rejections = sum(defect_totals.values())
            
            response = f"🎯 **Top {len(sorted_defects)} Rejection Reasons (AI-Enhanced Analysis):**\n\n"
            
            for i, (defect_type, count_val) in enumerate(sorted_defects, 1):
                percentage = (count_val / total_rejections) * 100
                severity = "🔴" if percentage > 10 else "🟠" if percentage > 5 else "🟡" if percentage > 2 else "🟢"
                response += f"{i}. {severity} **{defect_type}**: {count_val:,} parts ({percentage:.1f}%)\n"
            
            # Add AI insights
            response += f"\n🤖 **AI-Powered Insights:**\n"
            response += f"• **Pareto Analysis**: Top {min(3, len(sorted_defects))} defects account for {sum([count for _, count in sorted_defects[:3]])/total_rejections*100:.1f}% of rejections\n"
            response += f"• **Process Assessment**: {'Critical attention needed' if sorted_defects[0][1]/total_rejections > 0.3 else 'Manageable distribution'}\n"
            response += f"• **Improvement Potential**: Addressing top defect could reduce rejections by {sorted_defects[0][1]/total_rejections*100:.0f}%\n"
            
            return response
            
        except Exception as e:
            return f"❌ **Error analyzing rejection reasons:** {str(e)}"
    
    def _get_monthly_rejection_analysis(self, count: int = 5) -> str:
        """Get monthly breakdown of top rejection reasons"""
        try:
            if 'Date' not in self.df.columns:
                return "❌ **Date information not available for monthly analysis.**"
            
            # Group by month and get defect totals
            monthly_defects = {}
            months = self.df['Date'].dt.to_period('M').unique()
            
            response = f"📅 **Top {count} Rejection Reasons - Monthly Analysis:**\n\n"
            
            for month in sorted(months):
                month_data = self.df[self.df['Date'].dt.to_period('M') == month]
                month_defects = {}
                
                for col in self.defect_columns:
                    if col in month_data.columns:
                        total = month_data[col].sum()
                        if total > 0:
                            month_defects[col] = total
                
                if month_defects:
                    sorted_month_defects = sorted(month_defects.items(), key=lambda x: x[1], reverse=True)[:count]
                    total_month_rejections = sum(month_defects.values())
                    
                    response += f"📅 **{month} ({month_data['Date'].dt.strftime('%B %Y').iloc[0]}):**\n"
                    
                    for i, (defect_type, defect_count) in enumerate(sorted_month_defects, 1):
                        percentage = (defect_count / total_month_rejections) * 100
                        severity = "🔴" if percentage > 15 else "🟠" if percentage > 10 else "🟡" if percentage > 5 else "🟢"
                        response += f"  {i}. {severity} **{defect_type}**: {defect_count:,} parts ({percentage:.1f}%)\n"
                    
                    response += f"  📊 **Month Total**: {total_month_rejections:,} rejections\n"
                    
                    # Monthly insights
                    if len(sorted_month_defects) >= 3:
                        top_3_percentage = sum([count for _, count in sorted_month_defects[:3]]) / total_month_rejections * 100
                        response += f"  💡 **Top 3 Impact**: {top_3_percentage:.1f}% of monthly rejections\n"
                    
                    response += "\n"
            
            # Summary analysis across all months
            response += f"📊 **Cross-Month Analysis Summary:**\n"
            
            # Find the most consistent top defects across months
            defect_frequency = {}
            for month in sorted(months):
                month_data = self.df[self.df['Date'].dt.to_period('M') == month]
                month_defects = {}
                
                for col in self.defect_columns:
                    if col in month_data.columns:
                        total = month_data[col].sum()
                        if total > 0:
                            month_defects[col] = total
                
                if month_defects:
                    top_month_defect = max(month_defects, key=month_defects.get)
                    defect_frequency[top_month_defect] = defect_frequency.get(top_month_defect, 0) + 1
            
            if defect_frequency:
                most_frequent_defect = max(defect_frequency, key=defect_frequency.get)
                response += f"• **Most Consistent Issue**: {most_frequent_defect} (top defect in {defect_frequency[most_frequent_defect]} out of {len(months)} months)\n"
            
            # Seasonal patterns
            response += f"• **Temporal Coverage**: Analysis covers {len(months)} months\n"
            response += f"• **Trend Analysis**: {'Consistent patterns detected' if len(months) >= 6 else 'More data needed for trend analysis'}\n\n"
            
            response += f"💡 **Month-wise Recommendations:**\n"
            response += f"• **Focus Strategy**: Target the most consistent monthly top defects for sustainable improvement\n"
            response += f"• **Resource Planning**: Allocate quality resources based on monthly defect patterns\n"
            response += f"• **Process Control**: Implement month-specific quality measures for recurring issues\n"
            
            return response
            
        except Exception as e:
            return f"❌ **Error in monthly rejection analysis:** {str(e)}"
    
    def _get_comprehensive_analysis(self) -> str:
        """Provide comprehensive data analysis"""
        try:
            response = "📊 **Comprehensive Data Analysis Report**\n\n"
            
            # Data overview
            response += f"📋 **Dataset Overview:**\n"
            response += f"• Records: {len(self.df):,}\n"
            response += f"• Features: {len(self.df.columns)}\n"
            response += f"• Date Range: {self.df['Date'].min().strftime('%Y-%m-%d')} to {self.df['Date'].max().strftime('%Y-%m-%d')}\n"
            response += f"• Analysis Period: {(self.df['Date'].max() - self.df['Date'].min()).days} days\n\n"
            
            # Key metrics
            if 'Total Rej Qty.' in self.df.columns:
                total_rejections = self.df['Total Rej Qty.'].sum()
                total_inspected = self.df['Inspected Qty.'].sum()
                rejection_rate = (total_rejections / total_inspected) * 100
                
                response += f"📈 **Key Quality Metrics:**\n"
                response += f"• Total Rejections: {total_rejections:,}\n"
                response += f"• Total Inspected: {total_inspected:,}\n"
                response += f"• Overall Rejection Rate: {rejection_rate:.2f}%\n"
                response += f"• Quality Level: {'Excellent' if rejection_rate < 1 else 'Good' if rejection_rate < 3 else 'Needs Improvement'}\n\n"
            
            # ML insights if available
            if self.ml_models and 'ml_insights' in self.metadata:
                response += f"🤖 **Machine Learning Insights:**\n"
                top_features = self.metadata['ml_insights'].get('top_features', [])
                for i, (feature, importance) in enumerate(top_features, 1):
                    response += f"• **Factor {i}**: {feature} (importance: {importance:.3f})\n"
                response += "\n"
            
            # Anomaly detection results
            if 'anomalies' in self.metadata and self.metadata['anomalies']:
                response += f"⚠️ **Anomaly Detection Results:**\n"
                for anomaly_type, data in self.metadata['anomalies'].items():
                    response += f"• **{anomaly_type}**: {data['count']} anomalies ({data['percentage']:.1f}%)\n"
                response += "\n"
            
            response += f"💡 **Ask me specific questions like:**\n"
            response += f"• 'Create a pie chart of defects'\n"
            response += f"• 'Show trend analysis over time'\n"
            response += f"• 'What are the top 10 rejection reasons?'\n"
            response += f"• 'Predict next month's quality performance'\n"
            
            return response
            
        except Exception as e:
            return f"❌ **Error generating comprehensive analysis:** {str(e)}"
    
    def _generate_predictions(self) -> str:
        """Generate predictions using ML models"""
        try:
            if not self.ml_models:
                return "🔮 **Prediction capability not available.** Need more data to train predictive models."
            
            response = "🔮 **AI-Powered Predictions & Forecasts**\n\n"
            
            # Simple trend-based prediction
            if 'Date' in self.df.columns and 'Total Rej Qty.' in self.df.columns:
                monthly_data = self.df.groupby(self.df['Date'].dt.to_period('M'))['Total Rej Qty.'].sum()
                
                if len(monthly_data) > 3:
                    # Linear trend prediction
                    x = np.arange(len(monthly_data))
                    slope, intercept = np.polyfit(x, monthly_data.values, 1)
                    next_month_pred = slope * len(monthly_data) + intercept
                    
                    response += f"📈 **Next Month Forecast:**\n"
                    response += f"• Predicted Rejections: ~{max(0, next_month_pred):,.0f}\n"
                    response += f"• Trend Direction: {'⬇️ Improving' if slope < 0 else '⬆️ Declining' if slope > 0 else '➡️ Stable'}\n"
                    response += f"• Confidence: {'High' if len(monthly_data) > 12 else 'Medium' if len(monthly_data) > 6 else 'Low'}\n\n"
            
            # Feature importance predictions
            if 'ml_insights' in self.metadata:
                response += f"🎯 **Key Predictive Factors:**\n"
                top_features = self.metadata['ml_insights'].get('top_features', [])[:3]
                for feature, importance in top_features:
                    response += f"• **{feature}**: {importance:.1%} predictive power\n"
                response += "\n"
            
            response += f"💡 **Predictive Recommendations:**\n"
            response += f"• Monitor key predictive factors for early warning\n"
            response += f"• Implement predictive maintenance based on trends\n"
            response += f"• Use forecasts for resource planning and quality control\n"
            
            return response
            
        except Exception as e:
            return f"❌ **Error generating predictions:** {str(e)}"
    
    def _provide_explanations(self, question: str) -> str:
        """Provide explanations for quality issues"""
        try:
            response = "🔍 **Quality Analysis Explanations**\n\n"
            
            # Analyze the question for specific explanation needs
            if 'why' in question.lower():
                if any(word in question.lower() for word in ['high', 'increase', 'rising']):
                    response += f"🔍 **Why Quality Issues Increase:**\n"
                    response += f"• **Tool Wear**: Progressive deterioration affects precision\n"
                    response += f"• **Process Drift**: Gradual parameter changes over time\n"
                    response += f"• **Material Variation**: Inconsistent raw material properties\n"
                    response += f"• **Environmental Factors**: Temperature, humidity, vibration\n\n"
                    
                elif any(word in question.lower() for word in ['defect', 'rejection']):
                    response += f"🔍 **Root Causes of Defects:**\n"
                    
                    # Analyze actual defect patterns
                    defect_totals = {}
                    for col in self.defect_columns:
                        if col in self.df.columns:
                            total = self.df[col].sum()
                            if total > 0:
                                defect_totals[col] = total
                    
                    if defect_totals:
                        top_defect = max(defect_totals, key=defect_totals.get)
                        response += f"• **Primary Issue**: {top_defect} ({defect_totals[top_defect]:,} occurrences)\n"
                        
                        # Provide specific explanations based on defect type
                        if any(word in top_defect.lower() for word in ['oversize', 'undersize', 'size']):
                            response += f"  - **Likely Causes**: Tool wear, thermal expansion, measurement error\n"
                            response += f"  - **Solutions**: Calibration, tool replacement, temperature control\n"
                        elif any(word in top_defect.lower() for word in ['damage', 'mark', 'toolmark']):
                            response += f"  - **Likely Causes**: Worn tools, improper feeds/speeds, handling damage\n"
                            response += f"  - **Solutions**: Tool maintenance, parameter optimization, careful handling\n"
                        elif any(word in top_defect.lower() for word in ['position', 'off']):
                            response += f"  - **Likely Causes**: Fixture wear, setup error, machine accuracy\n"
                            response += f"  - **Solutions**: Fixture maintenance, setup verification, machine calibration\n"
            
            else:
                # General explanations
                response += f"📚 **Quality System Explanations:**\n"
                response += f"• **Rejection Rate**: Percentage of parts that don't meet specifications\n"
                response += f"• **Process Capability**: System's ability to produce consistent quality\n"
                response += f"• **Statistical Control**: Using data to monitor and improve processes\n"
                response += f"• **Root Cause Analysis**: Systematic investigation of problem sources\n\n"
            
            response += f"💡 **Ask specific questions like:**\n"
            response += f"• 'Why is [specific defect] happening?'\n"
            response += f"• 'How can I reduce rejection rates?'\n"
            response += f"• 'What causes sizing problems?'\n"
            
            return response
            
        except Exception as e:
            return f"❌ **Error providing explanations:** {str(e)}"
    
    def _generate_smart_response_with_api(self, question: str) -> str:
        """Generate smart responses using Google API for unhandled questions"""
        try:
            if not self.google_model:
                return "❌ **Google API not available for smart response generation.**"
            
            # Prepare data context for API
            data_summary = {
                'total_records': len(self.df),
                'date_range': f"{self.df['Date'].min().strftime('%Y-%m')} to {self.df['Date'].max().strftime('%Y-%m')}",
                'total_rejections': self.df['Total Rej Qty.'].sum() if 'Total Rej Qty.' in self.df.columns else 'N/A',
                'rejection_rate': f"{(self.df['Total Rej Qty.'].sum() / self.df['Inspected Qty.'].sum() * 100):.2f}%" if 'Total Rej Qty.' in self.df.columns else 'N/A',
                'top_defects': []
            }
            
            # Get top 3 defects for context
            defect_totals = {}
            for col in self.defect_columns[:10]:  # Limit to avoid token limits
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:
                        defect_totals[col] = total
            
            if defect_totals:
                sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:3]
                data_summary['top_defects'] = [{defect: count} for defect, count in sorted_defects]
            
            prompt = f"""
            You are an AI quality engineer analyzing manufacturing data. Answer this question based on the data context provided.
            
            Question: "{question}"
            
            Data Context:
            - Total Records: {data_summary['total_records']}
            - Date Range: {data_summary['date_range']}
            - Total Rejections: {data_summary['total_rejections']}
            - Overall Rejection Rate: {data_summary['rejection_rate']}
            - Top Defect Types: {data_summary['top_defects']}
            - Available Defect Categories: {len(self.defect_columns)} types
            
            Provide a comprehensive, professional response that:
            1. Directly addresses the question
            2. Uses the actual data context provided
            3. Includes specific insights and recommendations
            4. Uses professional formatting with emojis and bullet points
            5. Provides actionable next steps
            
            If the question asks for visualization, mention that charts can be created and suggest specific chart types.
            If the question is about forecasting or trends, provide analytical insights based on the data.
            
            Format your response professionally like a quality engineer would.
            """
            
            response = self.google_model.generate_content(prompt)
            api_response = response.text.strip()
            
            # Add a header to indicate this is an AI-powered response
            smart_response = f"🤖 **AI-Powered Quality Analysis**\n\n{api_response}"
            
            # If the response seems too generic or short, enhance it
            if len(api_response) < 200:
                smart_response += f"\n\n💡 **Additional Insights:**\n"
                smart_response += f"• Based on {data_summary['total_records']:,} records analyzed\n"
                smart_response += f"• Quality performance: {data_summary['rejection_rate']} rejection rate\n"
                smart_response += f"• Data spans: {data_summary['date_range']}\n\n"
                smart_response += f"📊 **Available Analysis Options:**\n"
                smart_response += f"• Create detailed charts and visualizations\n"
                smart_response += f"• Perform statistical analysis and trend detection\n"
                smart_response += f"• Generate predictive insights and forecasts\n"
            
            return smart_response
            
        except Exception as e:
            logger.error(f"Google API smart response failed: {e}")
            return f"❌ **Error generating smart response:** {str(e)}"
    
    def _create_correlation_heatmap(self, question: str) -> str:
        """Create correlation heatmap for numeric variables"""
        try:
            if len(self.numeric_columns) < 2:
                return "❌ **Insufficient numeric data for correlation analysis.**"
            
            # Select relevant numeric columns (limit to avoid clutter)
            relevant_cols = [col for col in self.numeric_columns 
                           if col in self.df.columns and self.df[col].sum() > 0][:15]
            
            if len(relevant_cols) < 2:
                return "❌ **No suitable numeric columns found for correlation analysis.**"
            
            # Calculate correlation matrix
            corr_matrix = self.df[relevant_cols].corr()
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=np.round(corr_matrix.values, 2),
                texttemplate="%{text}",
                textfont={"size": 10},
                hovertemplate='<b>%{x}</b><br><b>%{y}</b><br>Correlation: %{z:.3f}<extra></extra>'
            ))
            
            fig.update_layout(
                title={
                    'text': '🔥 Quality Metrics Correlation Heatmap - Data Relationships',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#2E86AB'}
                },
                width=1000,
                height=800,
                xaxis={'side': 'bottom'},
                yaxis={'side': 'left'}
            )
            
            # Convert to base64
            img_bytes = fig.to_image(format="png", width=1000, height=800)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Find strong correlations
            strong_correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_value = corr_matrix.iloc[i, j]
                    if abs(corr_value) > 0.5:  # Strong correlation threshold
                        strong_correlations.append({
                            'var1': corr_matrix.columns[i],
                            'var2': corr_matrix.columns[j],
                            'correlation': corr_value
                        })
            
            response = f"🔥 **Advanced Correlation Analysis - Data Relationship Intelligence**\n\n"
            
            if strong_correlations:
                response += f"⚡ **Strong Correlations Detected:**\n"
                for corr in sorted(strong_correlations, key=lambda x: abs(x['correlation']), reverse=True)[:5]:
                    strength = "Very Strong" if abs(corr['correlation']) > 0.8 else "Strong"
                    direction = "Positive" if corr['correlation'] > 0 else "Negative"
                    response += f"• **{corr['var1']}** ↔ **{corr['var2']}**: {strength} {direction} ({corr['correlation']:.3f})\n"
                response += "\n"
            
            response += f"📊 **Correlation Insights:**\n"
            response += f"• **Variables Analyzed**: {len(relevant_cols)} quality metrics\n"
            response += f"• **Strong Relationships**: {len(strong_correlations)} correlations above 0.5\n"
            response += f"• **Data Points**: {len(self.df):,} records analyzed\n\n"
            
            response += f"🎯 **Strategic Implications:**\n"
            if strong_correlations:
                response += f"• **Process Connections**: Related defects may share common root causes\n"
                response += f"• **Improvement Focus**: Fixing one issue may positively impact correlated problems\n"
                response += f"• **Quality Control**: Monitor correlated metrics together for better insights\n\n"
            else:
                response += f"• **Independent Issues**: Most defects appear to have separate root causes\n"
                response += f"• **Targeted Solutions**: Each defect type may require specific interventions\n\n"
            
            response += f"💡 **Recommendations:**\n"
            response += f"• **Root Cause Analysis**: Investigate shared causes for highly correlated defects\n"
            response += f"• **Process Optimization**: Address process parameters affecting multiple quality metrics\n"
            response += f"• **Monitoring Strategy**: Implement correlated metrics tracking for early detection\n\n"
            
            response += f"🔥 **Interactive Correlation Heatmap:**\n"
            response += f"![Chart](data:image/png;base64,{img_base64})"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating correlation heatmap:** {str(e)}"
    
    def _create_scatter_plot(self, question: str) -> str:
        """Create scatter plot for relationship analysis"""
        try:
            if len(self.numeric_columns) < 2:
                return "❌ **Need at least 2 numeric variables for scatter plot analysis.**"
            
            # Select two most relevant columns
            x_col = 'Total Rej Qty.' if 'Total Rej Qty.' in self.df.columns else self.numeric_columns[0]
            y_col = 'Inspected Qty.' if 'Inspected Qty.' in self.df.columns else self.numeric_columns[1]
            
            # Create scatter plot
            fig = px.scatter(
                self.df,
                x=x_col,
                y=y_col,
                title=f'📊 Quality Relationship Analysis: {y_col} vs {x_col}',
                hover_data=['Date'] if 'Date' in self.df.columns else None,
                color='Rejection_Rate' if 'Rejection_Rate' in self.df.columns else None,
                size='Total Rej Qty.' if 'Total Rej Qty.' in self.df.columns and x_col != 'Total Rej Qty.' else None
            )
            
            fig.update_layout(
                title={
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#2E86AB'}
                },
                width=1000,
                height=600
            )
            
            # Convert to base64
            img_bytes = fig.to_image(format="png", width=1000, height=600)
            img_base64 = base64.b64encode(img_bytes).decode()
            
            # Calculate correlation
            correlation = self.df[x_col].corr(self.df[y_col])
            
            response = f"📊 **Scatter Plot Analysis - Relationship Intelligence**\n\n"
            response += f"🔍 **Relationship Analysis:**\n"
            response += f"• **Variables**: {y_col} vs {x_col}\n"
            response += f"• **Correlation**: {correlation:.3f} ({'Strong positive' if correlation > 0.7 else 'Moderate positive' if correlation > 0.3 else 'Weak positive' if correlation > 0 else 'Negative' if correlation < 0 else 'No correlation'})\n"
            response += f"• **Data Points**: {len(self.df):,} observations\n\n"
            
            response += f"📈 **Key Insights:**\n"
            if abs(correlation) > 0.5:
                response += f"• **Strong Relationship**: Changes in {x_col} are {'positively' if correlation > 0 else 'negatively'} associated with {y_col}\n"
                response += f"• **Predictive Power**: {x_col} can help predict {y_col} patterns\n"
            else:
                response += f"• **Independent Behavior**: {x_col} and {y_col} show little linear relationship\n"
                response += f"• **Separate Analysis**: Each variable should be analyzed independently\n"
            
            response += f"\n📊 **Interactive Scatter Plot:**\n"
            response += f"![Chart](data:image/png;base64,{img_base64})"
            
            return response
            
        except Exception as e:
            return f"❌ **Error creating scatter plot:** {str(e)}"
    
    def _generate_primary_response_with_api(self, question: str) -> str:
        """Generate primary response using Google API with data context"""
        try:
            if not self.google_model:
                return "❌ **Google API not available.**"
            
            # Prepare comprehensive data context
            data_context = self._prepare_data_context_for_api()
            
            prompt = f"""
            You are a helpful AI assistant that analyzes manufacturing quality data. Answer the user's question in a conversational, friendly way like ChatGPT.
            
            User Question: "{question}"
            
            Data Available:
            {data_context}
            
            RESPONSE STYLE:
            1. Be conversational and friendly, not formal or business-like
            2. Answer directly without email greetings or formal structure
            3. Use specific data insights with emojis and clear formatting
            4. Provide helpful recommendations in a casual, advisory tone
            5. If asked for charts, mention what visualization would help
            6. Be confident about the data quality ({len(self.df):,} records over {(self.df['Date'].max() - self.df['Date'].min()).days} days)
            
            Respond like you're having a helpful conversation, not writing a business report.
            """
            
            response = self.google_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Primary API response failed: {e}")
            return f"❌ **Error generating API response:** {str(e)}"
    
    def _prepare_data_context_for_api(self) -> str:
        """Prepare comprehensive data context for Google API"""
        try:
            context = f"Data Overview:\n"
            context += f"- Records: {len(self.df):,}\n"
            context += f"- Date Range: {self.df['Date'].min().strftime('%Y-%m-%d')} to {self.df['Date'].max().strftime('%Y-%m-%d')}\n"
            
            if 'Total Rej Qty.' in self.df.columns:
                total_rejections = self.df['Total Rej Qty.'].sum()
                total_inspected = self.df['Inspected Qty.'].sum()
                rejection_rate = (total_rejections / total_inspected) * 100
                
                context += f"\nQuality Metrics:\n"
                context += f"- Total Rejections: {total_rejections:,}\n"
                context += f"- Total Inspected: {total_inspected:,}\n"
                context += f"- Overall Rejection Rate: {rejection_rate:.2f}%\n"
            
            # Top defects
            defect_totals = {}
            for col in self.defect_columns[:10]:  # Limit for API token limits
                if col in self.df.columns:
                    total = self.df[col].sum()
                    if total > 0:
                        defect_totals[col] = total
            
            if defect_totals:
                sorted_defects = sorted(defect_totals.items(), key=lambda x: x[1], reverse=True)[:5]
                context += f"\nTop 5 Defect Types:\n"
                for i, (defect, count) in enumerate(sorted_defects, 1):
                    percentage = (count / sum(defect_totals.values())) * 100
                    context += f"{i}. {defect}: {count:,} parts ({percentage:.1f}%)\n"
            
            # Recent trends
            if 'Date' in self.df.columns and len(self.df) > 30:
                recent_data = self.df.tail(30)
                recent_rejections = recent_data['Total Rej Qty.'].sum() if 'Total Rej Qty.' in self.df.columns else 0
                context += f"\nRecent Trends (Last 30 records):\n"
                context += f"- Recent Rejections: {recent_rejections:,}\n"
            
            return context
            
        except Exception as e:
            return f"Error preparing context: {str(e)}"
    
    def _extract_data_requirements_with_nlp(self, question: str) -> Dict[str, Any]:
        """Extract specific data requirements from question using NLP"""
        requirements = {
            'needs_data_extraction': False,
            'chart_type': None,
            'temporal_analysis': False,
            'specific_defects': [],
            'specific_months': [],
            'count_requested': None
        }
        
        question_lower = question.lower()
        
        # Check for visualization requests
        viz_keywords = ['chart', 'graph', 'plot', 'visualization', 'visualize', 'show']
        if any(keyword in question_lower for keyword in viz_keywords):
            requirements['needs_data_extraction'] = True
            
            # Detect chart type
            if 'pie' in question_lower:
                requirements['chart_type'] = 'pie'
            elif 'bar' in question_lower:
                requirements['chart_type'] = 'bar'
            elif 'line' in question_lower or 'trend' in question_lower:
                requirements['chart_type'] = 'line'
            elif 'heatmap' in question_lower:
                requirements['chart_type'] = 'heatmap'
        
        # Check for temporal analysis
        temporal_keywords = ['monthly', 'every month', 'month by month', 'over time', 'trend']
        if any(keyword in question_lower for keyword in temporal_keywords):
            requirements['temporal_analysis'] = True
            requirements['needs_data_extraction'] = True
        
        # Extract specific defects mentioned
        for defect in self.defect_columns:
            if defect.lower() in question_lower:
                requirements['specific_defects'].append(defect)
                requirements['needs_data_extraction'] = True
        
        # Extract month names
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                 'july', 'august', 'september', 'october', 'november', 'december']
        for month in months:
            if month in question_lower:
                requirements['specific_months'].append(month)
                requirements['needs_data_extraction'] = True
        
        # Extract count requests
        numbers = re.findall(r'\b(\d+)\b', question)
        if numbers:
            requirements['count_requested'] = int(numbers[0])
        
        return requirements
    
    def _enhance_response_with_data(self, api_response: str, requirements: Dict[str, Any]) -> str:
        """Enhance API response with specific data extraction and visualization"""
        try:
            enhanced_response = api_response
            
            # Add specific data if chart was requested
            if requirements.get('chart_type'):
                enhanced_response += "\n\n📊 **Data Visualization:**\n"
                
                if requirements['chart_type'] == 'pie':
                    chart_response = self._create_advanced_pie_chart("", requirements.get('count_requested', 10))
                    if "data:image/png;base64," in chart_response:
                        # Extract just the chart part
                        chart_start = chart_response.find("![Chart]")
                        if chart_start != -1:
                            enhanced_response += chart_response[chart_start:]
                elif requirements['chart_type'] == 'bar':
                    chart_response = self._create_advanced_bar_chart("", requirements.get('count_requested', 15))
                    if "data:image/png;base64," in chart_response:
                        chart_start = chart_response.find("![Chart]")
                        if chart_start != -1:
                            enhanced_response += chart_response[chart_start:]
                elif requirements['chart_type'] == 'line':
                    chart_response = self._create_advanced_line_chart("")
                    if "data:image/png;base64," in chart_response:
                        chart_start = chart_response.find("![Chart]")
                        if chart_start != -1:
                            enhanced_response += chart_response[chart_start:]
                elif requirements['chart_type'] == 'heatmap':
                    chart_response = self._create_correlation_heatmap("")
                    if "data:image/png;base64," in chart_response:
                        chart_start = chart_response.find("![Chart]")
                        if chart_start != -1:
                            enhanced_response += chart_response[chart_start:]
            
            # Add temporal analysis if requested
            elif requirements.get('temporal_analysis'):
                enhanced_response += "\n\n📅 **Temporal Analysis:**\n"
                monthly_analysis = self._get_monthly_rejection_analysis(requirements.get('count_requested', 5))
                # Extract key insights from monthly analysis
                if "Cross-Month Analysis Summary" in monthly_analysis:
                    summary_start = monthly_analysis.find("📊 **Cross-Month Analysis Summary:**")
                    if summary_start != -1:
                        enhanced_response += monthly_analysis[summary_start:]
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Error enhancing response: {e}")
            return api_response  # Return original if enhancement fails

# Test function
def test_super_intelligent_analyzer():
    """Test the super intelligent analyzer"""
    try:
        analyzer = SuperIntelligentAnalyzer('uploads/QUALITY_DAILY_Machining_Rejection.xlsx')
        
        test_questions = [
            "Create an advanced pie chart of rejection reasons",
            "Show me trend analysis with predictions",
            "What are the top 5 defects and why do they occur?",
            "Generate a comprehensive quality report",
            "Predict next month's quality performance",
            "Explain why rejection rates are high",
            "Compare performance across different time periods"
        ]
        
        print("🧪 Testing Super Intelligent Analyzer")
        print("=" * 60)
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{i}. Question: '{question}'")
            response = analyzer.answer_question(question)
            print("Response preview:", response[:200] + "..." if len(response) > 200 else response)
            print("-" * 60)
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_super_intelligent_analyzer()
