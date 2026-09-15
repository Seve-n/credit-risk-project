-- Manual review analysis
-- Mirrors python/analysis.py's manual-review functions. Boolean columns are
-- INTEGER 0/1 in SQLite (see sql/README.md).

-- Manual review rate by customer segment.
SELECT
    customer_segment,
    COUNT(*) AS n,
    AVG(manual_review) AS manual_review_rate
FROM credit_applications
GROUP BY customer_segment
ORDER BY manual_review_rate DESC;

-- Manual review rate by loan size band.
SELECT
    CASE
        WHEN requested_amount < 10000 THEN '<10k'
        WHEN requested_amount < 25000 THEN '10k-25k'
        WHEN requested_amount < 50000 THEN '25k-50k'
        WHEN requested_amount < 100000 THEN '50k-100k'
        ELSE '100k+'
    END AS loan_size_band,
    COUNT(*) AS n,
    AVG(manual_review) AS manual_review_rate
FROM credit_applications
GROUP BY loan_size_band
ORDER BY MIN(requested_amount);

-- Manual review rate by document completeness: the single strongest
-- predictor of whether a file needs a human, per python/analysis.py.
SELECT
    documents_complete,
    COUNT(*) AS n,
    AVG(manual_review) AS manual_review_rate
FROM credit_applications
GROUP BY documents_complete;

-- What manual review actually decides: of the applications sent to manual
-- review, what share end up approved, rejected, or withdrawn? This is the
-- number that supports or undercuts an automation argument.
SELECT
    CASE
        WHEN application_status = 'withdrawn' THEN 'withdrawn'
        ELSE decision
    END AS manual_review_outcome,
    COUNT(*) AS n,
    COUNT(*) * 1.0 / (SELECT COUNT(*) FROM credit_applications WHERE manual_review = 1) AS share
FROM credit_applications
WHERE manual_review = 1
GROUP BY manual_review_outcome;
