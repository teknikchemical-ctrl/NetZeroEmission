"""Inventaris semua sumber (PDF, CSV) di sources/, papers/, data/: metadata, SHA-256, halaman, ekstrak abstrak dan kesimpulan; tulis notes/INVENTARIS_SUMBER.csv dan bahan catatan per sumber di /tmp/claude-0/inv.json."""
import os,re,json,hashlib,subprocess,glob,csv
R='/home/user/NetZeroEmission'
files=[]
for d in ('sources','papers','data'):
    for p in sorted(glob.glob(f'{R}/{d}/*')):
        if p.endswith(('.pdf','.csv')): files.append(p)
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def pdfinfo(p):
    o=subprocess.run(['pdfinfo',p],capture_output=True,text=True).stdout
    g=lambda k: (re.search(k+r':\s*(.*)',o) or [None,''])[1].strip()
    return g('Title'),g('Author'),g('Pages')
def text(p):
    return subprocess.run(['pdftotext','-l','40',p,'-'],capture_output=True,text=True).stdout
def excerpt(t,pat,n=700):
    m=re.search(pat,t,re.I)
    if not m: return ''
    s=t[m.end():m.end()+n]; return re.sub(r'\s+',' ',s).strip()
inv=[];seen={}
for i,p in enumerate(files,1):
    rel=os.path.relpath(p,R); h=sha(p); b=os.path.basename(p)
    rec=dict(id=f'S{i:03d}',path=rel,name=b,type=os.path.splitext(b)[1][1:],sha=h,size=os.path.getsize(p),dup_of=seen.get(h,''))
    seen.setdefault(h,f'S{i:03d}')
    if p.endswith('.pdf'):
        ti,au,pg=pdfinfo(p); t=text(p)
        rec.update(title=ti,author=au,pages=pg,chars=len(t),first=re.sub(r'\s+',' ',t[:300]),abstract=excerpt(t,r'abstract|abstrak|ringkasan|executive summary'),conclusion=excerpt(t,r'\bconclusions?\b|kesimpulan|penutup',600))
    else:
        rows=list(csv.reader(open(p,encoding='utf-8-sig')))
        rec.update(title='',author='',pages='',chars=0,first=' | '.join(rows[0])[:300] if rows else '',abstract='',conclusion='',nrows=len(rows)-1)
    inv.append(rec)
json.dump(inv,open('/tmp/claude-0/inv.json','w'),ensure_ascii=False,indent=1)
print(len(inv),'berkas;',sum(1 for r in inv if r['dup_of']),'duplikat isi')
