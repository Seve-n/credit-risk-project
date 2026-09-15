# Banking Credit Risk & Decision Process Analysis

**Status:** Complete. All 16 phases delivered, from business framing to interview
preparation.

A Business Analyst case study simulating a credit process efficiency investigation for
**Chevron Constantine Banking**, a fictional bank, built as a portfolio project for a
Business Analyst alternance application. This project is the second in a two-part
portfolio: the first project ([banking-customer-journey-analysis](https://github.com/Seve-n/Chevron-Constantine-banking-))
looks at digital customer journeys, and this one looks at the credit decision process,
a domain closer to risk, compliance, and decision support.

## Business Problem

Chevron Constantine Banking's credit department does not have a clear, data-backed view
of what drives processing delays, which applications require manual review, and where
the process could be made more efficient without weakening the controls it relies on.
This project investigates the problem end-to-end using a synthetic dataset and produces
concrete, evidence-based recommendations.

Full framing: [business-analysis/project-brief.md](business-analysis/project-brief.md)

## Start here

- **Full findings:** [docs/final-report.md](docs/final-report.md), 6 insights with
  evidence, interpretation, a recommendation, and a KPI to monitor, plus the
  prioritized recommendations roadmap and the automation-opportunity matrix.
- **How this was built:** [docs/methodology.md](docs/methodology.md), including a
  real bug the Python/SQL cross-check caught.
- **Skills demonstrated, with evidence:** [docs/skills.md](docs/skills.md).

## Key Findings

- Manual review affects 15.5% of applications but is associated with a **~4.5x
  increase in median processing time** (94.4h vs. 20.9h).
- Of applications reaching manual review, **14% end in the customer withdrawing**
  before any decision - a process cost, not a risk outcome.
- **Document completeness at intake** is the single most consistent signal across
  manual review rate, processing time, and approval rate.
- A history of previous defaults drops approval rate sharply (91% to 68%), but does
  not scale further with additional defaults in this dataset.

Full detail and recommendations: [docs/final-report.md](docs/final-report.md).

## Methodology

This project follows a Business Analyst workflow, not a straight-to-code approach:

```text
Business Problem → Stakeholders → Business Questions → Data Requirements
    → Synthetic Data → Data Quality → Analysis (Python, SQL)
    → Business Insights → Recommendations → As-Is / To-Be Process
    → Functional Requirements → User Stories → Dashboard Specification
    → Final Report
```

Work is done in phases, each producing a reviewable, standalone deliverable, and each
phase is reviewed before moving to the next.

## Project Structure

```text
banking-credit-risk-analysis/
│
├── business-analysis/    # Business framing: brief, stakeholders, questions,
│                          # data requirements, as-is/to-be process, requirements,
│                          # user stories
├── data/                  # raw/ and processed/ synthetic datasets
├── python/                # Data generation, cleaning, and analysis scripts
├── notebooks/              # Executed exploratory analysis notebook
├── sql/                    # SQLite KPI, processing time, and decision queries
├── dashboard/              # Power BI dashboard specification
└── docs/                   # Assumptions, methodology, final report, skills summary
```

> **Note on `docs/interview-preparation.md`:** it exists locally (see
> `business-analysis/user-stories.md`-style personal rehearsal notes) but is
> gitignored rather than published, since a recruiter is better served by the
> finished deliverables above than by rehearsed talking points.

## Current Progress

| Phase | Deliverable | Status |
|---|---|---|
| 1 | Business framing (brief, stakeholders, questions, data requirements, assumptions) | Done |
| 2 | Dataset design | Done |
| 3 | Synthetic data generation | Done |
| 4 | Data quality & cleaning | Done |
| 5 | Exploratory analysis (notebook) | Done |
| 6 | SQL analysis | Done |
| 7 | Credit decision analysis | Done |
| 8 | Processing time & manual review analysis | Done |
| 9 | Business insights | Done |
| 10 | Recommendations | in-progress |
| 11 | As-Is / To-Be process | in-progress|
| 12 | Requirements | in-progress|
| 13 | User stories & acceptance criteria | in-progress|
| 14 | Dashboard specification |in-progress|
| 15 | Final report & README | in-progress|


## Technologies

Python (pandas, numpy), SQL (SQLite), Power BI (specification only; see
[dashboard/README.md](dashboard/README.md) for why), Jupyter, Git/GitHub.

## How to Run

```bash
pip install -r requirements.txt
python python/data_generation.py   # writes data/raw/credit_applications_raw.csv
python python/data_cleaning.py     # writes data/processed/credit_applications_clean.csv
python python/analysis.py          # portfolio KPIs, processing time, manual review
python python/risk_analysis.py     # decision analysis
```

SQL queries in `sql/` need a local SQLite database built from the cleaned CSV; see
[sql/README.md](sql/README.md) for the exact command.

## Business Analyst Skills Demonstrated

- **Stakeholder analysis:** [business-analysis/stakeholders.md](business-analysis/stakeholders.md)
- **Requirements engineering:** [business-analysis/requirements.md](business-analysis/requirements.md),
  10 requirements, MoSCoW-prioritized, one (REQ-010) deliberately left at discovery
  stage rather than forced
- **Process mapping (As-Is / To-Be):** [as-is-process.md](business-analysis/as-is-process.md) /
  [to-be-process.md](business-analysis/to-be-process.md), every to-be change traced
  back to a specific pain point and requirement
- **Root-cause / pain point analysis:** [business-analysis/pain-points.md](business-analysis/pain-points.md),
  every pain point tied to a specific measured number
- **Data analysis (Python, SQL):** KPI design, decision analysis, processing time
  and manual review deep dives, cross-checked between Python and SQL
- **KPI design & governance:** one set of KPI definitions reused consistently
  across Python, SQL, and the dashboard spec (see [docs/methodology.md](docs/methodology.md))
- **User stories & acceptance criteria:** [business-analysis/user-stories.md](business-analysis/user-stories.md),
  including a story (US-007) intentionally left without acceptance criteria
  pending discovery
- **Business recommendations & prioritization:** impact/effort roadmap and an
  automation-opportunity matrix in [docs/final-report.md](docs/final-report.md)
- **Dashboard specification:** [dashboard/README.md](dashboard/README.md)

## Disclaimer

This is a fictional, educational portfolio project. **Chevron Constantine Banking** is
not a real company. All data is synthetically generated. This project is not affiliated
with, and does not use any data, scoring model, or internal process from, Belfius or any
real financial institution.

## License

[MIT](LICENSE)
