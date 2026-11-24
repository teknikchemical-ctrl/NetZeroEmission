import re,glob,zipfile,sys,openpyxl
from openpyxl.utils import range_boundaries
p='/home/user/NetZeroEmission/Indonesia_NZE_Data_Grafik_v2 (4).xlsx'
z=zipfile.ZipFile(p)
wb=openpyxl.load_workbook(p,data_only=True)
# map chart -> sheet via drawings
rels={}
for n in z.namelist():
    m=re.match(r'xl/drawings/_rels/drawing(\d+)\.xml\.rels',n)
    if m: rels[m.group(1)]=re.findall(r'charts/(chart\d+)\.xml',z.read(n).decode())
issues=[]
cnt=0
for n in sorted(z.namelist()):
    m=re.match(r'xl/charts/(chart\d+)\.xml$',n)
    if not m: continue
    cnt+=1
    s=re.sub(r'<(/?)c:',r'<\1',z.read(n).decode())
    t=re.findall(r'<a:t>([^<]*)</a:t>',s); title=t[0][:55] if t else '(no title)'
    sers=re.findall(r'<ser>.*?</ser>',s,re.S)
    if not sers: issues.append((m.group(1),title,'no series')); continue
    for i,se in enumerate(sers):
        name=re.search(r'<tx>.*?<(?:v|f)>([^<]*)</(?:v|f)>',se,re.S)
        name=name.group(1) if name else None
        for kind in ('val','yVal','xVal','cat'):
            for f in re.findall(r'<%s>.*?<f>([^<]*)</f>'%kind,se,re.S):
                sh,rg=f.rsplit('!',1); sh=sh.strip("'")
                if sh not in wb.sheetnames: issues.append((m.group(1),title,f'{name}: missing sheet {sh}')); continue
                ws=wb[sh]
                try: c1,r1,c2,r2=range_boundaries(rg.replace('$',''))
                except: issues.append((m.group(1),title,f'bad ref {f}')); continue
                vals=[ws.cell(r,c).value for r in range(r1,r2+1) for c in range(c1,c2+1)]
                num=[v for v in vals if isinstance(v,(int,float))]
                if kind in('val','yVal') and not num: issues.append((m.group(1),title,f'{name}: series has NO numeric data {f}'))
        if name and name.startswith('Indeks'): issues.append((m.group(1),title,'legend name bad'))
print('charts',cnt); 
for i in issues: print(i)
print(len(issues),'issues')
