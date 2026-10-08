import sys, unittest, tempfile, sqlite3
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import run_pipeline as p

class EligibilityTests(unittest.TestCase):
    def test_partial_entry_and_exit_excluded(self):
        self.assertEqual(list(p.eligible_months('2024-01-15','2024-04-15')),['2024-02','2024-03'])
    def test_leap_month_and_exit_boundary(self):
        self.assertEqual(list(p.eligible_months('2024-02-01','2024-03-01')),['2024-02'])
        self.assertEqual(list(p.eligible_months('2024-02-02','2024-03-01')),[])
    def test_open_episode_complete_followup(self):
        self.assertEqual(list(p.eligible_months('2025-12-01','')),['2025-12'])
        self.assertEqual(list(p.eligible_months('2025-12-02','')),[])
    def test_zero_denominator_is_missing(self):
        self.assertIsNone(p.rate(0,0))
    def test_comparison_direction_and_boundary(self):
        self.assertEqual(p.classify(3,4,5,'lower'),'Better')
        self.assertEqual(p.classify(3,4,5,'higher'),'Worse')
        self.assertEqual(p.classify(3,5,5,'lower'),'No different')

class ValidationTests(unittest.TestCase):
    def test_multiple_visits_one_numerator_and_missing_visit_denominator(self):
        db=sqlite3.connect(':memory:')
        db.executescript('CREATE TABLE child_months(episode_id,month,quarter,state); CREATE TABLE visits(episode_id,visit_date,in_person);')
        db.executemany('INSERT INTO child_months VALUES (?,?,?,?)',[('a','2024-01','2024-Q1','KS'),('b','2024-01','2024-Q1','KS')])
        db.executemany('INSERT INTO visits VALUES (?,?,?)',[('a','2024-01-02',1),('a','2024-01-20',1),('b','2024-01-15',0)])
        self.assertEqual(db.execute((p.ROOT/'measure_validation.sql').read_text()).fetchall(),[('KS','2024-Q1',1,2)])
        db.close()
    def test_conflicting_key_quarantines_all_versions(self):
        with tempfile.TemporaryDirectory() as td:
            raw=Path(td)/'raw';out=Path(td)/'out';out.mkdir()
            p.write_csv(raw/'children.csv',[dict(child_id='x',state='KS',age_at_entry=5),dict(child_id='x',state='KS',age_at_entry=6),dict(child_id='y',state='MI',age_at_entry=8)])
            p.write_csv(raw/'episodes.csv',[],['episode_id','child_id','entry_date','exit_date','exit_reason'])
            p.write_csv(raw/'visits.csv',[],['visit_id','episode_id','visit_date','in_person'])
            with patch.object(p,'RAW',raw),patch.object(p,'OUT',out):clean,audit=p.clean_sources()
            self.assertEqual([r['child_id'] for r in clean['children']],['y'])
            self.assertEqual(sum(a['rule']=='conflicting_primary_key' for a in audit),2)
    def test_quarantine_and_duplicate_conservation(self):
        with tempfile.TemporaryDirectory() as td:
            raw=Path(td)/'raw';out=Path(td)/'out';out.mkdir()
            with patch.object(p,'RAW',raw),patch.object(p,'OUT',out):
                p.synthetic_source();clean,audit=p.clean_sources()
                for table in clean:
                    self.assertEqual(len(p.read_csv(raw/f'{table}.csv')),len(clean[table])+sum(a['table']==table for a in audit))
                rules={a['rule'] for a in audit}
                self.assertTrue({'overlapping_episodes','orphan_child','orphan_episode','visit_outside_episode','exact_duplicate'}.issubset(rules))
    def test_public_source_expected_rows_and_both_checks(self):
        rows=p.read_csv(p.OUT/'public_indicators.csv')
        self.assertEqual(len(rows),28)
        self.assertTrue(all(r['arithmetic_pass']=='True' and r['classification_pass']=='True' for r in rows))

if __name__=='__main__':unittest.main()
