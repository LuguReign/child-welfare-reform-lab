# Workplan, QA and partner engagement

Illustrative implementation plan for a real monitoring engagement; no actual partner meetings or approvals are claimed.

| Phase | Owner role | Output / dependency | Completion gate |
|---|---|---|---|
| 1. Scope (days 1–2) | Analyst + monitor | Legal measure register; audience and timeline | Approved definitions and source authority |
| 2. Intake (days 3–4) | Analyst + agency data lead | Frozen extracts, control totals, field map | Completeness and provenance assessed |
| 3. Quality (days 5–7) | Analyst | Defect register, quarantine report, corrections | Material exclusions resolved or disclosed |
| 4. Calculation (days 8–10) | Analyst | Eligibility tables, numerator/denominator outputs | Independent replication completed |
| 5. Peer review (days 11–12) | Second reviewer | Reviewed code, tables, interpretation | Reviewer signs off or logs blocking issues |
| 6. Discussion (days 13–14) | Monitor + analyst | Findings memo and operational questions | Assumptions agreed; follow-up owners named |
| 7. Release (day 15) | Project lead | Approved public aggregates | Disclosure and accessibility review |

## Reviewer checklist

- [ ] Match the downloaded source hash, release date and workbook pages to extraction.
- [ ] Spot-check all 28 public rows, not only rates; confirm denominator unit and cohort.
- [ ] Confirm that observed rates are not compared with risk-standardized benchmarks.
- [ ] Inspect exact duplicate versus conflicting-key rules; account for every source row.
- [ ] Review all exclusion patterns by state and time before interpreting trends.
- [ ] Independently rebuild eligible child-months from approved requirements; inspect partial-month and leap-year cases.
- [ ] Check visit multiplicity, missing records, in-person coding and count conservation.
- [ ] Reconcile submitted and validated numerator and denominator before rate-only checks.
- [ ] Run unit tests and pipeline; inspect manifest and referential integrity.
- [ ] Match memo statements, dashboard labels and downloadable tables.
- [ ] Confirm small-cell/complementary disclosure controls for real publication.
- [ ] Record reviewer name, date, version, unresolved concerns and decision.

No external peer review has been performed on this portfolio. Automated checks support but do not replace that review.

## Risk and issue register template

| ID | Risk / question | Priority | Owner role | Evidence to close | Due / status |
|---|---|---|---|---|---|
| R1 | Missing visits could be reporting gaps | High | Agency data lead | Extract completeness and case review | Before interpretation / open in real use |
| R2 | Quarantine changes denominator | High | Analyst + agency | Corrected extracts and impact analysis | Before release / open in real use |
| R3 | Federal indicator differs from legal measure | High | Monitor | Signed specification crosswalk | At scope / open in real use |
| R4 | Rounded interval touches national benchmark | Medium | Analyst | Higher-precision source and federal guidance | Before classification / review as needed |
| R5 | Multiple projects compete for same review deadline | Medium | Project lead | Prioritized review schedule and capacity | Weekly / template |

## Meeting agenda and proactive status template

1. Decisions needed: definition, data completeness, material exclusions.
2. Evidence: count reconciliation, exception examples, confidence and uncertainty.
3. Interpretation: what is observed, what is unknown, whose experience is missing.
4. Actions: owner, due date, closing evidence and next review.

Status update: **Completed / Next milestone / Blocking issue and impact / Decision needed by / Owner.** Escalate uncertainty before a deadline rather than presenting a qualified number as final.

## Measure register template

Provision ID; approved definition/version; source fields; cohort/freeze; numerator; denominator; exclusions; benchmark or legal target; missing-data rule; independent reviewer; approval date; change history. Populate from primary legal and monitor documents—do not infer from a federal indicator title.
