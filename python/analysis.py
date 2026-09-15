"""
Portfolio KPIs, processing time, and manual review analysis for the Chevron
Constantine Banking credit application dataset.

This module is the single source of truth for how every KPI in this project
is defined. The SQL queries in sql/ and the Power BI measures in
dashboard/README.md must compute the same numbers using the same logic - if
they ever disagree, this file is right and the other one has a bug (see
docs/methodology.md once written, for why this matters and what it caught
last time on the companion project).

Every function returns a plain pandas object (Series, DataFrame, or float) so
it can be called directly from the notebook, or wrapped in a print/plot call
without needing to modify this file.
"""

from pathlib import Path

import numpy as np
import pandas as pd

PROCESSED_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "processed" / "credit_applications_clean.csv"
)


def load_clean_data():
    df = pd.read_csv(PROCESSED_PATH)
    df["application_date"] = pd.to_datetime(df["application_date"])
    for col in ("documents_complete", "manual_review"):
        df[col] = df[col].astype(str).str.strip().str.lower().map({"true": True, "false": False})
    return df


# ---------------------------------------------------------------------------
# Portfolio KPIs
# ---------------------------------------------------------------------------
#
# `decision` is only meaningful for completed applications (withdrawn
# applications have no decision by construction, see data_cleaning.py).
# Approval and rejection rate are therefore expressed as a share of decided
# applications, not of the full portfolio, otherwise a change in the
# withdrawal rate would silently move both rates without anything about the
# decision logic actually changing.


def total_applications(df):
    return len(df)


def approval_rate(df):
    decided = df[df["decision"].notna()]
    return (decided["decision"] == "approved").mean()


def rejection_rate(df):
    decided = df[df["decision"].notna()]
    return (decided["decision"] == "rejected").mean()


def withdrawal_rate(df):
    return (df["application_status"] == "withdrawn").mean()


def manual_review_rate(df):
    return df["manual_review"].mean()


def processing_time_stats(df):
    return {
        "mean": df["processing_time_hours"].mean(),
        "median": df["processing_time_hours"].median(),
        "p90": df["processing_time_hours"].quantile(0.90),
    }


def average_requested_amount(df):
    return df["requested_amount"].mean()


def incomplete_application_rate(df):
    return (~df["documents_complete"]).mean()


def average_verification_errors(df):
    return df["verification_errors"].mean()


def portfolio_kpi_summary(df):
    """One-row summary of every top-level KPI, for a quick sanity check or a
    dashboard header card."""
    stats = processing_time_stats(df)
    return pd.Series(
        {
            "total_applications": total_applications(df),
            "approval_rate": approval_rate(df),
            "rejection_rate": rejection_rate(df),
            "withdrawal_rate": withdrawal_rate(df),
            "manual_review_rate": manual_review_rate(df),
            "avg_processing_time_hours": stats["mean"],
            "median_processing_time_hours": stats["median"],
            "p90_processing_time_hours": stats["p90"],
            "avg_requested_amount": average_requested_amount(df),
            "incomplete_application_rate": incomplete_application_rate(df),
            "avg_verification_errors": average_verification_errors(df),
        }
    )


# ---------------------------------------------------------------------------
# KPI breakdowns
# ---------------------------------------------------------------------------


def kpi_by_group(df, group_col):
    """Core KPIs recomputed per value of `group_col` (channel, segment,
    loan_term_months, manual_review, decision, ...). Kept generic rather than
    writing one function per dimension, since the calculation is identical
    and only the grouping column changes."""
    decided = df[df["decision"].notna()]

    approval = decided.groupby(group_col, observed=True)["decision"].apply(lambda s: (s == "approved").mean())
    rejection = decided.groupby(group_col, observed=True)["decision"].apply(lambda s: (s == "rejected").mean())

    grouped = df.groupby(group_col, observed=True)
    result = pd.DataFrame(
        {
            "count": grouped.size(),
            "approval_rate": approval,
            "rejection_rate": rejection,
            "manual_review_rate": grouped["manual_review"].mean(),
            "avg_processing_time_hours": grouped["processing_time_hours"].mean(),
            "median_processing_time_hours": grouped["processing_time_hours"].median(),
            "avg_requested_amount": grouped["requested_amount"].mean(),
            "incomplete_application_rate": grouped["documents_complete"].apply(lambda s: (~s).mean()),
        }
    )
    return result.sort_values("count", ascending=False)


