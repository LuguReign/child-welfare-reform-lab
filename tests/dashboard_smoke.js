// JavaScript/DOM logic smoke check. This is not a browser layout/accessibility test.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(__dirname+'/../output/dashboard.html','utf8');
const elements=new Map();
function el(id){if(!elements.has(id))elements.set(id,{id,value:id==='indicator'?'maltreatment':id==='state'?'KS':'',innerHTML:'',textContent:'',events:{},addEventListener(e,f){this.events[e]=f;}});return elements.get(id);}
const tabs=['public','demo','validation','methods'].map(id=>({dataset:{tab:id},events:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(e,f){this.events[e]=f}}));
const panels=tabs.map(t=>({id:t.dataset.tab,classList:{active:false,toggle(k,v){this.active=v}}}));
const document={getElementById:el,querySelectorAll:s=>s==='[data-tab]'?tabs:panels};
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
vm.runInNewContext(script,{document,console});
for(const k of ['maltreatment','recurrence','permanency_entry','permanency_12_23','permanency_24','reentry','stability']){el('indicator').value=k;el('indicator').events.change();assert(el('interval').innerHTML.includes('<svg'));assert.equal((el('publicTable').innerHTML.match(/<tr>/g)||[]).length,5);assert(!/NaN|undefined/.test(el('interval').innerHTML));}
for(const s of ['KS','MI','NM','TX']){el('state').value=s;el('state').events.change();assert.equal((el('trendTable').innerHTML.match(/<tr>/g)||[]).length,13);assert(!/NaN|undefined/.test(el('trend').innerHTML));}
for(const tab of tabs){tab.events.click();assert.equal(tab.attrs['aria-selected'],'true');assert.equal(panels.filter(p=>p.classList.active).length,1);}
assert.equal((el('reconciliation').innerHTML.match(/<tr>/g)||[]).length,6);
console.log('PASS: 7 indicator selections, 4 synthetic jurisdictions, 4 tab transitions, 5 reconciliation exceptions; no NaN/undefined chart values.');
