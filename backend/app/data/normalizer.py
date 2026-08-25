import re

import pandas as pd


NULL_VALUES = {
    "",
    "-",
    "--",
    "n/a",
    "na",
    "none",
    "null",
    "nil",
    "nan",
    "not available",
    "unknown",
}


SECTOR_MAP = {

    "renewables":
        "Renewables",

    "renewable energy":
        "Renewables",

    "energy":
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

    "others":
        "Others",

    "other":
        "Others",

    "dsp":
        "DSP",

    "tender":
        "Tender",

    "security and surveillance":
        "Security & Surveillance",

    "security & surveillance":
        "Security & Surveillance",
}


STATUS_MAP = {

    "open":
        "Open",

    "won":
        "Won",

    "dead":
        "Dead",

    "lost":
        "Dead",

    "on hold":
        "On Hold",

    "ongoing":
        "Ongoing",

    "completed":
        "Completed",

    "not started":
        "Not Started",

    "cancelled":
        "Cancelled",

    "canceled":
        "Cancelled",

    "in progress":
        "Ongoing",
}


PROBABILITY_MAP = {

    "high":
        0.80,

    "medium":
        0.50,

    "low":
        0.20,
}


def clean_text(value):

    if value is None:
        return None

    if isinstance(value, float):

        if pd.isna(value):
            return None

    value = str(value).strip()

    if value.lower() in NULL_VALUES:
        return None

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value


def normalize_sector(value):

    value = clean_text(value)

    if not value:
        return None

    cleaned = value.lower().strip()

    return SECTOR_MAP.get(
        cleaned,
        value.title()
    )


def normalize_status(value):

    value = clean_text(value)

    if not value:
        return None

    cleaned = value.lower().strip()

    return STATUS_MAP.get(
        cleaned,
        value.title()
    )


def normalize_probability(value):

    value = clean_text(value)

    if not value:
        return None

    cleaned = value.lower().strip()

    if cleaned in PROBABILITY_MAP:

        return PROBABILITY_MAP[
            cleaned
        ]

    try:

        number = float(
            cleaned.replace(
                "%",
                ""
            )
        )

        if number > 1:
            number /= 100

        if number < 0 or number > 1:
            return None

        return number

    except (
        ValueError,
        TypeError
    ):

        return None


def parse_number(value):

    value = clean_text(value)

    if value is None:
        return None

    try:

        cleaned = re.sub(
            r"[₹$€£,\s]",
            "",
            value
        )

        return float(cleaned)

    except (
        ValueError,
        TypeError
    ):

        return None


def parse_date(value):

    value = clean_text(value)

    if not value:
        return None

    parsed = pd.to_datetime(
        value,
        errors="coerce"
    )

    if pd.isna(parsed):
        return None

    return parsed


def remove_header_rows(
    df,
    checks
):

    if df.empty:
        return df

    mask = pd.Series(
        True,
        index=df.index
    )

    for column, value in checks.items():

        if column in df.columns:

            mask &= (
                df[column]
                .astype(str)
                .str.strip()
                != value
            )

    return df[mask].copy()


def monday_items_to_dataframe(
    items
):

    rows = []

    for item in items:

        row = {

            "monday_item_id":
                item.get("id"),

            "name":
                clean_text(
                    item.get("name")
                )
        }

        for column in item.get(
            "column_values",
            []
        ):

            column_id = column.get(
                "id"
            )

            row[column_id] = clean_text(
                column.get("text")
            )

        rows.append(row)

    return pd.DataFrame(rows)


def rename_monday_columns(
    df,
    mapping
):

    """
    Convert Monday column IDs into
    normalized business field names.
    """

    if df.empty:
        return df

    rename_map = {}

    for monday_id, field_name in mapping.items():

        if monday_id in df.columns:

            rename_map[monday_id] = (
                field_name
            )

    return df.rename(
        columns=rename_map
    )


def normalize_deals(df):

    if df.empty:
        return df

    df = df.copy()


    # Deal status

    if "status" in df.columns:

        df["status"] = (
            df["status"]
            .apply(normalize_status)
        )


    # Sector

    if "sector" in df.columns:

        df["sector"] = (
            df["sector"]
            .apply(normalize_sector)
        )


    # Probability

    if "probability" in df.columns:

        df["probability"] = (
            df["probability"]
            .apply(
                normalize_probability
            )
        )


    # Deal value

    if "deal_value" in df.columns:

        df["deal_value"] = (
            df["deal_value"]
            .apply(parse_number)
        )


    # Dates

    for column in [

        "close_date",

        "tentative_close",

        "created_date"

    ]:

        if column in df.columns:

            df[column] = (
                df[column]
                .apply(parse_date)
            )


    # Remove accidental/header-like rows

    if (
        "status" in df.columns
        and
        "deal_name" in df.columns
    ):

        df = df[
            df["status"].notna()
            |
            df["deal_name"].notna()
        ]


    return df


def normalize_work_orders(df):

    if df.empty:
        return df

    df = df.copy()


    # Sector

    if "sector" in df.columns:

        df["sector"] = (
            df["sector"]
            .apply(normalize_sector)
        )


    # Status fields

    for column in [

        "execution_status",

        "invoice_status",

        "wo_status",

        "billing_status"

    ]:

        if column in df.columns:

            df[column] = (
                df[column]
                .apply(normalize_status)
            )


    # Money fields

    money_columns = [

        "amount_ex_gst",

        "amount_inc_gst",

        "billed_ex_gst",

        "billed_inc_gst",

        "collected_inc_gst",

        "to_be_billed_ex_gst",

        "to_be_billed_inc_gst",

        "receivable"

    ]


    for column in money_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .apply(parse_number)
            )


    # Quantity fields

    number_columns = [

        "quantity_ops",

        "quantity_po",

        "quantity_billed",

        "balance_quantity"

    ]


    for column in number_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .apply(parse_number)
            )


    # Date fields

    date_columns = [

        "delivery_date",

        "po_date",

        "start_date",

        "end_date",

        "last_invoice_date",

        "collection_date"

    ]


    for column in date_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .apply(parse_date)
            )


    return df