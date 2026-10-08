# Measure specification and validation protocol

## A. Public federal indicators (snapshot)

**Population:** KS, MI, NM, TX, seven published CFSR Round 4 indicators. **Release:** March 2026 workbook; profiles dated February 2026, submissions as of January 10, 2026. Each row retains its own source cohort, page and original text. Release date is not the observation date.

**Arithmetic:** `numerator / denominator × scale`, where scale is 100 for percentages, 1,000 for placement moves and 100,000 for maltreatment victimizations per care-day exposure. Published observed performance is checked against its displayed precision (half a unit in the last decimal place). Rates are never averaged across states or indicators. Zero denominators would yield missing, not zero.

**National comparison:** use reported risk-standardized estimates and uncertainty intervals. For lower-is-favorable indicators, an upper limit below the benchmark is Better; a lower limit above it is Worse. For higher-is-favorable indicators, reverse the logic. An interval covering the benchmark is No different. This is a consistency check on rounded published values, not re-estimation of the federal risk-standardization model. All 28 extracted rows happen to have nonmissing values; the extractor fails closed if an expected row becomes absent or a DQ marker replaces a numeric row. A future release with exclusions needs explicit nullable handling before inclusion, rather than interpreting DQ as zero.

**Underlying numerator/denominator validation:** unavailable here. The federal source supplies aggregated counts. Replicating the count arithmetic does not prove that agency microdata, cohort selection or risk adjustment is correct.

## B. Synthetic full-month in-person visit coverage

**Purpose:** demonstrate validation of an operational measure from fictional administrative records. **Version:** 1.0. **Freeze:** December 31, 2025. **Unit:** eligible child-month; one nonoverlapping episode at a time.

**Denominator:** a child-month wholly contained within an accepted care episode, on or before the data freeze. Entry is inclusive and exit is exclusive. Entry January 1 and exit February 1 includes January. Entry January 2 excludes January. An open episode is administratively closed at January 1, 2026 for exposure calculation. Age at entry must be 0–17 and stays fixed for descriptive grouping. Multiple valid, nonoverlapping episodes would be allowed.

**Numerator:** denominator child-months with at least one accepted visit coded `in_person=1` during that episode and calendar month. Multiple visits contribute at most one. Telephone-only visits do not count. Months without a documented qualifying visit remain in the denominator. Both source completeness and visit-type validity require agency confirmation in real use.

**Grouping:** state and calendar quarter. Age-at-entry bands 0–5, 6–12, 13–17 for descriptive equity-related inquiry; this is not a complete equity analysis and contains no observed race, income, sexuality or disability data.

**Formula:** numerator ÷ denominator ×100. Counts must reconcile exactly. Submitted rounded rates tolerate 0.005 percentage points; counts always take precedence over matching percentages.

**Independence:** Python uses a set of episode/month visit pairs; SQL uses correlated `EXISTS` against visits and grouped eligible-month counts. They share the cleaned source and eligibility table. Therefore their agreement validates aggregation only. Independently reviewed boundary tests validate eligibility logic; production review should independently rebuild the denominator from the approved protocol as well.

**DQ protocol:** preserve raw rows; remove exact duplicates; quarantine every version of conflicting primary keys; quarantine invalid demographics/dates, orphan references, visits outside accepted episodes and all members of overlapping episode pairs. Audit each action, including downstream orphan visits caused by episode exclusion. Require `raw = clean + deduplicated + quarantined` per table. No automatic imputation. Nonempty exit reason codes are required for closed episodes; child identity linkage relies on supplied IDs and is not probabilistic.

**Disclosure:** age table cells with fewer than 20 child-months mask numerator, denominator and rate. Public demonstration records are synthetic and downloadable. Real records require secure environments, access controls, complementary suppression/other disclosure checks and jurisdiction-specific policies; this demonstration rule alone is insufficient.

## C. Before litigation or production use

Obtain executed measure definitions, amendments and monitor-approved interpretation. Create a crosswalk from each legal requirement to fields, eligibility, exclusions and time windows. Obtain data sharing authority and a secure approved environment. Validate completeness against agency control totals, investigate all unresolved exclusions, independently reconstruct denominators and obtain peer review and monitor approval. Record source freeze, extract version, changes and approval evidence. Federal national performance is not a settlement target. This project intentionally has no compliance status field or inferred court target.
