# Skylark Drones — Founder Business Intelligence Agent

An AI-powered Founder Business Intelligence Agent that connects to
[monday.com](https://monday.com) and answers natural-language questions
about Skylark Drones' sales pipeline, operations, billing, collections,
receivables, and overall business performance.

The application is designed for founders and leadership teams who need
quick, actionable insights from messy operational data without manually
querying multiple business systems.

The agent dynamically retrieves data from monday.com, normalizes inconsistent
records, calculates business metrics, and uses an AI layer to convert the
results into founder-oriented insights.

> **Important:** The application is read-only with respect to monday.com.
> It does not create, update, or delete business records.

---

## 🚀 Live Prototype

### Frontend

**Hosted Prototype:**

https://skylark-bi-agent-1-d60b.onrender.com

Use the frontend URL above to interact with the complete dashboard and
conversational BI agent.

### Backend

**Backend API:**

https://skylark-bi-agent-o454.onrender.com

### API Documentation

https://skylark-bi-agent-o454.onrender.com/docs

The backend exposes interactive Swagger/OpenAPI documentation for testing
the available API endpoints.

---

# ✨ Features

## 📊 monday.com Integration

The application integrates with monday.com through its GraphQL API.

It dynamically retrieves live business data from two separate boards:

- Deals
- Work Orders

The application does **not** hardcode the supplied CSV/XLSX business data.

The architecture follows a read-only approach:

```text
React Frontend
      │
      ▼
FastAPI Backend
      │
      ▼
Monday.com Repository
      │
      ▼
Monday.com GraphQL API
      │
      ├── Deals Board
      │
      └── Work Orders Board

Monday.com credentials remain on the backend and are never exposed to the
frontend.

🤖 AI Business Intelligence Agent

Founders can ask questions in natural language.

Example questions:

How's our pipeline looking for the Energy sector this quarter?
Which sectors have the strongest active pipeline?
How much is currently receivable?
How many work orders are ongoing?
Compare Renewables pipeline with Renewables work orders.
What are the biggest data quality issues?
Give me a leadership update.

The agent combines dynamically retrieved business data with deterministic
business metrics and produces executive-oriented responses.

📈 Executive Dashboard

The dashboard provides visibility into:

Sales
Active pipeline
Weighted pipeline
Active deals
Pipeline by sector
Pipeline by owner
Won deal value
Lost / Dead deal value
Quarter-wise pipeline
Operations
Total work orders
Work-order execution status
Completed work orders
Ongoing work orders
Not-started work orders
Paused / struck work orders
Work orders by sector
Software involvement
Finance
Total billed value
Total collected value
Outstanding receivables
Amount remaining to be billed
Invoice status
Billing status
Collection status
Data Quality
Missing deal values
Missing close dates
Missing probabilities
Missing billing information
Missing collection information
Missing dates
Null and empty values
Inconsistent text values
Currency formatting issues
🧠 Business Intelligence Architecture
                    ┌──────────────────────────┐
                    │   Founder / Leadership   │
                    │    Natural Language      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │     React + Vite         │
                    │    Founder Dashboard     │
                    │                          │
                    │ Overview                 │
                    │ Pipeline                 │
                    │ Operations               │
                    │ AI Business Agent        │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      FastAPI API         │
                    └────────────┬─────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
      ┌──────────────┐   ┌──────────────┐   ┌───────────────┐
      │ AI Query     │   │ Metrics      │   │ Data Quality  │
      │ Router       │   │ Engine       │   │ Engine        │
      └──────┬───────┘   └──────┬───────┘   └───────┬───────┘
             │                  │                   │
             └──────────────────┼───────────────────┘
                                ▼
                    ┌──────────────────────────┐
                    │   Data Normalization     │
                    │         Layer            │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │  Monday.com Repository   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   Monday.com GraphQL     │
                    │           API            │
                    └────────────┬─────────────┘
                                 │
                         ┌───────┴────────┐
                         ▼                ▼
                   Deals Board      Work Orders Board
🛠️ Tech Stack
Layer	Technology
Frontend	React
Frontend Build Tool	Vite
Styling	CSS
Backend	Python
API Framework	FastAPI
Data Processing	Pandas
API Server	Uvicorn
Business Data	monday.com
Integration	monday.com GraphQL API
AI Layer	Gemini API
Environment Management	python-dotenv
Containerization	Docker
Hosting	Render
📁 Project Structure
skylark-bi-agent/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── agent/
│   │   │   ├── agent.py
│   │   │   ├── prompts.py
│   │   │   └── router.py
│   │   │
│   │   ├── data/
│   │   │   ├── column_mapping.py
│   │   │   ├── metrics.py
│   │   │   ├── normalizer.py
│   │   │   └── quality.py
│   │   │
│   │   ├── monday/
│   │   │   ├── client.py
│   │   │   └── repository.py
│   │   │
│   │   ├── schemas/
│   │   │   └── models.py
│   │   │
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── DECISION_LOG.md
│
├── .gitignore
├── docker-compose.yml
└── README.md
🚀 Getting Started
1. Clone the Repository
git clone https://github.com/ShreyaVenkangouda/skylark-bi-agent.git
cd skylark-bi-agent
Backend Setup
2. Navigate to Backend
cd backend
3. Create a Virtual Environment
Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
macOS / Linux
python3 -m venv venv
source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
🔐 Environment Variables

Create:

backend/.env

with:

MONDAY_API_TOKEN=your_monday_api_token
DEALS_BOARD_ID=your_deals_board_id
WORK_ORDERS_BOARD_ID=your_work_orders_board_id
GEMINI_API_KEY=your_gemini_api_key

The exact monday.com column mappings are configured in:

backend/app/data/column_mapping.py
Security

Never commit the real .env file.

The following credentials must remain server-side:

MONDAY_API_TOKEN
GEMINI_API_KEY

The repository contains .env.example for configuration reference.

▶️ Run the Backend Locally

From the backend directory:

uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
🎨 Frontend Setup

Open another terminal.

cd frontend

Install dependencies:

npm install

Set the frontend API URL if required:

VITE_API_URL=http://127.0.0.1:8000

Start the frontend:

npm run dev

Vite will provide the local frontend URL, typically:

http://localhost:5173
🐳 Docker Setup

The application can also be run using Docker.

The repository contains separate Dockerfiles for the backend and frontend.

Build the containers

From the project root:

docker compose build
Start the application
docker compose up

The frontend and backend will run as separate containers.

The frontend communicates with the backend through the configured
VITE_API_URL.

To stop the application:

docker compose down
☁️ Deployment

The hosted prototype uses Render.

The application is deployed as two services:

                    Render
                      │
            ┌─────────┴─────────┐
            │                   │
            ▼                   ▼
       Frontend Service    Backend Service
            │                   │
            │                   ▼
            │             FastAPI
            │                   │
            │                   ▼
            │             monday.com
            │
            └──────► Backend API

The frontend uses:

VITE_API_URL=https://skylark-bi-agent-o454.onrender.com

The backend stores the monday.com and Gemini credentials as server-side
environment variables.

🔐 monday.com Configuration

Create two separate monday.com boards using the supplied assignment data.

Deals Board

The application expects the Deals board to contain fields corresponding to:

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

The application expects the Work Orders board to contain fields corresponding
to:

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
Method	Endpoint	Description
GET	/	Health check
GET	/boards	Configured monday.com boards
GET	/data/summary	Business metrics and data-quality summary
POST	/ask	Natural-language BI query
Health Check
GET /

Used to verify that the backend is running.

Board Information
GET /boards

Returns information about the configured monday.com boards.

Business Data Summary
GET /data/summary

Returns calculated business metrics including:

Pipeline metrics
Operational metrics
Financial metrics
Pipeline by sector
Work orders by sector
Data-quality indicators
AI Business Intelligence
POST /ask

Example request:

{
  "question": "Give me a leadership update."
}

Example response:

{
  "answer": "Executive summary...\nKey metrics...\nRisks...\nRecommended actions..."
}
📊 Business Logic
Active Pipeline

Active pipeline includes deals whose status is:

Open
On Hold

The following statuses are excluded:

Won
Lost
Dead
Weighted Pipeline

The application calculates weighted pipeline using deal value and the
available probability information.

The standard probability mapping is:

Probability	Weight
High	80%
Medium	50%
Low	20%

Conceptually:

Weighted Pipeline
=
Deal Value × Probability Weight

Missing probability information is surfaced as a data-quality limitation
rather than being silently interpreted as a guaranteed probability.

📅 Quarterly Forecast Logic

For period-specific analysis, the application uses:

close_date
     │
     │ missing
     ▼
tentative_close_date

If both dates are missing, the deal cannot reliably be assigned to a
reporting period.

The application therefore avoids inventing a reporting period for those
records.

🧹 Data Quality Intelligence

The assignment data contains real-world inconsistencies and incomplete
records.

The application explicitly detects and communicates these issues.

It handles:

Null values
Empty strings
N/A values
Missing financial fields
Missing dates
Mixed date formats
Currency-formatted numbers
Percentage-formatted probabilities
Sector naming differences
Status naming differences
Incomplete billing records
Incomplete collection records
📋 Data Quality Impact
Issue	Business Impact
Missing Close Date	Quarter forecasting becomes less reliable
Missing Deal Value	Pipeline value may be understated
Missing Probability	Weighted forecast becomes less reliable
Missing Billing Value	Revenue visibility is reduced
Missing Collection Information	Cash-flow visibility is reduced
Inconsistent Sector Names	Sector-level aggregation can be affected
Inconsistent Status Names	Pipeline classification can be affected
Missing Dates	Period-based analysis may be incomplete

The application reports these limitations directly to executives rather than
silently filling in business information.

💬 Supported Business Questions
Sales Pipeline

The agent can answer questions about:

Active pipeline
Weighted pipeline
Pipeline by sector
Pipeline by owner
Active deal counts
Won deals
Lost / Dead deals
Quarter-wise pipeline
Sector performance
Pipeline concentration

Example:

Which sectors have the strongest active pipeline?
Operations

The agent can answer:

How many work orders are ongoing?
How many are completed?
Which sectors have the most work orders?
What is the execution-status breakdown?
How many projects are paused?
Which sectors have the strongest operational footprint?
How involved is software in current work?
Finance

The agent can answer:

How much has been billed?
How much has been collected?
How much is currently receivable?
How much remains to be billed?
What is the invoice status breakdown?
What is the collection status?
Cross-functional Questions

The agent can combine information across the Deals and Work Orders boards.

Example:

Compare Renewables pipeline with Renewables work orders.

This allows leadership to compare sales opportunity with operational
execution in the same sector.

👔 Leadership Updates

The application supports an executive leadership-update mode.

When the user asks:

Give me a leadership update.

the agent produces a structured summary containing:

EXECUTIVE SUMMARY

KEY METRICS

WINS

RISKS / WATCH-OUTS

RECOMMENDED ACTIONS

The leadership update combines:

Sales pipeline
Pipeline concentration
Operational execution
Billing
Collections
Receivables
Work-order status
Data-quality risks

The purpose is to transform raw business data into a concise founder-level
business review.

🔒 Read-Only Design

The application follows the assignment's read-only requirement.

It only retrieves information from monday.com.

It does not:

Create boards
Create items
Update items
Delete items
Modify business records
Change statuses
Modify financial information

All calculations and AI insights are generated from dynamically retrieved
data.

🔐 Security

Sensitive credentials are stored using environment variables.

The following values must never be exposed in the frontend:

MONDAY_API_TOKEN
GEMINI_API_KEY

The frontend communicates with the FastAPI backend.

It does not communicate directly with monday.com.

The backend is responsible for authentication with monday.com and the AI
provider.

⚠️ Error Handling

The backend is designed to handle:

monday.com API failures
Missing board configuration
Missing columns
Missing data
Invalid financial values
Invalid dates
Empty records
AI API failures

The application surfaces data limitations instead of generating unsupported
business conclusions.

🧪 Example Founder Queries
Pipeline
How's our pipeline looking for the Energy sector this quarter?
Sector Comparison
Which sectors have the strongest active pipeline?
Collections
How much is currently receivable?
Operations
How many work orders are ongoing?
Cross-functional Analysis
Compare Renewables pipeline with Renewables work orders.
Data Quality
What are the biggest data quality issues?
Leadership
Give me a leadership update.
📌 Assignment Requirement Coverage
Assignment Requirement	Implementation
monday.com integration	monday.com GraphQL API
Read-only access	Backend only performs read operations
Deals board	Monday.com repository
Work Orders board	Monday.com repository
Messy data handling	Normalization layer
Missing values	Data quality engine
Query understanding	AI query router
Business intelligence	Metrics engine + AI
Conversational interface	React chat interface
Pipeline analysis	Metrics engine
Sector analysis	Sector aggregation
Operational analysis	Work-order metrics
Financial analysis	Billing, collections and receivables
Leadership updates	Executive summary generation
Error handling	Backend validation and exception handling
Hosted prototype	Render
Source code	GitHub repository
Decision Log	docs/DECISION_LOG.md
Docker support	Backend + frontend Dockerfiles
📄 Decision Log

The architecture and implementation decisions are documented in:

docs/DECISION_LOG.md

The Decision Log covers:

Architecture decisions
Technology choices
Key assumptions
Data normalization strategy
Data-quality handling
Read-only integration
AI approach
Error handling
Leadership-update interpretation
Trade-offs
Future improvements
🌱 Future Improvements

With additional development time, the following improvements could be added:

Analytics
Interactive time-series charts
Revenue forecasting
Pipeline conversion analysis
Deal aging analysis
Sector trend analysis
Historical pipeline movement
Data
Automated data-quality scoring
More sophisticated entity matching
Better duplicate detection
Historical snapshots of monday.com data
API response caching
Product
Authentication
Role-based access control
Saved founder queries
Custom executive dashboards
PDF export for leadership updates
Scheduled executive reports
Integrations
Slack executive summaries
Email leadership reports
Calendar integration
Additional business data sources
🎯 Design Principles

The application follows five core principles:

1. Live Data

Business insights should come from monday.com rather than hardcoded sample
data.

2. Read-Only Safety

The BI agent should analyze business information without modifying the source
system.

3. Transparent Uncertainty

Missing data should be surfaced instead of silently guessed.

4. Founder-Oriented Answers

Responses should focus on:

What happened?
Why does it matter?
What is the risk?
What should leadership do next?
5. Separation of Responsibilities

The system separates:

Data Retrieval
      ↓
Normalization
      ↓
Metrics
      ↓
Data Quality
      ↓
AI Interpretation
      ↓
Executive Response

This keeps deterministic business calculations separate from AI-generated
language.

👩‍💻 Author

Shreya Patil

Skylark Drones — Business Intelligence Agent

GitHub:

https://github.com/ShreyaVenkangouda/skylark-bi-agent