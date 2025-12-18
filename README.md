# ChatGPT-Style Analytics Bot

A web application that provides ChatGPT-like interface for data analysis, calculations, and visualizations.

## Features

- 💬 ChatGPT-style conversational interface
- 📊 Data analysis from CSV, Excel, PDF files
- 📈 Graph generation (pie charts, line graphs, bar charts)
- 🖼️ Image generation and processing
- 📤 File upload functionality (images, PDFs, CSV, Excel)
- 🧮 Complex calculations and data insights
- 📱 Responsive design
- ☁️ **Serverless deployment ready** (Vercel)

## Tech Stack

**Frontend:**
- React.js with TypeScript
- Tailwind CSS for styling
- Chart.js for data visualizations
- Axios for API calls

**Backend:**
- Python Flask/FastAPI
- Pandas for data analysis
- Matplotlib/Plotly for chart generation
- PIL for image processing
- OpenAI API integration
- File processing libraries

## Quick Start

1. Install dependencies:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Add your OpenAI API key and other configurations
```

3. Run the application:
```bash
# Backend
cd backend
python app.py

# Frontend
cd frontend
npm start
```

## Project Structure

```
chatbot-analytics/
├── api/                    # Serverless API functions (Vercel)
│   ├── upload.py          # File upload endpoint
│   ├── chat.py            # AI chat endpoint
│   ├── charts.py          # Chart generation
│   └── health.py          # Health check
├── backend/               # Original Flask app (for local dev)
│   ├── app.py            # Main Flask application
│   ├── requirements.txt  # Python dependencies
│   └── uploads/          # File upload directory
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── vercel.json           # Vercel deployment config
├── requirements.txt      # Serverless dependencies
└── README.md
```

## Deployment

### Vercel (Recommended)

This app is configured for serverless deployment on Vercel:

1. **Quick Deploy**: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

2. **Manual Setup**: See detailed guide in [`VERCEL_DEPLOYMENT.md`](./VERCEL_DEPLOYMENT.md)

3. **Environment Variables** (required):
   - `GOOGLE_API_KEY`: Your Google AI API key

### Local Development

For development, you can still run the original Flask backend:

```bash
# Backend (Terminal 1)
cd backend
pip install -r requirements.txt
python app.py

# Frontend (Terminal 2)
cd frontend
npm install
npm run dev
```
