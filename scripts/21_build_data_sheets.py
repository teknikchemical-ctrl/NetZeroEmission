"""Lapisan data: D_Sumber (induk sumber), D_Data_Struktur (satu angka per baris dengan jejak sumber), G_Data_Sumber (grafik semua deret bersumber).
Semua angka dari berkas CSV/PDF di repo atau dari tabel PDF yang diperiksa; tanpa proyeksi. Dipanggil oleh 13_assemble_model.py."""
import csv,collections,re,sys
sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from modelkit import *
import chartkit as ck
R='/home/user/NetZeroEmission'
INV=list(csv.DictReader(open(f'{R}/notes/INVENTARIS_SUMBER.csv',encoding='utf-8')))
SID={r['nama']:r['id'] for r in INV}
def sid(prefix): return next(r['id'] for r in INV if r['nama'].startswith(prefix))
COLS=['2E75B6','C00000','2E7D32','7030A0','BF8F00','00838F','7F7F7F','E36C09']
# ---------------- D_Sumber ----------------
def D_Sumber():
    sh=Sheet('D_Sumber','FF7F7F7F'); n=len(INV)
    sh.t('A1','Lembar 129. Induk sumber: setiap berkas (PDF, CSV) dan sumber tanpa berkas, dengan jenis, kedalaman baca, jumlah butir tercatat, dan jalur catatan serta data','title')
    sh.t('A2','Satu baris per sumber. Kedalaman baca: A angka diverifikasi pada sumber; B abstrak, kesimpulan, dan kalimat berangka dibaca (bagian lain belum); C diarsip tanpa pembacaan. Catatan per sumber ada di notes/sumber, data register per sumber di data/per_sumber. Berkas duplikat isi ditandai.','note')
    r0=11; r1=r0+n-1
    sh.f('A3',f'"Temuan utama: "&COUNTA(B{r0}:B{r1})&" sumber; kedalaman A "&COUNTIF(G{r0}:G{r1},"A")&", B "&COUNTIF(G{r0}:G{r1},"B")&", C "&COUNTIF(G{r0}:G{r1},"C")&"; "&COUNTIF(I{r0}:I{r1},"S*")&" berkas duplikat isi."','txt')
    sh.t('B5','Tabel 129.A. Ringkasan menurut kedalaman baca','tbl')
    for c,t in zip('BCD',['Kedalaman','Jumlah sumber','Arti']): sh.t(f'{c}6',t,'hdr')
    for i,(k,a) in enumerate([('A','Angka diverifikasi pada PDF atau CSV'),('B','Abstrak, kesimpulan, dan kalimat berangka dibaca'),('C','Diarsip tanpa pembacaan atau tanpa berkas')]):
        r=7+i; sh.t(f'B{r}',k); sh.f(f'C{r}',f'COUNTIF($G${r0}:$G${r1},B{r})','n0'); sh.t(f'D{r}',a)
    sh.t('B9','Tabel 129.B. Daftar sumber','tbl')
    for c,t in zip('BCDEFGHIJKL',['ID','Nama berkas atau sumber','Jenis','WP','Halaman','Kedalaman','Butir register','Duplikat isi dari','Catatan','Data','Konteks']): sh.t(f'{c}10',t,'hdr')
    for i,rw in enumerate(INV):
        r=r0+i
        sh.t(f'B{r}',rw['id'],'txtt'); sh.t(f'C{r}',rw['nama'],'txtt'); sh.t(f'D{r}',rw['jenis'],'txtt'); sh.t(f'E{r}',rw['wp'],'txtt'); sh.t(f'F{r}',rw['halaman'],'txtt'); sh.t(f'G{r}',rw['kedalaman'],'txtt')
        sh.n(f'H{r}',int(rw['butir_register']),'n0i'); sh.t(f'I{r}',rw['duplikat_dari'],'txtt'); sh.t(f'J{r}',rw['catatan'],'txtt'); sh.t(f'K{r}',rw['data'],'txtt'); sh.t(f'L{r}',rw['konteks'],'txtt')
    sh.width('A','A',3); sh.width('B','B',9); sh.width('C','C',48); sh.width('D','D',22); sh.width('E','G',11); sh.width('H','I',13); sh.width('J','K',30); sh.width('L','L',90)
    return sh
# ---------------- data terstruktur ----------------
class Long:
    def __init__(s): s.rows=[]; s.key={}
    def add(s,key,sumber,dok,lok,ind,val,sat,thn,skn,kat,st,cat=''):
        s.rows.append((sumber,dok,lok,ind,val,sat,thn,skn,kat,st,cat)); 
        if key is not None: s.key[key]=len(s.rows)-1
