import zipfile,re,shutil
src='/home/user/NetZeroEmission/Indonesia_NZE_Data_Grafik_v2 (4).xlsx'
dst='fixed.xlsx'
zi=zipfile.ZipFile(src); zo=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
stat=dict(panes=0,base=0,dash=0)
for it in zi.infolist():
    d=zi.read(it.filename)
    n=it.filename
    if re.match(r'xl/worksheets/sheet\d+\.xml$',n):
        s=d.decode('utf8')
        s2=re.sub(r'<pane\b[^>]*/>','',s); s2=re.sub(r'<selection\b[^>]*/>','',s2)
        if s2!=s: stat['panes']+=1
        d=s2.encode('utf8')
    elif n=='xl/sharedStrings.xml':
        s=d.decode('utf8'); s2=s.replace('2013–2020','2013 sampai 2020')
        stat['dash']+=s!=s2; d=s2.encode('utf8')
    elif re.match(r'xl/charts/chart\d+\.xml$',n):
        s=d.decode('utf8')
        if '<tx><v>base</v></tx>' in s:
            s=s.replace('<tx><v>base</v></tx>','<tx><v> </v></tx>',1); stat['base']+=1; d=s.encode('utf8')
    zo.writestr(it,d)
zo.close(); print(stat)
