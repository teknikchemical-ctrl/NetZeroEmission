"""Catat isi cabang research/nze-data-handoff (tim, 24 Nov 2026) pada berkas base setelah 14 dan 15:
butir baru D_Register_Sumber (nomor 843 dan seterusnya), konflik K147 sampai K153, jumlah dan teks ringkasan.
Setiap angka diperiksa terhadap teks PDF di /tmp/claude-0/alltxt (hasil pdftotext) atau berkas CSV sebelum ditulis."""
import re,zipfile,sys,glob,os,csv
sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from xlsxkit import istr,num
P=sys.argv[1] if len(sys.argv)>1 else '/tmp/claude-0/base_model.xlsx'
E='Status E (eksternal), tidak dijumlahkan dengan CM1 atau CM2 resmi. '
def norm(t): return re.sub(r'[\s­,.]','',t.replace('\u2212','-').replace('\u2013','-'))
TXT={os.path.basename(p)[:-4]:norm(open(p,encoding='utf8',errors='ignore').read()) for p in glob.glob('/tmp/claude-0/alltxt/*.txt') if not p.endswith('.lay.txt')}
def has(stem,*vals):
    t=''.join(v for k,v in TXT.items() if k.startswith(stem))
    return [x for x in vals if norm(x) not in t]
# CSV Squire
def sq():
    r=list(csv.reader(open('/home/user/NetZeroEmission/sources/2024_Squire-dkk_Emisi-Skenario-Co-firing.csv',encoding='utf-8-sig')))
    return {x[0]:[float(v) for v in x[1:12]] for x in r[1:6]}
