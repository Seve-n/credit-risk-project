-- Credit decision analysis
-- Mirrors python/risk_analysis.py. Association only, not causation, and not
-- a credit scoring model - see docs/assumptions.md.

-- Profile by decision path: manual_review (regardless of eventual outcome),
-- or approved / rejected / withdrawn among applications NOT sent to manual
-- review. This separates "what triggers manual review" from "what gets
-- approved," which is a different question.
SELECT
    CASE
        WHEN manual_review = 1 THEN 'manual_review'
        WHEN decision IS NULL THEN 'withdrawn'
        ELSE decision
    END AS decision_path,
    COUNT(*) AS n,
    AVG(annual_income) AS avg_annual_income,
    AVG(monthly_expenses) AS avg_monthly_expenses,
    AVG(debt_to_income_ratio) AS avg_debt_to_income_ratio,
    AVG(requested_amount) AS avg_requested_amount,
    AVG(previous_defaults) AS avg_previous_defaults,
    AVG(CASE WHEN documents_complete = 0 THEN 1.0 ELSE 0 END) AS incomplete_document_rate
FROM credit_applications
GROUP BY decision_path;

-- Approval rate by debt-to-income band, decided applications only.
SELECT
    CASE
        WHEN debt_to_income_ratio < 0.20 THEN '<0.20'
        WHEN debt_to_income_ratio < 0.35 THEN '0.20-0.35'
        WHEN debt_to_income_ratio < 0.50 THEN '0.35-0.50'
        WHEN debt_to_income_ratio < 0.70 THEN '0.50-0.70'
        ELSE '0.70+'
    END AS dti_band,
    COUNT(*) AS n,
    AVG(CASE WHEN decision = 'approved' THEN 1.0 ELSE 0 END) AS approval_rate
FROM credit_applications
WHERE decision IS NOT NULL
GROUP BY dti_band
ORDER BY MIN(debt_to_income_ratio);

-- Approval rate by previous defaults, decided applications only.
SELECT
    CASE WHEN previous_defaults >= 3 THEN '3+' ELSE CAST(previous_defaults AS TEXT) END AS previous_defaults_band,
    COUNT(*) AS n,
    AVG(CASE WHEN decision = 'approved' THEN 1.0 ELSE 0 END) AS approval_rate
FROM credit_applications
WHERE decision IS NOT NULL
GROUP BY previous_defaults_band
ORDER BY MIN(previous_defaults);

-- Approval rate by income-to-requested-amount ratio, decided applications only.
SELECT
    CASE
        WHEN annual_income * 1.0 / requested_amount < 0.5 THEN '<0.5x'
        WHEN annual_income * 1.0 / requested_amount < 1.0 THEN '0.5x-1x'
        WHEN annual_income * 1.0 / requested_amount < 2.0 THEN '1x-2x'
        ELSE '2x+'
    END AS ratio_band,
    COUNT(*) AS n,
    AVG(CASE WHEN decision = 'approved' THEN 1.0 ELSE 0 END) AS approval_rate
FROM credit_applications
WHERE decision IS NOT NULL
GROUP BY ratio_band
ORDER BY MIN(annual_income * 1.0 / requested_amount);

-- Approval rate by document completeness, decided applications only.
SELECT
    documents_complete,
    COUNT(*) AS n,
    AVG(CASE WHEN decision = 'approved' THEN 1.0 ELSE 0 END) AS approval_rate
FROM credit_applications
WHERE decision IS NOT NULL
GROUP BY documents_complete;