def build_long():
    L=Long(); csvp=lambda p: list(csv.DictReader(open(f'{R}/{p}',encoding='utf-8-sig')))
    # Squire
    S13=sid('2024_Squire-dkk_Emisi'); r=list(csv.reader(open(f'{R}/sources/2024_Squire-dkk_Emisi-Skenario-Co-firing.csv',encoding='utf-8-sig')))
    yrs=[int(x) for x in r[0][1:12]]
    for row in r[1:6]:
        for y,v in zip(yrs,row[1:12]): L.add(('sq',row[0],y),S13,'Squire dkk. 2024 (CSV penulis)','Gambar 2','Emisi CO2 PLTU menurut skenario co-firing',float(v),'MtCO2 per tahun',y,row[0],'PLTU nasional','E','Emisi pembangkit model; tanpa emisi hulu biomassa')
    S12=sid('2024_Squire-dkk_Biomassa'); bp=list(csv.reader(open(f'{R}/sources/2024_Squire-dkk_Biomassa-Provinsi.csv',encoding='utf-8-sig')))
    hd=[h.strip() for h in bp[0]]
    for row in bp[1:]:
        if row[0].strip(): L.add(None,S12,'Squire dkk. 2024 (CSV penulis)','Biomassa per provinsi','Pasokan limbah biomassa, jumlah semua jenis',float(row[-1])/1e9,'miliar MJ per tahun','',row[0].strip(),'Provinsi','E','Jumlah 34 provinsi 504,4')
    # OWID
    SO=sid('2026_OWID_Energi'); ow=csvp('sources/2026_OWID_Energi-Indonesia_2015-2024.csv')
    unit=lambda c: 'gCO2e per kWh' if 'intensity' in c else 'TWh'
    nm={'coal_electricity':'Listrik dari batubara','gas_electricity':'Listrik dari gas','oil_electricity':'Listrik dari minyak','solar_electricity':'Listrik surya','wind_electricity':'Listrik angin','hydro_electricity':'Listrik hidro','biofuel_electricity':'Listrik bioenergi','other_renewable_exc_biofuel_electricity':'Listrik terbarukan lain (di luar bioenergi)','electricity_generation':'Pembangkitan listrik total','carbon_intensity_elec':'Intensitas karbon listrik (siklus hidup)','gas_production':'Produksi gas','oil_production':'Produksi minyak','gas_consumption':'Konsumsi energi primer gas','oil_consumption':'Konsumsi energi primer minyak'}
    for rw in ow:
        for c in nm:
            if rw[c]!='': L.add(('ow',c,int(rw['year'])),SO,'Our World in Data (Energy Institute, Ember)','CSV cuplikan Indonesia',nm[c],float(rw[c]),unit(c),int(rw['year']),'Realisasi','Nasional','R','Rata-rata nasional, bukan faktor marginal')
    # ETP
    SE=sid('2023_ETP-Kompensasi')
    for rw in csvp('sources/2023_ETP-Kompensasi-Pensiun-PLTU_Tabel-14-1.csv'):
        y=int(rw['scenario_retirement_year']); nmx=rw['asset_group']+' ('+rw['owner']+')'
        L.add(('etp',nmx,'pay'),SE,'ETP/UNOPS 2023','Tabel 14.1 hlm. 183 sampai 184','Kompensasi pensiun dini pada tahun pensiun',float(rw['payment_usd_million_at_retirement_year']),'USD juta',y,'Skenario studi ETP',nmx,'E','Sisa umur '+rw['remaining_life_years_at_retirement']+' tahun; valuasi aset, bukan harga terminasi')
        L.add(('etp',nmx,'pv'),SE,'ETP/UNOPS 2023','Tabel 14.1 hlm. 183 sampai 184','Kompensasi pensiun dini, nilai kini 2022',float(rw['payment_usd_million_pv_2022']),'USD juta',y,'Skenario studi ETP',nmx,'E','')
    # Pipeline EBT
    SP=sid('PIPELINE_EBT'); agg=collections.defaultdict(float)
    for rw in csvp('data/PIPELINE_EBT_RUPTL.csv'):
        mw=float(rw['kapasitas_mw'] or 0)
        for scn,k in (('RE Base','cod_re_base'),('ARED','cod_ared')):
            if rw[k]: agg[(scn,rw['jenis'],int(rw[k]))]+=mw
    for (scn,j,y),v in sorted(agg.items()):
        L.add(('ebt',scn,j,y),SP,'RUPTL 2025 sampai 2034 via D_Gen_RUPTL','data/PIPELINE_EBT_RUPTL.csv','Tambahan kapasitas menurut tahun COD rencana',v,'MW',y,scn,j,'P','Jumlah proyek per jenis dan tahun COD; BESS dalam MW (MWh terpisah); status proyek dan tambahan terhadap CPOS belum diverifikasi')
    # Energy Institute (salinan olahan)
    SEI=sid('2026_EI_Indonesia')
    for rw in csvp('sources/2026_EI_Indonesia_biofuel-dan-gas-suar_2015-2025.csv'):
        L.add(('ei',rw['lembar_asal'],int(rw['tahun'])),SEI,'Energy Institute Statistical Review 2026 (salinan olahan pihak ketiga)','Lembar '+rw['lembar_asal'],rw['indikator'],float(rw['nilai']),rw['satuan'],int(rw['tahun']),'Realisasi','Nasional','R','Salinan pihak ketiga pada commit tetap; gas suar berbasis VIIRS Nightfire dan GCV 40 MJ per m3')
    # TJB 5 dan 6 operasi aktual
    SER=sid('2025_ERIA')
    for ind,u,vals in (('Pembangkitan listrik','GWh',(6748,7546)),('Faktor kapasitas tabel','persen',(77,86)),('Emisi CO2','MtCO2',(5.8,6.4))):
        for un,v in zip((5,6),vals): L.add(('tjb',ind,un),SER,'ERIA/Sumitomo 2025','Tabel 4.1 hlm. 27 (dibaca dari gambar)','TJB unit '+str(un)+': '+ind+' (1 Okt 2022 sampai 30 Sep 2023)',float(v),u,2023,'Operasi aktual','TJB unit '+str(un),'R','Unit 5 berhenti Mei sampai Juni 2023; kapasitas neto 1.000 MW per unit')
    L.add(('tjb','Emisi CO2','total'),SER,'ERIA/Sumitomo 2025','Tabel 4.1 hlm. 27 (dibaca dari gambar)','TJB unit 5 dan 6: emisi CO2 total',12.2,'MtCO2',2023,'Operasi aktual','TJB 5 dan 6','R','Dibanding 9,404 (estimasi GEM, Prabowo dan Dalimi) dan 13 (desain ERIA); K167')
    # Riau: tutupan hutan alam
    SRI=sid('KajianGap')
    for lans,vals in (('Semenanjung Kampar',(690611.81,553027.05,371563.78,345368.36)),('Kerumutan',(1162334.63,607860.94,369749.82,310851.79))):
        for y,v in zip((1982,2002,2012,2022),vals): L.add(('riau',lans,y),SRI,'Nursamsu dkk. 2024 (Paradigma)','Tabel 21 dan 24 hlm. 36 dan 40','Tutupan hutan alam '+lans,v,'ha',y,'Observasi spasial','Lanskap Riau','R','SIGAP KLHK; deforestasi melambat 2012 sampai 2022')
    # PLN
    SPL=sid('2025_PLN'); D='PLN Laporan Pengungkapan Iklim 2024'
    for k,(lok,ind,vals,thn,kat) in enumerate([
     ('Tabel 10 hlm. 61','Emisi Lingkup 1 batubara',{2022:119.06,2023:117.22,2024:123.71},'MtCO2e','pembangkitan'),
     ('Tabel 10 hlm. 61','Emisi Lingkup 1 gas',{2022:21.53,2023:25.11,2024:23.91},'MtCO2e','pembangkitan'),
     ('Tabel 10 hlm. 61','Emisi Lingkup 1 minyak',{2022:6.06,2023:6.43,2024:7.74},'MtCO2e','pembangkitan'),
     ('Tabel 10 hlm. 61','Emisi Lingkup 1 total',{2022:148.33,2023:150.68,2024:156.31},'MtCO2e','semua'),
     ('Tabel 10 hlm. 61','Emisi Lingkup 2 total',{2022:8.16,2023:8.79,2024:13.59},'MtCO2e','semua'),
     ('Tabel 10 hlm. 61','Emisi Lingkup 3 total',{2022:84.57,2023:98.57,2024:106.66},'MtCO2e','semua'),
     ('Tabel 10 hlm. 61','Emisi Lingkup 1, 2, 3 pembangkitan',{2022:233.42,2023:249.12,2024:266.11},'MtCO2e','pembangkitan'),
     ('Tabel 10 hlm. 61','Emisi Lingkup 1, 2, 3 semua kegiatan',{2022:241.05,2023:258.03,2024:276.56},'MtCO2e','semua'),
     ('Tabel 11 hlm. 62','Intensitas emisi pembangkitan Lingkup 1, 2, 3',{2022:0.76,2023:0.77,2024:0.77},'tCO2e per MWh','pembangkitan'),
     ('Tabel 14 hlm. 63','Emisi PLTU milik PLN',{2022:119.4,2023:118.6,2024:125.1},'MtCO2e','PLTU'),
     ('Tabel 14 hlm. 63','Emisi PLTGU',{2022:15.5,2023:18.0,2024:18.1},'MtCO2e','PLTGU'),
     ('Tabel 14 hlm. 63','Emisi PLTMG',{2022:4.8,2023:4.9,2024:5.2},'MtCO2e','PLTMG'),
     ('Tabel 14 hlm. 63','Emisi PLTD',{2022:3.3,2023:3.5,2024:3.8},'MtCO2e','PLTD'),
     ('Tabel 14 hlm. 63','Emisi PLTG',{2022:3.7,2023:3.8,2024:3.3},'MtCO2e','PLTG'),
     ('Tabel 17 hlm. 66','Realisasi pengurangan: EBT tambahan',{2022:2.0,2023:3.4,2024:4.2},'MtCO2e','EBT tambahan'),
     ('Tabel 17 hlm. 66','Realisasi pengurangan: teknologi batubara bersih',{2022:2.8,2023:4.2,2024:4.6},'MtCO2e','Batubara bersih'),
     ('Tabel 17 hlm. 66','Realisasi pengurangan: konversi gas ke siklus kombinasi',{2022:0.6,2023:1.1,2024:2.1},'MtCO2e','Gas ke siklus kombinasi'),
     ('Tabel 17 hlm. 66','Realisasi pengurangan: co-firing biomassa',{2022:0.6,2023:1.1,2024:1.8},'MtCO2e','Co-firing biomassa'),
     ('Tabel 17 hlm. 66','Realisasi pengurangan: total',{2022:6.0,2023:9.7,2024:12.7},'MtCO2e','Total'),
     ('Tabel 17 hlm. 66','Target pengurangan: total',{2023:6.9,2024:10.8},'MtCO2e','Total target')]):
        for y,v in vals.items(): L.add(('pln',ind,y),SPL,D,lok,ind,v,thn,y,'Realisasi',kat,'R','Laporan perusahaan; Lingkup 3 memuat listrik IPP')
    for y,v in zip(range(2020,2061,5),[247,310,326,325,321,272,224,154,0]): L.add(('ared',y),SPL,D,'Gambar 7 hlm. 23 (dibaca dari gambar)','Jalur ARED: emisi Lingkup 1 sampai 3 pembangkitan',float(v),'MtCO2e per tahun',y,'ARED PLN','pembangkitan','R','Dibaca dari gambar; pemeriksaan kedua diminta; tanpa pensiun dini PLTU')
    for y,v in ((2020,0.89),(2030,0.74),(2040,0.50),(2050,0.21),(2060,0.0)): L.add(('aredi',y),SPL,D,'Gambar 7 hlm. 23 (dibaca dari gambar)','Jalur ARED: intensitas emisi',v,'tCO2 per MWh',y,'ARED PLN','pembangkitan','R','Dibaca dari gambar')
    # Studi lain: titik pembanding
    def pt(key,sid_,dok,lok,ind,v,sat,y,skn,kat,st,cat=''): L.add(key,sid_,dok,lok,ind,v,sat,y,skn,kat,st,cat)
    pt(('ru',2030,'RE Base'),'X002','RUPTL 2025 sampai 2034','Tabel 5.175','Emisi pembangkitan listrik',354.0,'MtCO2',2030,'RE Base','PLN dan IPP on-grid','P','Tercatat di D_RUPTL')
    pt(('ru',2030,'ARED'),'X002','RUPTL 2025 sampai 2034','Tabel 5.176','Emisi pembangkitan listrik',348.0,'MtCO2',2030,'ARED','PLN dan IPP on-grid','P','Tercatat di D_RUPTL')
    pt(('ru',2034,'RE Base'),'X002','RUPTL 2025 sampai 2034','Tabel 5.175','Emisi pembangkitan listrik',374.0,'MtCO2',2034,'RE Base','PLN dan IPP on-grid','P','')
    pt(('ru',2034,'ARED'),'X002','RUPTL 2025 sampai 2034','Tabel 5.176','Emisi pembangkitan listrik',362.0,'MtCO2',2034,'ARED','PLN dan IPP on-grid','P','')
    pt(('jetp',2030),'X002','JETP CIPP 2023','Bab 1 hlm. 3','Batas emisi pembangkitan on-grid',250.0,'MtCO2',2030,'CIPP on-grid','on-grid','P','D_JETP!C6')
    pt(('fad',2023),sid('2026_Fadiilah_Dye'),'Fadiilah dan Dye 2026','Bagian 4.1','Emisi CO2 armada 92 PLTU',302.12,'MtCO2 per tahun',2023,'Observasi studi','92 PLTU termasuk IPP dan captive','R','')
    pt(('fit',2060,'BAU'),sid('2026_Fitriana'),'Fitriana dkk. 2026','Tabel 5 hlm. 7','Emisi pembangkitan listrik',544.0,'MtCO2 per tahun',2060,'BAU LEAP-NEMO','pembangkitan','E','')
    pt(('fit',2060,'NZE'),sid('2026_Fitriana'),'Fitriana dkk. 2026','Tabel 5 hlm. 7','Emisi pembangkitan listrik',60.0,'MtCO2 per tahun',2060,'NZE LEAP-NEMO','pembangkitan','E','')
    # titik teknis lain (tercatat pada register)
    for ind,v,sat,thn,sk,kat,st,cat,s_,d_,lok in [
      ('Penalti daya CCS simulasi 2 x 315 MW',30.8,'persen',2025,'Simulasi','PLTU PCC','E','Biaya tangkap saja',sid('2025_Sugito'),'Sugito dkk. 2025','Tabel 5'),
      ('Biaya tangkap CO2 simulasi 2 x 315 MW',51.8,'USD per tCO2 tertangkap',2025,'Simulasi','PLTU PCC','E','Hanya tangkap',sid('2025_Sugito'),'Sugito dkk. 2025','Tabel 6'),
      ('CAPEX CCS simulasi 2 x 315 MW',334.4,'USD juta',2025,'Simulasi','PLTU PCC','E','',sid('2025_Sugito'),'Sugito dkk. 2025','Tabel 6'),
      ('Biaya CCS TJB 5 dan 6 dua unit 13 Mt, kapal dan pipa darat',63.7,'USD per tCO2 tertangkap',2025,'ERIA Kasus A','TJB','E','Total rantai',sid('2025_ERIA'),'ERIA 2025','Tabel 5.11'),
      ('Biaya CCS TJB 5 dan 6 dua unit 13 Mt, pipa',72.4,'USD per tCO2 tertangkap',2025,'ERIA Kasus B','TJB','E','Total rantai',sid('2025_ERIA'),'ERIA 2025','Tabel 5.12'),
      ('Biaya CCS TJB satu unit 6,5 Mt, pipa',92.6,'USD per tCO2 tertangkap',2025,'ERIA Kasus B','TJB','E','Bukan untuk 13 Mt (K147)',sid('2025_ERIA'),'ERIA 2025','Tabel 5.12'),
      ('Potensi panas bumi Indonesia',29500.0,'MW',2022,'Observasi','Nasional','E','',sid('2024_Pambudi'),'Pambudi dan Ulfa 2024','Bagian 3'),
      ('Panas bumi terpasang akhir 2022',2356.0,'MW',2022,'Observasi','Nasional','E','',sid('2024_Pambudi'),'Pambudi dan Ulfa 2024','Bagian 3.1'),
      ('Sumber daya penyimpanan CO2 akuifer salin',680.57,'GtCO2',2026,'Kelas undiscovered prospective','21 cekungan','E','Mungkin tumpang tindih dengan 572,77 Gt (K160)',sid('2026_Usman'),'Usman dkk. 2026','Hasil'),
      ('Penangkapan CO2 retrofit Indramayu, 2040',6.3,'MtCO2 per tahun',2040,'Studi PLN dan mitra','Indramayu','E','Studi kelayakan',SPL,D,'Bagian CCS hlm. 48'),
      ('Kompensasi Ombilin per tCO2e dihindari (140,8 per 4,4)',32.0,'USD per tCO2e',2024,'Studi ETP','Ombilin','E','AC; sebelum biaya pengganti',SE,'ETP/UNOPS 2023','Bab 9')]:
        L.add(None,s_,d_,lok,ind,v,sat,thn,sk,kat,st,cat)
    return L
