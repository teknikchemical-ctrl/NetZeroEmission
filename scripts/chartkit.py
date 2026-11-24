"""Build OOXML line / shaded-band charts directly (no LibreOffice or openpyxl re-save)."""
from xml.sax.saxutils import escape
NS=('xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
def _rpr(sz=900,b=False,color='404040'):
    return f'<a:defRPr sz="{sz}" b="{1 if b else 0}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="Calibri"/></a:defRPr>'
def _title(text,sz=1100,b=True,rot=None):
    bp='<a:bodyPr/>' if rot is None else f'<a:bodyPr rot="{rot}" vert="horz"/>'
    return (f'<c:title><c:tx><c:rich>{bp}<a:lstStyle/><a:p><a:pPr>{_rpr(sz,b,"262626")}</a:pPr>'
            f'<a:r><a:rPr lang="id-ID" sz="{sz}" b="{1 if b else 0}"><a:solidFill><a:srgbClr val="262626"/></a:solidFill><a:latin typeface="Calibri"/></a:rPr><a:t>{escape(text)}</a:t></a:r></a:p></c:rich></c:tx><c:overlay val="0"/></c:title>')
def _txpr(sz=900,b=False,color='404040',rot=None):
    bp='<a:bodyPr/>' if rot is None else f'<a:bodyPr rot="{rot}" vert="horz"/>'
    return f'<c:txPr>{bp}<a:lstStyle/><a:p><a:pPr>{_rpr(sz,b,color)}</a:pPr><a:endParaRPr lang="id-ID"/></a:p></c:txPr>'
def _tx(name_ref,name_text):
    if name_ref: return f'<c:tx><c:strRef><c:f>{escape(name_ref)}</c:f><c:strCache><c:ptCount val="1"/><c:pt idx="0"><c:v>{escape(name_text)}</c:v></c:pt></c:strCache></c:strRef></c:tx>'
    return f'<c:tx><c:v>{escape(name_text)}</c:v></c:tx>'
def _cat(ref,numeric): 
    return f'<c:cat><c:numRef><c:f>{escape(ref)}</c:f></c:numRef></c:cat>' if numeric else f'<c:cat><c:strRef><c:f>{escape(ref)}</c:f></c:strRef></c:cat>'
def _dlbls(show,fmt,pos,color):
    if not show: return '<c:dLbls><c:delete val="1"/></c:dLbls>'
    return (f'<c:dLbls><c:numFmt formatCode="{escape(fmt)}" sourceLinked="0"/><c:spPr><a:noFill/><a:ln><a:noFill/></a:ln></c:spPr>{_txpr(800,True,color)}'
            f'<c:dLblPos val="{pos}"/><c:showLegendKey val="0"/><c:showVal val="1"/><c:showCatName val="0"/><c:showSerName val="0"/><c:showPercent val="0"/><c:showBubbleSize val="0"/></c:dLbls>')
def line_ser(idx,cat_ref,val_ref,name_ref=None,name='',color='1F4E79',width=25400,dash=None,marker='circle',msize=7,labels=True,fmt='#,##0.0',pos='t',cat_numeric=True):
    d=f'<a:prstDash val="{dash}"/>' if dash else ''
    mk=('<c:marker><c:symbol val="none"/></c:marker>' if marker=='none' else
        f'<c:marker><c:symbol val="{marker}"/><c:size val="{msize}"/><c:spPr><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:ln w="9525"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:ln></c:spPr></c:marker>')
    return (f'<c:ser><c:idx val="{idx}"/><c:order val="{idx}"/>{_tx(name_ref,name)}'
            f'<c:spPr><a:ln w="{width}" cap="rnd"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>{d}<a:round/></a:ln></c:spPr>{mk}'
            f'{_dlbls(labels,fmt,pos,color)}{_cat(cat_ref,cat_numeric)}<c:val><c:numRef><c:f>{escape(val_ref)}</c:f></c:numRef></c:val><c:smooth val="0"/></c:ser>')
def area_ser(idx,cat_ref,val_ref,name_ref=None,name='',fill=None,alpha=None,cat_numeric=True):
    if fill:
        a=f'<a:alpha val="{alpha}"/>' if alpha else ''
        sp=f'<c:spPr><a:solidFill><a:srgbClr val="{fill}">{a}</a:srgbClr></a:solidFill><a:ln><a:noFill/></a:ln></c:spPr>'
    else: sp='<c:spPr><a:noFill/><a:ln><a:noFill/></a:ln></c:spPr>'
    return (f'<c:ser><c:idx val="{idx}"/><c:order val="{idx}"/>{_tx(name_ref,name)}{sp}<c:dLbls><c:delete val="1"/></c:dLbls>'
            f'{_cat(cat_ref,cat_numeric)}<c:val><c:numRef><c:f>{escape(val_ref)}</c:f></c:numRef></c:val></c:ser>')
def chart_xml(title,bands,lines,ytitle,xtitle,cat_ref,cat_numeric=True,yfmt='#,##0',xfmt='General',ymin=None,ymax=None,legend='b',note=None,ytitle2=None,yfmt2='#,##0'):
    """bands: list of dict(base_ref,band_ref,name_ref,name,fill,alpha). lines: list of dict for line_ser (without idx/cat)."""
    sers=[];hide=[];k=0;areas=''
    for b in bands:
        areas+=area_ser(k,cat_ref,b['base_ref'],name=' ',cat_numeric=cat_numeric); hide.append(k); k+=1
        areas+=area_ser(k,cat_ref,b['band_ref'],b.get('name_ref'),b.get('name',''),b.get('fill','F4B183'),b.get('alpha',55000),cat_numeric); k+=1
    ls='';ls2=''
    for l in lines:
        l=dict(l); sec=l.pop('sec',False)
        x=line_ser(k,cat_ref,cat_numeric=cat_numeric,**l); k+=1
        if sec: ls2+=x
        else: ls+=x
    plot=''
    if areas: plot+=f'<c:areaChart><c:grouping val="stacked"/><c:varyColors val="0"/>{areas}<c:axId val="50010"/><c:axId val="50020"/></c:areaChart>'
    plot+=f'<c:lineChart><c:grouping val="standard"/><c:varyColors val="0"/>{ls}<c:marker val="1"/><c:axId val="50010"/><c:axId val="50020"/></c:lineChart>'
    if ls2: plot+=f'<c:lineChart><c:grouping val="standard"/><c:varyColors val="0"/>{ls2}<c:marker val="1"/><c:axId val="50030"/><c:axId val="50040"/></c:lineChart>'
    sc='<c:scaling><c:orientation val="minMax"/>'+(f'<c:max val="{ymax}"/>' if ymax is not None else '')+(f'<c:min val="{ymin}"/>' if ymin is not None else '')+'</c:scaling>'
    grid='<c:majorGridlines><c:spPr><a:ln w="6350"><a:solidFill><a:srgbClr val="D9D9D9"/></a:solidFill></a:ln></c:spPr></c:majorGridlines>'
    axln='<c:spPr><a:ln w="9525"><a:solidFill><a:srgbClr val="7F7F7F"/></a:solidFill></a:ln></c:spPr>'
    catax=(f'<c:catAx><c:axId val="50010"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:delete val="0"/><c:axPos val="b"/>{_title(xtitle,900,True)}'
           f'<c:numFmt formatCode="{escape(xfmt)}" sourceLinked="0"/><c:majorTickMark val="out"/><c:minorTickMark val="none"/><c:tickLblPos val="low"/>{axln}{_txpr(900)}'
           '<c:crossAx val="50020"/><c:crosses val="autoZero"/><c:auto val="1"/><c:lblAlgn val="ctr"/><c:lblOffset val="100"/><c:noMultiLvlLbl val="0"/></c:catAx>')
    valax=(f'<c:valAx><c:axId val="50020"/>{sc}<c:delete val="0"/><c:axPos val="l"/>{grid}{_title(ytitle,900,True,rot="-5400000")}'
           f'<c:numFmt formatCode="{escape(yfmt)}" sourceLinked="0"/><c:majorTickMark val="out"/><c:minorTickMark val="none"/><c:tickLblPos val="nextTo"/>{axln}{_txpr(900)}'
           '<c:crossAx val="50010"/><c:crosses val="autoZero"/><c:crossBetween val="midCat"/></c:valAx>')
    if ls2:
        valax+=(f'<c:valAx><c:axId val="50040"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:delete val="0"/><c:axPos val="r"/>{_title(ytitle2 or "",900,True,rot="-5400000")}'
                f'<c:numFmt formatCode="{escape(yfmt2)}" sourceLinked="0"/><c:majorTickMark val="out"/><c:minorTickMark val="none"/><c:tickLblPos val="nextTo"/>{axln}{_txpr(900)}'
                '<c:crossAx val="50030"/><c:crosses val="max"/><c:crossBetween val="midCat"/></c:valAx>'
                '<c:catAx><c:axId val="50030"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:delete val="1"/><c:axPos val="b"/><c:majorTickMark val="none"/><c:minorTickMark val="none"/><c:tickLblPos val="nextTo"/><c:crossAx val="50040"/><c:crosses val="autoZero"/><c:auto val="1"/><c:lblAlgn val="ctr"/><c:lblOffset val="100"/><c:noMultiLvlLbl val="0"/></c:catAx>')
    hid=''.join(f'<c:legendEntry><c:idx val="{i}"/><c:delete val="1"/></c:legendEntry>' for i in hide)
    leg=f'<c:legend><c:legendPos val="{legend}"/>{hid}<c:overlay val="0"/>{_txpr(900)}</c:legend>' if legend else ''
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
      f'<c:chartSpace {NS}><c:roundedCorners val="0"/><c:chart>{_title(title,1100,True)}<c:autoTitleDeleted val="0"/>'
      f'<c:plotArea><c:layout/>{plot}{catax}{valax}<c:spPr><a:noFill/></c:spPr></c:plotArea>{leg}<c:plotVisOnly val="1"/><c:dispBlanksAs val="span"/></c:chart>'
      '<c:spPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:ln w="9525"><a:solidFill><a:srgbClr val="BFBFBF"/></a:solidFill></a:ln></c:spPr>'
      '<c:printSettings><c:headerFooter/><c:pageMargins b="0.75" l="0.7" r="0.7" t="0.75" header="0.3" footer="0.3"/><c:pageSetup/></c:printSettings></c:chartSpace>')
def drawing_xml(anchors):
    """anchors: list of (col,row,cx,cy) 0-based col/row, EMU size; r:id = rId{n} in order."""
    out=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" '
         'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">')
    for n,(col,row,cx,cy) in enumerate(anchors,1):
        out+=(f'<xdr:oneCellAnchor><xdr:from><xdr:col>{col}</xdr:col><xdr:colOff>0</xdr:colOff><xdr:row>{row}</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:from><xdr:ext cx="{cx}" cy="{cy}"/>'
              f'<xdr:graphicFrame macro=""><xdr:nvGraphicFramePr><xdr:cNvPr id="{n+1}" name="Grafik {n}"/><xdr:cNvGraphicFramePr/></xdr:nvGraphicFramePr>'
              f'<xdr:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></xdr:xfrm><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart">'
              f'<c:chart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" r:id="rId{n}"/></a:graphicData></a:graphic></xdr:graphicFrame><xdr:clientData/></xdr:oneCellAnchor>')
    return out+'</xdr:wsDr>'
