"""Lembar 102 P_Portofolio (tabel utama) dan grafik portofolio."""
import sys; sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from modelkit import *; import chartkit as ck; import src
EN=[('B1',30),('B2',31),('B3',32),('B4',33),('B5',34),('B6',35),('B7',36)]
FO=[(f'B{i}',54+i) for i in range(1,12)]
def P_Portofolio(sel):   # sel: name of B_Selisih sheet cells fixed: C7 energi gap, C8 FOLU gap, C12 total
    sh=Sheet('P_Portofolio','FF2A78D6')
    sh.t('A1','Lembar 102. Portofolio solusi: tabel utama (pengurangan, biaya, investasi, pelaksanaan, kumulatif, persen selisih 2030)','title')
    sh.t('A2','Dua bagian: (1) mengirim CM1 yang belum terkirim; (2) solusi baru di atas CM1 (lapis B). Angka menarik langsung dari C_Solusi_2030 dan B_Selisih_Penyebab. Urutan kumulatif mengikuti status sumber: resmi, turunan, lalu tidak resmi. Sumber pihak ketiga tidak dijumlahkan dengan CM1 atau CM2 resmi; kolom status menunjukkan asalnya.','title')
    H=['No','Sektor','Solusi','Lapis','Pendorong yang dituju','Pengurangan 2030 rendah (MtCO2e)','Pengurangan 2030 tinggi (MtCO2e)','Biaya rendah (USD per tCO2)','Biaya tinggi (USD per tCO2)','Biaya tahunan tengah (USD juta)','Investasi modal (USD miliar)','Persen selisih sektor, rendah','Persen selisih sektor, tinggi','Kumulatif rendah (MtCO2e)','Kumulatif tinggi (MtCO2e)','Kumulatif persen, rendah','Kumulatif persen, tinggi','Pelaksanaan saat ini (persen)','Pengurangan pada pelaksanaan saat ini, rendah','Status','Lembar solusi','Catatan']
    cols='BCDEFGHIJKLMNOPQRSTUVW'
    # ---- Part 1
    sh.t('B4','Bagian 1. Mengirim CM1 yang belum terkirim (sisa dari capaian bersumber)','tbl')
    for c,t in zip(cols,H): sh.t(f'{c}5',t,'hdr')
    P1=[('Energi','Efisiensi energi (enam program)',25,'Permintaan listrik dan bahan bakar','B_Selisih_Penyebab',28),('Energi','Co-firing biomassa',27,'Batubara PLTU','B_Selisih_Penyebab',29),('FOLU','Restorasi gambut',47,'Gambut terdrainase','B_Selisih_Penyebab',30),('FOLU','Hutan tanaman PBPH-HT',52,'Konversi dan hutan alam','B_Selisih_Penyebab',31)]
    for i,(sec,nm,cr,drv,_,br) in enumerate(P1):
        r=6+i; sh.n(f'B{r}',i+1,'n0'); sh.t(f'C{r}',sec); sh.t(f'D{r}',nm); sh.t(f'E{r}','A: sisa CM1'); sh.t(f'F{r}',drv)
        sh.f(f'G{r}',f'B_Selisih_Penyebab!H{br}','n1l'); sh.f(f'H{r}',f'B_Selisih_Penyebab!I{br}','n1l')
        sh.f(f'I{r}',f'C_Solusi_2030!G{cr}','n2l'); sh.f(f'J{r}',f'C_Solusi_2030!H{cr}','n2l')
        sh.f(f'K{r}',f'G{r}*C_Solusi_2030!I{cr}','n1')
        sh.t(f'L{r}','WP-J')
        sh.f(f'M{r}',f'G{r}/B_Selisih_Penyebab!$C${7 if sec=="Energi" else 8}','pc'); sh.f(f'N{r}',f'H{r}/B_Selisih_Penyebab!$C${7 if sec=="Energi" else 8}','pc')
        sh.f(f'O{r}',f'SUM($G$6:G{r})','n1'); sh.f(f'P{r}',f'SUM($H$6:H{r})','n1')
        sh.f(f'Q{r}',f'O{r}/B_Selisih_Penyebab!$C$12','pc'); sh.f(f'R{r}',f'P{r}/B_Selisih_Penyebab!$C$12','pc')
        sh.f(f'S{r}',f'B_Selisih_Penyebab!E{br}','pcl'); sh.f(f'T{r}',f'G{r}-G{r}+C_Solusi_2030!{"E" if False else "E"}{cr}*B_Selisih_Penyebab!E{br}','n1')
        sh.f(f'U{r}',f'B_Selisih_Penyebab!G{br}','tl'); sh.t(f'V{r}',['menunggu data (R2)','S_Cofiring','S_Restorasi_Gambut','S_Hutan_Tanaman'][i]); sh.t(f'W{r}','Capaian posisi saat ini terhadap target 2030; persen pada kolom M dan N dibandingkan dengan selisih sektor resmi.')
    sh.t('D10','Jumlah sisa CM1 bersumber'); sh.f('G10','SUM(G6:G9)','n1'); sh.f('H10','SUM(H6:H9)','n1'); sh.f('K10','SUM(K6:K9)','n1')
    # ---- Part 2
    sh.t('B12','Bagian 2. Solusi baru di atas CM1 (lapis B)','tbl')
    for c,t in zip(cols,H): sh.t(f'{c}13',t,'hdr')
    drivers={'B1':'PLTU batubara (pensiun)','B2':'Gas suar migas','B3':'Tidak dirinci (CM2)','B4':'PLTU batubara (pensiun lanjutan)','B5':'Emisi PLTU (penangkapan)','B6':'Batubara (diganti panas bumi)','B7':'Batubara (diganti surya)'}
    fdrv={'B1':'Gambut terdrainase','B2':'Degradasi gambut','B3':'Pembalakan konsesi','B4':'Deforestasi gambut','B5':'Gambut terdrainase','B6':'Degradasi hutan mineral','B7':'Deforestasi hutan mineral','B8':'Lahan kritis','B9':'Lahan kritis (rotasi)','B10':'Konversi hutan alam','B11':'Tidak dirinci (CM2)'}
    r=14; first_en=r
    erows={}
    for k,(bid,cr) in enumerate(EN):
        sh.n(f'B{r}',k+1,'n0'); sh.t(f'C{r}','Energi'); sh.f(f'D{r}',f'C_Solusi_2030!D{cr}','tl'); sh.f(f'E{r}',f'C_Solusi_2030!C{cr}','tl'); sh.t(f'F{r}',drivers[bid])
        sh.f(f'G{r}',f'C_Solusi_2030!E{cr}','n1l'); sh.f(f'H{r}',f'C_Solusi_2030!F{cr}','n1l'); sh.f(f'I{r}',f'C_Solusi_2030!G{cr}','n2l'); sh.f(f'J{r}',f'C_Solusi_2030!H{cr}','n2l'); sh.f(f'K{r}',f'C_Solusi_2030!J{cr}','n1l')
        erows[bid]=r; r+=1
    last_en=r-1
    for rr in range(first_en,last_en+1):
        sh.f(f'M{rr}',f'G{rr}/B_Selisih_Penyebab!$C$7','pc'); sh.f(f'N{rr}',f'H{rr}/B_Selisih_Penyebab!$C$7','pc')
        sh.f(f'O{rr}',f'SUM($G${first_en}:G{rr})','n1'); sh.f(f'P{rr}',f'SUM($H${first_en}:H{rr})','n1')
        sh.f(f'Q{rr}',f'O{rr}/B_Selisih_Penyebab!$C$7','pc'); sh.f(f'R{rr}',f'P{rr}/B_Selisih_Penyebab!$C$7','pc')
        cr=EN[rr-first_en][1]; sh.f(f'U{rr}',f'C_Solusi_2030!Q{cr}','tl'); sh.t(f'S{rr}','tidak ada data (WP-F)')
        sh.t(f'V{rr}',['S_Pensiun_Dini','menunggu data (R21)','bukan teknologi (resmi tidak dirinci)','S_Pensiun_Dini','S_CCS_TJB','S_Panas_Bumi','S_Surya (bersumber dari RUPTL menggantikan sisa selisih)'][rr-first_en])
        sh.f(f'W{rr}',f'C_Solusi_2030!R{cr}&": "&C_Solusi_2030!S{cr}','tl')
    # investment: geothermal (B6) and solar (B7)
    r6=erows['B6']; r7=erows['B7']
    sh.f(f'L{r6}',f'C_Portofolio_2030!F53/(D_Teknis_Opsi!F21*8.76)*C_Biaya_Teknologi!E11/1000','n1')
    sh.f(f'L{r7}',f'C_Solusi_2030!E39*C_Biaya_Teknologi!E13/1000','n1')
    sh.t(f'D{last_en+1}','Jumlah energi (lapis B)'); 
    for c in 'GHK': sh.f(f'{c}{last_en+1}',f'SUM({c}{first_en}:{c}{last_en})','n1')
    sh.f(f'L{last_en+1}',f'SUM(L{first_en}:L{last_en})','n1')
    sh.t(f'D{last_en+2}','Selisih energi 2030 (CPOS dikurangi LCCP_L)'); sh.f(f'G{last_en+2}','B_Selisih_Penyebab!C7','n1l'); sh.f(f'H{last_en+2}','B_Selisih_Penyebab!C7','n1l')
    sh.t(f'D{last_en+3}','Selisih energi yang belum tertutup'); sh.f(f'G{last_en+3}',f'G{last_en+2}-G{last_en+1}','n1'); sh.f(f'H{last_en+3}',f'H{last_en+2}-H{last_en+1}','n1')
    sh.t(f'D{last_en+4}','Persen selisih energi tertutup'); sh.f(f'G{last_en+4}',f'G{last_en+1}/G{last_en+2}','pc'); sh.f(f'H{last_en+4}',f'H{last_en+1}/H{last_en+2}','pc')
    r=last_en+6; first_fo=r
    for k,(bid,cr) in enumerate(FO):
        sh.n(f'B{r}',len(EN)+k+1,'n0'); sh.t(f'C{r}','FOLU'); sh.f(f'D{r}',f'C_Solusi_2030!D{cr}','tl'); sh.f(f'E{r}',f'C_Solusi_2030!C{cr}','tl'); sh.t(f'F{r}',fdrv[bid])
        sh.f(f'G{r}',f'C_Solusi_2030!E{cr}','n1l'); sh.f(f'H{r}',f'C_Solusi_2030!F{cr}','n1l'); sh.f(f'I{r}',f'C_Solusi_2030!G{cr}','n2l'); sh.f(f'J{r}',f'C_Solusi_2030!H{cr}','n2l'); sh.f(f'K{r}',f'C_Solusi_2030!J{cr}','n1l')
        sh.t(f'L{r}','WP-J'); sh.t(f'S{r}','tidak ada data (WP-F)')
        sh.f(f'U{r}',f'C_Solusi_2030!Q{cr}','tl'); sh.t(f'V{r}',['S_Tata_Air_Gambut','S_Degradasi_Gambut','S_PHL','S_Deforestasi_Gambut','S_Restorasi_Gambut','S_Degradasi_Mineral','S_Deforestasi_Mineral','S_Rehab_Tanpa_Rotasi','S_Rehab_Rotasi','S_Hutan_Tanaman','bukan teknologi (resmi tidak dirinci)'][k])
        sh.f(f'W{r}',f'C_Solusi_2030!R{cr}&": "&C_Solusi_2030!S{cr}','tl'); r+=1
    last_fo=r-1
    for rr in range(first_fo,last_fo+1):
        sh.f(f'M{rr}',f'G{rr}/B_Selisih_Penyebab!$C$8','pc'); sh.f(f'N{rr}',f'H{rr}/B_Selisih_Penyebab!$C$8','pc')
        sh.f(f'O{rr}',f'SUM($G${first_fo}:G{rr})','n1'); sh.f(f'P{rr}',f'SUM($H${first_fo}:H{rr})','n1')
        sh.f(f'Q{rr}',f'O{rr}/B_Selisih_Penyebab!$C$8','pc'); sh.f(f'R{rr}',f'P{rr}/B_Selisih_Penyebab!$C$8','pc')
    sh.t(f'D{last_fo+1}','Jumlah FOLU (lapis B)')
    for c in 'GHK': sh.f(f'{c}{last_fo+1}',f'SUM({c}{first_fo}:{c}{last_fo})','n1')
    sh.t(f'D{last_fo+2}','Selisih FOLU 2030 (CPOS dikurangi LCCP_L)'); sh.f(f'G{last_fo+2}','B_Selisih_Penyebab!C8','n1l'); sh.f(f'H{last_fo+2}','B_Selisih_Penyebab!C8','n1l')
    sh.t(f'D{last_fo+3}','Selisih FOLU yang belum tertutup'); sh.f(f'G{last_fo+3}',f'G{last_fo+2}-G{last_fo+1}','n1'); sh.f(f'H{last_fo+3}',f'H{last_fo+2}-H{last_fo+1}','n1')
    sh.t(f'D{last_fo+4}','Persen selisih FOLU tertutup'); sh.f(f'G{last_fo+4}',f'G{last_fo+1}/G{last_fo+2}','pc'); sh.f(f'H{last_fo+4}',f'H{last_fo+1}/H{last_fo+2}','pc')
    # total: tahap penutupan menurut status sumber
    rt=last_fo+6; sh.t(f'B{rt}','Bagian 3. Penutupan selisih 2030 menurut tahap status sumber (kumulatif)','tbl')
    for c,t in zip('DGHIJ',['Tahap','Kumulatif rendah (MtCO2e)','Kumulatif tinggi (MtCO2e)','Persen selisih, rendah','Persen selisih, tinggi']): sh.t(f'{c}{rt+1}',t,'hdr')
    e=erows; fE='B_Selisih_Penyebab!$C$7'; fF='B_Selisih_Penyebab!$C$8'; fT='B_Selisih_Penyebab!$C$12'
    stages=[('Energi: selisih 2030 (CPOS dikurangi LCCP_L)',fE,fE,None,'n1l'),
            ('Energi: opsi resmi (CM2: B1, B2, B3)',f'O{e["B3"]}',f'P{e["B3"]}',fE,'n1'),
            ('Energi: ditambah turunan dokumen (B4 pensiun lanjutan, B5 CCS)',f'O{e["B5"]}',f'P{e["B5"]}',fE,'n1'),
            ('Energi: ditambah pihak ketiga, panas bumi (B6, status E)',f'O{e["B6"]}',f'P{e["B6"]}',fE,'n1'),
            ('Energi: sisa selisih yang belum punya solusi bersumber (B7 menutupnya hanya sebagai sisa)',f'G{rt+2}-G{rt+5}',f'H{rt+2}-H{rt+5}',fE,'n1'),
            ('FOLU: selisih 2030 (CPOS dikurangi LCCP_L)',fF,fF,None,'n1l'),
            ('FOLU: turunan per aksi (B1 sampai B10, luas dikali faktor)',f'O{last_fo-1}',f'P{last_fo-1}',fF,'n1'),
            ('FOLU: tambahan CM2 resmi 195 Mt (termasuk bagian tidak dirinci B11)',f'O{last_fo}',f'P{last_fo}',fF,'n1')]
    for i,(a_,fl,fh,den,sty) in enumerate(stages):
        rr=rt+2+i; sh.t(f'D{rr}',a_); sh.f(f'G{rr}',fl,sty); sh.f(f'H{rr}',fh,sty)
        if den: sh.f(f'I{rr}',f'G{rr}/{den}','pc'); sh.f(f'J{rr}',f'H{rr}/{den}','pc')
    r2=rt+2+len(stages)+1
    sh.t(f'D{r2}','Biaya tahunan tengah lapis B energi tanpa B7 (USD miliar)'); sh.f(f'G{r2}',f'(SUM(K{first_en}:K{last_en})-K{e["B7"]})/1000','n2'); sh.f(f'H{r2}',f'G{r2}','n2')
    sh.t(f'D{r2+1}','Biaya tahunan tengah B7 yang berupa sisa selisih (USD miliar)'); sh.f(f'G{r2+1}',f'K{e["B7"]}/1000','n2'); sh.f(f'H{r2+1}',f'G{r2+1}','n2')
    sh.t(f'D{r2+2}','Biaya tahunan tengah lapis B FOLU (USD miliar)'); sh.f(f'G{r2+2}',f'K{last_fo+1}/1000','n2'); sh.f(f'H{r2+2}',f'G{r2+2}','n2')
    sh.t(f'D{r2+3}','Sisa CM1 yang harus dikirim, bagian 1 (MtCO2e)'); sh.f(f'G{r2+3}','G10','n1'); sh.f(f'H{r2+3}','H10','n1')
    sh.t(f'D{r2+4}','Selisih nyata indikatif: selisih resmi total ditambah sisa CM1 (MtCO2e)'); sh.f(f'G{r2+4}',f'{fT}+G{r2+3}','n1'); sh.f(f'H{r2+4}',f'{fT}+H{r2+3}','n1')
    sh.t(f'D{r2+6}','Catatan 102. Tahap kumulatif mengikuti status sumber. B7 (surya sebesar sisa selisih) menutup selisih hanya sebagai sisa dan bukan angka bersumber; pengganti bersumber dari RUPTL ada di S_Surya. Investasi dihitung hanya bila kapasitas dan biaya modal bersumber ada (panas bumi, surya); lainnya menunggu WP-J. Angka E dan AC tidak dijumlahkan sebagai angka resmi.','note'); sh.merges.append(f'D{r2+6}:W{r2+6}')
    sh.f('A3',f'"Temuan utama: opsi resmi menutup "&ROUND(I{rt+3}*100,0)&" persen selisih energi 2030, dengan turunan "&ROUND(I{rt+4}*100,0)&" persen, dengan pihak ketiga "&ROUND(I{rt+5}*100,0)&" persen; sisa "&ROUND(G{rt+6},0)&" MtCO2e belum punya solusi bersumber. FOLU: turunan per aksi "&ROUND(I{rt+8}*100,0)&" sampai "&ROUND(J{rt+8}*100,0)&" persen, CM2 resmi "&ROUND(I{rt+9}*100,0)&" persen. Sisa CM1 yang harus dikirim menambah "&ROUND(G10,0)&" sampai "&ROUND(H10,0)&" MtCO2e."','title')
    sh.width('A','A',3); sh.width('B','B',5); sh.width('C','C',9); sh.width('D','D',44); sh.width('E','E',18); sh.width('F','F',26); sh.width('G','R',13); sh.width('L','L',16); sh.width('S','S',17); sh.width('T','T',13); sh.width('U','U',34); sh.width('V','V',34); sh.width('W','W',55)
    sh.pos=dict(first_en=first_en,last_en=last_en,first_fo=first_fo,last_fo=last_fo,rt=rt,erows=erows)
    return sh
