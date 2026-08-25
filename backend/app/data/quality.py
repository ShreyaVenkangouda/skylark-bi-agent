import pandas as pd


def calculate_quality(df):

    if df.empty:

        return {
            "rows": 0,
            "columns": 0,
            "missing_cells": 0,
            "missing_percentage": 0,
            "issues": [
                "No records found."
            ]
        }

    total_cells = (
        df.shape[0]
        *
        df.shape[1]
    )

    missing_cells = int(
        df.isna()
        .sum()
        .sum()
    )

    missing_percentage = (
        missing_cells
        /
        total_cells
        *
        100
    )

    issues = []

    for column in df.columns:

        missing = int(
            df[column]
            .isna()
            .sum()
        )

        if missing:

            percentage = (
                missing
                /
                len(df)
                *
                100
            )

            issues.append(
                f"{column}: "
                f"{missing} missing "
                f"({percentage:.1f}%)"
            )

    return {

        "rows":
            len(df),

        "columns":
            len(df.columns),

        "missing_cells":
            missing_cells,

        "missing_percentage":
            round(
                missing_percentage,
                2
            ),

        "issues":
            issues[:20]
    }