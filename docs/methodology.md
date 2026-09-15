# Methodology

## Workflow

This project follows a Business Analyst workflow end to end, not a straight-to-code
approach:

```text
Business Problem -> Stakeholders -> Business Questions -> Data Requirements
    -> Synthetic Data -> Data Quality -> Analysis (Python, SQL)
    -> Business Insights -> Recommendations -> As-Is / To-Be Process
    -> Functional Requirements -> User Stories -> Dashboard Specification
    -> Final Report
```

Each phase produced a standalone, reviewable deliverable before the next one
started - dataset design was written down before the dataset existed, business
questions were listed before any data requirement was drafted, and so on. The point
is not process for its own sake: it forces every downstream artifact (dataset,
analysis, requirement) to trace back to a specific business question rather than
existing because it seemed useful in the moment.

## Why a synthetic dataset

No real credit application data was used, and none was available for a portfolio
project of this kind - nor would it be appropriate to use real data even if it were
available, given the sensitivity of credit decisioning. A synthetic dataset with
deliberately simulated relationships (documented in `docs/assumptions.md`) lets the
project practice the full analysis workflow - data quality, KPI design, decision
analysis, process mapping - without any of the privacy, regulatory, or
confidentiality issues real credit data would raise.

## Tools

| Tool | Role |
|---|---|
| Python (pandas, numpy) | Data generation, cleaning, and all KPI/analysis logic - the single source of truth |
| SQLite | A second, independently written query layer, used specifically to cross-check the Python KPIs |
| Jupyter | Narrative exploration and visualization, built on top of the Python functions rather than redefining them |
| Power BI (specification only) | Dashboard design, written as DAX measures mirroring the Python KPI definitions |
| Git / GitHub | Version control and public portfolio hosting |

## Consistency principle: one KPI, one definition

Every KPI in this project (approval rate, manual review rate, processing time
percentiles, and so on) is defined exactly once, in `python/analysis.py` or
`python/risk_analysis.py`. The SQL queries in `sql/` and the DAX measures in
`dashboard/README.md` are written to reproduce those definitions, not to define the
KPI independently.

This is not a formality. Actually cross-checking the SQL against Python caught a
real bug while building this project: the first draft of `sql/01_portfolio_kpis.sql`
assumed SQLite would store the `manual_review` and `documents_complete` boolean
columns as the text `'True'`/`'False'`, since that is how pandas writes them to CSV.
`pandas.to_sql()` actually stores them as `INTEGER` `0`/`1`. The query ran without
error and silently returned a 0% manual review rate and a 0% incomplete application
rate - a wrong answer that looked like a real one, not a crash that would have been
obvious. It was only caught because the query was actually run against the database
and compared to the Python output, rather than assumed correct because it was
syntactically valid. Full detail: `sql/README.md`.

This mirrors a lesson from the companion customer-journey project, where the same
cross-check practice caught a `COALESCE(LEAD(...), 0)` bug producing a false 100%
drop-off rate on the last funnel step. Two different bugs, two different projects,
same root cause: an assumption about the data that nobody actually tested against
real output. The practice of cross-checking independently written implementations of
the same KPI is what catches this class of bug - a passing test only proves the
code ran, not that its assumptions about the underlying data were correct.

## Honesty principle

Three things in this project are deliberately left incomplete rather than forced or
hidden:

- **REQ-010** and **US-007** (self-service document correction) are left at
  discovery stage because writing a firm requirement before Compliance and IT weigh
  in on document re-verification would risk specifying something that is not
  actually implementable.
- The non-monotonic approval rate observed in the highest debt-to-income bands
  (Section 5 of the notebook) is reported alongside its small sample size (14-126
  applications) rather than smoothed over or re-binned until it looked cleaner.
- Two small, understood discrepancies between the SQL and Python results (DTI band
  edges, p90 threshold ties) are documented in `sql/README.md` rather than forced
  into an exact match that would have made the code less readable for no analytical
  benefit.

## Non-causal framing

Every finding in `docs/final-report.md` and the exploratory notebook is phrased as
an association observed in this dataset - *associated with*, *related to*, *higher
rate*, *may indicate* - never as a proven cause. This project does not build, and
does not claim to build, a credit scoring or risk model. The dataset is synthetic
and every relationship in it was simulated on purpose (see `docs/assumptions.md`);
finding a simulated relationship confirms the simulation, not a real-world
mechanism.

## Limitations

See `docs/assumptions.md` for the full list of what this dataset cannot support. In
short: no real credit data, no regulatory validation, descriptive analysis rather
than a predictive or causal model, and conclusions that are illustrative of a
Business Analyst workflow rather than production-ready findings for a real bank.