def kpi_by_loan_size_band(df, bins=(0, 10_000, 25_000, 50_000, 100_000, np.inf)):
    labels = ["<10k", "10k-25k", "25k-50k", "50k-100k", "100k+"]
    df = df.copy()
    df["loan_size_band"] = pd.cut(df["requested_amount"], bins=bins, labels=labels)
    return kpi_by_group(df, "loan_size_band")


# ---------------------------------------------------------------------------
# Processing time analysis (section: which applications take the longest)
# ---------------------------------------------------------------------------


def processing_time_by_manual_review(df):
    """The core comparison behind the manual-review pain point: automated
    vs. manually reviewed applications, median and p90 rather than just the
    mean, since processing time is right-skewed and the mean alone hides how
    bad the tail is."""
    return df.groupby("manual_review")["processing_time_hours"].agg(
        mean="mean", median="median", p90=lambda s: s.quantile(0.90), count="count"
    )


def processing_time_by_channel(df):
    return df.groupby("channel")["processing_time_hours"].agg(
        mean="mean", median="median", p90=lambda s: s.quantile(0.90), count="count"
    ).sort_values("median", ascending=False)


def processing_time_by_documents_complete(df):
    return df.groupby("documents_complete")["processing_time_hours"].agg(
        mean="mean", median="median", p90=lambda s: s.quantile(0.90), count="count"
    )


def verification_errors_vs_processing_time(df):
    """Average processing time for each distinct verification error count,
    to check whether the relationship looks roughly monotonic rather than
    just reporting a single correlation coefficient."""
    return df.groupby("verification_errors")["processing_time_hours"].agg(mean="mean", count="count")


def top_decile_processing_time_profile(df):
    """Profile of the slowest 10% of applications: what do they have in
    common? Used to check whether "slow" mostly means "manual review and
    incomplete documents" or something less expected."""
    threshold = df["processing_time_hours"].quantile(0.90)
    slow = df[df["processing_time_hours"] >= threshold]
    return pd.Series(
        {
            "count": len(slow),
            "manual_review_rate": slow["manual_review"].mean(),
            "incomplete_rate": (~slow["documents_complete"]).mean(),
            "avg_verification_errors": slow["verification_errors"].mean(),
            "avg_requested_amount": slow["requested_amount"].mean(),
        }
    )


# ---------------------------------------------------------------------------
# Manual review analysis
# ---------------------------------------------------------------------------


def manual_review_rate_by_segment(df):
    return df.groupby("customer_segment")["manual_review"].mean().sort_values(ascending=False)


def manual_review_rate_by_loan_size(df):
    return kpi_by_loan_size_band(df)["manual_review_rate"]


def manual_review_rate_by_documents_complete(df):
    return df.groupby("documents_complete")["manual_review"].mean()


def manual_review_outcome_breakdown(df):
    """Of the applications that went to manual review, what share ended up
    approved, rejected, or withdrawn? This is the number that supports (or
    undercuts) an automation argument: if manual review overwhelmingly
    confirms the same outcome an automated rule would have reached, that is
    an automation opportunity; if it frequently overturns the likely
    automated outcome, that is evidence the human step is doing real work."""
    reviewed = df[df["manual_review"]]
    outcome = reviewed["application_status"].where(
        reviewed["application_status"] == "withdrawn", reviewed["decision"]
    )
    return outcome.value_counts(normalize=True)


if __name__ == "__main__":
    data = load_clean_data()
    print("Portfolio KPI summary:")
    print(portfolio_kpi_summary(data))
    print("\nManual review vs. processing time:")
    print(processing_time_by_manual_review(data))
    print("\nManual review outcome breakdown:")
    print(manual_review_outcome_breakdown(data))
