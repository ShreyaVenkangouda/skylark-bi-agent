import pandas as pd


# ============================================================
# HELPER
# ============================================================

def numeric_column(
    df,
    column
):
    """
    Safely convert a dataframe column to numeric.

    Missing or invalid values become 0.
    """

    if column not in df.columns:

        return pd.Series(
            0,
            index=df.index,
            dtype=float
        )

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)


# ============================================================
# PIPELINE METRICS
# ============================================================

def pipeline_metrics(
    deals
):
    """
    Calculate overall sales pipeline metrics.

    Active pipeline =
        Open + On Hold deals
    """

    if deals.empty:

        return {
            "total_deals": 0,
            "active_deals": 0,
            "pipeline_value": 0,
            "weighted_pipeline": 0,
            "won_value": 0,
            "dead_value": 0,
        }


    temp = deals.copy()


    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    if "deal_value" not in temp.columns:

        temp["deal_value"] = 0


    if "probability" not in temp.columns:

        temp["probability"] = 0


    if "status" not in temp.columns:

        temp["status"] = None


    # --------------------------------------------------------
    # Numeric deal value
    # --------------------------------------------------------

    temp["numeric_value"] = numeric_column(
        temp,
        "deal_value"
    )


    # --------------------------------------------------------
    # Probability
    #
    # normalize_probability() should already have converted:
    #
    # High   -> 0.80
    # Medium -> 0.50
    # Low    -> 0.20
    # --------------------------------------------------------

    temp["numeric_probability"] = pd.to_numeric(
        temp["probability"],
        errors="coerce"
    ).fillna(0)


    # --------------------------------------------------------
    # Active deals
    # --------------------------------------------------------

    active = temp[
        temp["status"].isin([
            "Open",
            "On Hold"
        ])
    ].copy()


    # --------------------------------------------------------
    # Pipeline value
    # --------------------------------------------------------

    pipeline_value = (
        active["numeric_value"]
        .sum()
    )


    # --------------------------------------------------------
    # Weighted pipeline
    # --------------------------------------------------------

    weighted_pipeline = (
        active["numeric_value"]
        *
        active["numeric_probability"]
    ).sum()


    # --------------------------------------------------------
    # Won
    # --------------------------------------------------------

    won_value = (
        temp.loc[
            temp["status"] == "Won",
            "numeric_value"
        ].sum()
    )


    # --------------------------------------------------------
    # Dead / Lost
    # --------------------------------------------------------

    dead_value = (
        temp.loc[
            temp["status"] == "Dead",
            "numeric_value"
        ].sum()
    )


    return {

        "total_deals":
            int(len(temp)),

        "active_deals":
            int(len(active)),

        "pipeline_value":
            float(pipeline_value),

        "weighted_pipeline":
            float(weighted_pipeline),

        "won_value":
            float(won_value),

        "dead_value":
            float(dead_value),
    }


# ============================================================
# PIPELINE BY SECTOR
# ============================================================

def sector_metrics(
    deals
):
    """
    Calculate ACTIVE pipeline by sector.

    Only Open and On Hold deals are included.
    """

    if deals.empty:

        return []


    temp = deals.copy()


    # --------------------------------------------------------
    # Make sure required columns exist
    # --------------------------------------------------------

    if "status" not in temp.columns:

        return []


    if "sector" not in temp.columns:

        return []


    if "deal_value" not in temp.columns:

        temp["deal_value"] = 0


    # --------------------------------------------------------
    # Only active pipeline
    # --------------------------------------------------------

    temp = temp[
        temp["status"].isin([
            "Open",
            "On Hold"
        ])
    ].copy()


    if temp.empty:

        return []


    # --------------------------------------------------------
    # Numeric deal value
    # --------------------------------------------------------

    temp["numeric_value"] = numeric_column(
        temp,
        "deal_value"
    )


    # --------------------------------------------------------
    # Missing sectors
    # --------------------------------------------------------

    temp["sector"] = (
        temp["sector"]
        .fillna("Unknown")
    )


    temp["sector"] = (
        temp["sector"]
        .replace(
            "",
            "Unknown"
        )
    )


    # --------------------------------------------------------
    # Group
    # --------------------------------------------------------

    grouped = (
        temp
        .groupby("sector")
        .agg(
            deals=(
                "monday_item_id",
                "count"
            ),

            value=(
                "numeric_value",
                "sum"
            )
        )
        .reset_index()
    )


    # --------------------------------------------------------
    # Sort highest pipeline first
    # --------------------------------------------------------

    grouped = grouped.sort_values(
        "value",
        ascending=False
    )


    # --------------------------------------------------------
    # Convert numpy values to Python values
    # --------------------------------------------------------

    grouped["deals"] = (
        grouped["deals"]
        .astype(int)
    )

    grouped["value"] = (
        grouped["value"]
        .astype(float)
    )


    return grouped.to_dict(
        orient="records"
    )


