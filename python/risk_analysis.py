"""
Credit decision analysis for the Chevron Constantine Banking dataset.

Compares the profile of applications that were approved automatically,
rejected automatically, or routed to manual review, and looks at how
individual factors (debt-to-income ratio, previous defaults, income relative
to the requested amount, document completeness) line up with the decision.

None of this is a credit scoring model, and none of the results below should
be read as a proven cause of a decision. Everything here is an association in
a synthetic, simulated dataset: useful for practicing the analysis, not for
inferring how a real credit decision is actually made.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from analysis import load_clean_data


def decision_path_category(df):
    """Three mutually exclusive buckets, independent of the final outcome of
    a manual review: `manual_review` (sent to a human, regardless of what
    happened next), `approved` / `rejected` (decided automatically, straight
    through), and `withdrawn` (no manual review, but the customer pulled out
    anyway). This isolates "what kind of file triggers manual review" from
    "what kind of file gets approved," which is a different question."""
    decision = df["decision"].fillna("withdrawn")
    return np.where(df["manual_review"], "manual_review", decision)


def profile_by_decision_path(df):
    df = df.copy()
    df["decision_path"] = decision_path_category(df)
    grouped = df.groupby("decision_path")
    return pd.DataFrame(
        {
            "count": grouped.size(),
            "avg_annual_income": grouped["annual_income"].mean(),
            "avg_monthly_expenses": grouped["monthly_expenses"].mean(),
            "avg_debt_to_income_ratio": grouped["debt_to_income_ratio"].mean(),
            "avg_requested_amount": grouped["requested_amount"].mean(),
            "avg_previous_defaults": grouped["previous_defaults"].mean(),
            "incomplete_document_rate": grouped["documents_complete"].apply(lambda s: (~s).mean()),
        }
    )


def dti_band_vs_decision(df, bins=(0, 0.20, 0.35, 0.50, 0.70, np.inf)):
    """Approval rate by debt-to-income band, restricted to applications that
    reached an automatic or manual decision (withdrawn applications have no
    decision to compare)."""
    labels = ["<0.20", "0.20-0.35", "0.35-0.50", "0.50-0.70", "0.70+"]
    decided = df[df["decision"].notna()].copy()
    decided["dti_band"] = pd.cut(decided["debt_to_income_ratio"], bins=bins, labels=labels)
    return decided.groupby("dti_band", observed=True)["decision"].apply(lambda s: (s == "approved").mean())


def previous_defaults_vs_decision(df):
    decided = df[df["decision"].notna()].copy()
    decided["previous_defaults_band"] = decided["previous_defaults"].clip(upper=3).astype(str)
    decided.loc[decided["previous_defaults"] >= 3, "previous_defaults_band"] = "3+"
    return decided.groupby("previous_defaults_band")["decision"].apply(lambda s: (s == "approved").mean())


def income_to_amount_ratio_vs_decision(df, bins=(0, 0.5, 1.0, 2.0, np.inf)):
    """Ratio of annual income to requested amount: a rough affordability
    signal. Higher ratio means the requested amount is small relative to
    income."""
    labels = ["<0.5x", "0.5x-1x", "1x-2x", "2x+"]
    decided = df[df["decision"].notna()].copy()
    decided["income_to_amount_ratio"] = decided["annual_income"] / decided["requested_amount"]
    decided["ratio_band"] = pd.cut(decided["income_to_amount_ratio"], bins=bins, labels=labels)
    return decided.groupby("ratio_band", observed=True)["decision"].apply(lambda s: (s == "approved").mean())


def documents_complete_vs_decision(df):
    decided = df[df["decision"].notna()]
    return decided.groupby("documents_complete")["decision"].apply(lambda s: (s == "approved").mean())


if __name__ == "__main__":
    data = load_clean_data()

    print("Profile by decision path (approved / rejected / manual_review / withdrawn):")
    print(profile_by_decision_path(data))

    print("\nApproval rate by debt-to-income band:")
    print(dti_band_vs_decision(data))

    print("\nApproval rate by previous defaults:")
    print(previous_defaults_vs_decision(data))

    print("\nApproval rate by income-to-requested-amount ratio:")
    print(income_to_amount_ratio_vs_decision(data))

    print("\nApproval rate by document completeness:")
    print(documents_complete_vs_decision(data))
