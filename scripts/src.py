import openpyxl,re
from openpyxl.utils import get_column_letter as CL
BASE='/tmp/claude-0/base_model.xlsx'
_wb=None
def wb():
    global _wb
    if _wb is None: _wb=openpyxl.load_workbook(BASE,data_only=True)
    return _wb
def ws(n): return wb()[n]
def find_row(sheet,text,col=None,start=1,end=None,exact=False,nth=1):
    w=ws(sheet); k=0
    for r in range(start,(end or w.max_row)+1):
        cells=[w.cell(r,col)] if col else w[r]
        for c in cells:
            v=c.value
            if isinstance(v,(int,float)) and not isinstance(v,bool): v=str(int(v)) if float(v).is_integer() else str(v)
            if isinstance(v,str) and ((v==text) if exact else v.startswith(text)):
                k+=1
                if k==nth: return r
    raise KeyError((sheet,text))
def year_cols(sheet,row):
    w=ws(sheet); d={}
    for c in w[row]:
        v=c.value
        try: y=int(float(str(v)))
        except: continue
        if 1990<y<2100: d[y]=c.column_letter
    return d
def val(sheet,ref): return ws(sheet)[ref].value
def label_col(sheet,row,text):
    for c in ws(sheet)[row]:
        if isinstance(c.value,str) and c.value.startswith(text): return c.column_letter
    raise KeyError
