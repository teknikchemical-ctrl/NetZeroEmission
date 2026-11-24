import re,zipfile,shutil,os
from xml.sax.saxutils import escape
exec(open('rows2.py',encoding='utf8').read())
SRC='/home/user/NetZeroEmission/Indonesia_NZE_Data_Grafik_v2 (4).xlsx'
DST='/home/user/NetZeroEmission/Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx'
def istr(ref,s,t): return f'<c r="{ref}" s="{s}" t="inlineStr"><is><t xml:space="preserve">{escape(t)}</t></is></c>'
def num(ref,s,v): return f'<c r="{ref}" s="{s}" t="n"><v>{v}</v></c>'
def fml(ref,s,f,v): return f'<c r="{ref}" s="{s}" t="n"><f aca="false">{escape(f)}</f><v>{v}</v></c>'
def fstr(ref,s,f,v): return f'<c r="{ref}" s="{s}" t="str"><f aca="false">{escape(f)}</f><v>{escape(v)}</v></c>'
RA='customFormat="false" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
def row(r,cells,ht=None): return f'<row r="{r}" {RA}'+(f' ht="{ht}"' if ht else '')+'>'+''.join(cells)+'</row>'

# ---------- new sheet C_Biaya_Teknologi ----------
r_disc=0.09
techA=[ # name, life, avail, capex20, capex50, fom20(USD/kW), status note
('PLTA besar',50,41,2200,1960,43.0),
('PLTU superkritis (batubara)',30,80,1600,1500,47.0),
('PLTG (gas)',25,80,1120,990,26.5),
('PLTGU (gas siklus gabungan)',25,80,1080,950,26.8),
('Panas bumi',30,80,4400,3960,110.0),
('Angin darat',30,25,1650,950,40.0),
('Surya PV',30,17,960,480,7.5),
('Biomassa',30,80,2280,1820,54.0),
('PLTU dengan CCS',30,80,3840,2770,97.0),
('Nuklir',60,80,5800,4500,127.0),
]
crf=lambda n:r_disc/(1-(1+r_disc)**(-n))
cells=[]; R={}
rowsX=[]
rowsX.append(row(1,[istr('A1',2,'Lembar 96. Biaya teknologi pembangkit: asumsi LEAP (Nursidik dkk. 2025) dibanding perkiraan EPC dan LCOE PLN (Cahyo dkk. 2024)')]))
rowsX.append(row(2,[istr('A2',2,'Biaya modal, BTT tetap, dan umur dari Tabel 4 Nursidik dkk. 2025 (dibaca dari gambar tabel); EPC dan LCOE dari Tabel 2 dan 4 Cahyo dkk. 2024. Biaya modal dan BTT tetap per MWh dihitung tanpa bahan bakar dan BTT variabel. Status E untuk angka sumber, AC untuk turunan hitung.')]))
# computed values
IA={}
for i,(n,life,av,c20,c50,fom) in enumerate(techA):
    H=c20*crf(life); I=(H+fom)/(8.76*av/100); IA[n]=(H,I)
