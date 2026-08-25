Skylark Drones — Founder Business Intelligence Agent

An AI-powered Founder Business Intelligence Dashboard that connects to monday.com and answers natural-language questions about Skylark Drones' sales pipeline, operations, billing, collections, receivables, and overall business performance.

Built for founders and leadership teams, the application transforms messy operational data into actionable business insights while explicitly surfacing data-quality limitations instead of hiding missing or inconsistent records.

✨ Features
📊 monday.com Integration

Secure read-only integration with monday.com GraphQL API.

Dynamically retrieves live business data from:

Deals Board

Work Orders Board

No business data is hardcoded.

monday.com credentials remain securely on the backend.

🤖 AI Business Intelligence Agent

Ask questions in plain English such as:

How's our pipeline looking for the Energy sector this quarter?

Which sectors have the strongest active pipeline?

How much is currently receivable?

Compare Renewables pipeline with Renewables work orders.

Give me a leadership update.

The agent analyzes live business data and returns founder-oriented insights.

📈 Executive Metrics

The dashboard provides insights into:

Active sales pipeline

Weighted pipeline forecast

Pipeline by sector

Won vs Lost deal value

Work order execution status

Work orders by sector

Billing performance

Collections

Receivables

Amount remaining to be billed

Data quality health

Executive leadership summaries

🧹 Data Quality Intelligence

Designed for real-world operational datasets.

Automatically detects and reports:

Missing deal values

Missing close dates

Missing billing information

Missing collection information

Null or empty fields

Currency formatting inconsistencies

Sector naming inconsistencies

Status inconsistencies

Invalid or incomplete dates

Instead of guessing missing information, the application clearly communicates forecasting limitations.

🏗️ System Architecture
                   Founder / Leadership Team
                           │
                           ▼
                React + Vite Frontend Dashboard
                           │
                           ▼
                    FastAPI Backend API
                           │
     ┌─────────────────────┼─────────────────────┐
     ▼                     ▼                     ▼
 AI Query Router      Metrics Engine      Data Quality Engine
     │                     │                     │
     └─────────────────────┼─────────────────────┘
                           ▼
                  Data Normalization Layer
                           ▼
                 monday.com Repository Layer
                           ▼
                 monday.com GraphQL API
                           ▼
              Deals Board + Work Orders Board
🛠️ Tech Stack

Layer

	

Technology




Frontend

	

React, Vite, CSS




Backend

	

FastAPI, Python




Data Processing

	

Pandas




API Server

	

Uvicorn




Business Data

	

monday.com GraphQL API




AI Layer

	

Gemini API




Environment Management

	

python-dotenv

📁 Project Structure
skylark-bi-agent/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── data/
│   │   ├── monday/
│   │   ├── schemas/
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── DECISION_LOG.md
│
├── .gitignore
└── README.md
🚀 Getting Started
1. Clone the Repository
git clone https://github.com/<your-username>/skylark-bi-agent.git
cd skylark-bi-agent
2. Backend Setup

Navigate to the backend folder.

cd backend
Create a Virtual Environment

Windows

python -m venv venv
.\venv\Scripts\Activate.ps1

macOS / Linux

python3 -m venv venv
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Configure Environment Variables

Create a .env file inside the backend folder.

MONDAY_API_TOKEN=your_monday_api_token
DEALS_BOARD_ID=your_deals_board_id
WORK_ORDERS_BOARD_ID=your_work_orders_board_id
GEMINI_API_KEY=your_gemini_api_key

Important: Never commit .env to GitHub.

Start the Backend Server
uvicorn app.main:app --reload

Backend URL:

http://127.0.0.1:8000

Swagger API Documentation:

http://127.0.0.1:8000/docs
3. Frontend Setup

Open another terminal.

cd frontend
Install Node Packages
npm install
Start the Frontend
npm run dev

Vite will start the application at:

http://localhost:5173
🔐 monday.com Configuration

