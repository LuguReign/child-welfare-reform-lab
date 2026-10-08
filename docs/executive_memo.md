# Analyst memo: child welfare performance context and validation demonstration

**Audience:** hiring panel, research colleagues and prospective monitoring partners  
**Date:** October 8, 2026  
**Purpose:** demonstrate the analytic approach required for Action Research's Research Analyst role. This is a portfolio exercise, not an assessment commissioned by a court monitor.

## Findings and their practical meaning

The March 2026 federal CFSR workbook reports different performance patterns across Kansas, Michigan, New Mexico and Texas. For the selected snapshot:

- **Maltreatment in foster care:** Kansas is classified Better than national performance; Michigan, New Mexico and Texas are Worse.
- **Permanency for children entering care:** Kansas, Michigan and New Mexico are Worse; Texas is No different.
- **Placement stability:** Michigan is Better; Kansas, New Mexico and Texas are Worse.
- **Permanency for children already in care 24+ months:** all four states are Worse.

These are the Children's Bureau's risk-standardized comparisons with national performance, using published uncertainty intervals. They identify areas for inquiry; they do not determine settlement compliance, rank systems overall, explain causes, or demonstrate change over time. The seven indicators refer to different source cohorts. Public observed rates should not be directly compared with the national risk-standardized benchmark.

All **28 observed rates** were independently recalculated from the published numerator and denominator within the displayed rounding precision. All **28 published comparison classifications** were consistent with the rounded interval endpoints. This verifies extraction and arithmetic, not the underlying microdata or the federal risk-adjustment model.

## Administrative-data validation demonstration

The separate **synthetic** exercise contains 1,600 fictional children and accepted episodes yielding **17,617 eligible child-months**. It illustrates how a monitoring team could validate full-month in-person visit coverage. None of its values represent real state performance or real children.

Two implementations—Python set-based aggregation and SQL `EXISTS`/grouped counts—agree exactly on all **48 state-quarter numerator and denominator pairs**. Comparison against deliberately flawed fictional submissions flags **five exceptions**: two denominator omissions, two multiple-visit overcounts and one rate/count inconsistency. The exercise shows why matching a submitted percentage alone is insufficient: denominator and numerator agreement must be assessed separately.

The data-quality audit accounts for every row: **three exact duplicate rows** are removed and **16 rows** are quarantined across the child, episode and visit tables. Quarantine includes invalid demographics and dates, orphan relationships, overlapping episodes and visits outside accepted care dates. Downstream visit exclusions are counted separately; these are row counts, not counts of affected children. These issues require source investigation before any production performance finding.

The visit definition excludes partial months and treats an undocumented qualifying visit as absent from the numerator. In actual administrative data, a missing visit could indicate recording failure or no visit. Source completeness, exceptions and denominator impact must therefore be established with the agency. This operational demonstration is not a CFSR or court-approved measure.

## Recommended next steps for a real engagement

1. Obtain the specific settlement requirements and approved measurement protocols; map every requirement to data fields and eligibility rules.
2. Freeze extracts, reconcile to agency control totals, investigate exclusions, and assess completeness by state and time.
3. Independently reconstruct denominators as well as aggregations; submit count-level exceptions for agency response and reviewer assessment.
4. Discuss the patterns with monitoring partners and integrate approved case review, staff inquiry and children/family perspectives before selecting operational interventions.
5. Release findings only after independent review, appropriate disclosure checks and a documented decision on unresolved limitations.

## What the project demonstrates for this role

A reproducible Python/SQL workflow, normalized data management, auditable cleaning, independent performance checks, uncertainty-aware visualization, technical documentation and an accessible findings memo. A workplan, reviewer checklist, issue register and qualitative research guide connect calculations to coordination, partner discussion and learning.

## Source and verification

Children's Bureau, *CFSR Round 4 Statewide Data Indicators Workbook*, March 2026, retrieved October 8, 2026: https://www.cfsrportal.acf.hhs.gov/document/download/gLMYON. Original PDF and extraction text are bundled; every public output row retains source page, cohort and original row. Methods and supporting syntax: https://www.cfsrportal.acf.hhs.gov/resources/round-4-resources/cfsr-round-4-statewide-data-indicators.

Run `python run_pipeline.py`, then `python -m unittest discover -s tests -v`. Automated checks do not substitute for an external peer reviewer; no external review or agency endorsement is claimed.
