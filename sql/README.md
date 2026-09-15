# SQL Analysis

These queries run against a SQLite database built from
`data/processed/credit_applications_clean.csv`. The database itself is not
committed (see `.gitignore`): it is a regenerated artifact, not a source of
truth, so keeping it out of version control avoids two copies of the same
data silently drifting apart.

## Building the database locally

```bash
python -c "
import sqlite3, pandas as pd
df = pd.read_csv('data/processed/credit_applications_clean.csv')
conn = sqlite3.connect('credit_applications.db')
df.to_sql('credit_applications', conn, if_exists='replace', index=False)
conn.close()
"
```

Then run any file here with the `sqlite3` CLI, e.g.:

```bash
sqlite3 credit_applications.db < sql/01_portfolio_kpis.sql
```

## Notes on the schema as SQLite sees it

- `documents_complete` and `manual_review` are Python booleans in the CSV,
  but `pandas.to_sql()` stores them in SQLite as `INTEGER` `0`/`1`, not as
  text. The queries below compare against `0`/`1` for that reason. (The
  first draft of this file assumed they would land as the strings
  `'True'`/`'False'`, which silently produced a 0% manual review rate -
  caught only by actually running the query against the database instead of
  trusting the assumption.)
- `decision` is `NULL` for withdrawn applications by design (see
  `python/data_cleaning.py`). Every query that computes an approval or
  rejection rate filters to `decision IS NOT NULL` first, exactly like
  `python/analysis.py` does, so the two stay comparable.
- SQLite has no built-in `MEDIAN()` or `PERCENTILE_CONT()`. The median and
  p90 queries use the standard `ROW_NUMBER() OVER (...)` trick instead
  (order the values, then pick the row(s) at the target rank). It is
  documented inline in `01_portfolio_kpis.sql` the first time it is used.

## Files

| File | Business questions answered |
|---|---|
| `01_portfolio_kpis.sql` | Overall approval/rejection/withdrawal/manual review rate, processing time distribution, average requested amount, incomplete application rate |
| `02_processing_time.sql` | Which applications take the longest: manual review vs. automatic, by channel, by verification error count, profile of the slowest 10% |
| `03_decision_analysis.sql` | Profile comparison across decision paths, approval rate by DTI band, previous defaults, income-to-amount ratio, document completeness |
| `04_manual_review.sql` | Manual review rate by segment, loan size, document completeness, and what manual review actually decides |

Every number in these files is meant to match the equivalent function in
`python/analysis.py` / `python/risk_analysis.py`. That cross-check is worth
actually running rather than assuming: it caught a real bug here too. The
first draft of `01_portfolio_kpis.sql` assumed boolean columns would be
stored as the text `'True'`/`'False'` in SQLite, which silently produced a
0% manual review rate and a 0% incomplete application rate. `pandas.to_sql()`
actually stores them as `INTEGER` `0`/`1`. Running the query against the real
database, instead of trusting the assumption, is what surfaced it (the same
lesson the companion customer-journey project learned from a `LEAD()`
window function bug).

Two small, understood differences remain between the SQL and Python results,
both from binning convention rather than a logic error:

- **DTI bands**: pandas' `pd.cut()` is right-inclusive by default (a value of
  exactly `0.20` falls in the `<0.20` bucket), while the SQL uses a strict
  `<` comparison (a value of exactly `0.20` falls in the next bucket up).
  This shifts a handful of rows between adjacent bands.
- **P90 threshold**: pandas' `quantile(0.90)` interpolates and then includes
  every row `>=` that interpolated value, while the SQL ranks rows and picks
  the exact value sitting at the 90th-percentile rank. When several rows
  share that value, the two methods can include a slightly different count
  (1,998 in Python vs. 2,000 in SQL on this dataset).

Both are documented here rather than "fixed" to force an exact match, because
forcing one method to mimic the other's rounding behavior would make the
code less readable for a difference that does not change any conclusion.
