# Data Requirements

This document maps each business question from
[business-questions.md](business-questions.md) to the data needed to answer it, the
KPI(s) involved, and the analysis method. Its purpose is to make sure the synthetic
dataset (designed in Phase 2) is built to answer these specific questions, rather than
building a generic dataset and hoping it happens to cover them.

| # | Business Question | Data Required | KPI | Analysis Method |
|---|---|---|---|---|
| 1 | Overall approval rate | `decision` | Approval rate | Count of approved / total applications |
| 2 | Overall rejection rate | `decision` | Rejection rate | Count of rejected / total applications |
| 3 | Share of applications in manual review | `manual_review` | Manual review rate | Count of manual review / total applications |
| 4 | Average / median processing time | `processing_time_hours` | Avg. and median processing time | Descriptive statistics |
| 5 | Tail of the processing time distribution (p90) | `processing_time_hours`, application attributes | P90 processing time | Percentile calculation + profile of applications above p90 |
| 6 | Slowest application types | `processing_time_hours`, `channel`, `customer_segment`, `loan_term_months` | Avg. processing time by type | Group-by comparison |
| 7 | Longest process steps | Step-level timestamps or a step-duration breakdown | Avg. duration per step (if step-level data exists) | Group-by comparison across steps |
| 8 | Factors associated with manual review | `manual_review`, `documents_complete`, `verification_errors`, `requested_amount`, `debt_to_income_ratio` | Manual review rate by factor | Group-by comparison + simple association check |
| 9 | Most frequent missing data, and its link to delay | `documents_complete`, missing-value flags, `processing_time_hours` | Incomplete application rate | Frequency count + comparison of processing time with/without missing data |
| 10 | Verification errors vs. processing time | `verification_errors`, `processing_time_hours` | Avg. verification error count | Correlation / grouped comparison |
| 11 | Factors associated with approval vs. rejection | `decision`, `annual_income`, `monthly_expenses`, `debt_to_income_ratio`, `previous_defaults`, `requested_amount` | Approval/rejection rate by factor | Group-by comparison across decision outcome |
| 12 | Previous defaults vs. decision | `previous_defaults`, `decision` | Approval rate by default history | Group-by comparison |
| 13 | Debt-to-income ratio vs. decision | `debt_to_income_ratio`, `decision` | Approval/rejection rate by DTI band | Group-by comparison across DTI bands |
| 14 | Segments/channels with higher manual review | `customer_segment`, `channel`, `manual_review` | Manual review rate by segment/channel | Group-by comparison |
| 15 | Segments/channels with longer processing time | `customer_segment`, `channel`, `processing_time_hours` | Avg. processing time by segment/channel | Group-by comparison |
| 16 | Automation candidates | `manual_review`, `verification_errors`, `documents_complete`, outcome of manual review vs. automated decision | Manual review rate, error rate, outcome agreement rate | Cross-tab of review trigger vs. final decision |
| 17 | Where human judgment is still needed | `manual_review`, `decision_reason`, complexity indicators (`requested_amount`, `debt_to_income_ratio`, `previous_defaults`) | Manual review rate on complex profiles | Group-by comparison on complexity indicators |

## Core fields this implies for the dataset

Reading across the table, every business question can be answered as long as the
dataset captures, at minimum, one row per **credit application**, with:

- **Identifiers:** `application_id`, `customer_id`
- **Application context:** `application_date`, `channel`, `customer_segment`,
  `age_group`, `employment_status`
- **Financial profile:** `annual_income`, `monthly_expenses`, `existing_loans`,
  `requested_amount`, `loan_term_months`, `debt_to_income_ratio`,
  `credit_history_length`, `previous_defaults`
- **Process quality:** `documents_complete`, `verification_errors`
- **Process outcome:** `manual_review`, `processing_time_hours`
- **Decision:** `decision`, `decision_reason`, `application_status`

Every column exists because a business question in this document needs it. If a field
in the eventual dataset cannot be traced back to a row in this table, it should not be
in the dataset, and if a question above cannot be answered with the fields listed, the
dataset design in Phase 2 needs to add one.
