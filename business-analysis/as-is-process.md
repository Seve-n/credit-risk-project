# As-Is Process

This maps the credit application process as it exists today, adapted to what the
dataset actually shows rather than a generic textbook flow. It is the baseline
`to-be-process.md` will change against.

```text
Application
    |
Data Collection
    |
Document Verification
    |
Risk Checks
    |
Decision
   /    \
Approve  Reject
   \
    Manual Review (if triggered)
       /    |    \
  Approve Reject Withdraw
```

## 1. Application

- **Actor:** Customer, via one of five channels (online, mobile app, branch, broker,
  phone).
- **Input:** Customer identity, requested amount, loan term, stated purpose.
- **Output:** An application record (`application_id`) with a timestamp.
- **Decision:** None at this step.
- **Pain point:** None observed here directly, but the channel chosen at this step
  strongly predicts what happens downstream (see Data Collection).
- **System interaction:** Application intake system creates the record.

## 2. Data Collection

- **Actor:** Customer (self-service on digital channels) or Credit Analyst
  (branch/broker/phone).
- **Input:** Income, expenses, employment status, existing loans, credit history.
- **Output:** A populated applicant profile.
- **Decision:** None at this step, but data quality here determines everything
  downstream.
- **Pain point:** `employment_status` and `annual_income` are the two fields most
  often missing at this stage (200 and 300 applications respectively out of ~20,000,
  before cleaning).
- **System interaction:** Application intake system stores the profile.

## 3. Document Verification

- **Actor:** System (automated checks) with Credit Analyst escalation.
- **Input:** Supporting documents (proof of income, identity, etc.).
- **Output:** `documents_complete` flag, `verification_errors` count.
- **Decision:** Whether the file has enough information to proceed automatically.
- **Pain point:** the single strongest signal in the whole analysis. Incomplete
  documentation is associated with a much higher manual review rate (47% of manually
  reviewed applications are incomplete vs. 9% of automatically approved ones), a
  lower approval rate (80% vs. 91%), and more verification errors. Fully digital
  channels (online, mobile app) show a higher incomplete-application rate than
  in-person channels (branch, broker).
- **System interaction:** Document management system; verification rules engine.

## 4. Risk Checks

- **Actor:** System (automated scoring logic), Risk Manager (policy owner).
- **Input:** Debt-to-income ratio, previous defaults, credit history length,
  requested amount relative to income.
- **Output:** A risk profile used to route the file.
- **Decision:** Whether the file can be decided automatically or needs manual
  review.
- **Pain point:** manual review rate rises with requested amount (11% for loans
  under 25k to 29% for loans of 100k+) and with customer segment (small
  business/retail affluent ~22% vs. retail mass ~12%) - by design, since these are
  genuinely more complex files, but the resulting queue is where most of the
  process's total delay accumulates.
- **System interaction:** Risk rules engine; case routing.

## 5. Decision

- **Actor:** System (automated path) or Credit Analyst (manual review path).
- **Input:** Everything collected and verified so far.
- **Output:** `decision` (approved / rejected), `decision_reason`.
- **Decision:** The actual credit decision.
- **Pain point:** processing time for automatically decided applications (median
  20.9 hours) is dramatically shorter than for manually reviewed ones (median 94.4
  hours) - a ~4.5x difference that is the single largest driver of delay found in
  this analysis.
- **System interaction:** Decision engine; notification system.

## 6. Manual Review (conditional)

- **Actor:** Credit Analyst.
- **Input:** The full file, plus the reason it was flagged.
- **Output:** A final decision, or a withdrawal if the customer does not wait for
  one.
- **Decision:** Approve, reject, or the file is abandoned.
- **Pain point:** of applications reaching manual review, 73% are still approved,
  13% rejected, and 14% withdrawn by the customer before any decision - the
  withdrawal share is a cost the process is generating on its own, independent of
  the underlying risk.
- **System interaction:** Case management queue for analysts.

## 7. Communication of the Decision

- **Actor:** System (automated notification).
- **Input:** Final decision and reason.
- **Output:** Customer notified of the outcome.
- **Decision:** None.
- **Pain point:** not directly measurable in this dataset, but the 14% withdrawal
  rate during manual review suggests customers are not being kept informed of
  progress while they wait, which is a plausible contributor even though this
  dataset cannot prove it (no "customer contacted support" or "status viewed"
  field was modeled here, unlike in the companion customer-journey project).
