import math
# --- Keystone mark: trapezoid, top wider. Proportions from a real voussoir (taper ~12°)
KEY='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M16 28A98 98 0 0 1 84 28L66 77A46 46 0 0 0 34 77Z" fill="currentColor"/><g fill="none" stroke="var(--bg,#fff)" stroke-width="4.6" stroke-linecap="butt" stroke-linejoin="miter"><path d="M42.5 38.5v27"/><path d="M42.5 40.5h7.5a6.5 6.5 0 0 1 0 13h-7.5"/><path d="M49 53.5l9 11.5"/></g></svg>'
# with a hairline "joint": the stone reads as set, not floating
KEY2='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M16 28A98 98 0 0 1 84 28L66 77A46 46 0 0 0 34 77Z" fill="currentColor"/><g fill="none" stroke="var(--bg,#fff)" stroke-width="4.6" stroke-linecap="butt" stroke-linejoin="miter"><path d="M42.5 38.5v27"/><path d="M42.5 40.5h7.5a6.5 6.5 0 0 1 0 13h-7.5"/><path d="M49 53.5l9 11.5"/></g><path d="M8 84H92" stroke="currentColor" stroke-width="2"/></svg>'
# --- The story: an arch of stones, only the keystone filled
def arch():
    cx,cy,R,r=50,78,46,30
    n=9  # stones across 180°
    parts=[]
    for i in range(n):
        a0=math.pi - i*math.pi/n; a1=math.pi-(i+1)*math.pi/n
        p=lambda rad,a:(cx+rad*math.cos(a), cy-rad*math.sin(a))
        x0,y0=p(R,a0); x1,y1=p(R,a1); x2,y2=p(r,a1); x3,y3=p(r,a0)
        d=f'M{x0:.1f} {y0:.1f}A{R} {R} 0 0 1 {x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}A{r} {r} 0 0 0 {x3:.1f} {y3:.1f}Z'
        fill='currentColor' if i==n//2 else 'none'
        parts.append(f'<path d="{d}" fill="{fill}" stroke="currentColor" stroke-width="1.2" stroke-linejoin="miter"/>')
    legs=f'<path d="M{cx-R} {cy}v14M{cx-r} {cy}v14M{cx+r} {cy}v14M{cx+R} {cy}v14" stroke="currentColor" stroke-width="1.2"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{"".join(parts)}{legs}</svg>'
ARCH=arch()
DISC=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="currentColor"/><g transform="translate(50 50) scale(.62) translate(-50 -52)"><path d="M16 28A98 98 0 0 1 84 28L66 77A46 46 0 0 0 34 77Z" fill="var(--bg,#fff)"/><g fill="none" stroke="currentColor" stroke-width="4.6" stroke-linecap="butt" stroke-linejoin="miter"><path d="M42.5 38.5v27"/><path d="M42.5 40.5h7.5a6.5 6.5 0 0 1 0 13h-7.5"/><path d="M49 53.5l9 11.5"/></g></g></svg>'
SQ=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="24" fill="currentColor"/><g transform="translate(50 50) scale(.62) translate(-50 -52)"><path d="M16 28A98 98 0 0 1 84 28L66 77A46 46 0 0 0 34 77Z" fill="var(--bg,#fff)"/><g fill="none" stroke="currentColor" stroke-width="4.6" stroke-linecap="butt" stroke-linejoin="miter"><path d="M42.5 38.5v27"/><path d="M42.5 40.5h7.5a6.5 6.5 0 0 1 0 13h-7.5"/><path d="M49 53.5l9 11.5"/></g></g></svg>'
for n,s in [('r9-keystone',KEY),('r9-keystone-arch',ARCH),('r9-keystone-disc',DISC),('r9-keystone-square',SQ)]: open(n+'.svg','w').write(s+'\n')

