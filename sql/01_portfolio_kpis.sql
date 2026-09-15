-- Portfolio KPIs
-- Mirrors python/analysis.py::portfolio_kpi_summary(). If a number here does
-- not match the Python output, this file or that function has a bug -
-- they are not allowed to define the KPI differently.

-- Total applications in the portfolio.
SELECT COUNT(*) AS total_applications
FROM credit_applications;

-- Approval rate and rejection rate, as a share of DECIDED applications only.
-- `decision` is NULL for withdrawn applications by design (see
-- python/data_cleaning.py), so they are excluded here exactly like in
-- analysis.py::approval_rate() / rejection_rate() - otherwise a change in
-- the withdrawal rate would silently move these two rates.
SELECT
    SUM(CASE WHEN decision = 'approved' THEN 1 ELSE 0 END) * 1.0
        / COUNT(*) AS approval_rate,
    SUM(CASE WHEN decision = 'rejected' THEN 1 ELSE 0 END) * 1.0
        / COUNT(*) AS rejection_rate
FROM credit_applications
WHERE decision IS NOT NULL;

-- Withdrawal rate, over the full portfolio (withdrawal is a portfolio-level
-- outcome, not conditional on reaching a decision).
SELECT
    SUM(CASE WHEN application_status = 'withdrawn' THEN 1 ELSE 0 END) * 1.0
        / COUNT(*) AS withdrawal_rate
FROM credit_applications;

-- Manual review rate.
-- Boolean columns land in SQLite as INTEGER 0/1 via pandas.to_sql(), not as
-- text - checked against the actual database rather than assumed.
SELECT
    SUM(manual_review) * 1.0 / COUNT(*) AS manual_review_rate
FROM credit_applications;

-- Average processing time. Straightforward with AVG().
SELECT AVG(processing_time_hours) AS avg_processing_time_hours
FROM credit_applications;

-- Median processing time.
-- SQLite has no MEDIAN()/PERCENTILE_CONT(), so this uses the standard
-- ROW_NUMBER() trick: rank every row by the value, then average the row(s)
-- sitting at the middle rank(s) (two of them when the row count is even).
WITH ranked AS (
    SELECT
        processing_time_hours,
        ROW_NUMBER() OVER (ORDER BY processing_time_hours) AS rn,
        COUNT(*) OVER () AS total_rows
    FROM credit_applications
)
SELECT AVG(processing_time_hours) AS median_processing_time_hours
FROM ranked
WHERE rn IN ((total_rows + 1) / 2, (total_rows + 2) / 2);

-- P90 processing time.
-- Same ranking approach, picking the row at the 90th percentile position.
WITH ranked AS (
    SELECT
        processing_time_hours,
        ROW_NUMBER() OVER (ORDER BY processing_time_hours) AS rn,
        COUNT(*) OVER () AS total_rows
    FROM credit_applications
)
SELECT processing_time_hours AS p90_processing_time_hours
FROM ranked
WHERE rn = CAST(0.9 * total_rows AS INTEGER);

-- Average requested amount.
SELECT AVG(requested_amount) AS avg_requested_amount
FROM credit_applications;

-- Incomplete application rate.
SELECT
    SUM(CASE WHEN documents_complete = 0 THEN 1 ELSE 0 END) * 1.0
        / COUNT(*) AS incomplete_application_rate
FROM credit_applications;

-- Average verification error count.
SELECT AVG(verification_errors) AS avg_verification_errors
FROM credit_applications;
