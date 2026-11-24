import uno
from com.sun.star.beans import PropertyValue
def pv(n,v):
    p=PropertyValue();p.Name=n;p.Value=v;return p
ctx=uno.getComponentContext()
r=ctx.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",ctx)
c=r.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
desk=c.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",c)
doc=desk.loadComponentFromURL("file:///home/user/NetZeroEmission/Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx","_blank",0,(pv("Hidden",True),pv("ReadOnly",True)))
doc.calculateAll()
sh=doc.Sheets.getByName('C_Biaya_Teknologi')
mx=0
for addr in ['H7','I7','H8','I8','I13','H16','I16','F23','G23','G31','E37','F37','F38','C53']:
    cell=sh.getCellRangeByName(addr); print(addr,round(cell.Value,3),cell.Error)
print('A3:',sh.getCellRangeByName('A3').String[:230])
errs=0;nsh=0
for s in doc.Sheets:
    nsh+=1
    cur=s.createCursor(); cur.gotoEndOfUsedArea(False)
    rng=s.getCellRangeByPosition(0,0,cur.RangeAddress.EndColumn,cur.RangeAddress.EndRow)
    q=rng.queryFormulaCells(4)  # ERROR
    for a in q.RangeAddresses: 
        errs+= (a.EndRow-a.StartRow+1)*(a.EndColumn-a.StartColumn+1) if s.Name!='C_Deret_Opsi' else 0
print('sheets',nsh,'formula errors (excluding C_Deret_Opsi NA)',errs)
for nm in ('D_Register_Sumber','K_Konflik'):
    s=doc.Sheets.getByName(nm)
print('Q_Cek D?:',doc.Sheets.getByName('D_Register_Sumber').getCellRangeByName('A3').String)
doc.close(True)
