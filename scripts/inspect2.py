import re,glob,os
out=[]
files=glob.glob('wv/**/*.css',recursive=True)
out.append('css files: '+' '.join(files))
for f in files:
    css=open(f,errors='ignore').read()
    for key in ['tw-bg-bg-nav','tw-bg-bg-nav-hover','tw-text-fg-nav','bg-nav','fg-nav','nav-divider']:
        for m in list(re.finditer(re.escape(key),css))[:2]:
            out.append('%s: %s :: %s'%(os.path.basename(f),key,css[max(0,m.start()-60):m.start()+160].replace('\n',' ')))
open('report/v7.txt','w').write('\n'.join(out))
