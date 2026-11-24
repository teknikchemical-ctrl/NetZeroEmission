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
def add_sheets(path,new,index_rows,front=()):
    """new: list of dict(name, xml, charts=[(chart_xml,(col,row,cx,cy))]) or (name,xml,None). index_rows: list of (no,name,jenis,isi,sumber)."""
    import sys,os
    sys.path.insert(0,os.path.dirname(__file__))
    from chartkit import drawing_xml
    zi=zipfile.ZipFile(path); items=[(i,zi.read(i.filename)) for i in zi.infolist()]; zi.close()
    names={i.filename for i,_ in items}
    wbx=[d for i,d in items if i.filename=='xl/workbook.xml'][0].decode('utf8')
    rels=[d for i,d in items if i.filename=='xl/_rels/workbook.xml.rels'][0].decode('utf8')
    maxid=max(int(x) for x in re.findall(r'sheetId="(\d+)"',wbx)); maxr=max(int(x) for x in re.findall(r'Id="rId(\d+)"',rels))
    maxfile=max(int(x) for x in re.findall(r'xl/worksheets/sheet(\d+)\.xml',' '.join(names)))
    maxchart=max([int(x) for x in re.findall(r'xl/charts/chart(\d+)\.xml',' '.join(names))]+[0])
    maxdraw=max([int(x) for x in re.findall(r'xl/drawings/drawing(\d+)\.xml',' '.join(names))]+[0])
    add_wb='';add_rel='';add_ct='';files={};front_wb={}
    for k,it_ in enumerate(new,1):
        if isinstance(it_,tuple): it_={'name':it_[0],'xml':it_[1],'charts':[]}
        name,xml,charts=it_['name'],it_['xml'],it_.get('charts') or []
        sid,rid,fn=maxid+k,maxr+k,maxfile+k
        tag=f'<sheet name="{name}" sheetId="{sid}" state="visible" r:id="rId{rid}"/>'
        if name in front: front_wb[name]=tag
        else: add_wb+=tag
        add_rel+=f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{fn}.xml"/>'
        add_ct+=f'<Override PartName="/xl/worksheets/sheet{fn}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        if charts:
            maxdraw+=1; dn=maxdraw
            crels=''
            for q,(cx_,anc) in enumerate(charts,1):
                maxchart+=1
                files[f'xl/charts/chart{maxchart}.xml']=cx_
                add_ct+=f'<Override PartName="/xl/charts/chart{maxchart}.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.chart+xml"/>'
                crels+=f'<Relationship Id="rId{q}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart" Target="../charts/chart{maxchart}.xml"/>'
            files[f'xl/drawings/drawing{dn}.xml']=drawing_xml([a for _,a in charts])
            files[f'xl/drawings/_rels/drawing{dn}.xml.rels']='<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+crels+'</Relationships>'
            add_ct+=f'<Override PartName="/xl/drawings/drawing{dn}.xml" ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/>'
            files[f'xl/worksheets/_rels/sheet{fn}.xml.rels']=f'<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" Target="../drawings/drawing{dn}.xml"/></Relationships>'
            xml=xml.replace('</worksheet>','<drawing r:id="rId1"/></worksheet>')
        files[f'xl/worksheets/sheet{fn}.xml']=xml
    out=zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED)
    for it,d in items:
        n=it.filename
        if n=='xl/workbook.xml':
            d=d.decode('utf8')
            k_=len(front_wb)
            if k_:
                d=re.sub(r'localSheetId="(\d+)"',lambda m:f'localSheetId="{int(m.group(1))+k_}"',d)
                d=d.replace('<sheets>','<sheets>'+''.join(front_wb[x] for x in front if x in front_wb))
            d=d.replace('</sheets>',add_wb+'</sheets>').encode('utf8')
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
