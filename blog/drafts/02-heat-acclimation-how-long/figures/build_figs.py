# Builds self-contained HTML figure snippets (EN/ES) for blog 02, plus a preview page.
# Same structure and class names as blog 01; Heat pillar color #B83C0B, heat-soft #FCE7DC.
import html
CSS = """<style>
.rp-fig{--ink:#15171A;--muted:#5B5F64;--line:#DDD9D0;--card:#FFFFFF;--heat:#B83C0B;--heat2:#FCE7DC;--ref:#A4A9AE;
 position:relative;margin:32px 0;padding:20px;background:var(--card);border:1px solid var(--line);border-radius:10px;font-family:Inter,system-ui,sans-serif;color:var(--ink)}
.rp-fig *{box-sizing:border-box}
.rp-fig h4{margin:0;font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:20px;line-height:1.25;letter-spacing:-0.01em}
.rp-fig .rp-sub{margin:4px 0 16px;font-size:14px;color:var(--muted)}
.rp-fig .rp-row{display:grid;grid-template-columns:minmax(120px,40%) 1fr;gap:10px;align-items:center;margin:10px 0}
.rp-fig .rp-lab{font-size:14px;font-weight:600;line-height:1.25}
.rp-fig .rp-lab small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.rp-fig .rp-track{position:relative;height:24px}
.rp-fig .rp-grid{position:absolute;top:0;bottom:0;border-left:1px solid var(--line)}
.rp-fig .rp-bar{position:absolute;top:2px;height:20px;border-radius:0 4px 4px 0}
.rp-fig .rp-bar.rp-range{border-radius:4px}
.rp-fig .rp-dot{position:absolute;top:5px;width:14px;height:14px;margin-left:-7px;border-radius:50%;background:var(--heat)}
.rp-fig .rp-val{position:absolute;top:2px;line-height:20px;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px;color:var(--ink);white-space:nowrap;padding-left:10px}
.rp-fig .rp-val.rp-left{padding-left:0;padding-right:10px;transform:translateX(-100%)}
.rp-fig .rp-axis{position:relative;height:18px;margin-left:calc(40% + 10px);border-top:1px solid var(--line);font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11px;color:var(--muted)}
.rp-fig .rp-axis span{position:absolute;top:3px;transform:translateX(-50%);white-space:nowrap}
.rp-fig .rp-axl{margin:6px 0 0 calc(40% + 10px);font-size:12px;color:var(--muted)}
.rp-fig .rp-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.rp-fig .rp-card{background:var(--heat2);border-radius:10px;padding:14px 16px}
.rp-fig .rp-card b{display:block;font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:28px;line-height:1.1;letter-spacing:-0.02em;color:var(--heat)}
.rp-fig .rp-card span{display:block;margin-top:4px;font-size:14px;line-height:1.35;color:var(--ink)}
.rp-fig .rp-card small{display:block;margin-top:6px;font-size:12px;color:var(--muted)}
.rp-fig figcaption{margin-top:14px;padding-top:10px;border-top:1px solid var(--line);font-size:12px;line-height:1.5;color:var(--muted)}
.rp-fig figcaption a{color:var(--muted)}
.rp-fig .rp-sr{position:absolute;left:0;top:0;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}
@media (max-width:480px){.rp-fig{padding:16px}.rp-fig h4{font-size:18px}.rp-fig .rp-row{grid-template-columns:132px 1fr}.rp-fig .rp-axis,.rp-fig .rp-axl{margin-left:142px}.rp-fig .rp-cards{grid-template-columns:1fr}.rp-fig .rp-card b{font-size:24px}}
</style>"""

