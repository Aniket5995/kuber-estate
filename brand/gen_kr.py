import math, json

def seg(P, Q, w):
    """Thick line segment P->Q as a polygon (square ends)."""
    (x1,y1),(x2,y2)=P,Q
    dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy); nx,ny=-dy/L*w/2, dx/L*w/2
    pts=[(x1+nx,y1+ny),(x2+nx,y2+ny),(x2-nx,y2-ny),(x1-nx,y1-ny)]
    return 'M'+' L'.join('%.1f %.1f'%p for p in pts)+'Z'

def rect(x,y,w,h): return 'M%.1f %.1f h%.1f v%.1f h%.1f Z'%(x,y,w,h,-w)

def bowl(x, y, w, W, H):
    """R bowl as a ring: outer D from (x,y) width W height H, stroke w. evenodd."""
    r=H/2
    outer='M%.1f %.1f H%.1f A%.1f %.1f 0 0 1 %.1f %.1f H%.1f Z'%(x,y, x+W-r, r,r, x+W-r, y+H, x)
    ri=r-w
    inner='M%.1f %.1f H%.1f A%.1f %.1f 0 0 1 %.1f %.1f H%.1f Z'%(x+w,y+w, x+W-r, ri,ri, x+W-r, y+H-w, x+w)
    return outer+' '+inner

def letters(kx,ky,rx,ry,w=15,H=80,arm=42):
    """K at (kx,ky), R at (rx,ry); returns dict of named paths."""
    K={}
    K['stem']=rect(kx,ky,w,H)
    jx,jy=kx+w,ky+H*0.52
    K['up']=seg((jx-4,jy),(kx+w+arm,ky+2),w)
    K['dn']=seg((jx-4,jy),(kx+w+arm+2,ky+H-2),w)
    R={}
    R['stem']=rect(rx,ry,w,H)
    bw=arm+4; bh=H*0.5
    R['bowl']=bowl(rx,ry,w,bw,bh)
    lx=rx+w+6; ly=ry+bh-w/2
    R['leg']=seg((lx-6,ly),(rx+bw-2,ry+H-2),w)
    return K,R

def svg(K,R,vb,mint=None,weave=None,bg='var(--bg,#fff)',halo=10):
    """weave: list of (top_letter, part) segments drawn last with halo."""
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s">'%vb]
    fill='currentColor'
    out.append('<g fill="%s" fill-rule="evenodd">'%fill)
    for p in K.values(): out.append('<path d="%s"/>'%p)
    for p in R.values(): out.append('<path d="%s"/>'%p)
    out.append('</g>')
    if mint:
        # intersection K∩R in mint via clipPath
        out.append('<clipPath id="ck">'+''.join('<path d="%s" clip-rule="evenodd"/>'%p for p in K.values())+'</clipPath>')
        out.append('<g clip-path="url(#ck)" fill="#d1ffca" fill-rule="evenodd">'+''.join('<path d="%s"/>'%p for p in R.values())+'</g>')
    if weave:
        for (letter,part,pts) in weave:
            P,Q=pts
            out.append('<path d="%s" fill="%s"/>'%(seg(P,Q,15+halo), bg))
            out.append('<path d="%s" fill="%s"/>'%(seg(P,Q,15), fill))
    out.append('</svg>')
    return ''.join(out)

variants={}
# --- Composition 1: R raised (ascending), K's lower arm woven under R stem, K upper arm over the bowl
K,R=letters(kx=8,ky=20,rx=56,ry=0)
variants['ascend']=svg(K,R,'0 0 120 100')
variants['ascend_mint']=svg(K,R,'0 0 120 100',mint=True)
# --- Composition 2: K raised, single clean crossing (K lower arm x R stem), R over K
K2,R2=letters(kx=8,ky=0,rx=56,ry=20)
variants['kraised']=svg(K2,R2,'0 0 120 100')
variants['kraised_mint']=svg(K2,R2,'0 0 120 100',mint=True)
json.dump(variants,open('kr_variants.json','w'))
html='''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{margin:0;background:#e5e5e5;font-family:Inter,system-ui,sans-serif;padding:24px;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.c{background:#fff;border-radius:20px;padding:16px;display:flex;flex-direction:column;align-items:center;gap:10px}
.c.dark{background:#000;color:#fff;--bg:#000}.c svg{width:200px;height:auto;display:block;color:#000}.dark svg{color:#fff}
.l{font:11px ui-monospace,monospace;color:#979797;text-transform:uppercase;align-self:flex-start}
</style></head><body>'''
for k,v in variants.items():
    html+='<div class="c"><span class="l">%s</span>%s</div><div class="c dark"><span class="l">%s</span>%s</div>'%(k,v,k,v)
html+='</body></html>'
open('kr_test.html','w').write(html)
print('ok', list(variants))