# ============================================================
# OPERATIONAL METRICS
# ============================================================

def operational_metrics(
    work_orders
):
    """
    Calculate operational and billing metrics
    from the Work Orders board.
    """

    if work_orders.empty:

        return {
            "total_work_orders": 0,
            "status_breakdown": {},
            "total_receivable": 0,
            "total_to_be_billed": 0,
        }


    temp = work_orders.copy()


    result = {

        "total_work_orders":
            int(len(temp))
    }


    # --------------------------------------------------------
    # Execution status
    # --------------------------------------------------------

    if "execution_status" in temp.columns:

        status_series = (
            temp["execution_status"]
            .fillna("Unknown")
            .replace(
                "",
                "Unknown"
            )
        )

        result[
            "status_breakdown"
        ] = (
            status_series
            .value_counts()
            .to_dict()
        )

    else:

        result[
            "status_breakdown"
        ] = {}


    # --------------------------------------------------------
    # Receivable
    # --------------------------------------------------------

    if "receivable" in temp.columns:

        result[
            "total_receivable"
        ] = float(
            numeric_column(
                temp,
                "receivable"
            ).sum()
        )

    else:

        result[
            "total_receivable"
        ] = 0


    # --------------------------------------------------------
    # Amount to be billed
    # --------------------------------------------------------

    if "to_be_billed_inc_gst" in temp.columns:

        result[
            "total_to_be_billed"
        ] = float(
            numeric_column(
                temp,
                "to_be_billed_inc_gst"
            ).sum()
        )

    else:

        result[
            "total_to_be_billed"
        ] = 0


    # --------------------------------------------------------
    # Billed value
    # --------------------------------------------------------

    if "billed_inc_gst" in temp.columns:

        result[
            "total_billed"
        ] = float(
            numeric_column(
                temp,
                "billed_inc_gst"
            ).sum()
        )

    else:

        result[
            "total_billed"
        ] = 0


    # --------------------------------------------------------
    # Collected amount
    # --------------------------------------------------------

    if "collected_inc_gst" in temp.columns:

        result[
            "total_collected"
        ] = float(
            numeric_column(
                temp,
                "collected_inc_gst"
            ).sum()
        )

    else:

        result[
            "total_collected"
        ] = 0


    return result


# ============================================================
# OPERATIONS BY SECTOR
# ============================================================

def sector_operational_metrics(
    work_orders
):
    """
    Number of work orders by sector.
    """

    if work_orders.empty:

        return []


    if "sector" not in work_orders.columns:

        return []


    temp = work_orders.copy()


    temp["sector"] = (
        temp["sector"]
        .fillna("Unknown")
    )


    temp["sector"] = (
        temp["sector"]
        .replace(
            "",
            "Unknown"
        )
    )


    grouped = (
        temp
        .groupby("sector")
        .size()
        .reset_index(
            name="work_orders"
        )
    )


    grouped = grouped.sort_values(
        "work_orders",
        ascending=False
    )


    grouped["work_orders"] = (
        grouped["work_orders"]
        .astype(int)
    )


    return grouped.to_dict(
        orient="records"
    )


# ============================================================
# BILLING METRICS BY SECTOR
# ============================================================

def billing_by_sector(
    work_orders
):
    """
    Calculate billing and receivable metrics by sector.
    """

    if work_orders.empty:

        return []


    if "sector" not in work_orders.columns:

        return []


    temp = work_orders.copy()


    temp["sector"] = (
        temp["sector"]
        .fillna("Unknown")
    )


    # --------------------------------------------------------
    # Ensure numeric columns
    # --------------------------------------------------------

    temp["receivable_numeric"] = (
        numeric_column(
            temp,
            "receivable"
        )
    )


    temp["billed_numeric"] = (
        numeric_column(
            temp,
            "billed_inc_gst"
        )
    )


    temp["collected_numeric"] = (
        numeric_column(
            temp,
            "collected_inc_gst"
        )
    )


    temp["to_be_billed_numeric"] = (
        numeric_column(
            temp,
            "to_be_billed_inc_gst"
        )
    )


    # --------------------------------------------------------
    # Group
    # --------------------------------------------------------

    grouped = (
        temp
        .groupby("sector")
        .agg(

            work_orders=(
                "sector",
                "size"
            ),

            receivable=(
                "receivable_numeric",
                "sum"
            ),

            billed=(
                "billed_numeric",
                "sum"
            ),

            collected=(
                "collected_numeric",
                "sum"
            ),

            to_be_billed=(
                "to_be_billed_numeric",
                "sum"
            ),
        )
        .reset_index()
    )


    grouped = grouped.sort_values(
        "receivable",
        ascending=False
    )


    return grouped.to_dict(
        orient="records"
    )


