import openpyxl,collections,sys
sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from xlsxkit import *
P='/home/user/NetZeroEmission/Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx'
wb=openpyxl.load_workbook(P,data_only=True,read_only=True)
cs=wb['C_Solusi_2030']; csv={}
from openpyxl.utils import get_column_letter as L
for i,r in enumerate(cs.iter_rows(min_row=1,max_row=70,values_only=True),1):
    for j,v in enumerate(r,1): csv[f'{L(j)}{i}']=v
dt=wb['D_Teknis_Opsi']; cnt=collections.Counter()
for r in dt.iter_rows(min_row=6,values_only=True):
    if r[0]: cnt[(r[2],'all')]+=1; cnt[(r[2],r[8])]+=1
SIAP,HIT,KUR,BEL,PEN,PEM,BUK='Siap','Siap setelah hitung ulang','Kurang masukan','Belum bisa','Pendukung','Pembanding','Bukan solusi'
CO='Faktor emisi PLTU batubara 0,79 sampai 1,22 kgCO2 per kWh, rata-rata 0,96 (Fadiilah dan Dye 2026; Zahari dan McLellan 2024)'
RU='Tambahan kapasitas RUPTL 2025 sampai 2034 per jenis (D_RUPTL_Tambahan)'
# (sektor, solusi, D_Teknis name, A cells, B cells, asal, skala, FE, deret, kesiapan, kurang, rujukan)
R=[
('Energi','EBT RUPTL 2021 (20,9 GW), agregat',None,('D24','E24'),None,'P resmi (D_Solusi_Kuantif butir 7)',RU,CO,'Ya (G_Opsi_Detail, EBT RUPTL)',SIAP,'Total siap; rincian per teknologi di baris berikut.',''),
('Energi','Surya skala utilitas','Surya skala utilitas',None,('D36','E36'),'AC, sisa selisih (BUKAN angka bersumber)',RU+'; IEEFA Agt 2026 (100 GW)',CO,'Ya (kapasitas pengganti, penyimpanan)',HIT,'Angka 61,4 Mt adalah sisa selisih. Ganti dengan kapasitas surya bersumber x faktor kapasitas 0,205 x 8,76 x 0,96; sisa selisih menjadi selisih yang belum tertutup.','R5, R15'),
('Energi','Surya atap','Surya atap',None,None,'Tidak ada',"Tidak ada rencana kapasitas atap tersendiri (RUPTL menggabung PLTS)",CO,'Tidak','Kurang masukan'.replace('Kurang masukan',KUR),'Rencana kapasitas surya atap bersumber (2030) dan pemisahan PLTS atap dari PLTS utilitas.','R19'),
('Energi','Surya terapung','Surya terapung',None,None,'Tidak ada','Tidak ada rencana kapasitas terapung tersendiri',CO,'Tidak',KUR,'Rencana kapasitas surya terapung bersumber (2030).','R19'),
('Energi','Angin darat','Angin darat',None,None,'Tidak ada','RUPTL memuat PLTB gabungan dengan PLTS ("Surya dan bayu")',CO,'Ya (kapasitas RUPTL gabungan)',KUR,'Pemisahan PLTB dari PLTS dalam RUPTL atau rencana kapasitas angin bersumber; faktor kapasitas 0,28 sudah ada.','R19'),
('Energi','Angin laut','Angin laut',None,None,'Tidak ada','Tidak ada rencana kapasitas 2030 yang tercatat',CO,'Tidak',BEL,'Rencana atau potensi kapasitas angin laut bersumber.','R19'),
('Energi','PLTA besar','PLTA besar',None,None,'Tidak ada',RU+' (PLTA)',CO,'Ya (kapasitas RUPTL)',SIAP,'Hitung: tambahan PLTA x 0,55 x 8,76 x 0,96.',''),
('Energi','Mini hidro','Mini hidro',None,None,'Tidak ada',RU+' (PLTM)',CO,'Ya (kapasitas RUPTL)',SIAP,'Hitung: tambahan PLTM x 0,55 x 8,76 x 0,96.',''),
('Energi','Panas bumi','Panas bumi',None,('D35','E35'),'AC dari jalur PLN 3 GW',RU+' (PLTP); jalur PLN 3 GW',CO,'Ya (EBT RUPTL)',SIAP,'Hitung ulang langsung dari tambahan PLTP RUPTL x 0,853; cek terhadap 19,2 Mt.',''),
('Energi','Biomassa (PLTBm tersendiri)','Biomassa',None,None,'Tidak ada',RU+' (PLTBM)','Faktor CO2 serbuk gergaji 1,25 tCO2 per ton; rentang LCA biopower negatif 1.000 sampai 1.300 gCO2e per kWh (CREA 2025)','Ya (kebutuhan biomassa RUPTL)',KUR,'Emisi siklus hidup biomassa tidak netral; perlu aturan pembukuan (netral atau tidak) bersumber sebelum menghitung pengurangan.','R20'),
('Energi','Nuklir','Nuklir',None,None,'Tidak ada','RUPTL 2025 sampai 2034: PLTN 0 MW; kapasitas muncul hanya pada skenario LEAP 2060 (Nursidik 2025)',CO,'Tidak',BEL,'Tidak ada kapasitas pada 2030. Hanya dapat disusun untuk 2060 setelah jadwal resmi (R6).','R6'),
('Energi','Baterai dan penyimpanan','Baterai dan penyimpanan',None,None,'Tidak ada','RUPTL: BESS dan PLTA PS (Penyimpanan)','Tidak berlaku','Ya (penyimpanan pendamping)',PEN,'Pendukung surya dan angin; tidak punya pengurangan emisi sendiri. Grafik hanya menunjukkan kebutuhan pendamping dan pengurangan emisi surya yang didukungnya.',''),
('Energi','Pensiun dini PLTU (resmi, 36 Mt)','Pensiun dini PLTU',None,('D30','E30'),'P resmi (potensi CM2)','Daftar unit dan kapasitas PLTU (D_Gen_Eksisting, D_Phasedown)',CO+'; enam PLTU 93,52 MtCO2 per tahun (Fadiilah dan Dye 2026)','Ya (kapasitas dan emisi PLTU)',SIAP,'',''),
('Energi','Pensiun dini enam PLTU, bagian tambahan','Pensiun dini PLTU',None,('D33','E33'),'AC: 93,52 dikurangi 36','Enam PLTU (Fadiilah dan Dye 2026)',CO,'Ya',SIAP,'Tumpang tindih dengan CCS TJB belum dipastikan.',''),
('Energi','CCS PLTU Tanjung Jati B (dua unit)','CCS PLTU',None,('D34','E34'),'AC dari kapasitas dan laju tangkap','Dua unit TJB; ERIA CCS 2025','Laju tangkap (kinerja); faktor emisi PLTU',"Tidak",SIAP,'Penalti energi CCS belum ada; biaya 63,7 sampai 92,6 USD per tCO2.','R7'),
('Energi','Co-firing biomassa','Biomassa',('D27','E27'),None,'P (PLN dan ENDC 11 Mt); diandaikan di dalam CM1','Target PLN 52 unit 18.895 MW, 10,2 juta t biomassa; pasokan limbah 504,4 miliar MJ (Squire 2024)','Faktor CO2 serbuk gergaji 1,25 t per t; rasio termal per boiler (Squire Tabel 3)','Ya (kebutuhan biomassa RUPTL)',SIAP,'Konflik 11 Mt dengan 14,2 sampai 152,5 Mt (K125); realisasi 14,3 persen.','R11'),
('Energi','Efisiensi energi (enam program)',None,('D25','E25'),None,'P resmi (D_Solusi_Kuantif butir 8 sampai 13)','Target tiap program (D_Solusi_Kuantif)','Tidak tercatat per program','Tidak',KUR,'Parameter teknis per program (tidak ada di D_Teknis_Opsi), deret tahunan, biaya Indonesia.','R2'),
('Energi','Biodiesel B40','Biofuel (B40 dan B50)',('D26','E26'),None,'E klaim ESDM 41,46 Mt per tahun (K122: 32,2)','Volume biodiesel dan kuota B40 tidak tercatat','Klaim pengurangan; faktor per liter belum bersumber','Tidak',KUR,'Volume per tahun dan faktor emisi per liter bersumber agar klaim dapat dihitung, bukan hanya dikutip.','R1'),
('Energi','Pemanfaatan gas suar',None,None,('D31','E31'),'P resmi 1,7 Mt','Tidak ada parameter teknis','Tidak ada','Tidak',BEL,'Volume gas suar dan faktor emisi; tidak ada baris di D_Teknis_Opsi.','R21'),
('Energi','Sisa CM1 energi yang tidak dirinci',None,('D28','E28'),None,'AC sisa (358 dikurangi program tercatat)','Tidak berlaku','Tidak berlaku','Tidak',BUK,'Residual, bukan teknologi; tidak mendapat lembar.','R8'),
('Energi','Potensi CM2 energi yang tidak dirinci',None,None,('D32','E32'),'P resmi 50,3 Mt','Tidak berlaku','Tidak berlaku','Tidak',BUK,'Tidak dirinci dalam dokumen; tidak mendapat lembar.','R8'),
('FOLU','Tata air gambut','Tata air gambut',('D43','E43'),('D55','E55'),'AC: luas Renops x faktor BTR-1 16,83 tCO2 per ha','Luas target (D_Aksi, Renops)','16,83 tCO2 per ha per tahun (BTR-1, D_Faktor)','Ya (BTR-1 dan target)',SIAP,'Tambahan CM2 sama dengan nol.',''),
('FOLU','Penghindaran degradasi gambut','Degradasi hutan',('D44','E44'),('D56','E56'),'AC','Luas Renops','Faktor BTR-1 dan FREL','Ya (FREL, FOLU historis)',SIAP,'D_Teknis_Opsi menggabung degradasi gambut dan mineral.',''),
('FOLU','Pengelolaan hutan lestari (RIL-C dan ENR)','Pengelolaan hutan lestari (PHL)',('D45','E45'),('D57','E57'),'AC','Luas target BTR-1','Faktor SFM tersirat 3,96 tCO2 per ha','Ya (BTR-1 dan target)',SIAP,'',''),
('FOLU','Penghindaran deforestasi gambut','Deforestasi gambut',('D46','E46'),('D58','E58'),'AC','Kuota Renops (D_Aksi)','Faktor gambut BTR-1 (13 butir)','Ya',SIAP,'',''),
('FOLU','Restorasi gambut','Restorasi gambut',('D47','E47'),('D59','E59'),'AC; rentang lebar 1,6 sampai 57,2','Luas target dan capaian 10 persen (2018)','Faktor 32,42 tCO2 per ha (BTR-1)','Ya',SIAP,'Rentang lebar menurut definisi luas; capaian terbaru belum ada.','R10'),
('FOLU','Penghindaran degradasi hutan mineral','Degradasi hutan',('D48','E48'),('D60','E60'),'AC','Luas Renops','Faktor FREL dan BTR-1','Ya',SIAP,'',''),
('FOLU','Penghindaran deforestasi mineral','Deforestasi mineral',('D49','E49'),('D61','E61'),'AC','Kuota Renops','Faktor FREL','Ya',SIAP,'',''),
('FOLU','Rehabilitasi lahan tanpa rotasi','Rehabilitasi lahan',('D50','E50'),('D62','E62'),'AC','Target Net Sink; Aryapratama 2026: 0,44 sampai 3,60 Mha cocok','Faktor pertumbuhan BTR-1','Ya',SIAP,'Batas luas lahan cocok (K126) harus ditampilkan.','R14'),
('FOLU','Rehabilitasi lahan dengan rotasi','Rehabilitasi lahan',('D51','E51'),('D63','E63'),'AC; tambahan CM2 nol','Target Net Sink','Faktor pertumbuhan BTR-1','Tidak',SIAP,'Tidak ada deret tahunan terpisah; tambahan CM2 sama dengan nol.',''),
('FOLU','Hutan tanaman (PBPH-HT)','Hutan tanaman (HTI)',('D52','E52'),('D64','E64'),'AC; tambahan CM2 nol','Target dan capaian 14 persen (2017)','Faktor tanaman 9,6 t per ha per tahun','Ya',SIAP,'Realisasi lama (2017); rentang biaya sangat lebar.','R10'),
('FOLU','CM1 dan CM2 FOLU resmi yang belum dijelaskan',None,('D53','E53'),('D65','E65'),'AC residual','Tidak berlaku','Tidak berlaku','Ya (janji ENDC)',BUK,'Residual resmi; tidak mendapat lembar.','R8'),
('FOLU','Mangrove','Mangrove',None,None,'Tidak ada','Potensi 3 butir; tidak ada target luas 2030 tercatat','8 butir faktor (Murdiyarso 2024)','Tidak',KUR,'Target luas restorasi mangrove 2030 bersumber (Renops atau RPJMN).','R14'),
('Industri','Semen','Semen',None,None,'Tidak ada','Skala 1 butir','Intensitas BAU 702 kgCO2e per t (Utama 2025)','Tidak',KUR,'Pengurangan per teknologi dari skenario TIMES (PDF Utama 2025) belum diekstrak.','R22'),
('Industri','Baja','Baja',None,None,'Tidak ada','Tidak ada','Intensitas BAU 1.994 kgCO2e per t','Tidak',KUR,'Pengurangan TIMES dan produksi bersumber.','R22'),
('Industri','Kertas dan pulp','Kertas dan pulp',None,None,'Tidak ada','Tidak ada','Intensitas BAU 618 kgCO2e per t','Tidak',KUR,'Pengurangan TIMES dan produksi bersumber.','R22'),
('Industri','Amonia','Amonia',None,None,'Tidak ada','Potensi 1 butir','Intensitas BAU 1.805 kgCO2e per t','Tidak',KUR,'Pengurangan TIMES dan produksi bersumber.','R22'),
('Industri','Metanol','Metanol',None,None,'Tidak ada','Tidak ada','Intensitas BAU 183 kgCO2e per t','Tidak',KUR,'Pengurangan TIMES dan produksi bersumber.','R22'),
('Industri','Olefin','Olefin',None,None,'Tidak ada','Tidak ada','Intensitas BAU 900 kgCO2e per t','Tidak',KUR,'Pengurangan TIMES dan produksi bersumber.','R22'),
('Industri','CCS industri','CCS industri',None,None,'Tidak ada','Potensi dan skala 1 butir','Tidak ada','Tidak',BEL,'Faktor penangkapan dan volume bersumber.','R7'),
('Industri','Efisiensi energi industri','Efisiensi energi industri',None,None,'E contoh SETI (9.550 tCO2 per tiga pabrik)','Tidak ada','Faktor emisi 19 produk energi (Zain 2025)','Tidak',KUR,'Skala nasional dan pengurangan agregat HEIO (Zain 2025) belum dicatat per opsi.','R2, R22'),
('Industri','Captive PLTU nikel','Captive PLTU nikel',None,None,'E tidak ada nilai nasional','Skala 1 butir; Squire 2024: captive 17,7 GW pada 2030','Intensitas nikel 58,6 sampai 99 tCO2e per t Ni (E)','Tidak',KUR,'Kapasitas captive per unit dan opsi pensiun bersumber.','R17'),
('Transportasi','Kendaraan listrik (BEV)','Elektrifikasi kendaraan (BEV)',None,None,'Tidak ada (target ENDC CM1 15,2 juta unit)','Target 15.197.000 EV 2030; realisasi 195.084 (Nov 2024)','Faktor jaringan 0,82 kgCO2 per kWh; siklus hidup per pkm (Greenpeace dan RDI)','Tidak',KUR,'Kilometer tempuh per jenis kendaraan bersumber untuk mengubah unit menjadi MtCO2e.','R23'),
('Transportasi','Angkutan umum dan peralihan moda','Angkutan umum dan peralihan moda',None,None,'E Transjakarta 277.000 tCO2e per tahun','Bus listrik: 8.925 unit (BAU) sampai 132.000 (Robbi 2026)','66,6 tCO2 per bus ICE per tahun (Robbi 2026); siklus hidup per pkm','Tidak',KUR,'Skala nasional bersumber dan jumlah bus yang diganti sampai 2030.','R23'),
('Penggunaan akhir','LPG ke kompor induksi','LPG ke kompor induksi',None,None,'Tidak ada','Skala 1 butir','Faktor LPG ASUMSI penulis, belum bersumber','Tidak',BEL,'Faktor emisi LPG bersumber dan jumlah rumah tangga.','R16'),
('Penggunaan akhir','Rice cooker','Rice cooker',None,None,'Tidak ada','Skala 2 butir','Tidak ada','Tidak',KUR,'Faktor emisi listrik pengganti dan jumlah unit; program kecil.','R16'),
('Pertanian','Sawah AWD (pengeringan berkala)','Sawah AWD (pengeringan berkala)',None,None,'Tidak ada','Tidak ada','Tidak ada','Tidak',BEL,'Luas sawah AWD dan faktor CH4 bersumber.','R24'),
('Limbah','PLTSa (sampah menjadi listrik)','Pengolahan sampah menjadi listrik (PLTSa)',None,None,'Tidak ada','Tidak ada; RUPTL memuat PLTSa','Tidak ada','Tidak',BEL,'Kapasitas PLTSa dan faktor emisi sampah bersumber.','R24'),
('Pembanding','PLTU batubara baru (acuan)','PLTU batubara baru (acuan)',None,None,'Tidak berlaku','Acuan biaya dan emisi','Sumber faktor 0,96 kgCO2 per kWh','Tidak',PEM,'Acuan perhitungan; bukan solusi.',''),
('Pembanding','PLTG siklus tunggal','PLTG siklus tunggal',None,None,'Tidak berlaku','Acuan','Tidak ada','Tidak',PEM,'Acuan; bukan solusi.',''),
('Pembanding','CCGT','CCGT',None,None,'Tidak berlaku','Acuan','Tidak ada','Tidak',PEM,'Acuan; bukan solusi.',''),
]
cat=collections.Counter(x[9] for x in R)
print(len(R),dict(cat))
# ---------- build sheet ----------
H=['No','Sektor','Solusi','Lapis A rendah (MtCO2e)','Lapis A tinggi (MtCO2e)','Lapis B rendah (MtCO2e)','Lapis B tinggi (MtCO2e)','Asal angka pengurangan','Skala atau potensi bersumber','Faktor emisi bersumber','Parameter teknis di D_Teknis_Opsi','Berstatus R','Berstatus E','Deret tahunan di C_Deret_Opsi','Kesiapan','Masukan yang kurang atau catatan','Rujukan riset']
cols='<cols><col min="1" max="1" width="3" customWidth="true"/><col min="2" max="2" width="5" customWidth="true"/><col min="3" max="3" width="14" customWidth="true"/><col min="4" max="4" width="36" customWidth="true"/><col min="5" max="8" width="12" customWidth="true"/><col min="9" max="11" width="34" customWidth="true"/><col min="12" max="13" width="10" customWidth="true"/><col min="14" max="14" width="22" customWidth="true"/><col min="15" max="15" width="18" customWidth="true"/><col min="16" max="16" width="60" customWidth="true"/><col min="17" max="17" width="12" customWidth="true"/></cols>'
rows=[]
rows.append(row(1,[istr('A1',2,'Lembar 97. Audit kesiapan semua solusi alternatif: apakah ada skala dan faktor emisi bersumber untuk membuat lembar teknis dan grafik pengurangan emisi')]))
rows.append(row(2,[istr('A2',2,'Aturan: hanya angka bersumber dan hitungan sederhana (kali, bagi, jumlah, konversi satuan). Tidak ada proyeksi statistik, ekstrapolasi, atau ukuran sebesar sisa selisih. Solusi hanya mendapat lembar setelah data kajian tersedia. Status R/E dihitung dari D_Teknis_Opsi dengan COUNTIFS.')]))
order=[SIAP,HIT,KUR,BEL,PEN,PEM,BUK]
r3='"Temuan utama: dari "&COUNTA(D8:D%d)&" solusi, siap "&COUNTIF(P8:P%d,"Siap")&", siap setelah hitung ulang "&COUNTIF(P8:P%d,"Siap setelah hitung ulang")&", kurang masukan "&COUNTIF(P8:P%d,"Kurang masukan")&", belum bisa "&COUNTIF(P8:P%d,"Belum bisa")&"; sisanya pendukung, pembanding, atau residual."'
last=8+len(R)
v3=f'Temuan utama: dari {len(R)} solusi, siap {cat[SIAP]}, siap setelah hitung ulang {cat[HIT]}, kurang masukan {cat[KUR]}, belum bisa {cat[BEL]}; sisanya pendukung, pembanding, atau residual.'
rows.append(row(3,[fml('A3',2,r3.replace('%d','XX').replace('XX',str(last)) if False else r3%(last,last,last,last,last),v3)]))
rows=rows[:3]
rows.append(row(5,[istr('B5',19,'Tabel 97.A. Kesiapan tiap solusi (rujukan: C_Solusi_2030, D_Teknis_Opsi, C_Deret_Opsi, D_RUPTL_Tambahan, D_Faktor)')]))
rows.append(row(7,[istr(f'{c}7',23,h) for c,h in zip('BCDEFGHIJKLMNOPQR',H)]))
def cell(ref): 
    v=csv.get(ref); return v