S=sq(); d30={k:S['BAU'][-1]-S[k][-1] for k in ('Low','Equalized','Mid','High')}
def fmt(x,n=3): return f'{x:,.{n}f}'.replace(',','_').replace('.',',').replace('_','.')
prov=list(csv.reader(open('/home/user/NetZeroEmission/sources/2024_Squire-dkk_Biomassa-Provinsi.csv',encoding='utf-8-sig')))
pt=sum(float(r[-1]) for r in prov[1:] if r[0].strip())/1e9
SQ='Kelayakan co-firing limbah biomassa (Squire, Lou, Hilde 2024, Communications Earth and Environment 5:423)'
PD='Evaluasi emisi PLTU batubara dan pensiun dini (Prabowo dan Dalimi 2026)'
GU='Transisi batubara ke EBT, model sistem BPS DPS CPS (Gulagi dkk. 2025, IET Renewable Power Generation)'
AR='Kerangka kebijakan dan realisasi NZE, tolok ukur LCOE IESR (Ardiansyah, Wahyuni, Ekadewi 2024, J. Phys. Conf. Ser. 2828)'
CI='Surya terapung Cirata (Kibtiah dkk. 2024; Sudarwanto dan Daryanti 2025)'
JE='Implementasi Just Energy Transition Partnership di Indonesia (artikel 2024)'
MK='Bursa karbon IDXCarbon (Mukti dkk. 2025)'
CP='Kebijakan penetapan harga karbon (Nurhayati dkk.)'
GS='Green sukuk dan energi terbarukan (Aminin dan Khayati 2025)'
DH='Rehabilitasi hutan dan lahan 2015 sampai 2019 dan target FOLU (Dharmawan dan Pratiwi 2023)'
HU='Pelestarian lahan basah, kinerja 2023 (Husain dan Korbaffo 2024)'
MA='Ancaman deforestasi terhadap NZE (Maulida dkk. 2025)'
SU='Reaktualisasi FOLU Net Sink 2030 (Subekti dan Aristawidya 2025)'
NB='Dilema bauran energi Indonesia menuju NZE (Nasir dan Bengi 2024)'
ER='ERIA CCS thermal (Sumitomo/ERIA 2025)'
# (dokumen,tabel,butir,nilai,satuan,catatan,stem,cek)
rows=[
(SQ,'Berkas CSV penulis (Gambar 2)','Emisi CO2 PLTU 2030 menurut skenario co-firing',f'BAU {fmt(S["BAU"][-1])}; Rendah {fmt(S["Low"][-1])}; Setara {fmt(S["Equalized"][-1])}; Menengah {fmt(S["Mid"][-1])}; Tinggi {fmt(S["High"][-1])}','MtCO2 per tahun',E+'Berkas sources/2024_Squire-dkk_Emisi-Skenario-Co-firing.csv, deret 2020 sampai 2030; semua skenario sama sampai 2023 (277,723). Emisi pembangkit model, tanpa emisi hulu biomassa. Catat dari tim (cabang codex), diperiksa langsung pada berkas.',None,()),
(SQ,'Berkas CSV penulis (hitungan)','Selisih emisi PLTU 2030 terhadap BAU',f'Rendah {fmt(d30["Low"])}; Setara {fmt(d30["Equalized"])}; Menengah {fmt(d30["Mid"])}; Tinggi {fmt(d30["High"])}','MtCO2 per tahun','Status AC (BAU dikurangi skenario). Rendah dan Tinggi sama dengan 14,2 dan 152,5 pada butir Gambar 6 (K125); dua skenario tengah sebelumnya belum tercatat. Bukan bagian CM1 atau CM2.',None,()),
(SQ,'Berkas CSV penulis, Biomassa-Provinsi','Pasokan limbah biomassa nasional (jumlah 34 provinsi)',f'{fmt(pt)}','miliar MJ per tahun','Status AC (jumlah kolom Total). Cocok dengan 504,4 pada Tabel 1 (butir sebelumnya), sehingga pasokan di S_Cofiring tervalidasi dua arah. Per jenis (miliar MJ): kayu limbah 69,76; sekam 107,34; karet 151,34; MSW 68,88; EFB 47,17; bagas 44,23; PKS 8,91; jerami 6,78.',None,()),
(PD,'Tabel 1 (hlm. 321)','Cakupan armada PLTU batubara (GEM, Februari 2026)','Semua status 526 unit 127,68 GW; garis dasar 318 unit 71,63 GW; operasi 287 unit 60,705 GW','unit; GW',E+'Termasuk pembangkit captive; cakupan berbeda dengan proyeksi RUPTL dan batas JETP.','Evaluation_of_Coal',('526','127.68','318','71.63','287')),
(PD,'Tabel 3 (hlm. 323 sampai 324)','Emisi kumulatif PLTU sampai 2045 tanpa pensiun dipercepat','7.892,143 MtCO2 kumulatif; setara 394,607 MtCO2 per tahun (20 tahun)','MtCO2',E+'Tabel 3 tidak memuat 2032 dan 2033 serta mengulang 2034 dan 2035; selisih 2037 dan 2038 (590,296 dan 205,516) tidak konsisten dengan narasi sekitar 394 per tahun. Jangan impor deret per tahun.','Evaluation_of_Coal',('7892.143',)),
(PD,'Tabel 2','Kapasitas superkritis: tabel dibanding teks','Tabel 12.645 MW; teks 14.545 MW','MW',E+'Ketidakkonsistenan internal makalah; dicatat K152.','Evaluation_of_Coal',('12645','14545')),
(PD,'Tabel 5 (hlm. 326)','Tanjung Jati B unit 5 dan 6: kapasitas dan emisi','1.000 MW dan 4,702 MtCO2 per tahun per unit; dua unit 9,404','MW; MtCO2 per tahun',E+'COD 2022 dan emisi sama dengan estimasi GEM di D_GEM_ID (4,702326), jadi pemeriksaan silang atas estimasi, bukan emisi terukur. Jumlah dua unit (9,404, AC) lebih kecil dari tangkapan kotor 13 Mt pada ERIA (K150).','Evaluation_of_Coal',('4.702',)),
(GU,'Bagian 3.3 (hlm. 9 sampai 12)','Kapasitas transfer antarwilayah 2050','BPS 158 GW; DPS 107 GW; CPS 22 GW; Sumatera ke Jawa 52 GW (BPS) dan 30 GW (DPS)','GW',E+'Sensitivitas jaringan model; tidak dapat memberi biaya sambungan tingkat tapak untuk surya B6 atau B7.','Accelerating',('158','107','52','30')),
(GU,'Bagian 3.6 (hlm. 15 sampai 16)','Biaya listrik tersedia 2050','BPS 37; DPS 41; CPS 87','EUR per MWh',E+'Biaya sistem model termasuk harga karbon model; perbedaan antar jalur juga mencerminkan permintaan, aset, dan bahan bakar berbeda.','Accelerating',('37€/MWh','41€/MWh','87€/MWh')),
(GU,'Pembahasan (hlm. 17 sampai 18)','Aset batubara terdampar 2045 dan penambahan surya per tahun','53 GW kapasitas terdampar bernilai 26 miliar USD (kasus bersyarat 14 GW pipeline tetap dibangun); surya 7 sampai 10 GW per tahun dekade pertama dan 59 sampai 68 GW per tahun dekade terakhir; biaya 15 persen lebih tinggi tanpa tautan antarpulau','GW; miliar USD',E+'Kasus 37,47 GW surya di B7 setara 7,49 GW per tahun pada jendela lima tahun (AC), di dalam rentang dekade pertama makalah. CCS tidak masuk bauran biaya terendah model.','Accelerating',('53 GW','26','59','68','15%')),
(AR,'Tabel 1 (hlm. 3) dan Tabel 2 (hlm. 6 sampai 7)','Tolok ukur teknologi pembangkit, kalkulator LCOE IESR 2023','Batubara 1.400 sampai 1.650 USD per kW, CF 70, 6,04 sen per kWh, 820 g CO2e per kWh; panas bumi 4.000 sampai 5.000, CF 80, 6,79 (besar) dan 8,53 (kecil), 38 g; surya 790 sampai 1.320, CF 18 sampai 19, 5,79 (utilitas) dan 9,76 (atap), 48 dan 41 g; nuklir 4.300, CF 85, 10,16, 12 g','USD per kW; persen; sen USD per kWh; g CO2e per kWh',E+'Faktor siklus hidup dari nilai global IPCC AR5. Biaya pengurangan layar (AC, selisih LCOE dibagi selisih intensitas): panas bumi besar 9,59 dan kecil 31,84; surya utilitas -3,24; surya atap 47,75; nuklir 50,99 USD per tCO2e; batas siklus hidup berbeda dengan inventaris nasional.','Bridging',('4000','5000','790','1320','1400','1650','6.04','10.16','820')),
(CI,'Kibtiah dkk. 2024 bagian 5.2; Sudarwanto dan Daryanti 2025 hlm. 7','PLTS terapung Cirata','145 MW; investasi 129 juta USD; proyeksi 250 GWh per tahun','MW; juta USD; GWh',E+'Hitungan AC: sekitar 0,89 juta USD per MW dan faktor pemanfaatan 19,7 persen dari nilai proyeksi, bukan CF terukur. Cakupan AC atau DC dan biaya sambungan belum dipastikan.','Solar_Energy',('145',)),
(CI,'Sudarwanto dan Daryanti 2025','Nilai investasi dan proyeksi keluaran Cirata (sumber kedua)','129 juta USD; 250 GWh per tahun','juta USD; GWh',E,'Examining_legal',('129','250')),
(JE,'Bagian pembiayaan','Biaya energi terbarukan dispatchable JETP sampai 2030 dan peta jalan jaringan pintar PLN','49,2 miliar USD untuk 16,1 GW; distribusi 2,0, transmisi 0,3 dan sistem kontrol cerdas 0,5 miliar USD','miliar USD; GW',E+'Rasio 3,06 juta USD per MW program campuran sama dengan bagian B D_Opsi_Solusi. Jangan dijumlahkan dengan total transmisi seluruh sistem.','Implementasi_Just',('16,1','49,2','0,5')),
(MK,'PDF hlm. 6','Harga dan volume IDXCarbon 2024','Pasar reguler Rp40.000 sampai Rp80.000 per unit; penutupan Q4 Rp58.800; 413.764 tCO2e; nilai Rp19,73 miliar','IDR; tCO2e',E+'Data pasar sekunder; bukan biaya pengurangan fisik.','Bursa_Karbon',('40.000','58.800','413.764')),
(CP,'Bagian 4 (PDF hlm. 7)','Batas bawah harga karbon dalam UU HPP Pasal 13','Rp30 per kgCO2e (Rp30.000 per tCO2e); saran penulis 10 USD per t','IDR; USD',E+'Konteks kebijakan, bukan biaya pengurangan.','Carbon_Pricing',('30','10')),
(GS,'Kesimpulan; Tabel 3 dan 4','Green sukuk 2018 sampai 2022','Alokasi energi terbarukan 2018 sekitar 110 juta USD; 5.487.041 tCO2 portofolio 2018 sampai 2022; klaim 0,46 persen terhadap ENDC energi','juta USD; tCO2; persen',E+'Pembilang satu tahun terbit dibanding penyebut beberapa kategori dan tahun; 0,46 persen bukan kemajuan terhadap target mitigasi energi.','3.Artikel',('110','5487041','0.46')),
(DH,'Tabel 1 (hlm. 3); Tabel 2 dan Gambar 1 (hlm. 4 sampai 5)','Rehabilitasi 2015 sampai 2019 dan target peningkatan stok karbon FOLU 2022 sampai 2030','1.183.581 ha (236.716 ha per tahun); target 8.255.323 ha: rotasi 5.533.087 ha dan nonrotasi 2.722.236 ha (917.258 ha per tahun)','ha',E+'Target sekitar 3,9 kali laju historis (AC); kategori historis (hutan kota, hutan rakyat, mangrove) tidak sama dengan target.','Implementation_of_forest',('1183581','8255323','5533087','2722236')),
(HU,'hlm. 955 sampai 956','Kinerja lahan basah 2023 (laporan kinerja KLHK)','Pemulihan ekosistem gambut BRGM 271.721 ha di tujuh provinsi; tanam mangrove BRGM 3.064 ha; RHL mangrove KLHK 747 ha','ha',E+'Mengkonfirmasi butir sekunder D_Restorasi_BRGM 2023. Dua baris mangrove menurut lembaga; tumpang tindih belum diperiksa.','Upaya_Pemerintah',('271.721','3.064','747')),
('Efektivitas FOLU Net Sink (Irwanto 2025)','Tabel 1 (hlm. 7)','Capaian kumulatif sampai 2023 (tinjauan pustaka)','Restorasi gambut lebih dari 1,4 juta ha; mangrove 260.000 ha','ha',E+'Basis akumulasi tidak jelas; tabel berakhir 2023; sebagian nilai sementara.','Analysis_of_The_Effectiveness',('260000','1.4')),
(MA,'Bagian proyeksi deforestasi','Deforestasi kumulatif masa depan (LTS-LCCR 2021)','CPOS 14,6 juta ha (486.666 ha per tahun); LCCP 6,8 juta ha (226.666 ha per tahun)','juta ha',E+'Sama dengan D_LTS_LCCR; pembagi 30 tahun adalah anggapan penulis.','Ancaman',('14,6','6,8')),
(SU,'Bagian pendahuluan','Deforestasi 2012 sampai 2030 menurut kebijakan','5,32 juta ha direncanakan; 5,15 juta ha tidak direncanakan; 325.000 ha per tahun','juta ha',E+'Klaim kebijakan; periksa terhadap rencana resmi sebelum dipakai.','Reaktualisasi',('5,32','5,15','325')),
(NB,'Tabel jalan peta (hlm. 104) dan hlm. 103','Rujukan DEN dan biaya transisi','388 MtCO2e pengurangan dan 11 GW panas bumi 2035; 1.043,8 MtCO2e 2050; 994 miliar USD biaya transisi','MtCO2e; GW; miliar USD',E+'Mendahului B40 (memuat B30 2025). Jumlah 994 miliar USD menggabungkan IESR dan DEN tanpa rincian; jangan memakainya untuk biaya selisih 2060.','The_energy_mix',('388','1043.8','994')),
(ER,'Tabel 5.11 dan 5.12; Rekomendasi','Biaya satuan CCS total (USD per tCO2) menurut skala dan rute','Satu unit 6,5 Mt: kapal dan pipa darat 74,0; pipa 92,6. Dua unit 13,0 Mt: kapal 63,7; pipa 72,4. ERIA 2022: 62,8','USD per tCO2',E+'92,6 adalah kasus SATU unit pipa 6,5 Mt, bukan batas atas untuk 13 Mt. Rentang yang sah untuk dua unit 13 Mt adalah 63,7 sampai 72,4 (K147). Diperiksa langsung pada teks Tabel 5.11 dan 5.12 serta Rekomendasi.','2025_ERIA',('63.7','72.4','92.6','74.0')),
]
bad=[(r[2][:50],has(r[6],*r[7])) for r in rows if r[6] and has(r[6],*r[7])]
print('belum ditemukan pada teks PDF:',bad)
if '--strict' in sys.argv: assert not bad
conf=[
('K147','Biaya CCS PLTU TJB per tCO2 pada skala 13 Mt (dua unit)','USD per tCO2',63.7,'ERIA 2025 Tabel 5.11 (kapal dan pipa darat), dua unit 13,0 Mt',72.4,'ERIA 2025 Tabel 5.12 (pipa), dua unit 13,0 Mt',92.6,'D_Opsi_Solusi baris 205 dan C_Solusi_2030 H34 (ini kasus satu unit 6,5 Mt pipa; tidak sah untuk 13 Mt). Belum dikoreksi di judul P_Portofolio, menunggu keputusan'),
('K148','Emisi PLTU batubara 2030','MtCO2',369.49,'Squire dkk. 2024 skenario BAU (CSV penulis)',354,'RUPTL 2025 sampai 2034 RE Base, Tabel 5.175',348,'RUPTL ARED Tabel 5.176; Squire emisi pembangkit model, bukan perkiraan resmi (E)'),
('K149','Biaya restorasi gambut per hektare','USD per ha',400.36,'Renops Tabel 145 dan 146, 2025 sampai 2030 (Rp4,78 triliun per 728.000 ha, kurs 16.400)',445.07,'Renops dua blok pendanaan (Rp9,54 triliun per 1.307.000 ha; periode tidak sejajar)',584.24,'Rossita dan Boer 2025 Tabel 6 (swasta, jenis cepat tumbuh, seluruh komponen); rentang swasta 584,24 sampai 670,06; komunitas 359,19 sampai 379,40'),
('K150','Emisi CO2 PLTU TJB unit 5 dan 6 dibanding tangkapan CCS','MtCO2 per tahun',9.404,'Prabowo dan Dalimi 2026 Tabel 5 (2 x 4,702; estimasi GEM)',13.0,'ERIA 2025 tangkapan kotor desain dua unit (laju 0,95; CF 0,86)',24.01,'Fadiilah dan Dye 2026 Tabel 3 (seluruh enam unit TJB, 2023). Tangkapan 13 Mt melebihi emisi estimasi unit 5 dan 6; asumsi pemanfaatan dan bahan bakar perlu diseragamkan'),
('K151','Pengurangan efisiensi energi yang dilaporkan','MtCO2',30.0,'ESDM via Kabarbursa, 24 April 2026 (periode dan baseline tidak jelas)',31.87,'ESDM via ECCJ, 13 November 2024 (tahun antara tidak berlabel)',132.25,'Sasaran CM1 2030 (slide KESDM 25 Oktober 2023). 22,7 persen adalah 30 dibagi 132,25 (hasil serah terima tim)'),
('K152','Kapasitas PLTU superkritis dalam makalah Prabowo dan Dalimi','MW',12645,'Tabel 2',14545,'Teks makalah',None,None),
('K153','Biaya restorasi mangrove per hektare','USD per ha',1524,'BRGM sekitar Rp25 juta per ha (kurs 16.400; belum diverifikasi, status E)',1870,'BRGM Rp18,4 triliun per 600.000 ha via Mongabay (Rp30,67 juta per ha)',3863,'Bank Dunia 2022 (D_Opsi_Solusi baris 172; horizon 30 tahun, diskonto 5,5 persen). Tiga batas biaya berbeda; skema biaya asli belum ada'),
]
RA='customFormat="false" ht="35.05" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
RA2='customFormat="false" ht="23.85" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
N0=842; L0=N0+5; L1=L0+len(rows); N1=N0+len(rows)
docs_old=29; docs_new=len({r[0] for r in rows}-{SQ,ER})
KN0=146; KN1=KN0+len(conf)
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
        s=s.replace('COUNTA(K_Konflik!A5:A125)</f><v>121</v>',f'COUNTA(K_Konflik!A5:A{125+len(conf)})</f><v>{121+len(conf)}</v>')
        d=s.encode('utf8')
    elif n=='xl/worksheets/sheet7.xml':   # K_Konflik
        s=d.decode('utf8')
        i=s.find('<row r="127"'); j=s.find('</row>',i)+6; assert i>0
        note=s[i:j]; sh=len(conf)
        for c in 'ABCDEF': note=note.replace(f'{c}127',f'{c}{127+sh}')
        note=note.replace('r="127"',f'r="{127+sh}"'); s=s[:i]+s[j:]
        out=''
        for k,(idv,q,u,v1,s1,v2,s2,v3,s3) in enumerate(conf):
            r=126+k
            c=istr(f'A{r}',39,idv)+istr(f'B{r}',39,q)+istr(f'C{r}',39,u)+num(f'D{r}',62,v1)+istr(f'E{r}',39,s1)+num(f'F{r}',62,v2)+istr(f'G{r}',39,s2)
            c+=(num(f'H{r}',62,v3)+istr(f'I{r}',39,s3)) if v3 is not None else f'<c r="H{r}" s="39"/><c r="I{r}" s="39"/>'
            c+=f'<c r="J{r}" s="39"/><c r="K{r}" s="39"/>'+istr(f'L{r}',39,'Dicatat, belum dianalisis')
            out+=f'<row r="{r}" {RA2}>'+c+'</row>'
        s=s.replace('</sheetData>',out+note+'</sheetData>').replace('A1:L127',f'A1:L{127+sh}').replace('A127:F127',f'A{127+sh}:F{127+sh}')
        d=s.encode('utf8')
    elif n=='xl/sharedStrings.xml':
        s=d.decode('utf8'); assert 'K25 sampai K146' in s; d=s.replace('K25 sampai K146',f'K25 sampai K{KN1}').encode('utf8')
    zo.writestr(it,d)
zo.close(); print('register',N1,'dokumen',docs_old+docs_new,'konflik sampai',KN1)
