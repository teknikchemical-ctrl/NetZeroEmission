"""Blok B: garis pembangunan (dari rencana), garis NZE, selisih menurut penyebab. Lembar 98 sampai 101."""
import sys; sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from modelkit import *; import chartkit as ck; import src
YR=list(range(2025,2035)); 
def rowfind(sheet,txt,**k): return src.find_row(sheet,txt,**k)
def ccol(i): return CL(i)
def B_Pendorong():
    sh=Sheet('B_Pendorong')
    pc=src.year_cols('C_Pembangkit',16); lc=src.year_cols('C_Listrik_Rencana',6); rc=src.year_cols('D_RUPTL_Tambahan',4)
    r_gem=rowfind('C_Pembangkit','Unit GEM beroperasi',start=16); r_add=rowfind('C_Pembangkit','Kapasitas on-grid tanpa',start=16); r_em=rowfind('C_Pembangkit','Emisi, tanpa pensiun',start=16)
    r_ared=rowfind('C_Listrik_Rencana','Emisi batubara RUPTL ARE'); r_rebase=rowfind('C_Listrik_Rencana','Emisi batubara RUPTL RE')
    r_gu=rowfind('D_RUPTL_Tambahan','PLTGU',col=1,start=5)
    sh.t('A1','Lembar 98. Pendorong garis pembangunan: emisi dari rencana dan kebijakan (aktivitas x faktor emisi)',  'title')
    sh.t('A2','Garis pembangunan dibangun dari bawah ke atas: tiap pendorong adalah aktivitas yang direncanakan dikali faktor emisi bersumber. Hanya titik bersumber dan hitungan sederhana (kali, bagi, jumlah). Biru: masukan ketikan bersumber; hijau: tautan lembar lain; hitam: hitungan. Blok yang belum terukur dibiarkan kosong untuk diisi tim (kode WP).','title')
    sh.f('A3','"Temuan utama: PLTU baru dalam RUPTL RE Base menambah "&ROUND(K20,1)&" MtCO2 pada 2030 dan "&ROUND(O20,1)&" pada 2034; emisi pembangkitan RUPTL 2030 ("&ROUND(C34,0)&") melampaui batas JETP ("&ROUND(C32,0)&") sebesar "&ROUND(C34-C32,0)&" MtCO2."','title')
    # --- A: parameters
    sh.t('B5','Tabel 98.A. Parameter pendorong listrik','tbl')
    for c,h in zip('BCDEF',['Parameter','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}6',h,'hdr')
    P=[('Faktor kapasitas PLTU batubara 2025 (dipertahankan)',f"C_Pembangkit!E10",'fraksi','AC','C_Pembangkit (produksi batubara RUPTL dibagi kapasitas)','n2l','f'),
       ('Faktor emisi PLTU batubara 2025 (dipertahankan)',f"C_Pembangkit!E11",'tCO2 per MWh','AC','C_Pembangkit (emisi dibagi produksi); rentang resmi 0,911 sampai 1,297 (Sunanda dkk. 2026, K137)','n2l','f'),
       ('Faktor kapasitas PLTGU (gas)',0.55,'fraksi','R','Afriani dan Poletti 2026, bagian 5.1','n2i','n'),
       ('Efisiensi PLTGU',0.50,'fraksi','R','Nursidik dkk. 2025, Tabel 4 (PLTGU 50 persen)','n2i','n'),
       ('Faktor emisi gas bumi (basis energi bahan bakar)',201.96,'kg per MWh termal','R','Sunanda dkk. 2026, Tabel 6','n2i','n'),
       ('Faktor emisi listrik PLTGU',None,'tCO2 per MWh','AC','Faktor gas dibagi 1.000 dibagi efisiensi','n2','f'),
       ('Jam per tahun',8760,'jam','D','Definisi','n0i','n')]
    for i,(a,v,u,st,so,sty,k) in enumerate(P):
        r=7+i; sh.t(f'B{r}',a); 
        if k=='f': sh.f(f'C{r}',v if v else 'C11/1000/C10',sty)
        else: sh.n(f'C{r}',v,sty)
        sh.t(f'D{r}',u); sh.t(f'E{r}',st); sh.t(f'F{r}',so)
    # --- B: yearly drivers
    sh.t('B15','Tabel 98.B. Pendorong listrik per tahun (RUPTL 2025 sampai 2034)','tbl')
    for c,h in zip('BCDE',['ID','Pendorong','Satuan','Status']): sh.t(f'{c}16',h,'hdr')
    ycol={y:CL(6+i) for i,y in enumerate(YR)}   # F..O
    for y in YR: sh.n(f'{ycol[y]}16',y,'hdr')
    sh.t('P16','Sumber dan catatan','hdr')
    rows=[('L1','PLTU batubara on-grid RUPTL RE Base (dilaporkan RUPTL)','MtCO2','P','C_Listrik_Rencana baris 7 (RUPTL 2025 sampai 2034)'),
          ('L2','PLTU batubara RUPTL ARED','MtCO2','P','C_Listrik_Rencana baris 8'),
          ('L3','Kapasitas PLTU baru RUPTL, kumulatif','MW','AC','C_Pembangkit: kapasitas on-grid dikurangi unit GEM'),
          ('L4','Emisi dari PLTU baru RUPTL','MtCO2','AC','L3 x faktor kapasitas x jam x faktor emisi'),
          ('L5','Emisi PLTU di luar tambahan baru (eksisting dan lainnya)','MtCO2','AC','L1 dikurangi L4'),
          ('G1','Kapasitas PLTGU baru RUPTL RE Base, kumulatif','MW','AC','D_RUPTL_Tambahan baris PLTGU'),
          ('G2','Emisi dari PLTGU baru RUPTL','MtCO2','AC','G1 x faktor kapasitas gas x jam x faktor emisi gas listrik'),
          ('K1','PLTU captive 2030 (hanya titik 2030)','GW','E','Squire dkk. 2024: 17,7 GW (127 unit); emisi belum dihitung karena faktor kapasitas captive tidak bersumber (WP-A)')]
    for i,(id_,nm,u,st,so) in enumerate(rows):
        r=17+i; sh.t(f'B{r}',id_); sh.t(f'C{r}',nm); sh.t(f'D{r}',u); sh.t(f'E{r}',st); sh.t(f'P{r}',so)
        for y in YR:
            c=ycol[y]
            if id_=='L1': sh.f(f'{c}{r}',f"C_Listrik_Rencana!{lc[y]}{r_rebase}",'n1l')
            elif id_=='L2': sh.f(f'{c}{r}',f"C_Listrik_Rencana!{lc[y]}{r_ared}",'n1l')
            elif id_=='L3': sh.f(f'{c}{r}',f"C_Pembangkit!{pc[y]}{r_add}-C_Pembangkit!{pc[y]}{r_gem}",'n0l')
            elif id_=='L4': sh.f(f'{c}{r}',f"{c}19*$C$7*$C$13*$C$8/1000000",'n1')
            elif id_=='L5': sh.f(f'{c}{r}',f"{c}17-{c}20",'n1')
            elif id_=='G1': sh.f(f'{c}{r}',f"SUM(D_RUPTL_Tambahan!$D${r_gu}:{rc[y]}{r_gu})",'n0l')
            elif id_=='G2': sh.f(f'{c}{r}',f"{c}22*$C$9*$C$13*$C$12/1000000",'n1')
            elif id_=='K1': 
                if y==2030: sh.n(f'{c}{r}',17.7,'n1i')
                else: sh.f(f'{c}{r}','NA()','n1')
    # comparison points 2030
    r_j=rowfind('D_JETP','Batas emisi sektor listrik',start=1,end=12)
    r_jr=rowfind('D_JETP','Emisi pembangkitan RUPTL 2025',start=36)
    sh.t('B25','Titik pembanding 2030 (JETP CIPP dan RUKN)','tbl')
    cmp_=[('J1','Batas JETP CIPP on-grid 2030',f'D_JETP!C{r_j}'),('J2','Proyeksi draf RUKN 2030',f'D_JETP!C{rowfind("D_JETP","Proyeksi draf RUKN",start=1,end=12)}'),('J3','Emisi pembangkitan RUPTL 2030 (RE Base)',f'D_JETP!C{r_jr}')]
    for i,(id_,nm,f_) in enumerate(cmp_):
        r=26+i; sh.t(f'B{r}',id_); sh.t(f'C{r}',nm); sh.t(f'D{r}','MtCO2'); sh.t(f'E{r}','P'); sh.t(f'P{r}','D_JETP (CIPP hlm 3, 78; RUPTL 2025 sampai 2034)')
        for y in YR:
            c=ycol[y]
            if y==2030: sh.f(f'{c}{r}',f_,'n1l')
            else: sh.f(f'{c}{r}','NA()','n1')
    # fix finding references: put 2030 values in col K, 2034 in O (rows 20); C32/C34 -> use J rows
    sh.cells['A3']=('f','"Temuan utama: PLTU baru dalam RUPTL RE Base menambah "&ROUND(K20,1)&" MtCO2 pada 2030 dan "&ROUND(O20,1)&" pada 2034; emisi pembangkitan RUPTL 2030 ("&ROUND(K28,0)&") melampaui batas JETP ("&ROUND(K26,0)&") sebesar "&ROUND(K28-K26,0)&" MtCO2 (hanya PLTU on-grid; PLTU captive belum terukur)."',S['title'])
    # --- C: land drivers (model v2.1)
    mv=src.year_cols('D_Model_v21',5)
    LY=list(range(2024,2036)); lcol={y:CL(6+i) for i,y in enumerate(LY)}  # F..Q
    sh.t('B31','Tabel 98.C. Pendorong lahan: laju deforestasi dan FOLU neto, tiga skenario model v2.1 (salinan nilai; model tidak diubah)','tbl')
    for c,h in zip('BCDE',['ID','Pendorong','Satuan','Status']): sh.t(f'{c}32',h,'hdr')
    for y in LY: sh.n(f'{lcol[y]}32',y,'hdr')
    sh.t('R32','Sumber dan catatan','hdr')
    blocks=[('Adverse',6,7),('Central',15,16),('Ambitious',24,25)]
    for i,(nm,rd,rf) in enumerate(blocks):
        r1=33+2*i; r2=34+2*i
        sh.t(f'B{r1}',f'D{i+1}'); sh.t(f'C{r1}',f'Deforestasi, skenario {nm}'); sh.t(f'D{r1}','ha per tahun'); sh.t(f'E{r1}','AC'); sh.t(f'R{r1}','D_Model_v21 (asumsi model; bukan rencana resmi)')
        sh.t(f'B{r2}',f'F{i+1}'); sh.t(f'C{r2}',f'FOLU neto, skenario {nm}'); sh.t(f'D{r2}','MtCO2e'); sh.t(f'E{r2}','AC'); sh.t(f'R{r2}','D_Model_v21 (hasil model)')
        for y in LY:
            sh.f(f'{lcol[y]}{r1}',f'D_Model_v21!{mv[y]}{rd}','n0l'); sh.f(f'{lcol[y]}{r2}',f'D_Model_v21!{mv[y]}{rf}','n1l')
    r_inv=src.find_row('D_KLH_Inventaris','2024',col=1,start=5)
    sh.t('B39','F0'); sh.t('C39','FOLU neto inventaris 2024 (realisasi)'); sh.t('D39','MtCO2e'); sh.t('E39','R'); sh.t('R39','D_KLH_Inventaris (FOLU, Mt)')
    for y in LY:
        if y==2024: sh.f(f'{lcol[y]}39',f'D_KLH_Inventaris!I{r_inv}' if False else f'D_KLH_Inventaris!{src.label_col("D_KLH_Inventaris",4,"FOLU (Mt)")}{r_inv}','n1l')
        else: sh.f(f'{lcol[y]}39','NA()','n1')
    # --- D: unmeasured blocks (structure for team)
    sh.t('B42','Tabel 98.D. Blok pendorong yang belum terukur (diisi tim; jumlah otomatis)','tbl')
    for c,h in zip('BCDE',['ID','Pendorong','Satuan','Kode WP']): sh.t(f'{c}43',h,'hdr')
    for i,y in enumerate(YR): sh.t(f'{CL(6+i)}43',str(y),'hdr')
    sh.t('P43','Catatan','hdr')
    un=[('M1','Minyak dan gas hulu: emisi per aktivitas (produksi, flaring, venting, fugitive)','MtCO2e','WP-C'),('M2','Minyak dan gas tengah dan hilir (pemrosesan, LNG, kilang)','MtCO2e','WP-C'),('M3','Batubara hulu: metana fugitive tambang','MtCO2e','WP-E'),('M4','PLTU captive (kapasitas x faktor kapasitas x faktor emisi)','MtCO2','WP-A'),('M5','Transportasi (pertumbuhan armada dan bahan bakar)','MtCO2e','WP-I'),('M6','Industri (kapasitas smelter, semen, baja, pupuk)','MtCO2e','WP-I'),('M7','Gedung dan rumah tangga (pendingin, LPG)','MtCO2e','WP-I')]
    for i,(id_,nm,u,wp) in enumerate(un):
        r=44+i; sh.t(f'B{r}',id_); sh.t(f'C{r}',nm); sh.t(f'D{r}',u); sh.t(f'E{r}',wp); sh.t(f'P{r}','Belum terukur: biarkan kosong sampai data bersumber tersedia (RESEARCH_PLAN_TIM.md)')
        for y in YR: sh.blank(f'{ycol[y]}{r}','n1i')
    r_cap=rowfind('D_Energi_Potensi','Emisi PLTU captive fosil',col=3)
    sh.f('F47',f'D_Energi_Potensi!E{r_cap}','n1l'); sh.t('P47','Terukur sebagian: kolom 2025 memuat emisi dasar 2024 (Ember, 48 persen emisi listrik 2024, status E); proyeksi 2025 sampai 2034 belum ada (WP-A). Kapasitas captive 25,9 GW (2024) dan 17,7 GW fosil pada 2030 (Squire 2024).')
    sh.t('B51','Jumlah blok belum terukur (otomatis)'); 
    for y in YR: sh.f(f'{ycol[y]}51',f'SUM({ycol[y]}44:{ycol[y]}50)','n1')
    sh.width('A','A',3); sh.width('B','B',9); sh.width('C','C',58); sh.width('D','D',14); sh.width('E','E',10); sh.width('F','Q',10); sh.width('P','P',70); sh.width('R','R',48)
    # charts
    cat='B_Pendorong!$F$16:$O$16'
    c1=ck.chart_xml('Gambar 98.1. Emisi PLTU batubara on-grid menurut RUPTL: eksisting dan PLTU baru (arsir), dibanding batas JETP, draf RUKN, dan RUPTL 2030',
      [dict(base_ref='B_Pendorong!$F$21:$O$21',band_ref='B_Pendorong!$F$20:$O$20',name_ref='B_Pendorong!$C$20',name='Emisi dari PLTU baru RUPTL',fill='F4B183')],
      [dict(val_ref='B_Pendorong!$F$17:$O$17',name_ref='B_Pendorong!$C$17',name='PLTU RE Base',color='C00000',pos='t'),
       dict(val_ref='B_Pendorong!$F$18:$O$18',name_ref='B_Pendorong!$C$18',name='ARED',color='7F7F7F',pos='b',labels=False,dash='sysDash'),
       dict(val_ref='B_Pendorong!$F$21:$O$21',name_ref='B_Pendorong!$C$21',name='Eksisting',color='1F4E79',pos='b'),
       dict(val_ref='B_Pendorong!$F$26:$O$26',name_ref='B_Pendorong!$C$26',name='Batas JETP',color='2E7D32',marker='diamond',msize=9,pos='b',width=12700),
       dict(val_ref='B_Pendorong!$F$27:$O$27',name_ref='B_Pendorong!$C$27',name='Draf RUKN',color='BF8F00',marker='diamond',msize=9,pos='r',width=12700),
       dict(val_ref='B_Pendorong!$F$28:$O$28',name_ref='B_Pendorong!$C$28',name='RUPTL 2030',color='7030A0',marker='diamond',msize=9,pos='t',width=12700)],
      'MtCO2 per tahun','Tahun',cat,yfmt='#,##0',ymin=200,ymax=400)
    cat2='B_Pendorong!$F$32:$Q$32'
    c2=ck.chart_xml('Gambar 98.2. Laju deforestasi per skenario model v2.1 (ha per tahun)',[],
      [dict(val_ref='B_Pendorong!$F$33:$Q$33',name_ref='B_Pendorong!$C$33',name='Adverse',color='C00000',pos='t',fmt='#,##0'),
       dict(val_ref='B_Pendorong!$F$35:$Q$35',name_ref='B_Pendorong!$C$35',name='Central',color='BF8F00',pos='t',labels=False),
       dict(val_ref='B_Pendorong!$F$37:$Q$37',name_ref='B_Pendorong!$C$37',name='Ambitious',color='2E7D32',pos='b',fmt='#,##0')],
      'ha per tahun','Tahun',cat2,yfmt='#,##0')
    c3=ck.chart_xml('Gambar 98.3. FOLU neto per skenario model v2.1 dan inventaris 2024 (MtCO2e)',[],
      [dict(val_ref='B_Pendorong!$F$34:$Q$34',name_ref='B_Pendorong!$C$34',name='Adverse',color='C00000',pos='t'),
       dict(val_ref='B_Pendorong!$F$36:$Q$36',name_ref='B_Pendorong!$C$36',name='Central',color='BF8F00',pos='t',labels=False),
       dict(val_ref='B_Pendorong!$F$38:$Q$38',name_ref='B_Pendorong!$C$38',name='Ambitious',color='2E7D32',pos='b'),
       dict(val_ref='B_Pendorong!$F$39:$Q$39',name_ref='B_Pendorong!$C$39',name='Inventaris 2024',color='000000',marker='diamond',msize=10,pos='l')],
      'MtCO2e','Tahun',cat2,yfmt='#,##0')
    EMU=(640000,520000)
    sh.charts=[(c1,(1,54,9200000,4400000)),(c2,(1,77,7000000,3800000)),(c3,(10,77,7000000,3800000))]
    return sh
if __name__=='__main__':
    sheets=[B_Pendorong()]
    cache,errs=build('/tmp/claude-0/base_model.xlsx','/tmp/claude-0/stageB.xlsx',sheets,[])
    print('errors',errs)
    for k in ['A3','K20','O20','K28','K26']: print(k,cache.get(('B_Pendorong',k)))

# ======================= Lembar 99, 100, 101 =======================
SECT=['Energi','IPPU','Limbah','Pertanian','FOLU','Neto']
def sndc_row(scen,sector):
    w=src.ws('D_SNDC')
    for r in range(1,70):
        if w.cell(r,1).value==scen and w.cell(r,2).value==sector and w.cell(r,8).value=='MtCO2e': return r
    raise KeyError((scen,sector))
YRS5=[2019,2025,2030,2035,2060]; Y5C=dict(zip(YRS5,'DEFGH'))   # columns in table 99.A
def B_Garis_Pembangunan():
    sh=Sheet('B_Garis_Pembangunan')
    sh.t('A1','Lembar 99. Garis pembangunan dan jalur net zero per sektor pada tahun bersumber (SNDC 2025), dibanding model v2.1 dan inventaris','title')
    sh.t('A2','Garis pembangunan resmi = CPOS (kebijakan berjalan); target = LCCP_L (jalur net zero yang dipakai) dan LCCP_H. Hanya titik bersumber (2019, 2025, 2030, 2035, 2060); garis grafik menghubungkan titik bersumber dan bukan proyeksi. Satuan MtCO2e.','title')
    sh.f('A3','"Temuan utama: selisih CPOS terhadap LCCP_L sebesar "&ROUND(F37,0)&" MtCO2e pada 2030 dan "&ROUND(H37,0)&" pada 2060; pendorong terukur (PLTU on-grid dan PLTGU baru) baru menjelaskan "&ROUND(D59*100,0)&" persen emisi energi CPOS 2030."','title')
    sh.t('B5','Tabel 99.A. CPOS, LCCP_L, LCCP_H, dan selisih menurut sektor (D_SNDC Tabel 1)','tbl')
    for c,h in zip('BC',['Sektor','Garis']): sh.t(f'{c}6',h,'hdr')
    for y in YRS5: sh.n(f'{Y5C[y]}6',y,'hdr')
    sh.t('I6','Satuan','hdr'); sh.t('J6','Status','hdr'); sh.t('K6','Sumber','hdr')
    r=7; refs={}
    for sct in SECT:
        for nm,key in (('CPOS','CPOS'),('LCCP_L','LCCP_L'),('LCCP_H','LCCP_H')):
            sr=sndc_row(key,sct); sh.t(f'B{r}',sct); sh.t(f'C{r}',nm)
            for y in YRS5: sh.f(f'{Y5C[y]}{r}',f'D_SNDC!{ {2019:"C",2025:"D",2030:"E",2035:"F",2060:"G"}[y] }{sr}','n1l')
            sh.t(f'I{r}','MtCO2e'); sh.t(f'J{r}','P'); sh.t(f'K{r}',f'D_SNDC Tabel 56.B baris {sr}'); refs[(sct,key)]=r; r+=1
        sh.t(f'B{r}',sct); sh.t(f'C{r}','Selisih CPOS dikurangi LCCP_L')
        for y in YRS5: sh.f(f'{Y5C[y]}{r}',f'{Y5C[y]}{refs[(sct,"CPOS")]}-{Y5C[y]}{refs[(sct,"LCCP_L")]}','n1')
        sh.t(f'I{r}','MtCO2e'); sh.t(f'J{r}','AC'); sh.t(f'K{r}','Hitungan sederhana'); refs[(sct,'gap')]=r; r+=1
    # r now 7+24=31 ; row 37 expected for Neto gap? compute
    gap_net=refs[('Neto','gap')]
    sh.cells['A3']=('f',f'"Temuan utama: selisih CPOS terhadap LCCP_L sebesar "&ROUND(F{gap_net},0)&" MtCO2e pada 2030 dan "&ROUND(H{gap_net},0)&" pada 2060; pendorong terukur (PLTU on-grid dan PLTGU baru) baru menjelaskan "&ROUND(F{r+16}*100,0)&" persen emisi energi CPOS 2030."',S['title'])
    # --- B: model v2.1 vs CPOS at 2030
    sh.t(f'B{r+1}','Tabel 99.B. Pembanding 2030: CPOS, model v2.1 (tiga skenario), dan inventaris terbaru (MtCO2e)','tbl')
    h=['Sektor','CPOS 2030','Model v2.1 Adverse','Model v2.1 Central','Model v2.1 Ambitious','Selisih Central dikurangi CPOS','LCCP_L 2030','Inventaris 2024 (R)']
    for c,t in zip('BCDEFGHI',h): sh.t(f'{c}{r+2}',t,'hdr')
    mvc=src.year_cols('D_Model_v21',5)['2030' if False else 2030]
    mv_rows={'Energi':(11,20,29),'IPPU':(8,17,26),'Limbah':(10,19,28),'Pertanian':(9,18,27),'FOLU':(7,16,25),'Neto':(12,21,30)}
    invc={'Energi':'H','IPPU':'I','Pertanian':'J','FOLU':'K','Limbah':'L','Neto':'M'}
    r_inv=src.find_row('D_KLH_Inventaris','2024',col=1,start=5)
    hdr_inv=[c.value for c in src.ws('D_KLH_Inventaris')[4]]
    def invcol(label):
        for i,v in enumerate(hdr_inv):
            if v==label: return CL(i+1)
    invl={'Energi':'Energi (Mt)','IPPU':'IPPU (Mt)','Pertanian':'Pertanian (Mt)','FOLU':'FOLU (Mt)','Limbah':'Limbah (Mt)'}
    rb=r+3
    for i,sct in enumerate(SECT):
        rr=rb+i; sh.t(f'B{rr}',sct)
        sh.f(f'C{rr}',f'F{refs[(sct,"CPOS")]}','n1')
        for c,mr in zip('DEF',mv_rows[sct]): sh.f(f'{c}{rr}',f'D_Model_v21!{mvc}{mr}','n1l')
        sh.f(f'G{rr}',f'E{rr}-C{rr}','n1'); sh.f(f'H{rr}',f'F{refs[(sct,"LCCP_L")]}','n1')
        if sct in invl: sh.f(f'I{rr}',f'D_KLH_Inventaris!{invcol(invl[sct])}{r_inv}','n1l')
        else: sh.f(f'I{rr}',f'SUM(I{rb}:I{rb+4})','n1')
    # headers fix: columns are C..I -> map header text
    rt=rb+len(SECT)+1
    sh.t(f'B{rt}','Catatan 99.B. Model v2.1 (dokumen pengguna, tidak diubah) berbeda jauh dari CPOS pada energi dan limbah; perbedaan dicatat sebagai temuan, bukan diselesaikan. Basis FOLU inventaris dan SNDC juga berbeda (K27 dan K28).','note')
    sh.merges.append(f'B{rt}:K{rt}')
    # --- C: coverage
    rc=rt+2
    sh.t(f'B{rc}','Tabel 99.C. Cakupan pendorong terukur terhadap emisi energi CPOS 2030','tbl')
    for c,t in zip('BCD',['Butir','MtCO2','Persen emisi energi CPOS 2030']): sh.t(f'{c}{rc+1}',t,'hdr')
    items=[('PLTU batubara on-grid RUPTL RE Base (B_Pendorong L1)','B_Pendorong!K17','n1l'),('PLTGU baru RUPTL (B_Pendorong G2)','B_Pendorong!K23','n1l')]
    for i,(a,f_,sty) in enumerate(items):
        rr=rc+2+i; sh.t(f'B{rr}',a); sh.f(f'C{rr}',f_,sty); sh.f(f'D{rr}',f'C{rr}/$C${rc+5}','pc')
    rr=rc+4; sh.t(f'B{rr}','Jumlah pendorong terukur'); sh.f(f'C{rr}',f'SUM(C{rc+2}:C{rc+3})','n1'); sh.f(f'D{rr}',f'C{rr}/$C${rc+5}','pc')
    rr=rc+5; sh.t(f'B{rr}','Emisi energi CPOS 2030 (D_SNDC)'); sh.f(f'C{rr}',f'F{refs[("Energi","CPOS")]}','n1'); sh.f(f'D{rr}',f'C{rr}/C{rr}','pc')
    rr=rc+6; sh.t(f'B{rr}','Belum terukur oleh pendorong (minyak dan gas, transportasi, industri, gedung, captive, fugitive, dan lainnya)'); sh.f(f'C{rr}',f'C{rc+5}-C{rc+4}','n1'); sh.f(f'D{rr}',f'C{rr}/C{rc+5}','pc')
    covrow=rc+4
    sh.cells['A3']=('f',f'"Temuan utama: selisih CPOS terhadap LCCP_L sebesar "&ROUND(F{gap_net},0)&" MtCO2e pada 2030 dan "&ROUND(H{gap_net},0)&" pada 2060; pendorong terukur (PLTU on-grid dan PLTGU baru) baru menjelaskan "&ROUND(D{covrow}*100,0)&" persen emisi energi CPOS 2030."',S['title'])
    # --- D: yearly lines for charts (model v2.1 + SNDC points)
    rd=rc+9; sh.t(f'B{rd}','Tabel 99.D. Total neto dan energi: model v2.1 (tahunan) dan titik SNDC (CPOS, LCCP_L)','tbl')
    LY=list(range(2024,2036)); lcol={y:CL(5+i) for i,y in enumerate(LY)}   # E..P
    for c,t in zip('BCD',['Butir','Garis','Satuan']): sh.t(f'{c}{rd+1}',t,'hdr')
    for y in LY: sh.n(f'{lcol[y]}{rd+1}',y,'hdr')
    mvy=src.year_cols('D_Model_v21',5)
    series=[('Neto','Model v2.1 Adverse',12,'mv'),('Neto','Model v2.1 Central',21,'mv'),('Neto','Model v2.1 Ambitious',30,'mv'),('Neto','CPOS (SNDC)',None,'CPOS'),('Neto','LCCP_L (SNDC)',None,'LCCP_L'),
            ('Energi','Model v2.1 Adverse',11,'mv'),('Energi','Model v2.1 Central',20,'mv'),('Energi','Model v2.1 Ambitious',29,'mv'),('Energi','CPOS (SNDC)',None,'CPOS'),('Energi','LCCP_L (SNDC)',None,'LCCP_L')]
    ymap={2025:'E',2030:'F',2035:'G'}
    dd={}
    for i,(sct,nm,mr,kind) in enumerate(series):
        rr=rd+2+i; dd[(sct,nm)]=rr; sh.t(f'B{rr}',sct); sh.t(f'C{rr}',nm); sh.t(f'D{rr}','MtCO2e')
        for y in LY:
            c=lcol[y]
            if kind=='mv': sh.f(f'{c}{rr}',f'D_Model_v21!{mvy[y]}{mr}','n1l')
            elif y in ymap: sh.f(f'{c}{rr}',f'{ymap[y]}{refs[(sct,kind)]}','n1')
            else: sh.f(f'{c}{rr}','NA()','n1')
    # charts
    EM=9000000
    cats='B_Garis_Pembangunan!$D$6:$H$6'
    def band_chart(sct,title):
        g=refs[(sct,'gap')]; l=refs[(sct,'LCCP_L')]; c_=refs[(sct,'CPOS')]; lh=refs[(sct,'LCCP_H')]
        return ck.chart_xml(title,
          [dict(base_ref=f'B_Garis_Pembangunan!$D${l}:$H${l}',band_ref=f'B_Garis_Pembangunan!$D${g}:$H${g}',name_ref=f'B_Garis_Pembangunan!$C${g}',name='Selisih CPOS dikurangi LCCP_L',fill='F4B183')],
          [dict(val_ref=f'B_Garis_Pembangunan!$D${c_}:$H${c_}',name_ref=f'B_Garis_Pembangunan!$C${c_}',name='CPOS',color='C00000',pos='t'),
           dict(val_ref=f'B_Garis_Pembangunan!$D${l}:$H${l}',name_ref=f'B_Garis_Pembangunan!$C${l}',name='LCCP_L',color='1F4E79',pos='b'),
           dict(val_ref=f'B_Garis_Pembangunan!$D${lh}:$H${lh}',name_ref=f'B_Garis_Pembangunan!$C${lh}',name='LCCP_H',color='7F7F7F',pos='r',labels=False,dash='sysDash',marker='none')],
          'MtCO2e','Tahun (titik bersumber, jarak tidak proporsional)',cats,cat_numeric=True,yfmt='#,##0')
    ch=[band_chart('Energi','Gambar 99.1. Energi: CPOS dan LCCP_L, selisih berarsir'),band_chart('FOLU','Gambar 99.2. FOLU: CPOS dan LCCP_L, selisih berarsir'),band_chart('Neto','Gambar 99.3. Total neto: CPOS dan LCCP_L, selisih berarsir')]
    cy=f'B_Garis_Pembangunan!${lcol[2024]}${rd+1}:${lcol[2035]}${rd+1}'
    def mv_chart(sct,idxs,title):
        L=[]
        cols=['C00000','BF8F00','2E7D32','000000','1F4E79']
        for k,nm in enumerate(['Model v2.1 Adverse','Model v2.1 Central','Model v2.1 Ambitious','CPOS (SNDC)','LCCP_L (SNDC)']):
            rr=dd[(sct,nm)]
            L.append(dict(val_ref=f'B_Garis_Pembangunan!${lcol[2024]}${rr}:${lcol[2035]}${rr}',name_ref=f'B_Garis_Pembangunan!$C${rr}',name=nm,color=cols[k],pos='t' if k<3 else ('t' if k==3 else 'b'),marker='circle' if k<3 else 'diamond',msize=7 if k<3 else 11,labels=(k in (0,2,3,4)),width=19050 if k<3 else 12700))
        return ck.chart_xml(title,[],L,'MtCO2e','Tahun',cy,cat_numeric=True,yfmt='#,##0')
    ch+= [mv_chart('Neto',None,'Gambar 99.4. Total neto: tiga skenario model v2.1 dan titik SNDC (CPOS, LCCP_L)'),mv_chart('Energi',None,'Gambar 99.5. Energi: tiga skenario model v2.1 dan titik SNDC (CPOS, LCCP_L)')]
    top=rd+14
    sh.charts=[(ch[0],(1,top,7800000,4000000)),(ch[1],(8,top,7800000,4000000)),(ch[2],(1,top+22,7800000,4000000)),(ch[3],(8,top+22,7800000,4000000)),(ch[4],(1,top+44,7800000,4000000))]
    sh.width('A','A',3); sh.width('B','B',34); sh.width('C','C',32); sh.width('D','P',13); sh.width('K','K',30)
    sh.refs=refs; sh.covrow=covrow
    return sh
if __name__=='__main__' and 'B2' in sys.argv:
    sheets=[B_Pendorong(),B_Garis_Pembangunan()]
    cache,errs=build('/tmp/claude-0/base_model.xlsx','/tmp/claude-0/stageB2.xlsx',sheets,[])
    print([e for e in errs if 'NA()' not in e[3]])
    for k in ['A3']: print(cache.get(('B_Garis_Pembangunan',k)))

def B_Garis_NZE(gp):
    sh=Sheet('B_Garis_NZE'); refs=gp.refs
    sh.t('A1','Lembar 100. Garis net zero (target): LCCP_L menurut sektor dan jalur bersumber lain','title')
    sh.t('A2','Target yang dipakai: jalur LCCP_L (SNDC 2025), yang paling mapan. Jalur lain dicatat sebagai pembanding berstatus bersumber. Titik bersumber saja; garis grafik menghubungkan titik dan bukan proyeksi.','title')
    sh.f('A3','"Temuan utama: LCCP_L menuntut emisi neto "&ROUND(H8,0)&" MtCO2e pada 2060 (energi "&ROUND(H9,0)&", FOLU "&ROUND(H12,0)&"); jalur on-grid JETP menurun dari "&ROUND(D19,0)&" pada 2025 menjadi "&ROUND(F19,0)&" pada 2050."','title')
    sh.t('B5','Tabel 100.A. LCCP_L per sektor pada tahun bersumber (tautan ke Lembar 99)','tbl')
    sh.t('B6','Sektor','hdr'); sh.t('C6','Garis','hdr')
    for y in YRS5: sh.n(f'{Y5C[y]}6',y,'hdr')
    rows=['Neto','Energi','IPPU','Limbah','Pertanian','FOLU']
    for i,sct in enumerate(rows):
        r=8+i if False else 7+i
        sh.t(f'B{r}',sct); sh.t(f'C{r}','LCCP_L')
        for y in YRS5: sh.f(f'{Y5C[y]}{r}',f'B_Garis_Pembangunan!{Y5C[y]}{refs[(sct,"LCCP_L")]}','n1l')
    # A3 refs: Neto row7? fix text to use row numbers
    sh.cells['A3']=('f','"Temuan utama: LCCP_L menuntut emisi neto "&ROUND(H7,0)&" MtCO2e pada 2060 (energi "&ROUND(H8,0)&", FOLU "&ROUND(H12,0)&"); jalur on-grid JETP menurun dari "&ROUND(E19,0)&" MtCO2 pada 2025 menjadi "&ROUND(H19,0)&" pada 2050."',S['title'])
    sh.t('B15','Tabel 100.B. Jalur emisi on-grid listrik, skenario JETP CIPP (MtCO2)','tbl')
    for c,t in zip('BCDEFGH',['Garis','Satuan','Status']+['','','','']): 
        if t: sh.t(f'{c}16',t,'hdr')
    JY=[2021,2025,2030,2040,2050]; jc=dict(zip(JY,'DEFGH'))
    sh.t('B16','Garis','hdr'); sh.t('C16','Sumber','hdr')
    for y in JY: sh.n(f'{jc[y]}16',y,'hdr')
    sh.t('B17','Batas dan puncak JETP 2030 (batas 250; puncak 290)'); sh.t('C17','D_JETP')
    jr={2021:'Emisi CO2 on-grid, skenario JETP',}
    w=src.ws('D_JETP'); jrows={}
    for r in range(6,26):
        b=w.cell(r,2).value; yv=w.cell(r,5).value
        if isinstance(b,str) and b.startswith('Emisi CO2 on-grid, skenario JETP'): jrows[int(float(yv))]=r
    sh.t('B19','Emisi on-grid, skenario JETP'); sh.t('C19','D_JETP (CIPP bab 5 hlm 59 sampai 60)')
    for y in JY:
        if y in jrows: sh.f(f'{jc[y]}19',f'D_JETP!C{jrows[y]}','n1l')
        elif y==2030: sh.f(f'{jc[y]}19',f'D_JETP!C{rowfind("D_JETP","Batas emisi sektor listrik",start=1,end=12)}','n1l')
        else: sh.f(f'{jc[y]}19','NA()','n1')
    sh.t('B20','Emisi pembangkitan RUPTL 2030 (RE Base)'); sh.t('C20','D_JETP Tabel 68.C')
    sh.t('B21','Proyeksi draf RUKN 2030'); sh.t('C21','D_JETP hlm 78')
    for y in JY:
        sh.f(f'{jc[y]}20',f'D_JETP!C{r_jr_global}' if y==2030 else 'NA()','n1l' if y==2030 else 'n1')
        sh.f(f'{jc[y]}21',f'D_JETP!C{rowfind("D_JETP","Proyeksi draf RUKN",start=1,end=12)}' if y==2030 else 'NA()','n1l' if y==2030 else 'n1')
    sh.t('B17','')   # remove placeholder
    for c in 'BC': sh.cells.pop(f'{c}17',None)
    sh.t('B23','Tabel 100.C. Angka target dan jalur lain yang dicatat (pembanding)','tbl')
    for c,t in zip('BCDEF',['Butir','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}24',t,'hdr')
    oth=[('Slide LTS-LCCR: FOLU 2030',-140,'MtCO2','P','D_LTS_Slide slide 5'),('Slide LTS-LCCR: FOLU 2040',-246,'MtCO2','P','D_LTS_Slide'),('Emisi 2030 skenario ENDC CM2',1632,'MtCO2e','P','D_SNDC Tabel 56.C (SNDC hlm 25)'),('LTS-LCCR: emisi sekitar 2050',540,'MtCO2e','E','Afriani dan Poletti 2026 mengutip LTS-LCCR (verifikasi ke dokumen primer)')]
    for i,(a,v,u,st,so) in enumerate(oth):
        r=25+i; sh.t(f'B{r}',a); sh.n(f'C{r}',v,'n1i'); sh.t(f'D{r}',u); sh.t(f'E{r}',st); sh.t(f'F{r}',so)
    sh.width('A','A',3); sh.width('B','B',46); sh.width('C','C',34); sh.width('D','H',13); sh.width('F','F',40)
    cats='B_Garis_NZE!$D$6:$H$6'
    cols={'Energi':'C00000','IPPU':'7F7F7F','Limbah':'BF8F00','Pertanian':'2E7D32','FOLU':'7030A0','Neto':'000000'}
    L=[dict(val_ref=f'B_Garis_NZE!$D${7+i}:$H${7+i}',name_ref=f'B_Garis_NZE!$B${7+i}',name=sct,color=cols[sct],pos='t',marker='circle',msize=7) for i,sct in enumerate(rows)]
    c1=ck.chart_xml('Gambar 100.1. Jalur LCCP_L menurut sektor pada tahun bersumber (MtCO2e)',[],L,'MtCO2e','Tahun (titik bersumber, jarak tidak proporsional)',cats,yfmt='#,##0')
    c2=ck.chart_xml('Gambar 100.2. Emisi on-grid listrik: jalur JETP dan titik 2030 (RUPTL, draf RUKN)',[],
        [dict(val_ref='B_Garis_NZE!$D$19:$H$19',name_ref='B_Garis_NZE!$B$19',name='Jalur JETP',color='2E7D32',pos='t'),
         dict(val_ref='B_Garis_NZE!$D$20:$H$20',name_ref='B_Garis_NZE!$B$20',name='RUPTL 2030',color='7030A0',marker='diamond',msize=11,pos='t'),
         dict(val_ref='B_Garis_NZE!$D$21:$H$21',name_ref='B_Garis_NZE!$B$21',name='Draf RUKN 2030',color='BF8F00',marker='diamond',msize=11,pos='r')],
        'MtCO2','Tahun',('B_Garis_NZE!$D$16:$H$16'),yfmt='#,##0')
    sh.charts=[(c1,(1,30,7800000,4000000)),(c2,(8,30,7800000,4000000))]
    return sh
r_jr_global=src.find_row('D_JETP','Emisi pembangkitan RUPTL 2025',start=36)

def B_Selisih(gp):
    sh=Sheet('B_Selisih_Penyebab'); refs=gp.refs
    sh.t('A1','Lembar 101. Selisih menurut penyebab: sektor, pendorong terukur, dan CM1 yang belum terkirim','title')
    sh.t('A2','Selisih = garis pembangunan dikurangi jalur LCCP_L. Bagian A menguraikan selisih menurut sektor dan tahun; B menunjukkan penyebab terukur sektor listrik (basis berbeda dari selisih energi SNDC, tidak dijumlahkan); C menambahkan bagian CM1 yang belum terkirim menurut capaian bersumber sehingga selisih nyata lebih besar dari selisih resmi.','title')
    sh.t('B5','Tabel 101.A. Selisih CPOS dikurangi LCCP_L menurut sektor (MtCO2e) dan pangsa terhadap total','tbl')
    sh.t('B6','Sektor','hdr')
    cols3=[2030,2035,2060]; cc=dict(zip(cols3,'CDE')); pc_=dict(zip(cols3,'FGH'))
    for y in cols3: sh.n(f'{cc[y]}6',y,'hdr'); sh.t(f'{pc_[y]}6',f'Pangsa {y}','hdr')
    secs=['Energi','FOLU','Limbah','IPPU','Pertanian','Neto']
    for i,sct in enumerate(secs):
        r=7+i; sh.t(f'B{r}',sct)
        for y in cols3:
            sh.f(f'{cc[y]}{r}',f'B_Garis_Pembangunan!{Y5C[y]}{refs[(sct,"gap")]}','n1l')
            sh.f(f'{pc_[y]}{r}',f'{cc[y]}{r}/{cc[y]}$12','pc')
    sh.t('B14','Tabel 101.B. Penyebab terukur pada listrik on-grid 2030 (MtCO2; basis berbeda dari selisih energi SNDC)','tbl')
    for c,t in zip('BCDE',['Butir','Nilai','Status','Sumber']): sh.t(f'{c}15',t,'hdr')
    pb=[('Emisi pembangkitan RUPTL 2030 (RE Base)','B_Pendorong!K28','P','D_JETP Tabel 68.C'),('Batas JETP CIPP on-grid 2030','B_Pendorong!K26','P','D_JETP'),('Selisih RUPTL dikurangi batas JETP','C16-C17','AC','Hitungan sederhana'),('Proyeksi draf RUKN 2030','B_Pendorong!K27','P','D_JETP'),('Selisih draf RUKN dikurangi batas JETP','C19-C17','AC','Sama dengan intervensi JETP 55 pada teks CIPP'),
        ('Dari PLTU baru RUPTL 2030 (kapasitas x faktor)','B_Pendorong!K20','AC','B_Pendorong L4'),('Dari PLTGU baru RUPTL 2030','B_Pendorong!K23','AC','B_Pendorong G2'),('PLTU captive 2030 (kapasitas, GW)','B_Pendorong!K24','E','Squire 2024; emisi belum terukur (WP-A)')]
    for i,(a,f_,st,so) in enumerate(pb):
        r=16+i; sh.t(f'B{r}',a); sh.f(f'C{r}',f_,'n1' if '-' in f_ and 'B_' not in f_ else 'n1l'); sh.t(f'D{r}',st); sh.t(f'E{r}',so)
    # C: CM1 not delivered
    sh.t('B26','Tabel 101.C. CM1 belum terkirim menurut capaian bersumber: selisih nyata 2030 (MtCO2e)','tbl')
    hh=['Aksi dalam garis dasar (CM1)','Potensi 2030 rendah','Potensi 2030 tinggi','Capaian saat ini terhadap target','Tahun data','Status capaian','Sisa harus dikirim, rendah','Sisa harus dikirim, tinggi']
    for c,t in zip('BCDEFGHI',hh): sh.t(f'{c}27',t,'hdr')
    rs=[('Efisiensi energi',25,71),('Co-firing biomassa',27,72),('Restorasi gambut (FOLU)',47,73),('Hutan tanaman PBPH-HT (FOLU)',52,74)]
    for i,(nm,cr,kr) in enumerate(rs):
        r=28+i; sh.t(f'B{r}',nm)
        sh.f(f'C{r}',f'C_Solusi_2030!E{cr}','n1l'); sh.f(f'D{r}',f'C_Solusi_2030!F{cr}','n1l'); sh.f(f'E{r}',f'C_Solusi_2030!D{kr}','pcl'); sh.f(f'F{r}',f'C_Solusi_2030!E{kr}','tl'); sh.f(f'G{r}',f'C_Solusi_2030!F{kr}','tl')
        sh.f(f'H{r}',f'C{r}*(1-E{r})','n1'); sh.f(f'I{r}',f'D{r}*(1-E{r})','n1')
    sh.t('B32','Jumlah sisa CM1 bersumber'); sh.f('H32','SUM(H28:H31)','n1'); sh.f('I32','SUM(I28:I31)','n1')
    sh.t('B33','Selisih resmi total 2030 (CPOS dikurangi LCCP_L)'); sh.f('H33','C12','n1'); sh.f('I33','C12','n1')
    sh.t('B34','Selisih nyata indikatif 2030 (resmi ditambah sisa CM1 turunan)'); sh.f('H34','H33+H32','n1'); sh.f('I34','I33+I32','n1')
    sh.t('B35','Tambahan terhadap selisih resmi (persen)'); sh.f('H35','H32/H33','pc'); sh.f('I35','I32/I33','pc')
    sh.t('B37','Catatan 101.C. Capaian adalah posisi saat ini terhadap target 2030 (bukan jalur 2030); sisa = potensi dikali (1 dikurangi capaian). Aksi CM1 lain (EBT, B40, FOLU lainnya) tidak punya capaian bersumber dan dianggap terkirim sampai data tersedia (WP-F). Capaian berstatus E dan AC tidak dijumlahkan dengan angka resmi.','note'); sh.merges.append('B37:I37')
    sh.f('A3','"Temuan utama: selisih resmi 2030 sebesar "&ROUND(C12,0)&" MtCO2e (energi "&ROUND(C7,0)&", FOLU "&ROUND(C8,0)&"); CM1 yang belum terkirim menurut capaian bersumber menambah "&ROUND(H32,0)&" sampai "&ROUND(I32,0)&" MtCO2e sehingga selisih nyata indikatif (resmi ditambah turunan dari capaian berstatus E dan AC, tidak dijumlahkan sebagai angka resmi) menjadi "&ROUND(H34,0)&" sampai "&ROUND(I34,0)&"."','title')
    sh.width('A','A',3); sh.width('B','B',52); sh.width('C','I',16); sh.width('E','E',22)
    # charts
    catp='B_Selisih_Penyebab!$C$6:$E$6'
    cols={'Energi':'C00000','FOLU':'7030A0','Limbah':'BF8F00','IPPU':'7F7F7F','Pertanian':'2E7D32','Neto':'000000'}
    L=[dict(val_ref=f'B_Selisih_Penyebab!$C${7+i}:$E${7+i}',name_ref=f'B_Selisih_Penyebab!$B${7+i}',name=s_,color=cols[s_],pos='t',marker='circle',msize=7) for i,s_ in enumerate(secs)]
    c1=ck.chart_xml('Gambar 101.1. Selisih CPOS dikurangi LCCP_L menurut sektor, 2030, 2035, 2060 (MtCO2e)',[],L,'MtCO2e','Tahun (titik bersumber, jarak tidak proporsional)',catp,yfmt='#,##0')
    c2=ck.chart_xml('Gambar 101.2. CM1: potensi 2030 dan sisa yang harus dikirim menurut capaian bersumber (MtCO2e)',
        [dict(base_ref='B_Selisih_Penyebab!$H$28:$H$31',band_ref='B_Selisih_Penyebab!$J$28:$J$31',name_ref='B_Selisih_Penyebab!$J$27',name='Rentang sisa (tinggi dikurangi rendah)',fill='F4B183')],
        [dict(val_ref='B_Selisih_Penyebab!$D$28:$D$31',name_ref='B_Selisih_Penyebab!$D$27',name='Potensi 2030 tinggi',color='1F4E79',pos='t'),
         dict(val_ref='B_Selisih_Penyebab!$I$28:$I$31',name_ref='B_Selisih_Penyebab!$I$27',name='Sisa harus dikirim, tinggi',color='C00000',pos='t'),
         dict(val_ref='B_Selisih_Penyebab!$H$28:$H$31',name_ref='B_Selisih_Penyebab!$H$27',name='Sisa harus dikirim, rendah',color='BF8F00',pos='b')],
        'MtCO2e per tahun','Aksi CM1 dengan capaian bersumber','B_Selisih_Penyebab!$B$28:$B$31',cat_numeric=False,yfmt='#,##0')
    for i in range(4): sh.f(f'J{28+i}',f'I{28+i}-H{28+i}','n1')
    sh.t('J27','Rentang sisa (tinggi dikurangi rendah)','hdr')
    sh.charts=[(c1,(1,39,7800000,4000000)),(c2,(8,39,7800000,4000000))]
    return sh
if __name__=='__main__' and 'B3' in sys.argv:
    gp=B_Garis_Pembangunan()
    sheets=[B_Pendorong(),gp,B_Garis_NZE(gp),B_Selisih(gp)]
    cache,errs=build('/tmp/claude-0/base_model.xlsx','/tmp/claude-0/stageB3.xlsx',sheets,[])
    print([e for e in errs if 'NA()' not in e[3]])
    for sn in ('B_Garis_NZE','B_Selisih_Penyebab'): print(cache.get((sn,'A3')))
