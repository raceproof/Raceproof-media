# Builds self-contained HTML figure snippets (EN/ES) for blog 07, plus a preview page.
# Same structure and class names as blogs 01 to 06; Gut pillar color #1F5FAF, maintain tint #D6E2F1.
import html
CSS = """<style>
.rp-fig{--ink:#15171A;--muted:#5B5F64;--line:#DDD9D0;--card:#FFFFFF;--gut:#1F5FAF;--gut2:#D6E2F1;--gutmid:#7FA3D6;--ref:#A4A9AE;
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
.rp-fig .rp-dot{position:absolute;top:5px;width:14px;height:14px;margin-left:-7px;border-radius:50%;background:var(--gut)}
.rp-fig .rp-val{position:absolute;top:2px;line-height:20px;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px;color:var(--ink);white-space:nowrap;padding-left:10px}
.rp-fig .rp-val.rp-left{padding-left:0;padding-right:10px;transform:translateX(-100%)}
.rp-fig .rp-axis{position:relative;height:18px;margin-left:calc(40% + 10px);border-top:1px solid var(--line);font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11px;color:var(--muted)}
.rp-fig .rp-axis span{position:absolute;top:3px;transform:translateX(-50%);white-space:nowrap}
.rp-fig .rp-axl{margin:6px 0 0 calc(40% + 10px);font-size:12px;color:var(--muted)}
.rp-fig .rp-cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.rp-fig .rp-card{background:var(--gut2);border-radius:10px;padding:14px 16px}
.rp-fig .rp-card b{display:block;white-space:nowrap;font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:28px;line-height:1.1;letter-spacing:-0.02em;color:var(--gut)}
.rp-fig .rp-card span{display:block;margin-top:4px;font-size:14px;line-height:1.35;color:var(--ink)}
.rp-fig .rp-card small{display:block;margin-top:6px;font-size:12px;color:var(--muted)}
.rp-fig figcaption{margin-top:14px;padding-top:10px;border-top:1px solid var(--line);font-size:12px;line-height:1.5;color:var(--muted)}
.rp-fig figcaption a{color:var(--muted)}
.rp-fig .rp-ci{position:absolute;top:11px;height:2px;background:var(--ink)}
.rp-fig .rp-ci:before,.rp-fig .rp-ci:after{content:'';position:absolute;top:-5px;width:2px;height:12px;background:var(--ink)}
.rp-fig .rp-ci:before{left:0}.rp-fig .rp-ci:after{right:0}
.rp-fig .rp-bar.rp-muted{background:var(--ref)}
.rp-fig .rp-zero{position:absolute;top:-4px;bottom:-4px;border-left:2px solid var(--muted)}
.rp-fig .rp-note{margin:8px 0 0;font-size:13px;font-weight:600;color:var(--ink)}
.rp-fig .rp-sr{position:absolute;left:0;top:0;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}
@media (max-width:480px){.rp-fig{padding:16px}.rp-fig h4{font-size:18px}.rp-fig .rp-row{grid-template-columns:132px 1fr}.rp-fig .rp-axis,.rp-fig .rp-axl{margin-left:142px}.rp-fig .rp-cards{grid-template-columns:1fr}.rp-fig .rp-card b{font-size:24px}}
</style>"""
L = {
 'viribay': '<a href="https://doi.org/10.3390/nu12051367">Viribay et al. 2020</a>',
 'norte': '<a href="https://doi.org/10.1111/sms.70326">Norte et al. 2026</a>',
 'stuempfle': '<a href="https://doi.org/10.1080/02640414.2015.1012104">Stuempfle &amp; Hoffman 2015</a>',
 'mougin': '<a href="https://www.sciencedirect.com/science/article/pii/S1440244026002318">Mougin et al. 2026</a>',
}

def pct(v, lo, hi): return (v - lo) / (hi - lo) * 100

def axis(ticks, lo, hi, fmt):
    return '<div class="rp-axis">' + ''.join(f'<span style="left:{pct(t,lo,hi):.2f}%">{fmt(t)}</span>' for t in ticks) + '</div>'