nuk=IA['Nuklir'][1]; sur=IA['Surya PV'][1]; coal=IA['PLTU superkritis (batubara)'][1]
f3=('"Temuan utama: biaya modal nuklir "&ROUND(E16,0)&" USD per kW (LEAP, 2020) dibanding "&ROUND(C31,0)&" sampai "&ROUND(D31,0)&" (EPC PLN); biaya modal dan BTT tetap per MWh: nuklir "&ROUND(I16,0)&", surya "&ROUND(I13,0)&", PLTU "&ROUND(I8,0)&" USD (tanpa bahan bakar), sehingga biaya bahan bakar dan faktor emisi masih diperlukan untuk biaya per tCO2."')
v3=f'Temuan utama: biaya modal nuklir 5,800 USD per kW (LEAP, 2020) dibanding 6,000 sampai 7,000 (EPC PLN); biaya modal dan BTT tetap per MWh: nuklir {round(nuk)}, surya {round(sur)}, PLTU {round(coal)} USD (tanpa bahan bakar), sehingga biaya bahan bakar dan faktor emisi masih diperlukan untuk biaya per tCO2.'
v3=v3.replace('5,800','5800').replace('6,000','6000').replace('7,000','7000')
f3=f3.replace('ROUND(E16,0)','ROUND(E16,0)')
rowsX.append(row(3,[fstr('A3',2,f3,v3)]))
rowsX.append(row(5,[istr('B5',19,'Tabel 96.A. Parameter teknologi pembangkit (Nursidik dkk. 2025, Tabel 4) dan biaya modal serta BTT tetap per MWh (hitung)')]))
hdrA=['Teknologi','Umur (tahun)','Ketersediaan atau faktor kapasitas (persen)','Biaya modal 2020 (USD per kW)','Biaya modal 2050 (USD per kW)','BTT tetap 2020 (USD per kW per tahun)','Biaya modal tahunan 2020 (USD per kW per tahun)','Biaya modal dan BTT tetap (USD per MWh)','Status dan catatan']
rowsX.append(row(6,[istr(f'{c}6',23,h) for c,h in zip('BCDEFGHIJ',hdrA)]))
for k,(n,life,av,c20,c50,fom) in enumerate(techA):
    r=7+k; H,I=IA[n]
    rowsX.append(row(r,[istr(f'B{r}',24,n),num(f'C{r}',62,life),num(f'D{r}',62,av),num(f'E{r}',62,c20),num(f'F{r}',62,c50),num(f'G{r}',25,fom),
       fml(f'H{r}',25,f'E{r}*$C$19/(1-(1+$C$19)^(-C{r}))',H),fml(f'I{r}',25,f'(H{r}+G{r})/(8.76*D{r}/100)',I),
       istr(f'J{r}',24,'E untuk masukan dan AC untuk H dan I. Biaya modal MUSD per MW dikalikan 1.000; BTT tetap USD per MW dibagi 1.000. Dibaca dari gambar tabel; verifikasi ke katalog sumber.')]))
rowsX.append(row(17,[istr('B17',24,'BESS (penyimpanan baterai)'),num('C17',62,15),istr('D17',24,'80 sampai 90 (efisiensi)'),num('E17',62,470),num('F17',62,230),num('G17',25,15.0),
   fml('H17',25,'E17*$C$19/(1-(1+$C$19)^(-C17))',470*crf(15)),istr('I17',24,'tidak berlaku (penyimpanan)'),istr('J17',24,'E. Biaya per MWh tidak berarti tanpa siklus penyimpanan.')]))
rowsX.append(row(19,[istr('B19',24,'Tingkat diskonto (ADB, Nursidik dkk. 2025 Tabel 3)'),num('C19',30,0.09),istr('D19',24,'Status E. Ubah sel ini untuk uji sensitivitas; H dan I mengikuti.')]))
# Table B
rowsX.append(row(21,[istr('B21',19,'Tabel 96.B. Perkiraan biaya EPC PLN (Cahyo dkk. 2024, Tabel 4) dibanding biaya modal LEAP 2020')]))
hdrB=['Teknologi','EPC rendah (USD per kW)','EPC tinggi (USD per kW)','Skala (MW) dan bahan bakar','Biaya modal LEAP 2020 (USD per kW)','LEAP dibanding rata-rata EPC','Status dan catatan']
rowsX.append(row(22,[istr(f'{c}22',23,h) for c,h in zip('BCDEFGH',hdrB)]))
B=[('PLTU batubara',1500,1800,'25 sampai 50; batubara 70 USD per ton',8,'PLTU superkritis'),
('Mesin diesel',700,700,'semua ukuran; 13.000 Rp per liter',None,''),
('Mesin gas',800,900,'sampai 50; 13.000 Rp per liter',9,'dibanding PLTG'),
('Biomassa',1700,2200,'10 sampai 25; 15 sampai 80 USD per ton',14,''),
('WtE insinerator',7000,8000,'15 sampai 50; biaya tipping 50 USD',None,''),
('WtE gasifikasi',4000,7000,'sampai 50; gratis',None,''),
('Turbin angin',1600,2600,'10 sampai 50; gratis',12,'memerlukan pembangkit cadangan'),
('Surya PV',360,1170,'1 sampai 50; gratis',13,'memerlukan pembangkit cadangan'),
('Nuklir',6000,7000,'1.000; uranium 60 USD per lb',16,'mengisi kekosongan biaya nuklir'),
('PLTA',2600,3200,'sampai 50; gratis',7,'dibanding PLTA besar'),
('Mini hidro',2000,5000,'0,5 sampai 10; gratis',None,'')]
for k,(n,lo,hi,sk,ref,nt) in enumerate(B):
    r=23+k; cs=[istr(f'B{r}',24,n),num(f'C{r}',62,lo),num(f'D{r}',62,hi),istr(f'E{r}',24,sk)]
    if ref:
        e=techA[ref-7][3]; cs+= [fml(f'F{r}',62,f'E{ref}',e), fml(f'G{r}',25,f'F{r}/AVERAGE(C{r}:D{r})',e/((lo+hi)/2))]
    else: cs+=[istr(f'F{r}',24,'tidak ada pembanding'),istr(f'G{r}',24,'')]
    cs.append(istr(f'H{r}',24,'E. '+nt if nt else 'E.'))
    rowsX.append(row(r,cs))
