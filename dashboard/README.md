# Power BI Dashboard: Specification

This is a specification, not a built `.pbix` file, for the same reason as the
companion customer-journey project: a `.pbix` binary does not diff or review well
in Git, and every number in it needs to already exist and be trusted (in
`python/analysis.py` / `python/risk_analysis.py`) before a dashboard is worth
building on top of it. What follows is precise enough to build from directly:
data model, every DAX measure, and what each page needs to show and why.

## Data model

A single flat table, `credit_applications`, loaded from
`data/processed/credit_applications_clean.csv`. No star schema: every business
question in this project answers directly off one row per application, and adding a
separate dimension model here would be complexity without a corresponding KPI need
(see `docs/methodology.md`'s consistency principle for the underlying reasoning).

## DAX measures

Every measure below is written to compute the same thing as its Python counterpart
in `python/analysis.py` / `python/risk_analysis.py`. If a number in Power BI ever
disagrees with the Python output, the DAX measure is assumed wrong until proven
otherwise, not the other way around - Python is the source of truth (see
`docs/methodology.md`).

```dax
Total Applications = COUNTROWS(credit_applications)

Decided Applications =
    CALCULATE(COUNTROWS(credit_applications), NOT ISBLANK(credit_applications[decision]))

Approval Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(credit_applications), credit_applications[decision] = "approved"),
        [Decided Applications]
    )

Rejection Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(credit_applications), credit_applications[decision] = "rejected"),
        [Decided Applications]
    )

Withdrawal Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(credit_applications), credit_applications[application_status] = "withdrawn"),
        [Total Applications]
    )

Manual Review Rate = AVERAGE(credit_applications[manual_review])

Avg Processing Time (Hours) = AVERAGE(credit_applications[processing_time_hours])

Median Processing Time (Hours) = MEDIAN(credit_applications[processing_time_hours])

P90 Processing Time (Hours) =
    PERCENTILE.INC(credit_applications[processing_time_hours], 0.9)

Avg Requested Amount = AVERAGE(credit_applications[requested_amount])

Incomplete Application Rate =
    DIVIDE(
        CALCULATE(COUNTROWS(credit_applications), credit_applications[documents_complete] = FALSE),
        [Total Applications]
    )

Avg Verification Errors = AVERAGE(credit_applications[verification_errors])
```

`Decision Path` (used on Page 3 to distinguish manual review from a straight-through
decision, matching `risk_analysis.decision_path_category`):

```dax
Decision Path =
    SWITCH(
        TRUE(),
        credit_applications[manual_review] = TRUE, "Manual Review",
        ISBLANK(credit_applications[decision]), "Withdrawn",
        credit_applications[decision]
    )
```

`DTI Band` (used on Page 3, matching `risk_analysis.dti_band_vs_decision`):

```dax
DTI Band =
    SWITCH(
        TRUE(),
        credit_applications[debt_to_income_ratio] < 0.20, "<0.20",
        credit_applications[debt_to_income_ratio] < 0.35, "0.20-0.35",
        credit_applications[debt_to_income_ratio] < 0.50, "0.35-0.50",
        credit_applications[debt_to_income_ratio] < 0.70, "0.50-0.70",
        "0.70+"
    )
```

## Page 1: Credit Portfolio Overview

**Audience:** Credit Manager, first thing in the morning.

| Visual | Measure(s) | Business question answered |
|---|---|---|
| KPI card | `Total Applications` | How big is the portfolio right now? |
| KPI card | `Approval Rate` | What share of decided applications are approved? |
| KPI card | `Rejection Rate` | What share are rejected? |
| KPI card | `Manual Review Rate` | How much of the portfolio needs a human? |
| KPI card | `Avg Processing Time (Hours)` | How long does a file take on average? |

Filters: date range (`application_date`), channel, customer segment.

## Page 2: Process Performance

**Audience:** Credit Manager and Credit Analysts, for operational monitoring.

| Visual | Measure(s) | Business question answered |
|---|---|---|
| Histogram | `processing_time_hours` distribution | What does the processing time distribution actually look like (not just the average)? |
| Bar chart by channel | `Avg Processing Time (Hours)`, `Median Processing Time (Hours)` | Which channel is slowest? |
| Bar chart, manual vs. automatic | `Median Processing Time (Hours)`, `P90 Processing Time (Hours)`, split by `manual_review` | How much of the delay is specifically attributable to manual review? |
| Bar chart by segment | `Avg Processing Time (Hours)` split by `customer_segment` | Which segment experiences the longest delays? |

## Page 3: Decision & Risk Insights

**Audience:** Credit Manager, Risk Manager, Compliance.

| Visual | Measure(s) | Business question answered |
|---|---|---|
| Bar chart by segment | `Approval Rate`, `Rejection Rate` split by `customer_segment` | Do approval/rejection patterns differ by segment? |
| Bar chart by DTI band | `Approval Rate` split by `DTI Band` | How does affordability relate to approval? |
| Bar chart by decision path | `Total Applications`, `Incomplete Application Rate` split by `Decision Path` | What distinguishes files that need manual review from those decided automatically? |
| Bar chart | `Incomplete Application Rate` split by `channel` | Where does incomplete documentation originate? |

Every visual on this page carries an on-canvas note: *"Shows association within
this dataset, not a causal or regulatory risk assessment."* This is not a
decoration - Compliance is a named stakeholder specifically because this page could
otherwise be misread as a scoring model.

## Recommendations tracker (optional Page 4)

If the dashboard is extended, a simple table view of `requirements.md` (ID,
requirement, priority, status) gives the Credit Manager a way to track whether the
recommendations in `docs/final-report.md` are actually being acted on - the same
pattern used in the companion project's dashboard spec.
