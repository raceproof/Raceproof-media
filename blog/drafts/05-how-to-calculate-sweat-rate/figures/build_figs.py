# Builds self-contained HTML figure snippets (EN/ES) for blog 05, plus a preview page.
# Same structure and class names as blogs 01 to 03; Hydration pillar color #2E9FD8.
import html
PC, PC2 = '#2E9FD8', '#E3F2FA'
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
.rp-fig .rp-wh{position:absolute;top:11px;height:2px;background:var(--ink)}
.rp-fig .rp-wh:before,.rp-fig .rp-wh:after{content:"";position:absolute;top:-5px;width:2px;height:12px;background:var(--ink)}
.rp-fig .rp-wh:before{left:0}.rp-fig .rp-wh:after{right:0}
.rp-fig .rp-refl{position:absolute;top:-4px;bottom:-4px;border-left:2px solid var(--ink)}\n.rp-fig .rp-val{z-index:2}\n.rp-fig .rp-bar,.rp-fig .rp-wh{z-index:1}\n.rp-fig .rp-refl{z-index:0}\n.rp-fig .rp-refl ~ .rp-val:not(.rp-left):not(.rp-in){background:var(--card);padding-right:10px;margin-left:2px}
.rp-fig .rp-val.rp-in{color:#FFFFFF}\n.rp-fig .rp-card.rp-res{background:var(--pc)}.rp-fig .rp-card.rp-res b,.rp-fig .rp-card.rp-res span,.rp-fig .rp-card.rp-res small{color:#FFFFFF}
.rp-fig .rp-card b{color:#1B6F99}
.rp-fig figcaption{margin-top:14px;padding-top:10px;border-top:1px solid var(--line);font-size:12px;line-height:1.5;color:var(--muted)}
.rp-fig figcaption a{color:var(--muted)}
.rp-fig .rp-sr{position:absolute;left:0;top:0;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%%);white-space:nowrap;border:0}
@media (max-width:480px){.rp-fig{padding:16px}.rp-fig h4{font-size:18px}.rp-fig .rp-row{grid-template-columns:132px 1fr}.rp-fig .rp-axis,.rp-fig .rp-axl{margin-left:142px}.rp-fig .rp-cards{grid-template-columns:1fr}.rp-fig .rp-card b{font-size:24px}}
</style>""" % (PC, PC2)

L = {
 'sawka': '<a href="https://doi.org/10.1249/mss.0b013e31802ca597">Sawka et al. 2007</a>',
 'baker': '<a href="https://doi.org/10.1007/s40279-017-0691-5">Baker 2017</a>',
 'barnes': '<a href="https://doi.org/10.1080/02640414.2019.1633159">Barnes et al. 2019</a>',
 'klous': '<a href="https://doi.org/10.1016/j.jtherbio.2020.102697">Klous et al. 2020</a>',
}

def pct(v, lo, hi): return (v - lo) / (hi - lo) * 100

def axis(ticks, lo, hi, fmt):
    return '<div class="rp-axis">' + ''.join(f'<span style="left:{pct(t,lo,hi):.2f}%">{fmt(t)}</span>' for t in ticks) + '</div>'

def table(caption, head, rows):
    h = ''.join(f'<th>{html.escape(x)}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(c))}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="rp-sr"><table><caption>{html.escape(caption)}</caption><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

COL = {'pc': 'var(--pc)', 'ref': 'var(--ref)'}

def bars(rows, lo, hi, ticks, tickfmt, refline=None):
    out = ''
    grid = ''.join(f'<div class="rp-grid" style="left:{pct(x,lo,hi):.2f}%"></div>' for x in ticks)
    rl = f'<div class="rp-refl" style="left:{pct(refline,lo,hi):.2f}%"></div>' if refline is not None else ''
    for lab, small, v, label, kind, wh in rows:
        p = pct(v, lo, hi)
        whisk = ''
        lp = p
        if wh:
            a, b = pct(wh[0], lo, hi), pct(wh[1], lo, hi)
            whisk = f'<div class="rp-wh" style="left:{a:.2f}%;width:{b-a:.2f}%"></div>'
            lp = 0
        side = ' rp-left' if lp > 66 else (' rp-in' if wh else '')
        out += (f'<div class="rp-row"><div class="rp-lab">{lab}{f"<small>{small}</small>" if small else ""}</div>'
                f'<div class="rp-track" title="{html.escape(lab)}: {html.escape(label)}">{grid}{rl}'
                f'<div class="rp-bar" style="left:0;width:{max(p,0.6):.2f}%;background:{COL[kind]}"></div>{whisk}'
                f'<div class="rp-val{side}" style="left:{lp:.2f}%">{label}</div></div></div>')
    return out + axis(ticks, lo, hi, tickfmt)

T = {
 'en': dict(
  f1t='Your sweat rate from two weigh-ins', f1s='An example: a steady 1-hour run',
  f1cards=[('70.0 kg','Weight before','154.3 lb',''),('68.9 kg','Weight after','151.9 lb. Lost 1.1 kg',''),
           ('+ 0.4 L','What you drank','About 14 oz',''),('1.5 L/h','Your sweat rate: 1.1 + 0.4, over 1 hour','About 51 oz an hour','res')],
  f1c=f'Method: {L["sawka"]}; {L["baker"]}. Example numbers are illustrative. 1 kg of weight lost counts as about 1 L of sweat (our conversion).',
  tabh1=['Value','Step','Imperial'],
  f2t='Endurance athletes sweat about 1.3 L an hour, with a wide spread', f2s='Average whole-body sweat rate by sport. The line on the endurance bar shows ± 0.57 L/h.',
  f2r=[('Endurance','1.28 ± 0.57 L/h',1.28,'1.28','pc',(0.71,1.85)),('American football','',1.51,'1.51','ref',None),
       ('Basketball','',0.95,'0.95','ref',None),('Soccer','',0.94,'0.94','ref',None),('Baseball','',0.83,'0.83','ref',None)],
  f2ax='Liters per hour',
  f2c=f'Source: {L["barnes"]}. Testing data from 1,303 athletes, 2000 to 2017. Athletes who came in for testing, not a random sample. All authors work at the Gatorade Sports Science Institute (PepsiCo).',
  tabh2=['Sport','Detail','Sweat rate (L/h)'],
  f3t='After 10 days of heat, more sweat and less salt', f3s='Change by day 10 of heat training, as a share of day 1 (day 1 = 100%, dark line)',
  f3r=[('Sweat rate, arm','local patch',158,'+58%','pc',None),('Sweat rate, back','local patch',136,'+36%','pc',None),
       ('Sweat sodium','',60,'about 60%','ref',None)],
  f3ax='Percent of day 1',
  f3c=f'Source: {L["klous"]}. Lab study, 8 people, 10 days of cycling at 33°C (91°F) and 65% humidity. Local sweat patches, not whole-body weigh-ins.',
  tabh3=['Measure','Detail','Day 10 vs day 1'],
 ),
 'es': dict(
  f1t='Tu tasa de sudoración con dos pesajes', f1s='Un ejemplo: 1 hora de carrera a ritmo constante',
  f1cards=[('70.0 kg','Peso antes','154.3 lb',''),('68.9 kg','Peso después','151.9 lb. Perdiste 1.1 kg',''),
           ('+ 0.4 L','Lo que tomaste','Unas 14 oz',''),('1.5 L/h','Tu tasa de sudoración: 1.1 + 0.4, en 1 hora','Unas 51 oz por hora','res')],
  f1c=f'Método: {L["sawka"]}; {L["baker"]}. Los números del ejemplo son ilustrativos. 1 kg de peso perdido cuenta como cerca de 1 L de sudor (conversión nuestra).',
  tabh1=['Valor','Paso','Imperial'],
  f2t='Los atletas de resistencia sudan cerca de 1.3 L por hora, con mucha variación', f2s='Tasa de sudoración promedio de todo el cuerpo por deporte. La línea en la barra de resistencia muestra ± 0.57 L/h.',
  f2r=[('Resistencia','1.28 ± 0.57 L/h',1.28,'1.28','pc',(0.71,1.85)),('Fútbol americano','',1.51,'1.51','ref',None),
       ('Básquetbol','',0.95,'0.95','ref',None),('Fútbol','',0.94,'0.94','ref',None),('Béisbol','',0.83,'0.83','ref',None)],
  f2ax='Litros por hora',
  f2c=f'Fuente: {L["barnes"]}. Datos de pruebas de 1,303 atletas, 2000 a 2017. Atletas que fueron a hacerse la prueba, no una muestra al azar. Todos los autores trabajan en el Gatorade Sports Science Institute (PepsiCo).',
  tabh2=['Deporte','Detalle','Sudoración (L/h)'],
  f3t='Tras 10 días de calor, más sudor y menos sal', f3s='Cambio al día 10 de entrenamiento con calor, frente al día 1 (día 1 = 100%, línea oscura)',
  f3r=[('Sudoración, brazo','parche local',158,'+58%','pc',None),('Sudoración, espalda','parche local',136,'+36%','pc',None),
       ('Sodio del sudor','',60,'cerca del 60%','ref',None)],
  f3ax='Porcentaje del día 1',
  f3c=f'Fuente: {L["klous"]}. Estudio de laboratorio, 8 personas, 10 días de bici a 33°C (91°F) y 65% de humedad. Parches locales de sudor, no el peso de todo el cuerpo.',
  tabh3=['Medida','Detalle','Día 10 frente al día 1'],
 )}

def fig1(t):
    cards = '<div class="rp-cards" aria-hidden="true">' + ''.join(f'<div class="rp-card{" rp-res" if k else ""}"><b>{n}</b><span>{d}</span><small>{s}</small></div>' for n, d, s, k in t['f1cards']) + '</div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f1t"])}"><h4>{t["f1t"]}</h4><p class="rp-sub">{t["f1s"]}</p>{cards}' + \
      table(t['f1s'], t['tabh1'], [(n, d, s) for n, d, s, k in t['f1cards']]) + f'<figcaption>{t["f1c"]}</figcaption></figure>'

def fig2(t):
    body = bars(t['f2r'], 0, 2.0, [0, 0.5, 1.0, 1.5, 2.0], lambda x: f'{x:.1f}')
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f2t"])}"><h4>{t["f2t"]}</h4><p class="rp-sub">{t["f2s"]}</p>{body}<p class="rp-axl">{t["f2ax"]}</p>' + \
      table(t['f2s'], t['tabh2'], [(a, b, v) for a, b, v, l, k, w in t['f2r']]) + f'<figcaption>{t["f2c"]}</figcaption></figure>'

def fig3(t):
    body = bars(t['f3r'], 0, 200, [0, 50, 100, 150, 200], lambda x: f'{x}%' if x in (0,100,200) else '', refline=100)
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f3t"])}"><h4>{t["f3t"]}</h4><p class="rp-sub">{t["f3s"]}</p>{body}<p class="rp-axl">{t["f3ax"]}</p>' + \
      table(t['f3s'], t['tabh3'], [(a, b, l) for a, b, v, l, k, w in t['f3r']]) + f'<figcaption>{t["f3c"]}</figcaption></figure>'

FIGS = [('fig1-sweat-test', fig1), ('fig2-sweat-spread', fig2), ('fig3-heat-change', fig3)]
out = {}
for Lg in ('en', 'es'):
    for name, fn in FIGS:
        snip = fn(T[Lg])
        open(f'{name}-{Lg}.html', 'w').write(CSS + '\n' + snip + '\n')
        out[(name, Lg)] = snip
prev = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blog 05 figures</title><link rel="stylesheet" href="../../../../assets/fonts/fonts.css">' + CSS + \
 '<style>body{margin:0;background:#F4F2ED;font-family:Inter,sans-serif}main{max-width:720px;margin:0 auto;padding:24px 16px}h2{font-family:"Inter Display",Inter;margin:40px 0 0}</style></head><body><main>'
for Lg in ('en', 'es'):
    prev += f'<h2>{Lg.upper()}</h2>' + ''.join(out[(n, Lg)] for n, _ in FIGS)
open('preview.html', 'w').write(prev + '</main></body></html>')
print('ok')
