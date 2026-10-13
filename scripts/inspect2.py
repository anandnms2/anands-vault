import re,glob
css=open(glob.glob('wv/styles.*.css')[0],errors='ignore').read()
out=[]
pat=re.compile(r'(--color-(?:bg-nav|bg-nav-hover|fg-nav|border-nav|bg-brand[\w-]*|fg-brand[\w-]*|border-brand[\w-]*|bg-hover[\w-]*|brand-\d+|gray-\d+|bg-primary|bg-secondary|bg-tertiary|bg-contrast|border-[\w-]*)):\s*([^;]+);')
for m in re.finditer(r'([^{}]{0,80})\{([^{}]*--color-bg-nav[^{}]*)\}',css):
    out.append('### SELECTOR: '+m.group(1).strip()[-80:])
    out.append(' '.join('%s=%s'%(a,b.strip()) for a,b in pat.findall(m.group(2))))
# any block defining brand scale
for m in re.finditer(r'([^{}]{0,80})\{([^{}]*--color-brand-500[^{}]*)\}',css):
    out.append('### BRAND SCALE SELECTOR: '+m.group(1).strip()[-80:])
    out.append(' '.join('%s=%s'%(a,b.strip()) for a,b in re.findall(r'(--color-brand-\d+):\s*([^;]+);',m.group(2))))
open('report/v7.txt','w').write('\n'.join(out))
