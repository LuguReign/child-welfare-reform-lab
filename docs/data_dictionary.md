# Data dictionary, lineage and management

All dates use ISO `YYYY-MM-DD`; empty `exit_date` means still in care at the synthetic freeze. UTF-8 CSVs include headers. IDs beginning DEMO are fictional; no real child records are present.

| Table / field | Definition / validation |
|---|---|
| children.child_id | Fictional unique child key; exact duplicate removed; conflicting versions quarantined |
| children.state | KS, MI, NM, TX; fictional jurisdiction in this layer |
| children.age_at_entry | Integer 0–17; fixed age band, not time-varying age |
| episodes.episode_id | Unique care-episode key |
| episodes.child_id | Foreign key to accepted child |
| episodes.entry_date | First care date; must be valid and no later than freeze |
| episodes.exit_date | First day out of care; empty = open; must be after entry |
| episodes.exit_reason | reunification, adoption, guardianship, other; required for closed episode |
| visits.visit_id | Unique source visit row key |
| visits.episode_id | Foreign key to accepted episode |
| visits.visit_date | Date within `[entry, exit)` |
| visits.in_person | 1 = in person; 0 = other contact |
| child_months.episode_id, month | Composite unique eligible episode-month; materialized denominator |
| child_months.quarter, state, age_group | Group labels derived from calendar and accepted child |
| public_indicators.numerator / denominator | Published federal counts or care-day exposure, depending on indicator |
| public_indicators.observed / recalculated | Published observed rate and arithmetic reconstruction |
| public_indicators.scale / decimals | Units and published display precision |
| public_indicators.rsp, rsp_lower, rsp_upper | Imported federal risk-standardized estimate and interval |
| public_indicators.national / direction | National RSP benchmark; higher or lower favorable |
| public_indicators.period | Federal source cohort; not dashboard generation date |
| public_indicators.source_page / line / row | Original PDF printed page, layout text line and original source row |
| reconciliation.submitted_* / validated_* | Fictional agency submission compared to audited calculation |
| reconciliation.difference_pp | Submitted minus validated rate, percentage points |
| quality_audit.rule / action / raw_record | Reason, disposition and original row as JSON; internal QA lineage |

## Flow and ownership

Public PDF → layout text → strict extraction → arithmetic/classification checks → dashboard.

Seeded fictional raw CSVs → row and relationship QA → accepted normalized warehouse → full-month eligibility → Python/SQL aggregates → submission reconciliation → dashboard and memo.

Raw, clean and derived artifacts remain separate. The source manifest preserves hashes for source files and generated raw CSVs. SQLite enforces primary keys, foreign keys and visit/age constraints; referential integrity is checked on every run. Output rows retain counts so rate discrepancies can be decomposed into numerator, denominator and arithmetic issues. Audit logs would be sensitive if applied to real records and must never enter a public repository.

## Updating sources

Do not silently replace a federal release. Preserve the prior release, capture retrieval date and hash, confirm the workbook structure and periods, rerun extraction and review changed rows. If source types or definitions change, version the measure specification and regenerate outputs only after reviewer agreement. No automatic internet refresh is configured.