html=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kuber Estate — the keystone</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--canvas:#e5e5e5;--mist:#f3f3f3;--smoke:#979797;--slate:#444}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--canvas);color:#000;font-family:Inter,system-ui,sans-serif;font-size:14px;line-height:1.5;padding:40px 28px 72px}}
h1{{font-weight:600;font-size:40px;letter-spacing:-.03em;line-height:1.05;margin:0 0 10px}}
.sub{{color:var(--slate);font-size:17px;max-width:720px;margin:0 0 32px}}
.k{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--smoke)}}
.concept{{background:#fff;border-radius:6px;padding:36px;margin-bottom:22px}}
.concept h2{{font-weight:600;font-size:22px;letter-spacing:-.02em;margin:0 0 6px}}
.concept .why{{color:var(--slate);margin:0 0 24px;max-width:720px}}
.row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}}
.cell{{background:var(--mist);padding:22px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;min-height:230px}}
.cell.dark{{background:#000;color:#fff;--bg:#000}}.cell.far{{background:#e5e5e5}}
.cell .k{{align-self:flex-start}}
svg{{display:block}}
.mark{{width:130px;color:#000}}.dark .mark{{color:#fff}}.mark svg{{width:100%;height:auto}}
.big .mark{{width:210px}}
.lockup{{display:flex;align-items:center;gap:18px;max-width:100%}}.lockup .mark{{width:54px;flex:none}}
.word{{font-weight:600;font-size:21px;letter-spacing:.2em;text-transform:uppercase;line-height:1}}
.word small{{display:block;font-weight:400;font-size:9px;letter-spacing:.22em;color:var(--smoke);margin-top:8px;text-transform:uppercase;white-space:nowrap}}
.stack{{display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center}}.stack .mark{{width:72px}}.stack .word{{font-size:14px;letter-spacing:.32em}}
.sizes{{display:flex;align-items:flex-end;gap:18px}}.sizes .mark{{width:22px}}.sizes .mark.m{{width:40px}}.sizes .mark.l{{width:64px}}
.far .mark{{width:34px}}
.quote{{font-size:22px;font-weight:500;letter-spacing:-.02em;max-width:640px;line-height:1.3;margin:0 0 6px}}
.note{{color:var(--slate);margin-top:26px;max-width:720px}}
</style></head><body>
<span class="k">Kuber Estate · identity · from scratch</span>
<h1>The keystone, with the R.</h1>
<p class="sub">Every arch in the world stands because of one stone: the wedge at the top that locks all the others in place. Remove it and the whole thing comes down. That is what Kuber Estate is inside a property deal — the verification, the judgement, the piece that makes it hold. One shape. No letters, no arrows, no accents. Built from architecture's own vocabulary, so it means the same thing in Pune, Dubai or London.</p>

<section class="concept">
  <h2>The story</h2>
  <p class="quote">"Every deal has a lot of stones. We are the one that holds it."</p>
  <p class="why">The arch shows where the mark comes from; the mark alone is what people will remember.</p>
  <div class="row">
    <div class="cell big" style="grid-column:span 2"><span class="k">Where it comes from</span><div class="mark">{ARCH}</div></div>
    <div class="cell big" style="grid-column:span 2"><span class="k">The mark</span><div class="mark">{KEY}</div></div>
  </div>
</section>

<section class="concept">
  <h2>The mark in use</h2>
  <p class="why">Solid black, the proportions of a real voussoir, and the <b>R</b> cut into the stone — the way a mason marks the one he set. Geometric R, one weight, cut clean through so it works reversed, engraved or embossed.</p>
  <div class="row">
    <div class="cell"><span class="k">Mark</span><div class="mark">{KEY}</div></div>
    <div class="cell dark"><span class="k">Reversed</span><div class="mark">{KEY}</div></div>
    <div class="cell far"><span class="k">From a distance</span><div class="mark">{KEY}</div></div>
    <div class="cell"><span class="k">Icon · disc</span><div class="mark">{DISC}</div></div>
    <div class="cell"><span class="k">Icon · square</span><div class="mark">{SQ}</div></div>
    <div class="cell dark"><span class="k">Icon, reversed</span><div class="mark">{DISC}</div></div>
    <div class="cell" style="grid-column:span 3"><span class="k">Horizontal lockup</span><div class="lockup"><div class="mark">{KEY}</div><div class="word">Kuber Estate<small>Real estate investment consultants · Pune</small></div></div></div>
    <div class="cell"><span class="k">Stacked</span><div class="stack"><div class="mark">{KEY}</div><div class="word">Kuber<br>Estate</div></div></div>
    <div class="cell dark" style="grid-column:span 3"><span class="k">Lockup, reversed</span><div class="lockup"><div class="mark">{KEY}</div><div class="word">Kuber Estate<small style="color:#979797">Real estate investment consultants · Pune</small></div></div></div>
    <div class="cell"><span class="k">22 / 40 / 64 px</span><div class="sizes"><div class="mark">{KEY}</div><div class="mark m">{KEY}</div><div class="mark l">{KEY}</div></div></div>
  </div>
</section>

<p class="note">Wordmark: Inter Semibold capitals, tracked +20% — modern, neutral, international; the mark carries the character so the type doesn't have to. Colour: black and white. Mint stays on the website as the interface accent. If this is it, I finalise the outline and roll it out across the site, favicon, app icon and share image.</p>
</body></html>'''
open('logo-round9.html','w',encoding='utf-8').write(html); print('ok')
