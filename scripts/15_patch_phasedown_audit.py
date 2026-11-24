"""Pada berkas base (setelah 14): tambah K142 sampai K146 (phase-down dan faktor LPG) dan perbarui audit kesiapan rice cooker dan LPG."""
import re,zipfile,sys
sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from xlsxkit import istr,num
from xml.sax.saxutils import escape
P=sys.argv[1] if len(sys.argv)>1 else '/tmp/claude-0/base_model.xlsx'
conf=[
('K142','Emisi CO2 PLTU batubara tahunan','MtCO2',302.12,'Fadiilah dan Dye 2026: 92 PLTU, 2023',271.3,'C_Listrik_Rencana: RUPTL RE Base 2025 (on-grid)',341.78,'C_Pembangkit: estimasi GEM 2025 (status E); IEA 2022 untuk batubara sekitar 279 (via Fadiilah)'),
('K143','Kapasitas enam PLTU prioritas pensiun dini','MW',14310,'Fadiilah dan Dye 2026 Tabel 3',16735,'Jumlah unit GEM pada C_Phasedown_Unit (Suralaya 6.025 dibanding 4.025; dugaan: Suralaya 9 dan 10 dan Lontar 4 beroperasi setelah data makalah; sisa 110 MW belum dijelaskan)',None,None),
('K144','Intensitas pengurangan pensiun dini PLTU','MtCO2 per GW',6.54,'Fadiilah dan Dye 2026: 93,52 per 14,31 GW',6.4,'D_Energi_Potensi: 28,8 per 4,5 GW',6.62,'Faktor workbook: faktor kapasitas 0,673 x 8,76 x 1,124'),
('K145','Faktor emisi LPG','tCO2 per ton',2.98,'D_Teknis_Opsi baris 159 (ASUMSI penulis)',3.16,'Turunan: 60,6 kgCO2e per GJ x 52,145 GJ per ton (Zain dkk. 2025, IPCC 2006 Tier 1)',None,None),
('K146','Kapasitas PLTU pensiun sampai 2030','GW',0,'JETP CIPP skenario utama (pensiun paling awal 2035 atau 2036)',5.2,'JETP CIPP sensitivitas (hlm 66)',6.85,'C_Phasedown_Unit jalur 2060 (jalur 2050: 9,3; jalur 2045: 11,2; jadwal PLN: uap mulai 2030, subkritis 2035)'),
]
RA2='customFormat="false" ht="23.85" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
zi=zipfile.ZipFile(P); items=[(i,zi.read(i.filename)) for i in zi.infolist()]; zi.close()
zo=zipfile.ZipFile(P,'w',zipfile.ZIP_DEFLATED)
for it,d in items:
    n=it.filename
    if n=='xl/worksheets/sheet7.xml':
        s=d.decode('utf8')
        i=s.find('<row r="122"'); j=s.find('</row>',i)+6; assert i>0
        note=s[i:j]
        for c in 'ABCDEF': note=note.replace(f'{c}122',f'{c}127')
        note=note.replace('r="122"','r="127"'); s=s[:i]+s[j:]
        out=''
        for k,(idv,q,u,v1,s1,v2,s2,v3,s3) in enumerate(conf):
            r=121+k
            c=istr(f'A{r}',39,idv)+istr(f'B{r}',39,q)+istr(f'C{r}',39,u)+num(f'D{r}',62,v1)+istr(f'E{r}',39,s1)+num(f'F{r}',62,v2)+istr(f'G{r}',39,s2)
            c+=(num(f'H{r}',62,v3)+istr(f'I{r}',39,s3)) if v3 is not None else f'<c r="H{r}" s="39"/><c r="I{r}" s="39"/>'
            c+=f'<c r="J{r}" s="39"/><c r="K{r}" s="39"/>'+istr(f'L{r}',39,'Dicatat, belum dianalisis')
            out+=f'<row r="{r}" {RA2}>'+c+'</row>'
        s=s.replace('</sheetData>',out+note+'</sheetData>').replace('A1:L122','A1:L127').replace('A122:F122','A127:F127')
        d=s.encode('utf8')
    elif n in ('xl/worksheets/sheet3.xml','xl/worksheets/sheet4.xml','xl/worksheets/sheet5.xml'):
        s=d.decode('utf8'); s=s.replace('COUNTA(K_Konflik!A5:A120)</f><v>116</v>','COUNTA(K_Konflik!A5:A125)</f><v>121</v>'); d=s.encode('utf8')
    elif n=='xl/sharedStrings.xml':
        s=d.decode('utf8'); assert 'K25 sampai K141' in s; d=s.replace('K25 sampai K141','K25 sampai K146').encode('utf8')
    elif n=='xl/worksheets/sheet97.xml':   # A_Kesiapan_Solusi
        s=d.decode('utf8')
        def patch_row(key,newP,newQ):
            global s
            m=re.search(r'<row r="(\d+)"[^>]*>(?:(?!</row>).)*?>%s</t>(?:(?!</row>).)*?</row>'%re.escape(key),s,re.S); row=m.group(0); r=m.group(1)
            row2=re.sub(r'(<c r="P%s"[^>]*><is><t[^>]*>)[^<]*'%r,r'\g<1>'+escape(newP),row)
            row2=re.sub(r'(<c r="Q%s"[^>]*><is><t[^>]*>)[^<]*'%r,r'\g<1>'+escape(newQ),row2)
            s=s.replace(row,row2)
        patch_row('Rice cooker','Siap','Dihitung di S_Rice_Cooker: LPG dihindari dikurangi listrik tambahan; netto sekitar -3,5 sampai 41 ktCO2 per tahun (tidak signifikan nasional). Tambahan listrik grafik PLN (10 sampai 11 kWh) belum dipakai.')
        patch_row('LPG ke kompor induksi','Kurang masukan','Faktor emisi LPG kini bersumber (3,16 tCO2 per ton, turunan IPCC via Zain 2025; K145). Masih perlu jumlah rumah tangga dan listrik induksi per rumah tangga bersumber.')
        s=re.sub(r'(COUNTIF\(\$P\$8:\$P\$59,C62\)</f><v>)19(</v>)',r'\g<1>20\2',s)
        s=re.sub(r'(COUNTIF\(\$P\$8:\$P\$59,C65\)</f><v>)7(</v>)',r'\g<1>6\2',s)
        s=s.replace('siap 19, siap setelah hitung ulang 1, kurang masukan 17, belum bisa 7','siap 20, siap setelah hitung ulang 1, kurang masukan 17, belum bisa 6')
        d=s.encode('utf8')
    zo.writestr(it,d)
zo.close(); print('patched')
