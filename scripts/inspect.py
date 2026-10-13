import re,glob,subprocess
out=[]
css=open(glob.glob('wv/styles.*.css')[0],errors='ignore').read()
out.append("## css new-logo-themed")
for m in re.finditer(r'[^}]{0,80}new-logo-themed[^{]*\{[^}]*\}',css): out.append(m.group(0))
out.append("## bwi-bitwarden-shield")
for m in re.finditer(r'\.bwi-bitwarden-shield[^}]*\}',css): out.append(m.group(0))
js=open(glob.glob('wv/app/main.*.js')[0],errors='ignore').read()
out.append("## svg literals")
for vb in ['0 0 290 60','0 0 800 200','0 0 580 104','0 0 684 291','0 0 60 60']:
    m=re.search('viewBox="%s"'%re.escape(vb),js)
    if not m: out.append('--- %s not found'%vb); continue
    st=js.rfind('<svg',0,m.start()); en=js.find('</svg>',m.end())
    seg=js[max(0,st-200):en+6]
    out.append('--- %s len %d'%(vb,en-st)); out.append(seg[:900]+(' ...[cut]... '+seg[-200:] if len(seg)>1100 else seg[900:]))
open('report/web-vault5.txt','w').write("\n".join(out))
