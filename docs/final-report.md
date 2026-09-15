# Final Report: Banking Credit Risk & Decision Process Analysis

## 1. Executive Summary

Chevron Constantine Banking's credit department asked for a clear, evidence-based
view of what drives processing delays and where the process could be made more
efficient without weakening its risk controls. Across ~20,000 synthetic credit
applications, the analysis found that delay is concentrated almost entirely in one
place: manual review, which affects 15.5% of applications but takes roughly 4.5
times longer than the automated path (median 94.4 vs. 20.9 hours) and is associated
with a 14% withdrawal rate - customers leaving the process before any decision is
reached. Document completeness at intake is the single most consistent signal behind
manual review, processing time, and approval rate alike. Six recommendations follow
directly from these findings, prioritized by impact and effort, none of which
propose removing the human decision-maker from credit review.

## 2. Business Context

Full framing: [business-analysis/project-brief.md](../business-analysis/project-brief.md).
In short: the credit department observes variable processing times, a share of
applications in manual review, incomplete information, and process errors, without a
precise, data-backed view of why. This report investigates the "why" and turns it
into recommendations.

## 3. Methodology

Full detail: [docs/methodology.md](methodology.md). In short: a synthetic dataset
with deliberately simulated relationships, analyzed in Python (the single source of
truth for every KPI), cross-checked against independently written SQL queries, and
explored narratively in a Jupyter notebook. Every finding below is an association
observed in this dataset, not a proven cause, and this project is not a credit
scoring model.

## 4. Data Quality

Full detail: [python/data_cleaning.py](../python/data_cleaning.py). In short: of
20,080 generated applications, 100 were removed (80 exact duplicates, 20
business-rule violations), 300 had `annual_income` imputed from the median for their
employment status, and 200 had a missing `employment_status` recoded to an explicit
`"unknown"` category. `decision` is missing for the 587 withdrawn applications by
design, not as a data defect.

## 5. KPI Analysis

| KPI | Value |
|---|---|
| Total applications (post-cleaning) | 19,980 |
| Approval rate (of decided applications) | 89.4% |
| Rejection rate (of decided applications) | 10.6% |
| Withdrawal rate | 2.9% |
| Manual review rate | 15.5% |
| Median processing time | 22.6 hours |
| P90 processing time | 85.5 hours |
| Average requested amount | ~52,800 |
| Incomplete application rate | 15.9% |
| Average verification errors | 0.63 |

Full breakdowns by channel, segment, loan size, and decision: `python/analysis.py`,
`sql/01_portfolio_kpis.sql`, and Section 4 of the notebook.

## 6. Process Analysis

Full detail: [business-analysis/as-is-process.md](../business-analysis/as-is-process.md).
The process has seven steps; processing time is overwhelmingly concentrated at the
Decision step when a file requires manual review (median 94.4h vs. 20.9h for the
automated path), not distributed evenly across the process.

## 7. Decision Analysis

Full detail: `python/risk_analysis.py`, Section 5 of the notebook. Approval rate
declines with debt-to-income ratio (92% under 0.20 to 78% at 0.35-0.50), drops
sharply with any previous default (91% to 68%, without scaling further for
additional defaults), and is lowest for applications where the requested amount is
large relative to income (75% approval when income is under 0.5x the requested
amount).

## 8. Manual Review Analysis

Full detail: `python/analysis.py`, Section 7 of the notebook. Manual review rate is
roughly double for small business and retail affluent customers (~22%) compared to
retail mass (~12%), and rises from 11% to 29% as requested loan amount increases. Of
applications reaching manual review, 73% are approved, 13% rejected, and 14%
withdrawn.

## 9. Key Insights

### Insight 1: Manual review is the dominant driver of processing time

**Evidence:** median processing time is 94.4 hours for manually reviewed
applications versus 20.9 hours for automatically decided ones - a ~4.5x difference,
widening further at the tail (p90: 130.3h vs. 34.7h).

**Interpretation:** manual review is associated with the largest measured effect on
processing time in this analysis, larger than any channel or segment difference.

**Business impact:** a 15.5%-of-portfolio process step accounts for a
disproportionate share of total processing time and, very plausibly, of customer
frustration with the process.

