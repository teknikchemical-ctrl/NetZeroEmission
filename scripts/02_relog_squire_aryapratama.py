import re,zipfile
from xml.sax.saxutils import escape
src='/home/user/NetZeroEmission/Indonesia_NZE_Data_Grafik_v2 (4).xlsx'
D1='Kelayakan co-firing limbah biomassa (Squire, Lou, Hilde 2024, Communications Earth and Environment 5:423)'
D2='Restorasi lahan terdegradasi untuk kayu dan energi (Aryapratama, Schulte, Pauliuk 2026, Biomass and Bioenergy 211:109191)'
E='Status E (eksternal), tidak dijumlahkan dengan CM1 atau CM2 resmi. '
rows=[
(D1,'Hasil, Tabel 1','Pasokan limbah biomassa yang masih tersedia setelah pemakaian lain','504,4','miliar MJ per tahun',E+'Hanya 30,7 persen dari 1.641,2 miliar MJ pasokan awal; pupuk memakai 25,7 persen.'),
(D1,'Tabel 1','Permintaan biomassa skenario Rendah, Setara, Menengah, Tinggi','196,8 / 504,4 / 651,7 / 1.608,6','miliar MJ per tahun',E+'Selisih pasokan dikurangi permintaan: +307,6 / 0 / -147,3 / -1.104,2. Skenario Menengah mengikuti target PLN untuk 52 unit.'),
(D1,'Tabel 3','Rasio co-firing termal PC / CFB / stoker: Rendah, Setara, Menengah, Tinggi','Rendah 3/10/20; Setara 5/24,6/24,6; Menengah 10/30/70; Tinggi 40/50/100','persen termal',E),
(D1,'Hasil, Gambar 6','Pengurangan emisi PLTU batubara dari co-firing pada 2030','14,2 sampai 152,5','juta tCO2 per tahun',E+'Biomassa limbah dianggap netral karbon; emisi budi daya, angkut, dan simpan tidak dihitung.'),
(D1,'Hasil, Gambar 6','Emisi PLTU batubara garis dasar 2030 (14,9 GW dalam konstruksi beroperasi)','369,5','juta tCO2 per tahun',E+'91,8 juta tCO2 di atas dasar 2023. Hanya skenario Tinggi yang mampu mengimbangi pertumbuhan.'),
(D1,'Diskusi','Emisi alih guna lahan bila co-firing memakai pelet kayu akasia, empat skenario','13,3 / 34,0 / 43,9 / 108,3','juta tCO2',E+'Setara deforestasi 1,2 sampai 9,9 juta ha (38 persen konsesi dibuka di hutan alam).'),
(D1,'Hasil, sensitivitas','Kisaran pasokan tahunan dan permintaan 2030 (Rendah / Menengah / Tinggi)','Pasokan 424 sampai 558; permintaan 126 sampai 239 / 431 sampai 782 / 1.172 sampai 1.829','miliar MJ',E),
(D1,'Hasil','Provinsi yang pasokannya mencukupi menurut skenario','82 persen (Rendah); sedikit di atas 35 persen (Tinggi)','persen provinsi',E+'Defisit terpusat di Indonesia timur, tempat PLTU captive bertambah.'),
(D1,'Pendahuluan','Target PLN co-firing: 52 unit, kapasitas, dan pengurangan 2025','18.895 MW; 11 juta tCO2 (2025) tambah 1 juta tCO2 dari limbah pertanian','MW; juta tCO2',E+'Kontrak 2023 hanya 0,6 juta ton dari target 2,2 juta ton; pemakaian 2022 0,45 juta ton (90 persen serbuk gergaji). NDC mencatat pemanfaatan biomassa 9 juta ton.'),
(D1,'Pendahuluan','Kapasitas PLTU 2023 dan 2030 menurut jenis','2023: 43,4 GW beroperasi, 14,9 GW konstruksi; 2030: captive 17,7 GW (127 unit), non-captive 40,5 GW (219 unit)','GW',E+'Komposisi boiler 2030: PC 57,59 persen, CFB 41,72 persen, stoker kurang dari 1 persen.'),
(D1,'Pendahuluan','Harga batubara dengan kewajiban pasar domestik','sekitar 70','USD per ton',E+'Harga biomassa terkirim bervariasi; biaya modal retrofit dan operasi tidak dianalisis makalah.'),
(D2,'Abstrak, Hasil GIS','Luas lahan terdegradasi yang sesuai untuk akasia, jati, dan karet (DLS1 sampai DLS3)','0,44 sampai 3,60','juta ha',E+'Target pemerintah 12 juta ha; DLS3 lebih kecil 64 sampai 88 persen dari dua skenario lain. Pada DLS2: karet 3,60; akasia 2,38; jati 1,93.'),
(D2,'Tabel 4','Emisi kumulatif dinamis (GWPdyn) 2030, DLS1: akasia kayu / jati kayu / karet energi','-163 / 85 / 129','juta tCO2e kumulatif',E+'Nilai kumulatif, bukan per tahun; tidak boleh dibandingkan langsung dengan selisih per tahun. Hanya akasia negatif pada 2030.'),
(D2,'Tabel 4','GWPdyn 2030, DLS1 dengan reforestasi: akasia / jati / karet','-163 / -154 / -169','juta tCO2e kumulatif',E+'Kumulatif.'),
(D2,'Tabel 4','GWPdyn 2030, DLS2: kayu akasia / jati / karet energi','174 / 331 / 1.141','juta tCO2e kumulatif',E+'Positif karena pembukaan lahan berkarbon tinggi.'),
(D2,'Tabel 4','GWPdyn 2030, DLS2 dengan reforestasi: akasia / jati / karet','-175 / -142 / -262','juta tCO2e kumulatif',E+'Kumulatif; -262 adalah batas bawah rentang reforestasi.'),
(D2,'Tabel 4','GWPdyn 2030, DLS3: kayu akasia / jati / karet energi','-57 / 31 / 24','juta tCO2e kumulatif',E+'Kumulatif.'),
(D2,'Tabel 4','GWPdyn 2030, DLS3 dengan reforestasi: akasia / jati / karet','-58 / -52 / -32','juta tCO2e kumulatif',E+'Kumulatif.'),
(D2,'Tabel 4','GWPdyn tahun ke-200 (2223) terendah: reforestasi jati DLS1 dan kayu jati DLS1','-456 dan -324','juta tCO2e kumulatif',E+'Horizon 200 tahun; di luar cakupan 2030.'),
(D2,'Hasil 3.3','Kontribusi 2030 terhadap emisi BAU total dan FOLU (kayu, lalu reforestasi)','1,1 sampai 9,1 persen dan 4,5 sampai 36,7 persen','persen BAU',E+'Pemetaan rentang ke pembanding dibaca dari teks makalah; akasia saja 5,7 persen dari emisi NDC 2030 (abstrak).'),
(D2,'Hasil 3.3','Emisi BAU 2030 yang dirujuk makalah dan target pemotongan','2.869; pemotongan 29 sampai 41 persen; FOLU 17 sampai 24 persen dari pengurangan','MtCO2e; persen',E+'Angka BAU sama dengan ENDC BTR-1 Tabel 4 di K28.'),
(D2,'Tabel 5','Produk kayu kumulatif sampai 2100 untuk skenario bahan (akasia dan jati)','0,42 sampai 4,58','miliar m3',E+'Setara 6,5 sampai 68,7 persen dari konsumsi kayu proyeksi nasional.'),
]
conf=[
('K125','Pengurangan emisi co-firing biomassa 2030','MtCO2e per tahun',11,'Target PLN (Squire dkk. 2024 mengutip; diandaikan di dalam CM1)',14.2,'Squire dkk. 2024, skenario Rendah',152.5,'Squire dkk. 2024, skenario Tinggi'),
('K126','Luas lahan terdegradasi untuk restorasi atau hutan tanaman','juta ha',12,'Target pemerintah (Aryapratama dkk. 2026)',0.44,'Aryapratama dkk. 2026, DLS3 (batas bawah)',3.6,'Aryapratama dkk. 2026, DLS2 karet (batas atas)'),
('K127','Pasokan limbah biomassa tersedia dibanding permintaan co-firing','miliar MJ per tahun',504.4,'Squire dkk. 2024, pasokan tersedia',196.8,'Squire dkk. 2024, permintaan Rendah',651.7,'Squire dkk. 2024, permintaan Menengah (target PLN)'),
]
def istr(ref,s,t): return f'<c r="{ref}" s="{s}" t="inlineStr"><is><t xml:space="preserve">{escape(t)}</t></is></c>'
def num(ref,s,v): return f'<c r="{ref}" s="{s}" t="n"><v>{v}</v></c>'
ROWATTR='customFormat="false" ht="35.05" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
zi=zipfile.ZipFile(src); items=[(i,zi.read(i.filename)) for i in zi.infolist()]; zi.close()
zo=zipfile.ZipFile(src,'w',zipfile.ZIP_DEFLATED)
last=746+len(rows); ndocs=19; nitems=741+len(rows)
for it,d in items:
    n=it.filename
    if n=='xl/worksheets/sheet88.xml':
        s=d.decode('utf8'); out=''
        for k,(a,b,c,e,f,g) in enumerate(rows):
            r=747+k
            out+=f'<row r="{r}" {ROWATTR}>'+num(f'A{r}',164,742+k)+istr(f'B{r}',39,a)+istr(f'C{r}',39,b)+istr(f'D{r}',39,c)+istr(f'E{r}',39,e)+istr(f'F{r}',39,f)+istr(f'G{r}',39,g)+'</row>'
        s=s.replace('</sheetData>',out+'</sheetData>')
        s=s.replace('D6:D746',f'D6:D{last}').replace('B6:B746',f'B6:B{last}').replace('A1:L746',f'A1:L{last}').replace('A5:G542',f'A5:G{last}')
        s=s.replace('Temuan utama: 741 butir dari 17 dokumen',f'Temuan utama: {nitems} butir dari {ndocs} dokumen')
        d=s.encode('utf8')
    elif n=='xl/worksheets/sheet7.xml':
        s=d.decode('utf8')
        i=s.find('<row r="105"'); j=s.find('</row>',i)+6
        note=s[i:j].replace('r="105"','r="108"').replace('A105','A108').replace('B105','B108').replace('C105','C108').replace('D105','D108').replace('E105','E108').replace('F105','F108')
        s=s[:i]+s[j:]
        out=''
        for k,(idv,q,u,v1,s1,v2,s2,v3,s3) in enumerate(conf):
            r=104+k
            out+=f'<row r="{r}" {ROWATTR.replace("35.05","23.85")}>'+istr(f'A{r}',39,idv)+istr(f'B{r}',39,q)+istr(f'C{r}',39,u)+num(f'D{r}',62,v1)+istr(f'E{r}',39,s1)+num(f'F{r}',62,v2)+istr(f'G{r}',39,s2)+num(f'H{r}',62,v3)+istr(f'I{r}',39,s3)+f'<c r="J{r}" s="39"/><c r="K{r}" s="39"/>'+istr(f'L{r}',39,'Dicatat, belum dianalisis')+'</row>'
        s=s.replace('</sheetData>',out+note+'</sheetData>')
        s=s.replace('A1:L105','A1:L108').replace('A105:F105','A108:F108')
        d=s.encode('utf8')
    elif n in ('xl/worksheets/sheet3.xml','xl/worksheets/sheet4.xml','xl/worksheets/sheet5.xml'):
        s=d.decode('utf8')
        s=s.replace('COUNTA(K_Konflik!A5:A103)</f><v>99</v>','COUNTA(K_Konflik!A5:A106)</f><v>102</v>')
        s=s.replace('COUNTA(D_Register_Sumber!D6:D746)</f><v>741</v>',f'COUNTA(D_Register_Sumber!D6:D{last})</f><v>{nitems}</v>')
        s=s.replace('D_Register_Sumber!B6:B746',f'D_Register_Sumber!B6:B{last}')
        d=s.encode('utf8')
    zo.writestr(it,d)
zo.close(); print('rows',last,'items',nitems)