def D_Data_Struktur(L):
    sh=Sheet('D_Data_Struktur','FF7F7F7F'); n=len(L.rows)
    sh.t('A1','Lembar 130. Data terstruktur: satu angka per baris dengan sumber, tabel atau halaman, satuan, tahun, skenario, cakupan, dan status','title')
    sh.t('A2','Lapisan data untuk tabel dan grafik. Semua angka berasal dari berkas CSV atau PDF di repo (kolom Sumber merujuk D_Sumber). Warna biru: angka bersumber yang diketik. Status: R bacaan, P rencana, E eksternal, AC hitungan. Tanpa proyeksi, tanpa interpolasi, tanpa penjumlahan antar studi. Butir register yang masih bercampur (beberapa angka dalam satu sel) dipecah bertahap.','note')
    r0=7; r1=r0+n-1
    sh.f('A3',f'"Temuan utama: "&COUNTA(F{r0}:F{r1})&" angka terstruktur dari "&SUMPRODUCT(1/COUNTIF(C{r0}:C{r1},C{r0}:C{r1}))&" sumber."','txt')
    for c,t in zip('BCDEFGHIJKLM',['No','Sumber','Dokumen','Tabel atau halaman','Indikator','Nilai','Satuan','Tahun','Skenario','Cakupan atau kategori','Status','Catatan']): sh.t(f'{c}6',t,'hdr')
    for i,(s_,d_,lok,ind,v,sat,thn,skn,kat,st,cat) in enumerate(L.rows):
        r=r0+i
        sh.n(f'B{r}',i+1,'n0i'); sh.t(f'C{r}',s_,'txtt'); sh.t(f'D{r}',d_,'txtt'); sh.t(f'E{r}',lok,'txtt'); sh.t(f'F{r}',ind,'txtt')
        sh.n(f'G{r}',v,'n0i' if abs(v)>=1000 else 'n2i'); sh.t(f'H{r}',sat,'txtt')
        if thn!='': sh.n(f'I{r}',thn,'n0i')
        else: sh.t(f'I{r}','','txtt')
        sh.t(f'J{r}',skn,'txtt'); sh.t(f'K{r}',kat,'txtt'); sh.t(f'L{r}',st,'txtt'); sh.t(f'M{r}',cat,'txtt')
    sh.width('A','A',3); sh.width('B','B',6); sh.width('C','C',8); sh.width('D','D',34); sh.width('E','E',30); sh.width('F','F',52); sh.width('G','G',13); sh.width('H','H',22); sh.width('I','I',8); sh.width('J','K',24); sh.width('L','L',8); sh.width('M','M',60)
    sh.rng=(r0,r1)
    return sh
