# Setup Notes

Planted data-quality issues:

- Exact duplicate row: `2026-03-18,West,Enterprise,55000,2` appears twice.
- Missing amount: `2026-03-11,East,Starter,,16`.
- `amount` currency/meaning is not documented anywhere; the agent should not assert a business definition from the column name alone.

Q1 = Jan-Mar, Q2 = Apr-Jun. Enterprise growth dominates Q2; Starter declines. The correct analysis states how duplicates and the missing value were handled and cross-checks totals.
