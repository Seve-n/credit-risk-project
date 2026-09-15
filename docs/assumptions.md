# Assumptions

This document exists to make the fictional nature of this project impossible to miss.
It is written before the dataset itself, so it works as a specification for what the
data generation script (Phase 3) is allowed to simulate, and it will be revisited once
that script exists to confirm nothing drifted.

## Why this document exists

A synthetic dataset can look convincing without being meaningful. The goal here is not
to hide that the data is generated, but to be explicit about every relationship that was
deliberately built into it, so that anyone reading the analysis later, including a
recruiter, can tell exactly what is a designed pattern versus a data-driven discovery.

## Why these variables

Each variable in the dataset (defined in full in `business-analysis/data-requirements.md`)
exists because a business question needs it, not because it makes the dataset look more
realistic. For example:

- `debt_to_income_ratio`, `previous_defaults`, and `credit_history_length` exist because
  business questions 11-13 ask what is associated with the approval/rejection decision.
- `documents_complete` and `verification_errors` exist because business questions 8-10
  ask what is associated with delays and manual review.
- `channel` and `customer_segment` exist because business questions 6, 14, and 15 ask
  whether certain groups experience a different process.

## Relationships that will be simulated

The data generation script (Phase 3) will build in a small number of plausible,
directional relationships, not a full statistical model of real credit risk:

- incomplete applications (`documents_complete = False`) will tend to have longer
  `processing_time_hours` and more `verification_errors`;
- applications with more `verification_errors` will be more likely to be routed to
  `manual_review`;
- a higher `debt_to_income_ratio` and a history of `previous_defaults` will be
  associated with a higher rejection rate;
- `manual_review` applications will tend to have longer `processing_time_hours` than
  automated ones;
- digital channels will tend to process faster on average than in-branch or paper-based
  channels, reflecting a difference in process design, not a difference in risk.

These relationships will be implemented as directional tendencies with randomness on
top, not as deterministic rules. The exact strength of each relationship, and the
specific implementation, will be documented in the code comments of
`python/data_generation.py` once it is written, and any deviation from what is described
here will be reflected back into this document.

## Simplifications

- A single fictional bank (Chevron Constantine Banking) with a single, generic credit
  process, when real institutions operate several credit products with different rules.
- No macroeconomic variation over time; every application is generated under the same
  implicit "market conditions."
- No explicit fraud category; `previous_defaults` and `verification_errors` stand in as
  simplified risk and data-quality signals.
- Decisions are represented as three categories (approved / rejected / manual review)
  rather than the finer-grained internal statuses a real bank might use.

## Limitations of the dataset

- It is entirely synthetic. No real applicant, transaction, or scoring outcome is
  represented, directly or indirectly.
- The relationships it contains were chosen to be plausible and useful for practicing
  analysis, not calibrated against real credit risk statistics.
- It does not reproduce, and was not derived from, the internal scoring model, policies,
  or process of any real bank, including Belfius.
- Because the relationships are simulated by design, finding them in the analysis
  confirms that the simulation works, not that a real-world causal mechanism has been
  discovered.

## What cannot be concluded from this data

- That any of the simulated relationships hold in a real credit portfolio.
- That any segment, channel, or profile "causes" a longer processing time or a
  different decision rate; the dataset can only show association, by construction.
- That the recommendations in this project are ready to apply to a real credit process
  without validation against real data, real controls, and real regulatory review.
- That this project constitutes, or was informed by, an actual credit risk model.
