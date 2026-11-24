"""Lembar solusi energi non-RUPTL (pensiun dini, CCS TJB, co-firing, B40), K_Studi, Q_Portofolio."""
import sys; sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from modelkit import *; import chartkit as ck; import src
import importlib.util
def _load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); sys.argv=['x']; spec.loader.exec_module(m); return m
def er(txt,col=3,start=6,end=70):  # D_Energi_Potensi row by item text prefix
    return src.find_row('D_Energi_Potensi',txt,col=col,start=start,end=end)
def single(name,nomor,label,rowC,desc,params_rows,srcrows,extra_inputs,chart_title,cost_cells=None,find_extra=None):
    """srcrows: list of (label,low_formula,high_formula,unit,status,source,style)"""
    sh=Sheet(name,'FF1BAF7A')
    sh.t('A1',f'Lembar {nomor}. Solusi {label}: tabel teknis, pengurangan emisi menurut sumber, biaya, dan pelaksanaan','title')
    sh.t('A2',desc,'title')
    # A summary
    sh.t('B5',f'Tabel {nomor}.A. Ringkasan 2030 (C_Solusi_2030)','tbl')
    for c,t in zip('BCDEFG',['Butir','Rendah','Tinggi','Satuan','Status','Sumber']): sh.t(f'{c}6',t,'hdr')
    S_=[('Pengurangan 2030',f'C_Solusi_2030!E{rowC}',f'C_Solusi_2030!F{rowC}','MtCO2e per tahun','n2l'),('Biaya per tCO2',f'C_Solusi_2030!G{rowC}',f'C_Solusi_2030!H{rowC}','USD per tCO2','n2l'),
        ('Biaya tahunan tengah',f'C_Solusi_2030!J{rowC}',f'C_Solusi_2030!J{rowC}','USD juta per tahun','n1l')]
    for i,(a,fl,fh,u,sty) in enumerate(S_):
        r=7+i; sh.t(f'B{r}',a); sh.f(f'C{r}',fl,sty); sh.f(f'D{r}',fh,sty); sh.t(f'E{r}',u); sh.f(f'F{r}',f'C_Solusi_2030!Q{rowC}','tl'); sh.f(f'G{r}',f'C_Solusi_2030!R{rowC}','tl')
    sh.t('B10','Persen selisih energi 2030 (rendah, tinggi)'); sh.f('C10','C7/B_Selisih_Penyebab!$C$7','pc'); sh.f('D10','D7/B_Selisih_Penyebab!$C$7','pc'); sh.t('E10','fraksi'); sh.t('F10','AC'); sh.t('G10','B_Selisih_Penyebab')
    sh.t('B11','Catatan C_Solusi_2030'); sh.f('C11',f'C_Solusi_2030!S{rowC}','tl'); sh.merges.append('C11:G11')
    # B params
    sh.t('B14',f'Tabel {nomor}.B. Parameter teknis bersumber (tautan ke D_Teknis_Opsi)','tbl')
    for c,t in zip('BCDEFGH',['Opsi','Kelas parameter','Parameter','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}15',t,'hdr')
    for i,r in enumerate(params_rows):
        rr=16+i
        sh.f(f'B{rr}',f'D_Teknis_Opsi!C{r}','tl'); sh.f(f'C{rr}',f'D_Teknis_Opsi!D{r}','tl'); sh.f(f'D{rr}',f'D_Teknis_Opsi!E{r}','tl'); sh.f(f'E{rr}',f'D_Teknis_Opsi!F{r}','tl'); sh.f(f'F{rr}',f'D_Teknis_Opsi!G{r}','tl'); sh.f(f'G{rr}',f'D_Teknis_Opsi!I{r}','tl'); sh.f(f'H{rr}',f'D_Teknis_Opsi!J{r}','tl')
    r0=16+len(params_rows)+2
    # C sources comparison
    sh.t(f'B{r0}',f'Tabel {nomor}.C. Pengurangan emisi menurut sumber (MtCO2e per tahun, kecuali dinyatakan lain)','tbl')
    for c,t in zip('BCDEFG',['Sumber','Rendah','Tinggi','Satuan','Status','Rujukan']): sh.t(f'{c}{r0+1}',t,'hdr')
    sh.t(f'H{r0+1}','Rentang (tinggi dikurangi rendah)','hdr')
    for i,(a,lo,hi,u,st,so,sty) in enumerate(srcrows):
        r=r0+2+i; sh.t(f'B{r}',a)
        if isinstance(lo,(int,float)): sh.n(f'C{r}',lo,'n2i')
        else: sh.f(f'C{r}',lo,sty)
        if isinstance(hi,(int,float)): sh.n(f'D{r}',hi,'n2i')
        else: sh.f(f'D{r}',hi,sty)
        sh.t(f'E{r}',u); sh.t(f'F{r}',st); sh.t(f'G{r}',so); sh.f(f'H{r}',f'D{r}-C{r}','n2')
    n=len(srcrows); rl=r0+2+n
    sh.t(f'B{rl}','Selisih energi 2030 (CPOS dikurangi LCCP_L)'); sh.f(f'C{rl}','B_Selisih_Penyebab!C7','n2l'); sh.f(f'D{rl}','B_Selisih_Penyebab!C7','n2l'); sh.t(f'E{rl}','MtCO2e'); sh.t(f'F{rl}','P'); sh.t(f'G{rl}','D_SNDC'); sh.f(f'H{rl}',f'D{rl}-C{rl}','n2')
    # D extra
    r2=rl+3
    sh.t(f'B{r2}',f'Tabel {nomor}.D. Hitungan sederhana dan masukan bersumber','tbl')
    for c,t in zip('BCDEF',['Butir','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}{r2+1}',t,'hdr')
    refs={}
    for i,(key,a,v,u,st,so,kind) in enumerate(extra_inputs):
        r=r2+2+i; refs[key]=r; sh.t(f'B{r}',a)
        if kind=='in': sh.n(f'C{r}',v,'n2i')
        elif kind=='link': sh.f(f'C{r}',v,'n2l')
        else:
            f_=v
            for k,rr in refs.items(): f_=f_.replace('{'+k+'}',f'C{rr}')
            sh.f(f'C{r}',f_,'n2')
        sh.t(f'D{r}',u); sh.t(f'E{r}',st); sh.t(f'F{r}',so)
    rg=r2+2+len(extra_inputs)+1
    sh.t(f'B{rg}',f'Tabel {nomor}.E. Pelaksanaan saat ini (diisi tim; kosong sampai ada data bersumber)','tbl')
    for c,t in zip('BCDE',['Butir','Nilai','Satuan','Kode WP']): sh.t(f'{c}{rg+1}',t,'hdr')
    for i,(a,u,wp) in enumerate([('Capaian terhadap target 2030','fraksi','WP-F'),('Tahun data capaian','tahun','WP-F')]):
        sh.t(f'B{rg+2+i}',a); sh.blank(f'C{rg+2+i}','n2i'); sh.t(f'D{rg+2+i}',u); sh.t(f'E{rg+2+i}',wp)
    # charts
    cat=f'{name}!$B${r0+2}:$B${r0+1+n}'
    def rg_(col): return f'{name}!${col}${r0+2}:${col}${r0+1+n}'
    c1=ck.chart_xml(f'Gambar {nomor}.1. {chart_title}: pengurangan emisi menurut sumber (MtCO2e per tahun), rentang berarsir',
        [dict(base_ref=rg_('C'),band_ref=rg_('H'),name='Rentang rendah sampai tinggi',fill='F4B183')],
        [dict(val_ref=rg_('D'),name='Tinggi',color='C00000',pos='t'),dict(val_ref=rg_('C'),name='Rendah',color='1F4E79',pos='b')],
        'MtCO2e per tahun','Sumber',cat,cat_numeric=False,yfmt='#,##0.0')
    sh.f('A3','"Temuan utama: '+label+': pengurangan 2030 pada C_Solusi "&ROUND(C7,1)&" sampai "&ROUND(D7,1)&" MtCO2e ("&ROUND(C10*100,1)&" sampai "&ROUND(D10*100,1)&" persen selisih energi); sumber lain pada Tabel C berkisar "&ROUND(MIN(C'+str(r0+2)+':C'+str(r0+1+n)+'),1)&" sampai "&ROUND(MAX(D'+str(r0+2)+':D'+str(r0+1+n)+'),1)&" MtCO2e."','title')
    sh.width('A','A',3); sh.width('B','B',58); sh.width('C','C',26); sh.width('D','D',30); sh.width('E','H',20); sh.width('G','G',44)
    sh.charts=[(c1,(1,rg+5,7600000,3900000))]
    sh.refs=dict(r0=r0,n=n,r2=r2,refs=refs,rg=rg)
    return sh
def S_Pensiun():
    return single('S_Pensiun_Dini',122,'pensiun dini PLTU',30,
      'Lapis resmi (CM2, 36 Mt) dan turunan (enam PLTU, bagian tambahan 57,5 Mt). Pengurangan emisi = emisi unit yang dipensiunkan; dibandingkan beberapa sumber bersumber. Biaya dari C_Solusi_2030 (13,49 USD per tCO2). Hanya angka bersumber dan hitungan sederhana.',
      [60,61,62,63,64,65,66],
      [('Resmi CM2: pensiun dini (D_Solusi_Kuantif)','C_Solusi_2030!E30','C_Solusi_2030!F30','MtCO2e','P','C_Solusi_2030 B1','n2l'),
       ('Turunan: enam PLTU, CO2 dihindari (Fadiilah dan Dye 2026)','D_Teknis_Opsi!F61','D_Teknis_Opsi!F61','MtCO2e (basis emisi 2023)','R','D_Teknis_Opsi baris 61','n2l'),
       ('Bagian tambahan enam PLTU di atas resmi (C_Solusi B4)','C_Solusi_2030!E33','C_Solusi_2030!F33','MtCO2e','A','C_Solusi_2030 B4','n2l'),
       ('Pihak ketiga: pensiun segera 4,5 GW on-grid',f'D_Energi_Potensi!E{er("Pensiun dini PLTU on-grid segera (4,5 GW)")}',f'D_Energi_Potensi!E{er("Pensiun dini PLTU on-grid segera (4,5 GW)")}','MtCO2 per tahun','E','D_Energi_Potensi','n2l')],
      [('inv1','Biaya pensiun dipercepat, rendah (pihak ketiga)',f'D_Energi_Potensi!E{er("Biaya pensiun dipercepat")}','USD miliar','E','D_Energi_Potensi','link'),
       ('inv2','Biaya pensiun dipercepat, tinggi (pihak ketiga)',f'D_Energi_Potensi!E{er("Biaya pensiun dipercepat",start=er("Biaya pensiun dipercepat")+1)}','USD miliar','E','D_Energi_Potensi','link'),
       ('cap','Kapasitas enam PLTU usulan (MW)','D_Teknis_Opsi!F60','MW','R','Fadiilah dan Dye 2026','link'),
       ('jetp','Pensiun dini sebelum 2030, skenario JETP CIPP (GW)',f'D_JETP!C{src.find_row("D_JETP","Pensiun dini PLTU sebelum 2030",col=2,start=1,end=30)}','GW','P','D_JETP (CIPP Tabel 4.3-1)','link'),
       ('cost','Biaya bersih pensiun (USD per tCO2)','C_Solusi_2030!G30','USD per tCO2','AC','C_Solusi_2030 B1','link'),
       ('ann','Biaya tahunan resmi: pengurangan x biaya (USD juta per tahun)','C_Solusi_2030!E30*{cost}','USD juta per tahun','AC','hitungan sederhana','calc')],
      'Pensiun dini PLTU')
def S_CCS():
    return single('S_CCS_TJB',123,'CCS PLTU Tanjung Jati B',34,
      'Dua unit 1.000 MW dengan laju tangkap 0,95 dan faktor kapasitas 0,86 menangkap sekitar 13 MtCO2 per tahun (ERIA CCS 2025). Biaya per tCO2 dari C_Solusi_2030; penalti energi CCS belum ada (WP-J). Hanya angka bersumber dan hitungan sederhana.',
      [67,68,69],
      [('C_Solusi B5: dua unit TJB (rendah)','C_Solusi_2030!E34','C_Solusi_2030!F34','MtCO2e','AC','C_Solusi_2030 B5','n2l'),
       ('Satu unit 1.000 MW (D_Teknis_Opsi)','D_Teknis_Opsi!F67','D_Teknis_Opsi!F67','MtCO2 per tahun','R','D_Teknis_Opsi baris 67','n2l')],
      [('capex1','Biaya modal PLTU uap dengan CCS, LEAP (USD per kW)','C_Biaya_Teknologi!E15','USD per kW','E','C_Biaya_Teknologi (Nursidik 2025)','link'),
       ('capex2','Biaya modal PLTU uap dengan CCS (USD per kW)',3460,'USD per kW','E','Sunanda dkk. 2026 Tabel 5','in'),
       ('cost_lo','Biaya per tCO2 rendah','C_Solusi_2030!G34','USD per tCO2','AC','C_Solusi_2030 B5','link'),
       ('cost_hi','Biaya per tCO2 tinggi','C_Solusi_2030!H34','USD per tCO2','AC','C_Solusi_2030 B5','link'),
       ('ann_lo','Biaya tahunan rendah (USD juta per tahun)','C_Solusi_2030!E34*{cost_lo}','USD juta per tahun','AC','hitungan sederhana','calc'),
       ('ann_hi','Biaya tahunan tinggi (USD juta per tahun)','C_Solusi_2030!F34*{cost_hi}','USD juta per tahun','AC','hitungan sederhana','calc')],
      'CCS TJB')
def S_Cofiring():
    return single('S_Cofiring',124,'co-firing biomassa',27,
      'Lapis A (dalam CM1): target PLN 11 MtCO2 per tahun. Dibandingkan rentang pengurangan skenario pasokan limbah biomassa (Squire dkk. 2024, K125). Realisasi 14,3 persen (2024). Faktor emisi biomassa dan pembukuan netral karbon belum diputuskan (WP-F, R20).',
      [r for r in TRBIO],
      [('Lapis A CM1: target PLN (C_Solusi A4)','C_Solusi_2030!E27','C_Solusi_2030!F27','MtCO2e','T','C_Solusi_2030 A4','n2l'),
       ('Squire dkk. 2024: skenario Rendah sampai Tinggi, 2030',14.2,152.5,'MtCO2 per tahun','E','D_Register_Sumber (Squire 2024, Gambar 6)','n2i')],
      [('ratio','Capaian terhadap target (C_Solusi Tabel 32.D)','C_Solusi_2030!D72','fraksi','AC','C_Cofiring_Biaya bagian D','link'),
       ('now','Pengurangan pada pelaksanaan saat ini (MtCO2e per tahun)','C_Solusi_2030!E27*{ratio}','MtCO2e','AC','hitungan sederhana','calc'),
       ('sup','Pasokan limbah biomassa tersedia (miliar MJ per tahun)',504.4,'miliar MJ','E','Squire dkk. 2024 Tabel 1','in'),
       ('dem','Permintaan skenario Menengah (target PLN, miliar MJ per tahun)',651.7,'miliar MJ','E','Squire dkk. 2024 Tabel 1','in'),
       ('cov','Pasokan dibagi permintaan Menengah','{sup}/{dem}','fraksi','AC','hitungan sederhana','calc'),
       ('cl','Biaya per tCO2 rendah (campuran realisasi)','C_Solusi_2030!G27','USD per tCO2','AC','C_Cofiring_Biaya','link'),
       ('ch','Biaya per tCO2 tinggi (harga ekspor)','C_Solusi_2030!H27','USD per tCO2','AC','C_Cofiring_Biaya','link')],
      'Co-firing biomassa')
def S_B40():
    return single('S_B40',125,'biodiesel B40',26,
      'Klaim pengurangan ESDM dibandingkan hitungan sederhana: volume biodiesel dikali faktor emisi solar. Hitungan memakai pembukuan biogenik netral tanpa alih guna lahan CPO (K138); faktor siklus hidup dan selisih harga per liter (biaya) belum diekstrak (R1).',
      [r for r in TRBF],
      [('Klaim ESDM (C_Solusi A3)','C_Solusi_2030!E26','C_Solusi_2030!F26','MtCO2e','E','C_Solusi_2030 A3','n2l'),
       ('ESDM sampai 2025 (catatan pengguna, K122)',32.2,32.2,'MtCO2e','E','K_Konflik K122','n2i')],
      [('vol','Volume biodiesel 2025 (alokasi)',15.62,'juta kL','E','Fitrady dkk. 2026','in'),
       ('ef','Faktor emisi solar',2.67,'kg CO2 per liter','R','Robbi 2026 Tabel 7 (Permenperin 48 Tahun 2020)','in'),
       ('calc','Hitung: volume x faktor (biogenik netral, tanpa alih guna lahan)','{vol}*{ef}','MtCO2e per tahun','AC','hitungan sederhana: juta kL x kg per L = MtCO2','calc'),
       ('pso','Volume bersubsidi (PSO) 2025',7.54,'juta kL','E','Fitrady dkk. 2026','in'),
       ('calcpso','Hitung untuk volume bersubsidi saja','{pso}*{ef}','MtCO2e per tahun','AC','hitungan sederhana','calc'),
       ('cap','Kapasitas produksi biodiesel',15.6,'juta kL','E','Fitrady dkk. 2026','in'),
       ('b50','Kebutuhan B50',20.1,'juta kL','E','Fitrady dkk. 2026 (APROBI 2025)','in'),
       ('calcb50','Hitung B50 (kebutuhan x faktor)','{b50}*{ef}','MtCO2e per tahun','AC','hitungan sederhana','calc')],
      'B40')
d_=src.ws('D_Teknis_Opsi'); TRBIO=[r for r in range(6,320) if d_.cell(r,3).value=='Biomassa']
TRBF=[r for r in range(6,320) if d_.cell(r,3).value=='Biofuel (B40 dan B50)']
if __name__=='__main__':
    bm=_load('bmod','/home/user/NetZeroEmission/scripts/09_build_model_B.py'); gp=bm.B_Garis_Pembangunan(); sel=bm.B_Selisih(gp)
    sheets=[gp,sel,S_Pensiun(),S_CCS(),S_Cofiring(),S_B40()]
    cache,errs=build('/tmp/claude-0/base_model.xlsx','/tmp/claude-0/stageX.xlsx',sheets,[])
    print([e for e in errs if 'NA()' not in e[3]][:6])
    for s in sheets[2:]: print(s.name,cache.get((s.name,'A3'),'')[:250])

def K_Studi(res,b40row):
    sh=Sheet('K_Studi','FF7F7F7F'); r_=dict((c['name'],s) for c,s in res)
    sh.t('A1','Lembar 126. Konkordansi studi: kapasitas 2030 menurut JETP CIPP dibanding RUPTL, dan angka per solusi menurut studi yang tercatat','title')
    sh.t('A2','Menyandingkan angka dari studi mapan yang sudah tercatat di workbook, tanpa memilih satu dan tanpa menjumlahkannya. Periode RUPTL (kumulatif 2025 sampai 2030) tidak sama dengan JETP (2022 sampai 2030); perbedaan periode dicatat. Studi lain yang perlu dikumpulkan tim tercantum di RESEARCH_PLAN_TIM.md (WP-K).','title')
    sh.t('B5','Tabel 126.A. Kapasitas terbarukan 2030: JETP CIPP (tambahan 2022 ke 2030) dibanding RUPTL (kumulatif 2025 sampai 2030), GW','tbl')
    for c,t in zip('BCDEFGHI',['Teknologi','JETP 2022','JETP 2030','JETP tambahan','RUPTL RE Base kumulatif 2030','RUPTL ARED kumulatif 2030','JETP tambahan dikurangi ARED','Emisi digantikan ARED 2030 (MtCO2, tengah)']): sh.t(f'{c}6',t,'hdr')
    jr=lambda t: src.find_row('D_JETP',t,col=2,start=27,end=35)
    mp=[('PV surya',['S_Surya']),('Tenaga air',['S_PLTA','S_Mini_Hidro']),('Bayu',['S_Angin']),('Panas bumi',['S_Panas_Bumi']),('Bioenergi',['S_Bioenergi'])]
    K='K'
    for i,(t,sheets) in enumerate(mp):
        r=7+i; j=jr(t); sh.t(f'B{r}',t); sh.f(f'C{r}',f'D_JETP!C{j}','n1l'); sh.f(f'D{r}',f'D_JETP!D{j}','n1l'); sh.f(f'E{r}',f'D_JETP!E{j}','n1l')
        sh.f(f'F{r}','+'.join(f'{s}!{K}{r_[s].rows["rd"]["D3"]}' for s in sheets)+'','n1'); 
        sh.cells[f'F{r}']=('f','('+'+'.join(f'{s}!{K}{r_[s].rows["rd"]["D3"]}' for s in sheets)+')/1000',S['n1'])
        sh.f(f'G{r}','('+'+'.join(f'{s}!{K}{r_[s].rows["rd"]["D4"]}' for s in sheets)+')/1000','n1')
        sh.f(f'H{r}',f'E{r}-G{r}','n1'); sh.f(f'I{r}','+'.join(f'{s}!{K}{r_[s].rows["re"]["E7"]}' for s in sheets),'n2')
    sh.t('B13','Jumlah'); 
    for c in 'EFGHI': sh.f(f'{c}13',f'SUM({c}7:{c}11)','n1' if c!='I' else 'n2')
    sh.t('B14','Catatan 126.A. JETP CIPP memuat tambahan EBT jauh lebih besar daripada RUPTL 2025 sampai 2034 pada 2030 (terutama surya); selisih ini adalah temuan antar studi, bukan kesalahan data. Periode, definisi on-grid, dan kapasitas penyimpanan berbeda (D_JETP, D_RUPTL_Tambahan).','note'); sh.merges.append('B14:I14')
    sh.t('B17','Tabel 126.B. Angka per solusi menurut studi yang tercatat (tidak dijumlahkan)','tbl')
    for c,t in zip('BCDEFGH',['Solusi','Studi atau sumber','Besaran','Nilai','Satuan','Tahun atau basis','Status']): sh.t(f'{c}18',t,'hdr')
    E=lambda t,**k: er(t,**k)
    rows=[('Pensiun dini PLTU','D_Solusi_Kuantif (resmi, C_Solusi B1)','Pengurangan','C_Solusi_2030!E30','MtCO2e per tahun','2030 (CM2)','P'),
          ('Pensiun dini PLTU','Fadiilah dan Dye 2026 (enam PLTU)','Pengurangan','D_Teknis_Opsi!F61','MtCO2 per tahun','basis emisi 2023','R'),
          ('Pensiun dini PLTU','Studi pihak ketiga (D_Energi_Potensi)','Pengurangan segera 4,5 GW',f'D_Energi_Potensi!E{E("Pensiun dini PLTU on-grid segera (4,5 GW)")}','MtCO2 per tahun','segera','E'),
          ('Pensiun dini PLTU','JETP CIPP','Pensiun sebelum 2030','D_JETP!C'+str(src.find_row("D_JETP","Pensiun dini PLTU sebelum 2030",col=2,start=1,end=30)),'GW','2030','P'),
          ('Pensiun dini PLTU','Studi pihak ketiga (D_Energi_Potensi)','Batalkan sembilan PLTU baru',f'D_Energi_Potensi!E{E("Batalkan sembilan PLTU baru dari pipeline PLN")}','MtCO2 kumulatif','kumulatif','E'),
          ('PLTU captive','Ember via D_Energi_Potensi','Emisi 2024',f'D_Energi_Potensi!E{E("Emisi PLTU captive fosil")}','MtCO2','2024','E'),
          ('PLTU captive','JETP 2025 via D_Energi_Potensi','Kapasitas semua bahan bakar',f'D_Energi_Potensi!E{E("Kapasitas captive semua bahan bakar")}','GW','2024','E'),
          ('Surya','IESR via D_Energi_Potensi','Terpasang',f'D_Energi_Potensi!E{E("Surya terpasang")}','GW','kuartal 1 2026','E'),
          ('Surya','JETP CIPP','PV surya 2030','D_JETP!D'+str(jr('PV surya')),'GW','2030','P'),
          ('Surya','D_Energi_Potensi','Jalur komitmen net zero',f'D_Energi_Potensi!E{E("Surya pada jalur komitmen net zero")}','GW','jalur','E'),
          ('Surya','D_Energi_Potensi','Program 100 GWp: investasi',f'D_Energi_Potensi!E{E("Program 100 GWp: investasi sampai 2030")}','USD miliar','sampai 2030','E'),
          ('CCS PLTU','ERIA CCS 2025 (D_Teknis_Opsi)','Satu unit 1.000 MW','D_Teknis_Opsi!F67','MtCO2 per tahun','CF 0,86','R'),
          ('Co-firing','PLN dan ENDC (C_Solusi A4)','Pengurangan','C_Solusi_2030!E27','MtCO2e per tahun','2030','T'),
          ('Co-firing','Squire dkk. 2024','Rentang skenario rendah',14.2,'MtCO2 per tahun','2030','E'),
          ('Co-firing','Squire dkk. 2024','Rentang skenario tinggi',152.5,'MtCO2 per tahun','2030','E'),
          ('B40','Klaim ESDM (C_Solusi A3)','Pengurangan','C_Solusi_2030!E26','MtCO2e per tahun','2025','E'),
          ('B40','Hitung dari Fitrady dkk. 2026 dan Robbi 2026','Volume x faktor solar','S_B40!C'+str(0),'MtCO2e per tahun','2025','AC')]
    # B40 calc cell reference resolved later
    for i,(a,b,c_,v,u,y,st) in enumerate(rows):
        r=19+i; sh.t(f'B{r}',a); sh.t(f'C{r}',b); sh.t(f'D{r}',c_)
        if isinstance(v,(int,float)): sh.n(f'E{r}',v,'n2i')
        elif v=='S_B40!C0': sh.f(f'E{r}',f'S_B40!C{b40row}','n2l')
        else: sh.f(f'E{r}',v,'n2l')
        sh.t(f'F{r}',u); sh.t(f'G{r}',y); sh.t(f'H{r}',st)
    sh.width('A','A',3); sh.width('B','B',26); sh.width('C','C',44); sh.width('D','D',30); sh.width('E','I',20)
    cats='K_Studi!$B$7:$B$11'
    c1=ck.chart_xml('Gambar 126.1. Kapasitas terbarukan 2030: JETP dibanding RUPTL (GW, kiri) dan emisi yang digantikan ARED (MtCO2, kanan)',[],
        [dict(val_ref='K_Studi!$E$7:$E$11',name_ref='K_Studi!$E$6',name='JETP tambahan',color='2E7D32',pos='t',fmt='#,##0.0'),
         dict(val_ref='K_Studi!$F$7:$F$11',name_ref='K_Studi!$F$6',name='RUPTL RE Base',color='1F4E79',pos='b',fmt='#,##0.0'),
         dict(val_ref='K_Studi!$G$7:$G$11',name_ref='K_Studi!$G$6',name='RUPTL ARED',color='7F7F7F',pos='b',fmt='#,##0.0',labels=False),
         dict(val_ref='K_Studi!$I$7:$I$11',name_ref='K_Studi!$I$6',name='Emisi digantikan ARED (kanan)',color='C00000',pos='t',sec=True,fmt='#,##0.0',dash='sysDash')],
        'GW','Teknologi',cats,cat_numeric=False,yfmt='#,##0',ytitle2='MtCO2 per tahun',yfmt2='#,##0')
    sh.charts=[(c1,(1,41,7600000,3900000))]
    sh.f('A3','"Temuan utama: JETP CIPP menambah "&ROUND(E7,1)&" GW surya pada 2030 sedangkan RUPTL RE Base mencatat "&ROUND(F7,1)&" GW dan ARED "&ROUND(G7,1)&" GW; secara total JETP "&ROUND(E13,1)&" GW terhadap RUPTL ARED "&ROUND(G13,1)&" GW (periode berbeda)."','title')
    return sh
def Q_Portofolio(pf,res,fsheets):
    sh=Sheet('Q_Portofolio','FF7F7F7F'); pos=pf.pos
    sh.t('A1','Lembar 127. Pemeriksaan portofolio dan lembar solusi','title')
    sh.t('A2','Pemeriksaan otomatis agar tidak ada hitung ganda atau angka tanpa asal: jumlah lapis sama dengan C_Solusi_2030, rantai hitung FOLU sama dengan C_Portofolio_FOLU_2030, faktor kapasitas wajar, dan jumlah sektor sama dengan total SNDC.','title')
    for c,t in zip('BCDEF',['Pemeriksaan','Nilai','Toleransi','Hasil','Penjelasan']): sh.t(f'{c}5',t,'hdr')
    fe,le,ff,lf=pos['first_en'],pos['last_en'],pos['first_fo'],pos['last_fo']
    checks=[('Jumlah lapis B energi (P_Portofolio) dikurangi C_Solusi_2030',f'ABS(P_Portofolio!G{le+1}-SUM(C_Solusi_2030!E30:E36))+ABS(P_Portofolio!H{le+1}-SUM(C_Solusi_2030!F30:F36))',0.001,'Jumlah rendah dan tinggi harus sama'),
            ('Jumlah lapis B FOLU (P_Portofolio) dikurangi C_Solusi_2030',f'ABS(P_Portofolio!G{lf+1}-SUM(C_Solusi_2030!E55:E65))+ABS(P_Portofolio!H{lf+1}-SUM(C_Solusi_2030!F55:F65))',0.001,'Jumlah rendah dan tinggi harus sama'),
            ('Rantai hitung 10 lembar FOLU dikurangi C_Portofolio_FOLU_2030','+'.join(f'{s.name}!C30' for s in fsheets),0.001,'Luas x faktor sama dengan hasil C_Portofolio_FOLU_2030'),
            ('Faktor kapasitas di luar (0, 1] pada 7 lembar terbarukan','+'.join(f'IF(AND({c["name"]}!C17>0,{c["name"]}!C17<=1),0,1)' for c,_ in res),0,'Setiap faktor kapasitas harus wajar'),
            ('Jumlah sektor SNDC dikurangi neto, selisih 2030 (MtCO2e)','ABS(SUM(B_Selisih_Penyebab!C7:C11)-B_Selisih_Penyebab!C12)',0.5,'Pembulatan SNDC'),
            ('Jumlah sektor SNDC dikurangi neto, selisih 2060 (MtCO2e)','ABS(SUM(B_Selisih_Penyebab!E7:E11)-B_Selisih_Penyebab!E12)',0.5,'Pembulatan SNDC'),
            ('Persen kumulatif energi sampai pihak ketiga tidak melebihi 100 persen',f'MAX(0,P_Portofolio!R{pos["erows"]["B6"]}-1)',0,'B7 menutup sisa sehingga tidak dihitung'),
            ('Galat rumus pada kolom utama P_Portofolio',f'SUMPRODUCT(--ISERROR(P_Portofolio!G6:R{lf+1}))',0,'Tidak boleh ada galat')]
    for i,(a,f_,tol,ex) in enumerate(checks):
        r=6+i; sh.t(f'B{r}',a); sh.f(f'C{r}',f_,'n2'); sh.n(f'D{r}',tol,'n2i'); sh.f(f'E{r}',f'IF(C{r}<=D{r},"OK","Periksa")','tl'); sh.t(f'F{r}',ex)
    n=len(checks)
    sh.t(f'B{7+n}','Jumlah pemeriksaan yang perlu diperiksa'); sh.f(f'C{7+n}',f'COUNTIF(E6:E{5+n},"Periksa")','n0'); 
    sh.f('A3',f'"Temuan utama: "&COUNTIF(E6:E{5+n},"OK")&" dari {n} pemeriksaan lulus; "&C{7+n}&" perlu diperiksa."','title')
    sh.width('A','A',3); sh.width('B','B',70); sh.width('C','D',14); sh.width('E','E',12); sh.width('F','F',60)
    return sh
