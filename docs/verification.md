# Verification record

Verified October 8, 2026 on the delivered version.

- Public extraction: 28 unique state/indicator rows, original source lineage preserved.
- Observed arithmetic: 28/28 pass at published rounding precision.
- RSP classification consistency: 28/28 match published labels using rounded endpoints.
- Accepted synthetic population: 1,600 children; 1,599 episodes; 14,600 visit rows.
- Eligible child-months: 17,617; 48 state-quarter numerator/denominator pairs match exactly in Python and SQL.
- Fictional submission reconciliation: all five planted exceptions flagged.
- Row accounting: every raw row is clean, deduplicated or quarantined; no unaccounted rows.
- SQLite foreign-key check: no violations.
- Python tests: nine passed, including leap month, entry/exit boundaries, open episodes, zero denominator, comparison direction, duplicate visit counting, conflicting keys and disposition conservation.
- JavaScript logic smoke check: all seven indicator choices, all four synthetic jurisdictions, all four tabs and five displayed exceptions pass without invalid chart values.

## Review still needed

The live GitHub Pages dashboard was subsequently checked in Chrome on October 8, 2026. All seven indicator selections, four synthetic jurisdiction selections, four section tabs and the five reconciliation exceptions were verified in the rendered page. The desktop dashboard was visually inspected; a screenshot is retained in `docs/assets/dashboard-public.jpg`. A formal accessibility audit and mobile/cross-browser layout review remain outstanding.

No external analytic peer reviewer, court monitor or agency has approved this project. No production source microdata or legal compliance assessment is included.
