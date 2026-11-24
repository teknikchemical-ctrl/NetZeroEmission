"""Catat temuan pembacaan ulang sumber berkedalaman B dan C (24 Nov 2026): butir D_Register_Sumber 898 dan seterusnya, K164 sampai K166. Tiap angka diperiksa pada teks PDF."""
import re,zipfile,sys,glob,os,csv
sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from xlsxkit import istr,num
P=sys.argv[1] if len(sys.argv)>1 else '/tmp/claude-0/base_model.xlsx'
E='Status E (eksternal), tidak dijumlahkan dengan CM1 atau CM2 resmi. '
def norm(t): return re.sub(r'[\s­,.]','',t.replace('\u2212','-').replace('\u2013','-'))
TXT={os.path.basename(p)[:-4]:norm(open(p,encoding='utf8',errors='ignore').read()) for p in glob.glob('/tmp/claude-0/alltxt/*.txt') if not p.endswith('.lay.txt')}
ER=None
def has(stem,*vals):
    t=''.join(v for k,v in TXT.items() if k.startswith(stem))
    return [x for x in vals if norm(x) not in t]
# CSV Squire
EP=' Status E (eksternal), tidak dijumlahkan dengan CM1 atau CM2 resmi.'
KA='RUPTL dan investasi PLTN (Kanugraha 2025)'
NB='Dilema bauran energi Indonesia menuju NZE (Nasir dan Bengi 2024)'
GS='Green sukuk dan energi terbarukan (Aminin dan Khayati 2025)'
JE='Implementasi Just Energy Transition Partnership di Indonesia (artikel 2024)'
DH='Rehabilitasi hutan dan lahan 2015 sampai 2019 dan target FOLU (Dharmawan dan Pratiwi 2023)'
PD='Evaluasi emisi PLTU batubara dan pensiun dini (Prabowo dan Dalimi 2026)'
MK='Bursa karbon IDXCarbon (Mukti dkk. 2025)'
EF='Efektivitas FOLU Net Sink (Irwanto 2025)'
SB='Reaktualisasi FOLU Net Sink 2030 (Subekti dan Aristawidya 2025)'
MA='Ancaman deforestasi terhadap NZE (Maulida dkk. 2025)'
AR='Kerangka kebijakan dan realisasi NZE, tolok ukur LCOE IESR (Ardiansyah, Wahyuni, Ekadewi 2024, J. Phys. Conf. Ser. 2828)'
SUS='Pertumbuhan ekonomi, deforestasi dan emisi CO2, model koreksi galat (Susilo dkk. 2026)'
RI='Gap analysis rencana kerja FOLU Net Sink Riau, Semenanjung Kampar dan Kerumutan (Nursamsu dkk. 2024, Paradigma)'
AM='Kerangka hukum dan kebijakan listrik menuju NZE (Amalia dkk. 2024)'
AY='Faktor penyumbang emisi CO2 Indonesia 1970 sampai 2023 (Aminy dkk. 2025, Narra X 3(3))'
IR='Peran IRENA dalam ketahanan energi (Luthfiani 2024)'
CI='Surya terapung Cirata (Kibtiah dkk. 2024; Sudarwanto dan Daryanti 2025)'
rows=[
(KA,'Hlm. 2480 dan pendahuluan','Tambahan kapasitas RUPTL 2025 sampai 2034 menurut jenis','Total 69,5 GW: EBT 42,6 GW (61 persen), penyimpanan 10,3 GW, fosil 16,6 GW (gas 10,3 dan batubara 6,3); surya 17,1, hidro 11,7, angin 7,2, panas bumi 5,2, bioenergi 0,9, nuklir 0,5 GW','GW',EP+' Ringkasan narasi; total jenis mendekati jumlah pipeline proyek di G_Data_Sumber (PLTS 17,6; PLTB 7,8; panas bumi 5,3 GW), jadi K163 lebih mungkin soal periode agregat 2025 sampai 2030 daripada selisih data.','2025_Kanugraha',('69,5','42,6','10,3','17,1','11,7','7,2','5,2')),
(KA,'Bagian investasi','Investasi satu PLTN menurut kajian','USD 5 sampai 10 miliar; konstruksi 8 sampai 12 tahun','USD miliar; tahun',EP+' Klaim hukum-investasi (rujukan 21); sejalan dengan USD 5,8 sampai 8,7 juta per MW (IEEFA).','2025_Kanugraha',('5','10','8','12')),
(NB,'Tabel jalan peta DEN (hlm. 103 sampai 104)','Sasaran pengurangan emisi 2025, 2035, 2050 dan syarat pendukung','Pengurangan 231,2 MtCO2e (2025); 388 (2035); 1.043,8 (2050). Kompor induksi: 8,1 juta (2025), 28,2 juta (2035), 46,6 juta rumah tangga (2050). Mobil listrik 300 ribu, 9,3 juta, 50,2 juta; motor listrik 1,3 juta, 51 juta, 163 juta. Jaringan gas rumah tangga 5,2; 15,2; 22,7 juta. Biofuel 40 persen (2035 dan 2050), B30 wajib 2025; panas bumi 11 GW (2035)','MtCO2e; juta rumah tangga; juta unit',EP+' Dikutip dari DEN 2023. Jumlah rumah tangga induksi mengisi celah skala untuk opsi LPG ke induksi (A_Kesiapan: kurang masukan); listrik induksi per rumah tangga belum ada. Verifikasi pada edisi DEN asli.','The_energy_mix',('231.2','388','1,043.8','8.1 million','28.2 million','46.6 million','50.2 million','163 million','15.2 million')),
(NB,'Pendahuluan','Konsumsi energi 2022','1,18 miliar BOE, naik 28,31 persen dari 924,19 juta BOE; bauran EBT sekitar 17 persen pada 2025 dibanding target 23 persen','BOE; persen',EP,'The_energy_mix',('1.18 billion','28.31','924.19')),
(GS,'Pembahasan pembiayaan','Kebutuhan dan realisasi pembiayaan iklim','Kesenjangan investasi USD 146,4 miliar sampai 2030; kebutuhan USD 20 sampai 40 miliar per tahun sampai 2050; belanja iklim 2016 sampai 2022 Rp569 triliun (Rp81,3 triliun per tahun; 3,5 persen APBN); green sukuk global pertama 2018 USD 1,25 miliar','USD miliar; Rp triliun',EP+' Sekunder; tidak untuk menghitung biaya selisih 2060.','3.Artikel',('146.4','569','81.3','1.25')),
(JE,'Bagian pendanaan dan target','JETP: dana dan target','USD 20 miliar (publik USD 10 miliar dari IPG); VRE dari sekitar 1 persen ke 14 persen (2030) dan 25 persen (2040) bauran terbarukan; emisi CO2 energi 696,7 juta ton (naik 4,1 persen; IESR 2023); target energi NDC pertama 314 sampai 446 juta ton','USD miliar; persen; MtCO2',EP,'Implementasi_Just',('20','14%','25%','696,7','4,1','314','446')),
(DH,'Tabel 1 (hlm. 3)','Rehabilitasi hutan dan lahan 2015 sampai 2019 per tahun','200.447; 198.346; 200.990; 188.630; 395.168 ha; target RPJMN 2020 sampai 2024 420.000 ha per tahun','ha',EP+' Jumlah lima tahun 1.183.581 ha (sama dengan butir sebelumnya).','Implementation_of_forest',('200,447','198,346','200,990','188,630','395,168','420,000')),
(EF,'Bagian pendahuluan dan hasil','Capaian FOLU 2020 sampai 2024 (tinjauan pustaka)','Deforestasi neto sekitar 104.000 ha (2022) dibanding rata-rata 450.000 ha per tahun (2010 sampai 2015); restorasi gambut 1,7 juta ha sejak 2016; mangrove 3,36 juta ha (rehabilitasi 600.000 ha sampai 2024); restorasi hidrologi gambut menurunkan potensi emisi 30 sampai 60 persen; kebutuhan pendanaan iklim USD 281 miliar (OECD 2022)','ha; persen; USD miliar',EP+' Rujukan sekunder (KLHK 2023, OECD 2022); faktor 30 sampai 60 persen bergantung pemulihan muka air.','Analysis_of_The_Effectiveness',('104,000','450,000','1.7 million','3.36 million','30–60','281')),
(PD,'Tabel 2 (hlm. 322 sampai 323)','Armada PLTU menurut teknologi (baseline 318 unit, 71,63 GW)','Subkritis 177 unit 28.675 MW (39 persen); superkritis 30 unit 14.545 MW (19,8 persen); ultra-superkritis 11 unit 10.121 MW (13,8 persen); tanpa klasifikasi 20.189 MW (27,4 persen); 20 unit menyumbang hampir seperempat emisi','unit; MW',EP+' Teks sesuai 14.545 MW; tabel yang dikutip tim menulis 12.645 (K152).','Evaluation_of_Coal',('28,675','14,545','10,121','20,189','177')),
(MK,'PDF hlm. 6','Bursa karbon sejak peluncuran','Unit terdaftar 1.349.894 tCO2e; transaksi kumulatif 908.018 tCO2e senilai Rp50,64 miliar; potensi pasar karbon diperkirakan USD 300 miliar per tahun (klaim)','tCO2e; Rp miliar',EP+' Klaim potensi USD 300 miliar tidak bersumber primer; jangan dipakai.','Bursa_Karbon',('1,349,894','908,018','50.64')),
(SB,'Bagian pendahuluan','Deforestasi 2012 sampai 2030 menurut kebijakan','Total tertulis 7,27 juta ha, terdiri 5,32 juta ha terencana dan 5,15 juta ha tidak terencana (jumlah komponen 10,47)','juta ha',EP+' Ketidakkonsistenan internal (K165). FWI: kehilangan hutan 1,47 juta ha per tahun 2013 sampai 2021; food estate Merauke dan lain-lain 2.684.680,68 ha.','Reaktualisasi',('7,27','5,32','5,15','1,47','2.684.680')),
(MA,'Bagian kebijakan','Capaian deforestasi menurut pemerintah (klaim)','Dari 460.000 ha (2018 sampai 2019) ke 120.000 ha (2019 sampai 2020); ENDC 31,89 persen dan 43,20 persen; kebutuhan investasi NDC Rp3.799 triliun (Adi 2023)','ha; persen; Rp triliun',EP,'Ancaman',('460,000','120,000','31,89','43,20','3,799')),
(AR,'Bagian potensi','Potensi panas bumi dalam makalah','23,9 GW (rujukan 14)','GW',EP+' Berbeda dengan 29,5 GW (Pambudi dan Ulfa; IETO 2022); K164.','Bridging',('23.9',)),
(SUS,'Tabel 4 sampai 6','Model koreksi galat CO2 2004 sampai 2023','R2 terkoreksi 0,615632; koefisien koreksi galat 0,8012; probabilitas pertumbuhan 0,7377 dan deforestasi 0,1251 (tidak signifikan individual)','statistik',EP+' Hasil statistik; tidak memberi faktor emisi per hektare dan tidak dipakai di model.','2026_Susilo',('0.615632','0.7377','0.1251')),
(RI,'Tabel 1 (hlm. 2 sampai 3)','Rencana aksi mitigasi di lanskap Kampar dan Kerumutan (ha)','Jumlah Kampar 625.940,11 dan Kerumutan 969.469,22 (total 1.595.409,33 ha; 27,95 persen target Renja FOLU Net Sink Riau). RO 2: 310.668,52 dan 144.713,00; RO 9: 243.354,70 dan 537.880,47; RO 10: 59.241,98 dan 171.672,55; RO 11: 247,01 dan 59.795,29; RO 12: 2.136,55 dan 13.076,36','ha',EP+' Analisis spasial Paradigma 2024 dari SIGAP KLHK; luas rencana, bukan realisasi. RO 3 dan RO 6 berbeda label dengan manual BRGM.','Kajian',('625,940','969,469','1,595,409','27,95','310,668','537,880','171,672')),
(AM,'Bagian analisis','Rencana PLTU dan bauran dalam peraturan','Tambahan PLTU 31,9 GW (43 persen dari kapasitas PLTU eksisting menurut RUPTL); EBT 51,6 persen dari tambahan RUPTL 2021 sampai 2030; target 2050: EBT paling sedikit 31 persen, batubara paling sedikit 25 persen, gas 24 persen','GW; persen',EP+' Konteks hukum; angka dari RUEN dan RUPTL lama.','2024_Amalia',('31.9','51.6','43%')),
(AY,'Hasil','Emisi CO2 historis Indonesia (OWID)','Sekitar 646.198.262 t dari 18.072.177.361 t global (sekitar 3 persen); puncak 1997 2,70 x 10^9 t; 1983 3,37 x 10^8 t ke 1984: teks 1,18 x 10^9 t, gambar 1,08 x 10^9 t','t CO2',EP+' Ketidakkonsistenan teks dan gambar (K166).','2025_Aminy',('646,198,262','18,072,177,361')),
(CI,'Bagian PLTS','Angka PLTS dan potensi (Kibtiah dkk. 2024)','PLTS 5.000 MW sekitar Rp165 triliun; potensi angin 60 GW; potensi EBT 400 GW dengan pemanfaatan sekitar 2,1 persen; investasi AS USD 9,4 miliar (2018 sampai kuartal 1 2023); Cirata dalam makalah lain disebut 16 MW','Rp triliun; GW',EP+' Angka potensi sekunder; Cirata 145 MW dibanding 16 MW di Artikel Hukum Lingkungan.','Solar_Energy',('165','60 GW','400 GW','2.1%','9.4')),
(IR,'Bagian kerja sama','Kerja sama IRENA','Dukungan pendanaan USD 4 miliar; 185.662 rumah tangga dan 140 desa belum berlistrik (target 100 persen 2024)','USD miliar; rumah tangga',EP+' Konteks; tidak dipakai di model.','Energy_Security',('185,662','140 villages')),
]
bad=[(r[2][:50],has(r[6],*r[7])) for r in rows if r[6] and has(r[6],*r[7])]
print('belum ditemukan pada teks PDF:',bad)
if '--strict' in sys.argv: assert not bad
conf=[
('K164','Potensi panas bumi Indonesia','GW',29.5,'Pambudi dan Ulfa 2024 (IETO 2022)',23.9,'Ardiansyah dkk. 2024 (rujukan 14)',None,None),
('K165','Deforestasi 2012 sampai 2030 menurut kebijakan','juta ha',7.27,'Subekti dan Aristawidya 2025 (total tertulis)',10.47,'Jumlah komponen 5,32 + 5,15 pada makalah yang sama',None,None),
('K166','Emisi CO2 Indonesia 1984','tCO2 (x10^9)',1.18,'Aminy dkk. 2025 teks',1.08,'Aminy dkk. 2025 gambar 1',None,None),
]
RA='customFormat="false" ht="35.05" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
RA2='customFormat="false" ht="23.85" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
N0=897; L0=N0+5; L1=L0+len(rows); N1=N0+len(rows)
docs_old=55; docs_new=4
KN0=163; KN1=KN0+len(conf)
zi=zipfile.ZipFile(P); items=[(i,zi.read(i.filename)) for i in zi.infolist()]; zi.close()
zo=zipfile.ZipFile(P,'w',zipfile.ZIP_DEFLATED)
for it,d in items:
    n=it.filename
    if n=='xl/worksheets/sheet88.xml':
        s=d.decode('utf8'); out=''
        assert f'D6:D{L0}' in s and f'Temuan utama: {N0} butir dari {docs_old} dokumen' in s
        for k,(a,b,c,e,f,g,stem,cek) in enumerate(rows):
            rr=L0+1+k
            out+=f'<row r="{rr}" {RA}>'+num(f'A{rr}',164,N0+1+k)+istr(f'B{rr}',39,a)+istr(f'C{rr}',39,b)+istr(f'D{rr}',39,c)+istr(f'E{rr}',39,e)+istr(f'F{rr}',39,f)+istr(f'G{rr}',39,g)+'</row>'
        s=s.replace('</sheetData>',out+'</sheetData>').replace(f'D6:D{L0}',f'D6:D{L1}').replace(f'B6:B{L0}',f'B6:B{L1}').replace(f'A1:L{L0}',f'A1:L{L1}').replace(f'A5:G{L0}',f'A5:G{L1}')
        s=s.replace(f'Temuan utama: {N0} butir dari {docs_old} dokumen',f'Temuan utama: {N1} butir dari {docs_old+docs_new} dokumen'); d=s.encode('utf8')
    elif n in ('xl/worksheets/sheet3.xml','xl/worksheets/sheet4.xml','xl/worksheets/sheet5.xml'):
        s=d.decode('utf8')
        s=s.replace(f'COUNTA(D_Register_Sumber!D6:D{L0})</f><v>{N0}</v>',f'COUNTA(D_Register_Sumber!D6:D{L1})</f><v>{N1}</v>').replace(f'D_Register_Sumber!B6:B{L0}',f'D_Register_Sumber!B6:B{L1}')
        s=s.replace('COUNTA(K_Konflik!A5:A142)</f><v>138</v>',f'COUNTA(K_Konflik!A5:A{142+len(conf)})</f><v>{138+len(conf)}</v>')
        d=s.encode('utf8')
    elif n=='xl/worksheets/sheet7.xml':   # K_Konflik
        s=d.decode('utf8')
        i=s.find('<row r="145"'); j=s.find('</row>',i)+6; assert i>0
        note=s[i:j]; sh=len(conf)
        for c in 'ABCDEF': note=note.replace(f'{c}145',f'{c}{146+sh}')
        note=note.replace('r="145"',f'r="{146+sh}"'); s=s[:i]+s[j:]
        out=''
        for k,(idv,q,u,v1,s1,v2,s2,v3,s3) in enumerate(conf):
            r=143+k
            c=istr(f'A{r}',39,idv)+istr(f'B{r}',39,q)+istr(f'C{r}',39,u)+num(f'D{r}',62,v1)+istr(f'E{r}',39,s1)+num(f'F{r}',62,v2)+istr(f'G{r}',39,s2)
            c+=(num(f'H{r}',62,v3)+istr(f'I{r}',39,s3)) if v3 is not None else f'<c r="H{r}" s="39"/><c r="I{r}" s="39"/>'
            c+=f'<c r="J{r}" s="39"/><c r="K{r}" s="39"/>'+istr(f'L{r}',39,'Dicatat, belum dianalisis')
            out+=f'<row r="{r}" {RA2}>'+c+'</row>'
        s=s.replace('</sheetData>',out+note+'</sheetData>').replace('A1:L145',f'A1:L{146+sh}').replace('A145:F145',f'A{146+sh}:F{146+sh}')
        d=s.encode('utf8')
    elif n=='xl/sharedStrings.xml':
        s=d.decode('utf8'); assert 'K25 sampai K163' in s; d=s.replace('K25 sampai K163',f'K25 sampai K{KN1}').encode('utf8')
    zo.writestr(it,d)
zo.close(); print('register',N1,'dokumen',docs_old+docs_new,'konflik sampai',KN1)
