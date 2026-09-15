"""
Synthetic dataset generator for the Chevron Constantine Banking credit
application portfolio.

This script does not model real credit risk. It builds a plausible, internally
consistent dataset for practicing Business Analyst-style work: KPI
calculation, processing time investigation, decision analysis, and data
quality checks. Every relationship implemented here is described in
docs/assumptions.md; this file is the code-level source of truth for how each
relationship is actually implemented, and the two should stay in sync.

Column list and rationale: business-analysis/data-requirements.md.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_APPLICATIONS = 20_000
OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "raw" / "credit_applications_raw.csv"
)

rng = np.random.default_rng(SEED)


def generate_application_dates(n):
    """Applications spread uniformly over an 18-month window."""
    end = pd.Timestamp("2026-06-30")
    start = end - pd.DateOffset(months=18)
    offsets = rng.integers(0, (end - start).days, size=n)
    return start + pd.to_timedelta(offsets, unit="D")


def generate_channel(n):
    channels = ["online", "mobile_app", "branch", "broker", "phone"]
    weights = [0.35, 0.25, 0.20, 0.15, 0.05]
    return rng.choice(channels, size=n, p=weights)


def generate_customer_segment(n):
    segments = ["retail_mass", "retail_affluent", "self_employed", "small_business"]
    weights = [0.55, 0.20, 0.15, 0.10]
    return rng.choice(segments, size=n, p=weights)


def generate_age_group(n):
    groups = ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
    weights = [0.08, 0.22, 0.24, 0.20, 0.16, 0.10]
    return rng.choice(groups, size=n, p=weights)


def generate_employment_status(age_group, customer_segment):
    """Employment status is not independent of age or segment: retirees
    cluster in the 65+ group, and self-employed/small-business customers are
    mostly self-employed by definition."""
    n = len(age_group)
    status = np.empty(n, dtype=object)
    for i in range(n):
        if age_group[i] == "65+":
            status[i] = rng.choice(
                ["retired", "employed", "self_employed"], p=[0.70, 0.20, 0.10]
            )
        elif customer_segment[i] in ("self_employed", "small_business"):
            status[i] = rng.choice(
                ["self_employed", "employed", "unemployed"], p=[0.80, 0.15, 0.05]
            )
        else:
            status[i] = rng.choice(
                ["employed", "self_employed", "unemployed", "retired"],
                p=[0.82, 0.08, 0.06, 0.04],
            )
    return status


def generate_annual_income(employment_status, customer_segment):
    """Income follows a log-normal draw per employment status, then scaled by
    segment, to get realistic right-skewed income distributions instead of a
    flat range."""
    n = len(employment_status)
    income = np.empty(n)
    base_params = {
        "employed": (42_000, 0.40),
        "self_employed": (38_000, 0.60),
        "unemployed": (14_000, 0.30),
        "retired": (22_000, 0.30),
    }
    segment_multiplier = {
        "retail_mass": 1.0,
        "retail_affluent": 1.8,
        "self_employed": 1.0,
        "small_business": 1.3,
    }
    for i in range(n):
        median, sigma = base_params[employment_status[i]]
        draw = rng.lognormal(mean=np.log(median), sigma=sigma)
        income[i] = draw * segment_multiplier[customer_segment[i]]
    return np.round(income, 2)


def generate_monthly_expenses(annual_income):
    monthly_income = annual_income / 12
    factor = rng.uniform(0.35, 0.85, size=len(annual_income))
    return np.round(monthly_income * factor, 2)


def generate_existing_loans(customer_segment, annual_income):
    base_lambda = np.where(
        np.isin(customer_segment, ["self_employed", "small_business"]), 1.3, 0.8
    )
    income_boost = np.clip(annual_income / 60_000, 0.5, 2.0)
    counts = rng.poisson(base_lambda * income_boost)
    return np.clip(counts, 0, 5)


def generate_requested_amount(customer_segment, annual_income):
    """Requested amount scales with income and segment (small businesses
    request larger amounts relative to income than retail customers)."""
    multiplier_by_segment = {
        "retail_mass": (0.3, 1.2),
        "retail_affluent": (0.5, 2.0),
        "self_employed": (0.4, 1.8),
        "small_business": (0.8, 3.0),
    }
    n = len(customer_segment)
    amounts = np.empty(n)
    for i in range(n):
        low, high = multiplier_by_segment[customer_segment[i]]
        amounts[i] = annual_income[i] * rng.uniform(low, high)
    return np.round(np.clip(amounts, 2_000, 500_000), 2)


def generate_loan_term_months(requested_amount):
    """Larger loans tend to be spread over longer terms."""
    terms = np.array([12, 24, 36, 48, 60, 84, 120])
    n = len(requested_amount)
    result = np.empty(n, dtype=int)
    for i in range(n):
        if requested_amount[i] < 10_000:
            weights = [0.35, 0.30, 0.20, 0.10, 0.05, 0.00, 0.00]
        elif requested_amount[i] < 50_000:
            weights = [0.05, 0.15, 0.25, 0.25, 0.20, 0.10, 0.00]
        else:
            weights = [0.00, 0.05, 0.10, 0.15, 0.25, 0.25, 0.20]
        result[i] = rng.choice(terms, p=weights)
    return result


def generate_debt_to_income_ratio(monthly_expenses, existing_loans, annual_income):
    monthly_income = annual_income / 12
    estimated_loan_payments = existing_loans * 150
    debt_related_expenses = monthly_expenses * 0.4 + estimated_loan_payments
    dti = debt_related_expenses / monthly_income
    noise = rng.normal(0, 0.03, size=len(annual_income))
    return np.round(np.clip(dti + noise, 0.02, 1.4), 3)


def generate_credit_history_length(age_group):
    age_floor = {"18-25": 21, "26-35": 30, "36-45": 40, "46-55": 50, "56-65": 60, "65+": 68}
    n = len(age_group)
    lengths = np.empty(n)
    for i in range(n):
        max_possible = max(age_floor[age_group[i]] - 18, 1)
        lengths[i] = rng.uniform(0, max_possible)
    return np.round(lengths, 1)


def generate_previous_defaults(debt_to_income_ratio, employment_status):
    base_lambda = np.where(employment_status == "unemployed", 0.6, 0.15)
    dti_boost = np.clip(debt_to_income_ratio, 0.1, 1.4)
    counts = rng.poisson(base_lambda * dti_boost * 2)
    return np.clip(counts, 0, 3)


def generate_documents_complete(channel):
    """In-person channels (branch, broker) catch missing documents on the
    spot more often than fully digital or phone channels."""
    completeness_by_channel = {
        "branch": 0.93,
        "broker": 0.90,
        "phone": 0.85,
        "mobile_app": 0.82,
        "online": 0.78,
    }
    probs = np.array([completeness_by_channel[c] for c in channel])
    return rng.random(len(channel)) < probs


def generate_verification_errors(documents_complete):
    """Incomplete applications carry more verification errors downstream."""
    lam = np.where(documents_complete, 0.3, 2.4)
    return np.clip(rng.poisson(lam), 0, 6)


def generate_manual_review(
    verification_errors, debt_to_income_ratio, requested_amount, previous_defaults, documents_complete
):
    """Manual review probability increases with each complexity signal:
    verification errors, high DTI, large requested amount, prior defaults,
    and incomplete documents. This is a weighted score, not a real risk
    model."""
    amount_percentile = pd.Series(requested_amount).rank(pct=True).values
    score = (
        0.35 * (verification_errors >= 2)
        + 0.25 * (debt_to_income_ratio > 0.55)
        + 0.20 * (amount_percentile > 0.75)
        + 0.15 * (previous_defaults >= 1)
        + 0.15 * (~documents_complete)
    )
    probability = np.clip(score, 0.03, 0.95)
    return rng.random(len(verification_errors)) < probability


def generate_processing_time_hours(manual_review, verification_errors, documents_complete, channel):
    """Base processing time plus additive delays for manual review, each
    verification error, incomplete documents, and a small channel effect."""
    n = len(manual_review)
    hours = rng.normal(loc=20, scale=5, size=n)
    hours += np.where(manual_review, rng.normal(60, 20, size=n), 0)
    hours += verification_errors * 6
    hours += np.where(~documents_complete, rng.normal(16, 5, size=n), 0)
    channel_adjustment = {"branch": -3, "broker": 0, "phone": 4, "mobile_app": -1, "online": -2}
    hours += np.array([channel_adjustment[c] for c in channel])
    return np.round(np.clip(hours, 2, 400), 1)


def generate_application_status(manual_review, processing_time_hours):
    """A small share of applications are withdrawn by the customer before a
    decision is made, disproportionately when manual review drags on. This
    is a legitimate business outcome, not a data quality problem: the
    resulting missing `decision` for these rows is expected and should not
    be imputed in the cleaning phase."""
    withdrawal_prob = np.where(
        manual_review & (processing_time_hours > 80),
        0.18,
        np.where(manual_review, 0.05, 0.01),
    )
    withdrawn = rng.random(len(manual_review)) < withdrawal_prob
    return np.where(withdrawn, "withdrawn", "completed")


def generate_decision(
    application_status, debt_to_income_ratio, previous_defaults, annual_income, requested_amount, documents_complete
):
    n = len(application_status)
    decision = np.full(n, None, dtype=object)
    reason = np.full(n, None, dtype=object)

    income_to_amount = annual_income / np.clip(requested_amount, 1, None)
    approval_score = (
        0.40 * (debt_to_income_ratio < 0.40)
        + 0.25 * (previous_defaults == 0)
        + 0.20 * (income_to_amount > 0.5)
        + 0.15 * documents_complete
    )
    approval_probability = np.clip(approval_score, 0.05, 0.95)
    approved_draw = rng.random(n) < approval_probability

    approval_reasons = [
        "stable income relative to requested amount",
        "clean credit history",
        "acceptable debt-to-income ratio",
    ]

    for i in range(n):
        if application_status[i] == "withdrawn":
            reason[i] = "customer withdrew before a decision was reached"
            continue
        if approved_draw[i]:
            decision[i] = "approved"
            reason[i] = rng.choice(approval_reasons)
        else:
            decision[i] = "rejected"
            if debt_to_income_ratio[i] >= 0.40:
                reason[i] = "debt-to-income ratio above acceptable threshold"
            elif previous_defaults[i] > 0:
                reason[i] = "previous credit default on record"
            elif not documents_complete[i]:
                reason[i] = "incomplete documentation"
            else:
                reason[i] = "income insufficient relative to requested amount"

    return decision, reason


def inject_data_quality_issues(df):
    """Deliberately introduces realistic data quality problems, so the
    Phase 4 cleaning step has real issues to find and document instead of a
    suspiciously perfect dataset. Every issue introduced here is listed in
    docs/assumptions.md."""
    df = df.copy()
    n = len(df)

    missing_income_idx = rng.choice(n, size=int(n * 0.015), replace=False)
    df.loc[missing_income_idx, "annual_income"] = np.nan

    missing_employment_idx = rng.choice(n, size=int(n * 0.01), replace=False)
    df.loc[missing_employment_idx, "employment_status"] = np.nan

    casing_idx = rng.choice(n, size=int(n * 0.02), replace=False)
    df.loc[casing_idx, "channel"] = df.loc[casing_idx, "channel"].str.capitalize()

    duplicate_idx = rng.choice(n, size=int(n * 0.004), replace=False)
    df = pd.concat([df, df.loc[duplicate_idx]], ignore_index=True)

    invalid_idx = rng.choice(len(df), size=max(int(len(df) * 0.001), 5), replace=False)
    for idx in invalid_idx:
        field = rng.choice(["requested_amount", "processing_time_hours", "loan_term_months"])
        if field == "requested_amount":
            df.loc[idx, "requested_amount"] = -abs(df.loc[idx, "requested_amount"])
        elif field == "processing_time_hours":
            df.loc[idx, "processing_time_hours"] = -1
        else:
            df.loc[idx, "loan_term_months"] = 0

    return df.sample(frac=1, random_state=SEED).reset_index(drop=True)


def main():
    n = N_APPLICATIONS

    application_date = generate_application_dates(n)
    channel = generate_channel(n)
    customer_segment = generate_customer_segment(n)
    age_group = generate_age_group(n)
    employment_status = generate_employment_status(age_group, customer_segment)
    annual_income = generate_annual_income(employment_status, customer_segment)
    monthly_expenses = generate_monthly_expenses(annual_income)
    existing_loans = generate_existing_loans(customer_segment, annual_income)
    requested_amount = generate_requested_amount(customer_segment, annual_income)
    loan_term_months = generate_loan_term_months(requested_amount)
    debt_to_income_ratio = generate_debt_to_income_ratio(monthly_expenses, existing_loans, annual_income)
    credit_history_length = generate_credit_history_length(age_group)
    previous_defaults = generate_previous_defaults(debt_to_income_ratio, employment_status)
    documents_complete = generate_documents_complete(channel)
    verification_errors = generate_verification_errors(documents_complete)
    manual_review = generate_manual_review(
        verification_errors, debt_to_income_ratio, requested_amount, previous_defaults, documents_complete
    )
    processing_time_hours = generate_processing_time_hours(
        manual_review, verification_errors, documents_complete, channel
    )
    application_status = generate_application_status(manual_review, processing_time_hours)
    decision, decision_reason = generate_decision(
        application_status, debt_to_income_ratio, previous_defaults, annual_income, requested_amount, documents_complete
    )

    df = pd.DataFrame(
        {
            "application_id": [f"APP-{i:06d}" for i in range(n)],
            "customer_id": [f"CUST-{i:06d}" for i in range(n)],
            "application_date": application_date,
            "channel": channel,
            "customer_segment": customer_segment,
            "age_group": age_group,
            "employment_status": employment_status,
            "annual_income": annual_income,
            "monthly_expenses": monthly_expenses,
            "existing_loans": existing_loans,
            "requested_amount": requested_amount,
            "loan_term_months": loan_term_months,
            "debt_to_income_ratio": debt_to_income_ratio,
            "credit_history_length": credit_history_length,
            "previous_defaults": previous_defaults,
            "documents_complete": documents_complete,
            "verification_errors": verification_errors,
            "manual_review": manual_review,
            "processing_time_hours": processing_time_hours,
            "decision": decision,
            "decision_reason": decision_reason,
            "application_status": application_status,
        }
    )

    df = inject_data_quality_issues(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(df)} rows -> {OUTPUT_PATH}")
    print("\napplication_status:\n", df["application_status"].value_counts())
    print("\ndecision (NaN = withdrawn):\n", df["decision"].value_counts(dropna=False))
    print("\nmanual_review:\n", df["manual_review"].value_counts())


if __name__ == "__main__":
    main()
