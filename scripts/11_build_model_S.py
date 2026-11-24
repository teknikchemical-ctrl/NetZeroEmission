"""Lembar solusi S_: terbarukan dari RUPTL (7 teknologi + rekap) dan FOLU (10 aksi)."""
import sys; sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from modelkit import *; import chartkit as ck; import src
YR=list(range(2025,2035)); YC={y:CL(6+i) for i,y in enumerate(YR)}   # F..O
RU=src.year_cols('D_RUPTL_Tambahan',4)
def _ruptl_rows():
    w=src.ws('D_RUPTL_Tambahan'); d={}
    for r in range(5,70):
        j,s=w.cell(r,1).value,w.cell(r,2).value
        if j and s in('RE Base','ARED'): d[(j,s)]=r
    return d
RR=_ruptl_rows()
def _teknis_rows():
    d=src.ws('D_Teknis_Opsi'); opt={}
    for r in range(6,320):
        if d.cell(r,3).value: opt.setdefault(d.cell(r,3).value,[]).append(r)
    return opt
TR=_teknis_rows()
def cfrow(option):
    d=src.ws('D_Teknis_Opsi')
    for r in TR[option]:
        if d.cell(r,5).value=='Faktor kapasitas': return r
RE_CFG=[
 dict(name='S_Surya',nomor=104,label='Surya PV skala utilitas',types=['PLTS','PLTS+BESS'],opt=['Surya skala utilitas'],cap=('E',13),capnote='Biaya modal LEAP 2020 (C_Biaya_Teknologi)',eda='Surya'),
 dict(name='S_Angin',nomor=105,label='Angin darat dan laut (PLTB)',types=['PLTB'],opt=['Angin darat','Angin laut'],cap=('E',12),capnote='Biaya modal LEAP 2020',eda='Angin',cfopt='Angin darat'),
 dict(name='S_PLTA',nomor=106,label='PLTA besar',types=['PLTA'],opt=['PLTA besar'],cap=('E',7),capnote='Biaya modal LEAP 2020',eda='PLTA'),
 dict(name='S_Mini_Hidro',nomor=107,label='Mini hidro (PLTM)',types=['PLTM'],opt=['Mini hidro'],cap=('R',33),capnote='EPC PLN 2.000 sampai 5.000 USD per kW (rentang)',eda='Mini hidro'),
 dict(name='S_Panas_Bumi',nomor=108,label='Panas bumi (PLTP)',types=['PLTP'],opt=['Panas bumi'],cap=('E',11),capnote='Biaya modal LEAP 2020',eda='Panas bumi'),
 dict(name='S_Bioenergi',nomor=109,label='Bioenergi dan sampah (PLTBM, PLTBg, PLTSa)',types=['PLTBM','PLTBg','PLTSa'],opt=['Biomassa'],cap=('E',14),capnote='Biaya modal LEAP 2020 (biomassa)',eda='Bioenergi',cfopt='Biomassa'),
 dict(name='S_Nuklir',nomor=110,label='Nuklir (PLTN)',types=['PLTN'],opt=['Nuklir'],cap=('E',16),capnote='Biaya modal LEAP 2020; PLN EPC 6.000 sampai 7.000',eda='Nuklir'),
]
PARAM='S_EBT_Rekap'
def re_sheet(cfg):
    n=cfg['name']; sh=Sheet(n,'FF1BAF7A'); lab=cfg['label']
    sh.t('A1',f'Lembar {cfg["nomor"]}. Solusi {lab}: tabel teknis, pengurangan emisi, biaya, dan investasi dari tambahan kapasitas RUPTL','title')
    sh.t('A2','Pengurangan emisi = kapasitas kumulatif RUPTL x faktor kapasitas x 8.760 jam x faktor emisi PLTU batubara yang digantikan (rentang resmi 0,79 sampai 1,22; tengah 0,96). RE Base adalah rencana dasar; ARED adalah skenario percepatan; selisihnya adalah peningkatan di atas rencana dasar. Hanya angka bersumber dan hitungan sederhana. Biru: ketikan bersumber; hijau: tautan; hitam: hitungan.','title')
    cf_opt=cfg.get('cfopt',cfg['opt'][0]); cfr=cfrow(cf_opt)
    # ---- parameters (rows 16-24)
    sh.t('B15',f'Tabel {cfg["nomor"]}.B. Parameter dan faktor (bersumber)','tbl')
    for c,t in zip('BCDEF',['Parameter','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}16',t,'hdr')
    cap_col,cap_row=cfg['cap']
    P=[('Faktor kapasitas',f'D_Teknis_Opsi!F{cfr}','fraksi','R',f'D_Teknis_Opsi baris {cfr}','n2l'),
       ('Faktor emisi batubara digantikan, rendah',f'{PARAM}!C7','tCO2 per MWh','R','Fadiilah dan Dye 2026; Zahari dan McLellan 2024','n2l'),
       ('Faktor emisi batubara digantikan, tengah',f'{PARAM}!C8','tCO2 per MWh','R','idem (rata-rata 0,96)','n2l'),
       ('Faktor emisi batubara digantikan, tinggi',f'{PARAM}!C9','tCO2 per MWh','R','idem','n2l'),
       ('Jam per tahun',f'{PARAM}!C10','jam','D','Definisi','n0l')]
    if cap_col=='E':
        P+=[('Biaya modal 2020',f'C_Biaya_Teknologi!E{cap_row}','USD per kW','E',cfg['capnote'],'n0l'),('Biaya modal, batas tinggi',f'C_Biaya_Teknologi!E{cap_row}','USD per kW','E','sama (satu nilai)','n0l'),
            ('Biaya modal dan BTT tetap tahunan',f'C_Biaya_Teknologi!H{cap_row}+C_Biaya_Teknologi!G{cap_row}','USD per kW per tahun','AC','C_Biaya_Teknologi (anuitas 9 persen ditambah BTT tetap)','n1l')]
    else:
        P+=[('Biaya modal, batas rendah',f'C_Biaya_Teknologi!C{cap_row}','USD per kW','E',cfg['capnote'],'n0l'),('Biaya modal, batas tinggi',f'C_Biaya_Teknologi!D{cap_row}','USD per kW','E',cfg['capnote'],'n0l'),
            ('Biaya modal dan BTT tetap tahunan',None,'USD per kW per tahun','A','tidak ada BTT tetap bersumber (WP-J)','n1l')]
    for i,(a,f_,u,st,so,sty) in enumerate(P):
        r=17+i; sh.t(f'B{r}',a)
        if f_: sh.f(f'C{r}',f_,sty)
        else: sh.f(f'C{r}','NA()','n1')
        sh.t(f'D{r}',u); sh.t(f'E{r}',st); sh.t(f'F{r}',so)
    # rows: CF 17, EFlow 18, EFmid 19, EFhigh 20, hours 21, capLow 22, capHigh 23, annual 24
    # ---- technical parameters from D_Teknis_Opsi
    sh.t('B27',f'Tabel {cfg["nomor"]}.C. Parameter teknis bersumber (tautan ke D_Teknis_Opsi)','tbl')
    for c,t in zip('BCDEFGH',['Opsi','Kelas parameter','Parameter','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}28',t,'hdr')
    rows=[r for o in cfg['opt'] for r in TR[o]]
    for i,r in enumerate(rows):
        rr=29+i
        sh.f(f'B{rr}',f'D_Teknis_Opsi!C{r}','tl'); sh.f(f'C{rr}',f'D_Teknis_Opsi!D{r}','tl'); sh.f(f'D{rr}',f'D_Teknis_Opsi!E{r}','tl'); sh.f(f'E{rr}',f'D_Teknis_Opsi!F{r}','tl'); sh.f(f'F{rr}',f'D_Teknis_Opsi!G{r}','tl'); sh.f(f'G{rr}',f'D_Teknis_Opsi!I{r}','tl'); sh.f(f'H{rr}',f'D_Teknis_Opsi!J{r}','tl')
    r0=29+len(rows)+2
    # ---- D capacity
    sh.t(f'B{r0}',f'Tabel {cfg["nomor"]}.D. Tambahan kapasitas RUPTL 2025 sampai 2034 (MW)','tbl')
    for c,t in zip('BCDE',['ID','Butir','Satuan','Status']): sh.t(f'{c}{r0+1}',t,'hdr')
    for y in YR: sh.n(f'{YC[y]}{r0+1}',y,'hdr')
    sh.t(f'P{r0+1}','Sumber','hdr')
    rY=r0+1
    def ruptl_sum(scen,y): return '+'.join(f'D_RUPTL_Tambahan!{RU[y]}{RR[(t,scen)]}' for t in cfg['types'])
    D=[('D1','Tambahan per tahun, RE Base'),('D2','Tambahan per tahun, ARED'),('D3','Kumulatif RE Base'),('D4','Kumulatif ARED'),('D5','Peningkatan ARED di atas RE Base (kumulatif)')]
    rd={}
    for i,(id_,nm) in enumerate(D):
        r=r0+2+i; rd[id_]=r; sh.t(f'B{r}',id_); sh.t(f'C{r}',nm); sh.t(f'D{r}','MW'); sh.t(f'E{r}','P' if i<2 else 'AC'); sh.t(f'P{r}','D_RUPTL_Tambahan (Tabel 5.80 dan 5.81)' if i<2 else 'Jumlah dan selisih sederhana')
        for y in YR:
            c=YC[y]
            if i==0: sh.f(f'{c}{r}',ruptl_sum('RE Base',y),'n0l')
            elif i==1: sh.f(f'{c}{r}',ruptl_sum('ARED',y),'n0l')
            elif i==2: sh.f(f'{c}{r}',f'SUM($F${rd["D1"]}:{c}{rd["D1"]})','n0')
            elif i==3: sh.f(f'{c}{r}',f'SUM($F${rd["D2"]}:{c}{rd["D2"]})','n0')
            else: sh.f(f'{c}{r}',f'{c}{rd["D4"]}-{c}{rd["D3"]}','n0')
    # ---- E reduction
    r1=r0+9
    sh.t(f'B{r1}',f'Tabel {cfg["nomor"]}.E. Energi dan emisi batubara yang digantikan (kumulatif, MtCO2 per tahun)','tbl')
    for c,t in zip('BCDE',['ID','Butir','Satuan','Status']): sh.t(f'{c}{r1+1}',t,'hdr')
    for y in YR: sh.n(f'{YC[y]}{r1+1}',y,'hdr')
    sh.t(f'P{r1+1}','Rumus','hdr')
    E=[('E1','Energi dibangkitkan, RE Base','TWh','D3','n1',None),('E2','Energi dibangkitkan, ARED','TWh','D4','n1',None),
       ('E3','Emisi digantikan, RE Base, rendah','MtCO2','E1','n2',18),('E4','Emisi digantikan, RE Base, tengah','MtCO2','E1','n2',19),('E5','Emisi digantikan, RE Base, tinggi','MtCO2','E1','n2',20),
       ('E6','Emisi digantikan, ARED, rendah','MtCO2','E2','n2',18),('E7','Emisi digantikan, ARED, tengah','MtCO2','E2','n2',19),('E8','Emisi digantikan, ARED, tinggi','MtCO2','E2','n2',20),
       ('E9','Peningkatan ARED di atas RE Base (tengah)','MtCO2','E7-E4','n2',None),('E10','Rentang faktor emisi, ARED (tinggi dikurangi rendah)','MtCO2','E8-E6','n2',None)]
    re_={}
    for i,(id_,nm,u,src_,sty,efr) in enumerate(E):
        r=r1+2+i; re_[id_]=r; sh.t(f'B{r}',id_); sh.t(f'C{r}',nm); sh.t(f'D{r}',u); sh.t(f'E{r}','AC')
        for y in YR:
            c=YC[y]
            if id_ in('E1','E2'): sh.f(f'{c}{r}',f'{c}{rd[src_]}*$C$17*$C$21/1000000','n1')
            elif id_=='E9': sh.f(f'{c}{r}',f'{c}{re_["E7"]}-{c}{re_["E4"]}','n2')
            elif id_=='E10': sh.f(f'{c}{r}',f'{c}{re_["E8"]}-{c}{re_["E6"]}','n2')
            else: sh.f(f'{c}{r}',f'{c}{re_[src_]}*$C${efr}','n2')
        sh.t(f'P{r}','kapasitas kumulatif x faktor kapasitas x jam dibagi 1.000.000' if id_ in('E1','E2') else ('energi x faktor emisi' if efr else 'selisih sederhana'))
    # ---- F cost
    r2=r1+2+len(E)+1
    sh.t(f'B{r2}',f'Tabel {cfg["nomor"]}.F. Investasi dan biaya tahunan (kumulatif)','tbl')
    for c,t in zip('BCDE',['ID','Butir','Satuan','Status']): sh.t(f'{c}{r2+1}',t,'hdr')
    for y in YR: sh.n(f'{YC[y]}{r2+1}',y,'hdr')
    sh.t(f'P{r2+1}','Rumus','hdr')
    F=[('F1','Investasi modal, RE Base, rendah','USD miliar','D3',22,'inv'),('F2','Investasi modal, RE Base, tinggi','USD miliar','D3',23,'inv'),('F3','Investasi modal, ARED, rendah','USD miliar','D4',22,'inv'),('F4','Investasi modal, ARED, tinggi','USD miliar','D4',23,'inv'),
       ('F5','Biaya modal dan BTT tetap tahunan, RE Base','USD juta per tahun','D3',24,'ann'),('F6','Biaya modal dan BTT tetap tahunan, ARED','USD juta per tahun','D4',24,'ann')]
    rf={}
    for i,(id_,nm,u,srcr,prow,kind) in enumerate(F):
        r=r2+2+i; rf[id_]=r; sh.t(f'B{r}',id_); sh.t(f'C{r}',nm); sh.t(f'D{r}',u); sh.t(f'E{r}','AC')
        for y in YR:
            c=YC[y]
            if kind=='inv': sh.f(f'{c}{r}',f'{c}{rd[srcr]}*$C${prow}/1000000','n2')
            else: sh.f(f'{c}{r}',f'IFERROR({c}{rd[srcr]}*$C${prow}/1000,NA())','n1')
        sh.t(f'P{r}','kapasitas kumulatif (MW) x biaya modal (USD per kW) dibagi 1.000.000' if kind=='inv' else 'kapasitas (MW) x biaya tahunan (USD per kW per tahun) dibagi 1.000')
    # ---- G implementation
    r3=r2+2+len(F)+1
    sh.t(f'B{r3}',f'Tabel {cfg["nomor"]}.G. Pelaksanaan saat ini (diisi tim; kosong sampai ada data bersumber)','tbl')
    for c,t in zip('BCDE',['Butir','Nilai','Satuan','Kode WP']): sh.t(f'{c}{r3+1}',t,'hdr')
    G=[('Terpasang akhir 2025','MW','WP-D'),('Tambahan terealisasi 2020 sampai 2025','MW','WP-D'),('Tambahan direncanakan 2020 sampai 2025 (RUPTL lama)','MW','WP-D'),('Proyek dalam konstruksi atau PPA ditandatangani','MW','WP-D')]
    for i,(a,u,wp) in enumerate(G):
        r=r3+2+i; sh.t(f'B{r}',a)
        if i==0 and cfg['eda']=='Surya':
            sh.f(f'C{r}',f'D_Energi_Potensi!E{src.find_row("D_Energi_Potensi","Surya terpasang",col=3,start=6,end=70)}*1000','n0l'); sh.t(f'D{r}',u); sh.t(f'E{r}','E: kuartal 1 2026, IESR via pv magazine (D_Energi_Potensi)')
        else: sh.blank(f'C{r}','n0i'); sh.t(f'D{r}',u); sh.t(f'E{r}',wp)
    rg=r3+2+len(G)
    sh.t(f'B{rg}','Pelaksanaan (terealisasi dibagi direncanakan)'); sh.f(f'C{rg}',f'IF(AND(ISNUMBER(C{r3+3}),ISNUMBER(C{r3+4}),C{r3+4}>0),C{r3+3}/C{r3+4},"belum ada data")','pc'); sh.t(f'D{rg}','fraksi'); sh.t(f'E{rg}','AC')
    # ---- A summary (rows 6-13)
    sh.t('B5',f'Tabel {cfg["nomor"]}.A. Ringkasan','tbl')
    for c,t in zip('BCDEFG',['Butir','2030','2034','Satuan','Status','Catatan']): sh.t(f'{c}6',t,'hdr')
    K,O=YC[2030],YC[2034]
    S_=[('Tambahan kapasitas kumulatif, RE Base',f'{K}{rd["D3"]}',f'{O}{rd["D3"]}','MW','n0','P'),
        ('Tambahan kapasitas kumulatif, ARED',f'{K}{rd["D4"]}',f'{O}{rd["D4"]}','MW','n0','P'),
        ('Emisi batubara digantikan, RE Base (tengah)',f'{K}{re_["E4"]}',f'{O}{re_["E4"]}','MtCO2 per tahun','n2','AC'),
        ('Emisi batubara digantikan, ARED (tengah)',f'{K}{re_["E7"]}',f'{O}{re_["E7"]}','MtCO2 per tahun','n2','AC'),
        ('Peningkatan ARED di atas RE Base (tengah)',f'{K}{re_["E9"]}',f'{O}{re_["E9"]}','MtCO2 per tahun','n2','AC'),
        ('Peningkatan ARED, persen selisih energi 2030 (CPOS dikurangi LCCP_L)',f'{K}{re_["E9"]}/B_Selisih_Penyebab!C7',None,'fraksi','pc','AC'),
        ('Investasi modal kumulatif ARED (rendah)',f'{K}{rf["F3"]}',f'{O}{rf["F3"]}','USD miliar','n2','AC'),
        ('Investasi modal kumulatif ARED (tinggi)',f'{K}{rf["F4"]}',f'{O}{rf["F4"]}','USD miliar','n2','AC')]
    for i,(a,f30,f34,u,sty,st) in enumerate(S_):
        r=7+i; sh.t(f'B{r}',a); sh.f(f'C{r}',f30,sty)
        if f34: sh.f(f'D{r}',f34,sty)
        sh.t(f'E{r}',u); sh.t(f'F{r}',st)
    sh.t('G7','RUPTL 2025 sampai 2034 (D_RUPTL_Tambahan)'); sh.t('G9','Tengah memakai faktor emisi 0,96 tCO2 per MWh'); sh.t('G11','Di atas rencana dasar; RE Base sudah termuat dalam garis dasar CPOS dan RUPTL'); sh.t('G13','Bukan biaya per tCO2; bahan bakar yang dihindari tidak dikurangkan')
    sh.f('A3',f'"Temuan utama: tambahan {lab} RE Base menggantikan sekitar "&ROUND({K}{re_["E4"]},1)&" MtCO2 per tahun pada 2030 dan "&ROUND({O}{re_["E4"]},1)&" pada 2034 (faktor emisi tengah); ARED menggantikan "&ROUND({K}{re_["E7"]},1)&" pada 2030 dan "&ROUND({O}{re_["E7"]},1)&" pada 2034, rentang faktor emisi "&ROUND({O}{re_["E6"]},1)&" sampai "&ROUND({O}{re_["E8"]},1)&"; peningkatan ARED di atas RE Base pada 2030 sebesar "&ROUND({K}{re_["E9"]},2)&" MtCO2 ("&ROUND({K}{re_["E9"]}/B_Selisih_Penyebab!C7*100,1)&" persen selisih energi)."','title')
    # ---- charts
    cat=f'{n}!${YC[2025]}${rY}:${YC[2034]}${rY}'
    def rng(r): return f'{n}!${YC[2025]}${r}:${YC[2034]}${r}'
    c1=ck.chart_xml(f'Gambar {cfg["nomor"]}.1. {lab}: emisi batubara yang digantikan (MtCO2 per tahun), rentang faktor emisi berarsir',
        [dict(base_ref=rng(re_['E6']),band_ref=rng(re_['E10']),name_ref=f'{n}!$C${re_["E10"]}',name='Rentang faktor emisi 0,79 sampai 1,22 (ARED)',fill='F4B183')],
        [dict(val_ref=rng(re_['E4']),name_ref=f'{n}!$C${re_["E4"]}',name='RE Base (tengah)',color='1F4E79',pos='b'),
         dict(val_ref=rng(re_['E7']),name_ref=f'{n}!$C${re_["E7"]}',name='ARED (tengah)',color='C00000',pos='t')],
        'MtCO2 per tahun','Tahun',cat,yfmt='#,##0.0')
    c2=ck.chart_xml(f'Gambar {cfg["nomor"]}.2. {lab}: pengurangan emisi (kiri) dan investasi modal kumulatif ARED (kanan)',[],
        [dict(val_ref=rng(re_['E7']),name_ref=f'{n}!$C${re_["E7"]}',name='ARED (tengah)',color='C00000',pos='t'),
         dict(val_ref=rng(re_['E4']),name_ref=f'{n}!$C${re_["E4"]}',name='RE Base (tengah)',color='1F4E79',pos='b'),
         dict(val_ref=rng(rf['F3']),name_ref=f'{n}!$C${rf["F3"]}',name='Investasi ARED rendah',color='2E7D32',pos='t',sec=True,fmt='#,##0.0',dash='sysDash',labels=False),
         dict(val_ref=rng(rf['F4']),name_ref=f'{n}!$C${rf["F4"]}',name='Investasi ARED tinggi',color='BF8F00',pos='b',sec=True,fmt='#,##0.0',dash='sysDash')],
        'MtCO2 per tahun','Tahun',cat,yfmt='#,##0.0',ytitle2='USD miliar (kumulatif)',yfmt2='#,##0')
    c3=ck.chart_xml(f'Gambar {cfg["nomor"]}.3. {lab}: pengurangan emisi ARED (kiri) dan kapasitas kumulatif (kanan)',[],
        [dict(val_ref=rng(re_['E7']),name_ref=f'{n}!$C${re_["E7"]}',name='ARED (tengah)',color='C00000',pos='t',fmt='#,##0.0'),
         dict(val_ref=rng(rd['D4']),name_ref=f'{n}!$C${rd["D4"]}',name='Kapasitas kumulatif ARED (MW)',color='1F4E79',pos='b',sec=True,fmt='#,##0',dash='sysDash'),
         dict(val_ref=rng(rd['D3']),name_ref=f'{n}!$C${rd["D3"]}',name='Kapasitas kumulatif RE Base (MW)',color='7F7F7F',pos='b',sec=True,fmt='#,##0',labels=False,dash='sysDash')],
        'MtCO2 per tahun','Tahun',cat,yfmt='#,##0.0',ytitle2='MW (kumulatif)',yfmt2='#,##0')
    for rr in range(6,15): sh.merges.append(f'G{rr}:O{rr}')
    for rr in range(16,25): sh.merges.append(f'F{rr}:O{rr}')
    for rr in range(28,29+len(rows)): sh.merges.append(f'H{rr}:O{rr}')
    top=rg+4
    W,H=7400000,3800000
    sh.charts=[(c1,(1,top,W,H)),(c2,(8,top,W,H)),(c3,(1,top+21,W,H))]
    sh.width('A','A',3); sh.width('B','B',46); sh.width('C','C',22); sh.width('D','E',24); sh.width('F','O',12); sh.width('P','P',55)
    sh.rows=dict(rd=rd,re=re_,rf=rf,rY=rY)
    return sh
def EBT_Rekap(res):
    sh=Sheet(PARAM,'FF1BAF7A')
    sh.t('A1','Lembar 111. Rekap terbarukan terukur dari RUPTL: seluruh teknologi, RE Base dan ARED, dan uji silang terhadap emisi batubara yang dilaporkan RUPTL','title')
    sh.t('A2','Menjumlahkan lembar teknologi (S_Surya, S_Angin, S_PLTA, S_Mini_Hidro, S_Panas_Bumi, S_Bioenergi, S_Nuklir). Pengurangan emisi = kapasitas x faktor kapasitas x jam x faktor emisi batubara; uji silang dengan selisih emisi batubara RE Base dan ARED yang dilaporkan RUPTL. Penyimpanan (BESS, PLTA PS) tidak mengurangi emisi sendiri. Pelaksanaan riil (terpasang, pipeline) belum terukur (WP-D).','title')
    sh.t('B5','Tabel 111.A. Parameter global bersumber','tbl')
    for c,t in zip('BCDEF',['Parameter','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}6',t,'hdr')
    P=[('Faktor emisi PLTU batubara, rendah',0.79,'tCO2 per MWh','R','Fadiilah dan Dye 2026; Zahari dan McLellan 2024 (D_Teknis_Opsi baris 54)'),
       ('Faktor emisi PLTU batubara, tengah (rata-rata)',0.96,'tCO2 per MWh','R','idem; di dalam batas PTBAE 0,911 sampai 1,297 (Sunanda dkk. 2026 Tabel 1)'),
       ('Faktor emisi PLTU batubara, tinggi',1.22,'tCO2 per MWh','R','idem'),('Jam per tahun',8760,'jam','D','Definisi')]
    for i,(a,v,u,st,so) in enumerate(P):
        r=7+i; sh.t(f'B{r}',a); sh.n(f'C{r}',v,'n2i' if i<3 else 'n0i'); sh.t(f'D{r}',u); sh.t(f'E{r}',st); sh.t(f'F{r}',so)
    sh.t('B13','Tabel 111.B. Emisi batubara yang digantikan menurut teknologi (tengah, MtCO2 per tahun)','tbl')
    for c,t in zip('BCDE',['ID','Teknologi','Skenario','Status']): sh.t(f'{c}14',t,'hdr')
    for y in YR: sh.n(f'{YC[y]}14',y,'hdr')
    sh.t('P14','Sumber','hdr')
    rows_base=[];rows_ared=[]
    r=15
    for scen,key in (('RE Base','E4'),('ARED','E7')):
        first=r
        for cfg,s in res:
            sh.t(f'B{r}',f'{cfg["eda"]}'); sh.t(f'C{r}',cfg['label']); sh.t(f'D{r}',scen); sh.t(f'E{r}','AC'); sh.t(f'P{r}',f'{cfg["name"]} (baris {s.rows["re"][key]})')
            for y in YR: sh.f(f'{YC[y]}{r}',f'{cfg["name"]}!{YC[y]}{s.rows["re"][key]}','n2l')
            r+=1
        sh.t(f'C{r}',f'Jumlah {scen}'); sh.t(f'D{r}',scen); sh.t(f'E{r}','AC')
        for y in YR: sh.f(f'{YC[y]}{r}',f'SUM({YC[y]}{first}:{YC[y]}{r-1})','n2')
        (rows_base if scen=='RE Base' else rows_ared).append(r); r+=2
    rtot_b,rtot_a=rows_base[0],rows_ared[0]
    # low/high totals for ARED
    sh.t(f'C{r}','Jumlah ARED, faktor emisi rendah'); sh.t(f'D{r}','ARED'); sh.t(f'E{r}','AC')
    for y in YR: sh.f(f'{YC[y]}{r}','+'.join(f'{c["name"]}!{YC[y]}{s.rows["re"]["E6"]}' for c,s in res),'n2')
    rlow=r; r+=1
    sh.t(f'C{r}','Jumlah ARED, faktor emisi tinggi'); sh.t(f'D{r}','ARED'); sh.t(f'E{r}','AC')
    for y in YR: sh.f(f'{YC[y]}{r}','+'.join(f'{c["name"]}!{YC[y]}{s.rows["re"]["E8"]}' for c,s in res),'n2')
    rhigh=r; r+=1
    sh.t(f'C{r}','Rentang faktor emisi ARED'); sh.t(f'D{r}','ARED'); sh.t(f'E{r}','AC')
    for y in YR: sh.f(f'{YC[y]}{r}',f'{YC[y]}{rhigh}-{YC[y]}{rlow}','n2')
    rband=r; r+=2
    sh.t(f'B{r}','Tabel 111.C. Uji silang: peningkatan ARED di atas RE Base, hitung sederhana dibanding selisih emisi batubara yang dilaporkan RUPTL','tbl'); r+=1
    for c,t in zip('BCDE',['ID','Butir','Satuan','Status']): sh.t(f'{c}{r}',t,'hdr')
    for y in YR: sh.n(f'{YC[y]}{r}',y,'hdr')
    rhdr=r; r+=1
    sh.t(f'C{r}','Peningkatan ARED di atas RE Base (hitung: kapasitas x faktor, tengah)'); sh.t(f'D{r}','MtCO2'); sh.t(f'E{r}','AC')
    for y in YR: sh.f(f'{YC[y]}{r}',f'{YC[y]}{rtot_a}-{YC[y]}{rtot_b}','n2')
    rcalc=r; r+=1
    sh.t(f'C{r}','Selisih emisi batubara RUPTL: RE Base dikurangi ARED (dilaporkan RUPTL)'); sh.t(f'D{r}','MtCO2'); sh.t(f'E{r}','P')
    for y in YR: sh.f(f'{YC[y]}{r}',f'B_Pendorong!{YC[y]}17-B_Pendorong!{YC[y]}18','n2l')
    rrep=r; r+=1
    sh.t(f'C{r}','Selisih hitung dikurangi dilaporkan'); sh.t(f'D{r}','MtCO2'); sh.t(f'E{r}','AC')
    for y in YR: sh.f(f'{YC[y]}{r}',f'{YC[y]}{rcalc}-{YC[y]}{rrep}','n2')
    r+=1
    sh.t(f'B{r}','Catatan 111. Selisih besar antara hitungan sederhana dan angka yang dilaporkan RUPTL menunjukkan bahwa tambahan EBT ARED tidak otomatis menurunkan emisi batubara satu banding satu (permintaan, pengaturan dispatch, dan jadwal pensiun ikut berperan). Keduanya ditampilkan tanpa memilih; pembahasan menjadi tugas WP-D dan WP-A.','note'); sh.merges.append(f'B{r}:P{r}')
    sh.f('A3',f'"Temuan utama: tambahan EBT RUPTL ARED menggantikan sekitar "&ROUND({YC[2030]}{rtot_a},1)&" MtCO2 per tahun pada 2030 (RE Base "&ROUND({YC[2030]}{rtot_b},1)&") dan "&ROUND({YC[2034]}{rtot_a},1)&" pada 2034, sedangkan RUPTL sendiri melaporkan emisi batubara ARED hanya "&ROUND({YC[2030]}{rrep},1)&" MtCO2 lebih rendah pada 2030 dan "&ROUND({YC[2034]}{rrep},1)&" pada 2034."','title')
    cat=f'{PARAM}!${YC[2025]}$14:${YC[2034]}$14'
    def rg(rr): return f'{PARAM}!${YC[2025]}${rr}:${YC[2034]}${rr}'
    c1=ck.chart_xml('Gambar 111.1. Seluruh terbarukan RUPTL: emisi batubara yang digantikan, RE Base dan ARED (rentang faktor emisi berarsir)',
        [dict(base_ref=rg(rlow),band_ref=rg(rband),name='Rentang faktor emisi 0,79 sampai 1,22 (ARED)',fill='F4B183')],
        [dict(val_ref=rg(rtot_b),name='RE Base (tengah)',color='1F4E79',pos='b'),dict(val_ref=rg(rtot_a),name='ARED (tengah)',color='C00000',pos='t')],
        'MtCO2 per tahun','Tahun',cat,yfmt='#,##0')
    c2=ck.chart_xml('Gambar 111.2. Uji silang: peningkatan ARED di atas RE Base, hitung sederhana dan dilaporkan RUPTL (MtCO2)',[],
        [dict(val_ref=rg(rcalc),name='Hitung: kapasitas x faktor (tengah)',color='C00000',pos='t'),dict(val_ref=rg(rrep),name='Dilaporkan RUPTL: selisih emisi batubara',color='1F4E79',pos='b')],
        'MtCO2 per tahun','Tahun',cat,yfmt='#,##0')
    sh.charts=[(c1,(1,r+3,7400000,3800000)),(c2,(8,r+3,7400000,3800000))]
    sh.width('A','A',3); sh.width('B','B',44); sh.width('C','C',44); sh.width('D','E',14); sh.width('F','O',11); sh.width('P','P',55)
    sh.rows=dict(tot_b=rtot_b,tot_a=rtot_a)
    return sh
def _main():
    import importlib.util
    spec=importlib.util.spec_from_file_location('bmod','/home/user/NetZeroEmission/scripts/09_build_model_B.py'); bm=importlib.util.module_from_spec(spec); sys.argv=['x']; spec.loader.exec_module(bm)
    gp=bm.B_Garis_Pembangunan(); pend=bm.B_Pendorong(); sel=bm.B_Selisih(gp)
    res=[(c,re_sheet(c)) for c in RE_CFG]
    rek=EBT_Rekap(res)
    sheets=[pend,gp,sel,rek]+[s for _,s in res]
    cache,errs=build('/tmp/claude-0/base_model.xlsx','/tmp/claude-0/stageS.xlsx',sheets,[])
    print([e for e in errs if 'NA()' not in e[3] and 'IFERROR' not in e[3]][:8])
    for s in sheets[3:]: print(s.name,cache.get((s.name,'A3'),'')[:230])
if __name__=='__main__' and 'FOLU' not in sys.argv: _main()

# ============================ FOLU ============================
FOLU_CFG=[ # name, nomor, label, C_Portofolio_FOLU input row, result row, C_Solusi A row, B row, teknis option, D_Rencana row, D_Kenyataan row, practice?
 dict(name='S_Tata_Air_Gambut',nomor=112,label='Tata air gambut',pin=15,pres=29,ra=43,rb=55,opt='Tata air gambut',rpl=15,rkn=14),
 dict(name='S_Degradasi_Gambut',nomor=113,label='Penghindaran degradasi gambut',pin=16,pres=30,ra=44,rb=56,opt='Degradasi hutan',rpl=9,rkn=8),
 dict(name='S_PHL',nomor=114,label='Pengelolaan hutan lestari (RIL-C dan ENR)',pin=17,pres=31,ra=45,rb=57,opt='Pengelolaan hutan lestari (PHL)',rpl=11,rkn=10),
 dict(name='S_Deforestasi_Gambut',nomor=115,label='Penghindaran deforestasi gambut',pin=18,pres=32,ra=46,rb=58,opt='Deforestasi gambut',rpl=8,rkn=7),
 dict(name='S_Restorasi_Gambut',nomor=116,label='Restorasi gambut',pin=19,pres=33,ra=47,rb=59,opt='Restorasi gambut',rpl=14,rkn=13,capr=73),
 dict(name='S_Degradasi_Mineral',nomor=117,label='Penghindaran degradasi hutan mineral',pin=20,pres=34,ra=48,rb=60,opt='Degradasi hutan',rpl=9,rkn=8),
 dict(name='S_Deforestasi_Mineral',nomor=118,label='Penghindaran deforestasi hutan mineral',pin=21,pres=35,ra=49,rb=61,opt='Deforestasi mineral',rpl=7,rkn=6),
 dict(name='S_Rehab_Tanpa_Rotasi',nomor=119,label='Rehabilitasi lahan tanpa rotasi',pin=22,pres=36,ra=50,rb=62,opt='Rehabilitasi lahan',rpl=13,rkn=12),
 dict(name='S_Rehab_Rotasi',nomor=120,label='Rehabilitasi lahan dengan rotasi',pin=23,pres=37,ra=51,rb=63,opt='Rehabilitasi lahan',rpl=12,rkn=11),
 dict(name='S_Hutan_Tanaman',nomor=121,label='Hutan tanaman (PBPH-HT)',pin=24,pres=38,ra=52,rb=64,opt='Hutan tanaman (HTI)',rpl=10,rkn=9,capr=74),
]
def folu_sheet(cfg):
    n=cfg['name']; sh=Sheet(n,'FF1BAF7A'); lab=cfg['label']; num_=cfg['nomor']
    PIN,PRES='C_Portofolio_FOLU_2030!','C_Portofolio_FOLU_2030!'
    sh.t('A1',f'Lembar {num_}. Solusi FOLU: {lab}: tabel teknis, pengurangan emisi, biaya, dan pelaksanaan','title')
    sh.t('A2','Pengurangan emisi = selisih luas terhadap garis dasar BaU (ribu ha) x faktor (tCO2 per ha) dibagi 1.000; penghindaran: BaU dikurangi CM; praktik: CM dikurangi BaU; tambahan CM2 tidak boleh negatif. Luas dan target dari Renops (D_Rencana, D_Kenyataan), faktor dari BTR-1, FRL, dan Rossita dan Boer. Hanya angka bersumber dan hitungan sederhana. Biru: ketikan bersumber; hijau: tautan; hitam: hitungan.','title')
    # ---- B chain (rows 17..)
    sh.t('B16',f'Tabel {num_}.B. Rantai hitung pengurangan emisi 2030 (CM1 dan CM2)','tbl')
    items=[('Jenis aksi',f'{PIN}D{cfg["pin"]}','tl','teks'),('Luas BaU (ribu ha)',f'{PIN}E{cfg["pin"]}','n0l','ribu ha'),('Luas CM1 (ribu ha)',f'{PIN}F{cfg["pin"]}','n0l','ribu ha'),('Luas CM2 (ribu ha)',f'{PIN}G{cfg["pin"]}','n0l','ribu ha'),
           ('Faktor rendah (tCO2 per ha)',f'{PIN}H{cfg["pin"]}','n2l','tCO2 per ha'),('Faktor tinggi (tCO2 per ha)',f'{PIN}I{cfg["pin"]}','n2l','tCO2 per ha')]
    for c,t in zip('BCDEF',['Butir','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}17',t,'hdr')
    for i,(a,f_,sty,u) in enumerate(items):
        r=18+i; sh.t(f'B{r}',a); sh.f(f'C{r}',f_,sty); sh.t(f'D{r}',u); sh.t(f'E{r}','P' if 'Luas' in a else ('R' if 'Faktor' in a else '')); sh.t(f'F{r}','C_Portofolio_FOLU_2030 Tabel 30.B (Renops Tabel 2; faktor BTR-1, FRL, Rossita dan Boer)')
    # rows: jenis 18, bau 19, cm1 20, cm2 21, flo 22, fhi 23
    calc=[('Pengurangan CM1, rendah','IF($C$18="Penghindaran",($C$19-$C$20),($C$20-$C$19))*$C$22/1000'),
          ('Pengurangan CM1, tinggi','IF($C$18="Penghindaran",($C$19-$C$20),($C$20-$C$19))*$C$23/1000'),
          ('Tambahan CM2 di atas CM1, rendah','MAX(0,IF($C$18="Penghindaran",($C$20-$C$21),($C$21-$C$20))*$C$22/1000)'),
          ('Tambahan CM2 di atas CM1, tinggi','MAX(0,IF($C$18="Penghindaran",($C$20-$C$21),($C$21-$C$20))*$C$23/1000)'),
          ('Total CM2, rendah','C24+C26'),('Total CM2, tinggi','C25+C27')]
    for i,(a,f_) in enumerate(calc):
        r=24+i; sh.t(f'B{r}',a); sh.f(f'C{r}',f_,'n2'); sh.t(f'D{r}','MtCO2e per tahun'); sh.t(f'E{r}','AC'); sh.t(f'F{r}','luas x faktor dibagi 1.000')
    sh.t('B30','Uji terhadap C_Portofolio_FOLU_2030 (selisih; nol berarti sama)')
    sh.f('C30',f'ABS(C24-{PRES}E{cfg["pres"]})+ABS(C25-{PRES}F{cfg["pres"]})+ABS(C26-{PRES}G{cfg["pres"]})+ABS(C27-{PRES}H{cfg["pres"]})','n2'); sh.t('D30','MtCO2e'); sh.t('E30','AC')
    # ---- C technical params
    sh.t('B33',f'Tabel {num_}.C. Parameter teknis bersumber (tautan ke D_Teknis_Opsi)','tbl')
    for c,t in zip('BCDEFGH',['Opsi','Kelas parameter','Parameter','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}34',t,'hdr')
    rows=TR[cfg['opt']]
    for i,r in enumerate(rows):
        rr=35+i
        sh.f(f'B{rr}',f'D_Teknis_Opsi!C{r}','tl'); sh.f(f'C{rr}',f'D_Teknis_Opsi!D{r}','tl'); sh.f(f'D{rr}',f'D_Teknis_Opsi!E{r}','tl'); sh.f(f'E{rr}',f'D_Teknis_Opsi!F{r}','tl'); sh.f(f'F{rr}',f'D_Teknis_Opsi!G{r}','tl'); sh.f(f'G{rr}',f'D_Teknis_Opsi!I{r}','tl'); sh.f(f'H{rr}',f'D_Teknis_Opsi!J{r}','tl')
    r0=35+len(rows)+2
    # ---- D target & capaian
    sh.t(f'B{r0}',f'Tabel {num_}.D. Target dan capaian bersumber (ha) dan setara pengurangan emisi (hanya aksi praktik)','tbl')
    for c,t in zip('BCDEF',['Butir','Luas (ha)','Tahun','Status','Setara pengurangan rendah (MtCO2e)']): sh.t(f'{c}{r0+1}',t,'hdr'); 
    sh.t(f'G{r0+1}','Setara pengurangan tinggi (MtCO2e)','hdr'); sh.t(f'H{r0+1}','Sumber','hdr')
    rp,rk=cfg['rpl'],cfg['rkn']
    D=[('Capaian kumulatif',f'D_Kenyataan!D{rk}',f'D_Kenyataan!C{rk}','R','D_Kenyataan Tabel 78.A'),
       ('Target Net Sink 2024',f'D_Rencana!F{rp}','2024','P','D_Rencana'),
       ('Target Net Sink 2030',f'D_Rencana!G{rp}','2030','P','D_Rencana'),
       ('Target NDC 2030',f'D_Rencana!E{rp}','2030','P','D_Rencana (kosong bila NDC tidak mencatat)')]
    rd={}
    for i,(a,fa,fy,st,so) in enumerate(D):
        r=r0+2+i; rd[a]=r; sh.t(f'B{r}',a); sh.f(f'C{r}',f'IFERROR(IF(ISNUMBER({fa}),{fa},NA()),NA())','n0l')
        if fy.startswith('D_'): sh.f(f'D{r}',f'IF(ISNUMBER({fy}),{fy},"")','tl')
        else: sh.n(f'D{r}',int(fy),'n0i')
        sh.t(f'E{r}',st)
        sh.f(f'F{r}',f'IF($C$18="Praktik",MAX(0,(C{r}/1000-$C$19)*$C$22/1000),NA())','n2'); sh.f(f'G{r}',f'IF($C$18="Praktik",MAX(0,(C{r}/1000-$C$19)*$C$23/1000),NA())','n2'); sh.t(f'H{r}',so)
    sh.t(f'B{r0+7}','Catatan: untuk aksi penghindaran, kuota Renops adalah batas atas kumulatif sejak 2013 dan tidak langsung setara pengurangan tahunan; konversi belum didefinisikan (WP-F), sehingga kolom setara dibiarkan #N/A.','note'); sh.merges.append(f'B{r0+7}:H{r0+7}')
    # ---- E cost
    r1=r0+9
    sh.t(f'B{r1}',f'Tabel {num_}.E. Biaya dan pelaksanaan','tbl')
    for c,t in zip('BCDEF',['Butir','Rendah','Tinggi','Satuan','Status']): sh.t(f'{c}{r1+1}',t,'hdr')
    sh.t(f'B{r1+2}','Biaya per tCO2'); sh.f(f'C{r1+2}',f'C_Solusi_2030!G{cfg["rb"]}','n2l'); sh.f(f'D{r1+2}',f'C_Solusi_2030!H{cfg["rb"]}','n2l'); sh.t(f'E{r1+2}','USD per tCO2'); sh.t(f'F{r1+2}','E (Rossita dan Boer 2025)')
    sh.t(f'B{r1+3}','Biaya tahunan CM1 (pengurangan x biaya)'); sh.f(f'C{r1+3}',f'C24*C{r1+2}','n1'); sh.f(f'D{r1+3}',f'C25*D{r1+2}','n1'); sh.t(f'E{r1+3}','USD juta per tahun'); sh.t(f'F{r1+3}','AC')
    sh.t(f'B{r1+4}','Biaya tahunan total CM2'); sh.f(f'C{r1+4}',f'C28*C{r1+2}','n1'); sh.f(f'D{r1+4}',f'C29*D{r1+2}','n1'); sh.t(f'E{r1+4}','USD juta per tahun'); sh.t(f'F{r1+4}','AC')
    sh.t(f'B{r1+5}','Biaya tahunan tambahan CM2 (di atas CM1)'); sh.f(f'C{r1+5}',f'C26*C{r1+2}','n1'); sh.f(f'D{r1+5}',f'C27*D{r1+2}','n1'); sh.t(f'E{r1+5}','USD juta per tahun'); sh.t(f'F{r1+5}','AC')
    if cfg.get('capr'):
        sh.t(f'B{r1+6}','Capaian saat ini terhadap target (C_Solusi Tabel 32.D)'); sh.f(f'C{r1+6}',f'C_Solusi_2030!D{cfg["capr"]}','pcl'); sh.f(f'D{r1+6}',f'C_Solusi_2030!E{cfg["capr"]}','tl'); sh.t(f'E{r1+6}','fraksi dan tahun data'); sh.t(f'F{r1+6}','E')
        sh.t(f'B{r1+7}','Pengurangan CM1 pada pelaksanaan saat ini'); sh.f(f'C{r1+7}',f'C24*C{r1+6}','n2'); sh.f(f'D{r1+7}',f'C25*C{r1+6}','n2'); sh.t(f'E{r1+7}','MtCO2e per tahun'); sh.t(f'F{r1+7}','AC')
    # ---- F chart data
    r2=r1+10
    sh.t(f'B{r2}',f'Tabel {num_}.F. Data grafik: pengurangan menurut tonggak CM','tbl')
    for c,t in zip('BCDEFG',['Tonggak','Pengurangan rendah (MtCO2e)','Pengurangan tinggi (MtCO2e)','Rentang (tinggi dikurangi rendah)','Biaya tahunan rendah (USD juta)','Biaya tahunan tinggi (USD juta)']): sh.t(f'{c}{r2+1}',t,'hdr')
    sh.t(f'B{r2+2}','Tanpa aksi (BaU)'); sh.n(f'C{r2+2}',0,'n2'); sh.n(f'D{r2+2}',0,'n2'); sh.f(f'E{r2+2}',f'D{r2+2}-C{r2+2}','n2'); sh.n(f'F{r2+2}',0,'n1'); sh.n(f'G{r2+2}',0,'n1')
    sh.f(f'B{r2+3}','"CM1 (luas "&ROUND($C$20,0)&" ribu ha)"','tl'); sh.f(f'C{r2+3}','C24','n2'); sh.f(f'D{r2+3}','C25','n2'); sh.f(f'E{r2+3}',f'D{r2+3}-C{r2+3}','n2'); sh.f(f'F{r2+3}',f'C{r1+3}','n1'); sh.f(f'G{r2+3}',f'D{r1+3}','n1')
    sh.f(f'B{r2+4}','"CM2 (luas "&ROUND($C$21,0)&" ribu ha)"','tl'); sh.f(f'C{r2+4}','C28','n2'); sh.f(f'D{r2+4}','C29','n2'); sh.f(f'E{r2+4}',f'D{r2+4}-C{r2+4}','n2'); sh.f(f'F{r2+4}',f'C{r1+4}','n1'); sh.f(f'G{r2+4}',f'D{r1+4}','n1')
    # ---- A summary rows 5..14
    sh.t('B5',f'Tabel {num_}.A. Ringkasan 2030','tbl')
    for c,t in zip('BCDEFG',['Butir','Rendah','Tinggi','Satuan','Status','Sumber']): sh.t(f'{c}6',t,'hdr')
    S_=[('Pengurangan CM1 (lapis A, dalam garis dasar)','C24','C25','MtCO2e per tahun','AC','C_Solusi_2030 lapis A'),
        ('Tambahan CM2 di atas CM1 (lapis B)','C26','C27','MtCO2e per tahun','AC','C_Solusi_2030 lapis B'),
        ('Total CM2','C28','C29','MtCO2e per tahun','AC','hitungan'),
        ('Persen selisih FOLU 2030 yang ditutup tambahan CM2','C26/B_Selisih_Penyebab!$C$8','C27/B_Selisih_Penyebab!$C$8','fraksi','AC','B_Selisih_Penyebab'),
        ('Biaya tahunan tambahan CM2',f'C{r1+5}',f'D{r1+5}','USD juta per tahun','AC','Tabel E'),
        ('Selisih FOLU 2030 (CPOS dikurangi LCCP_L)','B_Selisih_Penyebab!$C$8','B_Selisih_Penyebab!$C$8','MtCO2e','P','D_SNDC')]
    for i,(a,fl,fh,u,st,so) in enumerate(S_):
        r=7+i; sty='pc' if 'Persen' in a else 'n2'; sh.t(f'B{r}',a); sh.f(f'C{r}',fl,sty); sh.f(f'D{r}',fh,sty); sh.t(f'E{r}',u); sh.t(f'F{r}',st); sh.t(f'G{r}',so)
    sh.f('A3',f'"Temuan utama: {lab}: CM1 mengurangi "&ROUND(C24,1)&" sampai "&ROUND(C25,1)&" MtCO2e per tahun pada 2030 (dalam garis dasar) dan tambahan CM2 sebesar "&ROUND(C26,1)&" sampai "&ROUND(C27,1)&" ("&ROUND(C26/B_Selisih_Penyebab!C8*100,1)&" sampai "&ROUND(C27/B_Selisih_Penyebab!C8*100,1)&" persen selisih FOLU 2030); biaya tahunan tambahan CM2 USD "&ROUND(C{r1+5},2)&" sampai "&ROUND(D{r1+5},2)&" juta."','title')
    # ---- charts
    catF=f'{n}!$B${r2+2}:$B${r2+4}'
    def rg(col): return f'{n}!${col}${r2+2}:${col}${r2+4}'
    c1=ck.chart_xml(f'Gambar {num_}.1. {lab}: pengurangan emisi menurut tonggak CM (MtCO2e per tahun), rentang rendah sampai tinggi berarsir',
        [dict(base_ref=rg('C'),band_ref=rg('E'),name_ref=f'{n}!$E${r2+1}',name='Rentang rendah sampai tinggi',fill='F4B183')],
        [dict(val_ref=rg('D'),name_ref=f'{n}!$D${r2+1}',name='Pengurangan tinggi',color='C00000',pos='t'),dict(val_ref=rg('C'),name_ref=f'{n}!$C${r2+1}',name='Pengurangan rendah',color='1F4E79',pos='b')],
        'MtCO2e per tahun','Tonggak (luas bersumber)',catF,cat_numeric=False,yfmt='#,##0.0')
    c2=ck.chart_xml(f'Gambar {num_}.2. {lab}: pengurangan emisi (kiri) dan biaya tahunan (kanan)',[],
        [dict(val_ref=rg('D'),name_ref=f'{n}!$D${r2+1}',name='Pengurangan tinggi',color='C00000',pos='t'),dict(val_ref=rg('C'),name_ref=f'{n}!$C${r2+1}',name='Pengurangan rendah',color='1F4E79',pos='b'),
         dict(val_ref=rg('G'),name_ref=f'{n}!$G${r2+1}',name='Biaya tahunan tinggi',color='BF8F00',pos='t',sec=True,fmt='#,##0.0',dash='sysDash'),dict(val_ref=rg('F'),name_ref=f'{n}!$F${r2+1}',name='Biaya tahunan rendah',color='2E7D32',pos='b',sec=True,fmt='#,##0.0',dash='sysDash',labels=False)],
        'MtCO2e per tahun','Tonggak (luas bersumber)',catF,cat_numeric=False,yfmt='#,##0.0',ytitle2='USD juta per tahun',yfmt2='#,##0')
    sh.charts=[(c1,(1,r2+7,7400000,3800000)),(c2,(8,r2+7,7400000,3800000))]
    if True:
        catD=f'{n}!$B${r0+2}:$B${r0+5}'
        c3=ck.chart_xml(f'Gambar {num_}.3. {lab}: pelaksanaan: target dan capaian dalam setara emisi (MtCO2e per tahun); hanya aksi praktik',
            [dict(base_ref=f'{n}!$F${r0+2}:$F${r0+5}',band_ref=f'{n}!$I${r0+2}:$I${r0+5}',name='Rentang faktor rendah sampai tinggi',fill='F4B183')],
            [dict(val_ref=f'{n}!$G${r0+2}:$G${r0+5}',name='Setara, faktor tinggi',color='C00000',pos='t'),dict(val_ref=f'{n}!$F${r0+2}:$F${r0+5}',name='Setara, faktor rendah',color='1F4E79',pos='b')],
            'MtCO2e per tahun','Target dan capaian bersumber',catD,cat_numeric=False,yfmt='#,##0.0')
        for i in range(4): sh.f(f'I{r0+2+i}',f'IFERROR(G{r0+2+i}-F{r0+2+i},NA())','n2')
        sh.t(f'I{r0+1}','Rentang (tinggi dikurangi rendah)','hdr')
        sh.charts.append((c3,(1,r2+28,7400000,3800000)))
    sh.width('A','A',3); sh.width('B','B',50); sh.width('C','C',22); sh.width('D','D',34); sh.width('E','I',18); sh.width('H','H',40)
    sh.rows=dict(r1=r1,r2=r2,r0=r0)
    return sh
def _main2():
    import importlib.util
    spec=importlib.util.spec_from_file_location('bmod','/home/user/NetZeroEmission/scripts/09_build_model_B.py'); bm=importlib.util.module_from_spec(spec); sys.argv=['x']; spec.loader.exec_module(bm)
    gp=bm.B_Garis_Pembangunan(); sel=bm.B_Selisih(gp)
    fs=[folu_sheet(c) for c in FOLU_CFG]
    cache,errs=build('/tmp/claude-0/base_model.xlsx','/tmp/claude-0/stageF.xlsx',[gp,sel]+fs,[])
    print([e for e in errs if 'NA()' not in e[3] and 'IFERROR' not in e[3]][:8])
    for s in fs: print(s.name,cache.get((s.name,'A3'),'')[:200],'| uji',cache.get((s.name,'C30')))
if __name__=='__main__' and 'FOLU' in sys.argv: _main2()
