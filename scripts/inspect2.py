import re,glob
out=[]
css=open(glob.glob('wv/styles.*.css')[0],errors='ignore').read()
# root blocks with --color vars
for sel in [r':root', r'\.theme_light', r'\.theme_dark']:
    for m in re.finditer(r'(?<![\w.-])'+sel+r'\s*\{([^}]*)\}',css):
        body=m.group(1)
        if '--color' in body:
            vs=re.findall(r'(--color-[\w-]+)\s*:\s*([^;]+);',body)
            out.append('## %s : %d vars'%(sel,len(vs)))
            out.append(' '.join('%s=%s'%(a,b.strip()) for a,b in vs if re.search('background|primary|nav|shadow|text-alt|bg|fg|brand|marketing',a))[:6000])
js=''.join(open(f,errors='ignore').read() for f in glob.glob('wv/**/*.js',recursive=True))
out.append('## nav classes')
cls={}
for m in re.finditer(r'(side-?nav|nav-?item|nav-?group|bit-nav|navigation)',js):
    seg=js[m.start()-300:m.start()+500]
    for c in re.findall(r'tw-(?:bg|text|border|fill|ring)-[\w\-\[\]#/.()]+',seg): cls[c]=cls.get(c,0)+1
out.append(' '.join('%s(%d)'%(k,v) for k,v in sorted(cls.items(),key=lambda x:-x[1])[:80]))
out.append('## css rules for those bg tokens')
for tok in ['tw-bg-background-alt3','tw-bg-background-alt4','tw-bg-background-alt2','tw-bg-primary-600','tw-bg-bg-brand','tw-bg-bg-contrast']:
    m=re.search(r'\.'+re.escape(tok)+r'\s*\{[^}]*\}',css)
    out.append(tok+': '+(m.group(0)[:200] if m else 'none'))
out.append('## Vaultwarden in js strings')
for m in re.finditer(r'.{60}Vaultwarden.{80}',js): out.append(m.group(0))
for d in glob.glob('wv/locales/en/messages.json'):
    t=open(d).read(); out.append('en messages Vaultwarden count: %d'%t.count('Vaultwarden'))
    for m in re.finditer(r'"message": "[^"]*Vaultwarden[^"]*"',t): out.append(m.group(0))
open('report/v6.txt','w').write('\n'.join(out))
