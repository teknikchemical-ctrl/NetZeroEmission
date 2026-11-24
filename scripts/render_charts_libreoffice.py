import uno,sys,os
from com.sun.star.beans import PropertyValue
def pv(n,v):
    p=PropertyValue();p.Name=n;p.Value=v;return p
ctx=uno.getComponentContext()
r=ctx.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",ctx)
c=r.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
desk=c.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",c)
doc=desk.loadComponentFromURL("file:///tmp/claude-0/master.xlsx","_blank",0,(pv("Hidden",True),pv("ReadOnly",True)))
gf=c.ServiceManager.createInstanceWithContext("com.sun.star.drawing.GraphicExportFilter",c)
n=0
for sh in doc.Sheets:
    dp=sh.DrawPage
    for i in range(dp.Count):
        s=dp.getByIndex(i)
        gf.setSourceDocument(s)
        out="file:///tmp/claude-0/-home-user-NetZeroEmission/6b48b53e-8518-5cb3-a4f8-cbf5020cc249/scratchpad/png/%s_%02d.png"%(sh.Name,i)
        gf.filter((pv("URL",out),pv("MediaType","image/png"),pv("FilterData",uno.Any("[]com.sun.star.beans.PropertyValue",(pv("PixelWidth",900),pv("PixelHeight",560))))))
        n+=1
print(n,"exported")
doc.close(True)
