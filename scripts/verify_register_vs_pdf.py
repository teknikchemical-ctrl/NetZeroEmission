import openpyxl,re
wb=openpyxl.load_workbook('/home/user/NetZeroEmission/Indonesia_NZE_Data_Grafik_v2 (4).xlsx',data_only=True)
ws=wb['D_Register_Sumber']
maps={'TIMES industry':'txt/3.txt','Biaya LUCF':'txt/4.txt','Co-firing biomassa di Indonesia':'txt/crea.txt'}
def norm(t): return re.sub(r'[\s ]','',t.replace('−','-').replace('–','-'))
pdf={k:norm(open(v,encoding='utf8').read()) for k,v in maps.items()}
nums=lambda s: re.findall(r'\d[\d.,]*\d|\d',str(s))
for key,txt in pdf.items():
    tot=bad=0; ex=[]
    for r in ws.iter_rows(min_row=6,values_only=True):
        if not r[1] or key not in r[1]: continue
        vs=[n for n in nums(r[4]) if len(re.sub(r'\D','',n))>=2]
        if not vs: continue
        tot+=1
        def variants(n):
            v={n,n.replace(',','.'),n.replace('.',','),n.replace(',','')}
            return v
        miss=[n for n in vs if not any(x in txt for x in variants(n))]
        if len(miss)==len(vs): bad+=1; ex.append((r[0],str(r[3])[:50],str(r[4])[:50],miss[:3]))
    print(key,'rows with numbers',tot,'no number found in PDF text',bad)
    for e in ex[:12]: print('   ',e)
