import re,glob,os
out=[]
js={f:open(f,errors='ignore').read() for f in glob.glob('wv/**/*.js',recursive=True)}
allt='\n'.join(js.values())
tags=sorted(set(re.findall(r'"((?:bit|app)-[a-z0-9-]*(?:nav|layout|header|footer|navigation|side)[a-z0-9-]*)"',allt)))
out.append('## nav/layout element tags'); out.append(' '.join(tags))
for tag in ['bit-layout','bit-side-nav','bit-nav-group','bit-nav-item','app-header','app-user-layout','app-organization-layout','app-vault-banners','bit-banner']:
    for f,t in js.items():
        i=t.find('"%s"'%tag)
        if i>=0:
            out.append('--- %s in %s\n%s'%(tag,os.path.basename(f),t[max(0,i-700):i+900])); break
open('report/v9.txt','w').write('\n'.join(out))