**Recommendation:** reduce how many files unnecessarily reach manual review
(document completeness, complexity triage) rather than trying to shorten the manual
review step itself.

**KPI to monitor:** manual review rate, median/P90 processing time by
`manual_review`.

### Insight 2: Manual review generates a real withdrawal cost

**Evidence:** 14% of applications reaching manual review end in the customer
withdrawing before any decision, versus 73% approved and 13% rejected.

**Interpretation:** withdrawal during manual review is a process cost, not a risk
outcome - these customers were not told no, they stopped waiting for an answer.

**Business impact:** the bank may be losing viable customers specifically because of
process uncertainty, independent of their actual creditworthiness.

**Recommendation:** give customers a status indicator and estimated wait time during
manual review (REQ-003), and alert internally when a file exceeds an SLA threshold
(REQ-009).

**KPI to monitor:** withdrawal rate during manual review.

### Insight 3: Document completeness is the strongest cross-cutting signal

**Evidence:** incomplete applications make up 47% of the manually reviewed
population versus 9% of automatically approved applications, and show a lower
approval rate (80% vs. 91%). Fully digital channels show a higher incomplete-rate
than in-person channels.

**Interpretation:** document completeness at intake is associated with manual
review rate, processing time, and approval rate simultaneously - a single factor
touching three different KPIs.

**Business impact:** it is also the most tractable factor to influence at the
source, compared to income or credit history.

**Recommendation:** real-time document completeness validation at upload, on every
channel, prioritizing digital channels where the gap is largest (REQ-001).

**KPI to monitor:** incomplete application rate, by channel.

### Insight 4: Manual review scales with loan size, as a control should

**Evidence:** manual review rate rises from ~11% for loans under 25k to ~29% for
loans of 100k or more, and average processing time follows the same shape.

**Interpretation:** this pattern is consistent with the control working as
intended - larger, higher-exposure loans receive more scrutiny - rather than a
process defect.

**Business impact:** any automation proposal here needs to explicitly preserve this
scaling rather than flatten it; the finding is included specifically so a future
"speed up manual review" initiative does not accidentally reduce scrutiny where it
is doing its job.

**Recommendation:** triage files by complexity within manual review rather than by
loan size alone, so simple large-loan files and complex small-loan files are both
routed appropriately (REQ-004).

**KPI to monitor:** manual review rate by loan size band.

### Insight 5: Previous defaults show a threshold effect, not a scaling effect

**Evidence:** approval rate drops from 91% (no previous defaults) to 68% (one
previous default), but a second or third default does not push the rate meaningfully
lower in this dataset.

**Interpretation:** the decision logic (automated or manual) appears to treat "any
default on record" as the meaningful signal, rather than weighing the count of
defaults - worth confirming explicitly with Risk if this pattern held in a real
portfolio, since it is a modeling choice with real consequences either way.

**Business impact:** if unintentional, this could mean the process is not
differentiating between a customer with one old default and one with a pattern of
repeated defaults.

**Recommendation:** surface default history (count and recency, not just presence)
clearly to the analyst during manual review (REQ-006).

**KPI to monitor:** approval rate by previous defaults count.

### Insight 6: Missing data is concentrated in two fields

**Evidence:** before cleaning, `annual_income` (300 applications) and
`employment_status` (200 applications) accounted for essentially all of the
non-trivial missing-value cases; every other field was effectively complete.

**Interpretation:** the missing-data problem is narrow, not broad - a targeted fix
at intake would likely resolve most of it.

**Business impact:** a "improve data quality" initiative can be scoped precisely
instead of open-ended.

**Recommendation:** enforce these two fields as mandatory with inline validation at
data collection (REQ-002).

**KPI to monitor:** missing-value rate for `annual_income` and `employment_status`.

## 10. Recommendations Roadmap (Impact vs. Effort)

Impact is scored against how large and well-evidenced the underlying finding is;
effort against implementation complexity (new validation logic and UI vs. a new
scoring/triage system). REQ-008 (compliance audit log) is excluded from this
impact/effort ranking on purpose: it is a standing regulatory baseline, not an
optimization choice to prioritize against the others.

