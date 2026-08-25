import pandas as pd

from fastapi import (
    FastAPI,
    HTTPException,
)

from fastapi.middleware.cors import (
    CORSMiddleware,
)


# ============================================================
# CONFIG
# ============================================================

from app.config import settings


# ============================================================
# MONDAY.COM
# ============================================================

from app.monday.repository import (
    MondayRepository,
)


# ============================================================
# DATA NORMALIZATION
# ============================================================

from app.data.normalizer import (
    monday_items_to_dataframe,
    rename_monday_columns,
    normalize_deals,
    normalize_work_orders,
)


from app.data.column_mapping import (
    DEALS_COLUMN_MAPPING,
    WORK_ORDER_COLUMN_MAPPING,
)


# ============================================================
# DATA QUALITY
# ============================================================

from app.data.quality import (
    calculate_quality,
)


# ============================================================
# BUSINESS METRICS
# ============================================================

from app.data.metrics import (
    pipeline_metrics,
    sector_metrics,
    operational_metrics,
    sector_operational_metrics,
    period_pipeline_metrics,
)


# ============================================================
# AI AGENT
# ============================================================

from app.agent.router import (
    route_question,
)


from app.agent.agent import (
    BusinessAgent,
)


# ============================================================
# SCHEMAS
# ============================================================

from app.schemas.models import (
    QuestionRequest,
    QuestionResponse,
)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Skylark Drones BI Agent",
    version="1.0.0",
    description=(
        "Business Intelligence Agent for "
        "Skylark Drones using monday.com data."
    ),
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)


# ============================================================
# SERVICES
# ============================================================

repository = MondayRepository()

agent = BusinessAgent()


# ============================================================
# LOAD DEALS BOARD
# ============================================================

def load_deals():

    board_data = repository.get_board_data(
        settings.DEALS_BOARD_ID
    )

    raw_df = monday_items_to_dataframe(
        board_data["items"]
    )

    deals_df = rename_monday_columns(
        raw_df,
        DEALS_COLUMN_MAPPING
    )

    deals_df = normalize_deals(
        deals_df
    )

    return (
        deals_df,
        board_data["board"],
    )


# ============================================================
# LOAD WORK ORDERS BOARD
# ============================================================

def load_work_orders():

    board_data = repository.get_board_data(
        settings.WORK_ORDERS_BOARD_ID
    )

    raw_df = monday_items_to_dataframe(
        board_data["items"]
    )

    work_orders_df = rename_monday_columns(
        raw_df,
        WORK_ORDER_COLUMN_MAPPING
    )

    work_orders_df = normalize_work_orders(
        work_orders_df
    )

    return (
        work_orders_df,
        board_data["board"],
    )


# ============================================================
# LOAD BOTH BOARDS
# ============================================================

def load_all_data():

    deals, deals_board = load_deals()

    work_orders, work_orders_board = (
        load_work_orders()
    )

    return (
        deals,
        work_orders,
        deals_board,
        work_orders_board,
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "application":
            "Skylark Drones BI Agent",

        "status":
            "running",

        "version":
            "1.0.0",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status":
            "healthy"
    }


# ============================================================
# BOARD INFORMATION
# ============================================================

@app.get("/boards")
def boards():

    try:

        (
            deals,
            work_orders,
            deals_board,
            work_orders_board,
        ) = load_all_data()

        return {

            "deals": {

                "id":
                    deals_board["id"],

                "name":
                    deals_board["name"],

                "rows":
                    len(deals),

                "columns":
                    deals_board[
                        "columns"
                    ],
            },

            "work_orders": {

                "id":
                    work_orders_board["id"],

                "name":
                    work_orders_board["name"],

                "rows":
                    len(work_orders),

                "columns":
                    work_orders_board[
                        "columns"
                    ],
            },
        }

    except Exception as exc:

        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# DATA SUMMARY
# ============================================================

@app.get("/data/summary")
def data_summary():

    try:

        (
            deals,
            work_orders,
            _,
            _,
        ) = load_all_data()

        return {

            # ------------------------------------------------
            # DATA QUALITY
            # ------------------------------------------------

            "data_quality": {

                "deals":
                    calculate_quality(
                        deals
                    ),

                "work_orders":
                    calculate_quality(
                        work_orders
                    ),
            },


            # ------------------------------------------------
            # OVERALL PIPELINE
            # ------------------------------------------------

            "pipeline":
                pipeline_metrics(
                    deals
                ),


            # ------------------------------------------------
            # ACTIVE PIPELINE BY SECTOR
            # ------------------------------------------------

            "pipeline_by_sector":
                sector_metrics(
                    deals
                ),


            # ------------------------------------------------
            # OPERATIONS
            # ------------------------------------------------

            "operations":
                operational_metrics(
                    work_orders
                ),


            # ------------------------------------------------
            # OPERATIONS BY SECTOR
            # ------------------------------------------------

            "operations_by_sector":
                sector_operational_metrics(
                    work_orders
                ),
        }

    except Exception as exc:

        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ============================================================
