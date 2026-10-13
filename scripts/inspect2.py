import re,glob,os,json
out=[]
js={f:open(f,errors='ignore').read() for f in glob.glob('wv/**/*.js',recursive=True)}
out.append('## files containing footer strings')
for f,t in js.items():
    for s in ['Vaultwarden Web','A modified version of the Bitwarden','not associated with the Bitwarden']:
        if s in t: out.append('%s: %s x%d'%(os.path.basename(f),s,t.count(s)))
out.append('## layout contexts (bit-side-nav)')
n=0
for f,t in js.items():
    for m in re.finditer(r'bit-side-nav|bit-layout|"bit-nav-logo"',t):
        seg=t[max(0,m.start()-500):m.start()+600]
        if 'tw-' in seg and n<8:
            out.append('--- %s @%d\n%s'%(os.path.basename(f),m.start(),seg)); n+=1
css=open(glob.glob('wv/styles.*.css')[0],errors='ignore').read()
out.append('## illustration vars')
out.append(' '.join(sorted(set(re.findall(r'--color-illustration[\w-]*',css)))))
for m in re.finditer(r'(--color-illustration[\w-]*):\s*([^;]+);',css): out.append('%s=%s'%(m.group(1),m.group(2).strip()))
out.append('## fill classes used by illustrations')
allt=''.join(js.values())
out.append(' '.join(sorted(set(re.findall(r'tw-fill-illustration[\w-]*|tw-fill-bw-[\w-]*|tw-stroke-[\w-]*',allt)))))
out.append('## bw-blue defs')
for m in re.finditer(r'\.tw-fill-bw-blue\s*\{[^}]*\}|--color-bw-blue[^;]*;',css): out.append(m.group(0))
msgs=json.load(open('wv/locales/en/messages.json'))
out.append('## en messages still containing Bitwarden')
for k,v in msgs.items():
    if 'Bitwarden' in v.get('message',''): out.append('%s: %s'%(k,v['message'][:140]))
open('report/v8.txt','w').write('\n'.join(out))
