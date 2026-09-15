# Functional Requirements

Each requirement traces back to a pain point in `pain-points.md` and forward to the
`to-be-process.md` change it supports. Priority uses MoSCoW; the rationale column
explains why a requirement landed where it did, since "Must Have" should mean
something more specific than "seems important."

| ID | Requirement | Priority | Business Value | Stakeholder |
|---|---|---|---|---|
| REQ-001 | Validate document completeness in real time at upload, on every channel | Must | Targets the single strongest signal in the analysis (incomplete docs -> manual review, longer time, lower approval) | Customer, Credit Analyst |
| REQ-002 | Enforce mandatory fields (`annual_income`, `employment_status`) with inline validation at data collection | Must | These two fields account for nearly all missing-data cases found | Data Analyst, Credit Analyst |
| REQ-003 | Show the customer a status indicator and estimated wait time during manual review | Must | Directly targets the 14% withdrawal rate during manual review | Customer, Customer Service |
| REQ-004 | Triage files entering Risk Checks into low-complexity vs. full-complexity manual review | Should | Manual review is the dominant driver of delay; not every reviewed file needs the same depth of review | Credit Analyst, Credit Manager |
| REQ-005 | Show a pre-screen recommendation to the analyst for files in manual review | Should | Decision-support, not automation-replaces-human: gives analysts a documented starting point without removing judgment | Credit Analyst |
| REQ-006 | Surface previous-default history clearly to the analyst at the start of manual review | Should | Previous defaults show the largest single effect on approval rate found in the decision analysis | Credit Analyst, Risk Manager |
| REQ-007 | Provide a KPI dashboard (processing time, manual review rate, approval rate) by channel and segment | Should | Needed for the Credit Manager to monitor whether any of the above changes actually work | Credit Manager |
| REQ-008 | Log the reason for every decision, automated or manual, in an auditable format | Must | Standing regulatory/compliance requirement, independent of any specific finding | Compliance |
| REQ-009 | Alert internally when a file exceeds an SLA threshold in manual review | Could | Reduces the chance a file silently sits until the customer withdraws, but is a safety net rather than a root-cause fix | Credit Manager, Credit Analyst |
| REQ-010 | Self-service correction/resubmission of a flagged document without a full manual review restart | Won't (this phase) | Needs discovery: raises document re-verification and security questions outside this analysis's scope | Customer, IT / Application Team |

## Why each priority

- **Must Have (REQ-001, REQ-002, REQ-003, REQ-008):** REQ-001 through REQ-003
  target the three findings with the largest measured effect (document
  completeness, missing data, and withdrawal during review). REQ-008 is a
  compliance baseline that does not depend on what the analysis found - it would be
  a Must regardless.
- **Should Have (REQ-004, REQ-005, REQ-006, REQ-007):** these improve the process
  meaningfully but depend on REQ-001-003 landing first (there is limited point
  triaging complexity or building a KPI dashboard before the upstream data quality
  problem is addressed).
- **Could Have (REQ-009):** useful, but it is a safety net for a problem REQ-003
  should already reduce - lower priority than fixing the cause.
- **Won't Have this phase (REQ-010):** the only requirement deliberately left at
  discovery stage rather than force-scoped, because writing a firm requirement
  before Compliance and IT weigh in on document re-verification would risk
  specifying a solution that is not actually implementable.
