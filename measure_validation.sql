-- Independent SQL calculation. Count each eligible episode-month once,
-- irrespective of the number of visits. Child-month eligibility is materialized
-- separately and tested at calendar boundaries in tests/test_pipeline.py.
SELECT cm.state, cm.quarter,
       SUM(CASE WHEN EXISTS (
           SELECT 1 FROM visits v
           WHERE v.episode_id=cm.episode_id AND v.in_person=1
             AND substr(v.visit_date,1,7)=cm.month
       ) THEN 1 ELSE 0 END) AS numerator,
       COUNT(*) AS denominator
FROM child_months cm
GROUP BY cm.state, cm.quarter
ORDER BY cm.state, cm.quarter;
