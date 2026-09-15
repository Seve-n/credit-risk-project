# To-Be Process: Credit Decisioning (Post-Recommendations)

Every change below traces back to a specific pain point in `pain-points.md` and
forward to a requirement in `requirements.md`. Nothing here is added because it
sounds good in general; it exists because a number in the analysis pointed at it.

```text
Application
    |
Data Collection  <-- inline validation on income/employment (REQ-002)
    |
Document Verification  <-- real-time completeness check (REQ-001)
    |
Risk Checks  <-- complexity triage (REQ-004), default-history flag (REQ-006)
    |
    +-- Straight-Through Processing --------+
    |     (complete docs, low complexity)    |
    |            |                            |
    |         Decision                        |
    |        (auto approve/reject)            |
    |                                         |
    +-- Human Review Path -------------------+
          (incomplete docs, high DTI,
           prior default, large amount,
           or pre-screen score below
           confidence threshold)
              |
        Pre-Screen Recommendation (REQ-005)
              |
        Analyst Decision
              |
        Status Visibility + Wait Estimate (REQ-003)
              |
        SLA Alert if stuck (REQ-009)
              |
    Decision + Audit Log (REQ-008)
```

## What changes, and why

### Straight-through processing (STP)

Applications with complete documentation, no previous default, and a debt-to-income
ratio and requested amount inside normal ranges continue straight to an automated
decision, exactly as today. Nothing changes here: the analysis found no evidence
this path is a problem (median processing time 20.9 hours), so the recommendation is
to leave it alone rather than "optimize" a step that is not the bottleneck.

### Document Verification becomes a gate, not just a check

**Change:** real-time validation flags missing or invalid documents to the customer
at the point of upload, on every channel, especially the digital ones where the
incomplete-application rate is highest today.

**Traceability:** pain point 3 (incomplete documentation as the strongest single
signal in the dataset) -> REQ-001.

### Risk Checks route by complexity, not just pass/fail

**Change:** files are explicitly triaged into "low complexity, needs a light-touch
review" versus "genuinely complex, needs full manual review," using the same
signals already shown to matter (documents_complete, previous_defaults,
debt-to-income ratio, requested amount).

**Traceability:** pain point 1 (manual review as the dominant driver of delay) and
pain point 4 (manual review scales with loan size, as intended) -> REQ-004.

### Manual review keeps the human, adds a recommendation

**Change:** for files entering manual review, a pre-screen recommendation is shown
to the analyst alongside the file (not instead of the analyst's judgment). This does
not remove the human decision. It gives the analyst a documented starting point,
similar in spirit to how the automated path already decides low-complexity files.

**Traceability:** pain point 1 -> REQ-005. This is explicitly a **decision-support
opportunity**, not an automation-replaces-human change: 13% of manually reviewed
files are still rejected, which is evidence the human step is catching real cases a
purely automated rule should not swallow.

### The withdrawal problem gets addressed directly

**Change:** customers in manual review see a status indicator and an estimated wait
time, and files stuck beyond an SLA threshold trigger an internal alert rather than
sitting silently in a queue.

**Traceability:** pain point 2 (14% withdrawal rate during manual review) -> REQ-003
and REQ-009. This targets the process cost (uncertainty during the wait), not the
underlying risk decision.

### Compliance gets an explicit, always-on requirement

**Change:** every decision, automated or manual, is logged with its reason in a
form Compliance can audit.

**Traceability:** stakeholder need from `stakeholders.md` (Compliance) -> REQ-008.
This one is not derived from a specific analysis finding; it is a standing
regulatory-hygiene requirement that does not depend on what the data showed.

## What is deliberately left out

A self-service flow letting a customer correct an incomplete document themselves,
without a full manual review restart, would plausibly help with pain point 3
further. It is not included in this to-be process: it raises security and
verification questions (how do you re-verify a corrected document without
re-running the full check?) that are outside the scope of this analysis. It is
tracked as REQ-010 at discovery stage rather than force-designed here.
