import json
from gen_kr import seg, rect, bowl
from gen_kr2 import parts
W=15
def render(K,R,geo,vb,over=(),mint_counter=False,halo=8,bg='var(--bg,#fff)'):
    o=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s">'%vb,'<g fill="currentColor" fill-rule="evenodd">']
    for p in K.values(): o.append('<path d="%s"/>'%p)
    for p in R.values(): o.append('<path d="%s"/>'%p)
    o.append('</g>')
    for key,t0,t1 in over:
        P,Q=geo[key]
        if key=='rstem':
            # one-sided cut: a strip just left of the R stem where the K arm approaches, then the stem redrawn
            x=P[0]-W/2; y0=P[1]+(Q[1]-P[1])*t0; y1=P[1]+(Q[1]-P[1])*t1
            o.append('<path d="%s" fill="%s"/>'%(rect(x-halo,y0,halo+1,y1-y0),bg))
            o.append('<path d="%s" fill="currentColor"/>'%rect(x,P[1],W,Q[1]-P[1]))
            continue
        A=(P[0]+(Q[0]-P[0])*t0, P[1]+(Q[1]-P[1])*t0); B=(P[0]+(Q[0]-P[0])*t1, P[1]+(Q[1]-P[1])*t1)
        o.append('<path d="%s" fill="%s"/>'%(seg(A,B,W+halo*2),bg))      # cut beneath
        o.append('<path d="%s" fill="currentColor"/>'%seg(P,Q,W))          # redraw whole element on top (no seams)
    if mint_counter:
        cx,cy,r=geo['counter']; o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#d1ffca"/>'%(cx,cy,r+0.5))
    o.append('</svg>'); return ''.join(o)

K,R,g=parts(kx=6,ky=20,rx=56,ry=0,dn_ext=11)
OVER=[('rstem',0.12,0.52),('dn',0.60,1.0)]
final=render(K,R,g,'0 0 122 100',over=OVER,mint_counter=True)
plain=render(K,R,g,'0 0 122 100',over=OVER,mint_counter=False)
open('kr-weave.svg','w').write(final+'\n'); open('kr-weave-plain.svg','w').write(plain+'\n')

