"""Catat dua unggahan baru di main (laporan iklim PLN 2024 dan artikel panas bumi 2023) pada berkas base setelah 16:
butir D_Register_Sumber 867 dan seterusnya, konflik K154 sampai K157. Setiap angka diperiksa terhadap teks PDF."""
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
PL='Laporan pengungkapan terkait iklim PLN 2024 (IFRS S2), PT PLN (Persero), 23 Mei 2025'
GE='Lanskap energi panas bumi Indonesia, pembaruan 2023 (Pambudi dan Ulfa 2024, Renewable and Sustainable Energy Reviews 189:114008)'
EP=' Status R (laporan perusahaan, belum diaudit pihak ketiga dalam repo ini).'
rows=[
(PL,'Tabel 10 (hlm. 61)','Emisi PLN menurut lingkup 2024 (2023; 2022)','Lingkup 1: batubara 123,71; gas 23,91; minyak 7,74; total 156,31 (150,68; 148,33). Lingkup 2: 13,59. Lingkup 3: 106,66 termasuk listrik IPP 101,36. Pembangkitan lingkup 1 sampai 3: 266,11 (249,12; 233,42). Semua kegiatan: 276,56 (258,03; 241,05)','MtCO2e',EP+' Batas PLN: unit milik PLN pada Lingkup 1; IPP masuk Lingkup 3.','PLNplanNZE',('123.71','156.31','266.11','276.56','101.36')),
(PL,'Tabel 11 dan 12 (hlm. 62)','Intensitas emisi pembangkitan dan produksi listrik','0,774 tCO2e per MWh (2024); 0,770 (2023); 0,758 (2022); produksi 343,9 TWh (2024) dari 323,3 (2023); target 2025 0,79','tCO2e per MWh; TWh',EP,'PLNplanNZE',('0.774','0.770','0.758','343.9','323.3')),
(PL,'Tabel 14 (hlm. 63)','Emisi pembangkitan menurut jenis pembangkit 2024 (2023; 2022)','PLTU 125,1 (118,6; 119,4); PLTGU 18,1 (18; 15,5); PLTMG 5,2 (4,9; 4,8); PLTD 3,8 (3,5; 3,3); PLTG 3,3 (3,8; 3,7)','MtCO2e',EP+' PLTU milik PLN saja; berbeda cakupan dengan 302 Mt armada 92 PLTU (K142 dan K155).','PLNplanNZE',('125.1','118.6','119.4','18.1','5.2')),
(PL,'Gambar 7 (hlm. 23; dibaca dari gambar)','Jalur ARED emisi lingkup 1 sampai 3 pembangkitan','2020: 247; 2025: 310; 2030: 326 (puncak); 2035: 325; 2040: 321; 2045: 272; 2050: 224; 2055: 154; 2060: 0. Intensitas: 0,89 (2020); 0,74 (2030); 0,50 (2040); 0,21 (2050); 0 (2060)','MtCO2e per tahun; tCO2 per MWh',EP+' Angka dibaca dari gambar, pemeriksaan kedua diminta. Kasus ARED tanpa pensiun dini PLTU; mengandalkan co-firing dan CCS (hlm. 23).','PLNplanNZE',('247','310','326','325','321','272','224','154','0.89','0.74','0.50','0.21')),
(PL,'Gambar 6 (hlm. 22 sampai 23; dibaca dari gambar)','Skenario BAU PLN (kumulatif)','Label nilai 279; 447; 523; 786; 1.057 (2060); kenaikan 300 sampai 400 persen','MtCO2',EP+' Tahun label tengah tidak pasti pada gambar. Teks menulis "1.057 million tons" sedangkan sumbu gambar dalam MtCO2; satuan teks tidak konsisten (K154).','PLNplanNZE',('279','447','523','786','1,057')),
(PL,'Hlm. 66','Sasaran pengurangan PLN','ARED sekitar 99 MtCO2e lebih rendah dari BAU pada 2030; 88,00 MtCO2 dibanding BAU pada 2028 dengan intensitas 0,788; intensitas turun 15,7 persen pada 2030; target 51 MtCO2e pada 2025 (baseline 2010, ENDC); NZE 2060 dengan intensitas dari 0,89 (2021) ke 0','MtCO2e; persen',EP+' Angka 88 juga angka CM2 energi ENDC (sektor), tetapi di sini sasaran PLN 2028 terhadap BAU PLN.','PLNplanNZE',('99 million','88.00','15.7','51 million','0.788')),
(PL,'Tabel 17 (hlm. 66)','Realisasi pengurangan emisi PLN 2024 (target)','EBT tambahan 4,2 (3,1); teknologi batubara bersih 4,6 (4,2); konversi gas ke siklus kombinasi 2,1 (0,9); co-firing biomassa 1,8 (2,6); total 12,7 (10,8). Total 2023: 9,7; 2022: 6,0','MtCO2e',EP+' Co-firing 1,8 Mt sebanding dengan 1,57 Mt hitungan S_Cofiring (14,3 persen kali 11 Mt) dan 1,683 Mt CO2 biomassa dibakar (MEBI).','PLNplanNZE',('12.7','10.8','4.6','2.1','1.8','2.6')),
(PL,'Bagian co-firing (hlm. 39 sampai 40)','Co-firing biomassa PLN 2024','Konsumsi 1,62 juta ton (0,99 juta ton 2023; naik 70 persen); target tahunan 2,2 juta ton; kebutuhan puncak 10,2 juta ton 2025 lalu 8,91 juta ton 2030; 52 PLTU','juta ton',EP+' Konsumsi 1,62 dibanding 1,458 Mt di MEBI (butir S_Cofiring baris 25; K156).','PLNplanNZE',('1.62','0.99','2.2 million','10.2 million','8.91')),
(PL,'Hlm. 40 dan Tabel 18 (hlm. 67)','Biofuel dan teknologi batubara bersih','Biofuel PLN 2024 sekitar 1,94 MtCO2 (1,68 pada 2023; 1,48 pada 2022); B30 1.769,3 ribu tCO2 (2024); teknologi batubara bersih total 13,9 Mt dengan Jawa 9 dan 10 (2.000 MW USC) tertulis 44,1 Mt','MtCO2',EP+' Angka 44,1 Mt untuk Jawa 9 dan 10 tidak konsisten dengan total 13,9 dan Tabel 17 (4,6); jangan dipakai (K157).','PLNplanNZE',('1.94','1,769.3','13.9','44.1')),
(PL,'Hlm. 3, 4, 40 dan strategi','Skenario ARED 2040 dan rencana pembangunan EBT','Tambahan 61 GW (75 persen EBT; baseload 33 GW dan VRE 28 GW); gas 20 GW; nuklir 2,4 GW; Green Super Grid 33 GW baseload; RUPTL 2021 sampai 2030: 20,9 GW EBT (hidro 10,4; panas bumi 3,4; surya 4,7; lain 1,8; bio 0,6)','GW',EP,'PLNplanNZE',('61 GW','33 GW','28 GW','2.4 GW','20 GW','20.9','10.4','3.4','4.7')),
(PL,'Hlm. 3 dan bagian pelaksanaan','Pelaksanaan RUPTL 2021 sampai 2030','Baru 25 persen dari target 5,09 GW; 2024 selesai 480 MW (Asahan 3 2 x 87 MW; Jatigede 2 x 55 MW; IKN surya 10 MW); 3,4 GW pada 105 proyek konstruksi; target 2025 10,6 GW tambahan EBT','GW; MW',EP+' Bukti penundaan bagi baris pelaksanaan solusi EBT (WP-F).','PLNplanNZE',('25%','5.09','480 MW','105','3.4 GW','10.6 GW')),
(PL,'Bagian studi CCS (hlm. 48)','Studi CCS retrofit PLTU Indramayu','Potensi tangkapan sekitar 6,3 juta ton CO2 per tahun pada 2040; mitra INPEX, JERA, JGC','juta ton CO2 per tahun',EP+' Studi kelayakan; belum ada biaya atau jadwal.','PLNplanNZE',('6.3 million',)),
(PL,'Hlm. 42 sampai 43','Pasar karbon sektor listrik 2024','PTBAE-PU sekitar 119,39 MtCO2e untuk unit PLN; SPE-GRK terbit 4,01 Mt (0,93 pada 2023)','MtCO2e',EP,'PLNplanNZE',('119.39','4.01','0.93')),
(PL,'Hlm. 22 dan bagian efisiensi','Profil sistem PLN','Kapasitas terpasang 75,9 GW; 92,8 juta pelanggan; susut T&D 8,55 persen (9,91 persen 2013); AMI untuk 16 juta pelanggan sampai 2031 dengan biaya Rp26,8 triliun','GW; persen',EP,'PLNplanNZE',('75.9 GW','8.55','9.91','26.8')),
(GE,'Bagian 3 dan Tabel 3 sampai 5','Potensi dan kapasitas panas bumi','Potensi Indonesia 29,5 GW (29.500 MW; sekitar 40 persen potensi dunia); terpasang 2.356 MW akhir 2022 (kedua setelah AS 3.794 MW); perkiraan 2.339 MW pada Tabel 5; 1.948,5 MW pada 2018; dunia 15.854 MW (16.127 MW dalam sumber lain)','MW',E+'Pemanfaatan sekitar 8 persen potensi (AC, 2.356 dibagi 29.500). Bandingkan jalur PLN 3 GW (B6) dan potensi D_Energi_Potensi.','Geothermal',('29,500','2356','2339','3794','15,854','16,127','1948.5')),
(GE,'Bagian 3.2','Pembangkit panas bumi baru 2018 sampai 2022','Sarulla 110 MW; Karaha 30 MW; Lumut Balai 55 MW; Muara Laboh 85 MW; Sorik Merapi 137,3 MW; Rantau Dedap 98,4 MW; Sokoria 5 MW','MW',E+'Bukti laju historis; jumlah sekitar 520,7 MW dalam lima tahun (AC), sekitar 104 MW per tahun.','Geothermal',('110 MW','30 MW','55 MW','85 MW','137.3','98.4','5 MW')),
]
bad=[(r[2][:50],has(r[6],*r[7])) for r in rows if r[6] and has(r[6],*r[7])]
print('belum ditemukan pada teks PDF:',bad)
if '--strict' in sys.argv: assert not bad
conf=[
('K154','Satuan emisi BAU PLN 2060','MtCO2',1057,'PLN 2024 Gambar 6 dan 7 (sumbu dan label)',1.057,'PLN 2024 teks: "1.057 million tons"',None,None),
('K155','Emisi PLTU batubara menurut cakupan','MtCO2',125.1,'PLN 2024 Tabel 14 (PLTU milik PLN, 2024)',302.12,'Fadiilah dan Dye 2026 (92 PLTU termasuk IPP dan captive, 2023)',271.3,'C_Listrik_Rencana RUPTL RE Base; cakupan berbeda, bukan konflik angka murni'),
('K156','Konsumsi biomassa co-firing 2024','juta ton',1.62,'PLN 2024 hlm. 39',1.458,'MEBI via S_Cofiring baris 25',None,None),
('K157','Pengurangan Jawa 9 dan 10 (USC) 2024','MtCO2',44.1,'PLN 2024 teks hlm. 41 (Jawa 9 dan 10)',4.6,'PLN 2024 Tabel 17 (teknologi batubara bersih, seluruh program)',13.9,'PLN 2024 total teknologi batubara bersih; 44,1 lebih besar dari total (kemungkinan salah ketik 4,41)'),
]
RA='customFormat="false" ht="35.05" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
RA2='customFormat="false" ht="23.85" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
N0=866; L0=N0+5; L1=L0+len(rows); N1=N0+len(rows)
docs_old=43; docs_new=2
KN0=153; KN1=KN0+len(conf)
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
        s=s.replace('COUNTA(K_Konflik!A5:A132)</f><v>128</v>',f'COUNTA(K_Konflik!A5:A{132+len(conf)})</f><v>{128+len(conf)}</v>')
        d=s.encode('utf8')
    elif n=='xl/worksheets/sheet7.xml':   # K_Konflik
        s=d.decode('utf8')
        i=s.find('<row r="134"'); j=s.find('</row>',i)+6; assert i>0
        note=s[i:j]; sh=len(conf)
        for c in 'ABCDEF': note=note.replace(f'{c}134',f'{c}{134+sh}')
        note=note.replace('r="134"',f'r="{134+sh}"'); s=s[:i]+s[j:]
        out=''
        for k,(idv,q,u,v1,s1,v2,s2,v3,s3) in enumerate(conf):
            r=133+k
            c=istr(f'A{r}',39,idv)+istr(f'B{r}',39,q)+istr(f'C{r}',39,u)+num(f'D{r}',62,v1)+istr(f'E{r}',39,s1)+num(f'F{r}',62,v2)+istr(f'G{r}',39,s2)
            c+=(num(f'H{r}',62,v3)+istr(f'I{r}',39,s3)) if v3 is not None else f'<c r="H{r}" s="39"/><c r="I{r}" s="39"/>'
            c+=f'<c r="J{r}" s="39"/><c r="K{r}" s="39"/>'+istr(f'L{r}',39,'Dicatat, belum dianalisis')
            out+=f'<row r="{r}" {RA2}>'+c+'</row>'
        s=s.replace('</sheetData>',out+note+'</sheetData>').replace('A1:L134',f'A1:L{134+sh}').replace('A134:F134',f'A{134+sh}:F{134+sh}')
        d=s.encode('utf8')
    elif n=='xl/sharedStrings.xml':
        s=d.decode('utf8'); assert 'K25 sampai K153' in s; d=s.replace('K25 sampai K153',f'K25 sampai K{KN1}').encode('utf8')
    zo.writestr(it,d)
zo.close(); print('register',N1,'dokumen',docs_old+docs_new,'konflik sampai',KN1)