def _main():
    import importlib.util
    spec=importlib.util.spec_from_file_location('bmod','/home/user/NetZeroEmission/scripts/09_build_model_B.py'); bm=importlib.util.module_from_spec(spec); spec.loader.exec_module(bm)
    gp=bm.B_Garis_Pembangunan(); pend=bm.B_Pendorong(); nze=bm.B_Garis_NZE(gp); sel=bm.B_Selisih(gp); pf=P_Portofolio(sel); gf=G_Portofolio(pf)
    cache,errs=build('/tmp/claude-0/base_model.xlsx','/tmp/claude-0/stageP.xlsx',[pend,gp,nze,sel,pf,gf],[])
    print([e for e in errs if 'NA()' not in e[3] and 'IFERROR' not in e[3]])
    print(cache.get(('P_Portofolio','A3'))); print(cache.get(('G_Portofolio','A3')))

def G_Portofolio(pf):
    pos=pf.pos; e=pos['erows']; rt=pos['rt']; fo0=pos['first_fo']
    sh=Sheet('G_Portofolio','FF2A78D6')
    sh.t('A1','Lembar 103. Grafik portofolio: penutupan selisih 2030 menurut tahap, kurva biaya, dan biaya tahunan kumulatif','title')
    sh.t('A2','Semua deret menarik dari P_Portofolio (tanpa angka baru). Grafik garis dengan area berarsir untuk selisih yang belum tertutup; label angka pada setiap titik. Tahap mengikuti status sumber: resmi, turunan, lalu pihak ketiga.','title')
    sh.t('B5','Tabel 103.A. Penutupan selisih 2030 menurut tahap (MtCO2e)','tbl')
    H=['Tahap','Kumulatif rendah','Kumulatif tinggi','Selisih 2030','Sisa selisih (selisih dikurangi kumulatif tinggi)']
    for c,t in zip('BCDEF',H): sh.t(f'{c}6',t,'hdr')
    P='P_Portofolio!'
    def stage(r,label,rowref,gapref):
        sh.t(f'B{r}',label); sh.f(f'C{r}',f'{P}G{rowref}','n1l'); sh.f(f'D{r}',f'{P}H{rowref}','n1l'); sh.f(f'E{r}',gapref,'n1l'); sh.f(f'F{r}',f'E{r}-D{r}','n1')
    # energy stages rows: rt+3 (resmi), rt+4 (turunan), rt+5 (pihak ketiga); no B7
    stage(7,'Energi: resmi',rt+3,f'{P}G{rt+2}'); stage(8,'Energi: + turunan',rt+4,f'{P}G{rt+2}'); stage(9,'Energi: + pihak ketiga',rt+5,f'{P}G{rt+2}')
    sh.t('B11','FOLU: turunan per aksi'); sh.f('C11',f'{P}G{rt+8}','n1l'); sh.f('D11',f'{P}H{rt+8}','n1l'); sh.f('E11',f'{P}G{rt+7}','n1l'); sh.f('F11','E11-D11','n1')
    sh.t('B12','FOLU: CM2 resmi 195'); sh.f('C12',f'{P}G{rt+9}','n1l'); sh.f('D12',f'{P}H{rt+9}','n1l'); sh.f('E12',f'{P}G{rt+7}','n1l'); sh.f('F12','E12-D12','n1')
    # total stages
    sh.t('B14','Total: energi resmi + FOLU turunan'); sh.f('C14','C7+C11','n1'); sh.f('D14','D7+D11','n1'); sh.f('E14','E7+E11','n1'); sh.f('F14','E14-D14','n1')
    sh.t('B15','Total: + energi turunan + FOLU CM2 resmi'); sh.f('C15','C8+C12','n1'); sh.f('D15','D8+D12','n1'); sh.f('E15','E8+E12','n1'); sh.f('F15','E15-D15','n1')
    sh.t('B16','Total: + energi pihak ketiga'); sh.f('C16','C9+C12','n1'); sh.f('D16','D9+D12','n1'); sh.f('E16','E9+E12','n1'); sh.f('F16','E16-D16','n1')
    # stage labels for categories
    # --- cost-ordered table
    sh.t('B20','Tabel 103.B. Solusi lapis B menurut urutan biaya per tCO2 (kurva biaya)','tbl')
    cand=[('Pensiun dini resmi',e['B1']),('Pensiun lanjutan 6 PLTU',e['B4']),('CCS TJB',e['B5']),('Panas bumi',e['B6'])]
    fo_names=['Tata air gambut','Degradasi gambut','PHL (RIL-C)','Deforestasi gambut','Restorasi gambut','Degradasi mineral','Deforestasi mineral','Rehabilitasi tanpa rotasi','Rehabilitasi rotasi','Hutan tanaman PBPH-HT']
    for k,nm in enumerate(fo_names): cand.append((nm,fo0+1+k-1+0)) if False else None
    # FOLU rows in P_Portofolio: first_fo is B1 (tata air) ... B11
    for k,nm in enumerate(fo_names): cand.append((nm,fo0+k))
    for c,t in zip('BCDEFGH',['Solusi (nama pendek)','Baris P_Portofolio','Pengurangan rendah','Biaya tengah (USD per tCO2)','Layak (pengurangan lebih dari nol dan biaya ada)','Kunci urut','Peringkat']): sh.t(f'{c}21',t,'hdr')
    n=len(cand)
    for i,(nm,pr) in enumerate(cand):
        r=22+i; sh.t(f'B{r}',nm); sh.n(f'C{r}',pr,'n0i')
        sh.f(f'D{r}',f'{P}G{pr}','n1l'); sh.f(f'E{r}',f'AVERAGE({P}I{pr}:J{pr})','n2')
        sh.f(f'F{r}',f'IF(AND(ISNUMBER(E{r}),D{r}>0),1,0)','n0'); sh.f(f'G{r}',f'IF(F{r}=1,E{r}+ROW()/1000000,"")','n2')
        sh.f(f'H{r}',f'IF(F{r}=1,COUNTIF($G$22:$G${21+n},"<"&G{r})+1,"")','n0')
    top=22+n+1
    sh.t(f'B{top}','Tabel 103.C. Urutan biaya (dari termurah), kumulatif pengurangan dan biaya tahunan','tbl')
    for c,t in zip('BCDEFG',['Urutan','Solusi','Pengurangan rendah (MtCO2e)','Biaya tengah (USD per tCO2)','Kumulatif pengurangan (MtCO2e)','Kumulatif biaya tahunan (USD miliar)']): sh.t(f'{c}{top+1}',t,'hdr')
    NS=12
    for k in range(1,NS+1):
        r=top+1+k; sh.n(f'B{r}',k,'n0')
        m=f'MATCH(B{r},$H$22:$H${21+n},0)'
        sh.f(f'C{r}',f'IFERROR(INDEX($B$22:$B${21+n},{m}),NA())','tl'); sh.f(f'D{r}',f'IFERROR(INDEX($D$22:$D${21+n},{m}),NA())','n1')
        sh.f(f'E{r}',f'IFERROR(INDEX($E$22:$E${21+n},{m}),NA())','n2')
        if k==1: sh.f(f'F{r}',f'IFERROR(D{r},NA())','n1'); sh.f(f'G{r}',f'IFERROR(D{r}*E{r}/1000,NA())','n2')
        else: sh.f(f'F{r}',f'IFERROR(F{r-1}+D{r},NA())','n1'); sh.f(f'G{r}',f'IFERROR(G{r-1}+D{r}*E{r}/1000,NA())','n2')
    s0=top+2; s1=top+1+NS
    sh.width('A','A',3); sh.width('B','B',44); sh.width('C','C',26); sh.width('D','H',18)
    CS='G_Portofolio!'
    def stage_chart(title,r0,r1,cats):
        return ck.chart_xml(title,
          [dict(base_ref=f'{CS}$D${r0}:$D${r1}',band_ref=f'{CS}$F${r0}:$F${r1}',name_ref=f'{CS}$F$6',name='Sisa selisih belum tertutup',fill='F4B183')],
          [dict(val_ref=f'{CS}$E${r0}:$E${r1}',name_ref=f'{CS}$E$6',name='Selisih 2030',color='C00000',pos='t'),
           dict(val_ref=f'{CS}$D${r0}:$D${r1}',name_ref=f'{CS}$D$6',name='Kumulatif tinggi',color='1F4E79',pos='t'),
           dict(val_ref=f'{CS}$C${r0}:$C${r1}',name_ref=f'{CS}$C$6',name='Kumulatif rendah',color='2E7D32',pos='b')],
          'MtCO2e per tahun','Tahap (status sumber)',cats,cat_numeric=False,yfmt='#,##0')
    c1=stage_chart('Gambar 103.1. Energi 2030: penutupan selisih menurut tahap',7,9,f'{CS}$B$7:$B$9')
    c2=stage_chart('Gambar 103.2. FOLU 2030: penutupan selisih menurut tahap',11,12,f'{CS}$B$11:$B$12')
    c3=stage_chart('Gambar 103.3. Total energi dan FOLU 2030: penutupan menurut tahap',14,16,f'{CS}$B$14:$B$16')
    c4=ck.chart_xml('Gambar 103.4. Kurva biaya: biaya tengah per tCO2 menurut urutan termurah',[],
        [dict(val_ref=f'{CS}$E${s0}:$E${s1}',name_ref=f'{CS}$E${top+1}',name='Biaya tengah (USD per tCO2)',color='7030A0',pos='t',fmt='#,##0.0')],'USD per tCO2','Solusi (urutan termurah)',f'{CS}$C${s0}:$C${s1}',cat_numeric=False,yfmt='#,##0')
    c5=ck.chart_xml('Gambar 103.5. Pengurangan kumulatif menurut urutan biaya (MtCO2e per tahun)',[],
        [dict(val_ref=f'{CS}$F${s0}:$F${s1}',name_ref=f'{CS}$F${top+1}',name='Kumulatif pengurangan',color='1F4E79',pos='t')],'MtCO2e per tahun','Solusi (urutan termurah)',f'{CS}$C${s0}:$C${s1}',cat_numeric=False,yfmt='#,##0')
    c6=ck.chart_xml('Gambar 103.6. Biaya tahunan kumulatif menurut urutan biaya (USD miliar per tahun)',[],
        [dict(val_ref=f'{CS}$G${s0}:$G${s1}',name_ref=f'{CS}$G${top+1}',name='Kumulatif biaya tahunan',color='C00000',pos='t',fmt='#,##0.00')],'USD miliar per tahun','Solusi (urutan termurah)',f'{CS}$C${s0}:$C${s1}',cat_numeric=False,yfmt='#,##0.0')
    ytop=s1+3
    W,Hh=7400000,3900000
    sh.charts=[(c1,(1,ytop,W,Hh)),(c2,(8,ytop,W,Hh)),(c3,(1,ytop+22,W,Hh)),(c4,(8,ytop+22,W,Hh)),(c5,(1,ytop+44,W,Hh)),(c6,(8,ytop+44,W,Hh))]
    sh.f('A3','"Temuan utama: pada 2030 energi tertutup "&ROUND(C7,0)&" sampai "&ROUND(D9,0)&" MtCO2e dari "&ROUND(E7,0)&" (sisa "&ROUND(F9,0)&"); FOLU "&ROUND(C11,0)&" sampai "&ROUND(D12,0)&" dari "&ROUND(E11,0)&"; total "&ROUND(D16,0)&" dari "&ROUND(E16,0)&" MtCO2e, dengan biaya tahunan kumulatif USD "&ROUND(INDEX(G'+str(s0)+':G'+str(s1)+',COUNT(G'+str(s0)+':G'+str(s1)+')),1)&" miliar pada urutan biaya."','title')
    return sh
if __name__=='__main__': _main()
