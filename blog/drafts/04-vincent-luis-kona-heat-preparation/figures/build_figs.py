# Builds self-contained HTML figure snippets (EN/ES) for blog 04 (pro article), plus a preview page.
# Same structure and class names as blogs 01 and 02; Heat pillar color #B83C0B, heat-soft #FCE7DC.
import html
PC, PC2 = '#B83C0B', '#FCE7DC'
CSS = """<style>
.rp-fig{--ink:#15171A;--muted:#5B5F64;--line:#DDD9D0;--card:#FFFFFF;--pc:%s;--pc2:%s;--heat:#B83C0B;--ref:#A4A9AE;
 position:relative;margin:32px 0;padding:20px;background:var(--card);border:1px solid var(--line);border-radius:10px;font-family:Inter,system-ui,sans-serif;color:var(--ink)}
.rp-fig *{box-sizing:border-box}
.rp-fig h4{margin:0;font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:20px;line-height:1.25;letter-spacing:-0.01em}
.rp-fig .rp-sub{margin:4px 0 16px;font-size:14px;color:var(--muted)}
.rp-fig .rp-row{display:grid;grid-template-columns:minmax(120px,40%%) 1fr;gap:10px;align-items:center;margin:10px 0}
.rp-fig .rp-lab{font-size:14px;font-weight:600;line-height:1.25}
.rp-fig .rp-lab small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.rp-fig .rp-track{position:relative;height:24px}
.rp-fig .rp-grid{position:absolute;top:0;bottom:0;border-left:1px solid var(--line)}
.rp-fig .rp-bar{position:absolute;top:2px;height:20px;border-radius:0 4px 4px 0}
.rp-fig .rp-val{position:absolute;top:2px;line-height:20px;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px;color:var(--ink);white-space:nowrap;padding-left:8px}
.rp-fig .rp-val.rp-left{padding-left:0;padding-right:8px;transform:translateX(-100%%);color:#FFFFFF}
.rp-fig .rp-axis{position:relative;height:18px;margin-left:calc(40%% + 10px);border-top:1px solid var(--line);font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11px;color:var(--muted)}
.rp-fig .rp-axis span{position:absolute;top:3px;transform:translateX(-50%%);white-space:nowrap}
.rp-fig .rp-axis span:last-child{transform:translateX(-100%%)}
.rp-fig .rp-axl{margin:6px 0 0 calc(40%% + 10px);font-size:12px;color:var(--muted)}
.rp-fig .rp-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.rp-fig .rp-card{background:var(--pc2);border-radius:10px;padding:14px 16px}
.rp-fig .rp-card b{display:block;font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:28px;line-height:1.1;letter-spacing:-0.02em;color:var(--pc)}
.rp-fig .rp-card span{display:block;margin-top:4px;font-size:14px;line-height:1.35;color:var(--ink)}
.rp-fig .rp-card small{display:block;margin-top:6px;font-size:12px;color:var(--muted)}
.rp-fig figcaption{margin-top:14px;padding-top:10px;border-top:1px solid var(--line);font-size:12px;line-height:1.5;color:var(--muted)}
.rp-fig figcaption a{color:var(--muted)}
.rp-fig .rp-sr{position:absolute;left:0;top:0;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%%);white-space:nowrap;border:0}
.rp-fig .rp-steps{list-style:none;margin:0;padding:0;position:relative}
.rp-fig .rp-steps:before{content:"";position:absolute;left:7px;top:6px;bottom:6px;border-left:2px solid var(--line)}
.rp-fig .rp-step{position:relative;padding:8px 10px 8px 30px;margin:4px 0;border-radius:10px}
.rp-fig .rp-step:before{content:"";position:absolute;left:2px;top:13px;width:12px;height:12px;border-radius:50%%;background:var(--card);border:2px solid var(--pc)}
.rp-fig .rp-step.rp-in{background:var(--pc2)}
.rp-fig .rp-step.rp-in:before{background:var(--pc)}
.rp-fig .rp-step b{display:block;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px;font-weight:600;color:var(--pc);letter-spacing:0.02em}
.rp-fig .rp-step span{display:block;font-size:14px;line-height:1.35}
.rp-fig .rp-step small{display:block;font-size:12px;color:var(--muted);margin-top:2px}
.rp-fig .rp-tag{display:inline-block;margin:0 0 10px;padding:3px 10px;border-radius:999px;background:var(--pc2);font-size:12px;color:var(--pc);font-weight:600}
@media (max-width:480px){.rp-fig{padding:16px}.rp-fig h4{font-size:18px}.rp-fig .rp-row{grid-template-columns:132px 1fr}.rp-fig .rp-axis,.rp-fig .rp-axl{margin-left:142px}.rp-fig .rp-cards{grid-template-columns:1fr}.rp-fig .rp-card b{font-size:24px}}
</style>""" % (PC, PC2)


