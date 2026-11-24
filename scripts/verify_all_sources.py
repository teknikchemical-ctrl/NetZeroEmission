"""Cocokkan setiap angka di D_Register_Sumber dengan teks PDF sumber di sources/ (lintas format ribuan dan desimal)."""
import openpyxl,re,sys,glob,os
MAP={'FOLU Net Sink 2030':'2022_KLHK','Transport ASI':'2024_Zahari','Industrial energy HEIO':'2025_Zain','Solar 2021':'2021_Sijabat','IEEFA 100 GW':'2026_IEEFA','ERIA CCS':'2025_ERIA','LPG to induction':'2024_Hilmiyati','Faktor emisi gambut':'2024_PNAS','RIL-C konsesi':'2024_Forests','Kelayakan co-firing':'1','Restorasi lahan terdegradasi':'2','TIMES industry':'3','Biaya LUCF':'4','Co-firing biomassa di Indonesia':'Cost Co Firing Biomass (1)','Tantangan sektor listrik':'PaperAndrew','Strategi ekonomi dan efisiensi':'Economic_Strategies','Optimasi skenario transisi':'Optimization_of_Electricity','Dampak inisiatif NZE':'Impact_of_Net_Zero','Analisis model arus':'Analysis_of_the_political','Biaya ekonomi dan fiskal':'At what cost','Jalur EBT dan target':'Evaluating renewable','Dekarbonisasi sektor listrik':'Optimizing power sector','Spesifikasi biosolar':'spesifikasi-b40','Penilaian siklus hidup biodiesel':'2025_LCA','Transformasi transportasi Jakarta':'Jakarta Transportation','Early retirement CFPP':'2026_Fadiilah','Rice cooker programme':'2025_Suntoro'}
def norm(t): return re.sub(r'[\s ­,]','',t.replace('−','-').replace('–','-'))
def load(stem):
    out=''
    for p in glob.glob(f'/tmp/claude-0/alltxt/{stem}*.txt'): out+=norm(open(p,encoding='utf8',errors='ignore').read())
    return out
def variants(n):
    n=n.strip('.,'); v={n.replace(',',''),n.replace(',','.'),n.replace('.','').replace(',','')}
    v|={x.rstrip('0').rstrip('.') if '.' in x else x for x in set(v)}
    return v
wb=openpyxl.load_workbook(sys.argv[1] if len(sys.argv)>1 else 'Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx',read_only=True,data_only=True)
ws=wb['D_Register_Sumber']; texts={}
res={}
for r in ws.iter_rows(min_row=6,values_only=True):
    if not r[1]: continue
    stem=next((s for k,s in MAP.items() if k in r[1]),None)
    if not stem: continue
    texts.setdefault(stem,load(stem))
    t=texts[stem]
    vs=[n for n in re.findall(r'\d[\d.,]*\d|\d',str(r[4])) if len(re.sub(r'\D','',n))>=2]
    if not vs: continue
    d=res.setdefault(stem,[0,0,[]]); d[0]+=1
    if all(not any(x in t for x in variants(n)) for n in vs): d[1]+=1; d[2].append((r[0],str(r[3])[:45],str(r[4])[:35]))
for stem,(tot,bad,ex) in res.items():
    print(f'{stem[:34]:34s} baris berangka {tot:3d} tidak ditemukan {bad:2d}')
    for e in ex[:6]: print('     ',e)
