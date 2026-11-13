# Builds self-contained HTML figure snippets (EN/ES) for blog 06, plus a preview page.
# Same structure and class names as blogs 01 to 05; Heat pillar color #B83C0B, heat-soft #FCE7DC.
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
.rp-fig .rp-ci{position:absolute;top:11px;height:2px;background:var(--ink)}
.rp-fig .rp-ci:before,.rp-fig .rp-ci:after{content:'';position:absolute;top:-5px;width:2px;height:12px;background:var(--ink)}
.rp-fig .rp-ci:before{left:0}.rp-fig .rp-ci:after{right:0}
.rp-fig .rp-bar.rp-muted{background:var(--ref)}
.rp-fig .rp-zero{position:absolute;top:-4px;bottom:-4px;border-left:2px solid var(--muted)}
.rp-fig .rp-sr{position:absolute;left:0;top:0;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}
@media (max-width:480px){.rp-fig{padding:16px}.rp-fig h4{font-size:18px}.rp-fig .rp-row{grid-template-columns:132px 1fr}.rp-fig .rp-axis,.rp-fig .rp-axl{margin-left:142px}.rp-fig .rp-cards{grid-template-columns:1fr}.rp-fig .rp-card b{font-size:24px}}
</style>"""

L = {
 'scoon': '<a href="https://doi.org/10.1016/j.jsams.2006.06.009">Scoon et al. 2007</a>',
 'stanley': '<a href="https://doi.org/10.1007/s00421-014-3060-1">Stanley et al. 2015</a>',
 'jenkins': '<a href="https://doi.org/10.1113/jp289874">Jenkins et al. 2025</a>',
 'zurawlew': '<a href="https://doi.org/10.1111/sms.12638">Zurawlew et al. 2016</a>',
}

def pct(v, lo, hi): return (v - lo) / (hi - lo) * 100

def axis(ticks, lo, hi, fmt):
    return '<div class="rp-axis">' + ''.join(f'<span style="left:{pct(t,lo,hi):.2f}%">{fmt(t)}</span>' for t in ticks) + '</div>'

def table(caption, head, rows):
    h = ''.join(f'<th>{html.escape(x)}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(c))}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="rp-sr"><table><caption>{html.escape(caption)}</caption><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

# fig1 rows: (label, note, value, low, high, measured?)
T = {
 'en': dict(
  f1t='32% longer to exhaustion is not 32% faster', f1s='Change after 3 weeks of sauna after training vs 3 weeks without, with 90% confidence limits',
  f1r=[('Run time to exhaustion','Measured, at 5 km race pace',32,21,43,True),
       ('Time trial','Authors’ estimate, not measured',1.9,1.3,2.4,False),
       ('Plasma volume','Measured',7.1,5.6,8.7,True),
       ('Red cell volume','Measured, unclear',3.5,-0.8,8.1,True)],
  f1ax='Change vs the block without sauna',
  f1c=f'{L["scoon"]}. Crossover trial, 6 competitive male distance runners, humid sauna at about 90°C for about 31 min after training, 12.7 sessions on average. Tested 1 to 2 days after each block.',
  to='to', tabh1=['Measure','Note','Change','90% confidence limits'],
  f2t='Small studies, small groups, mostly men', f2s='What sauna and hot baths after training did in four studies',
  f2cards=[('1.9%','estimated faster time trial after 3 weeks of sauna','Scoon 2007 · 6 men · crossover trial'),
           ('+17.8%','plasma volume, peaking after 4 sauna sessions','Stanley 2015 · 7 men · no control group'),
           ('+2.7','mL/kg/min VO2max after 5 weeks of hot baths','Jenkins 2025 · 10 runners, 9 men · crossover'),
           ('4.9%','faster 5 km in 33°C after 6 days of hot baths; no change at 18°C','Zurawlew 2016 · 17 men · randomized trial')],
  f2c=f'Sources: {L["scoon"]} (time trial figure estimated from a run to exhaustion); {L["stanley"]} (30 min at 87°C, 11% humidity); {L["jenkins"]} (5 x 45 min a week at 40°C or hotter); {L["zurawlew"]} (40 min at 40°C after a 40 min run).',
  tabh2=['Number','Finding','Study'],
 ),
 'es': dict(
  f1t='32% más tiempo hasta el agotamiento no es 32% más rápido', f1s='Cambio tras 3 semanas con sauna después de entrenar vs 3 semanas sin sauna, con límites de confianza del 90%',
  f1r=[('Tiempo hasta el agotamiento','Medido, a ritmo de 5 km',32,21,43,True),
       ('Contrarreloj','Estimación de los autores, no medida',1.9,1.3,2.4,False),
       ('Volumen de plasma','Medido',7.1,5.6,8.7,True),
       ('Volumen de glóbulos rojos','Medido, no es claro',3.5,-0.8,8.1,True)],
  f1ax='Cambio vs el bloque sin sauna',
  f1c=f'{L["scoon"]}. Ensayo cruzado, 6 corredores de fondo hombres de nivel competitivo, sauna húmedo a cerca de 90°C durante unos 31 min después de entrenar, 12.7 sesiones en promedio. Prueba 1 a 2 días después de cada bloque.',
  to='a', tabh1=['Medida','Nota','Cambio','Límites de confianza del 90%'],
  f2t='Estudios pequeños, grupos pequeños, casi todos hombres', f2s='Lo que hicieron el sauna y los baños calientes después de entrenar en cuatro estudios',
  f2cards=[('1.9%','contrarreloj más rápida, estimada, tras 3 semanas de sauna','Scoon 2007 · 6 hombres · ensayo cruzado'),
           ('+17.8%','volumen de plasma, con el máximo tras 4 sesiones de sauna','Stanley 2015 · 7 hombres · sin grupo de control'),
           ('+2.7','mL/kg/min de VO2max tras 5 semanas de baños calientes','Jenkins 2025 · 10 corredores, 9 hombres · cruzado'),
           ('4.9%','más rápido en 5 km a 33°C tras 6 días de baños calientes; sin cambios a 18°C','Zurawlew 2016 · 17 hombres · ensayo aleatorizado')],
  f2c=f'Fuentes: {L["scoon"]} (contrarreloj estimada a partir de una prueba hasta el agotamiento); {L["stanley"]} (30 min a 87°C, 11% de humedad); {L["jenkins"]} (5 x 45 min por semana a 40°C o más); {L["zurawlew"]} (40 min a 40°C tras correr 40 min).',
  tabh2=['Número','Hallazgo','Estudio'],
 )}

def fmt(v): return f'+{v:g}%' if v > 0 else f'{v:g}%'

def fig1(t):
    lo, hi = -5, 45
    ticks = [0, 10, 20, 30, 40]
    grid = ''.join(f'<div class="rp-grid" style="left:{pct(x,lo,hi):.2f}%"></div>' for x in ticks[1:])
    z = pct(0, lo, hi)
    rows = ''
    for lab, note, v, a, b, meas in t['f1r']:
        cls = 'rp-bar' + ('' if meas else ' rp-muted')
        bar = f'<div class="{cls}" style="left:{z:.2f}%;width:{pct(v,lo,hi)-z:.2f}%;{"background:var(--heat)" if meas else ""}"></div>'
        ci = f'<div class="rp-ci" style="left:{pct(a,lo,hi):.2f}%;width:{pct(b,lo,hi)-pct(a,lo,hi):.2f}%"></div>'
        if v > 20:  # wide bar: label inside it, white on heat, so it never runs past the whisker
            val = f'<div class="rp-val" style="left:{z:.2f}%;color:#FFFFFF;font-weight:600">{fmt(v)}</div>'
        else:
            val = f'<div class="rp-val" style="left:{pct(b,lo,hi):.2f}%">{fmt(v)}</div>'
        rows += f'<div class="rp-row"><div class="rp-lab">{lab}<small>{note}</small></div><div class="rp-track" title="{html.escape(lab)}: {fmt(v)} ({a:g} {t['to']} {b:g}%)">{grid}<div class="rp-zero" style="left:{z:.2f}%"></div>{bar}{ci}{val}</div></div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f1t"])}"><h4>{t["f1t"]}</h4><p class="rp-sub">{t["f1s"]}</p>{rows}{axis(ticks,lo,hi,lambda x: f"+{x}%" if x else "0")}<p class="rp-axl">{t["f1ax"]}</p>' + \
      table(t['f1s'], t['tabh1'], [(lab, note, fmt(v), f'{a:g}% {t["to"]} {b:g}%') for lab, note, v, a, b, m in t['f1r']]) + f'<figcaption>{t["f1c"]}</figcaption></figure>'

def fig2(t):
    cards = '<div class="rp-cards" aria-hidden="true">' + ''.join(f'<div class="rp-card"><b>{n}</b><span>{d}</span><small>{s}</small></div>' for n, d, s in t['f2cards']) + '</div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f2t"])}"><h4>{t["f2t"]}</h4><p class="rp-sub">{t["f2s"]}</p>{cards}' + \
      table(t['f2s'], t['tabh2'], t['f2cards']) + f'<figcaption>{t["f2c"]}</figcaption></figure>'

FIGS = [('fig1-sauna-trial', fig1), ('fig2-passive-heat-studies', fig2)]
out = {}
for Lg in ('en', 'es'):
    for name, fn in FIGS:
        snip = fn(T[Lg])
        open(f'{name}-{Lg}.html', 'w').write(CSS + '\n' + snip + '\n')
        out[(name, Lg)] = snip
prev = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blog 06 figures</title><link rel="stylesheet" href="../../../../assets/fonts/fonts.css">' + CSS + \
 '<style>body{margin:0;background:#F4F2ED;font-family:Inter,sans-serif}main{max-width:720px;margin:0 auto;padding:24px 16px}h2{font-family:"Inter Display",Inter;margin:40px 0 0}</style></head><body><main>'
for Lg in ('en', 'es'):
    prev += f'<h2>{Lg.upper()}</h2>' + ''.join(out[(n, Lg)] for n, _ in FIGS)
open('preview.html', 'w').write(prev + '</main></body></html>')
print('ok')