# note: header uses E for scale text; columns: B,C,D,E(scale),F(leap),G(ratio),H(note)
# fix: temuan formula refers C31,D31 -> nuclear row is 23+8=31 ok
# Table C
rowsX.append(row(35,[istr('B35',19,'Tabel 96.C. LCOE PLN (Cahyo dkk. 2024, Tabel 2) dibanding biaya modal dan BTT tetap LEAP')]))
hdrC=['Jenis pembangkit','LCOE rendah (sen USD per kWh)','LCOE tinggi (sen USD per kWh)','LCOE tengah (sen USD per kWh)','Biaya modal dan BTT tetap LEAP (sen USD per kWh)','Status dan catatan']
rowsX.append(row(36,[istr(f'{c}36',23,h) for c,h in zip('BCDEFG',hdrC)]))
C=[('Gas',6.69,12.94,10),('Batubara',5.01,8.41,8),('Angin darat',7.39,16.1,12),('Surya PV',5.84,10.28,13),('Biomassa',4.68,11.4,14),('Panas bumi',4.56,11.4,11)]
nameA=[t[0] for t in techA]
for k,(n,lo,hi,ref) in enumerate(C):
    r=37+k; I=IA[nameA[ref-7]][1]
    rowsX.append(row(r,[istr(f'B{r}',24,n),num(f'C{r}',25,lo),num(f'D{r}',25,hi),fml(f'E{r}',25,f'AVERAGE(C{r}:D{r})',(lo+hi)/2),fml(f'F{r}',25,f'I{ref}/10',I/10),
       istr(f'G{r}',24,'E untuk LCOE, AC untuk kolom LEAP. Kolom LEAP belum memuat bahan bakar dan BTT variabel, sehingga lebih rendah dari LCOE penuh.')]))
rowsX.append(row(44,[istr('B44',24,'Tarif rata-rata pelanggan PLN (sen USD per kWh)'),num('C44',25,9),num('D44',25,11),istr('E44',24,''),istr('F44',24,''),istr('G44',24,'E. Cahyo dkk. 2024 Hasil D; harga jual EBT 5 sampai 11 sen belum termasuk transmisi dan layanan penunjang.')]))
# Table D
rowsX.append(row(46,[istr('B46',19,'Tabel 96.D. Rencana PV skala besar sampai 2030 menurut wilayah (Cahyo dkk. 2024, Tabel 3; satuan perlu verifikasi)')]))
rowsX.append(row(47,[istr(f'{c}47',23,h) for c,h in zip('BCD',['Wilayah','Nilai tercetak','Status dan catatan'])]))
D=[('Jawa-Madura-Bali',2900000),('Sumatera',192000),('Kalimantan',303000),('Sulawesi',175000),('Indonesia Timur',1100000)]
for k,(n,v) in enumerate(D):
    r=48+k; rowsX.append(row(r,[istr(f'B{r}',24,n),num(f'C{r}',62,v),istr(f'D{r}',24,'E. Satuan tercetak MW, tetapi jumlahnya tidak masuk akal; diduga kW.')]))
