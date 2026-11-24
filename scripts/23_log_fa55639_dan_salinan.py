"""Catat commit codex fa55639 (data operasi TJB, biaya ETP, B40, gas suar) dan salinan pihak ketiga (EI, Perpres 132/2024): butir D_Register_Sumber 917 dan seterusnya, K167 sampai K171. Tiap angka diperiksa pada PDF, CSV, JSON asli atau gambar tabel yang dibaca langsung."""
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
RI='Gap analysis rencana kerja FOLU Net Sink Riau, Semenanjung Kampar dan Kerumutan (Nursamsu dkk. 2024, Paradigma)'
ER='ERIA CCS thermal (Sumitomo/ERIA 2025)'
ET='Studi implikasi fiskal pensiun dini PLTU (ETP/UNOPS, Oktober 2023)'
EI='Statistik biofuel dan gas suar Indonesia (Energy Institute Statistical Review 2026, salinan olahan pihak ketiga)'
PP='Perpres 132/2024 tentang pengelolaan dana perkebunan kelapa sawit, Pasal 18 dan 19 (salinan OCR pihak ketiga)'
rows=[
(ER,'Tabel 4.1 hlm. 27 (dibaca dari gambar)','Data operasi TJB 5 dan 6, 1 Oktober 2022 sampai 30 September 2023','Neto 1.000 MW per unit; COD Maret 2022 (unit 5) dan September 2022 (unit 6); produksi 6.748 dan 7.546 GWh (total 14.294); CF 77 persen (unit 5 berhenti Mei dan Juni 2023) dan 86 persen; batubara 6,7 juta ton; CO2 5,8 dan 6,4 Mt (total 12,2)','MW; GWh; persen; juta ton; MtCO2',EP+' Tabel gambar, dibaca langsung. Hitungan AC: intensitas 0,854 tCO2 per MWh; 0,469 t batubara per MWh; 1,82 tCO2 per t batubara; tangkapan 95 persen pada emisi aktual 11,59 Mt. Emisi aktual 12,2 Mt lebih dekat ke desain ERIA (13 Mt, atau 11,83 tanpa margin) daripada ke estimasi GEM 9,404 Mt (K167).',None,()),
(ER,'Hlm. 27','Dasar kapasitas tangkap','CO2 aktual September 2023 menurut CEMS 19.832 t per hari per unit; margin 10 persen; tangkap 95 persen; CF 0,86; 6,5 Mt per unit dan 13,0 Mt untuk dua unit','t per hari; Mt per tahun',EP,'2025_ERIA',('19,832','20,724','6,505,264')),
(ER,'Tabel 4.6 dan 4.10 (PDF hlm. 52 dan 57)','Kebutuhan pompa dan penukar panas rantai CCS pada aliran 35.616 t per hari','Rute A (kapal): pompa terminal 9.081 hp (6,77 MW mekanis), penukar panas 57.397 hp (42,80 MW termal); rute B (pipa): pompa booster 3.258 hp (2,43 MW)','hp; MW',EP+' Konversi 0,7457 kW per hp tanpa koreksi efisiensi (AC). Input parsial penalti energi; listrik tangkap, kompresi, injeksi dan uap belum ada.','2025_ERIA',('9,081','57,397','3,258','35,616')),
(ER,'Tabel 5.9 sampai 5.12','Total biaya CCS TJB 13 Mt (CAPEX ditambah OPEX 25 tahun)','Rute A USD 20.687,2 juta; rute B USD 23.525,5 juta; dibagi (13 Mt x 25 tahun) memberi USD 63,65 dan 72,39 per t (cocok dengan 63,7 dan 72,4)','USD juta; USD per tCO2',EP+' Replikasi AC. Biaya tingkat awal tanpa lahan, reklamasi, dan pemantauan kebocoran.','2025_ERIA',('20,687.2','23,525.5')),
(ER,'Gambar 5.1; Tabel 5.13 dan 5.14','Biaya levelized per kWh dan pembilang tersirat','7,42 dan 9,47 sen USD per kWh; bila penyebut produksi fisik 2.000 MW x CF 0,86 x 25 tahun (376,68 TWh), pembilang tersirat USD 27,95 dan 35,67 miliar, di atas total biaya tak didiskonto di atas','sen USD per kWh; USD miliar',EP+' Hitungan AC; jadwal arus kas dan diskonto belum bisa direplikasi (K170).','2025_ERIA',('7.42','9.47')),
(ET,'Tabel 14.1 hlm. 183 sampai 184; CSV padanan tim','Kompensasi enam kelompok aset yang beririsan dengan enam stasiun Fadiilah dan Dye','Suralaya 1 sampai 8, Cilacap 1 dan 2, Paiton 5 dan 6, Lontar 1 sampai 3: USD 2.474,27 juta pada tahun pensiun dan USD 1.701,41 juta nilai kini 2022; tiga baris bernilai nol (Suralaya 1 sampai 4, Suralaya 5 sampai 7, Paiton 5 dan 6)','USD juta',EP+' Jumlah baris CSV dicek langsung. Cakupan sebagian unit (25 unit GEM 14.420 MW dibanding 14.310 MW artikel); tidak dapat dibagi dengan 93,52 Mt. Belum ada biaya ETP untuk Tanjung Jati B, Cilacap 3 dan 4, atau Paiton-1.','2023_Studi-Implikasi',('770.00','1,029.60','674.67')),
(ET,'Lampiran 1.3 dan 1.4','Kapasitas Paiton 5 dan 6 (Jawa Power) menurut sumber','1.220 MW (Lampiran 1.4 ETP dan peta RUPTL); 1.519 MW (Lampiran 1.3 ETP); 1.320 MW (GEM dan Fadiilah dan Dye)','MW',EP+' K168. Suralaya 1 sampai 4 dan 5 sampai 7: ETP 1.800 dan 1.600 MW, GEM 1.600 dan 1.800 MW (tertukar; total sama; K169).','2023_Studi-Implikasi',('1,519','1,220')),
(EI,'Lembar Biofuels production, Biofuels consumption (CSV sources/2026_EI_...)','Biofuel Indonesia 2021 sampai 2025 (setara energi)','Produksi 337,070; 389,605; 432,912; 458,544; 515,214 PJ; konsumsi 305,930; 343,949; 404,552; 433,164; 440,313 PJ (2025: 122,309 TWh)','PJ',EP+' Dicek langsung pada JSON salinan olahan (commit 4803eba); bukan berkas Energy Institute asli. Pembanding aktivitas nasional, bukan liter B100 yang dibayar atau dicampur.',None,()),
(EI,'Lembar Natural Gas Flaring dan CO2 from Flaring','Gas suar Indonesia 2021 sampai 2025','Volume 0,746395; 0,765623; 1,00386; 0,893973; 0,865840 miliar m3 standar; CO2 1,50742; 1,54625; 2,02739; 1,80547; 1,74865 MtCO2','miliar m3; MtCO2',EP+' Dicek langsung pada JSON. Estimasi satelit VIIRS Nightfire (sejak 2013), GCV 40 MJ per m3 dan pembakaran sempurna; perubahan metode 2025. Mirip skala 1,7 MtCO2e potensi CM2 tetapi cakupan dan potensi pemulihan belum direkonsiliasi. Seri 2015 sampai 2025 di sources/2026_EI_Indonesia_biofuel-dan-gas-suar_2015-2025.csv.',None,()),
(RI,'Tabel 21 dan 24 (hlm. 36 dan 40)','Tutupan hutan alam lanskap, 1982 sampai 2022 (ha)','Kampar: 690.611,81 (1982); 553.027,05 (2002); 371.563,78 (2012); 345.368,36 (2022; 49,99 persen hilang sejak 1982). Kerumutan: 1.162.334,63; 607.860,94; 369.749,82; 310.851,79 (73,26 persen hilang)','ha',EP+' Analisis spasial Paradigma dari SIGAP KLHK; deforestasi melambat 2012 sampai 2022 (Kampar 26.195,42 ha; Kerumutan 36.342,42 ha).','Kajian',('690,611.81','553,027.05','371,563.78','345,368.36','1,162,334.63','607,860.94','369,749.82','310,851.79')),
(RI,'Tabel 52 (hlm. 93)','Areal rekomendasi tambahan RO 1 sampai RO 12','Total 253.221,44 ha: Kampar 58.210,47 dan Kerumutan 195.010,97; RO 7: 27.365,71 dan 143.883,99; RO 2: 24.886,71 dan 39.773,62; RO 8: 3.075,12 dan 7.198,41; RO 5: 1.963,50 dan 2.608,08; RO 12: 233,09 dan 977,47; RO 1: 34,91 dan 520,07','ha',EP+' Usulan penambahan ke Renja Riau; luas rencana, bukan realisasi atau pengurangan emisi.','Kajian',('253,221.44','58,210.47','195,010.97','27,365.71','143,883.99','24,886.71')),
(RI,'Bab VI (hlm. 94)','Sasaran FOLU Net Sink menurut kajian','-140 juta ton CO2e pada 2030 dan -304 juta ton CO2e pada 2050','MtCO2e',EP+' Sejalan dengan sasaran LTS-LCCR (FOLU -140 Mt 2030).','Kajian',('140','304')),
(PP,'Pasal 18 ayat (1) sampai (9); Pasal 19 ayat (4)','Dasar penyelesaian selisih HIP biodiesel','Dana menutup selisih kurang HIP minyak solar dan HIP biodiesel kelapa sawit, ditetapkan menteri bidang energi; berlaku semua jenis solar; dibayar setelah verifikasi (surveyor boleh didanai BPDP); perhitungan paling lambat tiga bulan sekali pada harga periode transaksi; dibatasi kebijakan Komite Pengarah; harga penyaluran biodiesel untuk pencampuran memakai HIP solar','pasal',EP+' Salinan OCR pihak ketiga (halaman 9 dan 10), dibaca langsung. Cocokkan dengan naskah pengundangan sebelum dikutip verbatim. Selisih HIP per bulan, volume terbayar, dan intensitas siklus hidup masih perlu data primer.',None,()),
]
bad=[(r[2][:50],has(r[6],*r[7])) for r in rows if r[6] and has(r[6],*r[7])]
print('belum ditemukan pada teks PDF:',bad)
if '--strict' in sys.argv: assert not bad
conf=[
('K167','Emisi CO2 PLTU Tanjung Jati B unit 5 dan 6, setahun','MtCO2',12.2,'ERIA 2025 Tabel 4.1 (aktual 1 Okt 2022 sampai 30 Sep 2023; unit 5 berhenti dua bulan)',9.404,'Prabowo dan Dalimi 2026 Tabel 5 (estimasi GEM, 2 x 4,702)',11.83,'ERIA desain tanpa margin (19.832 x 2 x 365 x 0,86 x 0,95); memperbarui K150: aktual 12,2 Mt sejalan dengan desain, estimasi GEM lebih rendah'),
('K168','Kapasitas Paiton 5 dan 6 (Jawa Power)','MW',1220,'ETP Lampiran 1.4 dan peta RUPTL (D_Gen_Eksisting baris 87)',1320,'GEM dan Fadiilah dan Dye',1519,'ETP Lampiran 1.3'),
('K169','Kapasitas Suralaya 1 sampai 4 dan 5 sampai 7','MW',1800,'ETP Lampiran 1.4: Suralaya 1 sampai 4 (dan 1.600 untuk 5 sampai 7)',1600,'GEM: Suralaya 1 sampai 4 (dan 1.800 untuk 5 sampai 7)',None,'Total dua kelompok sama; pembagian tertukar antar sumber'),
('K170','Pembilang tersirat biaya levelized CCS TJB','USD miliar',27.95,'7,42 sen per kWh x 376,68 TWh (ERIA Gambar 5.1; rute A)',20.6872,'ERIA Tabel 5.9 total CAPEX dan OPEX 25 tahun, rute A',35.67,'9,47 sen per kWh x 376,68 TWh dibanding USD 23,5255 miliar (rute B); jadwal diskonto belum dapat direplikasi'),
('K171','PLTP Lumut Balai: kapasitas yang masuk baseline','MW',110,'D_Gen_Eksisting baris 1644 (agregat eksisting COD 2019)',55,'PRJ-GEN-00156 Unit 2 pada pipeline EBT (COD rencana 2025)',None,'Kandidat duplikasi eksisting dan pipeline; tanggal snapshot dan unit dalam 110 MW belum dikonfirmasi'),
]
RA='customFormat="false" ht="35.05" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
RA2='customFormat="false" ht="23.85" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
N0=916; L0=N0+5; L1=L0+len(rows); N1=N0+len(rows)
docs_old=59; docs_new=2
KN0=166; KN1=KN0+len(conf)
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
        s=s.replace('COUNTA(K_Konflik!A5:A145)</f><v>141</v>',f'COUNTA(K_Konflik!A5:A{145+len(conf)})</f><v>{141+len(conf)}</v>')
        d=s.encode('utf8')
    elif n=='xl/worksheets/sheet7.xml':   # K_Konflik
        s=d.decode('utf8')
        i=s.find('<row r="149"'); j=s.find('</row>',i)+6; assert i>0
        note=s[i:j]; sh=len(conf)
        for c in 'ABCDEF': note=note.replace(f'{c}149',f'{c}{150+sh}')
        note=note.replace('r="149"',f'r="{150+sh}"'); s=s[:i]+s[j:]
        out=''
        for k,(idv,q,u,v1,s1,v2,s2,v3,s3) in enumerate(conf):
            r=146+k
            c=istr(f'A{r}',39,idv)+istr(f'B{r}',39,q)+istr(f'C{r}',39,u)+num(f'D{r}',62,v1)+istr(f'E{r}',39,s1)+num(f'F{r}',62,v2)+istr(f'G{r}',39,s2)
            c+=(num(f'H{r}',62,v3)+istr(f'I{r}',39,s3)) if v3 is not None else f'<c r="H{r}" s="39"/><c r="I{r}" s="39"/>'
            c+=f'<c r="J{r}" s="39"/><c r="K{r}" s="39"/>'+istr(f'L{r}',39,'Dicatat, belum dianalisis')
            out+=f'<row r="{r}" {RA2}>'+c+'</row>'
        s=s.replace('</sheetData>',out+note+'</sheetData>').replace('A1:L149',f'A1:L{150+sh}').replace('A149:F149',f'A{150+sh}:F{150+sh}')
        d=s.encode('utf8')
    elif n=='xl/sharedStrings.xml':
        s=d.decode('utf8'); assert 'K25 sampai K166' in s; d=s.replace('K25 sampai K166',f'K25 sampai K{KN1}').encode('utf8')
    zo.writestr(it,d)
zo.close(); print('register',N1,'dokumen',docs_old+docs_new,'konflik sampai',KN1)
