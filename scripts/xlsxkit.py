"""Helpers to add a sheet to the NZE workbook by editing the package XML directly (never re-save through LibreOffice or openpyxl)."""
import re,zipfile
from xml.sax.saxutils import escape
RA='customFormat="false" hidden="false" customHeight="false" outlineLevel="0" collapsed="false"'
def istr(ref,s,t): return f'<c r="{ref}" s="{s}" t="inlineStr"><is><t xml:space="preserve">{escape(str(t))}</t></is></c>'
def num(ref,s,v): return f'<c r="{ref}" s="{s}" t="n"><v>{v}</v></c>'
def fml(ref,s,f,v):
    if isinstance(v,str): return f'<c r="{ref}" s="{s}" t="str"><f aca="false">{escape(f)}</f><v>{escape(v)}</v></c>'
    return f'<c r="{ref}" s="{s}" t="n"><f aca="false">{escape(f)}</f><v>{v}</v></c>'
def row(r,cells,ht=None): return f'<row r="{r}" {RA}'+(f' ht="{ht}"' if ht else '')+'>'+''.join(cells)+'</row>'
def sheet_xml(rows,cols,dim,merges=(),tab='FF1BAF7A',extra=''):
    m=f'<mergeCells count="{len(merges)}">'+''.join(f'<mergeCell ref="{x}"/>' for x in merges)+'</mergeCells>' if merges else ''
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
      f'<sheetPr><tabColor rgb="{tab}"/></sheetPr><dimension ref="{dim}"/><sheetViews><sheetView showGridLines="true" workbookViewId="0"/></sheetViews><sheetFormatPr defaultRowHeight="12.8"/>'
      +cols+'<sheetData>'+''.join(rows)+'</sheetData>'+m+'<pageMargins left="0.75" right="0.75" top="1" bottom="1" header="0.5" footer="0.5"/>'+extra+'</worksheet>')
def shift_rows(s,start,by):
    i=s.find(f'<row r="{start}"')
    if i<0: return s
    head,tail=s[:i],s[i:]; j=tail.find('</sheetData>'); body,rest=tail[:j],tail[j:]
    body=re.sub(r'<row r="(\d+)"',lambda m:f'<row r="{int(m.group(1))+by}"',body)
    body=re.sub(r'<c r="([A-Z]+)(\d+)"',lambda m:f'<c r="{m.group(1)}{int(m.group(2))+by}"',body)
    def mc(m):
        a,b,c,d=m.group(1),int(m.group(2)),m.group(3),int(m.group(4))
        return f'<mergeCell ref="{a}{b+by if b>=start else b}:{c}{d+by if d>=start else d}"/>'
    rest=re.sub(r'<mergeCell ref="([A-Z]+)(\d+):([A-Z]+)(\d+)"/>',mc,rest)
    return head+body+rest
def add_sheets(path,new,index_rows):
    """new: list of (name, xml, extra_parts dict). index_rows: list of (no, name, jenis, isi, sumber)."""
    zi=zipfile.ZipFile(path); items=[(i,zi.read(i.filename)) for i in zi.infolist()]; zi.close()
    names={i.filename for i,_ in items}
    wbx=[d for i,d in items if i.filename=='xl/workbook.xml'][0].decode('utf8')
    rels=[d for i,d in items if i.filename=='xl/_rels/workbook.xml.rels'][0].decode('utf8')
    nsheet=len(re.findall(r'<sheet ',wbx)); maxid=max(int(x) for x in re.findall(r'sheetId="(\d+)"',wbx)); maxr=max(int(x) for x in re.findall(r'Id="rId(\d+)"',rels))
    maxfile=max(int(x) for x in re.findall(r'xl/worksheets/sheet(\d+)\.xml',' '.join(names)))
    add_wb='';add_rel='';add_ct='';files={}
    for k,(name,xml,extra) in enumerate(new,1):
        sid,rid,fn=maxid+k,maxr+k,maxfile+k
        add_wb+=f'<sheet name="{name}" sheetId="{sid}" state="visible" r:id="rId{rid}"/>'
        add_rel+=f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{fn}.xml"/>'
        add_ct+=f'<Override PartName="/xl/worksheets/sheet{fn}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        files[f'xl/worksheets/sheet{fn}.xml']=xml
        for p,(data,ct) in (extra or {}).items():
            files[p]=data
            if ct: add_ct+=f'<Override PartName="/{p}" ContentType="{ct}"/>'
    out=zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)
    for it,d in items:
        n=it.filename
        if n=='xl/workbook.xml': d=d.decode('utf8').replace('</sheets>',add_wb+'</sheets>').encode('utf8')
        elif n=='xl/_rels/workbook.xml.rels': d=d.decode('utf8').replace('</Relationships>',add_rel+'</Relationships>').encode('utf8')
        elif n=='[Content_Types].xml': d=d.decode('utf8').replace('</Types>',add_ct+'</Types>').encode('utf8')
        elif n=='xl/worksheets/sheet4.xml' and index_rows:   # Indeks
            s=d.decode('utf8')
            r0=max(int(x) for x in re.findall(r'<hyperlink ref="B(\d+)"',s))+1
            k=len(index_rows)
            s=shift_rows(s,r0+1,k)  # spacer and below move down
            new_rows=''
            for q,(no,name,jenis,isi,sumber) in enumerate(index_rows):
                r=r0+q
                new_rows+=(f'<row r="{r}" customFormat="false" ht="15" hidden="false" customHeight="false" outlineLevel="0" collapsed="false">'
                  f'<c r="A{r}" s="37" t="n"><v>{no}</v></c>'+istr(f'B{r}',38,name)+istr(f'C{r}',39,jenis)+istr(f'D{r}',39,isi)+istr(f'E{r}',39,sumber)+f'<c r="F{r}" s="40"/></row>')
            # insert before spacer row (old r0+1... after shift old row r0 (spacer) became r0+k)
            i=s.find(f'<row r="{r0+1+k}"'); assert i>0
            s=s[:i]+new_rows+s[i:]
            s=re.sub(r'<dimension ref="A1:G(\d+)"/>',lambda m:f'<dimension ref="A1:G{int(m.group(1))+k}"/>',s)
            hl=''.join(f'<hyperlink ref="B{r0+q}" location="&apos;{x[1]}&apos;!A1" display="{x[1]}"/>' for q,x in enumerate(index_rows))
            s=s.replace('</hyperlinks>',hl+'</hyperlinks>')
            d=s.encode('utf8')
        out.writestr(it,d)
    for p,data in files.items(): out.writestr(p,data)
    out.close()