rowsX.append(row(53,[istr('B53',24,'Jumlah'),fml('C53',62,'SUM(C48:C52)',sum(v for _,v in D)),istr('D53',24,'AC. 4.670.000 kW setara 4,67 GW bila satuan kW.')]))
notes=['Catatan 96.1. Semua angka biaya sumber berstatus E dan tidak dijumlahkan dengan CM1 atau CM2 resmi. Tabel sumber berupa gambar sehingga dibaca visual; mohon verifikasi ke katalog asli sebelum dipakai untuk keputusan.',
'Catatan 96.2. Kolom H dan I (Tabel 96.A) memakai anuitas pada tingkat diskonto sel C19 dan BTT tetap; bahan bakar, BTT variabel, dan efisiensi tidak termasuk. Biaya per tCO2 memerlukan faktor emisi dan biaya bahan bakar, belum dimasukkan (lihat RESEARCH_TODO.md).',
'Catatan 96.3. Biaya modal LEAP (2020) dan EPC PLN berselisih untuk nuklir, surya, dan angin; selisih dicatat di K_Konflik (K128 sampai K130).']
for k,t in enumerate(notes):
    r=55+k; rowsX.append(row(r,[istr(f'B{r}',63,t)]))
merges=''.join(f'<mergeCell ref="B{55+k}:H{55+k}"/>' for k in range(3))
cols='<cols><col min="1" max="1" width="3" customWidth="true"/><col min="2" max="2" width="38" customWidth="true"/><col min="3" max="8" width="18" customWidth="true"/><col min="9" max="9" width="22" customWidth="true"/><col min="10" max="10" width="60" customWidth="true"/></cols>'
sheet=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
 '<sheetPr><tabColor rgb="FF1BAF7A"/></sheetPr><dimension ref="A1:J57"/><sheetViews><sheetView showGridLines="true" workbookViewId="0"/></sheetViews><sheetFormatPr defaultRowHeight="12.8"/>'
 +cols+'<sheetData>'+''.join(rowsX)+'</sheetData><mergeCells count="3">'+merges+'</mergeCells><pageMargins left="0.75" right="0.75" top="1" bottom="1" header="0.5" footer="0.5"/></worksheet>')