L = {
 'racinais': '<a href="https://pubmed.ncbi.nlm.nih.gov/25943653/">Racinais et al. 2015</a>',
 'tyler': '<a href="https://pubmed.ncbi.nlm.nih.gov/27106556/">Tyler et al. 2016</a>',
 'snape': '<a href="https://doi.org/10.1371/journal.pone.0345346">Snape et al. 2026</a>',
 'stanley': '<a href="https://pubmed.ncbi.nlm.nih.gov/25432420/">Stanley et al. 2015</a>',
 'klous': '<a href="https://pubmed.ncbi.nlm.nih.gov/33077118/">Klous et al. 2020</a>',
 'zurawlew': '<a href="https://pubmed.ncbi.nlm.nih.gov/26661992/">Zurawlew et al. 2016</a>',
 'daanen': '<a href="https://pubmed.ncbi.nlm.nih.gov/29129022/">Daanen et al. 2018</a>',
}

def pct(v, lo, hi): return (v - lo) / (hi - lo) * 100

def axis(ticks, lo, hi, fmt):
    return '<div class="rp-axis">' + ''.join(f'<span style="left:{pct(t,lo,hi):.2f}%">{fmt(t)}</span>' for t in ticks) + '</div>'

def table(caption, head, rows):
    h = ''.join(f'<th>{html.escape(x)}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(c))}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="rp-sr"><table><caption>{html.escape(caption)}</caption><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

# fig1 rows: (finding, study, start_day, end_day or None, value text)
T = {
 'en': dict(
  f1t='The first heat changes come within days', f1s='When each change was measured, counted in days of heat training',
  f1r=[('Sweat sodium starts to fall','Klous 2020',3,None,'Day 3'),
       ('Plasma volume peaks, +17.8%','Stanley 2015, sauna',4,None,'4 sessions'),
       ('Heart rate down 8 bpm, plasma volume up 7.3%','Snape 2026',5,None,'Day 5'),
       ('5 km in 33°C, 4.9% faster','Zurawlew 2016, hot baths',6,None,'Day 6'),
       ('Sweat rate starts to rise','Klous 2020',7,8,'Day 7 to 8'),
       ('Sweat rate +58% (arm), sodium about 60% of day 1','Klous 2020',10,None,'Day 10'),
       ('Expert advice','Racinais 2015',7,14,'1 to 2 weeks'),
       ('Greatest adaptations','Tyler 2016, meta-analysis',14,16,'Beyond 14 days')],
  f1ax='Days of heat training', f1day=lambda d: f'Day {d}',
  f1c=f'Sources: {L["klous"]} (8 people, lab cycling, skin patches); {L["stanley"]} (7 cyclists, no control group); {L["snape"]} (14 men, 7 per group); {L["zurawlew"]} (17 men, 5 km lab test); {L["racinais"]} (expert consensus); {L["tyler"]} (meta-analysis of 96 articles).',
  tabh1=['Change','Study','When'],
  f2t='Six days of hot baths, faster only in the heat', f2s='Change in a 5 km treadmill time trial after 6 days of 40 min baths after running',
  f2r=[('Hot baths (40°C)','5 km in 33°C',4.9),('Hot baths (40°C)','5 km in 18°C',None),('Control (34°C water)','both tests',None)],
  nochange='No change', f2c=f'{L["zurawlew"]}. Randomized controlled trial, 17 men not used to heat (10 hot baths, 7 control). A 5 km lab test, not a long race.',
  tabh2=['Group','Test','Change'],
  f3t='Heat gains fade slowly', f3s='How heat adaptations hold up once the heat stops',
  f3cards=[('5+ days','of heat are enough for heart rate and core temperature changes','Daanen 2018'),
           ('About 2.5%','of the adaptations are lost for every day without heat','Daanen 2018'),
           ('28 days','after stopping, part of the adaptations was still there','Klous 2020, 4 people'),
           ('5 days','of heat again may restore them','Klous 2020')],
  f3c=f'Sources: {L["daanen"]} (systematic review and meta-analysis, mostly lab studies); {L["klous"]} (lab study, 4 people in the decay phase).',
  tabh3=['Number','Finding','Study'],
 ),
 'es': dict(
  f1t='Los primeros cambios llegan en días', f1s='Cuándo se midió cada cambio, contando los días de entrenamiento con calor',
  f1r=[('El sodio del sudor empieza a bajar','Klous 2020',3,None,'Día 3'),
       ('El volumen de plasma llega al máximo, +17.8%','Stanley 2015, sauna',4,None,'4 sesiones'),
       ('Frecuencia cardíaca 8 lpm menos, plasma 7.3% más','Snape 2026',5,None,'Día 5'),
       ('5 km a 33°C, 4.9% más rápido','Zurawlew 2016, baños calientes',6,None,'Día 6'),
       ('La sudoración empieza a subir','Klous 2020',7,8,'Día 7 a 8'),
       ('Sudoración +58% (brazo), sodio cerca del 60% del día 1','Klous 2020',10,None,'Día 10'),
       ('Lo que recomiendan los expertos','Racinais 2015',7,14,'1 a 2 semanas'),
       ('Mayores adaptaciones','Tyler 2016, metaanálisis',14,16,'Más de 14 días')],
  f1ax='Días de entrenamiento con calor', f1day=lambda d: f'Día {d}',
  f1c=f'Fuentes: {L["klous"]} (8 personas, bici en laboratorio, parches en la piel); {L["stanley"]} (7 ciclistas, sin grupo de control); {L["snape"]} (14 hombres, 7 por grupo); {L["zurawlew"]} (17 hombres, prueba de 5 km en laboratorio); {L["racinais"]} (consenso de expertos); {L["tyler"]} (metaanálisis de 96 artículos).',
  tabh1=['Cambio','Estudio','Cuándo'],
  f2t='Seis días de baños calientes: más rápido solo con calor', f2s='Cambio en una contrarreloj de 5 km en cinta tras 6 días de baños de 40 min después de correr',
  f2r=[('Baños calientes (40°C)','5 km a 33°C',4.9),('Baños calientes (40°C)','5 km a 18°C',None),('Control (agua a 34°C)','ambas pruebas',None)],
  nochange='Sin cambios', f2c=f'{L["zurawlew"]}. Ensayo controlado aleatorizado, 17 hombres no acostumbrados al calor (10 con baños calientes, 7 de control). Una prueba de 5 km en laboratorio, no una carrera larga.',
  tabh2=['Grupo','Prueba','Cambio'],
  f3t='Lo ganado con el calor se pierde despacio', f3s='Cómo se mantienen las adaptaciones cuando dejas el calor',
  f3cards=[('5+ días','de calor bastan para cambios en frecuencia cardíaca y temperatura corporal','Daanen 2018'),
           ('Cerca del 2.5%','de las adaptaciones se pierde por cada día sin calor','Daanen 2018'),
           ('28 días','después de parar, una parte de las adaptaciones seguía ahí','Klous 2020, 4 personas'),
           ('5 días','de calor otra vez podrían recuperarlas','Klous 2020')],
  f3c=f'Fuentes: {L["daanen"]} (revisión sistemática y metaanálisis, casi todo estudios de laboratorio); {L["klous"]} (estudio de laboratorio, 4 personas en la fase sin calor).',
  tabh3=['Número','Hallazgo','Estudio'],
 )}

def fig1(t):
    lo, hi = 0, 16
    ticks = [0, 3, 7, 10, 14]
    grid = ''.join(f'<div class="rp-grid" style="left:{pct(x,lo,hi):.2f}%"></div>' for x in ticks)
    rows = ''
    for lab, st, a, b, v in t['f1r']:
        if b is None:
            mark = f'<div class="rp-dot" style="left:{pct(a,lo,hi):.2f}%"></div>'
            pos = pct(a, lo, hi)
        else:
            mark = f'<div class="rp-bar rp-range" style="left:{pct(a,lo,hi):.2f}%;width:{pct(b,lo,hi)-pct(a,lo,hi):.2f}%;background:var(--heat)"></div>'
            pos = pct(b, lo, hi) if pct(b, lo, hi) < 60 else None
        if pos is None:
            val, small = '', f'{st} · <span style="font-family:JetBrains Mono,ui-monospace,monospace">{v}</span>'
        else:
            side = '' if pos < 55 else ' rp-left'
            val, small = f'<div class="rp-val{side}" style="left:{pos:.2f}%">{v}</div>', st
        rows += f'<div class="rp-row"><div class="rp-lab">{lab}<small>{small}</small></div><div class="rp-track" title="{html.escape(lab)}: {v}">{grid}{mark}{val}</div></div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f1t"])}"><h4>{t["f1t"]}</h4><p class="rp-sub">{t["f1s"]}</p>{rows}{axis(ticks,lo,hi,lambda x: str(x))}<p class="rp-axl">{t["f1ax"]}</p>' + \
      table(t['f1s'], t['tabh1'], [(lab, st, v) for lab, st, a, b, v in t['f1r']]) + f'<figcaption>{t["f1c"]}</figcaption></figure>'

def fig2(t):
    lo, hi = 0, 6
    rows = ''
    for g, test, v in t['f2r']:
        if v is None:
            inner = f'<div class="rp-grid" style="left:0;border-left:2px solid var(--muted)"></div><div class="rp-val" style="left:0;color:var(--muted)">{t["nochange"]}</div>'
        else:
            inner = f'<div class="rp-bar" style="left:0;width:{pct(v,lo,hi):.2f}%;background:var(--heat)"></div><div class="rp-val" style="left:{pct(v,lo,hi):.2f}%">+{v}%</div>'
        rows += f'<div class="rp-row"><div class="rp-lab">{g}<small>{test}</small></div><div class="rp-track" title="{html.escape(g)}, {html.escape(test)}">{inner}</div></div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f2t"])}"><h4>{t["f2t"]}</h4><p class="rp-sub">{t["f2s"]}</p>{rows}{axis([0,2,4,6],lo,hi,lambda x: f"+{x}%" if x else "0")}' + \
      table(t['f2s'], t['tabh2'], [(g, test, f'+{v}%' if v is not None else t['nochange']) for g, test, v in t['f2r']]) + f'<figcaption>{t["f2c"]}</figcaption></figure>'

def fig3(t):
    cards = '<div class="rp-cards" aria-hidden="true">' + ''.join(f'<div class="rp-card"><b>{n}</b><span>{d}</span><small>{s}</small></div>' for n, d, s in t['f3cards']) + '</div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f3t"])}"><h4>{t["f3t"]}</h4><p class="rp-sub">{t["f3s"]}</p>{cards}' + \
      table(t['f3s'], t['tabh3'], t['f3cards']) + f'<figcaption>{t["f3c"]}</figcaption></figure>'

FIGS = [('fig1-heat-timeline', fig1), ('fig2-hot-baths', fig2), ('fig3-heat-fade', fig3)]
out = {}
for Lg in ('en', 'es'):
    for name, fn in FIGS:
        snip = fn(T[Lg])
        open(f'{name}-{Lg}.html', 'w').write(CSS + '\n' + snip + '\n')
        out[(name, Lg)] = snip
prev = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blog 02 figures</title><link rel="stylesheet" href="../../../../assets/fonts/fonts.css">' + CSS + \
 '<style>body{margin:0;background:#F4F2ED;font-family:Inter,sans-serif}main{max-width:720px;margin:0 auto;padding:24px 16px}h2{font-family:"Inter Display",Inter;margin:40px 0 0}</style></head><body><main>'
for Lg in ('en', 'es'):
    prev += f'<h2>{Lg.upper()}</h2>' + ''.join(out[(n, Lg)] for n, _ in FIGS)
open('preview.html', 'w').write(prev + '</main></body></html>')
print('ok')