# ASK BUSINESS INTELLIGENCE AGENT
# ============================================================

@app.post(
    "/ask",
    response_model=QuestionResponse,
)
def ask(
    request: QuestionRequest,
):

    # ========================================================
    # GET QUESTION
    # ========================================================

    question = request.question.strip()


    # ========================================================
    # VALIDATE QUESTION
    # ========================================================

    if not question:

        raise HTTPException(
            status_code=400,
            detail=(
                "Question cannot be empty."
            ),
        )


    try:

        # ====================================================
        # LOAD DATA
        # ====================================================

        (
            deals,
            work_orders,
            _,
            _,
        ) = load_all_data()


        # ====================================================
        # UNDERSTAND QUESTION
        # ====================================================

        routing = route_question(
            question
        )


        # ====================================================
        # EXTRACT QUERY FILTERS
        # ====================================================

        sector = routing.get(
            "sector"
        )

        period = routing.get(
            "period",
            "all_time",
        )


        # ====================================================
        # BASE CONTEXT
        # ====================================================

        context = {

            "question":
                question,

            "query_routing":
                routing,

            "data_quality": {

                "deals":
                    calculate_quality(
                        deals
                    ),

                "work_orders":
                    calculate_quality(
                        work_orders
                    ),
            },
        }


        # ====================================================
        # DEALS / PIPELINE
        # ====================================================

        if routing.get(
            "deals",
            False,
        ):

            # -----------------------------------------------
            # Overall pipeline
            # -----------------------------------------------

            context[
                "pipeline_metrics"
            ] = pipeline_metrics(
                deals
            )


            # -----------------------------------------------
            # Active pipeline by sector
            # -----------------------------------------------

            context[
                "sector_metrics"
            ] = sector_metrics(
                deals
            )


            # -----------------------------------------------
            # Period + sector pipeline
            #
            # Example:
            #
            # "energy this quarter"
            #
            # -> Renewables
            # -> this_quarter
            # -----------------------------------------------

            context[
                "period_pipeline"
            ] = period_pipeline_metrics(
                deals,
                period=period,
                sector=sector,
            )


            # -----------------------------------------------
            # Raw deal records
            # -----------------------------------------------

            clean_deals = (
                deals
                .where(
                    pd.notna(
                        deals
                    ),
                    None,
                )
            )


            context[
                "deals"
            ] = clean_deals.to_dict(
                orient="records"
            )


        # ====================================================
        # WORK ORDERS / OPERATIONS
        # ====================================================

        if routing.get(
            "work_orders",
            False,
        ):

            # -----------------------------------------------
            # Overall operations
            # -----------------------------------------------

            context[
                "operational_metrics"
            ] = operational_metrics(
                work_orders
            )


            # -----------------------------------------------
            # Operations by sector
            # -----------------------------------------------

            context[
                "operational_by_sector"
            ] = (
                sector_operational_metrics(
                    work_orders
                )
            )


            # -----------------------------------------------
            # Raw work-order records
            # -----------------------------------------------

            clean_work_orders = (
                work_orders
                .where(
                    pd.notna(
                        work_orders
                    ),
                    None,
                )
            )


            context[
                "work_orders"
            ] = (
                clean_work_orders
                .to_dict(
                    orient="records"
                )
            )


        # ====================================================
        # LEADERSHIP QUESTIONS
        #
        # Leadership questions need both boards.
        # ====================================================

        if routing.get(
            "leadership",
            False,
        ):

            # -----------------------------------------------
            # Pipeline
            # -----------------------------------------------

            context[
                "pipeline_metrics"
            ] = pipeline_metrics(
                deals
            )


            context[
                "sector_metrics"
            ] = sector_metrics(
                deals
            )


            # -----------------------------------------------
            # Period pipeline
            # -----------------------------------------------

            context[
                "period_pipeline"
            ] = period_pipeline_metrics(
                deals,
                period=period,
                sector=sector,
            )


            # -----------------------------------------------
            # Operations
            # -----------------------------------------------

            context[
                "operational_metrics"
            ] = operational_metrics(
                work_orders
            )


            context[
                "operational_by_sector"
            ] = (
                sector_operational_metrics(
                    work_orders
                )
            )


        # ====================================================
        # GENERATE AI ANSWER
        # ====================================================

        answer = agent.answer(
            question,
            context,
        )


        # ====================================================
        # RETURN RESPONSE
        # ====================================================

        return {

            "answer":
                answer,

            "data_quality":
                context[
                    "data_quality"
                ],
        }


    except Exception as exc:

        import traceback

        traceback.print_exc()

        raise HTTPException(

            status_code=500,

            detail=(
                "Unable to process "
                f"question: {exc}"
            ),
        )