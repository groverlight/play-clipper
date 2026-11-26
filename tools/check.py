import json,re,bisect,sys
d=json.load(open(sys.argv[2] if len(sys.argv)>2 else 'play-clipper-debug.json')); o=json.load(open(sys.argv[3] if len(sys.argv)>3 else 'replay-out.json'))
B={float(k):v for k,v in d['bug2']['bug'].items() if v and v.get('s') is not None}; T=sorted(B)
def rd(t,tol=0.6):
    i=bisect.bisect_left(T,t-tol); c=[x for x in T[i:i+4] if abs(x-t)<=tol]
    return B[min(c,key=lambda x:abs(x-t))] if c else None
def reads(a,b): i=bisect.bisect_left(T,a); j=bisect.bisect_right(T,b); return [(x,B[x]) for x in T[i:j]]
plays=d['game']['plays']; me='2390'
skip=re.compile(r'kickoff|extra point|kick attempt|two-point|PAT|timeout|end of',re.I)
pre=re.compile(r'False Start|Delay of Game|Encroachment|Neutral Zone|Illegal (Formation|Shift|Substitution|Snap)|Too Many Men|Offside',re.I)
def cs_of(p):
    m=re.match(r'(\d+):(\d+)',p['clock'] or ''); return int(m[1])*60+int(m[2]) if m else None
def check(p,t):
    cs=cs_of(p)
    if t is None: return 'none'
    if cs is None or p['q']>4: return 'ok?'
    w=reads(t-3,t+15)
    if not w: return 'blind'
    if p.get('clkEnd'):
        # clock must run after t and stop at ~cs within 15s
        after=[v['s'] for x,v in w if x>t+0.5]
        if not after: return 'blind'
        if min(after)>cs+1: return f'end-early({min(after)-cs:+d})'
        r=rd(t-1,1.1)
        if r and r['s']<=cs+1: return f'end-late({r["s"]-cs:+d})'
        ww=reads(t-20,t+25); stop=None
        for j in range(1,len(ww)):
            if ww[j][0]>t and abs(ww[j][1]['s']-cs)<=1 and ww[j-1][1]['s']>ww[j][1]['s']: stop=j; break
        if stop:
            for j in range(stop-1,0,-1):
                b=ww[j][1]
                if not (j+1<len(ww) and ww[j+1][1]['s']<b['s']): continue
                k=j
                while k>0 and ww[k-1][1]['s']==b['s']: k-=1
                if ww[j][0]-ww[k][0]>=1.6:
                    rs=max(ww[j][0], ww[j+1][0]-(b['s']-ww[j+1][1]['s']))
                    if abs(rs-t)>2.5: return f'td-start-off({t-rs:+.1f})'
                    break
        return 'ok'
    r=rd(t-1,1.1) or rd(t-0.5,1.1) or rd(t-1,3)
    if not r: return 'blind'
    sd=r['s']-cs
    if sd<-1: return f'late({sd:+d})'
    if sd>8: return f'early({sd:+d})'
    return 'ok'
which=sys.argv[1] if len(sys.argv)>1 else 'fin'
P={k:s for k,s,*_ in o['raw']} if which=='raw' else ({k:s for k,s,*_ in o['fin']} if which=='fin' else None) or ({k:s for k,s,*_ in o['base']} if which=='base' else o['np'])
off=0; bad=[]
for i,p in enumerate(plays):
    unit='ST' if p['st'] else ('OFF' if p['off']==me else 'DEF')
    if unit=='OFF': off+=1
    if p['q']>4 or p.get('pat') or skip.search(p.get('type') or '') or re.match(r'(Kickoff|Punt|Extra point)',(p.get('sum') or {}).get('result') or '') or (('NO PLAY' in p['text']) and pre.search(p['text'])): continue
    c=check(p,P.get(p['id']))
    if c not in ('ok','ok?'): bad.append(f"{i} {unit}{(' o'+str(off)) if unit=='OFF' else ''} Q{p['q']} {p['clock']} {c} @ {P.get(p['id'])}")
print(which,'bad',len(bad)); print('\n'.join(bad))
