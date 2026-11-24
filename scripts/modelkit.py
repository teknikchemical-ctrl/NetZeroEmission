"""Small DSL to describe sheets (text, numbers, formulas with cached values) and charts; two-pass build with LibreOffice only used to COMPUTE cached values."""
import re,sys,os,subprocess,shutil,time
sys.path.insert(0,os.path.dirname(__file__))
from xlsxkit import istr,num,row as xrow,sheet_xml,add_sheets
from xml.sax.saxutils import escape
from openpyxl.utils import get_column_letter as CL, column_index_from_string as CI
# style roles (ids already present in the workbook; blue = typed input, green = link to another sheet, black = calculation)
S=dict(title=2,tbl=19,hdr=23,txt=24,txtt=39,note=63,
  n1=68,n1l=67,n1i=102,n0=100,n0l=83,n0i=103,n2=98,n2l=96,n2i=104,pc=74,pcl=73,pci=101,tl=66,ti=43)
class Sheet:
    def __init__(s,name,tab='FF1BAF7A'):
        s.name=name;s.cells={};s.widths={};s.merges=[];s.charts=[];s.tab=tab;s.heights={}
    def t(s,ref,text,style='txt'): s.cells[ref]=('t',text,S[style] if isinstance(style,str) else style)
    def n(s,ref,val,style='n1i'): s.cells[ref]=('n',val,S[style] if isinstance(style,str) else style)
    def f(s,ref,formula,style='n1'): s.cells[ref]=('f',formula,S[style] if isinstance(style,str) else style)   # formula without '='
    def blank(s,ref,style='txt'): s.cells[ref]=('b',None,S[style] if isinstance(style,str) else style)
    def width(s,c1,c2,w): s.widths[(c1,c2)]=w
    def formula_refs(s): return [r for r,(k,_,_) in s.cells.items() if k=='f']
    def xml(s,cache=None,drawing=True):
        cache=cache or {}
        rows={}
        for ref,(k,v,st) in s.cells.items():
            m=re.match(r'([A-Z]+)(\d+)$',ref); c,r=m.group(1),int(m.group(2))
            if k=='t': x=istr(ref,st,v)
            elif k=='n': x=num(ref,st,repr(float(v)) if isinstance(v,float) else v)
            elif k=='b': x=f'<c r="{ref}" s="{st}"/>'
            else:
                cv=cache.get((s.name,ref),0)
                if cv=='#N/A': x=f'<c r="{ref}" s="{st}" t="e"><f aca="false">{escape(v)}</f><v>#N/A</v></c>'
                elif isinstance(cv,str): x=f'<c r="{ref}" s="{st}" t="str"><f aca="false">{escape(v)}</f><v>{escape(cv)}</v></c>'
                else: x=f'<c r="{ref}" s="{st}" t="n"><f aca="false">{escape(v)}</f><v>{cv}</v></c>'
            rows.setdefault(r,[]).append((CI(c),x))
        body=[]
        for r in sorted(rows):
            body.append(xrow(r,[x for _,x in sorted(rows[r])],s.heights.get(r)))
        cols='<cols>'+''.join(f'<col min="{CI(a)}" max="{CI(b)}" width="{w}" customWidth="true"/>' for (a,b),w in sorted(s.widths.items(),key=lambda z:CI(z[0][0])))+'</cols>' if s.widths else ''
        maxr=max(rows) if rows else 1; maxc=max(CI(re.match(r'([A-Z]+)',r).group(1)) for r in s.cells) if s.cells else 1
        extra=[]
        for ref,(k,v,st) in s.cells.items():
            if k=='t' and st==S['tbl']:
                mm=re.match(r'([A-Z]+)(\d+)$',ref); c0,r0=CI(mm.group(1)),int(mm.group(2))
                end=c0+9
                if all(not (rr==r0 and c0<CI(re.match(r'([A-Z]+)',x).group(1))<=end) for x in s.cells for rr in [int(re.search(r'(\d+)$',x).group(1))]):
                    extra.append(f'{ref}:{CL(end)}{r0}')
        merges=list(s.merges)+[e for e in extra if e not in s.merges]
        return sheet_xml(body,cols,f'A1:{CL(maxc)}{maxr}',merges=merges,tab=s.tab)
def compute_cache(path,sheets):
    """Open path in LibreOffice (read only), recalc, return {(sheet,ref):value} for all formula cells of the given Sheet objects."""
    import uno
    from com.sun.star.beans import PropertyValue
    def pv(n,v):
        p=PropertyValue();p.Name=n;p.Value=v;return p
    ctx=uno.getComponentContext()
    r=ctx.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",ctx)
    c=r.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    desk=c.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",c)
    doc=desk.loadComponentFromURL("file://"+path,"_blank",0,(pv("Hidden",True),pv("ReadOnly",True)))
    doc.calculateAll(); out={}; errs=[]
    for sh in sheets:
        sx=doc.Sheets.getByName(sh.name)
        for ref in sh.formula_refs():
            cell=sx.getCellRangeByName(ref)
            if cell.getError()!=0: errs.append((sh.name,ref,cell.getError(),sh.cells[ref][1][:80])); out[(sh.name,ref)]='#N/A'; continue
            out[(sh.name,ref)]=cell.getString() if cell.FormulaResultType2==2 else cell.getValue()
    doc.close(True)
    return out,errs
def ensure_lo():
    try:
        import uno
        ctx=uno.getComponentContext()
        r=ctx.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",ctx)
        r.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"); return
    except Exception: pass
    subprocess.run("pkill -f soffice",shell=True)
    subprocess.Popen('soffice --headless --invisible --norestore --accept="socket,host=localhost,port=2002;urp;"',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(7)
def build(base,out,sheets,index_rows,front=()):
    """two-pass build: pass 1 with zero caches -> compute in LO -> pass 2 with real cached values."""
    ensure_lo()
    tmp='/tmp/claude-0/pass1.xlsx'; shutil.copy(base,tmp)
    add_sheets(tmp,[dict(name=s.name,xml=s.xml(),charts=s.charts) for s in sheets],index_rows,front)
    cache,errs=compute_cache(tmp,sheets)
    shutil.copy(base,out)
    add_sheets(out,[dict(name=s.name,xml=s.xml(cache),charts=s.charts) for s in sheets],index_rows,front)
    return cache,errs