for k,(sek,sol,dn,A,B,asal,skala,fe,der,kes,kur,rj) in enumerate(R):
    r=8+k; cs_=[num(f'B{r}',62,k+1),istr(f'C{r}',24,sek),istr(f'D{r}',24,sol)]
    for col,pair,idx in (('E',A,0),('F',A,1),('G',B,0),('H',B,1)):
        if pair:
            ref0=pair[idx]; ref=chr(ord(ref0[0])+1)+ref0[1:]; v=cell(ref)
            if isinstance(v,(int,float)): cs_.append(fml(f'{col}{r}',25,f"C_Solusi_2030!{ref}",v))
            else: cs_.append(istr(f'{col}{r}',24,'' if v is None else str(v)))
        else: cs_.append(istr(f'{col}{r}',24,''))
    cs_+=[istr(f'I{r}',24,asal),istr(f'J{r}',24,skala),istr(f'K{r}',24,fe)]
    if dn:
        cs_+=[fml(f'L{r}',62,f'COUNTIFS(D_Teknis_Opsi!$C$6:$C$318,"{dn}")',cnt[(dn,'all')]),
              fml(f'M{r}',62,f'COUNTIFS(D_Teknis_Opsi!$C$6:$C$318,"{dn}",D_Teknis_Opsi!$I$6:$I$318,"R")',cnt[(dn,'R')]),
              fml(f'N{r}',62,f'COUNTIFS(D_Teknis_Opsi!$C$6:$C$318,"{dn}",D_Teknis_Opsi!$I$6:$I$318,"E")',cnt[(dn,'E')])]
    else: cs_+=[istr(f'L{r}',24,'0'),istr(f'M{r}',24,'0'),istr(f'N{r}',24,'0')]
    cs_+=[istr(f'O{r}',24,der),istr(f'P{r}',24,kes),istr(f'Q{r}',24,kur),istr(f'R{r}',24,rj)]
    rows.append(row(r,cs_))
