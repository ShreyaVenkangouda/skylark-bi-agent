# Skylark Drones — Business Intelligence Agent
## Decision Log

### 1. Architecture

The solution uses a React frontend with a FastAPI backend.

The React frontend provides:
- Executive overview dashboard
- Pipeline dashboard
- Operations dashboard
- Conversational BI interface

The FastAPI backend:
- Connects to monday.com using its API
- Retrieves Deals and Work Orders dynamically
- Normalizes inconsistent source data
- Calculates business metrics
- Performs data-quality analysis
- Routes natural-language questions to the BI agent

Architecture:

React Frontend
        ↓
FastAPI Backend
        ↓
BI Agent / Query Router
        ↓
Metrics + Data Quality
        ↓
Data Normalizer
        ↓
Monday.com API
        ↓
Deals + Work Orders Boards

The application is read-only and does not modify monday.com data.

---

### 2. Key Assumptions

- The Deals and Work Orders boards are the source of truth.
- "Energy" is interpreted as "Renewables" because the dataset uses Renewables as the corresponding sector.
- Active pipeline is defined as deals with status Open or On Hold.
- Won and Dead/Lost deals are excluded from active pipeline calculations.
- `close_date` is preferred for period-based analysis.
- When `close_date` is unavailable, `tentative_close` is used as the analytical fallback.
- Deals missing both dates cannot be reliably assigned to a reporting period.
- Missing probability values are handled conservatively and do not receive an invented probability.
- Missing monetary values are not fabricated or inferred.
- Source monetary values are masked values supplied by the assignment dataset.
- The application is strictly read-only.

---

### 3. Data Resilience

The source data contains significant missing and inconsistent values.

The backend therefore performs:

- Null and empty-value normalization
- Text normalization
- Sector normalization
- Status normalization
- Probability normalization
- Numeric and monetary parsing
- Date parsing
- Header/invalid-row filtering
- Data-quality reporting

The agent communicates important data-quality limitations alongside its answers rather than hiding them.

For example, the current dataset contains high levels of missing deal close dates and probabilities. These limitations are explicitly surfaced to executives because they affect forecasting reliability.

---

### 4. Business Metrics

Business metrics are calculated by the backend rather than being calculated by the language model.

This was an intentional design decision to reduce the risk of hallucinated numbers.

The backend calculates metrics including:

- Total deals
- Active deals
- Active pipeline
- Weighted pipeline
- Won value
- Dead/Lost value
- Pipeline by sector
- Work-order status
- Work orders by sector
- Billed value
- Collected value
- Receivables
- Amount remaining to be billed

The AI agent receives these calculated metrics as context and focuses on interpreting them for the user.

---

### 5. Period Analysis

For questions involving:

- This quarter
- Last quarter
- Next quarter
- This month
- Year to date

the backend performs the period filtering.

The date selection logic prioritizes:

`close_date`

and falls back to:

`tentative_close`

when the primary close date is unavailable.

This prevents the language model from independently guessing reporting periods.

If important records cannot be assigned to a period because both dates are missing, the agent communicates that limitation.

---

### 6. Trade-offs

#### Monday.com API vs MCP

The Monday.com API was selected instead of MCP.

The assignment only requires read-only retrieval of structured board data. The API provided a simpler and more deterministic integration within the six-hour implementation window.

#### Backend metric calculation vs LLM calculation

Metrics are calculated deterministically in Python and supplied to the AI agent.

This reduces numerical hallucination risk and makes business calculations easier to test.

#### React + FastAPI

React was selected for the frontend because it allows a responsive conversational dashboard while keeping the frontend independent from the backend.

FastAPI was selected because it provides lightweight API endpoints, simple deployment and clear separation between data retrieval, business logic and presentation.

---

### 7. Leadership Updates

The optional "leadership updates" requirement was interpreted as a concise executive briefing.

When requested, the agent produces:

1. Executive Summary
2. Key Metrics
3. Wins
4. Risks / Watch-outs
5. Recommended Actions

The leadership update combines pipeline, operational and financial information and explicitly includes relevant data-quality caveats.

This allows a founder or executive to use the agent for both ad-hoc business questions and preparation for leadership discussions.

---

### 8. Error Handling

The application handles:

- Monday.com API failures
- Empty datasets
- Missing values
- Invalid dates
- Invalid numeric values
- Missing business fields
- Backend connectivity failures

The frontend displays connection/error states rather than silently showing incorrect business information.

---

### 9. What I Would Improve With More Time

With additional development time, I would:

- Add automated unit and integration tests
- Add historical pipeline trend analysis
- Add richer deal-level drill-down
- Add configurable KPI definitions
- Add caching while maintaining data freshness
- Improve clarification handling for ambiguous questions
- Add authentication for the hosted application
- Add structured production monitoring and logging
- Add more advanced cross-board relationship analysis