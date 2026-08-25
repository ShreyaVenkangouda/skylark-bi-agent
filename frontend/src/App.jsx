import { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";

import {
  Activity,
  AlertTriangle,
  ArrowDownRight,
  ArrowUpRight,
  BriefcaseBusiness,
  CheckCircle2,
  Database,
  RefreshCw,
  Send,
  TrendingUp,
  IndianRupee,
  Bot,
  User,
  XCircle,
  Clock3,
} from "lucide-react";

import "./App.css";


// ============================================================
// CONFIG
// ============================================================

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";


// ============================================================
// HELPERS
// ============================================================

function formatMoney(value) {
  const number = Number(value || 0);

  if (!Number.isFinite(number)) {
    return "₹0";
  }

  const absolute = Math.abs(number);

  if (absolute >= 1000000000) {
    return `₹${(number / 1000000000).toFixed(2)}B`;
  }

  if (absolute >= 10000000) {
    return `₹${(number / 10000000).toFixed(2)}Cr`;
  }

  if (absolute >= 1000000) {
    return `₹${(number / 1000000).toFixed(2)}M`;
  }

  if (absolute >= 1000) {
    return `₹${(number / 1000).toFixed(1)}K`;
  }

  return `₹${number.toFixed(0)}`;
}


function formatNumber(value) {
  const number = Number(value || 0);

  if (!Number.isFinite(number)) {
    return "0";
  }

  return number.toLocaleString("en-IN");
}


function formatPercent(value) {
  const number = Number(value || 0);

  if (!Number.isFinite(number)) {
    return "0%";
  }

  return `${number.toFixed(1)}%`;
}


// ============================================================
// STAT CARD
// ============================================================

function StatCard({
  icon: Icon,
  label,
  value,
  subtitle,
  tone = "default",
}) {
  return (
    <div className="stat-card">

      <div className={`stat-icon ${tone}`}>
        <Icon size={21} />
      </div>

      <div className="stat-content">

        <div className="stat-label">
          {label}
        </div>

        <div className="stat-value">
          {value}
        </div>

        {subtitle && (
          <div className="stat-subtitle">
            {subtitle}
          </div>
        )}

      </div>

    </div>
  );
}


// ============================================================
// OVERVIEW PAGE
// ============================================================

function Overview({
  summary,
  onAsk,
  loading,
  question,
  setQuestion,
  messages,
  onRefresh,
  refreshing,
}) {
  const pipeline = summary?.pipeline || {};
  const operations = summary?.operations || {};

  const sectors =
    summary?.pipeline_by_sector || [];

  const quality =
    summary?.data_quality || {};

  const dealsQuality =
    quality?.deals || {};

  const workOrdersQuality =
    quality?.work_orders || {};

  const latestMessage =
    messages.length > 0
      ? messages[messages.length - 1]
      : null;

  return (
    <div className="page">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="page-header">

        <div>
          <h1>Founder Intelligence</h1>

          <p>
            Ask questions about your business data in plain English.
          </p>
        </div>

        <button
          className="refresh-button"
          onClick={onRefresh}
          disabled={refreshing}
        >
          <RefreshCw
            size={17}
            className={
              refreshing
                ? "spin"
                : ""
            }
          />

          {refreshing
            ? "Refreshing..."
            : "Refresh data"}
        </button>

      </div>


      {/* =====================================================
          TOP METRICS
      ===================================================== */}

      <div className="stats-grid">

        <StatCard
          icon={TrendingUp}
          label="Active Pipeline"
          value={formatMoney(
            pipeline.pipeline_value
          )}
          subtitle={`${formatNumber(
            pipeline.active_deals
          )} active deals`}
        />

        <StatCard
          icon={IndianRupee}
          label="Weighted Pipeline"
          value={formatMoney(
            pipeline.weighted_pipeline
          )}
          subtitle="Probability weighted"
        />

        <StatCard
          icon={BriefcaseBusiness}
          label="Work Orders"
          value={formatNumber(
            operations.total_work_orders
          )}
          subtitle="Across all sectors"
        />

        <StatCard
          icon={IndianRupee}
          label="Receivables"
          value={formatMoney(
            operations.total_receivable
          )}
          subtitle="Outstanding"
          tone="warning"
        />

      </div>


      {/* =====================================================
          MAIN GRID
      ===================================================== */}

      <div className="overview-grid">

        {/* =================================================
            AI AGENT
        ================================================= */}

        <div className="panel agent-panel">

          <div className="panel-header">

            <div>

              <h2>
                Ask the BI Agent
              </h2>

              <p>
                Powered by live monday.com data
              </p>

            </div>

            <div className="online-status">

              <span className="online-dot" />

              Online

            </div>

          </div>


          <div className="chat-container">

            <div className="chat-messages">

              {messages.length === 0 && (
                <div className="welcome-message">

                  <div className="message-avatar bot">
                    <Bot size={17} />
                  </div>

                  <div className="message-bubble bot-bubble">

                    Hi! I'm your Skylark Drones BI Agent.

                    <br />

                    Ask me about pipeline, sectors,
                    work orders, billing, collections,
                    or leadership updates.

                  </div>

                </div>
              )}


              {messages.map(
                (message, index) => (

                  <div
                    className={`message-row ${message.role === "user"
                        ? "user-row"
                        : "bot-row"
                      }`}
                    key={index}
                  >

                    {message.role !== "user" && (
                      <div className="message-avatar bot">
                        <Bot size={16} />
                      </div>
                    )}

                    <div
                      className={`message-bubble ${message.role === "user"
                          ? "user-bubble"
                          : "bot-bubble"
                        }`}
                    >

                      {message.role === "user" ? (

                        message.content

                      ) : (

                        <div className="markdown-content">

                          <ReactMarkdown>
                            {message.content}
                          </ReactMarkdown>

                        </div>

                      )}

                    </div>

                    {message.role === "user" && (
                      <div className="message-avatar user">
                        <User size={16} />
                      </div>
                    )}

                  </div>

                )
              )}


              {loading && (
                <div className="message-row bot-row">

                  <div className="message-avatar bot">
                    <Bot size={16} />
                  </div>

                  <div className="message-bubble bot-bubble">

                    <div className="typing">

                      <span />
                      <span />
                      <span />

                    </div>

                  </div>

                </div>
              )}

            </div>


            {/* QUICK QUESTIONS */}

            <div className="quick-questions">

              <button
                onClick={() =>
                  onAsk(
                    "How's our pipeline looking for energy sector this quarter?"
                  )
                }
              >
                Pipeline this quarter
              </button>

              <button
                onClick={() =>
                  onAsk(
                    "Which sectors have the strongest active pipeline?"
                  )
                }
              >
                Strongest sectors
              </button>

              <button
                onClick={() =>
                  onAsk(
                    "How much is currently receivable?"
                  )
                }
              >
                Receivables
              </button>

              <button
                onClick={() =>
                  onAsk(
                    "Give me a leadership update."
                  )
                }
              >
                Leadership update
              </button>

            </div>


            {/* INPUT */}

            <form
              className="chat-input-container"
              onSubmit={(event) => {
                event.preventDefault();

                if (
                  question.trim() &&
                  !loading
                ) {
                  onAsk(question);
                }
              }}
            >

              <input
                type="text"
                value={question}
                onChange={(event) =>
                  setQuestion(
                    event.target.value
                  )
                }
                placeholder="Ask a business question..."
                disabled={loading}
              />

              <button
                type="submit"
                disabled={
                  loading ||
                  !question.trim()
                }
              >

                <Send size={18} />

              </button>

            </form>

          </div>

        </div>


        {/* =================================================
            SECTOR PIPELINE
        ================================================= */}

        <div className="right-column">

          <div className="panel">

            <div className="panel-header">

              <div>

                <h2>
                  Active Pipeline
                </h2>

                <p>
                  By sector
                </p>

              </div>

            </div>

            <SectorPipeline
              sectors={sectors}
            />

          </div>


          <DataQuality
            deals={dealsQuality}
            workOrders={workOrdersQuality}
          />

        </div>

      </div>

    </div>
  );
}


// ============================================================
// SECTOR PIPELINE
// ============================================================

function SectorPipeline({
  sectors,
}) {
  if (!sectors.length) {
    return (
      <div className="empty-state">
        No pipeline data available.
      </div>
    );
  }

  const maxValue = Math.max(
    ...sectors.map(
      (item) =>
        Number(item.value || 0)
    ),
    1
  );

  return (
    <div className="sector-list">

      {sectors.map((sector) => {

        const value =
          Number(sector.value || 0);

        const width =
          Math.max(
            2,
            (value / maxValue) * 100
          );

        return (
          <div
            className="sector-item"
            key={sector.sector}
          >

            <div className="sector-top">

              <span>
                {sector.sector}
              </span>

              <strong>
                {formatMoney(value)}
              </strong>

            </div>

            <div className="progress-track">

              <div
                className="progress-fill"
                style={{
                  width: `${width}%`,
                }}
              />

            </div>

            <small>
              {formatNumber(
                sector.deals
              )} active deals
            </small>

          </div>
        );
      })}

    </div>
  );
}


// ============================================================
// DATA QUALITY
// ============================================================

function DataQuality({
  deals,
  workOrders,
}) {
  return (
    <div className="panel">

      <div className="panel-header">

        <div>

          <h2>
            Data Quality
          </h2>

          <p>
            Current source health
          </p>

        </div>

        <Database size={20} />

      </div>


      <div className="quality-score">

        <strong>
          {formatPercent(
            deals.missing_percentage
          )}
        </strong>

        <span>
          deal data missing
        </span>

      </div>


      <div className="quality-list">

        <div className="quality-row">

          <span>
            Close dates missing
          </span>

          <strong>
            {findMissingPercentage(
              deals,
              "close_date"
            )}
          </strong>

        </div>

        <div className="quality-row">

          <span>
            Probabilities missing
          </span>

          <strong>
            {findMissingPercentage(
              deals,
              "probability"
            )}
          </strong>

        </div>

        <div className="quality-row">

          <span>
            Deal values missing
          </span>

          <strong>
            {findMissingPercentage(
              deals,
              "deal_value"
            )}
          </strong>

        </div>

        <div className="quality-row">

          <span>
            Work order data missing
          </span>

          <strong>
            {formatPercent(
              workOrders.missing_percentage
            )}
          </strong>

        </div>

      </div>

    </div>
  );
}


function findMissingPercentage(
  quality,
  field
) {
  const issues =
    quality?.issues || [];

  const issue =
    issues.find(
      (item) =>
        item.startsWith(`${field}:`)
    );

  if (!issue) {
    return "—";
  }

  const match =
    issue.match(
      /\(([\d.]+)%\)/
    );

  return match
    ? `${match[1]}%`
    : "—";
}


// ============================================================
// PIPELINE PAGE
// ============================================================

function PipelinePage({
  summary,
}) {
  const pipeline =
    summary?.pipeline || {};

  const sectors =
    summary?.pipeline_by_sector || [];

  return (
    <div className="page">

      <PageHeader
        title="Pipeline"
        subtitle="Sales pipeline and sector performance from live monday.com data."
      />


      <div className="stats-grid">

        <StatCard
          icon={Database}
          label="Total Deals"
          value={formatNumber(
            pipeline.total_deals
          )}
          subtitle="All deal records"
        />

        <StatCard
          icon={TrendingUp}
          label="Active Deals"
          value={formatNumber(
            pipeline.active_deals
          )}
          subtitle="Open + On Hold"
        />

        <StatCard
          icon={IndianRupee}
          label="Active Pipeline"
          value={formatMoney(
            pipeline.pipeline_value
          )}
          subtitle="Unweighted"
        />

        <StatCard
          icon={IndianRupee}
          label="Weighted Pipeline"
          value={formatMoney(
            pipeline.weighted_pipeline
          )}
          subtitle="Probability weighted"
        />

      </div>


      <div className="content-grid">

        <div className="panel">

          <div className="panel-header">

            <div>

              <h2>
                Pipeline by Sector
              </h2>

              <p>
                Active opportunities by sector
              </p>

            </div>

          </div>

          <SectorPipeline
            sectors={sectors}
          />

        </div>


        <div className="panel">

          <div className="panel-header">

            <div>

              <h2>
                Pipeline Outcome
              </h2>

              <p>
                Historical deal values
              </p>

            </div>

          </div>

          <div className="outcome-grid">

            <MetricBox
              icon={CheckCircle2}
              label="Won Value"
              value={formatMoney(
                pipeline.won_value
              )}
            />

            <MetricBox
              icon={XCircle}
              label="Dead / Lost Value"
              value={formatMoney(
                pipeline.dead_value
              )}
            />

          </div>

        </div>

      </div>


      <div className="panel">

        <div className="panel-header">

          <div>

            <h2>
              Sector Breakdown
            </h2>

            <p>
              Deal count and pipeline value
            </p>

          </div>

        </div>

        <div className="table-wrapper">

          <table>

            <thead>

              <tr>

                <th>
                  Sector
                </th>

                <th>
                  Active Deals
                </th>

                <th>
                  Pipeline Value
                </th>

              </tr>

            </thead>

            <tbody>

              {sectors.map(
                (sector) => (

                  <tr
                    key={
                      sector.sector
                    }
                  >

                    <td>
                      <strong>
                        {sector.sector}
                      </strong>
                    </td>

                    <td>
                      {formatNumber(
                        sector.deals
                      )}
                    </td>

                    <td>
                      {formatMoney(
                        sector.value
                      )}
                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}


// ============================================================
// OPERATIONS PAGE
// ============================================================

function OperationsPage({
  summary,
}) {
  const operations =
    summary?.operations || {};

  const statuses =
    operations.status_breakdown || {};

  const sectors =
    summary?.operations_by_sector || [];

  return (
    <div className="page">

      <PageHeader
        title="Operations"
        subtitle="Work orders, billing, collections and receivables."
      />


      <div className="stats-grid">

        <StatCard
          icon={BriefcaseBusiness}
          label="Work Orders"
          value={formatNumber(
            operations.total_work_orders
          )}
          subtitle="All work orders"
        />

        <StatCard
          icon={IndianRupee}
          label="Total Billed"
          value={formatMoney(
            operations.total_billed
          )}
          subtitle="Excluding? As supplied"
        />

        <StatCard
          icon={IndianRupee}
          label="Total Collected"
          value={formatMoney(
            operations.total_collected
          )}
          subtitle="Collected amount"
        />

        <StatCard
          icon={IndianRupee}
          label="Receivables"
          value={formatMoney(
            operations.total_receivable
          )}
          subtitle="Outstanding"
          tone="warning"
        />

      </div>


      <div className="content-grid">

        {/* STATUS */}

        <div className="panel">

          <div className="panel-header">

            <div>

              <h2>
                Work Order Status
              </h2>

              <p>
                Current execution status
              </p>

            </div>

          </div>

          <div className="status-list">

            {Object.entries(
              statuses
            ).map(
              ([status, count]) => (

                <div
                  className="status-row"
                  key={status}
                >

                  <div className="status-name">

                    <span className="status-dot" />

                    {status}

                  </div>

                  <strong>
                    {formatNumber(
                      count
                    )}
                  </strong>

                </div>

              )
            )}

          </div>

        </div>


        {/* SECTORS */}

        <div className="panel">

          <div className="panel-header">

            <div>

              <h2>
                Work Orders by Sector
              </h2>

              <p>
                Operational footprint
              </p>

            </div>

          </div>

          <div className="sector-list">

            {sectors.map(
              (sector) => (

                <div
                  className="sector-item"
                  key={
                    sector.sector
                  }
                >

                  <div className="sector-top">

                    <span>
                      {sector.sector}
                    </span>

                    <strong>
                      {formatNumber(
                        sector.work_orders
                      )}
                    </strong>

                  </div>

                  <div className="progress-track">

                    <div
                      className="progress-fill"
                      style={{
                        width: `${Math.max(
                          2,
                          (Number(
                            sector.work_orders ||
                            0
                          ) /
                            Math.max(
                              ...sectors.map(
                                (item) =>
                                  Number(
                                    item.work_orders ||
                                    0
                                  )
                              ),
                              1
                            )) *
                          100
                        )}%`,
                      }}
                    />

                  </div>

                </div>

              )
            )}

          </div>

        </div>

      </div>


      {/* BILLING */}

      <div className="panel">

        <div className="panel-header">

          <div>

            <h2>
              Billing & Collections
            </h2>

            <p>
              Financial operational metrics
            </p>

          </div>

        </div>

        <div className="financial-grid">

          <MetricBox
            icon={ArrowUpRight}
            label="To Be Billed"
            value={formatMoney(
              operations.total_to_be_billed
            )}
          />

          <MetricBox
            icon={IndianRupee}
            label="Billed"
            value={formatMoney(
              operations.total_billed
            )}
          />

          <MetricBox
            icon={CheckCircle2}
            label="Collected"
            value={formatMoney(
              operations.total_collected
            )}
          />

          <MetricBox
            icon={ArrowDownRight}
            label="Receivable"
            value={formatMoney(
              operations.total_receivable
            )}
          />

        </div>

      </div>


      {/* COLLECTION RATIO */}

      <div className="panel">

        <div className="panel-header">

          <div>

            <h2>
              Collection Health
            </h2>

            <p>
              Collected vs billed
            </p>

          </div>

        </div>

        <CollectionHealth
          billed={
            operations.total_billed
          }
          collected={
            operations.total_collected
          }
        />

      </div>

    </div>
  );
}


// ============================================================
// COLLECTION HEALTH
// ============================================================

function CollectionHealth({
  billed,
  collected,
}) {
  const billedNumber =
    Number(billed || 0);

  const collectedNumber =
    Number(collected || 0);

  const percentage =
    billedNumber > 0
      ? Math.min(
        100,
        (collectedNumber /
          billedNumber) *
        100
      )
      : 0;

  return (
    <div>

      <div className="collection-header">

        <div>

          <strong>
            {percentage.toFixed(1)}%
          </strong>

          <span>
            collected against billed value
          </span>

        </div>

        <span>
          {formatMoney(
            collectedNumber
          )} / {formatMoney(
            billedNumber
          )}
        </span>

      </div>

      <div className="large-progress">

        <div
          className="large-progress-fill"
          style={{
            width: `${percentage}%`,
          }}
        />

      </div>

    </div>
  );
}


// ============================================================
// METRIC BOX
// ============================================================

function MetricBox({
  icon: Icon,
  label,
  value,
}) {
  return (
    <div className="metric-box">

      <div className="metric-icon">
        <Icon size={18} />
      </div>

      <div>

        <span>
          {label}
        </span>

        <strong>
          {value}
        </strong>

      </div>

    </div>
  );
}


// ============================================================
// PAGE HEADER
// ============================================================

function PageHeader({
  title,
  subtitle,
}) {
  return (
    <div className="page-header">

      <div>

        <h1>
          {title}
        </h1>

        <p>
          {subtitle}
        </p>

      </div>

    </div>
  );
}


// ============================================================
// MAIN APP
// ============================================================

export default function App() {

  const [
    activePage,
    setActivePage,
  ] = useState("overview");


  const [
    summary,
    setSummary,
  ] = useState(null);


  const [
    loadingSummary,
    setLoadingSummary,
  ] = useState(true);


  const [
    refreshing,
    setRefreshing,
  ] = useState(false);


  const [
    question,
    setQuestion,
  ] = useState("");


  const [
    loadingAnswer,
    setLoadingAnswer,
  ] = useState(false);


  const [
    messages,
    setMessages,
  ] = useState([]);


  const [
    backendError,
    setBackendError,
  ] = useState(null);


  // ========================================================
  // LOAD SUMMARY
  // ========================================================

  async function loadSummary(
    isRefresh = false
  ) {

    if (isRefresh) {
      setRefreshing(true);
    } else {
      setLoadingSummary(true);
    }

    setBackendError(null);

    try {

      const response =
        await fetch(
          `${API_URL}/data/summary`
        );

      if (!response.ok) {
        throw new Error(
          `Backend returned ${response.status}`
        );
      }

      const data =
        await response.json();

      setSummary(data);

    } catch (error) {

      console.error(
        "Summary error:",
        error
      );

      setBackendError(
        "Could not connect to the BI backend."
      );

    } finally {

      setLoadingSummary(false);
      setRefreshing(false);

    }
  }


  // ========================================================
  // ASK AGENT
  // ========================================================

  async function askAgent(
    userQuestion
  ) {

    const trimmed =
      String(
        userQuestion || ""
      ).trim();

    if (!trimmed) {
      return;
    }

    setMessages(
      (previous) => [
        ...previous,
        {
          role: "user",
          content: trimmed,
        },
      ]
    );

    setQuestion("");
    setLoadingAnswer(true);


    try {

      const response =
        await fetch(
          `${API_URL}/ask`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              question: trimmed,
            }),
          }
        );


      if (!response.ok) {

        throw new Error(
          `Agent returned ${response.status}`
        );

      }


      const data =
        await response.json();


      const answer =
        data.answer ||
        data.response ||
        "I couldn't generate an answer.";


      setMessages(
        (previous) => [
          ...previous,
          {
            role: "assistant",
            content: answer,
          },
        ]
      );


    } catch (error) {

      console.error(
        "Ask error:",
        error
      );


      setMessages(
        (previous) => [
          ...previous,
          {
            role: "assistant",
            content:
              "I’m unable to retrieve the latest business data right now. Please check that the BI backend is running and try again.",
          },
        ]
      );

    } finally {

      setLoadingAnswer(false);

    }
  }


  // ========================================================
  // INITIAL LOAD
  // ========================================================

  useEffect(() => {

    loadSummary();

  }, []);


  // ========================================================
  // PAGE CONTENT
  // ========================================================

  const pageContent =
    useMemo(() => {

      if (
        loadingSummary &&
        !summary
      ) {

        return (
          <div className="loading-page">

            <RefreshCw
              size={25}
              className="spin"
            />

            <p>
              Loading live monday.com data...
            </p>

          </div>
        );

      }


      if (
        activePage === "pipeline"
      ) {

        return (
          <PipelinePage
            summary={summary}
          />
        );

      }


      if (
        activePage === "operations"
      ) {

        return (
          <OperationsPage
            summary={summary}
          />
        );

      }


      return (
        <Overview
          summary={summary}
          onAsk={askAgent}
          loading={loadingAnswer}
          question={question}
          setQuestion={setQuestion}
          messages={messages}
          onRefresh={() =>
            loadSummary(true)
          }
          refreshing={refreshing}
        />
      );

    }, [
      activePage,
      summary,
      loadingSummary,
      loadingAnswer,
      question,
      messages,
      refreshing,
    ]);


  // ========================================================
  // RENDER
  // ========================================================

  return (

    <div className="app-shell">


      {/* ====================================================
          SIDEBAR
      ==================================================== */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-logo">
            S
          </div>

          <div>

            <div className="brand-name">
              Skylark
            </div>

            <div className="brand-subtitle">
              Business Intelligence
            </div>

          </div>

        </div>


        <div className="sidebar-section-title">
          WORKSPACE
        </div>


        <nav className="sidebar-nav">

          <button
            className={`nav-item ${activePage === "overview"
                ? "active"
                : ""
              }`}
            onClick={() =>
              setActivePage("overview")
            }
          >

            <Activity size={18} />

            <span>
              Overview
            </span>

          </button>


          <button
            className={`nav-item ${activePage === "pipeline"
                ? "active"
                : ""
              }`}
            onClick={() =>
              setActivePage("pipeline")
            }
          >

            <TrendingUp size={18} />

            <span>
              Pipeline
            </span>

          </button>


          <button
            className={`nav-item ${activePage === "operations"
                ? "active"
                : ""
              }`}
            onClick={() =>
              setActivePage("operations")
            }
          >

            <BriefcaseBusiness size={18} />

            <span>
              Operations
            </span>

          </button>

        </nav>


        <div className="sidebar-footer">

          <div className="sidebar-status">

            <span className="online-dot" />

            <span>
              Monday.com connected
            </span>

          </div>

          <small>
            Read-only business intelligence
          </small>

        </div>

      </aside>


      {/* ====================================================
          MAIN
      ==================================================== */}

      <main className="main-content">

        {backendError && (

          <div className="error-banner">

            <AlertTriangle size={18} />

            <span>
              {backendError}
            </span>

            <button
              onClick={() =>
                loadSummary(true)
              }
            >
              Retry
            </button>

          </div>

        )}

        {pageContent}

      </main>

    </div>

  );
}