# fix header col mapping: header list H has 17 items B..R
rows=[x for x in rows]
rows.append(row(last+2,[istr(f'B{last+2}',19,'Tabel 97.B. Arti kategori kesiapan')]))
leg=[(SIAP,'Skala atau potensi dan faktor emisi bersumber ada; lembar dapat dibangun dengan hitungan sederhana.'),
(HIT,'Ada angka pengurangan tetapi bukan bersumber (sisa selisih); lembar menunggu hitung ulang dari kapasitas bersumber.'),
(KUR,'Satu atau lebih masukan bersumber belum tercatat; lembar menunggu data kajian (lihat kolom Rujukan riset).'),
(BEL,'Belum ada data skala atau faktor; tidak dibuat sampai kajian tersedia.'),
(PEN,'Tidak mengurangi emisi sendiri; hanya muncul sebagai pendamping di lembar lain.'),
(PEM,'Acuan biaya atau emisi; bukan solusi.'),
(BUK,'Residual atau bagian resmi yang tidak dirinci; bukan teknologi.')]
for q,(a,b) in enumerate(leg):
    r=last+3+q; rows.append(row(r,[istr(f'C{r}',24,a),fml(f'D{r}',62,f'COUNTIF($P$8:$P${last},C{r})',cat[a]),istr(f'E{r}',24,b)]))
sx=sheet_xml(rows,cols,f'A1:R{last+10}',merges=[f'E{last+3+q}:L{last+3+q}' for q in range(7)])
# header columns: H has 17 labels for B..R
sx=sx.replace('<c r="B7"','<c r="B7"')  # no-op
add_sheets(P,[('A_Kesiapan_Solusi',sx,None)],[(97,'A_Kesiapan_Solusi','Catatan','Audit kesiapan semua solusi alternatif: skala, faktor emisi, deret tahunan, dan masukan yang kurang','D_Teknis_Opsi, C_Solusi_2030, C_Deret_Opsi')])
print('done')
