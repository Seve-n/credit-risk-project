# Skills Matrix

A quick-reference mapping from claimed skill to concrete evidence in this
repository, for tailoring a CV bullet or answering "can you give me an example of
X" without reconstructing the project from memory.

## Business Analysis skills

| Skill | Evidence | File |
|---|---|---|
| Stakeholder analysis | 9 stakeholders identified (Credit Manager, Credit Analyst, Risk Manager, BA, PO, IT, Data Analyst, Compliance, Customer Service), each with a distinct information need feeding later design decisions | [business-analysis/stakeholders.md](../business-analysis/stakeholders.md) |
| Business problem framing | Problem and explicit in/out-of-scope boundaries written before any data existed | [business-analysis/project-brief.md](../business-analysis/project-brief.md) |
| Business questions -> data requirements | 17 business questions, each mapped to the specific data field(s) and analysis method needed to answer it | [business-analysis/business-questions.md](../business-analysis/business-questions.md), [business-analysis/data-requirements.md](../business-analysis/data-requirements.md) |
| Process mapping (As-Is) | 7-step process, each step tied to a measured pain point rather than a generic template | [business-analysis/as-is-process.md](../business-analysis/as-is-process.md) |
| Root-cause / pain point analysis | 6 pain points, each traced to a specific number in the analysis, not asserted | [business-analysis/pain-points.md](../business-analysis/pain-points.md) |
| Process mapping (To-Be) | Redesigned process distinguishing straight-through processing from human review, every change traced to a pain point and a requirement | [business-analysis/to-be-process.md](../business-analysis/to-be-process.md) |
| Requirements engineering | 10 functional requirements, MoSCoW-prioritized with explicit rationale, one intentionally left at discovery stage (REQ-010) | [business-analysis/requirements.md](../business-analysis/requirements.md) |
| User stories & acceptance criteria | Given/When/Then criteria for 6 stories; 1 story (US-007) left without criteria to mirror its requirement's discovery status | [business-analysis/user-stories.md](../business-analysis/user-stories.md) |
| Prioritization (impact/effort) | 8 actions scored independently on an impact/effort roadmap, with a compliance baseline explicitly excluded from the ranking | [docs/final-report.md](final-report.md#10-recommendations-roadmap-impact-vs-effort) |
| Automation vs. control judgment | Automation-opportunity matrix that explicitly marks the manual review decision itself as a poor automation candidate, with the evidence for why | [docs/final-report.md](final-report.md#13-automation-opportunities) |
| Non-causal, hedged interpretation | Every insight distinguishes association from proven cause; a non-monotonic finding is reported with its small sample size rather than hidden | [docs/final-report.md](final-report.md#9-key-insights) |
| Dashboard specification | Audience-per-page design, DAX measures traced 1:1 to Python KPI functions | [dashboard/README.md](../dashboard/README.md) |

## Technical skills

| Skill | Evidence | File |
|---|---|---|
| Python / pandas / numpy | Data generation (20,080 applications, reproducible via seed), cleaning, and 20+ reusable KPI/analysis functions across two modules | [python/data_generation.py](../python/data_generation.py), [python/analysis.py](../python/analysis.py), [python/risk_analysis.py](../python/risk_analysis.py) |
| Data cleaning & quality | 3 distinct missing-value strategies (structural null, imputation, explicit recoding), 80 duplicates removed, 5 business rules enforced with violations counted rather than silently fixed | [python/data_cleaning.py](../python/data_cleaning.py) |
| SQL | 4 independent SQLite query files (KPIs, processing time, decisions, manual review), cross-verified row by row against Python output | [sql/](../sql/) |
| Debugging / root-cause analysis | 2 documented bugs found and fixed during this project alone: an imputation-order edge case in cleaning, and a SQLite boolean-typing assumption that silently zeroed two KPIs | [docs/methodology.md](methodology.md#consistency-principle-one-kpi-one-definition) |
| KPI design & governance | Single KPI definitions reused (not re-derived) across Python, SQL, and the dashboard spec; two small, understood cross-check discrepancies documented rather than forced to match | [sql/README.md](../sql/README.md) |
| Reproducible analysis | Jupyter notebook built entirely on the same functions as the report, actually executed (not a static shell) via `nbconvert` | [notebooks/01_credit_risk_exploration.ipynb](../notebooks/01_credit_risk_exploration.ipynb) |
| Version control (Git/GitHub) | Full project history; `.gitignore` decisions documented (why the CSV is committed, why the SQLite DB is not) | [sql/README.md](../sql/README.md) |

## Soft skills demonstrated through project decisions

| Skill | Where it shows up |
|---|---|
| Intellectual honesty over completeness | REQ-010/US-007 left at discovery stage; a non-monotonic small-sample finding reported instead of re-binned away; two SQL/Python discrepancies documented instead of forced to match |
| Communicating trade-offs, not just answers | The automation-opportunity matrix explicitly argues *against* automating the one step where the evidence says a human still changes outcomes |
| Learning from your own mistakes | Two bug retrospectives written as reasoning, not just fixes: an imputation order bug and a SQLite type-assumption bug, both caught by actually running the code against real output rather than trusting it |
| Working across two related but distinct portfolio projects | This project deliberately reuses the naming conventions, cleaning philosophy, and cross-check discipline of [the companion customer-journey project](https://github.com/Seve-n/Chevron-Constantine-banking-) while covering a different business domain (credit/risk vs. digital/UX) |
