import re


# ============================================================
# SECTOR DETECTION
# ============================================================

SECTOR_KEYWORDS = {

    "energy": "Renewables",

    "renewable":
        "Renewables",

    "renewables":
        "Renewables",

    "mining":
        "Mining",

    "railways":
        "Railways",

    "railway":
        "Railways",

    "powerline":
        "Powerline",

    "power line":
        "Powerline",

    "construction":
        "Construction",

    "manufacturing":
        "Manufacturing",

    "aviation":
        "Aviation",

    "security":
        "Security & Surveillance",

    "surveillance":
        "Security & Surveillance",

    "dsp":
        "DSP",

    "tender":
        "Tender",
}


# ============================================================
# TIME PERIOD DETECTION
# ============================================================

def detect_period(question):

    q = question.lower()

    if "this quarter" in q:

        return "this_quarter"

    if "current quarter" in q:

        return "this_quarter"

    if "last quarter" in q:

        return "last_quarter"

    if "previous quarter" in q:

        return "last_quarter"

    if "next quarter" in q:

        return "next_quarter"

    if "this month" in q:

        return "this_month"

    if "current month" in q:

        return "this_month"

    if "last month" in q:

        return "last_month"

    if "next month" in q:

        return "next_month"

    if "year to date" in q:

        return "ytd"

    if "ytd" in q:

        return "ytd"

    return "all_time"


# ============================================================
# SECTOR DETECTION
# ============================================================

def detect_sector(question):

    q = question.lower()

    # Longest phrases first
    keywords = sorted(
        SECTOR_KEYWORDS.keys(),
        key=len,
        reverse=True
    )

    for keyword in keywords:

        if keyword in q:

            return SECTOR_KEYWORDS[
                keyword
            ]

    return None


# ============================================================
# QUESTION ROUTER
# ============================================================

def route_question(question):

    q = question.lower()


    # --------------------------------------------------------
    # Pipeline / sales
    # --------------------------------------------------------

    deals = any(
        word in q
        for word in [
            "pipeline",
            "deal",
            "deals",
            "sales",
            "opportunity",
            "opportunities",
            "revenue",
            "booking",
            "win",
            "won",
        ]
    )


    # --------------------------------------------------------
    # Operations
    # --------------------------------------------------------

    work_orders = any(
        word in q
        for word in [
            "work order",
            "work orders",
            "operations",
            "operational",
            "execution",
            "billing",
            "billed",
            "invoice",
            "invoices",
            "collection",
            "collected",
            "receivable",
            "receivables",
        ]
    )


    # --------------------------------------------------------
    # Leadership
    # --------------------------------------------------------

    leadership = any(
        word in q
        for word in [
            "leadership",
            "executive",
            "founder",
            "management",
            "management update",
            "leadership update",
            "board update",
            "business update",
        ]
    )


    # --------------------------------------------------------
    # Sector
    # --------------------------------------------------------

    sector = detect_sector(
        question
    )


    # --------------------------------------------------------
    # Period
    # --------------------------------------------------------

    period = detect_period(
        question
    )


    # --------------------------------------------------------
    # Sector questions usually imply deals
    # --------------------------------------------------------

    if sector:

        deals = True


    # --------------------------------------------------------
    # Leadership questions need both boards
    # --------------------------------------------------------

    if leadership:

        deals = True
        work_orders = True


    return {

        "deals":
            deals,

        "work_orders":
            work_orders,

        "leadership":
            leadership,

        "sector":
            sector,

        "period":
            period,
    }