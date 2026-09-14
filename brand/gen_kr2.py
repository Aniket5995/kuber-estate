import math, json
from gen_kr import seg, rect, bowl

W=15
def parts(kx,ky,rx,ry,H=80,arm=42,dn_ext=0):
    K={}; R={}
    K['stem']=rect(kx,ky,W,H)
    jx,jy=kx+W-4,ky+H*0.52
    up_P,up_Q=(jx,jy),(kx+W+arm,ky+2)
    dn_P,dn_Q=(jx,jy),(kx+W+arm+2+dn_ext,ky+H-2+dn_ext*0.72)
    K['up']=seg(up_P,up_Q,W); K['dn']=seg(dn_P,dn_Q,W)
    R['stem']=rect(rx,ry,W,H)
    bw=arm+4; bh=H*0.5
    R['bowl']=bowl(rx,ry,W,bw,bh)
    lx=rx+W+6; ly=ry+bh-W/2
    leg_P,leg_Q=(lx-6,ly),(rx+bw-2,ry+H-2)
    R['leg']=seg(leg_P,leg_Q,W)
    geo=dict(up=(up_P,up_Q),dn=(dn_P,dn_Q),leg=(leg_P,leg_Q),rstem=((rx+W/2,ry),(rx+W/2,ry+H)),counter=(rx+W+ (bw-W*2)/2, ry+bh/2, (bw-2*W)/2-2))
    return K,R,geo

def render(K,R,geo,vb,over=(),mint_counter=False,mint_tip=False,halo=9,bg='var(--bg,#fff)'):
    o=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s">'%vb,'<g fill="currentColor" fill-rule="evenodd">']
    for p in K.values(): o.append('<path d="%s"/>'%p)
    for p in R.values(): o.append('<path d="%s"/>'%p)
    o.append('</g>')
    # weaving: each entry = (segment key, t0, t1) draws that sub-segment on top with a halo cut beneath
    for key,t0,t1 in over:
        P,Q=geo[key]
        A=(P[0]+(Q[0]-P[0])*t0, P[1]+(Q[1]-P[1])*t0); B=(P[0]+(Q[0]-P[0])*t1, P[1]+(Q[1]-P[1])*t1)
        o.append('<path d="%s" fill="%s"/>'%(seg(A,B,W+halo*2),bg))
        o.append('<path d="%s" fill="currentColor"/>'%seg(A,B,W))
    if mint_counter:
        cx,cy,r=geo['counter']; o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#d1ffca"/>'%(cx,cy,r))
    if mint_tip:
        P,Q=geo['dn']; A=(P[0]+(Q[0]-P[0])*0.78, P[1]+(Q[1]-P[1])*0.78)
        o.append('<path d="%s" fill="#d1ffca"/>'%seg(A,Q,W))
    o.append('</svg>'); return ''.join(o)

V={}
# Ascending composition, K lower arm extended so it crosses the R stem fully
K,R,g=parts(kx=6,ky=20,rx=56,ry=0,dn_ext=16)
# weave A: R stem over K upper arm (top), K lower arm over R stem (bottom)
V['weave_A']=render(K,R,g,'0 0 124 100',over=[('rstem',0.30,0.62),('dn',0.55,0.92)])
V['weave_A_counter']=render(K,R,g,'0 0 124 100',over=[('rstem',0.30,0.62),('dn',0.55,0.92)],mint_counter=True)
V['weave_A_tip']=render(K,R,g,'0 0 124 100',over=[('rstem',0.30,0.62),('dn',0.55,0.92)],mint_tip=True)
# weave B: K upper arm over R (top), R stem over K lower arm (bottom)
V['weave_B']=render(K,R,g,'0 0 124 100',over=[('up',0.55,0.98),('rstem',0.62,0.98)])
V['weave_B_counter']=render(K,R,g,'0 0 124 100',over=[('up',0.55,0.98),('rstem',0.62,0.98)],mint_counter=True)
# flat overlap with mint intersection (no weave) for comparison
from gen_kr import svg as flat
V['cut_mint']=flat(K,R,'0 0 124 100',mint=True)
json.dump(V,open('kr_variants2.json','w'))
html='''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{margin:0;background:#e5e5e5;font-family:Inter,system-ui,sans-serif;padding:24px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.c{background:#fff;border-radius:20px;padding:16px;display:flex;flex-direction:column;align-items:center;gap:10px}
.c.dark{background:#000;color:#fff;--bg:#000}.c svg{width:200px;height:auto;display:block;color:#000}.dark svg{color:#fff}
.l{font:11px ui-monospace,monospace;color:#979797;text-transform:uppercase;align-self:flex-start}
</style></head><body>'''
for k,v in V.items():
    html+='<div class="c"><span class="l">%s</span>%s</div><div class="c dark"><span class="l">%s</span>%s</div>'%(k,v,k,v)
html+='</body></html>'
open('kr_test2.html','w').write(html); print('ok', list(V))