# ---------------- grafik ----------------
def G_Data_Sumber(L,ds):
    sh=Sheet('G_Data_Sumber','FFC55A11'); r0,r1=ds.rng; DS='D_Data_Struktur'
    rg=lambda c: f"{DS}!${c}${r0}:${c}${r1}"
    cell=lambda key: f"{DS}!G{r0+L.key[key]}"
    sh.t('A1','Lembar 131. Grafik semua deret bersumber dari D_Data_Struktur: skenario co-firing, jalur dan realisasi PLN, statistik energi nasional, kompensasi pensiun, pipeline EBT RUPTL, dan pembanding antar studi','title')
    sh.t('A2','Semua grafik garis dengan label pada tiap titik. Angka ditautkan ke D_Data_Struktur (hijau) atau dihitung sederhana (hitam); studi lain berstatus E dan tidak dijumlahkan dengan CM1 atau CM2. Grafik 131.1 dan 131.2 menampilkan pengurangan emisi terhadap BAU; 131.5 menampilkan realisasi pengurangan PLN; 131.10 sampai 131.12 menampilkan kapasitas terbarukan yang akan menggantikan pembangkitan fosil; grafik lain berupa deret data sumber (emisi, intensitas, kapasitas, biaya). Tidak ada proyeksi atau interpolasi: titik tanpa data berupa celah.','note')
    charts=[]; row=[5]
    def table(title,header,labels,fn,fmt='n2',first=None,note=None):
        """fn(i,j)-> formula str or None(NA). returns (first_row,last_row,cols)."""
        r=row[0]; sh.t(f'B{r}',title,'tbl'); r+=1
        sh.t(f'B{r}','Deret','hdr')
        for j,h in enumerate(header): sh.n(f'{CL(3+j)}{r}',h,'n0') if isinstance(h,int) else sh.t(f'{CL(3+j)}{r}',h,'hdr')
        hr=r; r+=1; rows=[]
        for i,lab in enumerate(labels):
            sh.t(f'B{r}',lab,'txtt')
            for j in range(len(header)):
                f=fn(i,j,r)
                sh.f(f'{CL(3+j)}{r}',f if f else 'NA()',(fmt+'l') if f and ('D_Data' in f or 'SUMIFS' in f) else (fmt if f else 'n1'))
            rows.append(r); r+=1
        if note: sh.t(f'B{r}',note,'note'); r+=1
        row[0]=r+1; return hr,rows
    def ref(rw,nc,hr_): return f"G_Data_Sumber!$C${rw}:${CL(2+nc)}${rw}",f"G_Data_Sumber!$B${rw}"
    def cats(hr_,nc): return f"G_Data_Sumber!$C${hr_}:${CL(2+nc)}${hr_}"
    # 131.A Squire
    yrs=list(range(2020,2031)); sc=['BAU','Low','Equalized','Mid','High']; lab=['BAU','Rendah','Setara','Menengah','Tinggi']
    hr,rws=table('Tabel 131.A. Emisi CO2 PLTU 2020 sampai 2030 menurut skenario co-firing (Squire dkk. 2024, CSV penulis), MtCO2 per tahun',yrs,lab,lambda i,j,r: cell(('sq',sc[i],yrs[j])),'n1')
    r=row[0]-1
    sh.t(f'B{r}','Dasar arsiran: skenario Tinggi','txtt'); sh.t(f'B{r+1}','Arsiran: BAU dikurangi Tinggi (rentang pengurangan)','txtt')
    for j in range(len(yrs)):
        c=CL(3+j); sh.f(f'{c}{r}',f'{c}{rws[4]}','n1'); sh.f(f'{c}{r+1}',f'{c}{rws[0]}-{c}{rws[4]}','n1')
    base=r; band=r+1; row[0]=r+3
    L1=[dict(val_ref=ref(rws[i],11,hr)[0],name_ref=ref(rws[i],11,hr)[1],name=lab[i],color=COLS[i],pos='t' if i<3 else 'b',marker='circle',msize=6) for i in range(5)]
    charts.append(ck.chart_xml('Gambar 131.1. Emisi CO2 PLTU 2020 sampai 2030 menurut skenario co-firing; arsir = rentang pengurangan terhadap BAU (Squire dkk. 2024, status E)',
        [dict(base_ref=f'G_Data_Sumber!$C${base}:$M${base}',band_ref=f'G_Data_Sumber!$C${band}:$M${band}',name_ref=f'G_Data_Sumber!$B${band}',name='Rentang pengurangan BAU ke Tinggi',fill='F4B183',alpha=55000)],
        L1,'MtCO2 per tahun','Tahun',cats(hr,11),yfmt='#,##0',ymin=180))
    # 131.B reduction
    y2=list(range(2024,2031))
    hr2,r2=table('Tabel 131.B. Pengurangan emisi PLTU terhadap BAU menurut skenario co-firing, 2024 sampai 2030 (BAU dikurangi skenario), MtCO2 per tahun',y2,lab[1:],lambda i,j,r: f"{cell(('sq','BAU',y2[j]))}-{cell(('sq',sc[i+1],y2[j]))}",'n1')
    L2=[dict(val_ref=ref(r2[i],7,hr2)[0],name_ref=ref(r2[i],7,hr2)[1],name=lab[i+1],color=COLS[i+1],pos='t',msize=7) for i in range(4)]
    charts.append(ck.chart_xml('Gambar 131.2. Pengurangan emisi PLTU terhadap BAU menurut skenario co-firing, 2024 sampai 2030 (hitungan sederhana atas data Squire dkk., status AC)',[],L2,'MtCO2 per tahun','Tahun',cats(hr2,7),yfmt='#,##0'))
    # 131.C PLN ARED
    ya=list(range(2020,2061,5))
    hr3,r3=table('Tabel 131.C. Jalur ARED PLN: emisi Lingkup 1 sampai 3 pembangkitan (MtCO2e per tahun) dan intensitas (tCO2 per MWh), dibaca dari Gambar 7 laporan PLN 2024',ya,['Emisi ARED (MtCO2e)','Intensitas ARED (tCO2 per MWh)'],
        lambda i,j,r: cell(('ared',ya[j])) if i==0 else (cell(('aredi',ya[j])) if ('aredi',ya[j]) in L.key else None),'n1',note='Intensitas hanya tercatat pada 2020, 2030, 2040, 2050, 2060; sel #N/A adalah celah, bukan data.')
    L3=[dict(val_ref=ref(r3[0],9,hr3)[0],name_ref=ref(r3[0],9,hr3)[1],name='Emisi ARED (MtCO2e)',color='C00000',pos='t'),
        dict(val_ref=ref(r3[1],9,hr3)[0],name_ref=ref(r3[1],9,hr3)[1],name='Intensitas ARED (tCO2 per MWh, sumbu kanan)',color='2E75B6',pos='b',sec=True,fmt='0.00')]
    charts.append(ck.chart_xml('Gambar 131.3. Jalur ARED PLN 2020 sampai 2060: emisi pembangkitan turun dari puncak 326 MtCO2e (2030) ke nol (2060), dengan intensitas (PLN 2024, status R)',[],L3,'MtCO2e per tahun','Tahun',cats(hr3,9),yfmt='#,##0',ytitle2='tCO2 per MWh',yfmt2='0.00'))
    # 131.D PLN plant type
    y3=[2022,2023,2024]; kind=['PLTU milik PLN','PLTGU','PLTMG','PLTD','PLTG']
    hr4,r4=table('Tabel 131.D. Emisi pembangkitan PLN menurut jenis pembangkit, 2022 sampai 2024 (PLN 2024 Tabel 14), MtCO2e',y3,kind,lambda i,j,r: cell(('pln','Emisi '+kind[i].replace(' milik PLN','') if i else 'Emisi PLTU milik PLN',y3[j])),'n1')
    L4=[dict(val_ref=ref(r4[i],3,hr4)[0],name_ref=ref(r4[i],3,hr4)[1],name=kind[i]+('' if i==0 else ' (sumbu kanan)'),color=COLS[i],pos='t' if i<2 else 'b',sec=(i>0)) for i in range(5)]
    charts.append(ck.chart_xml('Gambar 131.4. Emisi pembangkitan PLN menurut jenis pembangkit, 2022 sampai 2024: PLTU sumbu kiri, jenis lain sumbu kanan (PLN 2024, status R)',[],L4,'MtCO2e per tahun (PLTU)','Tahun',cats(hr4,3),yfmt='#,##0',ymin=0,ytitle2='MtCO2e per tahun (jenis lain)',yfmt2='#,##0'))
    # 131.E PLN reductions
    ini=['EBT tambahan','Teknologi batubara bersih','Konversi gas ke siklus kombinasi','Co-firing biomassa','Total realisasi']; indn=['Realisasi pengurangan: EBT tambahan','Realisasi pengurangan: teknologi batubara bersih','Realisasi pengurangan: konversi gas ke siklus kombinasi','Realisasi pengurangan: co-firing biomassa','Realisasi pengurangan: total']
    hr5,r5=table('Tabel 131.E. Realisasi pengurangan emisi PLN menurut inisiatif, 2022 sampai 2024 (PLN 2024 Tabel 17), MtCO2e; baris terakhir target total',y3,ini+['Target total'],lambda i,j,r: cell(('pln',(indn+['Target pengurangan: total'])[i],y3[j])) if (('pln',(indn+['Target pengurangan: total'])[i],y3[j])) in L.key else None,'n1')
    L5=[dict(val_ref=ref(r5[i],3,hr5)[0],name_ref=ref(r5[i],3,hr5)[1],name=(ini+['Target total'])[i],color=COLS[i] if i<5 else '7F7F7F',dash='dash' if i==5 else None,pos='t' if i in (4,5) else 'b') for i in range(6)]
    charts.append(ck.chart_xml('Gambar 131.5. Realisasi pengurangan emisi PLN menurut inisiatif, 2022 sampai 2024, dan target total (PLN 2024 Tabel 17, status R)',[],L5,'MtCO2e per tahun','Tahun',cats(hr5,3),yfmt='#,##0'))
    # 131.F OWID generation
    yo=list(range(2015,2025)); gen=[('coal_electricity','Batubara'),('gas_electricity','Gas'),('oil_electricity','Minyak'),('hydro_electricity','Hidro'),('biofuel_electricity','Bioenergi'),('other_renewable_exc_biofuel_electricity','Terbarukan lain'),('solar_electricity','Surya'),('wind_electricity','Angin')]
    hr6,r6=table('Tabel 131.F. Pembangkitan listrik Indonesia menurut sumber, 2015 sampai 2024 (OWID), TWh',yo,[g[1] for g in gen],lambda i,j,r: cell(('ow',gen[i][0],yo[j])),'n1')
    L6=[dict(val_ref=ref(r6[i],10,hr6)[0],name_ref=ref(r6[i],10,hr6)[1],name=gen[i][1]+('' if i<2 else ' (sumbu kanan)'),color=COLS[i%8],pos='t' if i<2 else 'b',msize=5,fmt='#,##0.0',sec=(i>=2)) for i in range(8)]
    charts.append(ck.chart_xml('Gambar 131.6. Pembangkitan listrik Indonesia menurut sumber, 2015 sampai 2024: batubara dan gas sumbu kiri, sumber lain sumbu kanan (OWID, status R)',[],L6,'TWh (batubara dan gas)','Tahun',cats(hr6,10),yfmt='#,##0',ytitle2='TWh (sumber lain)',yfmt2='#,##0'))
    hr7,r7=table('Tabel 131.G. Intensitas karbon listrik nasional (siklus hidup), 2015 sampai 2024 (OWID), gCO2e per kWh',yo,['Intensitas karbon listrik'],lambda i,j,r: cell(('ow','carbon_intensity_elec',yo[j])),'n1')
    charts.append(ck.chart_xml('Gambar 131.7. Intensitas karbon listrik nasional, 2015 sampai 2024: rata-rata nasional siklus hidup, bukan faktor marginal (OWID, status R)',[],
        [dict(val_ref=ref(r7[0],10,hr7)[0],name_ref=ref(r7[0],10,hr7)[1],name='Intensitas karbon listrik (gCO2e per kWh)',color='C00000',pos='t')],'gCO2e per kWh','Tahun',cats(hr7,10),yfmt='#,##0',ymin=600))
    # 131.H OWID oil gas
    og=[('gas_production','Produksi gas'),('gas_consumption','Konsumsi gas'),('oil_production','Produksi minyak'),('oil_consumption','Konsumsi minyak')]
    hr8,r8=table('Tabel 131.H. Produksi dan konsumsi energi primer minyak dan gas, 2015 sampai 2024 (OWID), TWh',yo,[g[1] for g in og],lambda i,j,r: cell(('ow',og[i][0],yo[j])),'n1')
    charts.append(ck.chart_xml('Gambar 131.8. Produksi dan konsumsi energi primer minyak dan gas Indonesia, 2015 sampai 2024: selisih tidak dapat diatribusikan ke gas suar atau kebocoran (OWID, status R)',[],
        [dict(val_ref=ref(r8[i],10,hr8)[0],name_ref=ref(r8[i],10,hr8)[1],name=og[i][1],color=COLS[i],pos='t' if i%2==0 else 'b',msize=5) for i in range(4)],'TWh','Tahun',cats(hr8,10),yfmt='#,##0'))
    # 131.I ETP
    ye=list(range(2024,2039))
    pay=f'{rg("F")},"Kompensasi pensiun dini pada tahun pensiun",{rg("I")}'
    hr9,r9=table('Tabel 131.I. Kompensasi pensiun dini 32 aset PLTU menurut tahun pensiun dalam skenario studi (ETP/UNOPS 2023 Tabel 14.1), USD juta',ye,['Pembayaran pada tahun pensiun','Kumulatif pembayaran'],
        lambda i,j,r: (f'SUMIFS({rg("G")},{rg("F")},"Kompensasi pensiun dini pada tahun pensiun",{rg("I")},{ye[j]})' if i==0 else (f'SUM($C{r-1}:{CL(3+j)}{r-1})')),'n0')
    charts.append(ck.chart_xml('Gambar 131.9. Kompensasi pensiun dini PLTU menurut tahun pensiun (skenario studi ETP/UNOPS 2023): pembayaran tahunan dan kumulatif, USD juta (status E, valuasi aset)',[],
        [dict(val_ref=ref(r9[0],15,hr9)[0],name_ref=ref(r9[0],15,hr9)[1],name='Pembayaran pada tahun pensiun',color='2E75B6',pos='t',fmt='#,##0'),
         dict(val_ref=ref(r9[1],15,hr9)[0],name_ref=ref(r9[1],15,hr9)[1],name='Kumulatif pembayaran (sumbu kanan)',color='C00000',pos='b',fmt='#,##0',sec=True)],'USD juta','Tahun pensiun',cats(hr9,15),yfmt='#,##0',ytitle2='USD juta kumulatif',yfmt2='#,##0'))
    # 131.J EBT
    yb=list(range(2025,2035)); ex=['PLTS','PLTB','PLTA','PLTA-PS','PLTM','PLTP','PLTBm','PLTBg','PLTSa','PLTAL','PLTN','Unknown']
    def ebt_f(scn,jenis,j): return f'SUMIFS({rg("G")},{rg("F")},"Tambahan kapasitas menurut tahun COD rencana",{rg("J")},"{scn}",{rg("K")},"{jenis}",{rg("I")},{yb[j]})'
    def annual(scn,j): return f'SUMIFS({rg("G")},{rg("F")},"Tambahan kapasitas menurut tahun COD rencana",{rg("J")},"{scn}",{rg("I")},{yb[j]})-SUMIFS({rg("G")},{rg("F")},"Tambahan kapasitas menurut tahun COD rencana",{rg("J")},"{scn}",{rg("K")},"BESS",{rg("I")},{yb[j]})'
    def kum(r_,j): return f'SUM($C{r_}:{CL(3+j)}{r_})'
    hr10,r10=table('Tabel 131.J. Tambahan kapasitas pembangkit terbarukan menurut RUPTL 2025 sampai 2034 (tanpa BESS), MW menurut tahun COD',yb,['RE Base: tahunan','ARED: tahunan','RE Base: kumulatif','ARED: kumulatif','Tambahan ARED terhadap RE Base (kumulatif)'],
        lambda i,j,r: annual('RE Base',j) if i==0 else (annual('ARED',j) if i==1 else (kum(r-2,j) if i in (2,3) else f'{CL(3+j)}{r-1}-{CL(3+j)}{r-2}')),'n0',note='Proyek tanpa COD pada suatu skenario tidak dihitung pada skenario itu. Status proyek dan tambahan terhadap CPOS belum diverifikasi (WP-D).')
    rr=row[0]-1
    sh.t(f'B{rr}','Dasar arsiran: RE Base kumulatif','txtt'); sh.t(f'B{rr+1}','Arsiran: tambahan ARED terhadap RE Base','txtt')
    for j in range(10): c=CL(3+j); sh.f(f'{c}{rr}',f'{c}{r10[2]}','n0'); sh.f(f'{c}{rr+1}',f'{c}{r10[4]}','n0')
    b10=rr; row[0]=rr+3
    charts.append(ck.chart_xml('Gambar 131.10. Tambahan kapasitas terbarukan kumulatif menurut RUPTL 2025 sampai 2034 (tanpa BESS): RE Base, ARED, dan tambahan ARED (arsir), MW',
        [dict(base_ref=f'G_Data_Sumber!$C${b10}:$L${b10}',band_ref=f'G_Data_Sumber!$C${b10+1}:$L${b10+1}',name_ref=f'G_Data_Sumber!$B${b10+1}',name='Tambahan ARED terhadap RE Base',fill='A9D18E',alpha=55000)],
        [dict(val_ref=ref(r10[2],10,hr10)[0],name_ref=ref(r10[2],10,hr10)[1],name='RE Base: kumulatif',color='2E75B6',pos='b',fmt='#,##0'),dict(val_ref=ref(r10[3],10,hr10)[0],name_ref=ref(r10[3],10,hr10)[1],name='ARED: kumulatif',color='2E7D32',pos='t',fmt='#,##0')],'MW kumulatif','Tahun COD',cats(hr10,10),yfmt='#,##0'))
    grp=[('PLTS surya',['PLTS']),('PLTB angin',['PLTB']),('Hidro dan PS',['PLTA','PLTA-PS','PLTM']),('Panas bumi',['PLTP']),('Bioenergi dan sampah',['PLTBm','PLTBg','PLTSa']),('Nuklir dan arus laut',['PLTN','PLTAL']),('BESS (MW)',['BESS'])]
    def gann(i,j): return '+'.join(ebt_f('ARED',x,j) for x in grp[i][1])
    hr11,r11=table('Tabel 131.K. Tambahan kapasitas menurut teknologi, skenario ARED, MW menurut tahun COD (tahunan lalu kumulatif; BESS terpisah)',yb,[g[0]+': tahunan' for g in grp]+[g[0]+': kumulatif' for g in grp],
        lambda i,j,r: gann(i,j) if i<7 else kum(r-7,j),'n0')
    big=[0,2,1]; small=[3,4,5,6]
    charts.append(ck.chart_xml('Gambar 131.11. Tambahan kapasitas surya, hidro dan angin, skenario ARED RUPTL 2025 sampai 2034, MW kumulatif (status P, belum diverifikasi)',[],
        [dict(val_ref=ref(r11[7+i],10,hr11)[0],name_ref=ref(r11[7+i],10,hr11)[1],name=grp[i][0],color=COLS[k],pos='t' if k<2 else 'b',msize=6,fmt='#,##0') for k,i in enumerate(big)],'MW kumulatif','Tahun COD',cats(hr11,10),yfmt='#,##0'))
    charts.append(ck.chart_xml('Gambar 131.12. Tambahan kapasitas panas bumi, bioenergi, nuklir dan BESS, skenario ARED RUPTL 2025 sampai 2034, MW kumulatif (BESS dalam MW; status P)',[],
        [dict(val_ref=ref(r11[7+i],10,hr11)[0],name_ref=ref(r11[7+i],10,hr11)[1],name=grp[i][0],color=COLS[k+3],pos='t' if k%2==0 else 'b',msize=6,fmt='#,##0') for k,i in enumerate(small)],'MW kumulatif','Tahun COD',cats(hr11,10),yfmt='#,##0'))
    # 131.L pembanding antar studi
    yc=[2020,2022,2023,2024,2025,2030,2034,2035,2040,2045,2050,2055,2060]
    def pv(key): return cell(key) if key in L.key else None
    series=[('PLN aktual: pembangkitan Lingkup 1 sampai 3',lambda y: pv(('pln','Emisi Lingkup 1, 2, 3 pembangkitan',y))),
            ('PLN ARED: pembangkitan Lingkup 1 sampai 3',lambda y: pv(('ared',y))),
            ('RUPTL RE Base: emisi on-grid',lambda y: pv(('ru',y,'RE Base'))),
            ('RUPTL ARED: emisi on-grid',lambda y: pv(('ru',y,'ARED'))),
            ('JETP CIPP: batas on-grid 2030',lambda y: pv(('jetp',y))),
            ('Squire BAU: emisi PLTU model',lambda y: pv(('sq','BAU',y))),
            ('Squire Tinggi: emisi PLTU model',lambda y: pv(('sq','High',y))),
            ('Fadiilah dan Dye: 92 PLTU',lambda y: pv(('fad',y))),
            ('Fitriana BAU: pembangkitan',lambda y: pv(('fit',y,'BAU'))),
            ('Fitriana NZE: pembangkitan',lambda y: pv(('fit',y,'NZE')))]
    hr12,r12=table('Tabel 131.L. Pembanding jalur emisi sektor listrik menurut studi yang tercatat (batas dan cakupan berbeda; tidak dijumlahkan), MtCO2 per tahun',yc,[s[0] for s in series],lambda i,j,r: series[i][1](yc[j]),'n1',note='Cakupan berbeda: PLN (Lingkup 1 sampai 3), RUPTL (on-grid PLN dan IPP), Squire (emisi PLTU model), Fadiilah (92 PLTU termasuk IPP dan captive), Fitriana (pembangkitan model). Sel #N/A adalah celah, bukan data. Jarak tahun tidak proporsional.')
    sty=[dict(color=COLS[0],marker='circle'),dict(color='C00000',marker='circle'),dict(color='7030A0',marker='diamond'),dict(color='BF8F00',marker='diamond'),dict(color='2E7D32',marker='square'),dict(color='7F7F7F',marker='triangle'),dict(color='00838F',marker='triangle'),dict(color='E36C09',marker='x'),dict(color='000000',marker='circle'),dict(color='1F4E79',marker='circle')]
    charts.append(ck.chart_xml('Gambar 131.13. Pembanding jalur emisi sektor listrik menurut studi yang tercatat: PLN, RUPTL, JETP, Squire, Fadiilah dan Dye, Fitriana (status E atau P; cakupan berbeda; titik bersumber saja)',[],
        [dict(val_ref=ref(r12[i],13,hr12)[0],name_ref=ref(r12[i],13,hr12)[1],name=series[i][0],pos='t' if i%2==0 else 'b',msize=8,**sty[i]) for i in range(10)],'MtCO2 per tahun','Tahun (titik bersumber, jarak tidak proporsional)',cats(hr12,13),yfmt='#,##0'))
    ye2=list(range(2015,2026)); bf=[('Biofuels production - PJ','Produksi biofuel (PJ)'),('Biofuels consumption - PJ','Konsumsi biofuel (PJ)')]
    hr13,r13=table('Tabel 131.M. Biofuel Indonesia, produksi dan konsumsi setara energi, 2015 sampai 2025 (Energy Institute 2026, salinan olahan), PJ',ye2,[b[1] for b in bf],lambda i,j,r: cell(('ei',bf[i][0],ye2[j])),'n0')
    charts.append(ck.chart_xml('Gambar 131.14. Produksi dan konsumsi biofuel Indonesia, 2015 sampai 2025, PJ: pembanding aktivitas nasional untuk B40 (Energy Institute 2026, status R; salinan pihak ketiga)',[],
        [dict(val_ref=ref(r13[i],11,hr13)[0],name_ref=ref(r13[i],11,hr13)[1],name=bf[i][1],color=COLS[i],pos='t' if i==0 else 'b',fmt='#,##0') for i in range(2)],'PJ','Tahun',cats(hr13,11),yfmt='#,##0'))
    fl=[('CO2 from Flaring','CO2 gas suar (MtCO2)'),('Natural Gas Flaring','Volume gas suar (miliar m3, sumbu kanan)')]
    hr14,r14=table('Tabel 131.N. Gas suar Indonesia: volume dan CO2, 2015 sampai 2025 (Energy Institute 2026, salinan olahan, VIIRS Nightfire)',ye2,[f[1] for f in fl],lambda i,j,r: cell(('ei',fl[i][0],ye2[j])),'n2',note='Perkiraan satelit migas hulu dan hilir; GCV 40 MJ per m3 dan pembakaran sempurna. Mirip dengan potensi 1,7 MtCO2e di workbook tetapi cakupan, metode, dan potensi pemulihan belum direkonsiliasi.')
    charts.append(ck.chart_xml('Gambar 131.15. Emisi CO2 dari gas suar Indonesia, 2015 sampai 2025 (Energy Institute 2026, status R; volume pada Tabel 131.N; pembanding skala 1,7 MtCO2e potensi migas)',[],
        [dict(val_ref=ref(r14[0],11,hr14)[0],name_ref=ref(r14[0],11,hr14)[1],name=fl[0][1],color='C00000',pos='t',fmt='0.00')],'MtCO2','Tahun',cats(hr14,11),yfmt='0.0',ymin=0))
    yr=[1982,2002,2012,2022]; ln=['Semenanjung Kampar','Kerumutan']
    hr15,r15=table('Tabel 131.O. Tutupan hutan alam lanskap Riau, 1982 sampai 2022 (Nursamsu dkk. 2024, SIGAP KLHK), ha',yr,ln,lambda i,j,r: cell(('riau',ln[i],yr[j])),'n0',note='Kehilangan tutupan hutan alam adalah sumber emisi FOLU yang dicegah RO 1 sampai RO 3; jarak tahun tidak proporsional.')
    charts.append(ck.chart_xml('Gambar 131.16. Tutupan hutan alam lanskap Semenanjung Kampar dan Kerumutan, 1982 sampai 2022, ha: dasar aksi pencegahan deforestasi FOLU Net Sink (status R; jarak tahun tidak proporsional)',[],
        [dict(val_ref=ref(r15[i],4,hr15)[0],name_ref=ref(r15[i],4,hr15)[1],name=ln[i],color=COLS[i],pos='t' if i==1 else 'b',fmt='#,##0') for i in range(2)],'ha','Tahun',cats(hr15,4),yfmt='#,##0',ymin=0))
    # tata letak grafik
    top=row[0]+2; sh.t(f'B{top-1}','Grafik','tbl')
    pos=[]
    for k,ch in enumerate(charts):
        col=1 if k%2==0 else 9; rw=top+(k//2)*25
        pos.append((ch,(col,rw-1,7800000,4600000)))
    sh.charts=pos
    sh.width('A','A',3); sh.width('B','B',60); sh.width('C','N',10)
    sh.f('A3',f'"Temuan utama: {len(charts)} grafik dari D_Data_Struktur ("&COUNTA({rg("F")})&" angka); PLN ARED puncak "&TEXT({cell(("ared",2030))},"0")&" MtCO2e pada 2030; skenario Squire Menengah mengurangi "&TEXT({cell(("sq","BAU",2030))}-{cell(("sq","Mid",2030))},"0.0")&" MtCO2 PLTU pada 2030; ARED menambah "&TEXT(L{r10[4]},"#,##0")&" MW terbarukan terhadap RE Base sampai 2034."','txt')
    return sh
def make():
    L=build_long(); ds=D_Data_Struktur(L); gs=G_Data_Sumber(L,ds); sd=D_Sumber()
    return sd,ds,gs
if __name__=='__main__':
    sd,ds,gs=make(); print(len(ds.cells),len(gs.charts))