| Action | Requirement | Impact | Effort | Priority |
|---|---|---|---|---|
| A. Customer status + wait estimate during manual review | REQ-003 | High | Low | 1 (quick win) |
| B. Mandatory field validation (income, employment) | REQ-002 | Medium | Low | 2 (quick win) |
| C. Real-time document completeness validation | REQ-001 | High | Medium | 3 |
| D. Complexity-based triage for manual review | REQ-004 | Medium | Medium | 4 |
| E. KPI dashboard by channel/segment | REQ-007 | Medium | Medium | 5 |
| F. Default-history detail on the review screen | REQ-006 | Low-Medium | Low | 6 |
| G. Pre-screen recommendation for analysts | REQ-005 | Medium | High | 7 |
| H. SLA alerting for stuck files | REQ-009 | Low | Low | 8 |
| — Investigate further: self-service document correction | REQ-010 | Unknown | Unknown | Not scoped - needs discovery |

Actions A and B are listed first because they are both low-effort and target the
two findings with the clearest, most direct evidence (withdrawal during review, and
the two fields responsible for nearly all missing data). Action C carries the
highest evidenced impact but medium effort, since real-time validation touches every
intake channel.

## 11. To-Be Process

Full detail: [business-analysis/to-be-process.md](../business-analysis/to-be-process.md).
Straight-through processing is left unchanged (no evidence it is a problem); the
changes concentrate on Document Verification, Risk Checks triage, and the manual
review experience itself.

## 12. Functional Requirements

Full detail: [business-analysis/requirements.md](../business-analysis/requirements.md)
(10 requirements, MoSCoW-prioritized) and
[business-analysis/user-stories.md](../business-analysis/user-stories.md) (7 user
stories with Given/When/Then acceptance criteria).

## 13. Automation Opportunities

| Process Step | Current State | Automation Potential | Risk | Recommendation |
|---|---|---|---|---|
| Document Verification | Manual spot-check after submission | High | Low | Real-time validation at intake (REQ-001) |
| Data Collection (mandatory fields) | Not enforced | High | Low | Inline validation (REQ-002) |
| Risk Checks routing | Single queue, no complexity split | Medium | Low-Medium | Complexity-based triage (REQ-004) |
| Manual review decision itself | Fully human | Low, by design | High if automated away | Decision-support recommendation only, not automated approval (REQ-005) - 13% of reviewed files are still rejected, evidence the human step catches real cases |
| Status communication during review | None | High | Low | Status + wait estimate (REQ-003) |
| Decision communication | Already automated | N/A | N/A | No change recommended |

The manual review decision itself is explicitly marked **not** a good automation
candidate: it is where the analysis found the human step still changes outcomes
(13% rejected, 14% withdrawn are not "automation would have approved these anyway"
numbers). Every automation recommendation in this report targets what happens
*before* or *around* that decision, not the decision itself.

## 14. Limitations

- All data is synthetic; no real applicant, transaction, or decision is represented.
- Every relationship in the dataset was deliberately simulated (see
  `docs/assumptions.md`); finding it in the analysis confirms the simulation, not a
  real-world mechanism.
- This project does not constitute, and was not informed by, any real credit scoring
  model or the internal process of any real bank, including Belfius.
- All findings describe association, not causation. Language throughout uses
  *associated with*, *related to*, *may indicate* rather than *causes*.
- No regulatory or compliance validation has been performed on any recommendation.
- Small-sample bands (e.g. the two highest debt-to-income bands, 14 and 126
  applications respectively) are reported with their sample size rather than treated
  as reliable trends.
- This project is a Business Analyst case study, not a production-ready proposal.

## 15. Next Steps

1. Validate the "any default vs. default count" finding (Insight 5) with Risk before
   assuming it reflects intended policy.
2. Prototype the two quick wins (Actions A and B) first, since they are both
   low-effort and target well-evidenced findings.
3. Take REQ-010 (self-service document correction) to Compliance and IT for a
   discovery conversation before writing a firm requirement.
4. If this were a real initiative, replace the synthetic dataset with real
   (anonymized, governed) data before drawing any operational conclusion.
