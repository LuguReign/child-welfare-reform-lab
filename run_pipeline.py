#!/usr/bin/env python3
"""Offline reproducible portfolio pipeline; Python 3.10+, standard library only."""
from pathlib import Path
from datetime import date, timedelta
from collections import Counter, defaultdict
import csv, hashlib, json, random, re, sqlite3

ROOT = Path(__file__).resolve().parent
RAW, OUT = ROOT/'data/raw', ROOT/'output'
STATES = {'KS':'Kansas','MI':'Michigan','NM':'New Mexico','TX':'Texas'}
CUTOFF = date(2025,12,31)
SOURCE = 'https://www.cfsrportal.acf.hhs.gov/document/download/gLMYON'
INDICATORS = [
 ('maltreatment','Maltreatment in foster care',100000,2,'lower','victimizations / 100,000 care days'),
 ('recurrence','Recurrence of maltreatment',100,1,'lower','percent'),
 ('permanency_entry','Permanency within 12 months: entrants',100,1,'higher','percent'),
 ('permanency_12_23','Permanency: in care 12–23 months',100,1,'higher','percent'),
 ('permanency_24','Permanency: in care 24+ months',100,1,'higher','percent'),
 ('reentry','Reentry within 12 months',100,1,'lower','percent'),
 ('stability','Placement stability',1000,2,'lower','moves / 1,000 care days')]

def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]) if rows else fields or ['empty']);w.writeheader();w.writerows(rows)

def read_csv(path):
    with path.open(encoding='utf-8') as f:return list(csv.DictReader(f))

def rate(n,d,scale=100):return n/d*scale if d else None

def classify(lo,hi,np,direction):
    if lo <= np <= hi:return 'No different'
    return ('Better' if hi<np else 'Worse') if direction=='lower' else ('Better' if lo>np else 'Worse')

def public_snapshot():
    """Parse original PDF's pdftotext layout; retain source line/page and row text."""
    text=(ROOT/'data/source/cfsr-march-2026.txt').read_text()
    rows=[]; idx=-1; period=''; page=1
    for line_no,line in enumerate(text.splitlines(),1):
        # Form-feed is consumed by splitlines; printed footer identifies page precisely.
        footer=re.search(r'CFSR Round 4 Statewide Data Indicators Workbook, March 2026\s+(\d+)\s*$',line)
        if footer:page=int(footer.group(1))+1
        if line.startswith('12-month period:'):
            idx+=1;period=line.split(':',1)[1].strip()
        m=re.match(r'^\s*(KS|MI|NM|TX)\s+([\d,]+)\s+([\d,]+)\s+([\d.]+)%?\s+([\d.]+)%?\s+([\d.]+)%?\s+([\d.]+)%?\s+([\d.]+)%?\s+(Better|Worse|No different)\s*$',line)
        if m and 0<=idx<7:
            s,d,n,op,lo,rsp,hi,np,status=m.groups();key,label,scale,dec,direction,unit=INDICATORS[idx]
            d,n=int(d.replace(',','')),int(n.replace(',','')); op,lo,rsp,hi,np=map(float,[op,lo,rsp,hi,np])
            calc=rate(n,d,scale)
            rows.append(dict(state=s,state_name=STATES[s],indicator=key,label=label,period=period,denominator=d,numerator=n,observed=op,recalculated=calc,scale=scale,decimals=dec,unit=unit,direction=direction,rsp_lower=lo,rsp=rsp,rsp_upper=hi,national=np,reported_class=status,replicated_class=classify(lo,hi,np,direction),arithmetic_pass=abs(calc-op)<=.5*10**(-dec)+1e-9,classification_pass=classify(lo,hi,np,direction)==status,source_page=page,source_line=line_no,source_row=line.strip(),source_url=SOURCE))
    assert len(rows)==28 and len({(r['state'],r['indicator']) for r in rows})==28, 'Source extraction changed; inspect source.'
    assert all(r['rsp_lower']<=r['rsp']<=r['rsp_upper'] for r in rows)
    write_csv(OUT/'public_indicators.csv',rows)
    return rows