L = {
 'zur': '<a href="https://doi.org/10.1111/sms.12638">Zurawlew et al. 2016</a>',
 'morton': '<a href="https://doi.org/10.1016/j.tjnut.2026.101442">Morton et al. 2026</a>',
 'ada': '<a href="https://pubmed.ncbi.nlm.nih.gov/26917108/">2016 position statement</a>',
 'allin': '<a href="https://youtu.be/TXpXTfYTn28">All-In Triathlon</a>',
 'ptn': '<a href="https://youtu.be/6Mpl1odkY5g">ProTriNews</a>',
 'th': '<a href="https://www.youtube.com/watch?v=uY61pcBHsyQ">The Triathlon Hour</a>',
}

def pct(v, lo, hi): return (v - lo) / (hi - lo) * 100

def axis(ticks, lo, hi, fmt):
    return '<div class="rp-axis">' + ''.join(f'<span style="left:{pct(t,lo,hi):.2f}%">{fmt(t)}</span>' for t in ticks) + '</div>'

def table(caption, head, rows):
    h = ''.join(f'<th>{html.escape(x)}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(c))}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="rp-sr"><table><caption>{html.escape(caption)}</caption><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

COL = {'pc': 'var(--pc)', 'ref': 'var(--ref)', 'ink': '#1F2328'}

T = {
 'en': dict(
  f1t='Kona 2026: a hot, humid day', f1s='The result and the conditions he raced in',
  f1cards=[('7:47:27','1st, IRONMAN World Championship, Oct 10, 2026','Official IRONMAN results'),
           ('88°F','high at Kona International Airport (PHKO)','Weather Underground daily history'),
           ('88%','humidity at 6:53 am, already 79°F','PHKO, not on the course'),
           ('79°F (26°C)','average water temperature','IRONMAN course page')],
  f1c='Sources: official IRONMAN results and course page; Weather Underground history for PHKO, Oct 10, 2026. The airport is not on the course. n = 1.',
  tabh1=['Number','What it is','Source'],
  f2t='His heat prep, in his words', f2s='Months and weeks before Kona (Oct 10, 2026)', f2tag='Shaded: inside our heat window, 6 to 2 weeks out',
  f2steps=[('JAN TO FEB','Passive heat: hot baths and sauna','All-In Triathlon',False),
           ('BEFORE TEXAS, APRIL','Easy rides and runs in the heat; raced Texas partly for heat and humidity','All-In Triathlon; ProTriNews',False),
           ('ABOUT 10 TO 12 WEEKS OUT','Altitude camp in Font-Romeu; heat chamber sessions at altitude','The Triathlon Hour',False),
           ('4 WEEKS OUT','Skipped Nice for big weeks and heat prep','The Triathlon Hour',True),
           ('3 WEEKS OUT','IRONMAN-pace sessions in a heat chamber at 32°C and 80% humidity','All-In Triathlon',True),
           ('OCT 10','Race day: 88°F high at the airport','Weather Underground, PHKO',False)],
  f2c=f'Sources: {L["allin"]} (uploaded Oct 12, 2026; episode sponsored by Precision Fuel &amp; Hydration); {L["ptn"]} (recorded Oct 11, 2026); {L["th"]} (Oct 18, 2026). Self-reported, n = 1. Our heat window is a general guideline.',
  tabh2=['When','What he did','Source'],
  f3t='His carbs are not a target', f3s='Carbs per hour: what he said he took, and what the guidance says',
  f3r=[('Luis, bike','his estimate',145,'pc'),('Luis, run','his estimate',100,'pc'),('Possible ceiling','trained athletes, review',120,'ref'),('Guideline','efforts over 2.5 to 3 h, up to',90,'ink')],
  f3ax='Grams of carbs per hour',
  f3c=f'Sources: Luis on {L["allin"]} (his nutrition partner is 6d Sports Nutrition); {L["morton"]} (review; several authors have ties to Science in Sport); {L["ada"]} (Academy of Nutrition and Dietetics, Dietitians of Canada, ACSM).',
  tabh3=['Who','Detail','g/h'],
 ),
 'es': dict(
  f1t='Kona 2026: un día caluroso y húmedo', f1s='El resultado y las condiciones de la carrera',
  f1cards=[('7:47:27','1.º, Campeonato Mundial IRONMAN, 10 de octubre de 2026','Resultados oficiales de IRONMAN'),
           ('88°F','máxima en el aeropuerto internacional de Kona (PHKO)','Historial de Weather Underground'),
           ('88%','de humedad a las 6:53 am, ya con 79°F','PHKO, fuera del recorrido'),
           ('79°F (26°C)','temperatura promedio del agua','Página oficial del recorrido')],
  f1c='Fuentes: resultados oficiales y página del recorrido de IRONMAN; historial de Weather Underground para PHKO, 10 de octubre de 2026. El aeropuerto no está en el recorrido. n = 1.',
  tabh1=['Número','Qué es','Fuente'],
  f2t='Su preparación para el calor, según él', f2s='Meses y semanas antes de Kona (10 de octubre de 2026)', f2tag='Sombreado: dentro de nuestra ventana de calor, 6 a 2 semanas antes',
  f2steps=[('ENERO A FEBRERO','Calor pasivo: baños calientes y sauna','All-In Triathlon',False),
           ('ANTES DE TEXAS, ABRIL','Rodadas y trotes suaves con calor; corrió Texas en parte por el calor y la humedad','All-In Triathlon; ProTriNews',False),
           ('UNAS 10 A 12 SEMANAS ANTES','Campamento en altura en Font-Romeu; sesiones en cámara de calor en altura','The Triathlon Hour',False),
           ('4 SEMANAS ANTES','No corrió en Niza para hacer semanas grandes y preparar el calor','The Triathlon Hour',True),
           ('3 SEMANAS ANTES','Sesiones a ritmo IRONMAN en cámara de calor a 32°C y 80% de humedad','All-In Triathlon',True),
           ('10 DE OCTUBRE','Día de carrera: máxima de 88°F en el aeropuerto','Weather Underground, PHKO',False)],
  f2c=f'Fuentes: {L["allin"]} (publicado el 12 de octubre de 2026; episodio patrocinado por Precision Fuel &amp; Hydration); {L["ptn"]} (grabado el 11 de octubre de 2026); {L["th"]} (18 de octubre de 2026). Autorreportado, n = 1. Nuestra ventana de calor es una guía general.',
  tabh2=['Cuándo','Qué hizo','Fuente'],
  f3t='Sus carbohidratos no son una meta', f3s='Carbohidratos por hora: lo que dijo que tomó y lo que dicen las guías',
  f3r=[('Luis, bici','su estimación',145,'pc'),('Luis, a pie','su estimación',100,'pc'),('Techo posible','atletas entrenados, revisión',120,'ref'),('Guía','esfuerzos de más de 2.5 a 3 h, hasta',90,'ink')],
  f3ax='Gramos de carbohidratos por hora',
  f3c=f'Fuentes: Luis en {L["allin"]} (su marca de nutrición es 6d Sports Nutrition); {L["morton"]} (revisión; varios autores tienen vínculos con Science in Sport); {L["ada"]} (Academy of Nutrition and Dietetics, Dietitians of Canada, ACSM).',
  tabh3=['Quién','Detalle','g/h'],
 )}

def fig1(t):
    cards = '<div class="rp-cards" aria-hidden="true">' + ''.join(f'<div class="rp-card"><b>{n}</b><span>{d}</span><small>{s}</small></div>' for n, d, s in t['f1cards']) + '</div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f1t"])}"><h4>{t["f1t"]}</h4><p class="rp-sub">{t["f1s"]}</p>{cards}' + \
      table(t['f1s'], t['tabh1'], t['f1cards']) + f'<figcaption>{t["f1c"]}</figcaption></figure>'

def fig2(t):
    steps = '<ol class="rp-steps" aria-hidden="true">' + ''.join(f'<li class="rp-step{" rp-in" if w else ""}"><b>{a}</b><span>{d}</span><small>{s}</small></li>' for a, d, s, w in t['f2steps']) + '</ol>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f2t"])}"><h4>{t["f2t"]}</h4><p class="rp-sub">{t["f2s"]}</p><span class="rp-tag">{t["f2tag"]}</span>{steps}' + \
      table(t['f2s'], t['tabh2'], [(a, d, s) for a, d, s, w in t['f2steps']]) + f'<figcaption>{t["f2c"]}</figcaption></figure>'

def fig3(t):
    lo, hi = 0, 150
    ticks = [0, 50, 100, 150]
    grid = ''.join(f'<div class="rp-grid" style="left:{pct(x,lo,hi):.2f}%"></div>' for x in ticks)
    rows = ''
    for lab, small, v, k in t['f3r']:
        p = pct(v, lo, hi)
        rows += (f'<div class="rp-row"><div class="rp-lab">{lab}<small>{small}</small></div><div class="rp-track" title="{html.escape(lab)}: {v} g/h">{grid}'
                 f'<div class="rp-bar" style="left:0;width:{p:.2f}%;background:{COL[k]}"></div><div class="rp-val rp-left" style="left:{p:.2f}%">{v} g/h</div></div></div>')
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f3t"])}"><h4>{t["f3t"]}</h4><p class="rp-sub">{t["f3s"]}</p>{rows}{axis(ticks,lo,hi,str)}<p class="rp-axl">{t["f3ax"]}</p>' + \
      table(t['f3s'], t['tabh3'], [(a, b, v) for a, b, v, k in t['f3r']]) + f'<figcaption>{t["f3c"]}</figcaption></figure>'

FIGS = [('fig1-race-day', fig1), ('fig2-heat-timeline', fig2), ('fig3-carbs', fig3)]
out = {}
for Lg in ('en', 'es'):
    for name, fn in FIGS:
        snip = fn(T[Lg])
        open(f'{name}-{Lg}.html', 'w').write(CSS + '\n' + snip + '\n')
        out[(name, Lg)] = snip
prev = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blog 04 figures</title><link rel="stylesheet" href="../../../../assets/fonts/fonts.css">' + CSS + \
 '<style>body{margin:0;background:#F4F2ED;font-family:Inter,sans-serif}main{max-width:720px;margin:0 auto;padding:24px 16px}h2{font-family:"Inter Display",Inter;margin:40px 0 0}</style></head><body><main>'
for Lg in ('en', 'es'):
    prev += f'<h2>{Lg.upper()}</h2>' + ''.join(out[(n, Lg)] for n, _ in FIGS)
open('preview.html', 'w').write(prev + '</main></body></html>')
print('ok')