# ---- sheet
head='''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kuber Estate — KR interlaced monogram</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400..500&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>
:root{--black:#000;--white:#fff;--canvas:#e5e5e5;--mist:#f3f3f3;--smoke:#979797;--slate:#444;--mint:#d1ffca}
*{box-sizing:border-box}body{margin:0;background:var(--canvas);color:#000;font-family:Inter,system-ui,sans-serif;font-size:14px;line-height:1.35;padding:32px 24px 64px}
h1{font-family:Anton,Impact,sans-serif;font-weight:400;text-transform:uppercase;font-size:44px;line-height:.9;letter-spacing:-.02em;margin:14px 0 8px}
.sub{color:var(--slate);font-size:16px;max-width:780px;margin:0 0 28px}
.mono{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11px;letter-spacing:-.02em;text-transform:uppercase;color:var(--smoke)}
.tag{display:inline-block;background:var(--mint);color:#000;border-radius:64px;padding:6px 12px;font-family:"JetBrains Mono",monospace;font-size:11px;text-transform:uppercase}
.hero{background:#fff;border-radius:32px;padding:32px;display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:20px}
.hero .big{display:flex;align-items:center;justify-content:center;background:var(--mist);border-radius:24px;min-height:320px}
.hero .big svg{width:260px;height:auto;color:#000}
.hero .big.dark{background:#000;--bg:#000}.hero .big.dark svg{color:#fff}
.concept{background:#fff;border-radius:32px;padding:28px;margin-bottom:20px}
.concept h2{font-family:Anton,Impact,sans-serif;font-weight:400;text-transform:uppercase;font-size:30px;line-height:1;margin:0 0 6px}
.concept .why{color:var(--slate);margin:0 0 20px;max-width:780px}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}
.cell{background:var(--mist);border-radius:20px;padding:18px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;min-height:180px}
.cell.dark{background:#000;color:#fff;--bg:#000}.cell.far{background:#e5e5e5;min-height:120px}
.cell .mono{align-self:flex-start}.cell.dark .mono{color:#979797}
.mark{width:104px;height:auto;color:#000}.dark .mark{color:#fff}.mark svg{width:100%;height:auto;display:block}
.tile{width:96px;height:96px;border-radius:26px;background:#000;--bg:#000;display:flex;align-items:center;justify-content:center}.tile .mark{width:66px;color:#fff}
.tile.mintt{background:var(--mint);--bg:#d1ffca}.tile.mintt .mark{color:#000}
.lockup{display:flex;align-items:center;gap:14px}.lockup .mark{width:54px}
.word{font-family:Anton,Impact,sans-serif;text-transform:uppercase;font-size:30px;line-height:.95;letter-spacing:-.01em}
.word small{display:block;font-family:"JetBrains Mono",monospace;font-size:9px;letter-spacing:.06em;color:var(--smoke);margin-top:4px}
.stack{display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center}.stack .mark{width:72px}.stack .word{font-size:22px}
.sizes{display:flex;align-items:flex-end;gap:16px}.sizes .mark{width:20px}.sizes .mark.s32{width:36px}.sizes .mark.s48{width:56px}
.far .mark{width:26px}
.note{color:var(--slate);margin-top:24px;max-width:780px}
</style></head><body>
<span class="tag">Kuber Estate · KR monogram</span>
<h1>Two letters, interlaced.</h1>
<p class="sub">A full <b>K</b> and a full <b>R</b>, woven: the R's stem passes <i>in front of</i> the K's upper arm, and the K's lower arm passes <i>in front of</i> the R's stem — a true over-under, the way a knot or a monogram on a gate is made. The R sits a step higher than the K, so the pair climbs to the right: <b>growth</b>. The mint coin in the R is Kuber's wealth — what comes back to the client. Square-cut strokes, 45° angles, one weight — it holds up as a favicon and on a hoarding.</p>
'''
def block(title, why, svgm):
    return f'''
<section class="concept">
  <h2>{title}</h2>
  <p class="why">{why}</p>
  <div class="row">
    <div class="cell"><span class="mono">Mark</span><div class="mark">{svgm}</div></div>
    <div class="cell dark"><span class="mono">On black</span><div class="mark">{svgm}</div></div>
    <div class="cell far"><span class="mono">From a distance</span><div class="mark">{svgm}</div></div>
    <div class="cell"><span class="mono">App / favicon tile</span><div class="tile"><div class="mark">{svgm}</div></div></div>
    <div class="cell"><span class="mono">Mint tile</span><div class="tile mintt"><div class="mark">{svgm}</div></div></div>
    <div class="cell" style="grid-column:span 2"><span class="mono">Lockup</span><div class="lockup"><div class="mark">{svgm}</div><div class="word">Kuber Estate<small>REAL ESTATE INVESTMENT CONSULTANTS · PUNE</small></div></div></div>
    <div class="cell"><span class="mono">Stacked</span><div class="stack"><div class="mark">{svgm}</div><div class="word">Kuber<br>Estate</div></div></div>
    <div class="cell"><span class="mono">20 / 36 / 56 px</span><div class="sizes"><div class="mark">{svgm}</div><div class="mark s32">{svgm}</div><div class="mark s48">{svgm}</div></div></div>
  </div>
</section>'''
body=f'''<div class="hero"><div class="big">{final}</div><div class="big dark">{final}</div></div>'''
body+=block('With the coin', 'The mint counter gives the mark one point of colour and a story: wealth held, and given. This is the primary version.', final)
body+=block('Pure black', 'The same weave with no accent — for stamps, embossing, single-colour print and anywhere the mint can\'t be reproduced.', plain)
tail='''<p class="note">If this is the direction, tell me what to tune: heavier or lighter strokes, more or less overlap, the R higher or level with the K, coin vs. no coin, or a version set inside a circle/square. Then I'll finalise and roll it out (nav, footer, favicon, app icon, social image).</p></body></html>'''
open('logo-kr-weave.html','w',encoding='utf-8').write(head+body+tail)
print('ok')
