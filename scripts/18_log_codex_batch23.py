"""Catat batch 23 PDF dan data codex (commit 07379a1) pada berkas base setelah 17: butir D_Register_Sumber 883 dan seterusnya, K158 sampai K162. Tiap angka diperiksa pada teks PDF atau CSV."""
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
ET='Studi implikasi fiskal pensiun dini PLTU (ETP/UNOPS, Oktober 2023)'
SG='Penangkap karbon PLTU 2 x 315 MW (Sugito dkk. 2025, J. Business and Management Studies 7(4))'
US='Kematangan sumber daya penyimpanan CO2 Indonesia (Usman dkk. 2026, Evergreen 13(1))'
F6='Analisis biaya manfaat transisi listrik, LEAP-NEMO (Fitriana dkk. 2026, Results in Engineering)'
F4='Optimisasi bauran pembangkit (Fitriana dkk. 2024, Int. J. Sustainable Energy Planning and Management 42)'
KA='RUPTL dan investasi PLTN (Kanugraha 2025)'
OW='Statistik energi Indonesia 2015 sampai 2024 (Our World in Data, Energy Institute dan Ember)'
BH='Proyeksi transisi energi nasional dengan ANFIS (Bhakti dkk. 2025)'
SU='Pertumbuhan ekonomi, deforestasi dan emisi CO2, model koreksi galat (Susilo dkk. 2026)'
RN='FOLU Net Sink 2030 operational plan (KLHK)'
ER='ERIA CCS thermal (Sumitomo/ERIA 2025)'
CA='Tantangan sektor listrik Indonesia menuju NZE (Cahyo, Priambodo, Aisyah; PLN Research Institute, 2024, konferensi ICT-NZE)'
EP=' Status E (eksternal), tidak dijumlahkan dengan CM1 atau CM2 resmi.'
rows=[
(ET,'Tabel 14.1 (hlm. 183 sampai 184); CSV 32 aset','Estimasi kompensasi pensiun dini 32 aset atau kelompok unit','Jumlah USD 11.757,36 juta pada tahun pensiun (2024 sampai 2038); nilai kini 2022 USD 7.578,96 juta; contoh Ombilin 1 dan 2 (2024) 140,80 dan 122,89; Suralaya 8 (2027) 770,00 dan 547,97; Cirebon 1 (2031) 622,29 dan 337,35; Pelabuhan Ratu 1 sampai 3 (2034) 803,48 dan 355,16','USD juta',EP+' Jumlah baris CSV dicek langsung (11.757,36 dan 7.578,96). Valuasi aset, bukan harga terminasi kontrak atau biaya sistem. Berkas sources/2023_ETP-Kompensasi-Pensiun-PLTU_Tabel-14-1.csv.','2023_Studi-Implikasi',('140.80','122.89','770.00','547.97','622.29','337.35','803.48','355.16')),
(ET,'Bab 9 (hlm. 70 sampai 73, 128, 132)','Ombilin: kompensasi dan emisi dihindari','USD 140,80 juta; 4,4 MtCO2e dihindari terhadap pensiun alami (25 MtCO2e bila pembanding operasi sampai 2040); USD 32 per tCO2e','USD juta; MtCO2e; USD per tCO2e',EP+' Hitungan USD 32 per t adalah AC (140,8 dibagi 4,4), sebelum biaya listrik pengganti dan jaringan; K158. Portofolio di Tabel 5.1 memuat sekitar 1,4 GW di luar aset Tabel 14.1.','2023_Studi-Implikasi',('4.4','140.80')),
(ET,'Tabel 4.10 dan 4.11 (hlm. 64 sampai 65)','Setoran dana pensiun Cirebon 1 dan Pelabuhan Ratu','USD 56,58 juta per tahun dan USD 47,67 juta per tahun','USD juta per tahun',EP,'2023_Studi-Implikasi',('56.58','47.67')),
(SG,'Tabel 5 dan 6','CCS pascapembakaran PLTU 2 x 315 MW (simulasi)','Daya 630 MW sebelum dan 436 MW sesudah CCS; penalti 193,9 MW (30,8 persen); CAPEX CCS USD 334,4 juta; biaya tangkap USD 51,8 per tCO2; kenaikan LCOE USD 35,5 per MWh; CO2 sebelum dan sesudah 642,6 dan 63,54 t per jam','MW; persen; USD',EP+' Biaya tangkap saja; biaya per ton dihindari dan unit Tanjung Jati B (ERIA) berbeda. Satuan baris reboiler (3,37 MJ per t; 128,39 MW) belum konsisten dengan aliran tangkapan; jangan dipakai untuk neraca panas.','2025_Sugito',('193.9','51.8','334.4','35.5','642.6','63.54')),
(US,'Abstrak dan bagian hasil','Sumber daya penyimpanan CO2 menurut kematangan (SPE-SRMS, ambang 10 MtCO2)','14 lapangan minyak 0,81 GtCO2 subkomersial; 66 lapangan gas 8,42 GtCO2 (sekitar 0,025 komersial dan 8,40 subkomersial); akuifer salin 680,57 GtCO2 di 21 cekungan (undiscovered prospective)','GtCO2',EP+' Stok menurut kelas, bukan laju injeksi atau proyek. Berpotensi tumpang tindih dengan 572,77 Gt di D_Solusi_Kuantif (K160).','2026_Usman',('680.57','8.42','0.81')),
(F6,'Tabel 5 (hlm. 7)','Emisi pembangkitan listrik, model LEAP-NEMO','2060: BAU 544 dan NZE 60 MtCO2 per tahun (selisih 484); 2075: tabel 3, teks sekitar 5','MtCO2 per tahun',EP+' Batas pembangkitan listrik saja dan baseline model sendiri; K161.','2026_Fitriana',('544','60')),
(F6,'Tabel 2 (hlm. 7); hlm. 10 sampai 11','Asumsi biaya dan hasil finansial','Modal 2021: PLTS 1.200, panas bumi 3.200, PLTN 6.000 USD per kW; CF panas bumi dan nuklir 85 persen, PLTS 20 persen; NPV sekitar USD 4,51 triliun (2020 sampai 2100, diskonto 10 persen, eskalasi tarif 2,1 persen, karbon USD 25 per t); biaya sistem BAU 5,3398 dan NZE 7,1756 triliun USD (selisih 1,8358; hlm. 11 menyebut 1,7418)','USD per kW; triliun USD',EP+' Selisih biaya sistem tidak konsisten antar halaman (K162). Komponen biaya dan perlakuan jaringan belum dipastikan.','2026_Fitriana',('1200','3200','6000','4.51')),
(F4,'Hlm. 5 dan 12 sampai 13','Jalur model terkait sampai 2075 dan 2100','2075: PLTS 224,3 GW dan BESS 198,8 GW; permintaan 2100: NZE 4.649 TWh dan BAU 4.037 TWh (hitungan 15,2 persen; abstrak menyebut 28 persen)','GW; TWh',EP+' Kapasitas sebagai keluaran studi; klaim pertumbuhan permintaan perlu klarifikasi.','2024_Fitriana',('224.3','198.8')),
(KA,'Hlm. 2480','Jadwal PLTN dalam RUPTL','Dua unit 250 MW di Sumatera dan Kalimantan, jendela 2032 sampai 2033 (agregat 500 MW sama dengan RUPTL ARED)','MW',EP+' Rujukan sekunder jadwal perencanaan; lokasi final, FID, CAPEX dan COD belum ada.','2025_Kanugraha',('250','2480')),
(ER,'Hlm. 27; hitungan tim','Batas fisik tangkapan CCS Tanjung Jati B','19.832 tCO2 per hari per unit pada beban nominal; CF 86 persen; tangkap 95 persen; desain 13 Mt memakai margin 10 persen; tanpa margin: 12,451 Mt sebelum tangkapan dan 11,828 Mt tangkapan bruto','MtCO2 per tahun',EP+' Hitungan AC (19.832 x 2 x 365 x 0,86 x 0,95); di S_CCS_TJB. Tetap di atas 9,404 Mt emisi estimasi unit 5 dan 6 (K150).','2025_ERIA',('19832',)),
(OW,'CSV cuplikan Indonesia dan kamus indikator','Statistik nasional 2023 dan 2024','Listrik surya 0,710 TWh (2023) dan 1,350 TWh (2024); intensitas listrik 680,250 gCO2e per kWh (2024, siklus hidup); produksi gas 713,887 TWh dan minyak 347,964 TWh; konsumsi energi primer gas 472,717 TWh dan minyak 878,984 TWh (2024)','TWh; gCO2e per kWh',EP+' Dicek langsung pada CSV sources/2026_OWID_Energi-Indonesia_2015-2024.csv. Rata-rata nasional, bukan faktor marginal; selisih produksi dan konsumsi tidak dapat diatribusikan ke gas suar atau kebocoran.',None,()),
(RN,'Tabel S1; Tabel 133 sampai 136; hlm. 136','Restorasi gambut menurut penyebut lama dan sasaran kebakaran','Capaian 835.288 ha dari target 2.724.866 ha (30,65 persen; sisa 1.889.578 ha sama dengan alokasi spasial Tabel 136); sasaran nol kebakaran gambut 2030; 93,09 persen alokasi di Kalimantan Tengah, Riau, Sumatera Selatan dan Kalimantan Barat','ha',EP+' Vintage sampai 2019; berbeda dengan 10 persen Rossita dan Boer (K149 terkait). Persentase adalah AC.','2022_KLHK',('835288','2724866','1889578')),
('Faktor emisi gambut dan mangrove (Murdiyarso dkk. 2024, PNAS 121:e2307219121)','Hasil kebakaran','Gambut terbakar dalam kawasan deforestasi (basis FRL)','Sekitar 41.100 ha per tahun dan 20,9 MtCO2e per tahun; sekitar 509 tCO2e per ha terbakar','ha per tahun; MtCO2e per tahun',EP+' Rasio 509 adalah AC (20,9 juta dibagi 41.100).','2024_PNAS',('20.9',)),
(BH,'Hlm. 2814 sampai 2816; abstrak','Model ANFIS dan daftar 22 rujukan','Data uji 2021 sampai 2024 dengan galat rata-rata 7,50566 persen; abstrak menyebut akurasi 93,5 persen','persen',EP+' Metrik akurasi tidak dijelaskan; jangan dipakai sebagai jaminan skenario 2060 (tidak ada proyeksi buatan pihak lain yang dipakai di model).','2025_Bhakti',('93.5',)),
(CA,'Tabel 3 dan 4 (PDF hlm. 3 sampai 4)','Tolok ukur biaya dalam makalah Cahyo','LCOE IESR 2019: PLTS 5,84 sampai 10,28 dan panas bumi 4,56 sampai 11,4 sen USD per kWh; EPC (Tabel 4): PLTU batubara 1.500 sampai 1.800; angin 1.600 sampai 2.600; PLTS 1 sampai 50 MW 360 sampai 1.170; PLTN 1.000 MW 6.000 sampai 7.000; hidro 2.600 sampai 3.200; minihidro 2.000 sampai 5.000 per kW','sen USD per kWh; per kW',EP+' Tabel berupa gambar, dibaca langsung pada halaman 3 dan 4 (cocok dengan catatan tim). Kolom EPC tanpa mata uang dan sumber tabel [32] tidak ada pada daftar pustaka unggahan; tahan impor sampai terkonfirmasi.',None,()),
]
bad=[(r[2][:50],has(r[6],*r[7])) for r in rows if r[6] and has(r[6],*r[7])]
print('belum ditemukan pada teks PDF:',bad)
if '--strict' in sys.argv: assert not bad
conf=[
('K158','Biaya pensiun dini PLTU per tCO2e','USD per tCO2e',13.49,'UMD/IESR via D_Energi_Potensi (USD 4,6 miliar per 341 Mt; dipakai di C_Solusi B4)',32.0,'ETP/UNOPS 2023: Ombilin, kompensasi 140,8 juta per 4,4 Mt terhadap pensiun alami (sebelum biaya pengganti)',31.0,'IESR Cirebon-1: 31 sampai 40 (register; cakupan perlu diperiksa)'),
('K159','Biaya tangkap CO2 per tCO2 tertangkap','USD per tCO2',30.5,'ERIA 2025 Tabel 5.11: komponen tangkap saja, dua unit 13 Mt',51.8,'Sugito dkk. 2025: biaya tangkap, simulasi 2 x 315 MW (penalti daya 30,8 persen)',63.7,'ERIA 2025 total dengan kapal dan penyimpanan (batas atas sah 72,4; K147)'),
('K160','Sumber daya penyimpanan CO2 Indonesia','GtCO2',680.57,'Usman dkk. 2026: akuifer salin 21 cekungan (undiscovered prospective)',572.77,'D_Solusi_Kuantif baris 26 (sumber lain)',None,'Kedua estimasi mungkin mencakup wilayah yang sama; jangan dijumlahkan'),
('K161','Emisi listrik 2060 menurut cakupan','MtCO2 per tahun',544,'Fitriana dkk. 2026: BAU pembangkitan (LEAP-NEMO)',60,'Fitriana dkk. 2026: NZE pembangkitan',1561.764,'SNDC CPOS seluruh sektor energi 2060 (LCCP_L 129); cakupan berbeda'),
('K162','Selisih biaya sistem NZE terhadap BAU (Fitriana 2026)','triliun USD',1.8358,'Hlm. 10 (7,1756 dikurangi 5,3398)',1.7418,'Hlm. 11 (teks)',None,None),
]
RA='customFormat="false" ht="35.05" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
RA2='customFormat="false" ht="23.85" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
N0=882; L0=N0+5; L1=L0+len(rows); N1=N0+len(rows)
docs_old=45; docs_new=10
KN0=157; KN1=KN0+len(conf)
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
        s=s.replace('COUNTA(K_Konflik!A5:A136)</f><v>132</v>',f'COUNTA(K_Konflik!A5:A{136+len(conf)})</f><v>{132+len(conf)}</v>')
        d=s.encode('utf8')
    elif n=='xl/worksheets/sheet7.xml':   # K_Konflik
        s=d.decode('utf8')
        i=s.find('<row r="138"'); j=s.find('</row>',i)+6; assert i>0
        note=s[i:j]; sh=len(conf)
        for c in 'ABCDEF': note=note.replace(f'{c}138',f'{c}{139+sh}')
        note=note.replace('r="138"',f'r="{139+sh}"'); s=s[:i]+s[j:]
        out=''
        for k,(idv,q,u,v1,s1,v2,s2,v3,s3) in enumerate(conf):
            r=137+k
            c=istr(f'A{r}',39,idv)+istr(f'B{r}',39,q)+istr(f'C{r}',39,u)+num(f'D{r}',62,v1)+istr(f'E{r}',39,s1)+num(f'F{r}',62,v2)+istr(f'G{r}',39,s2)
            c+=(num(f'H{r}',62,v3)+istr(f'I{r}',39,s3)) if v3 is not None else f'<c r="H{r}" s="39"/><c r="I{r}" s="39"/>'
            c+=f'<c r="J{r}" s="39"/><c r="K{r}" s="39"/>'+istr(f'L{r}',39,'Dicatat, belum dianalisis')
            out+=f'<row r="{r}" {RA2}>'+c+'</row>'
        s=s.replace('</sheetData>',out+note+'</sheetData>').replace('A1:L138',f'A1:L{139+sh}').replace('A138:F138',f'A{139+sh}:F{139+sh}')
        d=s.encode('utf8')
    elif n=='xl/sharedStrings.xml':
        s=d.decode('utf8'); assert 'K25 sampai K157' in s; d=s.replace('K25 sampai K157',f'K25 sampai K{KN1}').encode('utf8')
    zo.writestr(it,d)
zo.close(); print('register',N1,'dokumen',docs_old+docs_new,'konflik sampai',KN1)
