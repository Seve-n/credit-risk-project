# Stakeholders

This document lists the people and functions with a direct stake in how Chevron
Constantine Banking's credit process performs, what they each care about, and what they
would need from this analysis. It shapes later decisions: which KPIs to report, how to
structure the dashboard, and which recommendations to prioritize.

## Credit Manager

- **Role:** owns the overall performance of the credit department (throughput, SLAs,
  team workload).
- **Objectives:** reduce processing time and manual workload without increasing risk
  exposure.
- **Information sought:** where time is lost in the process, which segments or channels
  are slowest, how much manual review actually costs in time.
- **Pain points:** unpredictable processing times, team overload, no clear diagnosis of
  root causes.
- **Influence:** high. Sponsors process changes and resourcing decisions.
- **Potential needs:** a KPI dashboard, a ranked list of improvement opportunities.

## Credit Analyst

- **Role:** reviews individual credit files, in particular the ones flagged for manual
  review.
- **Objectives:** process files efficiently while catching the cases that genuinely need
  human judgment.
- **Information sought:** which files are routed to them and why, what makes a file
  complex.
- **Pain points:** repetitive verification work on files that did not need to reach
  manual review, incomplete files arriving without enough context.
- **Influence:** medium. Day-to-day process knowledge, limited decision authority.
- **Potential needs:** clearer routing rules, better visibility into why a file was
  flagged.

## Risk Manager

- **Role:** owns the risk appetite and the control framework the credit process must
  respect.
- **Objectives:** keep default and exposure risk under control while the process gets
  faster.
- **Information sought:** whether proposed efficiency gains touch any control that
  exists for risk reasons, and what the actual decision profile of the portfolio looks
  like.
- **Pain points:** improvement initiatives proposed without risk being consulted early.
- **Influence:** high. Can block or reshape any recommendation that reduces controls.
- **Potential needs:** explicit callouts of which steps are safe to automate versus
  which exist specifically for risk control.

## Business Analyst

- **Role:** conducts this analysis; translates business questions into data
  requirements, findings, and requirements.
- **Objectives:** produce an evidence-based, defensible set of insights and
  recommendations.
- **Information sought:** all of the above, structured and cross-checked.
- **Pain points:** ambiguous or conflicting stakeholder priorities, data that does not
  actually answer the business question it was collected for.
- **Influence:** medium. Shapes the analysis and the requirements, but does not decide
  resourcing.
- **Potential needs:** access to a realistic dataset, a documented methodology.

## Product Owner

- **Role:** owns the backlog for any tooling that supports the credit process
  (internal case management, dashboards, etc.).
- **Objectives:** turn validated requirements into a prioritized, buildable backlog.
- **Information sought:** which requirements are Must Have versus Should Have, which
  user stories are ready for development versus still at discovery stage.
- **Pain points:** requirements handed over without a clear acceptance criteria or
  priority.
- **Influence:** medium to high. Decides what actually gets built and in what order.
- **Potential needs:** a MoSCoW-prioritized requirements list and user stories with
  acceptance criteria.

## IT / Application Team

- **Role:** builds and maintains the systems that support the credit process.
- **Objectives:** implement functional requirements without introducing regressions or
  unnecessary complexity.
- **Information sought:** precise, testable requirements; which systems and data are
  involved at each process step.
- **Pain points:** vague requirements, late discovery of technical constraints.
- **Influence:** medium to high. Feasibility often gates what is actually deliverable.
- **Potential needs:** requirements written with enough technical precision to be
  estimated and built.

## Data Analyst

- **Role:** maintains the data feeding the credit process and its reporting.
- **Objectives:** ensure the data used for analysis and decisions is accurate and
  complete.
- **Information sought:** where data quality issues originate, which fields are
  unreliable.
- **Pain points:** downstream teams distrusting the data, or building on top of known
  data quality issues without them being documented.
- **Influence:** medium. Shapes what data is trustworthy enough to act on.
- **Potential needs:** a documented data quality assessment.

## Compliance

- **Role:** ensures the credit process respects internal policy and external
  regulatory obligations.
- **Objectives:** confirm that efficiency improvements do not create regulatory or
  fair-lending exposure.
- **Information sought:** whether any proposed change affects a control required for
  compliance, and whether the analysis draws conclusions it should not (e.g. treating
  correlation as causation in a way that could look like an informal scoring rule).
- **Pain points:** being brought in after decisions are already made rather than during
  the analysis.
- **Influence:** high on anything touching risk controls or customer treatment.
- **Potential needs:** explicit, hedged language in findings; a clear limitations
  section.

## Customer Service

- **Role:** handles customer questions about application status and outcomes.
- **Objectives:** give customers accurate, timely answers about where their file
  stands.
- **Information sought:** typical processing times by application type, common reasons
  for delay, so they can set expectations correctly.
- **Pain points:** customers asking about delays that the team cannot explain because
  there is no visibility into where a file actually sits in the process.
- **Influence:** low to medium. Does not shape the process but is affected by its
  transparency.
- **Potential needs:** clear, communicable processing time expectations by segment.

## Stakeholder matrix

| Stakeholder | Interest | Influence | Main Need |
|---|---|---|---|
| Credit Manager | High | High | Diagnosis of delay causes, KPI dashboard |
| Credit Analyst | High | Medium | Better routing, less repetitive review work |
| Risk Manager | High | High | Confirmation that efficiency does not weaken control |
| Business Analyst | High | Medium | Reliable data and a defensible methodology |
| Product Owner | Medium | Medium-High | Prioritized, testable requirements |
| IT / Application Team | Medium | Medium-High | Precise, buildable requirements |
| Data Analyst | Medium | Medium | Documented data quality findings |
| Compliance | Medium | High (on risk-related items) | Hedged conclusions, explicit limitations |
| Customer Service | Low-Medium | Low-Medium | Realistic processing time expectations |
