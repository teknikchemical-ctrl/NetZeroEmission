"""Rakit seluruh model ke Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx. Base: git show 41dafa7:Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx > /tmp/claude-0/base_model.xlsx (keadaan sebelum model, setelah audit dan pencatatan sumber)."""
import sys,os,importlib.util,subprocess,shutil
OUT_ARG=sys.argv[1] if len(sys.argv)>1 else '/tmp/claude-0/model_full.xlsx'
sys.path.insert(0,'/home/user/NetZeroEmission/scripts')
from modelkit import *
def load(n,p):
    spec=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(spec); sys.argv=['x']; spec.loader.exec_module(m); return m
S='/home/user/NetZeroEmission/scripts/'
bm=load('bm',S+'09_build_model_B.py'); pm=load('pm',S+'10_build_model_P.py'); sm=load('sm',S+'11_build_model_S.py'); xm=load('xm',S+'12_build_model_X.py')
BASE='/tmp/claude-0/base_model.xlsx'
OUT=OUT_ARG
def main(out=OUT):
    pend=bm.B_Pendorong(); gp=bm.B_Garis_Pembangunan(); nze=bm.B_Garis_NZE(gp); sel=bm.B_Selisih(gp)
    pf=pm.P_Portofolio(sel); gf=pm.G_Portofolio(pf)
    res=[(c,sm.re_sheet(c)) for c in sm.RE_CFG]; rek=sm.EBT_Rekap(res)
    fs=[sm.folu_sheet(c) for c in sm.FOLU_CFG]
    pen=xm.extend_pensiun(xm.S_Pensiun()); ccs=xm.S_CCS(); cof=xm.S_Cofiring(); b40=xm.S_B40(); rice=xm.S_RiceCooker()
    ks=xm.K_Studi(res,b40.refs['refs']['calc']); qs=xm.Q_Portofolio(pf,res,fs,pen)
    order=[pf,gf,pend,gp,nze,sel]+[s for _,s in res]+[rek]+fs+[pen,ccs,cof,b40,rice,ks,qs]
    nums={'P_Portofolio':102,'G_Portofolio':103,'B_Pendorong':98,'B_Garis_Pembangunan':99,'B_Garis_NZE':100,'B_Selisih_Penyebab':101,'S_EBT_Rekap':111,'S_Pensiun_Dini':122,'S_CCS_TJB':123,'S_Cofiring':124,'S_B40':125,'S_Rice_Cooker':128,'K_Studi':126,'Q_Portofolio':127}
    for c,s in res: nums[s.name]=c['nomor']
    for c,s in zip(sm.FOLU_CFG,fs): nums[s.name]=c['nomor']
    jen=lambda n: 'Portofolio' if n.startswith(('P_','G_')) else ('Model' if n.startswith('B_') else ('Solusi' if n.startswith('S_') else 'Catatan'))
    desc={'P_Portofolio':'Tabel utama portofolio: pengurangan, biaya, investasi, pelaksanaan, kumulatif, persen selisih 2030','G_Portofolio':'Grafik portofolio: penutupan selisih menurut tahap, kurva biaya, biaya kumulatif',
          'B_Pendorong':'Pendorong garis pembangunan dari rencana: aktivitas x faktor emisi','B_Garis_Pembangunan':'Garis pembangunan dan jalur LCCP_L per sektor, model v2.1, inventaris','B_Garis_NZE':'Garis net zero (LCCP_L) dan jalur bersumber lain','B_Selisih_Penyebab':'Selisih menurut sektor, pendorong, dan CM1 yang belum terkirim',
          'S_EBT_Rekap':'Rekap terbarukan terukur dari RUPTL dan uji silang','S_Pensiun_Dini':'Solusi pensiun dini PLTU: sumber, biaya','S_CCS_TJB':'Solusi CCS PLTU Tanjung Jati B','S_Cofiring':'Solusi co-firing biomassa','S_B40':'Solusi biodiesel B40','S_Rice_Cooker':'Solusi program rice cooker pengganti LPG','K_Studi':'Konkordansi studi: JETP dibanding RUPTL dan angka per solusi','Q_Portofolio':'Pemeriksaan portofolio dan lembar solusi'}
    idx=[(nums[s.name],s.name,jen(s.name),desc.get(s.name,'Solusi '+s.name[2:].replace('_',' ')+': tabel teknis, pengurangan emisi, biaya, pelaksanaan'),'C_Solusi_2030, D_Teknis_Opsi, D_RUPTL_Tambahan' if s.name.startswith('S_') else 'D_ dan C_ (lihat lembar)') for s in sorted(order,key=lambda z:nums[z.name])]
    for s_ in order:
        if any(k=='f' and 'NA()' in v for k,v,_ in s_.cells.values()) and 'A2' in s_.cells:
            k,v,st=s_.cells['A2']; s_.cells['A2']=(k,v+' Sel #N/A sengaja sebagai celah garis grafik (tidak ada data bersumber).',st)
    cache,errs=build(BASE,out,order,idx,front=['P_Portofolio','G_Portofolio'])
    bad=[e for e in errs if 'NA()' not in e[3] and 'IFERROR' not in e[3]]
    print('sheets',len(order),'charts',sum(len(s.charts) for s in order),'unexpected errors',len(bad)); print(bad[:10])
    for s in (pf,gf,qs): print(s.name,cache.get((s.name,'A3'),'')[:300])
    return order,cache
if __name__=='__main__': main()
