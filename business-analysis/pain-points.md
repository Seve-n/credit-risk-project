# Pain Points

Every pain point below is tied to a specific number produced by
`python/analysis.py` or `python/risk_analysis.py`, and to the process step it
belongs to in `as-is-process.md`. None of these are assumed; they are read off the
data.

## 1. Manual review is the dominant driver of delay

**Where:** Decision step.

**Evidence:** median processing time is 20.9 hours for automatically decided
applications versus 94.4 hours for manually reviewed ones - a ~4.5x difference. The
gap widens further at the tail (p90: 34.7h vs. 130.3h).

**Why it matters:** manual review affects only ~15.5% of applications, but it
accounts for a disproportionate share of the portfolio's total processing time. Any
initiative aimed at "make the process faster" that does not touch manual review is
unlikely to move the average much.

## 2. A meaningful share of customers give up during manual review

**Where:** Manual Review step.

**Evidence:** of applications sent to manual review, 14% end in the customer
withdrawing before any decision is reached, versus 73% approved and 13% rejected.

**Why it matters:** withdrawal is not a risk outcome, it is a process outcome. These
are potentially good customers lost not because the bank said no, but because the
wait was long enough that they stopped waiting.

## 3. Incomplete documentation is the strongest single signal in the dataset

**Where:** Document Verification step.

**Evidence:** incomplete applications make up 47% of the manually reviewed
population versus 9% of automatically approved applications, and show a lower
approval rate overall (80% vs. 91% for complete applications). Fully digital
channels (online, mobile app) show a higher incomplete-application rate than
in-person channels (branch, broker).

**Why it matters:** this is the one factor that shows up consistently across manual
review rate, processing time, and approval rate. It also looks like the most
tractable one to fix at the source, compared to income or credit history, which are
harder to influence at intake.

## 4. Manual review and processing time both scale with loan size, as intended

**Where:** Risk Checks step.

**Evidence:** manual review rate rises from ~11% for loans under 25k to ~29% for
loans of 100k or more; average processing time follows the same shape.

**Why it matters:** this is listed as a pain point only in the sense that it drives
volume into the slowest part of the process - the pattern itself looks like a
control working as designed, not something to remove. Any automation proposal
touching this step needs to say explicitly that it is not trying to reduce scrutiny
on large loans.

## 5. Previous defaults have an outsized, non-scaling effect on approval

**Where:** Decision step.

**Evidence:** approval rate drops from 91% (no previous defaults) to 68% (one
previous default), but a second or third default does not push the rate meaningfully
lower in this dataset.

**Why it matters:** if a similar pattern held in a real portfolio, it would suggest
the decision logic (automated or manual) treats "any default on record" as the
meaningful threshold, rather than weighing the number of defaults - worth confirming
explicitly with Risk rather than assumed.

## 6. Two data fields drive most of the missing-data problem

**Where:** Data Collection step.

**Evidence:** `annual_income` and `employment_status` were the two fields with
non-trivial missing rates before cleaning (300 and 200 applications respectively out
of ~20,000). Every other field had none.

**Why it matters:** a fix aimed at these two fields specifically (e.g. inline
validation at intake) would address nearly all of the missing-data problem, rather
than a broad, unfocused "improve data quality" initiative.