# ============================================================
# PIPELINE STATUS BREAKDOWN
# ============================================================

def pipeline_status_metrics(
    deals
):
    """
    Count and value deals by status.
    """

    if deals.empty:

        return []


    if "status" not in deals.columns:

        return []


    temp = deals.copy()


    if "deal_value" not in temp.columns:

        temp["deal_value"] = 0


    temp["numeric_value"] = numeric_column(
        temp,
        "deal_value"
    )


    temp["status"] = (
        temp["status"]
        .fillna("Unknown")
    )


    grouped = (
        temp
        .groupby("status")
        .agg(

            deals=(
                "status",
                "size"
            ),

            value=(
                "numeric_value",
                "sum"
            ),
        )
        .reset_index()
    )


    grouped = grouped.sort_values(
        "value",
        ascending=False
    )


    return grouped.to_dict(
        orient="records"
    )
# ============================================================
# PERIOD HELPERS
# ============================================================

def get_quarter_dates(
    reference_date=None
):
    """
    Return start and end dates for the quarter
    containing reference_date.
    """

    if reference_date is None:

        reference_date = pd.Timestamp.now()

    reference_date = pd.Timestamp(
        reference_date
    )

    quarter = (
        (reference_date.month - 1)
        // 3
    )

    start_month = (
        quarter * 3
    ) + 1

    start_date = pd.Timestamp(
        year=reference_date.year,
        month=start_month,
        day=1,
    )

    end_date = (
        start_date
        + pd.DateOffset(
            months=3
        )
        - pd.Timedelta(
            days=1
        )
    )

    return (
        start_date,
        end_date
    )


def get_period_dates(
    period,
    reference_date=None
):
    """
    Convert a period name into
    start/end dates.
    """

    if reference_date is None:

        reference_date = pd.Timestamp.now()

    reference_date = pd.Timestamp(
        reference_date
    )


    # --------------------------------------------------------
    # This quarter
    # --------------------------------------------------------

    if period == "this_quarter":

        return get_quarter_dates(
            reference_date
        )


    # --------------------------------------------------------
    # Last quarter
    # --------------------------------------------------------

    if period == "last_quarter":

        current_start, _ = (
            get_quarter_dates(
                reference_date
            )
        )

        last_day_previous_quarter = (
            current_start
            - pd.Timedelta(
                days=1
            )
        )

        return get_quarter_dates(
            last_day_previous_quarter
        )


    # --------------------------------------------------------
    # Next quarter
    # --------------------------------------------------------

    if period == "next_quarter":

        current_start, _ = (
            get_quarter_dates(
                reference_date
            )
        )

        next_quarter_date = (
            current_start
            + pd.DateOffset(
                months=3
            )
        )

        return get_quarter_dates(
            next_quarter_date
        )


    # --------------------------------------------------------
    # This month
    # --------------------------------------------------------

    if period == "this_month":

        start_date = pd.Timestamp(
            year=reference_date.year,
            month=reference_date.month,
            day=1,
        )

        end_date = (
            start_date
            + pd.offsets.MonthEnd(1)
        )

        return (
            start_date,
            end_date
        )


    # --------------------------------------------------------
    # Last month
    # --------------------------------------------------------

    if period == "last_month":

        first_of_current_month = (
            pd.Timestamp(
                year=reference_date.year,
                month=reference_date.month,
                day=1,
            )
        )

        last_month_date = (
            first_of_current_month
            - pd.Timedelta(
                days=1
            )
        )

        start_date = pd.Timestamp(
            year=last_month_date.year,
            month=last_month_date.month,
            day=1,
        )

        end_date = (
            start_date
            + pd.offsets.MonthEnd(1)
        )

        return (
            start_date,
            end_date
        )


    # --------------------------------------------------------
    # Next month
    # --------------------------------------------------------

    if period == "next_month":

        start_date = (
            pd.Timestamp(
                year=reference_date.year,
                month=reference_date.month,
                day=1,
            )
            + pd.DateOffset(
                months=1
            )
        )

        end_date = (
            start_date
            + pd.offsets.MonthEnd(1)
        )

        return (
            start_date,
            end_date
        )


    # --------------------------------------------------------
    # Year to date
    # --------------------------------------------------------

    if period == "ytd":

        start_date = pd.Timestamp(
            year=reference_date.year,
            month=1,
            day=1,
        )

        end_date = reference_date

        return (
            start_date,
            end_date
        )


    # --------------------------------------------------------
    # All time
    # --------------------------------------------------------

    return (
        None,
        None
    )


# ============================================================
# PERIOD-AWARE PIPELINE
# ============================================================

