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

A full browser rendering and accessibility review was not completed: a compatible local browser was unavailable and its download failed. The JavaScript test uses a minimal mocked DOM and does not validate layout, visual appearance, browser compatibility or assistive technology behavior. Responsive CSS and accessible chart tables are included, but those design features should be checked in a browser before portfolio publication.

No external analytic peer reviewer, court monitor or agency has approved this project. No production source microdata or legal compliance assessment is included.
