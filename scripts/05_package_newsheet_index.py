import re,zipfile,shutil
from xml.sax.saxutils import escape
P='/home/user/NetZeroEmission/Indonesia_NZE_Data_Grafik_v2_LATEST.xlsx'
newsheet=open('newsheet.xml',encoding='utf8').read()
zi=zipfile.ZipFile(P); items=[(i,zi.read(i.filename)) for i in zi.infolist()]; zi.close()
info={}
sst=[d for i,d in items if i.filename=='xl/sharedStrings.xml'][0].decode('utf8')
# find Jenis string used for a C_ sheet in Indeks, via a row for C_Solusi_2030
zo=zipfile.ZipFile(P,'w',zipfile.ZIP_DEFLATED)
def shift_rows(s,start,by):
    i=s.find(f'<row r="{start}"'); head,tail=s[:i],s[i:]
    j=tail.find('</sheetData>'); body,rest=tail[:j],tail[j:]
    body=re.sub(r'<row r="(\d+)"',lambda m:f'<row r="{int(m.group(1))+by}"',body)
    body=re.sub(r'<c r="([A-Z]+)(\d+)"',lambda m:f'<c r="{m.group(1)}{int(m.group(2))+by}"',body)
    rest=re.sub(r'<mergeCell ref="([A-Z]+)(\d+):([A-Z]+)(\d+)"/>',lambda m:f'<mergeCell ref="{m.group(1)}{int(m.group(2))+by if int(m.group(2))>=start else m.group(2)}:{m.group(3)}{int(m.group(4))+by if int(m.group(4))>=start else m.group(4)}"/>',rest)
    return head+body+rest
for it,d in items:
    n=it.filename
    if n=='xl/workbook.xml':
        s=d.decode('utf8')
        s=s.replace('</sheets>','<sheet name="C_Biaya_Teknologi" sheetId="96" state="visible" r:id="rId99"/></sheets>'); d=s.encode('utf8')
    elif n=='xl/_rels/workbook.xml.rels':
        s=d.decode('utf8'); assert 'rId99"' not in s
        s=s.replace('</Relationships>','<Relationship Id="rId99" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet96.xml"/></Relationships>'); d=s.encode('utf8')
    elif n=='[Content_Types].xml':
        s=d.decode('utf8')
        s=s.replace('</Types>','<Override PartName="/xl/worksheets/sheet96.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>'); d=s.encode('utf8')
    elif n=='xl/sharedStrings.xml':
        s=d.decode('utf8'); c=s.count('K25 sampai K124'); s=s.replace('K25 sampai K124','K25 sampai K132'); print('sst K124 repl',c)
        s=re.sub('(\\d)\\s*[\u2013\u2014]\\s*(\\d)',r'\\1 sampai \\2',s); s=s.replace(' \u2014 ',': ').replace(' \u2013 ',' - ').replace('\u2013','-').replace('\u2014','-'); d=s.encode('utf8')
    elif n=='xl/worksheets/sheet4.xml':  # Indeks
        s=d.decode('utf8')
        s=shift_rows(s,101,1)
        new=('<row r="100" customFormat="false" ht="15" hidden="false" customHeight="false" outlineLevel="0" collapsed="false">'
          '<c r="A100" s="37" t="n"><v>96</v></c>'
          '<c r="B100" s="38" t="inlineStr"><is><t>C_Biaya_Teknologi</t></is></c>'
          '<c r="C100" s="39" t="inlineStr"><is><t>Hitung</t></is></c>'
          '<c r="D100" s="39" t="inlineStr"><is><t>Biaya modal, BTT tetap, umur, EPC, dan LCOE pembangkit (LEAP dan PLN); biaya modal dan BTT tetap per MWh pada diskonto 9 persen</t></is></c>'
          '<c r="E100" s="39" t="inlineStr"><is><t>D_Register_Sumber (Nursidik 2025, Cahyo 2024)</t></is></c>'
          '<c r="F100" s="40"/></row>')
        i=s.find('<row r="102"'); assert i>0; s=s[:i]+new+s[i:]
        s=s.replace('A1:G121','A1:G122')
        # internal hyperlinks: add new, drop external r:id
        s=re.sub(r'<hyperlink ref="(B\d+)" r:id="rId\d+" location="([^"]*)"',r'<hyperlink ref="\1" location="\2"',s)
        s=s.replace('</hyperlinks>','<hyperlink ref="B100" location="&apos;C_Biaya_Teknologi&apos;!A1" display="C_Biaya_Teknologi"/></hyperlinks>')
        d=s.encode('utf8')
    elif n=='xl/worksheets/sheet11.xml':
        s=d.decode('utf8'); s=re.sub(r'<hyperlink ref="([A-Z]+\d+)" r:id="rId\d+" location="([^"]*)"',r'<hyperlink ref="\1" location="\2"',s); d=s.encode('utf8')
    zo.writestr(it,d)
zo.writestr('xl/worksheets/sheet96.xml',newsheet)
zo.close()
print('ok')