# ---------- patch package ----------
last=746+len(rows)+22   # register rows already include 22 from step 1
conf=[
('K128','Biaya modal pembangkit nuklir','USD per kW',5800,'Nursidik dkk. 2025 Tabel 4 (LEAP, 2020)',6000,'Cahyo dkk. 2024 Tabel 4, EPC rendah',7000,'Cahyo dkk. 2024 Tabel 4, EPC tinggi'),
('K129','Biaya modal surya PV','USD per kW',960,'Nursidik dkk. 2025 Tabel 4 (LEAP, 2020)',360,'Cahyo dkk. 2024 Tabel 4, EPC rendah',1170,'Cahyo dkk. 2024 Tabel 4, EPC tinggi'),
('K130','Biaya modal angin darat','USD per kW',1650,'Nursidik dkk. 2025 Tabel 4 (LEAP, 2020)',1600,'Cahyo dkk. 2024 Tabel 4, EPC rendah',2600,'Cahyo dkk. 2024 Tabel 4, EPC tinggi'),
('K131','Pangsa PLTU batubara efisien pada 2022','persen',23,'Rachmad dkk. 2024, teks',24.8,'Hitung: 26 efisien dari 105 PLTU',None,None),
('K132','Biaya operasi PLTU batubara','sen USD per kWh',19,'Rachmad dkk. 2024, rata-rata 0,19 USD per kWh',5.01,'Cahyo dkk. 2024 Tabel 2, LCOE batubara rendah',8.41,'Cahyo dkk. 2024 Tabel 2, LCOE batubara tinggi'),
]
RA2='customFormat="false" ht="23.85" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
zi=zipfile.ZipFile(SRC); items=[(i,zi.read(i.filename)) for i in zi.infolist()]; zi.close()
os.makedirs(os.path.dirname(DST),exist_ok=True)
zo=zipfile.ZipFile(DST,'w',zipfile.ZIP_DEFLATED)
for it,d in items:
    n=it.filename
    if n=='xl/worksheets/sheet88.xml':   # register
        s=d.decode('utf8'); out=''
        for k,(a,b,c,e,f,g) in enumerate(rows):
            rr=769+k
            out+=f'<row r="{rr}" customFormat="false" ht="35.05" hidden="false" customHeight="false" outlineLevel="0" collapsed="false">'+num(f'A{rr}',164,764+k)+istr(f'B{rr}',39,a)+istr(f'C{rr}',39,b)+istr(f'D{rr}',39,c)+istr(f'E{rr}',39,e)+istr(f'F{rr}',39,f)+istr(f'G{rr}',39,g)+'</row>'
        L=768+len(rows); N=763+len(rows)
        s=s.replace('</sheetData>',out+'</sheetData>')
        for a in ('768',):
            s=s.replace(f'D6:D{a}',f'D6:D{L}').replace(f'B6:B{a}',f'B6:B{L}').replace(f'A1:L{a}',f'A1:L{L}').replace(f'A5:G{a}',f'A5:G{L}')
        s=s.replace('Temuan utama: 763 butir dari 19 dokumen',f'Temuan utama: {N} butir dari 24 dokumen')
        d=s.encode('utf8')
    elif n=='xl/worksheets/sheet7.xml':  # K_Konflik
        s=d.decode('utf8')
        i=s.find('<row r="108"'); j=s.find('</row>',i)+6
        note=s[i:j]
        for c in 'ABCDEF': note=note.replace(f'{c}108',f'{c}113')
        note=note.replace('r="108"','r="113"')
        s=s[:i]+s[j:]
        out=''
        for k,(idv,q,u,v1,s1,v2,s2,v3,s3) in enumerate(conf):
            r=107+k
            c=istr(f'A{r}',39,idv)+istr(f'B{r}',39,q)+istr(f'C{r}',39,u)+num(f'D{r}',62,v1)+istr(f'E{r}',39,s1)+num(f'F{r}',62,v2)+istr(f'G{r}',39,s2)
            c+=(num(f'H{r}',62,v3)+istr(f'I{r}',39,s3)) if v3 is not None else f'<c r="H{r}" s="39"/><c r="I{r}" s="39"/>'
            c+=f'<c r="J{r}" s="39"/><c r="K{r}" s="39"/>'+istr(f'L{r}',39,'Dicatat, belum dianalisis')
            out+=f'<row r="{r}" {RA2}>'+c+'</row>'
        s=s.replace('</sheetData>',out+note+'</sheetData>').replace('A1:L108','A1:L113').replace('A108:F108','A113:F113')
        d=s.encode('utf8')
    elif n in ('xl/worksheets/sheet3.xml','xl/worksheets/sheet4.xml','xl/worksheets/sheet5.xml'):
        s=d.decode('utf8')
        s=s.replace('COUNTA(K_Konflik!A5:A106)</f><v>102</v>','COUNTA(K_Konflik!A5:A111)</f><v>107</v>')
        L=768+len(rows); N=763+len(rows)
        s=s.replace('COUNTA(D_Register_Sumber!D6:D768)</f><v>763</v>',f'COUNTA(D_Register_Sumber!D6:D{L})</f><v>{N}</v>')
        s=s.replace('D_Register_Sumber!B6:B768',f'D_Register_Sumber!B6:B{L}')
        d=s.encode('utf8')
    zo.writestr(it,d)
zo.close(); print('built',DST,'register total',763+len(rows))
open('newsheet.xml','w',encoding='utf8').write(sheet)
