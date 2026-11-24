"""Lembar solusi energi non-RUPTL (pensiun dini, CCS TJB, co-firing, B40), K_Studi, Q_Portofolio."""
import sys; sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from modelkit import *; import chartkit as ck; import src
import importlib.util
def _load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); sys.argv=['x']; spec.loader.exec_module(m); return m
def er(txt,col=3,start=6,end=70):  # D_Energi_Potensi row by item text prefix
    return src.find_row('D_Energi_Potensi',txt,col=col,start=start,end=end)
def single(name,nomor,label,rowC,desc,params_rows,srcrows,extra_inputs,chart_title,cost_cells=None,find_extra=None,finding=None,cfmt='#,##0.0'):
    """srcrows: list of (label,low_formula,high_formula,unit,status,source,style)"""
    sh=Sheet(name,'FF1BAF7A')
    sh.t('A1',f'Lembar {nomor}. Solusi {label}: tabel teknis, pengurangan emisi menurut sumber, biaya, dan pelaksanaan','title')
    sh.t('A2',desc,'title')
    # A summary
    if rowC is not None:
        sh.t('B5',f'Tabel {nomor}.A. Ringkasan 2030 (C_Solusi_2030)','tbl')
        for c,t in zip('BCDEFG',['Butir','Rendah','Tinggi','Satuan','Status','Sumber']): sh.t(f'{c}6',t,'hdr')
        S_=[('Pengurangan 2030',f'C_Solusi_2030!E{rowC}',f'C_Solusi_2030!F{rowC}','MtCO2e per tahun','n2l'),('Biaya per tCO2',f'C_Solusi_2030!G{rowC}',f'C_Solusi_2030!H{rowC}','USD per tCO2','n2l'),
            ('Biaya tahunan tengah',f'C_Solusi_2030!J{rowC}',f'C_Solusi_2030!J{rowC}','USD juta per tahun','n1l')]
        for i,(a,fl,fh,u,sty) in enumerate(S_):
            r=7+i; sh.t(f'B{r}',a); sh.f(f'C{r}',fl,sty); sh.f(f'D{r}',fh,sty); sh.t(f'E{r}',u); sh.f(f'F{r}',f'C_Solusi_2030!Q{rowC}','tl'); sh.f(f'G{r}',f'C_Solusi_2030!R{rowC}','tl')
        sh.t('B10','Persen selisih energi 2030 (rendah, tinggi)'); sh.f('C10','C7/B_Selisih_Penyebab!$C$7','pc'); sh.f('D10','D7/B_Selisih_Penyebab!$C$7','pc'); sh.t('E10','fraksi'); sh.t('F10','AC'); sh.t('G10','B_Selisih_Penyebab')
        sh.t('B11','Catatan C_Solusi_2030'); sh.f('C11',f'C_Solusi_2030!S{rowC}','tl'); sh.merges.append('C11:G11')

    # B params
    sh.t('B14',f'Tabel {nomor}.B. Parameter teknis bersumber (tautan ke D_Teknis_Opsi)','tbl')
    for c,t in zip('BCDEFGH',['Opsi','Kelas parameter','Parameter','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}15',t,'hdr')
    for i,r in enumerate(params_rows):
        rr=16+i
        sh.f(f'B{rr}',f'D_Teknis_Opsi!C{r}','tl'); sh.f(f'C{rr}',f'D_Teknis_Opsi!D{r}','tl'); sh.f(f'D{rr}',f'D_Teknis_Opsi!E{r}','tl'); sh.f(f'E{rr}',f'D_Teknis_Opsi!F{r}','tl'); sh.f(f'F{rr}',f'D_Teknis_Opsi!G{r}','tl'); sh.f(f'G{rr}',f'D_Teknis_Opsi!I{r}','tl'); sh.f(f'H{rr}',f'D_Teknis_Opsi!J{r}','tl')
    r0=16+len(params_rows)+2
    # C sources comparison
    sh.t(f'B{r0}',f'Tabel {nomor}.C. Pengurangan emisi menurut sumber (MtCO2e per tahun, kecuali dinyatakan lain)','tbl')
    for c,t in zip('BCDEFG',['Sumber','Rendah','Tinggi','Satuan','Status','Rujukan']): sh.t(f'{c}{r0+1}',t,'hdr')
    sh.t(f'H{r0+1}','Rentang (tinggi dikurangi rendah)','hdr')
    for i,(a,lo,hi,u,st,so,sty) in enumerate(srcrows):
        r=r0+2+i; sh.t(f'B{r}',a)
        if isinstance(lo,(int,float)): sh.n(f'C{r}',lo,'n2i')
        else: sh.f(f'C{r}',lo,sty)
        if isinstance(hi,(int,float)): sh.n(f'D{r}',hi,'n2i')
        else: sh.f(f'D{r}',hi,sty)
        sh.t(f'E{r}',u); sh.t(f'F{r}',st); sh.t(f'G{r}',so); sh.f(f'H{r}',f'D{r}-C{r}','n2')
    n=len(srcrows); rl=r0+2+n
    sh.t(f'B{rl}','Selisih energi 2030 (CPOS dikurangi LCCP_L)'); sh.f(f'C{rl}','B_Selisih_Penyebab!C7','n2l'); sh.f(f'D{rl}','B_Selisih_Penyebab!C7','n2l'); sh.t(f'E{rl}','MtCO2e'); sh.t(f'F{rl}','P'); sh.t(f'G{rl}','D_SNDC'); sh.f(f'H{rl}',f'D{rl}-C{rl}','n2')
    # D extra
    r2=rl+3
    sh.t(f'B{r2}',f'Tabel {nomor}.D. Hitungan sederhana dan masukan bersumber','tbl')
    for c,t in zip('BCDEF',['Butir','Nilai','Satuan','Status','Sumber']): sh.t(f'{c}{r2+1}',t,'hdr')
    refs={}
    for i,(key,a,v,u,st,so,kind) in enumerate(extra_inputs):
        r=r2+2+i; refs[key]=r; sh.t(f'B{r}',a)
        if kind=='in': sh.n(f'C{r}',v,'n2i')
        elif kind=='link': sh.f(f'C{r}',v,'n2l')
        else:
            f_=v
            for k,rr in refs.items(): f_=f_.replace('{'+k+'}',f'C{rr}')
            sh.f(f'C{r}',f_,'n2')
        sh.t(f'D{r}',u); sh.t(f'E{r}',st); sh.t(f'F{r}',so)
    rg=r2+2+len(extra_inputs)+1
    sh.t(f'B{rg}',f'Tabel {nomor}.E. Pelaksanaan saat ini (diisi tim; kosong sampai ada data bersumber)','tbl')
    for c,t in zip('BCDE',['Butir','Nilai','Satuan','Kode WP']): sh.t(f'{c}{rg+1}',t,'hdr')
    for i,(a,u,wp) in enumerate([('Capaian terhadap target 2030','fraksi','WP-F'),('Tahun data capaian','tahun','WP-F')]):
        sh.t(f'B{rg+2+i}',a); sh.blank(f'C{rg+2+i}','n2i'); sh.t(f'D{rg+2+i}',u); sh.t(f'E{rg+2+i}',wp)
    # charts
    cat=f'{name}!$B${r0+2}:$B${r0+1+n}'
    def rg_(col): return f'{name}!${col}${r0+2}:${col}${r0+1+n}'
    c1=ck.chart_xml(f'Gambar {nomor}.1. {chart_title}: pengurangan emisi menurut sumber (MtCO2e per tahun), rentang berarsir',
        [dict(base_ref=rg_('C'),band_ref=rg_('H'),name='Rentang rendah sampai tinggi',fill='F4B183')],
        [dict(val_ref=rg_('D'),name='Tinggi',color='C00000',pos='t',fmt=cfmt),dict(val_ref=rg_('C'),name='Rendah',color='1F4E79',pos='b',fmt=cfmt)],
        'MtCO2e per tahun','Sumber',cat,cat_numeric=False,yfmt=cfmt)
    if finding: sh.f('A3',finding(sh,r0,n,r2,refs),'title')
    else: sh.f('A3','"Temuan utama: '+label+': pengurangan 2030 pada C_Solusi "&ROUND(C7,1)&" sampai "&ROUND(D7,1)&" MtCO2e ("&ROUND(C10*100,1)&" sampai "&ROUND(D10*100,1)&" persen selisih energi); sumber lain pada Tabel C berkisar "&ROUND(MIN(C'+str(r0+2)+':C'+str(r0+1+n)+'),1)&" sampai "&ROUND(MAX(D'+str(r0+2)+':D'+str(r0+1+n)+'),1)&" MtCO2e."','title')
    sh.width('A','A',3); sh.width('B','B',58); sh.width('C','C',26); sh.width('D','D',30); sh.width('E','H',20); sh.width('G','G',44)
    sh.charts=[(c1,(1,rg+5,7600000,3900000))]
    sh.refs=dict(r0=r0,n=n,r2=r2,refs=refs,rg=rg)
    return sh
def S_Pensiun():
    return single('S_Pensiun_Dini',122,'pensiun dini PLTU',30,
      'Lapis resmi (CM2, 36 Mt) dan turunan (enam PLTU, bagian tambahan 57,5 Mt). Pengurangan emisi = emisi unit yang dipensiunkan; dibandingkan beberapa sumber bersumber. Biaya dari C_Solusi_2030 (13,49 USD per tCO2). Hanya angka bersumber dan hitungan sederhana.',
      [60,61,62,63,64,65,66],
      [('Resmi CM2: pensiun dini (D_Solusi_Kuantif)','C_Solusi_2030!E30','C_Solusi_2030!F30','MtCO2e','P','C_Solusi_2030 B1','n2l'),
       ('Turunan: enam PLTU, CO2 dihindari (Fadiilah dan Dye 2026)','D_Teknis_Opsi!F61','D_Teknis_Opsi!F61','MtCO2e (basis emisi 2023)','R','D_Teknis_Opsi baris 61','n2l'),
       ('Bagian tambahan enam PLTU di atas resmi (C_Solusi B4)','C_Solusi_2030!E33','C_Solusi_2030!F33','MtCO2e','A','C_Solusi_2030 B4','n2l'),
       ('Pihak ketiga: pensiun segera 4,5 GW on-grid',f'D_Energi_Potensi!E{er("Pensiun dini PLTU on-grid segera (4,5 GW)")}',f'D_Energi_Potensi!E{er("Pensiun dini PLTU on-grid segera (4,5 GW)")}','MtCO2 per tahun','E','D_Energi_Potensi','n2l')],
      [('inv1','Biaya pensiun dipercepat, rendah (pihak ketiga)',f'D_Energi_Potensi!E{er("Biaya pensiun dipercepat")}','USD miliar','E','D_Energi_Potensi','link'),
       ('inv2','Biaya pensiun dipercepat, tinggi (pihak ketiga)',f'D_Energi_Potensi!E{er("Biaya pensiun dipercepat",start=er("Biaya pensiun dipercepat")+1)}','USD miliar','E','D_Energi_Potensi','link'),
       ('cap','Kapasitas enam PLTU usulan (MW)','D_Teknis_Opsi!F60','MW','R','Fadiilah dan Dye 2026','link'),
       ('jetp','Pensiun dini sebelum 2030, skenario JETP CIPP (GW)',f'D_JETP!C{src.find_row("D_JETP","Pensiun dini PLTU sebelum 2030",col=2,start=1,end=30)}','GW','P','D_JETP (CIPP Tabel 4.3-1)','link'),
       ('cost','Biaya bersih pensiun (USD per tCO2)','C_Solusi_2030!G30','USD per tCO2','AC','C_Solusi_2030 B1','link'),
       ('ann','Biaya tahunan resmi: pengurangan x biaya (USD juta per tahun)','C_Solusi_2030!E30*{cost}','USD juta per tahun','AC','hitungan sederhana','calc'),
       ('etp_tot','ETP/UNOPS 2023: pembayaran kompensasi 32 aset, jumlah pada tahun pensiun (2024 sampai 2038)',11757.36,'USD juta','E','sources/2023_ETP-Kompensasi-Pensiun-PLTU_Tabel-14-1.csv (jumlah 32 baris)','in'),
       ('etp_pv','ETP/UNOPS 2023: nilai kini 2022',7578.96,'USD juta','E','berkas CSV yang sama','in'),
       ('omb_pay','ETP/UNOPS 2023: pembayaran Ombilin 1 dan 2 (pensiun 2024)',140.8,'USD juta','E','Tabel 14.1 hlm. 183','in'),
       ('omb_em','ETP/UNOPS 2023: emisi dihindari Ombilin terhadap pensiun alami',4.4,'MtCO2e','E','Bab 9 (hlm. 70 sampai 73)','in'),
       ('omb_c','Kompensasi Ombilin per tCO2e dihindari (sebelum biaya pengganti dan jaringan)','{omb_pay}/{omb_em}','USD per tCO2e','AC','hitungan sederhana; dibandingkan dengan biaya turunan di atas (K158)','calc'),
       ('omb_r','Kompensasi Ombilin dibagi biaya turunan C_Solusi B1','{omb_c}/{cost}','fraksi','AC','hitungan sederhana; di atas 1 berarti biaya ETP lebih tinggi','calc')],
      'Pensiun dini PLTU')
def S_CCS():
    return single('S_CCS_TJB',123,'CCS PLTU Tanjung Jati B',34,
      'Dua unit 1.000 MW dengan laju tangkap 0,95 dan faktor kapasitas 0,86 menangkap sekitar 13 MtCO2 per tahun (ERIA CCS 2025). Biaya per tCO2 dari C_Solusi_2030; penalti energi CCS belum ada (WP-J). Hanya angka bersumber dan hitungan sederhana.',
      [67,68,69],
      [('C_Solusi B5: dua unit TJB (rendah)','C_Solusi_2030!E34','C_Solusi_2030!F34','MtCO2e','AC','C_Solusi_2030 B5','n2l'),
       ('Satu unit 1.000 MW (D_Teknis_Opsi)','D_Teknis_Opsi!F67','D_Teknis_Opsi!F67','MtCO2 per tahun','R','D_Teknis_Opsi baris 67','n2l')],
      [('capex1','Biaya modal PLTU uap dengan CCS, LEAP (USD per kW)','C_Biaya_Teknologi!E15','USD per kW','E','C_Biaya_Teknologi (Nursidik 2025)','link'),
       ('capex2','Biaya modal PLTU uap dengan CCS (USD per kW)',3460,'USD per kW','E','Sunanda dkk. 2026 Tabel 5','in'),
       ('cost_lo','Biaya per tCO2 rendah','C_Solusi_2030!G34','USD per tCO2','AC','C_Solusi_2030 B5','link'),
       ('cost_hi','Biaya per tCO2 tinggi','C_Solusi_2030!H34','USD per tCO2','AC','C_Solusi_2030 B5','link'),
       ('ann_lo','Biaya tahunan rendah (USD juta per tahun)','C_Solusi_2030!E34*{cost_lo}','USD juta per tahun','AC','hitungan sederhana','calc'),
       ('ann_hi','Biaya tahunan tinggi (USD juta per tahun)','C_Solusi_2030!F34*{cost_hi}','USD juta per tahun','AC','hitungan sederhana','calc'),
       ('tjbco2','Emisi CO2 PLTU Tanjung Jati B 2023, seluruh unit (Fadiilah dan Dye 2026 Tabel 3)',24.01,'MtCO2','R','Fadiilah dan Dye 2026','in'),
       ('ovl','Tumpang tindih bila TJB dipensiunkan penuh (bagian tambahan B4): CCS 13 Mt menjadi redundan sebesar','MIN(C_Solusi_2030!E34,{tjbco2})','MtCO2e','AC','hitungan sederhana (K142 sampai K146 mencatat konteks pensiun dini)','calc'),
       ('em56','Emisi unit 5 dan 6 TJB (2 x 4,702; estimasi GEM)',9.404,'MtCO2 per tahun','E','Prabowo dan Dalimi 2026 Tabel 5 (K150)','in'),
       ('cap_em','Tangkapan kotor ERIA dibagi emisi unit 5 dan 6','C_Solusi_2030!E34/{em56}','fraksi','AC','hitungan sederhana; di atas 1 berarti asumsi pemanfaatan ERIA lebih tinggi dari estimasi GEM (K150)','calc'),
       ('c72','Biaya per tCO2, dua unit 13 Mt, pipa (batas atas yang sah)',72.4,'USD per tCO2','R','ERIA 2025 Tabel 5.12 (K147)','in'),
       ('c63','Biaya per tCO2, dua unit 13 Mt, kapal dan pipa darat',63.7,'USD per tCO2','R','ERIA 2025 Tabel 5.11','in'),
       ('annk_lo','Biaya tahunan dikoreksi, rendah (USD juta per tahun)','C_Solusi_2030!E34*{c63}','USD juta per tahun','AC','hitungan sederhana (K147: 92,6 pada tabel di atas adalah kasus satu unit)','calc'),
       ('annk_hi','Biaya tahunan dikoreksi, tinggi (USD juta per tahun)','C_Solusi_2030!F34*{c72}','USD juta per tahun','AC','hitungan sederhana (K147)','calc'),
       ('dt','ERIA hlm. 27: CO2 per hari per unit pada beban nominal',19832,'tCO2 per hari','R','ERIA 2025 hlm. 27','in'),
       ('cf86','Faktor kapasitas model ERIA',0.86,'fraksi','R','ERIA 2025 hlm. 27','in'),
       ('cr95','Laju tangkap ERIA',0.95,'fraksi','R','ERIA 2025 hlm. 27','in'),
       ('nomg','Tangkapan bruto dua unit tanpa margin desain 10 persen','{dt}*2*365*{cf86}*{cr95}/1000000','MtCO2 per tahun','AC','hitungan sederhana atas asumsi ERIA (11,83 dibanding 13)','calc'),
       ('nomg_r','Tangkapan tanpa margin dibagi emisi unit 5 dan 6 (GEM)','{nomg}/{em56}','fraksi','AC','hitungan sederhana; masih di atas 1 (K150)','calc'),
       ('sg_pen','Sugito dkk. 2025: penalti daya CCS, simulasi 2 x 315 MW (630 ke 436 MW)',0.308,'fraksi','E','Sugito dkk. 2025 Tabel 5','in'),
       ('sg_c','Sugito dkk. 2025: biaya tangkap',51.8,'USD per tCO2 tertangkap','E','Sugito dkk. 2025 Tabel 6 (hanya tangkap; K159)','in'),
       ('sg_cx','Sugito dkk. 2025: CAPEX CCS',334.4,'USD juta','E','Sugito dkk. 2025 Tabel 6','in'),
       ('sg_l','Sugito dkk. 2025: kenaikan LCOE',35.5,'USD per MWh','E','Sugito dkk. 2025 Tabel 6','in')],
      'CCS TJB')
def S_Cofiring():
    return single('S_Cofiring',124,'co-firing biomassa',27,
      'Lapis A (dalam CM1): target PLN 11 MtCO2 per tahun. Dibandingkan rentang pengurangan skenario pasokan limbah biomassa (Squire dkk. 2024, K125). Realisasi 14,3 persen (2024). Faktor emisi biomassa dan pembukuan netral karbon belum diputuskan (WP-F, R20).',
      [r for r in TRBIO],
      [('Lapis A CM1: target PLN (C_Solusi A4)','C_Solusi_2030!E27','C_Solusi_2030!F27','MtCO2e','T','C_Solusi_2030 A4','n2l'),
       ('Squire dkk. 2024: skenario Rendah sampai Tinggi, 2030',14.2,152.5,'MtCO2 per tahun','E','D_Register_Sumber (Squire 2024, Gambar 6)','n2i')],
      [('ratio','Capaian terhadap target (C_Solusi Tabel 32.D)','C_Solusi_2030!D72','fraksi','AC','C_Cofiring_Biaya bagian D','link'),
       ('now','Pengurangan pada pelaksanaan saat ini (MtCO2e per tahun)','C_Solusi_2030!E27*{ratio}','MtCO2e','AC','hitungan sederhana','calc'),
       ('sup','Pasokan limbah biomassa tersedia (miliar MJ per tahun)',504.4,'miliar MJ','E','Squire dkk. 2024 Tabel 1','in'),
       ('dem','Permintaan skenario Menengah (target PLN, miliar MJ per tahun)',651.7,'miliar MJ','E','Squire dkk. 2024 Tabel 1','in'),
       ('cov','Pasokan dibagi permintaan Menengah','{sup}/{dem}','fraksi','AC','hitungan sederhana','calc'),
       ('cl','Biaya per tCO2 rendah (campuran realisasi)','C_Solusi_2030!G27','USD per tCO2','AC','C_Cofiring_Biaya','link'),
       ('ch','Biaya per tCO2 tinggi (harga ekspor)','C_Solusi_2030!H27','USD per tCO2','AC','C_Cofiring_Biaya','link'),
       ('sq_bau','Squire dkk. 2024: emisi PLTU 2030 skenario BAU',369.491737,'MtCO2 per tahun','E','sources/2024_Squire-dkk_Emisi-Skenario-Co-firing.csv','in'),
       ('sq_low','Skenario Rendah, emisi PLTU 2030',355.30484,'MtCO2 per tahun','E','berkas CSV penulis','in'),
       ('sq_eq','Skenario Setara, emisi PLTU 2030',328.53,'MtCO2 per tahun','E','berkas CSV penulis','in'),
       ('sq_mid','Skenario Menengah, emisi PLTU 2030',311.523627,'MtCO2 per tahun','E','berkas CSV penulis','in'),
       ('sq_hi','Skenario Tinggi, emisi PLTU 2030',216.981,'MtCO2 per tahun','E','berkas CSV penulis','in'),
       ('d_low','Pengurangan skenario Rendah (BAU dikurangi skenario)','{sq_bau}-{sq_low}','MtCO2 per tahun','AC','hitungan sederhana','calc'),
       ('d_eq','Pengurangan skenario Setara','{sq_bau}-{sq_eq}','MtCO2 per tahun','AC','hitungan sederhana','calc'),
       ('d_mid','Pengurangan skenario Menengah','{sq_bau}-{sq_mid}','MtCO2 per tahun','AC','hitungan sederhana','calc'),
       ('d_hi','Pengurangan skenario Tinggi','{sq_bau}-{sq_hi}','MtCO2 per tahun','AC','hitungan sederhana','calc'),
       ('d_pln','Target PLN 11 Mt dibagi pengurangan skenario Menengah','C_Solusi_2030!E27/{d_mid}','fraksi','AC','hitungan sederhana; Squire memakai 651,7 miliar MJ untuk Menengah','calc')],
      'Co-firing biomassa')
def S_B40():
    return single('S_B40',125,'biodiesel B40',26,
      'Klaim pengurangan ESDM dibandingkan hitungan sederhana: volume biodiesel dikali faktor emisi solar. Hitungan memakai pembukuan biogenik netral tanpa alih guna lahan CPO (K138). LCA sawit (Wahyono dkk. 2020) memberi jejak netto sekitar 2,88 tCO2e per ton biodiesel (cradle to gate, belum dibandingkan solar); selisih harga per liter (biaya) belum diekstrak (R1).',
      [r for r in TRBF],
      [('Klaim ESDM (C_Solusi A3)','C_Solusi_2030!E26','C_Solusi_2030!F26','MtCO2e','E','C_Solusi_2030 A3','n2l'),
       ('ESDM sampai 2025 (catatan pengguna, K122)',32.2,32.2,'MtCO2e','E','K_Konflik K122','n2i')],
      [('lcaf','LCA per ton biodiesel: fosil (cradle to gate)',2893.613,'kg CO2e per ton','E','Wahyono dkk. 2020 Tabel 5','in'),
       ('lcab','LCA per ton biodiesel: biogenik',28.777,'kg CO2e per ton','E','Wahyono dkk. 2020 Tabel 5','in'),
       ('lcal','LCA per ton biodiesel: alih guna lahan',7.451,'kg CO2e per ton','E','Wahyono dkk. 2020 Tabel 5','in'),
       ('lcau','LCA per ton biodiesel: serapan CO2 (dikurangkan)',48.184,'kg CO2e per ton','E','Wahyono dkk. 2020 Tabel 5','in'),
       ('lcan','LCA netto: fosil + biogenik + alih guna lahan - serapan (belum diubah ke per liter; densitas biodiesel dan LCA solar belum bersumber, WP)','{lcaf}+{lcab}+{lcal}-{lcau}','kg CO2e per ton','AC','hitungan sederhana','calc'),
       ('lcaha','Lahan per ton biodiesel',0.86,'ha per ton','E','Wahyono dkk. 2020','in'),
       ('vol','Volume biodiesel 2025 (alokasi)',15.62,'juta kL','E','Fitrady dkk. 2026','in'),
       ('ef','Faktor emisi solar',2.67,'kg CO2 per liter','R','Robbi 2026 Tabel 7 (Permenperin 48 Tahun 2020)','in'),
       ('calc','Hitung: volume x faktor (biogenik netral, tanpa alih guna lahan)','{vol}*{ef}','MtCO2e per tahun','AC','hitungan sederhana: juta kL x kg per L = MtCO2','calc'),
       ('pso','Volume bersubsidi (PSO) 2025',7.54,'juta kL','E','Fitrady dkk. 2026','in'),
       ('calcpso','Hitung untuk volume bersubsidi saja','{pso}*{ef}','MtCO2e per tahun','AC','hitungan sederhana','calc'),
       ('cap','Kapasitas produksi biodiesel',15.6,'juta kL','E','Fitrady dkk. 2026','in'),
       ('b50','Kebutuhan B50',20.1,'juta kL','E','Fitrady dkk. 2026 (APROBI 2025)','in'),
       ('calcb50','Hitung B50 (kebutuhan x faktor)','{b50}*{ef}','MtCO2e per tahun','AC','hitungan sederhana','calc')],
      'B40')
d_=src.ws('D_Teknis_Opsi'); TRBIO=[r for r in range(6,320) if d_.cell(r,3).value=='Biomassa']
TRBF=[r for r in range(6,320) if d_.cell(r,3).value=='Biofuel (B40 dan B50)']
if __name__=='__main__':
    bm=_load('bmod','/home/user/NetZeroEmission/scripts/09_build_model_B.py'); gp=bm.B_Garis_Pembangunan(); sel=bm.B_Selisih(gp)
    sheets=[gp,sel,S_Pensiun(),S_CCS(),S_Cofiring(),S_B40()]
    cache,errs=build('/tmp/claude-0/base_model.xlsx','/tmp/claude-0/stageX.xlsx',sheets,[])
    print([e for e in errs if 'NA()' not in e[3]][:6])
    for s in sheets[2:]: print(s.name,cache.get((s.name,'A3'),'')[:250])

TRRC=[r for r in range(6,320) if d_.cell(r,3).value=='Rice cooker']
def _row_of(option,param):
    for r in range(6,320):
        if d_.cell(r,3).value==option and str(d_.cell(r,5).value).startswith(param): return r
def S_RiceCooker():
    r_units=_row_of('Rice cooker','Armada rice cooker program'); r_grid=_row_of('Elektrifikasi kendaraan (BEV)','EF jaringan untuk manfaat EV')
    keys=['units','lpg_lo','lpg_hi','kwh_lo','kwh_hi','efgj','gjt','eflpg','grid','grid30','lpgkt_lo','lpgkt_hi','co2l_lo','co2l_hi','gwh_lo','gwh_hi','co2e_w','co2e_b','net_lo','net_hi']
    extras=[('units','Rice cooker yang dibagikan 2023 dan 2024 (unit)',f'D_Teknis_Opsi!F{r_units}','unit','R','Suntoro dkk. 2025 (342.621 dan 127.628)','link'),
      ('lpg_lo','Pengurangan LPG 3 kg per rumah tangga, ringkasan',1.23,'kg per bulan','R','Suntoro dkk. 2025 bagian 3.3','in'),
      ('lpg_hi','Pengurangan LPG per rumah tangga, batas atas rinci',2.74,'kg per bulan','R','Suntoro dkk. 2025 bagian 3.4','in'),
      ('kwh_lo','Tambahan listrik per rumah tangga, batas bawah',4.67,'kWh per bulan','R','Suntoro dkk. 2025 bagian 3.4 (grafik PLN menunjukkan sekitar 10 sampai 11; dicatat sebagai celah)','in'),
      ('kwh_hi','Tambahan listrik per rumah tangga, batas atas',5.49,'kWh per bulan','R','Suntoro dkk. 2025 bagian 3.4','in'),
      ('efgj','Faktor emisi LPG (IPCC 2006 Tier 1)',60.6,'kgCO2e per GJ','R','Zain dkk. 2025 HEIO (D_Register_Sumber No 212)','in'),
      ('gjt','Kandungan energi LPG',52.145,'GJ per ton','R','Zain dkk. 2025 HEIO (D_Register_Sumber No 192)','in'),
      ('eflpg','Faktor emisi LPG turunan (menggantikan asumsi 2,98 di D_Teknis_Opsi)','{efgj}*{gjt}/1000','tCO2 per ton LPG','AC','hitungan sederhana; konflik di K145','calc'),
      ('grid','Faktor emisi jaringan, kasus terburuk',f'D_Teknis_Opsi!F{r_grid}','tCO2 per MWh','R','Zahari dan McLellan 2024','link'),
      ('grid30','Faktor emisi jaringan, skenario NZE 2050 (kasus terbaik)',0.282,'tCO2 per MWh','R','Greenpeace dan RDI Tabel 1 (D_Register_Sumber)','in'),
      ('lpgkt_lo','LPG dihindari armada, rendah','{units}*{lpg_lo}*12/1000000','kt per tahun','AC','hitungan sederhana (cocok 6,9 pada D_Teknis_Opsi)','calc'),
      ('lpgkt_hi','LPG dihindari armada, tinggi','{units}*{lpg_hi}*12/1000000','kt per tahun','AC','hitungan sederhana (cocok 15,5)','calc'),
      ('co2l_lo','CO2 LPG dihindari, rendah','{lpgkt_lo}*{eflpg}','ktCO2 per tahun','AC','hitungan sederhana','calc'),
      ('co2l_hi','CO2 LPG dihindari, tinggi','{lpgkt_hi}*{eflpg}','ktCO2 per tahun','AC','hitungan sederhana','calc'),
      ('gwh_lo','Listrik tambahan armada, rendah','{units}*{kwh_lo}*12/1000000','GWh per tahun','AC','hitungan sederhana','calc'),
      ('gwh_hi','Listrik tambahan armada, tinggi','{units}*{kwh_hi}*12/1000000','GWh per tahun','AC','hitungan sederhana','calc'),
      ('co2e_w','CO2 listrik tambahan, kasus terburuk (listrik tinggi x faktor terburuk)','{gwh_hi}*{grid}','ktCO2 per tahun','AC','hitungan sederhana','calc'),
      ('co2e_b','CO2 listrik tambahan, kasus terbaik (listrik rendah x faktor NZE)','{gwh_lo}*{grid30}','ktCO2 per tahun','AC','hitungan sederhana','calc'),
      ('net_lo','Pengurangan netto, kasus terburuk (LPG rendah dikurangi listrik terburuk)','{co2l_lo}-{co2e_w}','ktCO2 per tahun','AC','hitungan sederhana','calc'),
      ('net_hi','Pengurangan netto, kasus terbaik (LPG tinggi dikurangi listrik terbaik)','{co2l_hi}-{co2e_b}','ktCO2 per tahun','AC','hitungan sederhana','calc')]
    n=3; r0=16+len(TRRC)+2; rl=r0+2+n; r2=rl+3
    R=lambda k: f'C{r2+2+keys.index(k)}'
    src_=[('LPG dihindari (rendah sampai tinggi)',f'{R("co2l_lo")}/1000',f'{R("co2l_hi")}/1000','MtCO2e per tahun','AC','Tabel D','n2'),
          ('Listrik tambahan (terbaik sampai terburuk)',f'{R("co2e_b")}/1000',f'{R("co2e_w")}/1000','MtCO2e per tahun','AC','Tabel D','n2'),
          ('Pengurangan netto (terburuk sampai terbaik)',f'{R("net_lo")}/1000',f'{R("net_hi")}/1000','MtCO2e per tahun','AC','Tabel D','n2')]
    def fnd(sh,r0_,n_,r2_,refs):
        return f'"Temuan utama: program rice cooker ({{}} unit) menghindari "&ROUND({R("co2l_lo")},1)&" sampai "&ROUND({R("co2l_hi")},1)&" ktCO2 LPG per tahun tetapi menambah listrik "&ROUND({R("co2e_b")},1)&" sampai "&ROUND({R("co2e_w")},1)&" ktCO2; netto "&ROUND({R("net_lo")},1)&" sampai "&ROUND({R("net_hi")},1)&" ktCO2 per tahun, yaitu sekitar "&ROUND({R("net_hi")}/1000/B_Selisih_Penyebab!C7*100,3)&" persen selisih energi 2030 (tidak signifikan secara nasional)."'.replace('({} unit)',f'("&TEXT({R("units")},"0")&" unit)')
    sh=single('S_Rice_Cooker',128,'program rice cooker (pengganti LPG)',None,
      'Evaluasi Suntoro dkk. 2025: rice cooker gratis menggantikan LPG 3 kg untuk memasak nasi. Pengurangan netto = CO2 LPG yang dihindari dikurangi CO2 listrik tambahan; faktor LPG turunan dari IPCC 2006 Tier 1 (HEIO, Zain 2025) sehingga menggantikan asumsi 2,98 tCO2 per ton di D_Teknis_Opsi. Hanya angka bersumber dan hitungan sederhana. Biaya program belum bersumber (WP-I).',
      TRRC,src_,extras,'Program rice cooker',finding=fnd,cfmt='0.000')
    return sh
def extend_pensiun(sh):
    R=sh.refs['rg']+30
    sh.t(f'B{R}','Tabel 122.F. Enam PLTU prioritas menurut Retirement Index (Fadiilah dan Dye 2026, Tabel 3) dan padanan unit GEM di workbook','tbl')
    H=['Urutan menurut CO2','PLTU','Usia rata-rata (tahun)','CO2 2023 (MtCO2)','PM2.5 (ton per tahun)','Kumulatif CO2 (MtCO2)','Kumulatif PM2.5 (ton)','Kapasitas unit GEM di workbook (MW)','Jumlah unit GEM','Referensi resmi CM2 (MtCO2)']
    for c,t in zip('BCDEFGHIJK',H): sh.t(f'{c}{R+1}',t,'hdr')
    P=[('Banten Suralaya','Suralaya',29.63,28.51,9446),('Tanjung Jati B','Tanjung Jati B',9.83,24.01,10889),('Paiton-2','Paiton-2',23.00,11.60,3098),('Cilacap Sumber','Cilacap',11.25,11.46,5046),('Paiton-1','Paiton-1',24.00,10.81,2887),('Banten Lontar','Lontar',11.33,7.12,2218)]
    for i,(nm,key,age,co2,pm) in enumerate(P):
        r=R+2+i; sh.n(f'B{r}',i+1,'n0'); sh.t(f'C{r}',nm); sh.n(f'D{r}',age,'n2i'); sh.n(f'E{r}',co2,'n2i'); sh.n(f'F{r}',pm,'n0i')
        sh.f(f'G{r}',f'SUM($E${R+2}:E{r})','n2'); sh.f(f'H{r}',f'SUM($F${R+2}:F{r})','n0')
        sh.f(f'I{r}',f'SUMIF(C_Phasedown_Unit!$C$6:$C$152,"*{key}*",C_Phasedown_Unit!$E$6:$E$152)','n0l'); sh.f(f'J{r}',f'COUNTIF(C_Phasedown_Unit!$C$6:$C$152,"*{key}*")','n0l'); sh.f(f'K{r}','C_Solusi_2030!$E$30','n1l')
    rt=R+2+len(P)
    sh.t(f'C{rt}','Jumlah enam PLTU'); sh.f(f'E{rt}',f'SUM(E{R+2}:E{rt-1})','n2'); sh.f(f'F{rt}',f'SUM(F{R+2}:F{rt-1})','n0'); sh.f(f'I{rt}',f'SUM(I{R+2}:I{rt-1})','n0'); sh.f(f'J{rt}',f'SUM(J{R+2}:J{rt-1})','n0')
    sh.t(f'C{rt+1}','Angka dalam makalah (abstrak dan bagian 4.3)'); sh.f(f'E{rt+1}','D_Teknis_Opsi!F61','n2l'); sh.f(f'F{rt+1}','D_Teknis_Opsi!F62','n0l'); sh.f(f'I{rt+1}','D_Teknis_Opsi!F60','n0l')
    sh.t(f'C{rt+2}','Selisih jumlah tabel dikurangi angka makalah (pembulatan dan kapasitas)'); sh.f(f'E{rt+2}',f'E{rt}-E{rt+1}','n2'); sh.f(f'F{rt+2}',f'F{rt}-F{rt+1}','n0'); sh.f(f'I{rt+2}',f'I{rt}-I{rt+1}','n0')
    sh.t(f'B{rt+3}','Catatan 122.F. Kapasitas GEM di workbook lebih besar (Suralaya 6.025 MW dibanding 4.025 MW) karena unit Suralaya 9 dan 10 (2 x 1.000 MW, 2025) dan Lontar 4 (2024) dicatat di workbook tetapi tidak di makalah; ini dugaan dan dicatat di K143 (sisa 110 MW belum dijelaskan). Urutan prioritas makalah (Retirement Index per PLTU) berbeda dari urutan unit di C_Phasedown_Unit (usia dan intensitas): hanya 9 dari 28 unit enam PLTU berada di 30 peringkat teratas lembar itu.','note'); sh.merges.append(f'B{rt+3}:K{rt+3}')
    sh.refs['six_total']=rt
    # P2 intensity
    Q=rt+6
    sh.t(f'B{Q}','Tabel 122.G. Intensitas pengurangan per GW dan kapasitas setara pensiun resmi 36 Mt','tbl')
    for c,t in zip('BCDEF',['Sumber','Pengurangan (MtCO2 per tahun)','Kapasitas (GW)','Intensitas (MtCO2 per GW)','Kapasitas setara 36 Mt resmi (GW)']): sh.t(f'{c}{Q+1}',t,'hdr')
    I=[('Fadiilah dan Dye 2026, enam PLTU','D_Teknis_Opsi!F61','D_Teknis_Opsi!F60/1000'),
       ('Pihak ketiga: pensiun segera 4,5 GW (D_Energi_Potensi)','D_Energi_Potensi!E7','D_Energi_Potensi!E6'),
       ('Faktor workbook (faktor kapasitas x 8,76 x faktor emisi)','B_Pendorong!C7*B_Pendorong!C13/1000*B_Pendorong!C8','1')]
    for i,(a,fe,fg) in enumerate(I):
        r=Q+2+i; sh.t(f'B{r}',a); sh.f(f'C{r}',fe,'n2l'); sh.f(f'D{r}',fg,'n2l'); sh.f(f'E{r}',f'C{r}/D{r}','n2'); sh.f(f'F{r}',f'C_Solusi_2030!$E$30/E{r}','n2')
    sh.t(f'B{Q+5}','JETP CIPP: pensiun dini penuh, analisis sensitivitas 2030 (GW)'); sh.f(f'D{Q+5}','D_JETP!C'+str(src.find_row('D_JETP','Pensiun dini penuh',col=2,start=1,end=30)),'n2l')
    sh.t(f'B{Q+6}','Catatan: tiga sumber memberi intensitas sekitar 6,4 sampai 6,6 MtCO2 per GW; 36 Mt resmi setara sekitar 5,4 sampai 5,6 GW, dekat dengan 5,2 GW pada sensitivitas JETP (bukan skenario utama, yang tidak memensiunkan PLTU sebelum 2030).','note'); sh.merges.append(f'B{Q+6}:K{Q+6}')
    # P3 paths
    T=Q+9
    sh.t(f'B{T}','Tabel 122.H. Kapasitas PLTU yang pensiun sampai 2030 menurut jalur dan sumber, dengan emisi setara','tbl')
    for c,t in zip('BCDE',['Sumber atau jalur','Kapasitas pensiun sampai 2030 (GW)','Emisi setara (MtCO2 per tahun)','Cara']): sh.t(f'{c}{T+1}',t,'hdr')
    jm=src.find_row('D_JETP','Pensiun dini PLTU sebelum 2030',col=2,start=1,end=30); js=src.find_row('D_JETP','Pensiun dini penuh',col=2,start=1,end=30)
    rows=[('JETP CIPP skenario utama',f'D_JETP!C{jm}',f'C{T+2}*$E${Q+4}','kapasitas x intensitas workbook'),
          ('JETP CIPP sensitivitas',f'D_JETP!C{js}',f'C{T+3}*$E${Q+4}','kapasitas x intensitas workbook'),
          ('Pensiun resmi CM2 (D_Solusi_Kuantif)',f'F{Q+3}','C_Solusi_2030!E30','nilai resmi; kapasitas setara'),
          ('Jalur phase-down 2060 (C_Phasedown_Unit)','SUMIF(C_Phasedown_Unit!$L$6:$L$152,"<=2030",C_Phasedown_Unit!$E$6:$E$152)/1000',f'C{T+5}*$E${Q+4}','unit yang pensiun sampai 2030 x intensitas'),
          ('Jalur phase-down 2050','SUMIF(C_Phasedown_Unit!$M$6:$M$152,"<=2030",C_Phasedown_Unit!$E$6:$E$152)/1000',f'C{T+6}*$E${Q+4}','idem'),
          ('Jalur phase-down 2045','SUMIF(C_Phasedown_Unit!$N$6:$N$152,"<=2030",C_Phasedown_Unit!$E$6:$E$152)/1000',f'C{T+7}*$E${Q+4}','idem'),
          ('Enam PLTU prioritas (Fadiilah dan Dye 2026)','D_Teknis_Opsi!F60/1000','D_Teknis_Opsi!F61','nilai makalah')]
    for i,(a,fc,fe,how) in enumerate(rows):
        r=T+2+i; sh.t(f'B{r}',a); sh.f(f'C{r}',fc,'n2l'); sh.f(f'D{r}',fe,'n2'); sh.t(f'E{r}',how)
    sh.t(f'B{T+9}','Jadwal pensiun PLN (Hamdi dan Adhiguna 2021 via Fadiilah dan Dye 2026)'); sh.f(f'C{T+9}','D_Teknis_Opsi!F65','tl'); sh.merges.append(f'C{T+9}:K{T+9}')
    sh.t(f'B{T+10}','Catatan 122.H. Semua jalur phase-down di workbook memensiunkan lebih banyak kapasitas sebelum 2030 (6,9 sampai 11,2 GW) daripada skenario utama JETP (nol); PLN merencanakan mulai memensiunkan PLTU uap pada 2030 dan subkritis pada 2035 (K146).','note'); sh.merges.append(f'B{T+10}:K{T+10}')
    # charts
    nm='S_Pensiun_Dini'
    cat=f'{nm}!$C${R+2}:$C${R+1+len(P)}'
    c4=ck.chart_xml('Gambar 122.2. Enam PLTU prioritas: CO2 per PLTU dan kumulatif (MtCO2, kiri) dibanding 36 Mt resmi, dan PM2.5 kumulatif (ton, kanan)',[],
      [dict(val_ref=f'{nm}!$E${R+2}:$E${R+1+len(P)}',name='CO2 per PLTU',color='7F7F7F',pos='b'),
       dict(val_ref=f'{nm}!$G${R+2}:$G${R+1+len(P)}',name='CO2 kumulatif',color='C00000',pos='t'),
       dict(val_ref=f'{nm}!$K${R+2}:$K${R+1+len(P)}',name='Pensiun resmi CM2 (36 Mt)',color='2E7D32',marker='none',labels=False,dash='sysDash'),
       dict(val_ref=f'{nm}!$H${R+2}:$H${R+1+len(P)}',name='PM2.5 kumulatif (kanan)',color='7030A0',pos='t',sec=True,fmt='#,##0',dash='sysDash')],
      'MtCO2 per tahun','PLTU (urut menurut CO2)',cat,cat_numeric=False,yfmt='#,##0',ytitle2='ton PM2.5 per tahun',yfmt2='#,##0')
    c5=ck.chart_xml('Gambar 122.3. Pensiun PLTU sampai 2030: emisi setara (MtCO2, kiri) dan kapasitas (GW, kanan) menurut jalur dan sumber',[],
      [dict(val_ref=f'{nm}!$D${T+2}:$D${T+8}',name='Emisi setara (MtCO2 per tahun)',color='C00000',pos='t',fmt='#,##0.0'),
       dict(val_ref=f'{nm}!$C${T+2}:$C${T+8}',name='Kapasitas pensiun (GW, kanan)',color='1F4E79',pos='b',sec=True,fmt='#,##0.0',dash='sysDash')],
      'MtCO2 per tahun','Sumber atau jalur',f'{nm}!$B${T+2}:$B${T+8}',cat_numeric=False,yfmt='#,##0',ytitle2='GW',yfmt2='#,##0')
    sh.charts+= [(c4,(1,R-24,7600000,3900000)),(c5,(8,R-24,7600000,3900000))]
    sh.refs['R']=R; sh.refs['T']=T
    return sh
def K_Studi(res,b40row):
    sh=Sheet('K_Studi','FF7F7F7F'); r_=dict((c['name'],s) for c,s in res)
    sh.t('A1','Lembar 126. Konkordansi studi: kapasitas 2030 menurut JETP CIPP dibanding RUPTL, dan angka per solusi menurut studi yang tercatat','title')
    sh.t('A2','Menyandingkan angka dari studi mapan yang sudah tercatat di workbook, tanpa memilih satu dan tanpa menjumlahkannya. Periode RUPTL (kumulatif 2025 sampai 2030) tidak sama dengan JETP (2022 sampai 2030); perbedaan periode dicatat. Studi lain yang perlu dikumpulkan tim tercantum di RESEARCH_PLAN_TIM.md (WP-K).','title')
    sh.t('B5','Tabel 126.A. Kapasitas terbarukan 2030: JETP CIPP (tambahan 2022 ke 2030) dibanding RUPTL (kumulatif 2025 sampai 2030), GW','tbl')
    for c,t in zip('BCDEFGHI',['Teknologi','JETP 2022','JETP 2030','JETP tambahan','RUPTL RE Base kumulatif 2030','RUPTL ARED kumulatif 2030','JETP tambahan dikurangi ARED','Emisi digantikan ARED 2030 (MtCO2, tengah)']): sh.t(f'{c}6',t,'hdr')
    jr=lambda t: src.find_row('D_JETP',t,col=2,start=27,end=35)
    mp=[('PV surya',['S_Surya']),('Tenaga air',['S_PLTA','S_Mini_Hidro']),('Bayu',['S_Angin']),('Panas bumi',['S_Panas_Bumi']),('Bioenergi',['S_Bioenergi'])]
    K='K'
    for i,(t,sheets) in enumerate(mp):
        r=7+i; j=jr(t); sh.t(f'B{r}',t); sh.f(f'C{r}',f'D_JETP!C{j}','n1l'); sh.f(f'D{r}',f'D_JETP!D{j}','n1l'); sh.f(f'E{r}',f'D_JETP!E{j}','n1l')
        sh.f(f'F{r}','+'.join(f'{s}!{K}{r_[s].rows["rd"]["D3"]}' for s in sheets)+'','n1'); 
        sh.cells[f'F{r}']=('f','('+'+'.join(f'{s}!{K}{r_[s].rows["rd"]["D3"]}' for s in sheets)+')/1000',S['n1'])
        sh.f(f'G{r}','('+'+'.join(f'{s}!{K}{r_[s].rows["rd"]["D4"]}' for s in sheets)+')/1000','n1')
        sh.f(f'H{r}',f'E{r}-G{r}','n1'); sh.f(f'I{r}','+'.join(f'{s}!{K}{r_[s].rows["re"]["E7"]}' for s in sheets),'n2')
    sh.t('B13','Jumlah'); 
    for c in 'EFGHI': sh.f(f'{c}13',f'SUM({c}7:{c}11)','n1' if c!='I' else 'n2')
    sh.t('B14','Catatan 126.A. JETP CIPP memuat tambahan EBT jauh lebih besar daripada RUPTL 2025 sampai 2034 pada 2030 (terutama surya); selisih ini adalah temuan antar studi, bukan kesalahan data. Periode, definisi on-grid, dan kapasitas penyimpanan berbeda (D_JETP, D_RUPTL_Tambahan).','note'); sh.merges.append('B14:I14')
    sh.t('B17','Tabel 126.B. Angka per solusi menurut studi yang tercatat (tidak dijumlahkan)','tbl')
    for c,t in zip('BCDEFGH',['Solusi','Studi atau sumber','Besaran','Nilai','Satuan','Tahun atau basis','Status']): sh.t(f'{c}18',t,'hdr')
    E=lambda t,**k: er(t,**k)
    rows=[('Pensiun dini PLTU','D_Solusi_Kuantif (resmi, C_Solusi B1)','Pengurangan','C_Solusi_2030!E30','MtCO2e per tahun','2030 (CM2)','P'),
          ('Pensiun dini PLTU','Fadiilah dan Dye 2026 (enam PLTU)','Pengurangan','D_Teknis_Opsi!F61','MtCO2 per tahun','basis emisi 2023','R'),
          ('Pensiun dini PLTU','Studi pihak ketiga (D_Energi_Potensi)','Pengurangan segera 4,5 GW',f'D_Energi_Potensi!E{E("Pensiun dini PLTU on-grid segera (4,5 GW)")}','MtCO2 per tahun','segera','E'),
          ('Pensiun dini PLTU','JETP CIPP','Pensiun sebelum 2030','D_JETP!C'+str(src.find_row("D_JETP","Pensiun dini PLTU sebelum 2030",col=2,start=1,end=30)),'GW','2030','P'),
          ('Pensiun dini PLTU','Studi pihak ketiga (D_Energi_Potensi)','Batalkan sembilan PLTU baru',f'D_Energi_Potensi!E{E("Batalkan sembilan PLTU baru dari pipeline PLN")}','MtCO2 kumulatif','kumulatif','E'),
          ('PLTU captive','Ember via D_Energi_Potensi','Emisi 2024',f'D_Energi_Potensi!E{E("Emisi PLTU captive fosil")}','MtCO2','2024','E'),
          ('PLTU captive','JETP 2025 via D_Energi_Potensi','Kapasitas semua bahan bakar',f'D_Energi_Potensi!E{E("Kapasitas captive semua bahan bakar")}','GW','2024','E'),
          ('Surya','IESR via D_Energi_Potensi','Terpasang',f'D_Energi_Potensi!E{E("Surya terpasang")}','GW','kuartal 1 2026','E'),
          ('Surya','JETP CIPP','PV surya 2030','D_JETP!D'+str(jr('PV surya')),'GW','2030','P'),
          ('Surya','D_Energi_Potensi','Jalur komitmen net zero',f'D_Energi_Potensi!E{E("Surya pada jalur komitmen net zero")}','GW','jalur','E'),
          ('Surya','D_Energi_Potensi','Program 100 GWp: investasi',f'D_Energi_Potensi!E{E("Program 100 GWp: investasi sampai 2030")}','USD miliar','sampai 2030','E'),
          ('CCS PLTU','ERIA CCS 2025 (D_Teknis_Opsi)','Satu unit 1.000 MW','D_Teknis_Opsi!F67','MtCO2 per tahun','CF 0,86','R'),
          ('Co-firing','PLN dan ENDC (C_Solusi A4)','Pengurangan','C_Solusi_2030!E27','MtCO2e per tahun','2030','T'),
          ('Co-firing','Squire dkk. 2024','Rentang skenario rendah',14.2,'MtCO2 per tahun','2030','E'),
          ('Co-firing','Squire dkk. 2024','Rentang skenario tinggi',152.5,'MtCO2 per tahun','2030','E'),
          ('B40','Klaim ESDM (C_Solusi A3)','Pengurangan','C_Solusi_2030!E26','MtCO2e per tahun','2025','E'),
          ('B40','Hitung dari Fitrady dkk. 2026 dan Robbi 2026','Volume x faktor solar','S_B40!C'+str(0),'MtCO2e per tahun','2025','AC')]
    # B40 calc cell reference resolved later
    for i,(a,b,c_,v,u,y,st) in enumerate(rows):
        r=19+i; sh.t(f'B{r}',a); sh.t(f'C{r}',b); sh.t(f'D{r}',c_)
        if isinstance(v,(int,float)): sh.n(f'E{r}',v,'n2i')
        elif v=='S_B40!C0': sh.f(f'E{r}',f'S_B40!C{b40row}','n2l')
        else: sh.f(f'E{r}',v,'n2l')
        sh.t(f'F{r}',u); sh.t(f'G{r}',y); sh.t(f'H{r}',st)
    sh.width('A','A',3); sh.width('B','B',26); sh.width('C','C',44); sh.width('D','D',30); sh.width('E','I',20)
    cats='K_Studi!$B$7:$B$11'
    c1=ck.chart_xml('Gambar 126.1. Kapasitas terbarukan 2030: JETP dibanding RUPTL (GW, kiri) dan emisi yang digantikan ARED (MtCO2, kanan)',[],
        [dict(val_ref='K_Studi!$E$7:$E$11',name_ref='K_Studi!$E$6',name='JETP tambahan',color='2E7D32',pos='t',fmt='#,##0.0'),
         dict(val_ref='K_Studi!$F$7:$F$11',name_ref='K_Studi!$F$6',name='RUPTL RE Base',color='1F4E79',pos='b',fmt='#,##0.0'),
         dict(val_ref='K_Studi!$G$7:$G$11',name_ref='K_Studi!$G$6',name='RUPTL ARED',color='7F7F7F',pos='b',fmt='#,##0.0',labels=False),
         dict(val_ref='K_Studi!$I$7:$I$11',name_ref='K_Studi!$I$6',name='Emisi digantikan ARED (kanan)',color='C00000',pos='t',sec=True,fmt='#,##0.0',dash='sysDash')],
        'GW','Teknologi',cats,cat_numeric=False,yfmt='#,##0',ytitle2='MtCO2 per tahun',yfmt2='#,##0')
    sh.charts=[(c1,(1,41,7600000,3900000))]
    sh.f('A3','"Temuan utama: JETP CIPP menambah "&ROUND(E7,1)&" GW surya pada 2030 sedangkan RUPTL RE Base mencatat "&ROUND(F7,1)&" GW dan ARED "&ROUND(G7,1)&" GW; secara total JETP "&ROUND(E13,1)&" GW terhadap RUPTL ARED "&ROUND(G13,1)&" GW (periode berbeda)."','title')
    return sh
def Q_Portofolio(pf,res,fsheets,pen=None):
    sh=Sheet('Q_Portofolio','FF7F7F7F'); pos=pf.pos
    sh.t('A1','Lembar 127. Pemeriksaan portofolio dan lembar solusi','title')
    sh.t('A2','Pemeriksaan otomatis agar tidak ada hitung ganda atau angka tanpa asal: jumlah lapis sama dengan C_Solusi_2030, rantai hitung FOLU sama dengan C_Portofolio_FOLU_2030, faktor kapasitas wajar, dan jumlah sektor sama dengan total SNDC.','title')
    for c,t in zip('BCDEF',['Pemeriksaan','Nilai','Toleransi','Hasil','Penjelasan']): sh.t(f'{c}5',t,'hdr')
    fe,le,ff,lf=pos['first_en'],pos['last_en'],pos['first_fo'],pos['last_fo']
    checks=[('Jumlah lapis B energi (P_Portofolio) dikurangi C_Solusi_2030',f'ABS(P_Portofolio!G{le+1}-SUM(C_Solusi_2030!E30:E36))+ABS(P_Portofolio!H{le+1}-SUM(C_Solusi_2030!F30:F36))',0.001,'Jumlah rendah dan tinggi harus sama'),
            ('Jumlah lapis B FOLU (P_Portofolio) dikurangi C_Solusi_2030',f'ABS(P_Portofolio!G{lf+1}-SUM(C_Solusi_2030!E55:E65))+ABS(P_Portofolio!H{lf+1}-SUM(C_Solusi_2030!F55:F65))',0.001,'Jumlah rendah dan tinggi harus sama'),
            ('Rantai hitung 10 lembar FOLU dikurangi C_Portofolio_FOLU_2030','+'.join(f'{s.name}!C30' for s in fsheets),0.001,'Luas x faktor sama dengan hasil C_Portofolio_FOLU_2030'),
            ('Faktor kapasitas di luar (0, 1] pada 7 lembar terbarukan','+'.join(f'IF(AND({c["name"]}!C17>0,{c["name"]}!C17<=1),0,1)' for c,_ in res),0,'Setiap faktor kapasitas harus wajar'),
            ('Jumlah sektor SNDC dikurangi neto, selisih 2030 (MtCO2e)','ABS(SUM(B_Selisih_Penyebab!C7:C11)-B_Selisih_Penyebab!C12)',0.5,'Pembulatan SNDC'),
            ('Jumlah sektor SNDC dikurangi neto, selisih 2060 (MtCO2e)','ABS(SUM(B_Selisih_Penyebab!E7:E11)-B_Selisih_Penyebab!E12)',0.5,'Pembulatan SNDC'),
            ('Persen kumulatif energi sampai pihak ketiga tidak melebihi 100 persen',f'MAX(0,P_Portofolio!R{pos["erows"]["B6"]}-1)',0,'B7 menutup sisa sehingga tidak dihitung'),
            ('Jumlah CO2 enam PLTU (tabel) dikurangi angka makalah 93,52 (MtCO2)',f'ABS(S_Pensiun_Dini!E{pen.refs["six_total"]}-93.52)' if pen else '0',0.05,'Pembulatan Tabel 3 Fadiilah dan Dye'),
            ('Galat rumus pada kolom utama P_Portofolio',f'SUMPRODUCT(--ISERROR(P_Portofolio!G6:R{lf+1}))',0,'Tidak boleh ada galat')]
    for i,(a,f_,tol,ex) in enumerate(checks):
        r=6+i; sh.t(f'B{r}',a); sh.f(f'C{r}',f_,'n2'); sh.n(f'D{r}',tol,'n2i'); sh.f(f'E{r}',f'IF(C{r}<=D{r},"OK","Periksa")','tl'); sh.t(f'F{r}',ex)
    n=len(checks)
    sh.t(f'B{7+n}','Jumlah pemeriksaan yang perlu diperiksa'); sh.f(f'C{7+n}',f'COUNTIF(E6:E{5+n},"Periksa")','n0'); 
    sh.f('A3',f'"Temuan utama: "&COUNTIF(E6:E{5+n},"OK")&" dari {n} pemeriksaan lulus; "&C{7+n}&" perlu diperiksa."','title')
    sh.width('A','A',3); sh.width('B','B',70); sh.width('C','D',14); sh.width('E','E',12); sh.width('F','F',60)
    return sh
