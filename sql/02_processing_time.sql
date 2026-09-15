-- Processing time analysis
-- Mirrors python/analysis.py's processing-time functions. Boolean columns
-- are INTEGER 0/1 in SQLite (see sql/README.md).

-- Processing time by manual review: the core evidence behind the manual
-- review pain point. Median via the ROW_NUMBER() trick, computed per group.
WITH ranked AS (
    SELECT
        manual_review,
        processing_time_hours,
        ROW_NUMBER() OVER (PARTITION BY manual_review ORDER BY processing_time_hours) AS rn,
        COUNT(*) OVER (PARTITION BY manual_review) AS group_rows
    FROM credit_applications
)
SELECT
    manual_review,
    COUNT(*) AS n,
    AVG(processing_time_hours) AS mean_hours,
    AVG(CASE WHEN rn IN ((group_rows + 1) / 2, (group_rows + 2) / 2)
        THEN processing_time_hours END) AS median_hours
FROM ranked
GROUP BY manual_review;

-- Processing time by channel (mean and count - see analysis.py for the full
-- median/p90 breakdown, reproduced here as mean only to keep the query
-- readable, since the median-per-group pattern above generalizes the same way).
SELECT
    channel,
    COUNT(*) AS n,
    AVG(processing_time_hours) AS mean_hours
FROM credit_applications
GROUP BY channel
ORDER BY mean_hours DESC;

-- Verification errors vs. processing time: is the relationship roughly
-- monotonic, or does it plateau?
SELECT
    verification_errors,
    COUNT(*) AS n,
    AVG(processing_time_hours) AS mean_hours
FROM credit_applications
GROUP BY verification_errors
ORDER BY verification_errors;

-- Profile of the slowest 10% of applications (p90 threshold computed
-- separately, then reused - SQLite has no variable syntax across
-- statements in the CLI, so this repeats the p90 CTE from 01_portfolio_kpis.sql).
WITH ranked AS (
    SELECT
        processing_time_hours,
        ROW_NUMBER() OVER (ORDER BY processing_time_hours) AS rn,
        COUNT(*) OVER () AS total_rows
    FROM credit_applications
),
p90_threshold AS (
    SELECT processing_time_hours AS threshold
    FROM ranked
    WHERE rn = CAST(0.9 * total_rows AS INTEGER)
)
SELECT
    COUNT(*) AS n_slow_applications,
    AVG(manual_review) AS manual_review_rate,
    AVG(CASE WHEN documents_complete = 0 THEN 1.0 ELSE 0 END) AS incomplete_rate,
    AVG(verification_errors) AS avg_verification_errors,
    AVG(requested_amount) AS avg_requested_amount
FROM credit_applications, p90_threshold
WHERE processing_time_hours >= threshold;
