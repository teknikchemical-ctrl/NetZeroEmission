import re,zipfile,sys
sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from xlsxkit import istr,num
P='/home/user/NetZeroEmission/Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx'
E='Status E (eksternal), tidak dijumlahkan dengan CM1 atau CM2 resmi. '
DB='Biaya ekonomi dan fiskal program biodiesel (Fitrady, Cahyaningsih, Nugrahaningsih 2026, Energy Policy 212:115134)'
DO='Jalur EBT dan target emisi, model OSeMOSYS untuk PLN (Afriani dan Poletti 2026, Energy Policy 211:115093)'
DS='Dekarbonisasi sektor listrik, kerangka kebijakan terpadu MISCAP (Sunanda, Setyonegoro, Hadi, Sarjiya 2026, Green Technologies and Sustainability 4:100276)'
DB4='Spesifikasi biosolar B40 (SK Dirjen Migas 384.K/MG.06/DJM/2024; Kepmen ESDM 341.K/EK.01/MEM.E/2024)'
rows=[
(DB,'Pendahuluan','Volume biodiesel: alokasi 2025, cakupan subsidi (PSO), kapasitas produksi, kebutuhan B50','Alokasi 15,62; PSO bersubsidi 7,54; kapasitas 15,6; kebutuhan B50 sekitar 20,1','juta kL',E+'Segmen non-PSO tidak disubsidi; selisih harga eceran sampai Rp6.000 per liter. Dasar hitung pengurangan B40 (lihat K138).'),
(DB,'Pendahuluan','Produksi CPO dan pangsa ekspor Indonesia 2023','46,99 juta ton; pangsa ekspor dunia 55,43 persen','juta ton; persen',E),
(DB,'Pendahuluan','Mandat campuran biodiesel','B20, B30, B40 (2025); target B50 (2026)','teks',E+'Subsidi membiayai selisih harga biodiesel terhadap solar lewat pungutan ekspor BPDP.'),
(DB,'Bagian 4.6','Pendapatan BPDP dari pungutan ekspor','2015: sekitar 6,9; 2018: 14,37; 2019: 0; 2020: 20,26; 2021: 71,7; 2024: 25,77','Rp triliun',E+'Subsidi biodiesel 2024 melampaui pendapatan BPDP sekitar 11 persen; kekurangan terjadi pada 2019, 2020, dan 2024. Pembiayaan di luar cakupan biaya saja; dicatat sebagai konteks.'),
(DB,'Bagian 4.6','Tarif pungutan ekspor CPO','Puncak 255 USD per ton (2022); pungutan nol dari pertengahan 2022; 2025 tetap 10 persen, setara 75 sampai 107 USD per ton','USD per ton',E),
(DB,'Bagian 4.6','Empat simulasi pendapatan BPDP terhadap subsidi','Simulasi 1, 2, 4: pendapatan di bawah kebutuhan subsidi; Simulasi 3 (harga komoditas naik, subsidi per liter tetap): pendapatan melampaui subsidi setelah 2026','teks',E+'Subsidi dihitung volume PSO dikali selisih harga biodiesel dan solar; parameter Lampiran E.'),
(DB,'Abstrak','Hasil makroekonomi','Penetrasi biodiesel berkaitan positif dengan pertumbuhan jangka pendek, lalu menurun; interaksi dengan ekspor CPO berdampak negatif terhadap PDB','teks',E+'Estimasi ARDL-ECM dibaca sebagai asosiasi, bukan sebab jangka panjang.'),
(DO,'Abstrak, Tabel 6','Skenario OSeMOSYS 2015 sampai 2050: biaya total sistem','BAU 700; NCT 721; ACT 740; PREP 1.089; ARE 1.202','miliar USD',E+'Dolar 2022, diskonto 6 persen (Bank Indonesia). NCT = pajak karbon nasional 1,8 USD per tCO2; ACT = pajak 100,02 USD per tCO2; PREP = RUPTL 2021 sampai 2030; ARE = RUPTL 2025 sampai 2034.'),
(DO,'Tabel 6','Emisi kumulatif 2015 sampai 2050 dan selisih terhadap BAU','BAU 49.785; NCT 49.732; ACT 38.544; PREP 21.572; ARE 12.634 MtCO2. Selisih: 52,9; 11.240,77; 28.212,78; 37.150,82','MtCO2',E+'Cakupan sektor listrik; bukan angka tahunan.'),
(DO,'Tabel 6, bagian 5.4','Biaya abatemen marginal (MAC) terhadap BAU','NCT 397; ACT 3,56; PREP 13,78; ARE 13,51','USD per tCO2',E+'Selisih biaya 21, 40, 389, 502 miliar USD (tabel). Teks menyebut 527 untuk ARE; tidak konsisten dengan 13,51 (K135).'),
(DO,'Bagian 5.5 dan 6','Sensitivitas biaya modal EBT plus minus 20 persen pada MAC','ARE 13,51 menjadi 20,1 (naik 20 persen) dan 9,1 (turun 20 persen); PREP 13,78 menjadi 20,7 dan 9,4; NCT 397 menjadi 403 dan 404; ACT tetap 3,5','USD per tCO2',E+'Penghematan sistem ARE tetap sekitar 136 miliar USD pada biaya modal turun 20 persen.'),
(DO,'Bagian 5.7','Sensitivitas diskonto (6, 8, 10, 12 persen)','Biaya total BAU 700 ke 641,8; NCT 721 ke 666,3; PREP 1.089 ke 1.519,7; ARE 1.202 ke 1.566,8; ACT 740 ke 692,4 (10 persen) dan 690,2 (12 persen); MAC NCT 397 ke 222,72, 376,05, 462,9','miliar USD; USD per tCO2',E),
(DO,'Pendahuluan','RUPTL 2025 sampai 2034 menurut makalah','Tambahan 69,5 GW, 42,6 GW (61 persen) EBT; termasuk 16,6 GW termal baru dan 6,3 GW batubara baru','GW',E+'Cocok dengan RUPTL di D_RUPTL_Tambahan secara garis besar; penjumlahan belum dicek.'),
(DO,'Pendahuluan dan Bagian 4','Parameter kebijakan dan teknis','Pajak karbon 30.000 Rp per tCO2e (1,82 USD); LTS-LCCR puncak sekitar 2030 dan sekitar 540 MtCO2e pada 2050; EBT 19 sampai 23 persen 2030 (KEN PP 40/2025); faktor kapasitas batubara 0,75 dan gas 0,55; emisi industri energi 2022 sekitar 650 MtCO2','campuran',E),
(DO,'Bagian 5.1','Pangsa EBT dalam bauran pembangkitan PREP','40 persen (2030) menjadi 99 persen (2050); pembangkitan 1.552 PJ (2030) menjadi 3.445 PJ (2050)','persen; PJ',E+'Batubara 85 persen pembangkitan pada BAU dan NCT.'),
(DS,'Abstrak, Gambar 3','Emisi sektor listrik 2025 sampai 2050 menurut skenario (kebijakan: NP tanpa kebijakan, ETS, CT pajak karbon, CCS, EC = ETS dan CCS, CEC = harga karbon dan CCS)','2050: NP 1.222,8; ETS 855,9; CT 673,5; CCS 550,2; EC 438,1; CEC 389,1. NP 2025: 225,5','MtCO2',E+'CEC turun 68,2 persen terhadap NP pada 2050; CT 45 persen, ETS 30 persen. Cakupan sektor listrik.'),
(DS,'Bagian 5.1','Emisi sekitar 2030 menurut skenario','CCS 160,91; EC 151,77; CEC 135,1; CT 173,92 (harga karbon 100 USD) sampai 233,64 (30 USD)','MtCO2',E+'Setelah 2030 skenario CCS naik lagi ke 550,2 pada 2050 tanpa batas atau harga karbon.'),
(DS,'Tabel 7','Investasi modal tahunan menurut skenario: 2025, 2030, 2050','NP 5,14; 6,91; 26,33. ETS 5,30; 7,12; 28,75. CT 5,48; 7,31; 31,92. CCS 10,06; 16,75; 47,04. EC 9,90; 20,89; 60,77. CEC 16,19; 26,14; 78,42','miliar USD per tahun',E+'Hanya biaya pembangkitan; transmisi tidak termasuk.'),
(DS,'Bagian 5.2','Kapasitas terpasang menurut skenario','2030: ETS 84,3 sampai NP 91,54; CEC 154,15 GW. 2040: NP 158,05; EC 307,97; CCS 307,91; CEC 347,97. 2050: NP 377,83; ETS 539,24; CT 567,28; CCS 583,81; EC 583,85; CEC 616,05','GW',E+'Pangsa EBT kapasitas 2050: CEC 83,6; EC 82,2 persen. Harga karbon di atas 63 USD per tCO2 memberi manfaat marginal menurun.'),
(DS,'Tabel 1','Batas emisi PTBAE PU 2023 sampai 2024 untuk PLTU batubara ke jaringan PLN','25 sampai 100 MW: 1,297; 100 sampai 400 MW: 1,011; di atas 400 MW: 0,911; mulut tambang 100 MW ke atas: 1,089','tCO2 per MWh',E+'Batas teknis resmi; cocok dengan rentang 0,79 sampai 1,22 (rata-rata 0,96) pada D_Teknis_Opsi (K137).'),
(DS,'Tabel 4','Biaya teknologi: biaya modal, BTT tetap, BTT variabel','PLTU uap 1.880 USD/kW, 51.600 USD/MW/tahun, 1,50 USD/MWh; surya utilitas 960, 7.500, 0; angin 1.650, 40.000, 0; gas 1.080, 26.800, 2,60; panas bumi 4.400, 110.000, 0,27; hidro 2.200, 43.000, 0,74; biomassa 2.280, 54.000, 3,40; diesel 910, 9.120, 7,30','campuran',E+'Mengonfirmasi bacaan Tabel 4 Nursidik (surya, angin, gas, panas bumi, hidro, biomassa sama); PLTU uap berbeda (K133).'),
(DS,'Tabel 5','Biaya CCS menurut teknologi','PLTU uap dengan CCS: 3.460 USD/kW, 90.200 USD/MW/tahun, 4,20 USD/MWh; IGCC dengan CCS: 4.290, 121.800, 21,78; turbin gas dengan CCS: 2.150, 50.200, 4,36','campuran',E+'Biaya tangkap serendah 16 USD per tCO2 untuk lapangan Jambaran Tiung Biru; selisih dengan Nursidik di K134.'),
(DS,'Tabel 6','Faktor emisi pembakaran menurut bahan bakar','Batubara bituminus lain 340,56; gas bumi 201,96; biomassa padat 360,00; solar 266,76; minyak mentah 263,88','kg per MWh',E+'Basis energi bahan bakar (kg per MWh termal), bukan listrik keluaran; sumber [80] makalah.'),
(DS,'Bagian 4','Faktor kapasitas dan kebijakan','Batubara 75 persen (realisasi 2023: Jawa-Bali 59 persen, Sumatera 53 persen); batas ETS 15,5 persen pengurangan emisi listrik pada 2030, mengetat linear sampai 2050','persen',E+'Faktor 0,75 dicatat di K136.'),
(DB4,'Tabel spesifikasi','Mutu biosolar B40 (batas utama)','Angka setana minimum 51; berat jenis 815 sampai 880 kg/m3; viskositas 2,0 sampai 5,0 mm2/s; kandungan FAME 40 persen v/v; sulfur 0,005 persen m/m (50 ppm) berlaku 1 Des 2027','campuran','Status R (dokumen resmi). FAME 40 persen mengikuti Kepmen ESDM 341.K/EK.01/MEM.E/2024; acuan SK Dirjen Migas 384.K/MG.06/DJM/2024 (31 Des 2024).'),
(DB4,'Catatan','Nilai kalor minimum yang tercetak','44.000 (tercetak MJ per kg)','MJ per kg tercetak','Status R. Satuan tercetak tidak masuk akal (diduga kJ per kg, 44 MJ per kg); verifikasi sebelum dipakai.'),
(DB4,'Catatan','Penelitian terkait kebijakan','Dokumen tidak memuat faktor emisi atau volume; hanya spesifikasi mutu','teks','Status R. Tidak dapat dipakai langsung untuk menghitung pengurangan emisi.'),
]
conf=[
('K133','Biaya modal PLTU batubara uap','USD per kW',1880,'Sunanda dkk. 2026 Tabel 4',1600,'Nursidik dkk. 2025 Tabel 4 (LEAP)',1500,'Cahyo dkk. 2024 EPC rendah (tinggi 1.800)'),
('K134','Biaya modal PLTU uap dengan CCS','USD per kW',3460,'Sunanda dkk. 2026 Tabel 5',3840,'Nursidik dkk. 2025 Tabel 4',None,None),
('K135','Selisih biaya skenario ARE terhadap BAU (OSeMOSYS)','miliar USD',502,'Afriani dan Poletti 2026 Tabel 6 (konsisten dengan MAC 13,51)',527,'Afriani dan Poletti 2026 teks bagian 5.4',None,None),
('K136','Faktor kapasitas PLTU batubara','fraksi',0.75,'Afriani dan Poletti 2026; Sunanda dkk. 2026',0.70,'D_Teknis_Opsi PLTU baru acuan',0.80,'Nursidik dkk. 2025 ketersediaan'),
('K137','Intensitas emisi PLTU batubara','tCO2 per MWh',0.96,'Fadiilah dan Dye 2026, rata-rata (rentang 0,79 sampai 1,22)',0.911,'Sunanda dkk. 2026 Tabel 1, PTBAE di atas 400 MW',1.297,'Sunanda dkk. 2026 Tabel 1, PTBAE 25 sampai 100 MW'),
('K138','Pengurangan emisi B40 per tahun','MtCO2e',41.46,'Klaim ESDM (K122)',41.7,'Hitung: 15,62 juta kL x 2,67 kg CO2 per liter (Fitrady dkk. 2026; Robbi 2026)',32.2,'Catatan pengguna ESDM sampai 2025'),
('K139','Tingkat diskonto sistem energi','persen',6,'Afriani dan Poletti 2026 (Bank Indonesia, sosial)',9,'Nursidik dkk. 2025 (ADB)',None,None),
('K140','Emisi pembangkit listrik 2025','MtCO2',271.3,'C_Listrik_Rencana, batubara RUPTL RE Base',225.5,'Sunanda dkk. 2026 skenario NP, semua pembangkit',None,None),
('K141','Emisi listrik atau energi sekitar 2030','MtCO2',301,'C_Listrik_Rencana, batubara RUPTL RE Base 2030',440,'Nursidik dkk. 2025, energi 2030 (puncak 2031 sebesar 440)',None,None),
]
RA='customFormat="false" ht="35.05" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
RA2='customFormat="false" ht="23.85" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
zi=zipfile.ZipFile(P); items=[(i,zi.read(i.filename)) for i in zi.infolist()]; zi.close()
zo=zipfile.ZipFile(P,'w',zipfile.ZIP_DEFLATED)
L0=814; N0=809; L1=L0+len(rows); N1=N0+len(rows)
for it,d in items:
    n=it.filename
    if n=='xl/worksheets/sheet88.xml':
        s=d.decode('utf8'); out=''
        for k,(a,b,c,e,f,g) in enumerate(rows):
            rr=L0+1+k
            out+=f'<row r="{rr}" {RA}>'+num(f'A{rr}',164,N0+1+k)+istr(f'B{rr}',39,a)+istr(f'C{rr}',39,b)+istr(f'D{rr}',39,c)+istr(f'E{rr}',39,e)+istr(f'F{rr}',39,f)+istr(f'G{rr}',39,g)+'</row>'
        assert f'D6:D{L0}' in s
        s=s.replace('</sheetData>',out+'</sheetData>').replace(f'D6:D{L0}',f'D6:D{L1}').replace(f'B6:B{L0}',f'B6:B{L1}').replace(f'A1:L{L0}',f'A1:L{L1}').replace(f'A5:G{L0}',f'A5:G{L1}')
        assert f'butir dari 24 dokumen' in s and f'Temuan utama: {N0} butir' in s
        s=s.replace(f'Temuan utama: {N0} butir dari 24 dokumen',f'Temuan utama: {N1} butir dari 28 dokumen')
        d=s.encode('utf8')
    elif n=='xl/worksheets/sheet7.xml':
        s=d.decode('utf8')
        i=s.find('<row r="113"'); j=s.find('</row>',i)+6; note=s[i:j]; assert i>0
        for c in 'ABCDEF': note=note.replace(f'{c}113',f'{c}122')
        note=note.replace('r="113"','r="122"')
        s=s[:i]+s[j:]; out=''
        for k,(idv,q,u,v1,s1,v2,s2,v3,s3) in enumerate(conf):
            r=112+k
            c=istr(f'A{r}',39,idv)+istr(f'B{r}',39,q)+istr(f'C{r}',39,u)+num(f'D{r}',62,v1)+istr(f'E{r}',39,s1)+num(f'F{r}',62,v2)+istr(f'G{r}',39,s2)
            c+=(num(f'H{r}',62,v3)+istr(f'I{r}',39,s3)) if v3 is not None else f'<c r="H{r}" s="39"/><c r="I{r}" s="39"/>'
            c+=f'<c r="J{r}" s="39"/><c r="K{r}" s="39"/>'+istr(f'L{r}',39,'Dicatat, belum dianalisis')
            out+=f'<row r="{r}" {RA2}>'+c+'</row>'
        s=s.replace('</sheetData>',out+note+'</sheetData>').replace('A1:L113','A1:L122').replace('A113:F113','A122:F122')
        d=s.encode('utf8')
    elif n in ('xl/worksheets/sheet3.xml','xl/worksheets/sheet4.xml','xl/worksheets/sheet5.xml'):
        s=d.decode('utf8')
        s=s.replace('COUNTA(K_Konflik!A5:A111)</f><v>107</v>','COUNTA(K_Konflik!A5:A120)</f><v>116</v>')
        s=s.replace(f'COUNTA(D_Register_Sumber!D6:D{L0})</f><v>{N0}</v>',f'COUNTA(D_Register_Sumber!D6:D{L1})</f><v>{N1}</v>').replace(f'D_Register_Sumber!B6:B{L0}',f'D_Register_Sumber!B6:B{L1}')
        d=s.encode('utf8')
    elif n=='xl/sharedStrings.xml':
        s=d.decode('utf8'); assert 'K25 sampai K132' in s; d=s.replace('K25 sampai K132','K25 sampai K141').encode('utf8')
    zo.writestr(it,d)
zo.close(); print('register',N1,'items; K_Konflik 116')