def period_pipeline_metrics(
    deals,
    period="all_time",
    sector=None,
    reference_date=None,
):
    """
    Calculate pipeline for a specific
    time period and optionally sector.

    Uses:

    1. close_date when available
    2. tentative_close as fallback

    This is important because the source data
    contains many missing close dates.
    """

    if deals.empty:

        return {
            "period": period,
            "sector": sector,
            "start_date": None,
            "end_date": None,
            "total_matching_deals": 0,
            "active_deals": 0,
            "pipeline_value": 0,
            "weighted_pipeline": 0,
            "date_quality": {},
        }


    temp = deals.copy()


    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    if "status" not in temp.columns:

        temp["status"] = None


    if "deal_value" not in temp.columns:

        temp["deal_value"] = 0


    if "probability" not in temp.columns:

        temp["probability"] = 0


    if "close_date" not in temp.columns:

        temp["close_date"] = pd.NaT


    if "tentative_close" not in temp.columns:

        temp["tentative_close"] = pd.NaT


    # --------------------------------------------------------
    # Convert dates
    # --------------------------------------------------------

    temp["close_date"] = pd.to_datetime(
        temp["close_date"],
        errors="coerce"
    )


    temp["tentative_close"] = pd.to_datetime(
        temp["tentative_close"],
        errors="coerce"
    )


    # --------------------------------------------------------
    # Numeric fields
    # --------------------------------------------------------

    temp["numeric_value"] = numeric_column(
        temp,
        "deal_value"
    )


    temp["numeric_probability"] = (
        pd.to_numeric(
            temp["probability"],
            errors="coerce"
        )
        .fillna(0)
    )


    # --------------------------------------------------------
    # Active only
    # --------------------------------------------------------

    temp = temp[
        temp["status"].isin([
            "Open",
            "On Hold"
        ])
    ].copy()


    if temp.empty:

        return {
            "period": period,
            "sector": sector,
            "start_date": None,
            "end_date": None,
            "total_matching_deals": 0,
            "active_deals": 0,
            "pipeline_value": 0,
            "weighted_pipeline": 0,
            "date_quality": {},
        }


    # --------------------------------------------------------
    # Sector filter
    # --------------------------------------------------------

    if sector:

        temp = temp[
            temp["sector"]
            .fillna("")
            .str.lower()
            ==
            sector.lower()
        ].copy()


    # --------------------------------------------------------
    # Period
    # --------------------------------------------------------

    start_date, end_date = (
        get_period_dates(
            period,
            reference_date
        )
    )


    # --------------------------------------------------------
    # Date matching
    #
    # Prefer close_date.
    # If close_date missing, use tentative_close.
    # --------------------------------------------------------

    temp["analysis_date"] = (
        temp["close_date"]
        .combine_first(
            temp["tentative_close"]
        )
    )


    # --------------------------------------------------------
    # Date quality before filtering
    # --------------------------------------------------------

    total_before_date_filter = len(
        temp
    )

    close_date_available = (
        temp["close_date"]
        .notna()
        .sum()
    )

    tentative_date_available = (
        temp["tentative_close"]
        .notna()
        .sum()
    )

    usable_date = (
        temp["analysis_date"]
        .notna()
        .sum()
    )

    missing_both_dates = (
        temp["analysis_date"]
        .isna()
        .sum()
    )


    # --------------------------------------------------------
    # Apply period
    # --------------------------------------------------------

    if (
        start_date is not None
        and
        end_date is not None
    ):

        temp = temp[
            (
                temp["analysis_date"]
                >= start_date
            )
            &
            (
                temp["analysis_date"]
                <= end_date
            )
        ].copy()


    # --------------------------------------------------------
    # Calculate
    # --------------------------------------------------------

    pipeline_value = (
        temp["numeric_value"]
        .sum()
    )


    weighted_pipeline = (
        temp["numeric_value"]
        *
        temp["numeric_probability"]
    ).sum()


    return {

        "period":
            period,

        "sector":
            sector,

        "start_date":
            (
                str(
                    start_date.date()
                )
                if start_date is not None
                else None
            ),

        "end_date":
            (
                str(
                    end_date.date()
                )
                if end_date is not None
                else None
            ),

        "total_matching_deals":
            int(len(temp)),

        "active_deals":
            int(len(temp)),
            
        "unclassified_active_deals": int(
            missing_both_dates
        ),

        "pipeline_value":
            float(
                pipeline_value
            ),

        "weighted_pipeline":
            float(
                weighted_pipeline
            ),

        "date_quality": {

            "active_deals_before_date_filter":
                int(
                    total_before_date_filter
                ),

            "close_date_available":
                int(
                    close_date_available
                ),

            "tentative_close_available":
                int(
                    tentative_date_available
                ),

            "usable_analysis_date":
                int(
                    usable_date
                ),

            "missing_both_dates":
                int(
                    missing_both_dates
                ),
        },
    }