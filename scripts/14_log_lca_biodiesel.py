"""Catat LCA biodiesel sawit (Wahyono dkk. 2020) ke D_Register_Sumber pada berkas base (sebelum merakit model)."""
import re,zipfile,sys
sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from xlsxkit import istr,num
P=sys.argv[1] if len(sys.argv)>1 else '/tmp/claude-0/base_model.xlsx'
E='Status E (eksternal), tidak dijumlahkan dengan CM1 atau CM2 resmi. '
DL='Penilaian siklus hidup biodiesel sawit Indonesia, cradle to gate (Wahyono, Hadiyanto, Budihardjo, Adiansyah 2020, Energies 13:3248)'
rows=[
(DL,'Metode','Satuan fungsional, batas sistem, dan kebutuhan lahan','1 ton biodiesel; cradle to gate (kebun, pabrik minyak sawit, pabrik biodiesel); 0,86 ha lahan dan 6,39 ton TBS per ton biodiesel','ton; ha',E+'Data pabrik biodiesel dari proyek percontohan LEMIGAS; kebun dan pabrik di Sumatera Selatan. Tanpa pembanding solar dan tanpa densitas biodiesel, sehingga belum dapat diubah ke per liter.'),
(DL,'Tabel 5','Jejak karbon siklus hidup per ton biodiesel','Fosil 2.893,613; biogenik 28,777; alih guna lahan 7,451; serapan CO2 48,184','kg CO2e per ton biodiesel',E+'Jumlah netto sederhana fosil + biogenik + alih guna lahan - serapan = 2.881,66 kg CO2e per ton (dihitung di S_B40). Fosil terutama N2O dari gambut terdrainase di kebun (GWP N2O 298).'),
(DL,'Hasil 3.1 dan 3.2','Jejak karbon kebun dan produksi minyak sawit','Kebun 2.727; produksi minyak sawit 2.809','kg CO2e per ton biodiesel',E+'Kebun penyumbang terbesar; angka lebih besar dari studi lain (400 sampai 2.000 menurut teks) karena inventaris memasukkan N2O gambut dan pembakaran biomassa.'),
(DL,'Abstrak','Manfaat lingkungan penyerapan CO2 dan kontribusi fosfat','73,40 persen manfaat dari serapan CO2 kebun; fosfat 62,30 persen','persen',E),
(DL,'Abstrak','Kerusakan kesehatan manusia dan ekosistem per ton biodiesel','0,00563 DALY; 2,69 x 10^-5 spesies-tahun','DALY; spesies-tahun',E+'Pabrik biodiesel paling merusak untuk ketersediaan sumber daya; kebun paling merusak untuk karbon, kesehatan, dan ekosistem.'),
(DL,'Pendahuluan','Konteks energi Indonesia 2018 dan target kebijakan','Produksi primer 411,6 Mtoe (64 persen ekspor); konsumsi 114 Mtoe (transportasi 40 persen); target EBT 23 persen 2025 dan 31 persen 2050 (PP 79 Tahun 2014); mandat B20','Mtoe; persen',E),
]
RA='customFormat="false" ht="35.05" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
L0=841; N0=836; L1=L0+len(rows); N1=N0+len(rows)
zi=zipfile.ZipFile(P); items=[(i,zi.read(i.filename)) for i in zi.infolist()]; zi.close()
zo=zipfile.ZipFile(P,'w',zipfile.ZIP_DEFLATED)
for it,d in items:
    n=it.filename
    if n=='xl/worksheets/sheet88.xml':
        s=d.decode('utf8'); out=''
        for k,(a,b,c,e,f,g) in enumerate(rows):
            rr=L0+1+k
            out+=f'<row r="{rr}" {RA}>'+num(f'A{rr}',164,N0+1+k)+istr(f'B{rr}',39,a)+istr(f'C{rr}',39,b)+istr(f'D{rr}',39,c)+istr(f'E{rr}',39,e)+istr(f'F{rr}',39,f)+istr(f'G{rr}',39,g)+'</row>'
        assert f'D6:D{L0}' in s and f'Temuan utama: {N0} butir dari 28 dokumen' in s
        s=s.replace('</sheetData>',out+'</sheetData>').replace(f'D6:D{L0}',f'D6:D{L1}').replace(f'B6:B{L0}',f'B6:B{L1}').replace(f'A1:L{L0}',f'A1:L{L1}').replace(f'A5:G{L0}',f'A5:G{L1}')
        s=s.replace(f'Temuan utama: {N0} butir dari 28 dokumen',f'Temuan utama: {N1} butir dari 29 dokumen'); d=s.encode('utf8')
    elif n in ('xl/worksheets/sheet3.xml','xl/worksheets/sheet4.xml','xl/worksheets/sheet5.xml'):
        s=d.decode('utf8')
        s=s.replace(f'COUNTA(D_Register_Sumber!D6:D{L0})</f><v>{N0}</v>',f'COUNTA(D_Register_Sumber!D6:D{L1})</f><v>{N1}</v>').replace(f'D_Register_Sumber!B6:B{L0}',f'D_Register_Sumber!B6:B{L1}')
        d=s.encode('utf8')
    zo.writestr(it,d)
zo.close(); print('register',N1)
