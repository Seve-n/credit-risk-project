# Banking Credit Risk & Decision Process Analysis

**Status:** In progress. Phase 1 (business framing) complete.

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
├── notebooks/              # Exploratory analysis notebook
├── sql/                    # SQLite KPI, processing time, and decision queries
├── dashboard/              # Power BI dashboard specification
└── docs/                   # Assumptions, methodology, final report, interview prep
```

## Current Progress

| Phase | Deliverable | Status |
|---|---|---|
| 1 | Business framing (brief, stakeholders, questions, data requirements, assumptions) | Done |
| 2 | Dataset design | Not started |
| 3 | Synthetic data generation | Not started |
| 4 | Data quality & cleaning | Not started |
| 5 | Exploratory analysis | Not started |
| 6 | SQL analysis | Not started |
| 7 | Credit decision analysis | Not started |
| 8 | Processing time & manual review analysis | Not started |
| 9 | Business insights | Not started |
| 10 | Recommendations | Not started |
| 11 | As-Is / To-Be process | Not started |
| 12 | Requirements | Not started |
| 13 | User stories & acceptance criteria | Not started |
| 14 | Dashboard specification | Not started |
| 15 | Final report & README | Not started |
| 16 | Interview preparation | Not started |

## Technologies

Python (pandas), SQL (SQLite), Power BI (specification only), Git/GitHub.

## Disclaimer

This is a fictional, educational portfolio project. **Chevron Constantine Banking** is
not a real company. All data is synthetically generated. This project is not affiliated
with, and does not use any data, scoring model, or internal process from, Belfius or any
real financial institution.

## License

MIT
