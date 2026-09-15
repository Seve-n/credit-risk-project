"""
Data quality checks and cleaning for the Chevron Constantine Banking credit
application dataset.

Reads data/raw/credit_applications_raw.csv, applies documented checks and
fixes, and writes data/processed/credit_applications_clean.csv. Every action
taken here is printed as part of a data quality report, so the cleaning
decisions are auditable rather than silent.

Design principle: a missing or invalid value is either explained (and kept,
with the reason documented) or removed (and counted). Nothing is silently
guessed.
"""

from pathlib import Path

import numpy as np
import pandas as pd

RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "credit_applications_raw.csv"
PROCESSED_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "processed" / "credit_applications_clean.csv"
)

EXPECTED_TYPES = {
    "application_id": "object",
    "customer_id": "object",
    "channel": "object",
    "customer_segment": "object",
    "age_group": "object",
    "employment_status": "object",
    "annual_income": "float64",
    "monthly_expenses": "float64",
    "existing_loans": "int64",
    "requested_amount": "float64",
    "loan_term_months": "int64",
    "debt_to_income_ratio": "float64",
    "credit_history_length": "float64",
    "previous_defaults": "int64",
    "documents_complete": "bool",
    "verification_errors": "int64",
    "manual_review": "bool",
    "processing_time_hours": "float64",
    "decision": "object",
    "decision_reason": "object",
    "application_status": "object",
}


def load_data():
    df = pd.read_csv(RAW_PATH)
    df["application_date"] = pd.to_datetime(df["application_date"])
    return df


def enforce_types(df):
    """Casts columns to their expected type. Boolean columns come back from
    CSV as strings ("True"/"False"), which is the one type mismatch this
    dataset actually has after a round trip through disk."""
    df = df.copy()
    for col in ("documents_complete", "manual_review"):
        if df[col].dtype != bool:
            df[col] = df[col].astype(str).str.strip().str.lower().map({"true": True, "false": False})
    return df


def report_missing_values(df):
    missing = df.isna().sum()
    return missing[missing > 0].sort_values(ascending=False)


def handle_missing_values(df):
    """
    Three different missing-value situations, three different treatments:

    - `decision` is missing for withdrawn applications. This is a structural,
      expected null (the application never reached a decision), not a data
      quality defect. It is left as-is; any decision-focused analysis must
      filter to `application_status == "completed"` explicitly.
    - `employment_status` is missing for a small number of applications.
      There is no safe way to guess this categorical field, so it is
      recoded to an explicit "unknown" category rather than dropped or
      silently filled with the most common value. This happens first, on
      purpose: a handful of rows are missing both `employment_status` and
      `annual_income` at once, and grouping by `employment_status` before
      filling it would silently drop those rows from every group and leave
      their income un-imputed.
    - `annual_income` is missing for a small number of applications. Dropping
      these rows would bias the dataset (they are not random: mostly
      self-employed applicants who did not declare a single stable figure).
      Imputed with the median income for the same employment_status (now
      that "unknown" is itself a valid group), with an overall median as a
      fallback for the rare case a group has no non-missing income at all.
      Flagged in `annual_income_imputed` so downstream analysis can exclude
      or weight these rows differently if needed.
    """
    df = df.copy()

    df["employment_status"] = df["employment_status"].fillna("unknown")

    df["annual_income_imputed"] = df["annual_income"].isna()
    median_income_by_status = df.groupby("employment_status")["annual_income"].transform("median")
    overall_median_income = df["annual_income"].median()
    df["annual_income"] = (
        df["annual_income"].fillna(median_income_by_status).fillna(overall_median_income)
    )

    return df


def remove_duplicates(df):
    before = len(df)
    df = df.drop_duplicates(subset=[c for c in df.columns if c != "application_id"], keep="first")
    removed = before - len(df)
    return df, removed


def normalize_casing(df):
    """Channel values arrived with inconsistent casing from what looks like a
    legacy source system (e.g. "Online" vs "online"). Normalized to
    lowercase, matching the values used everywhere else in the pipeline."""
    df = df.copy()
    df["channel"] = df["channel"].str.lower()
    return df


def enforce_business_rules(df):
    """
    Business rules a valid credit application must satisfy. Rows failing any
    rule are removed rather than corrected: the raw values (e.g. a negative
    requested_amount) look like upstream data corruption, and silently
    guessing the "real" value (e.g. taking an absolute value) would invent
    data. Each violation is counted and reported.
    """
    df = df.copy()
    violations = {}

    rules = {
        "requested_amount > 0": df["requested_amount"] > 0,
        "loan_term_months > 0": df["loan_term_months"] > 0,
        "annual_income >= 0": df["annual_income"] >= 0,
        "processing_time_hours >= 0": df["processing_time_hours"] >= 0,
        "debt_to_income_ratio between 0 and 2": df["debt_to_income_ratio"].between(0, 2),
    }

    valid_mask = pd.Series(True, index=df.index)
    for rule_name, mask in rules.items():
        failing = (~mask).sum()
        violations[rule_name] = int(failing)
        valid_mask &= mask

    removed = int((~valid_mask).sum())
    return df[valid_mask].reset_index(drop=True), violations, removed


def main():
    df = load_data()
    print(f"Loaded {len(df)} rows from {RAW_PATH.name}")

    df = enforce_types(df)

    print("\nMissing values before cleaning:")
    print(report_missing_values(df))

    df = handle_missing_values(df)
    df = normalize_casing(df)
    df, duplicates_removed = remove_duplicates(df)
    df, rule_violations, rule_rows_removed = enforce_business_rules(df)

    print(f"\nExact duplicate rows removed: {duplicates_removed}")
    print("\nBusiness rule violations found (rows removed for failing at least one):")
    for rule, count in rule_violations.items():
        print(f"  {rule}: {count} violation(s)")
    print(f"Total rows removed for business rule violations: {rule_rows_removed}")

    print(f"\nRows with imputed annual_income: {int(df['annual_income_imputed'].sum())}")
    print(f"Rows with employment_status recoded to 'unknown': {int((df['employment_status'] == 'unknown').sum())}")

    print("\nMissing values after cleaning (decision is expected to remain, see docstring):")
    print(report_missing_values(df))

    print(f"\nFinal dataset: {len(df)} rows")

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Saved cleaned dataset -> {PROCESSED_PATH}")


if __name__ == "__main__":
    main()
