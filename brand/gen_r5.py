SW=5
marks = {
 'horizon': dict(title='1 — Horizon', tag='Monoline K · rising line',
   why="A single-weight <b>K</b> whose upper arm keeps going — it becomes the line on a chart, rising past the letter and ending in one mint point. The letter stays quiet and legible; the story is the line: <i>your investment, charted upward</i>. Thin, precise, lots of air — the Apple / Compass register.",
   svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"><path d="M28 20v66"/><path d="M28 56l30 30"/><path d="M28 56l54-42"/><circle cx="88" cy="9.5" r="5" fill="#d1ffca" stroke="none"/></svg>'''),
 'rooflines': dict(title='2 — Rooflines', tag='Three roofs · ascending',
   why="Three thin rooflines stepping up and away, each smaller than the last — a skyline in perspective and a staircase at once. <i>From the first home to the portfolio.</i> The mint point above the furthest roof is the destination: the one we're taking you to. Pure symbol, no letters to decode, reads at any distance.",
   svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"><path d="M8 72l26-26 26 26"/><path d="M40 46l18-18 18 18"/><path d="M64 30l12-12 12 12"/><circle cx="76" cy="7" r="4.5" fill="#d1ffca" stroke="none"/></svg>'''),
 'door': dict(title='3 — Open Door', tag='Threshold · light',
   why="A door frame in thin line, the door swung open towards you, and mint light coming through the gap. <i>We open the right door.</i> It's the warmest of the three and the one with the most personality — a small moment of welcome rather than a diagram. Still geometric, still one weight.",
   svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"><path d="M47 16H70V90" /><path d="M47 16h23v74" fill="#d1ffca" stroke="none" opacity="0"/><path d="M47 16v74H70" fill="#d1ffca" stroke="none"/><path d="M24 90V14H70v76"/><path d="M24 14L47 6v88L24 90"/></svg>'''),
}
# tidy the door: light fill = polygon of the opening (between the leaf's free edge and right jamb)
marks['door']['svg']=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"><path d="M47 6L70 14V90H47z" fill="#d1ffca" stroke="none"/><path d="M24 90V14H70v76"/><path d="M24 14L47 6v88L24 90"/></svg>'''
for k,m in marks.items(): open('r5-%s.svg'%k,'w').write(m['svg']+'\n')

head='''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kuber Estate — logo, modern premium</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300..600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>
:root{--black:#000;--white:#fff;--canvas:#e5e5e5;--mist:#f3f3f3;--smoke:#979797;--slate:#444;--mint:#d1ffca}
*{box-sizing:border-box}body{margin:0;background:var(--canvas);color:#000;font-family:Inter,system-ui,sans-serif;font-size:14px;line-height:1.4;padding:32px 24px 64px}
h1{font-weight:500;font-size:34px;letter-spacing:-.02em;line-height:1.05;margin:14px 0 8px}
.sub{color:var(--slate);font-size:16px;max-width:780px;margin:0 0 28px}
.mono{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11px;letter-spacing:-.02em;text-transform:uppercase;color:var(--smoke)}
.tag{display:inline-block;background:var(--mint);color:#000;border-radius:64px;padding:6px 12px;font-family:"JetBrains Mono",monospace;font-size:11px;text-transform:uppercase}
.concept{background:#fff;border-radius:32px;padding:28px;margin-bottom:20px}
.concept header{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:6px}
.concept h2{font-weight:500;font-size:24px;letter-spacing:-.02em;margin:0}
.concept .why{color:var(--slate);margin:0 0 20px;max-width:780px}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}
.cell{background:var(--mist);border-radius:20px;padding:18px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;min-height:190px}
.cell.dark{background:#000;color:#fff}.cell.far{background:#e5e5e5;min-height:120px}
.cell .mono{align-self:flex-start}.cell.dark .mono{color:#979797}
.mark{width:110px;height:110px;color:#000}.dark .mark{color:#fff}.mark svg{width:100%;height:100%;display:block}
.tile{width:96px;height:96px;border-radius:26px;background:#000;display:flex;align-items:center;justify-content:center}.tile .mark{width:60px;height:60px;color:#fff}
.tile .mark svg *{stroke-width:7}
.lockup{display:flex;align-items:center;gap:16px}.lockup .mark{width:48px;height:48px}
.word{font-weight:500;font-size:20px;letter-spacing:.18em;text-transform:uppercase;line-height:1}
.word small{display:block;font-family:"JetBrains Mono",monospace;font-size:9px;letter-spacing:.08em;color:var(--smoke);margin-top:7px;text-transform:uppercase}
.stack{display:flex;flex-direction:column;align-items:center;gap:12px;text-align:center}.stack .mark{width:64px;height:64px}.stack .word{font-size:15px}
.sizes{display:flex;align-items:flex-end;gap:16px}.sizes .mark{width:20px;height:20px}.sizes .mark.s32{width:36px;height:36px}.sizes .mark.s48{width:56px;height:56px}
.sizes .mark svg *{stroke-width:9}.sizes .mark.s48 svg *{stroke-width:7}
.far .mark{width:28px;height:28px}.far .mark svg *{stroke-width:8}
.note{color:var(--slate);margin-top:24px;max-width:780px}
</style></head><body>
<span class="tag">Kuber Estate · logo · modern premium</span>
<h1>Lighter. Quieter. One story each.</h1>
<p class="sub">Single-weight thin lines, generous space, refined geometry — the register of Apple, Compass and Godrej Properties rather than a heavy monogram. Each mark carries exactly one idea and one point of mint. The wordmark is set in Inter Medium, letter-spaced, so the name reads as premium rather than loud. At favicon size the stroke automatically thickens so it stays crisp.</p>
'''
def block(m):
    s=m['svg']
    return f'''
<section class="concept">
  <header><h2>{m['title']}</h2><span class="mono">{m['tag']}</span></header>
  <p class="why">{m['why']}</p>
  <div class="row">
    <div class="cell"><span class="mono">Mark</span><div class="mark">{s}</div></div>
    <div class="cell dark"><span class="mono">On black</span><div class="mark">{s}</div></div>
    <div class="cell far"><span class="mono">From a distance</span><div class="mark">{s}</div></div>
    <div class="cell"><span class="mono">App / favicon tile</span><div class="tile"><div class="mark">{s}</div></div></div>
    <div class="cell" style="grid-column:span 2"><span class="mono">Lockup</span><div class="lockup"><div class="mark">{s}</div><div class="word">Kuber Estate<small>Real estate investment consultants · Pune</small></div></div></div>
    <div class="cell"><span class="mono">Stacked</span><div class="stack"><div class="mark">{s}</div><div class="word">Kuber<br>Estate</div></div></div>
    <div class="cell"><span class="mono">20 / 36 / 56 px</span><div class="sizes"><div class="mark">{s}</div><div class="mark s32">{s}</div><div class="mark s48">{s}</div></div></div>
  </div>
</section>'''
body=''.join(block(m) for m in marks.values())
tail='''<p class="note">All three: black, white, one mint accent, one line weight, no gradients or shadows. My recommendation is <b>1 — Horizon</b>: it keeps the K, it's the most refined, and the rising line is a story people repeat. <b>3 — Open Door</b> is the one with the most warmth. If one of these is close, tell me what to adjust — line weight, the size of the mint point, curves vs. corners — and I'll finalise it.</p></body></html>'''
open('logo-round5.html','w',encoding='utf-8').write(head+body+tail)
print('ok')
