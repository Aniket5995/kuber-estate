SW=5; G=4  # stroke, weave gap
A=('stroke="currentColor" stroke-width="%d" stroke-linecap="round" stroke-linejoin="round" fill="none"'%SW)
BG='stroke="var(--bg,#fff)" stroke-width="%d" stroke-linecap="butt" fill="none"'%(SW+2*G)
marks={
 'woven': dict(title='1 — Woven', tag='K + R · interlaced · thin',
  why="A complete <b>K</b> and a complete <b>R</b> in one line weight, woven: the R's stem passes in front of the K's upper arm, the K's lower arm passes in front of the R's stem. The R sits a step higher, so the pair rises to the right. The same idea as before, but drawn like a jeweller's monogram rather than a stencil — the gaps at the crossings are what make it feel crafted.",
  svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><g {A}>
<path d="M24 20v68"/><path d="M24 56l34-32"/>
<path d="M58 12v68"/><path d="M58 14h14a13 13 0 0 1 0 26H58"/><path d="M68 40l18 40"/>
</g><path d="M58 20v14" {BG}/><path d="M58 12v68" {A}/>
<path d="M46 70l18 12" {BG}/><path d="M24 56l52 32" {A}/>
</svg>'''),
 'mirror': dict(title='2 — Mirror', tag='ꓘR · one stem',
  why="The K is mirrored so both letters hang off <b>one shared stem</b>: K's arms to the left, R's bowl and leg to the right. Perfectly balanced, reads instantly as KR, and the silhouette is almost a figure with open arms — welcoming. The mint point crowning the stem is growth: the line keeps going up.",
  svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><g {A}>
<path d="M50 16v72"/><path d="M50 54L20 26"/><path d="M50 54L20 84"/>
<path d="M50 18h15a14 14 0 0 1 0 28H50"/><path d="M60 46l22 42"/>
</g><circle cx="50" cy="8" r="4.5" fill="#d1ffca"/></svg>'''),
 'through': dict(title='3 — Through', tag='R · rising line',
  why="One stem, one bowl, one leg — a full <b>R</b>. From the point where the leg begins, a second line rises at 45° straight through the bowl and out the top: that line and the leg are the <b>K</b>'s two arms, and it is also the growth line — through the property, upward, to a mint point. Two letters, one gesture, and the most distinctive of the three.",
  svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -12 100 112"><g {A}>
<path d="M30 18v72"/><path d="M30 20h20a16 16 0 0 1 0 32H30"/><path d="M30 52l36 38"/>
</g><path d="M56 26l10-10" {BG}/><path d="M30 52L78 4" {A}/><circle cx="82" cy="-1" r="4.5" fill="#d1ffca"/></svg>'''),
}
for k,m in marks.items(): open('r6-%s.svg'%k,'w').write(m['svg']+'\n')
src=open('gen_r5.py').read()
head=src[src.index("head='''"):src.index("def block")]
exec(head)  # defines head
head=head.replace('.cell.dark{background:#000;color:#fff}','.cell.dark{background:#000;color:#fff;--bg:#000}').replace('.tile{width:96px;height:96px;border-radius:26px;background:#000;','.tile{width:96px;height:96px;border-radius:26px;background:#000;--bg:#000;').replace('logo, modern premium','logo, K+R thin').replace('<h1>Lighter. Quieter. One story each.</h1>','<h1>K and R. Thin, balanced, one gesture.</h1>').replace(
 "Single-weight thin lines, generous space, refined geometry — the register of Apple, Compass and Godrej Properties rather than a heavy monogram. Each mark carries exactly one idea and one point of mint. The wordmark is set in Inter Medium, letter-spaced, so the name reads as premium rather than loud. At favicon size the stroke automatically thickens so it stays crisp.",
 "Same premium register as the last round — one thin line weight, refined geometry, letter-spaced Inter wordmark — but now every mark carries a complete <b>K</b> and a complete <b>R</b>, and every one has growth built into its shape. At favicon size the stroke thickens automatically so it stays crisp.")
blk=src[src.index("def block"):src.index("body=''")]
exec(blk)
body=''.join(block(m) for m in marks.values())
tail='''<p class="note">Black, white, one mint point, one line weight. My pick is <b>3 — Through</b>: it's the most original and the growth line is the whole story. <b>2 — Mirror</b> is the safest and most balanced. Tell me which — or what to change — and I'll finalise it.</p></body></html>'''
open('logo-round6.html','w',encoding='utf-8').write(head+body+tail); print('ok')
