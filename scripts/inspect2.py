import re,glob
css=open(glob.glob('wv/styles.*.css')[0],errors='ignore').read()
out=[]
for key in ['--color-bg-nav:','--color-bg-nav-hover:','--color-fg-nav:','--color-border-nav-divider:','--color-brand-500:','--color-bg-brand:','--color-fg-brand:','--color-gray-900:']:
    for m in re.finditer(re.escape(key),css):
        # find enclosing selector
        st=css.rfind('{',0,m.start()); sel=css[max(0,css.rfind('}',0,st)+1):st].strip()[-70:]
        out.append('%s  [%s]  %s'%(key, sel, css[m.start():css.find(';',m.start())+1][:90]))
open('report/v7.txt','w').write('\n'.join(out))