def table(caption, head, rows):
    h = ''.join(f'<th>{html.escape(x)}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(c))}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="rp-sr"><table><caption>{html.escape(caption)}</caption><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

T = {
 'en': dict(
  f1t='More carbs, less muscle damage, same race time', f1s='Rise in a muscle damage marker (CK) from race day to 24 h later, by carbs per hour in a mountain marathon',
  f1r=[('60 g/h','6 runners',976.2,'mid'),('90 g/h','7 runners',963.4,'mid'),('120 g/h','7 runners',155.9,'gut')],
  f1ax='Rise in CK by the next day', f1note='Race time: no difference between groups (p = 0.871)',
  f1c=f'{L["viribay"]}. Randomized trial in a real mountain marathon, elite male trail runners, all gut trained, 2:1 maltodextrin to fructose gels. 6 of 26 starters did not finish, 3 for gut problems. Small groups, men only.',
  tabh1=['Carbs per hour','Runners analyzed','Rise in CK to 24 h'],
  f2t='Late power held better with more carbs', f2s='Critical power after 3 h of cycling at a moderate intensity',
  f2r=[('Fresh','Before the ride',277,'ref'),('Water','After 3 h',236,'ref'),('60 g/h','After 3 h',257,'mid'),('120 g/h','After 3 h',266,'gut')],
  f2ax='Critical power (W)',
  f2c=f'{L["norte"]}. Randomized crossover trial, 16 trained cyclists and triathletes (15 men, 1 woman), lab cycling after a full carb load. Race time not measured.',
  tabh2=['Condition','When','Critical power'],
  f3t='At Western States, the gut decides who finishes', f3s='What runners reported in two surveys at the Western States 100',
  f3cards=[('96.0%','had at least one gut symptom, mostly mild','Stuempfle 2015 · 272 runners'),
           ('43.9%','of finishers said gut symptoms hurt their performance','Stuempfle 2015'),
           ('35.6%','of runners who dropped out named gut symptoms as one reason','Stuempfle 2015'),
           ('100% vs 69%','had a structured carb plan: under 18 h vs 24 to 30 h finishers','Mougin 2026 · 2025 race')],
  f3c=f'Sources: {L["stuempfle"]} (post-race questionnaire, 71.0% of starters); {L["mougin"]} (pre- and post-race surveys, 106 and 66 runners). Both self-reported, one race each: links, not proof.',
  tabh3=['Number','Finding','Source'],
 ),
 'es': dict(
  f1t='Más carbohidratos, menos daño muscular, mismo tiempo', f1s='Aumento de un marcador de daño muscular (CK) del día de la carrera a 24 h después, según los carbohidratos por hora en un maratón de montaña',
  f1r=[('60 g/h','6 corredores',976.2,'mid'),('90 g/h','7 corredores',963.4,'mid'),('120 g/h','7 corredores',155.9,'gut')],
  f1ax='Aumento de CK al día siguiente', f1note='Tiempo de carrera: sin diferencia entre grupos (p = 0.871)',
  f1c=f'{L["viribay"]}. Ensayo aleatorizado en un maratón de montaña real, corredores de montaña hombres de élite, todos con el estómago entrenado, geles de maltodextrina y fructosa 2:1. 6 de 26 no terminaron, 3 por problemas digestivos. Grupos pequeños, solo hombres.',
  tabh1=['Carbohidratos por hora','Corredores analizados','Aumento de CK a 24 h'],
  f2t='Más carbohidratos, más potencia al final', f2s='Potencia crítica después de 3 h de ciclismo a intensidad moderada',
  f2r=[('Sin fatiga','Antes de pedalear',277,'ref'),('Agua','Tras 3 h',236,'ref'),('60 g/h','Tras 3 h',257,'mid'),('120 g/h','Tras 3 h',266,'gut')],
  f2ax='Potencia crítica (W)',
  f2c=f'{L["norte"]}. Ensayo cruzado aleatorizado, 16 ciclistas y triatletas entrenados (15 hombres, 1 mujer), ciclismo en laboratorio tras una carga completa de carbohidratos. No midió tiempo de carrera.',
  tabh2=['Condición','Momento','Potencia crítica'],
  f3t='En la Western States, el estómago decide quién termina', f3s='Lo que reportaron los corredores en dos encuestas en la Western States 100',
  f3cards=[('96.0%','tuvo al menos un síntoma digestivo, casi siempre leve','Stuempfle 2015 · 272 corredores'),
           ('43.9%','de quienes terminaron dijo que los síntomas digestivos afectaron su rendimiento','Stuempfle 2015'),
           ('35.6%','de quienes abandonaron nombró los síntomas digestivos como uno de los motivos','Stuempfle 2015'),
           ('100% vs 69%','tenía un plan de carbohidratos: menos de 18 h vs 24 a 30 h','Mougin 2026 · edición 2025')],
  f3c=f'Fuentes: {L["stuempfle"]} (cuestionario después de la carrera, 71.0% de los que salieron); {L["mougin"]} (encuestas antes y después de la carrera, 106 y 66 corredores). Ambas autorreportadas, una carrera cada una: asociaciones, no pruebas.',
  tabh3=['Número','Hallazgo','Fuente'],
 )}

COL = {'gut':'var(--gut)','mid':'var(--gutmid)','ref':'var(--ref)'}

def bars(rows, lo, hi, unit, grid_ticks):
    grid = ''.join(f'<div class="rp-grid" style="left:{pct(x,lo,hi):.2f}%"></div>' for x in grid_ticks if x > lo)
    out = ''
    for lab, note, v, c in rows:
        w = pct(v, lo, hi)
        if w > 55:
            val = f'<div class="rp-val rp-left" style="left:{w:.2f}%;color:{"#FFFFFF" if c=="gut" else "#15171A"};font-weight:600">{v:g}{unit}</div>'
        else:
            val = f'<div class="rp-val" style="left:{w:.2f}%">{v:g}{unit}</div>'
        out += f'<div class="rp-row"><div class="rp-lab">{lab}<small>{note}</small></div><div class="rp-track" title="{html.escape(lab)}: {v:g}{unit}">{grid}<div class="rp-bar" style="left:0;width:{w:.2f}%;background:{COL[c]}"></div>{val}</div></div>'
    return out

def fig1(t):
    lo, hi = 0, 1100
    ticks = [0, 500, 1000]
    rows = bars(t['f1r'], lo, hi, '%', ticks)
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f1t"])}"><h4>{t["f1t"]}</h4><p class="rp-sub">{t["f1s"]}</p>{rows}{axis(ticks,lo,hi,lambda x: f"{x}%")}<p class="rp-axl">{t["f1ax"]}</p><p class="rp-note">{t["f1note"]}</p>' + \
      table(t['f1s'], t['tabh1'], [(a, b, f'{v:g}%') for a, b, v, c in t['f1r']]) + f'<figcaption>{t["f1c"]}</figcaption></figure>'

def fig2(t):
    lo, hi = 0, 300
    ticks = [0, 100, 200, 300]
    rows = bars(t['f2r'], lo, hi, ' W', ticks)
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f2t"])}"><h4>{t["f2t"]}</h4><p class="rp-sub">{t["f2s"]}</p>{rows}{axis(ticks,lo,hi,lambda x: f"{x}")}<p class="rp-axl">{t["f2ax"]}</p>' + \
      table(t['f2s'], t['tabh2'], [(a, b, f'{v:g} W') for a, b, v, c in t['f2r']]) + f'<figcaption>{t["f2c"]}</figcaption></figure>'

def fig3(t):
    cards = '<div class="rp-cards" aria-hidden="true">' + ''.join(f'<div class="rp-card"><b>{n}</b><span>{d}</span><small>{s}</small></div>' for n, d, s in t['f3cards']) + '</div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f3t"])}"><h4>{t["f3t"]}</h4><p class="rp-sub">{t["f3s"]}</p>{cards}' + \
      table(t['f3s'], t['tabh3'], t['f3cards']) + f'<figcaption>{t["f3c"]}</figcaption></figure>'

FIGS = [('fig1-mountain-marathon', fig1), ('fig2-late-power', fig2), ('fig3-western-states', fig3)]
out = {}
for Lg in ('en', 'es'):
    for name, fn in FIGS:
        snip = fn(T[Lg])
        open(f'{name}-{Lg}.html', 'w').write(CSS + '\n' + snip + '\n')
        out[(name, Lg)] = snip
prev = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blog 07 figures</title><link rel="stylesheet" href="../../../../assets/fonts/fonts.css">' + CSS + \
 '<style>body{margin:0;background:#F4F2ED;font-family:Inter,sans-serif}main{max-width:720px;margin:0 auto;padding:24px 16px}h2{font-family:"Inter Display",Inter;margin:40px 0 0}</style></head><body><main>'
for Lg in ('en', 'es'):
    prev += f'<h2>{Lg.upper()}</h2>' + ''.join(out[(n, Lg)] for n, _ in FIGS)
open('preview.html', 'w').write(prev + '</main></body></html>')
print('ok')