Create two monday.com boards using the assignment dataset.

Deals Board

Required fields:

Field




Deal Name




Client




Owner




Deal Status




Deal Stage




Sector




Product




Deal Value




Closure Probability




Close Date




Tentative Close Date




Created Date

Work Orders Board

Required fields:

Field




Customer




Serial Number




Nature of Work




Execution Status




Sector




Owner




Type of Work




Software Involvement




PO / LOI Date




Probable Start Date




Probable End Date




Data Delivery Date




Invoice Number




Last Invoice Date




Amount




Billed Value




Collected Amount




Amount to be Billed




Receivable




Invoice Status




Billing Status




Collection Status




Collection Date




Quantity

Column mappings are configured in:

backend/app/data/column_mapping.py
📡 API Endpoints

Method

	

Endpoint

	

Description




GET

	

/

	

Health check




GET

	

/boards

	

Configured monday.com boards




GET

	

/data/summary

	

Business metrics and data quality summary




POST

	

/ask

	

AI business intelligence query

Example AI Request
{
  "question": "Give me a leadership update."
}
Example Response
{
  "answer": "Executive summary...\nKey metrics...\nRisks...\nRecommended actions..."
}
📊 Business Logic
Active Pipeline

Includes only deals with status:

Open

On Hold

Excludes:

Won

Lost / Dead

Weighted Pipeline

Probability mapping used for forecasting:

Probability

	

Weight




High

	

80%




Medium

	

50%




Low

	

20%

Weighted Pipeline = Deal Value × Probability Weight.

Quarterly Forecast Logic

The application uses:

close_date

tentative_close_date

If both are missing, the deal is excluded from period-based forecasting because it cannot be assigned to a reliable reporting period.

🧠 Supported Business Questions
Sales Pipeline

Active pipeline value.

Weighted pipeline forecast.

Pipeline by owner.

Pipeline by sector.

Won vs Lost deals.

Quarter-wise pipeline.

Operations

Ongoing work orders.

Completed work orders.

Work orders by sector.

Execution status.

Software involvement.

Finance

Total billed value.

Collections received.

Outstanding receivables.

Remaining amount to bill.

Invoice status breakdown.

Leadership Updates

Founder-style executive summaries including:

Executive Summary

Key Metrics

Wins

Risks / Watch-outs

Recommended Actions

🧹 Data Quality Handling

The backend is resilient to incomplete business data.

It automatically normalizes:

Null values.

Empty strings.

N/A.

Currency-formatted numbers.

Percentage values.

Mixed date formats.

Sector aliases.

Status aliases.

Example Data Quality Report

Issue

	

Business Impact




Missing Close Date

	

Quarter forecast unavailable.




Missing Deal Value

	

Pipeline underestimated.




Missing Probability

	

Weighted forecast unavailable.




Missing Billing Value

	

Revenue visibility reduced.




Missing Collection Status

	

Cash flow visibility reduced.

The AI agent explicitly reports these limitations rather than generating assumptions.

🔒 Security

API keys are stored using environment variables.

MONDAY_API_TOKEN and GEMINI_API_KEY remain server-side.

The frontend never communicates directly with monday.com.

The application performs read-only operations and never modifies monday.com data.

📌 Assignment Deliverables

This repository includes:

React conversational dashboard.

FastAPI backend.

monday.com GraphQL integration.

Data normalization engine.

Business metrics engine.

Data quality analysis.

AI Business Intelligence Agent.

Leadership update capability.

Architecture Decision Log.

📄 Decision Log

See:

docs/DECISION_LOG.md

The Decision Log documents architecture decisions, assumptions, trade-offs, error handling, data quality strategy, and future improvements.

🌱 Future Improvements

Interactive business dashboards with charts.

Revenue forecasting over time.

Authentication and role-based access.

Caching monday.com API responses.

Export leadership updates to PDF.

Slack or email executive summaries.