def synthetic_source():
    """Seeded fictional episodes and visits. State labels are examples only."""
    rng=random.Random(1042026);children=[];episodes=[];visits=[]
    for s in STATES:
        for i in range(1,401):
            cid=f'DEMO-{s}-{i:04d}';age=rng.randrange(0,18)
            children.append(dict(child_id=cid,state=s,age_at_entry=age))
            start=date(2023,1,1)+timedelta(days=rng.randrange(0,1000))
            end=min(start+timedelta(days=rng.randrange(45,850)),CUTOFF+timedelta(days=1))
            exit_date='' if end>CUTOFF else end.isoformat()
            episodes.append(dict(episode_id=f'E-{cid}',child_id=cid,entry_date=start.isoformat(),exit_date=exit_date,exit_reason=rng.choice(['reunification','adoption','guardianship','other']) if exit_date else ''))
            month=date(start.year,start.month,1)
            while month<=min(end,CUTOFF):
                nxt=date(month.year+month.month//12,month.month%12+1,1)
                # Source contains all months; analytic eligibility includes full calendar months only.
                probability=.74+.025*(month.year-2023)+{'KS':0,'MI':.04,'NM':-.03,'TX':.02}[s]
                if rng.random()<probability:
                    day=month+timedelta(days=rng.randrange((nxt-month).days))
                    if start<=day<end:visits.append(dict(visit_id=f'V-{len(visits):06d}',episode_id=f'E-{cid}',visit_date=day.isoformat(),in_person='1'))
                month=nxt
    # Deliberate defects, fully logged rather than quietly imputed.
    children.append(dict(children[0]));children.append(dict(child_id='DEMO-BAD-AGE',state='KS',age_at_entry=99))
    episodes.extend([dict(episodes[0]),dict(episode_id='E-ORPHAN',child_id='UNKNOWN',entry_date='2024-01-01',exit_date='',exit_reason=''),dict(episode_id='E-BAD-DATE',child_id=children[1]['child_id'],entry_date='01/35/2024',exit_date='',exit_reason=''),dict(episode_id='E-REVERSED',child_id=children[2]['child_id'],entry_date='2025-05-01',exit_date='2025-04-01',exit_reason='other'),dict(episode_id='E-OVERLAP',child_id=episodes[0]['child_id'],entry_date=episodes[0]['entry_date'],exit_date=episodes[0]['exit_date'],exit_reason=episodes[0]['exit_reason'])])
    visits.extend([dict(visits[0]),dict(visit_id='V-ORPHAN',episode_id='UNKNOWN',visit_date='2024-01-01',in_person='1'),dict(visit_id='V-OUTSIDE',episode_id=episodes[1]['episode_id'],visit_date='2000-01-01',in_person='1'),dict(visit_id='V-MISSING',episode_id=episodes[1]['episode_id'],visit_date='',in_person='1')])
    for name,rows in [('children',children),('episodes',episodes),('visits',visits)]:write_csv(RAW/f'{name}.csv',rows)

def clean_sources():
    audit=[];clean={};indices={}
    def log(table,row,rule,action):audit.append(dict(table=table,record_id=row.get({'children':'child_id','episodes':'episode_id','visits':'visit_id'}[table]),rule=rule,action=action,raw_record=json.dumps(row,sort_keys=True)))
    for table,key in [('children','child_id'),('episodes','episode_id'),('visits','visit_id')]:
        kept=[];seen={};bad=set();raw=read_csv(RAW/f'{table}.csv')
        # Conflicting duplicate primary keys: quarantine ALL versions; no arbitrary first-row wins.
        variants=defaultdict(set)
        for row in raw:variants[row[key]].add(json.dumps(row,sort_keys=True))
        conflicts={k for k,v in variants.items() if len(v)>1}
        for row in raw:
            reason=None
            if row[key] in conflicts:reason='conflicting_primary_key'
            elif row[key] in seen:log(table,row,'exact_duplicate','deduplicated');continue
            seen[row[key]]=row
            if not reason:
                try:
                    if table=='children':
                        if row['state'] not in STATES or not 0<=int(row['age_at_entry'])<18:reason='invalid_demographic'
                    elif table=='episodes':
                        a=date.fromisoformat(row['entry_date']);b=date.fromisoformat(row['exit_date']) if row['exit_date'] else CUTOFF+timedelta(days=1)
                        if row['child_id'] not in indices['children']:reason='orphan_child'
                        elif b<=a or a>CUTOFF or b>CUTOFF+timedelta(days=1):reason='invalid_episode_dates'
                        elif row['exit_date'] and row['exit_reason'] not in ['reunification','adoption','guardianship','other']:reason='invalid_exit_reason'
                    else:
                        day=date.fromisoformat(row['visit_date']);e=indices['episodes'].get(row['episode_id'])
                        if not e:reason='orphan_episode'
                        elif not date.fromisoformat(e['entry_date'])<=day<(date.fromisoformat(e['exit_date']) if e['exit_date'] else CUTOFF+timedelta(days=1)):reason='visit_outside_episode'
                        elif row['in_person'] not in ['0','1']:reason='invalid_visit_type'
                except (ValueError,KeyError):reason='missing_or_invalid_date_or_value'
            if reason:log(table,row,reason,'quarantined');continue
            kept.append(row)
        if table=='episodes':
            bychild=defaultdict(list)
            for row in kept:bychild[row['child_id']].append(row)
            overlaps=set()
            for group in bychild.values():
                group.sort(key=lambda x:x['entry_date'])
                for i,a in enumerate(group):
                    end=a['exit_date'] or '2026-01-01'
                    for b in group[i+1:]:
                        if b['entry_date']<end:overlaps.update([a['episode_id'],b['episode_id']])
            for row in kept:
                if row[key] in overlaps:log(table,row,'overlapping_episodes','quarantined')
            kept=[r for r in kept if r[key] not in overlaps]
        clean[table]=kept;indices[table]={r[key]:r for r in kept}
        write_csv(OUT/f'clean_{table}.csv',kept)
    write_csv(OUT/'quality_audit.csv',audit)
    return clean,audit

def eligible_months(entry,exit_date):
    """Full months only. Half-open episodes [entry, exit); complete follow-up cutoff."""
    start=date.fromisoformat(entry);end=date.fromisoformat(exit_date) if exit_date else CUTOFF+timedelta(days=1)
    m=date(start.year,start.month,1)
    while m<CUTOFF+timedelta(days=1):
        nxt=date(m.year+m.month//12,m.month%12+1,1)
        if m>=start and nxt<=end and nxt<=CUTOFF+timedelta(days=1):yield m.isoformat()[:7]
        if nxt>end:break
        m=nxt

def warehouse(clean):
    path=OUT/'warehouse.sqlite';path.unlink(missing_ok=True);db=sqlite3.connect(path)
    db.executescript('''PRAGMA foreign_keys=ON;
    CREATE TABLE children(child_id TEXT PRIMARY KEY,state TEXT NOT NULL,age_at_entry INTEGER CHECK(age_at_entry BETWEEN 0 AND 17));
    CREATE TABLE episodes(episode_id TEXT PRIMARY KEY,child_id TEXT REFERENCES children,entry_date TEXT NOT NULL,exit_date TEXT,exit_reason TEXT);
    CREATE TABLE visits(visit_id TEXT PRIMARY KEY,episode_id TEXT REFERENCES episodes,visit_date TEXT NOT NULL,in_person INTEGER CHECK(in_person IN(0,1)));
    CREATE TABLE child_months(episode_id TEXT REFERENCES episodes,month TEXT,quarter TEXT,state TEXT,age_group TEXT,PRIMARY KEY(episode_id,month));
    CREATE INDEX visits_episode_date ON visits(episode_id,visit_date);
    ''')
    for table in ['children','episodes','visits']:
        for row in clean[table]:db.execute(f'INSERT INTO {table} VALUES ({",".join("?" for _ in row)})',list(row.values()))
    children={c['child_id']:c for c in clean['children']}
    months=[]
    for e in clean['episodes']:
        child=children[e['child_id']];age=int(child['age_at_entry']);group='0–5' if age<6 else '6–12' if age<13 else '13–17'
        for m in eligible_months(e['entry_date'],e['exit_date']):
            q=m[:4]+'-Q'+str((int(m[5:])-1)//3+1);months.append((e['episode_id'],m,q,child['state'],group))
    db.executemany('INSERT INTO child_months VALUES (?,?,?,?,?)',months);db.commit()
    assert db.execute('PRAGMA foreign_key_check').fetchall()==[]
    return db,months

def metrics(db,months,clean):
    visitmonths={(v['episode_id'],v['visit_date'][:7]) for v in clean['visits'] if v['in_person']=='1'}
    counts=defaultdict(lambda:[0,0]);agecounts=defaultdict(lambda:[0,0])
    for e,m,q,s,a in months:
        counts[s,q][1]+=1;counts[s,q][0]+=int((e,m) in visitmonths)
        agecounts[s,q,a][1]+=1;agecounts[s,q,a][0]+=int((e,m) in visitmonths)
    sql=(ROOT/'measure_validation.sql').read_text()
    sql_rows={(s,q):[n,d] for s,q,n,d in db.execute(sql)}
    assert dict(counts)==sql_rows,'Independent SQL/Python numerator or denominator disagreement'
    rows=[dict(state=s,quarter=q,numerator=n,denominator=d,rate=rate(n,d),data_type='synthetic',measure='Full-month in-person visit coverage') for (s,q),(n,d) in sorted(counts.items())]
    write_csv(OUT/'synthetic_trends.csv',rows)
    # Small cells suppress both counts and rate. Not a production disclosure policy.
    disagg=[dict(state=s,quarter=q,age_group=a,numerator=n if d>=20 else None,denominator=d if d>=20 else None,rate=rate(n,d) if d>=20 else None,suppressed=d<20) for (s,q,a),(n,d) in sorted(agecounts.items())]
    write_csv(OUT/'synthetic_age_groups.csv',disagg)
    # Fictional agency submissions are intentionally generated with planted errors.
    submissions=[];reconciliation=[]
    for i,r in enumerate(rows):
        n,d=r['numerator'],r['denominator'];issue='none'
        if i in (8,20):d-=max(1,d//12);issue='omitted eligible child-months'
        if i in (14,32):n+=3;issue='counted multiple visits for the same child-month'
        submitted=round(rate(n,d),2)
        if i==42:submitted+=1;issue='reported rate does not match submitted counts'
        a=dict(state=r['state'],quarter=r['quarter'],submitted_numerator=n,submitted_denominator=d,submitted_rate=submitted)
        submissions.append(a)
        delta=submitted-r['rate'];ok=n==r['numerator'] and d==r['denominator'] and abs(delta)<=.00500001
        reconciliation.append(dict(**a,validated_numerator=r['numerator'],validated_denominator=r['denominator'],validated_rate=r['rate'],difference_pp=delta,status='Pass' if ok else 'Review',fixture_explanation=issue))
    write_csv(RAW/'fictional_agency_submissions.csv',submissions);write_csv(OUT/'agency_reconciliation.csv',reconciliation)
    return rows,disagg,reconciliation

def main():
    OUT.mkdir(exist_ok=True);RAW.mkdir(exist_ok=True)
    public=public_snapshot();synthetic_source();clean,audit=clean_sources();db,months=warehouse(clean);trends,disagg,reconciliation=metrics(db,months,clean);db.close()
    quality=[dict(table=t,raw=len(read_csv(RAW/f'{t}.csv')),clean=len(rows),deduplicated=sum(a['table']==t and a['action']=='deduplicated' for a in audit),quarantined=sum(a['table']==t and a['action']=='quarantined' for a in audit)) for t,rows in clean.items()]
    assert all(q['raw']==q['clean']+q['deduplicated']+q['quarantined'] for q in quality)
    write_csv(OUT/'quality_summary.csv',quality)
    payload=dict(public=public,trends=trends,disaggregation=disagg,reconciliation=reconciliation,quality=quality,audit=audit,cutoff=CUTOFF.isoformat(),states=STATES)
    (OUT/'dashboard_data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
    template=(ROOT/'dashboard_template.html').read_text();(OUT/'dashboard.html').write_text(template.replace('__PAYLOAD__',json.dumps(payload,ensure_ascii=False).replace('</','<\\/')))
    (ROOT/'docs/index.html').write_text((OUT/'dashboard.html').read_text())
    files=list((ROOT/'data').rglob('*.csv'))+[ROOT/'data/source/cfsr-march-2026.pdf',ROOT/'data/source/cfsr-march-2026.txt']
    manifest=dict(pipeline_version='1.0',generated_data_seed=1042026,source_retrieved='2026-10-08',source_url=SOURCE,cutoff=CUTOFF.isoformat(),files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},checks=dict(public_rows=len(public),public_arithmetic_pass=sum(r['arithmetic_pass'] for r in public),public_classification_pass=sum(r['classification_pass'] for r in public),synthetic_child_months=len(months),sql_python_exact_agreement=True,agency_review_rows=sum(r['status']=='Review' for r in reconciliation)))
    (OUT/'run_manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(manifest['checks'],indent=2))
if __name__=='__main__':main()
