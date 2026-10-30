# Builds self-contained HTML figure snippets (EN/ES) for blog 03, plus a preview page.
# Same structure and class names as blogs 01 and 02; Pacing pillar color #008A6C.
import html
PC, PC2 = '#008A6C', '#DCEFE9'
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
@media (max-width:480px){.rp-fig{padding:16px}.rp-fig h4{font-size:18px}.rp-fig .rp-row{grid-template-columns:132px 1fr}.rp-fig .rp-axis,.rp-fig .rp-axl{margin-left:142px}.rp-fig .rp-cards{grid-template-columns:1fr}.rp-fig .rp-card b{font-size:24px}}
</style>""" % (PC, PC2)

L = {
 'smyth': '<a href="https://doi.org/10.1371/journal.pone.0251513">Smyth 2021</a>',
 'dong': '<a href="https://doi.org/10.1371/journal.pone.0352808">Dong &amp; Li 2026</a>',
 'norte': '<a href="https://doi.org/10.1111/sms.70326">Norte et al. 2026</a>',
}

def pct(v, lo, hi): return (v - lo) / (hi - lo) * 100

def axis(ticks, lo, hi, fmt):
    return '<div class="rp-axis">' + ''.join(f'<span style="left:{pct(t,lo,hi):.2f}%">{fmt(t)}</span>' for t in ticks) + '</div>'

def table(caption, head, rows):
    h = ''.join(f'<th>{html.escape(x)}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(c))}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="rp-sr"><table><caption>{html.escape(caption)}</caption><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

def bars(rows, lo, hi, ticks, tickfmt, unit, color_of):
    out = ''
    grid = ''.join(f'<div class="rp-grid" style="left:{pct(x,lo,hi):.2f}%"></div>' for x in ticks)
    for lab, small, v, kind in rows:
        p = pct(v, lo, hi)
        side = ' rp-left' if p > 72 else ''
        out += (f'<div class="rp-row"><div class="rp-lab">{lab}{f"<small>{small}</small>" if small else ""}</div>'
                f'<div class="rp-track" title="{html.escape(lab)}: {v}{unit}">{grid}'
                f'<div class="rp-bar" style="left:0;width:{max(p,0.6):.2f}%;background:{color_of(kind)}"></div>'
                f'<div class="rp-val{side}" style="left:{p:.2f}%">{v}{unit}</div></div></div>')
    return out + axis(ticks, lo, hi, tickfmt)

T = {
 'en': dict(
  f1t='The wall is common, and it costs about half an hour', f1s='Recreational marathoners in more than 4 million race records, men and women',
  f1cards=[('28% / 17%','of men and of women hit the wall'),('Km 29.6 / 29.3','where it started, on average'),
           ('10.72 / 9.61 km','how long it lasted'),('31.50 / 33.20 min','lost against a recent best')],
  f1note='Men / women', f1c=f'Source: {L["smyth"]}. Observational race data, 270 races. The wall here means slowing at least 25% for 5 km or more after km 20.',
  tabh1=['Number (men / women)','Finding'],
  f2t='Fast starts were linked to the wall', f2s='Share of Boston finishers who hit the wall, by how they paced',
  f2r=[('Started more than 5% fast','vs their average pace',26.6,'heat'),('Started near average pace','',1.5,'pc'),
       ('Even pacers','47.9% of runners',0.2,'pc'),('Variable pacers','pace swung up and down',85.4,'heat')],
  f2c=f'Source: {L["dong"]}. 78,912 Boston Marathon finishers, 2015 to 2017. Observational: a link, not proof. One net-downhill course, no weather data.',
  tabh2=['Pacing','Detail','Hit the wall'],
  f3t='More carbs, more power left after 3 hours', f3s='Critical power after 3 h of cycling, by what riders took in',
  f3r=[('Fresh','before the ride',277,'ref'),('Water only','after 3 h',236,'heat'),('60 g/h','after 3 h',257,'pc'),('120 g/h','after 3 h',266,'pc')],
  f3c=f'Source: {L["norte"]}. Randomized crossover trial, 16 trained cyclists and triathletes (15 men). Lab cycling, no race time measured.',
  f3ax='Watts',
  tabh3=['Condition','When','Critical power'],
 ),
 'es': dict(
  f1t='El muro es común y cuesta cerca de media hora', f1s='Maratonistas recreativos en más de 4 millones de resultados, hombres y mujeres',
  f1cards=[('28% / 17%','de los hombres y de las mujeres chocó con el muro'),('Km 29.6 / 29.3','dónde empezó, en promedio'),
           ('10.72 / 9.61 km','cuánto duró'),('31.50 / 33.20 min','perdidos frente a su mejor marca reciente')],
  f1note='Hombres / mujeres', f1c=f'Fuente: {L["smyth"]}. Datos observacionales de 270 carreras. Aquí el muro es bajar el ritmo al menos un 25% durante 5 km o más después del km 20.',
  tabh1=['Número (hombres / mujeres)','Hallazgo'],
  f2t='Salir rápido se relacionó con el muro', f2s='Porcentaje de corredores de Boston que chocó con el muro, según cómo dosificó',
  f2r=[('Salió más de un 5% rápido','frente a su ritmo promedio',26.6,'heat'),('Salió cerca de su ritmo promedio','',1.5,'pc'),
       ('Ritmo parejo','47.9% de los corredores',0.2,'pc'),('Ritmo variable','cambió de ritmo una y otra vez',85.4,'heat')],
  f2c=f'Fuente: {L["dong"]}. 78,912 corredores que terminaron el Maratón de Boston, 2015 a 2017. Observacional: una relación, no una prueba. Un solo circuito en bajada neta, sin datos de clima.',
  tabh2=['Ritmo','Detalle','Chocó con el muro'],
  f3t='Más carbohidratos, más potencia tras 3 horas', f3s='Potencia crítica después de 3 h de bici, según lo que tomaron',
  f3r=[('Descansados','antes de la bici',277,'ref'),('Solo agua','tras 3 h',236,'heat'),('60 g/h','tras 3 h',257,'pc'),('120 g/h','tras 3 h',266,'pc')],
  f3c=f'Fuente: {L["norte"]}. Ensayo cruzado aleatorizado, 16 ciclistas y triatletas entrenados (15 hombres). Bici en laboratorio, sin tiempo de carrera.',
  f3ax='Vatios',
  tabh3=['Condición','Cuándo','Potencia crítica'],
 )}

COL = {'pc': 'var(--pc)', 'heat': 'var(--heat)', 'ref': 'var(--ref)'}

def fig1(t):
    cards = '<div class="rp-cards" aria-hidden="true">' + ''.join(f'<div class="rp-card"><b>{n}</b><span>{d}</span><small>{t["f1note"]}</small></div>' for n, d in t['f1cards']) + '</div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f1t"])}"><h4>{t["f1t"]}</h4><p class="rp-sub">{t["f1s"]}</p>{cards}' + \
      table(t['f1s'], t['tabh1'], t['f1cards']) + f'<figcaption>{t["f1c"]}</figcaption></figure>'

def fig2(t):
    body = bars(t['f2r'], 0, 100, [0, 25, 50, 75, 100], lambda x: f'{x}%' if x in (0,50,100) else '', '%', lambda k: COL[k])
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f2t"])}"><h4>{t["f2t"]}</h4><p class="rp-sub">{t["f2s"]}</p>{body}' + \
      table(t['f2s'], t['tabh2'], [(a, b, f'{v}%') for a, b, v, k in t['f2r']]) + f'<figcaption>{t["f2c"]}</figcaption></figure>'

def fig3(t):
    body = bars(t['f3r'], 0, 300, [0, 100, 200, 300], lambda x: str(x), ' W', lambda k: COL[k])
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f3t"])}"><h4>{t["f3t"]}</h4><p class="rp-sub">{t["f3s"]}</p>{body}<p class="rp-axl">{t["f3ax"]}</p>' + \
      table(t['f3s'], t['tabh3'], [(a, b, f'{v} W') for a, b, v, k in t['f3r']]) + f'<figcaption>{t["f3c"]}</figcaption></figure>'

FIGS = [('fig1-wall-numbers', fig1), ('fig2-fast-start', fig2), ('fig3-late-power', fig3)]
out = {}
for Lg in ('en', 'es'):
    for name, fn in FIGS:
        snip = fn(T[Lg])
        open(f'{name}-{Lg}.html', 'w').write(CSS + '\n' + snip + '\n')
        out[(name, Lg)] = snip
prev = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blog 03 figures</title><link rel="stylesheet" href="../../../../assets/fonts/fonts.css">' + CSS + \
 '<style>body{margin:0;background:#F4F2ED;font-family:Inter,sans-serif}main{max-width:720px;margin:0 auto;padding:24px 16px}h2{font-family:"Inter Display",Inter;margin:40px 0 0}</style></head><body><main>'
for Lg in ('en', 'es'):
    prev += f'<h2>{Lg.upper()}</h2>' + ''.join(out[(n, Lg)] for n, _ in FIGS)
open('preview.html', 'w').write(prev + '</main></body></html>')
print('ok')
