# Builds self-contained HTML figure snippets (EN/ES) for blog 01, plus a preview page.
import html
CSS = """<style>
.rp-fig{--ink:#15171A;--muted:#5B5F64;--line:#DDD9D0;--card:#FFFFFF;--gut:#1F5FAF;--gut2:#7FA3D6;--heat:#B83C0B;--ref:#A4A9AE;
 position:relative;margin:32px 0;padding:20px;background:var(--card);border:1px solid var(--line);border-radius:10px;font-family:Inter,system-ui,sans-serif;color:var(--ink)}
.rp-fig *{box-sizing:border-box}
.rp-fig h4{margin:0;font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:20px;line-height:1.25;letter-spacing:-0.01em}
.rp-fig .rp-sub{margin:4px 0 16px;font-size:14px;color:var(--muted)}
.rp-fig .rp-row{display:grid;grid-template-columns:minmax(88px,28%) 1fr;gap:10px;align-items:center;margin:10px 0}
.rp-fig .rp-lab{font-size:14px;font-weight:600;line-height:1.25}
.rp-fig .rp-lab small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.rp-fig .rp-track{position:relative;height:24px}
.rp-fig .rp-bar{position:absolute;top:2px;height:20px;border-radius:0 4px 4px 0}
.rp-fig .rp-bar.rp-range{border-radius:4px}
.rp-fig .rp-val{position:absolute;top:2px;line-height:20px;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px;color:var(--ink);white-space:nowrap;padding-left:6px}
.rp-fig .rp-axis{position:relative;height:18px;margin-left:calc(28% + 10px);border-top:1px solid var(--line);font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11px;color:var(--muted)}
.rp-fig .rp-axis span{position:absolute;top:3px;transform:translateX(-50%)}
.rp-fig .rp-plot{position:relative}
.rp-fig .rp-ref{position:absolute;top:24px;bottom:0;border-left:2px dashed var(--muted)}
.rp-fig .rp-refl{position:absolute;top:-22px;transform:translateX(-50%);font-size:12px;color:var(--muted);white-space:nowrap;background:var(--card);padding:0 4px}
.rp-fig .rp-zero{position:absolute;top:0;bottom:0;border-left:1px solid var(--muted)}
.rp-fig .rp-stats{display:flex;gap:24px;flex-wrap:wrap;margin:0 0 14px}
.rp-fig .rp-stat b{display:block;font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:28px;letter-spacing:-0.02em;color:var(--ink)}
.rp-fig .rp-stat span{font-size:13px;color:var(--muted)}
.rp-fig .rp-key{display:flex;gap:16px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin:2px 0 6px}
.rp-fig .rp-key i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.rp-fig figcaption{margin-top:14px;padding-top:10px;border-top:1px solid var(--line);font-size:12px;line-height:1.5;color:var(--muted)}
.rp-fig figcaption a{color:var(--muted)}
.rp-fig .rp-sr{position:absolute;left:0;top:0;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}
.rp-fig .rp-in{position:absolute;top:2px;line-height:20px;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px;white-space:nowrap;padding-right:8px;transform:translateX(-100%)}
@media (max-width:480px){.rp-fig{padding:16px}.rp-fig h4{font-size:18px}.rp-fig .rp-row{grid-template-columns:96px 1fr}.rp-fig .rp-axis{margin-left:106px}}
</style>"""

def pct(v, lo, hi): return (v - lo) / (hi - lo) * 100

def axis(ticks, lo, hi, fmt):
    return '<div class="rp-axis">' + ''.join(f'<span style="left:{pct(t,lo,hi):.2f}%">{fmt(t)}</span>' for t in ticks) + '</div>'

def table(caption, head, rows):
    h = ''.join(f'<th>{html.escape(x)}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(c))}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="rp-sr"><table><caption>{html.escape(caption)}</caption><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

T = {
 'en': dict(
  f1t='Your finish time sets your carb target', f1s='Guideline carbs per hour during the race, by how long you will be out there',
  f1r=[('2 to 3 hours','one sugar is fine',30,60,'30 to 60 g/h'),('Over 2.5 to 3 hours','mixed sugars',60,90,'up to 90 g/h')],
  f1ref='Seville average: 35 g/h', f1u='g/h',
  f1c='Guidelines: <a href="https://doi.org/10.1080/02640414.2011.585473">Burke et al. 2011</a>, <a href="https://doi.org/10.1007/s40279-014-0148-z">Jeukendrup 2014</a> (written at the Gatorade Sports Science Institute), <a href="https://pubmed.ncbi.nlm.nih.gov/26917108/">ADA, DC and ACSM 2016</a>. Seville average: <a href="https://doi.org/10.1186/s40798-024-00801-w">Jiménez-Alfageme et al. 2025</a>.',
  f2t='Most marathoners under-fuel, and slower runners most', f2s='Share of 2022 Seville Marathon runners taking under 30 g of carbs an hour, by finish time',
  f2stats=[('35 g/h','average intake'),('9%','in the 60 to 90 g/h range')],
  f2r=[('Under 3 h',22.2),('3 to 4 h',42.1),('Over 4 h',66.7)],
  f2c='<a href="https://doi.org/10.1186/s40798-024-00801-w">Jiménez-Alfageme et al. 2025</a>. Survey of 160 runners (140 men), self-reported intake. Shows what runners did, not what works.',
  f3t='More carbs, more power left late', f3s='Critical power after 3 hours of moderate cycling, by carbs taken during the ride',
  f3r=[('Water','no carbs',236,'ref'),('60 g/h','',257,'gut2'),('120 g/h','',266,'gut')], f3ref='Fresh: 277 W', f3u='W',
  f3c='<a href="https://doi.org/10.1111/sms.70326">Norte et al. 2026</a>. 16 trained cyclists and triathletes (15 men), lab study. Measures power, not race time.',
  f4t='Two weeks of gut training paid off', f4s='Change in distance on a 1-hour running test after 2 weeks of practice',
  f4r=[('Carb gels','symptoms down 60%',5.2),('Carb food','symptoms down 63%',4.3),('Placebo','',-2.1)],
  f4c='<a href="https://doi.org/10.1139/apnm-2016-0453">Costa et al. 2017</a>. 25 endurance runners, lab trial.',
  key3=[('ref','No carbs'),('gut2','60 g/h'),('gut','120 g/h')], key4=[('gut','Gut training'),('heat','Placebo')],
  tabh1=['Race length','Guideline'], tabh2=['Finish time','Under 30 g/h'], tabh3=['During the ride','Critical power after 3 h'], tabh4=['Group','Distance change'],
 ),
 'es': dict(
  f1t='Tu tiempo final define tu meta de carbohidratos', f1s='Carbohidratos por hora que recomiendan las guías, según cuánto tiempo vas a correr',
  f1r=[('2 a 3 horas','un solo azúcar',30,60,'30 a 60 g/h'),('Más de 2.5 a 3 h','azúcares mezclados',60,90,'hasta 90 g/h')],
  f1ref='Promedio en Sevilla: 35 g/h', f1u='g/h',
  f1c='Guías: <a href="https://doi.org/10.1080/02640414.2011.585473">Burke et al. 2011</a>, <a href="https://doi.org/10.1007/s40279-014-0148-z">Jeukendrup 2014</a> (escrito en el Gatorade Sports Science Institute), <a href="https://pubmed.ncbi.nlm.nih.gov/26917108/">ADA, DC y ACSM 2016</a>. Promedio en Sevilla: <a href="https://doi.org/10.1186/s40798-024-00801-w">Jiménez-Alfageme et al. 2025</a>.',
  f2t='Casi todos comen poco, y los más lentos, menos', f2s='Corredores del Maratón de Sevilla 2022 que tomaron menos de 30 g de carbohidratos por hora, según su tiempo',
  f2stats=[('35 g/h','consumo promedio'),('9%','entre 60 y 90 g/h')],
  f2r=[('Menos de 3 h',22.2),('3 a 4 h',42.1),('Más de 4 h',66.7)],
  f2c='<a href="https://doi.org/10.1186/s40798-024-00801-w">Jiménez-Alfageme et al. 2025</a>. Encuesta a 160 corredores (140 hombres), consumo autorreportado. Muestra lo que hicieron, no lo que funciona.',
  f3t='Más carbohidratos, más potencia al final', f3s='Potencia crítica después de 3 horas de bici a ritmo moderado, según los carbohidratos tomados',
  f3r=[('Agua','sin carbohidratos',236,'ref'),('60 g/h','',257,'gut2'),('120 g/h','',266,'gut')], f3ref='Descansado: 277 W', f3u='W',
  f3c='<a href="https://doi.org/10.1111/sms.70326">Norte et al. 2026</a>. 16 ciclistas y triatletas entrenados (15 hombres), estudio de laboratorio. Mide potencia, no tiempo de carrera.',
  f4t='Dos semanas entrenando el estómago sí sirvieron', f4s='Cambio en la distancia de una prueba de 1 hora corriendo, tras 2 semanas de práctica',
  f4r=[('Geles','molestias 60% menos',5.2),('Comida','molestias 63% menos',4.3),('Placebo','',-2.1)],
  f4c='<a href="https://doi.org/10.1139/apnm-2016-0453">Costa et al. 2017</a>. 25 corredores de resistencia, estudio de laboratorio.',
  key3=[('ref','Sin carbohidratos'),('gut2','60 g/h'),('gut','120 g/h')], key4=[('gut','Estómago entrenado'),('heat','Placebo')],
  tabh1=['Duración','Guía'], tabh2=['Tiempo final','Menos de 30 g/h'], tabh3=['Durante la bici','Potencia crítica tras 3 h'], tabh4=['Grupo','Cambio de distancia'],
 )}
COL = {'gut':'var(--gut)','gut2':'var(--gut2)','heat':'var(--heat)','ref':'var(--ref)'}
dec = lambda v, l: (f'{v:.1f}'.replace('.', '.') )

def fig1(t):
    lo, hi = 0, 100
    rows = ''.join(f'<div class="rp-row"><div class="rp-lab">{a}<small>{lab} · {b}</small></div><div class="rp-track" title="{a}: {lab}"><div class="rp-bar rp-range" style="left:{pct(x0,lo,hi):.2f}%;width:{pct(x1,lo,hi)-pct(x0,lo,hi):.2f}%;background:var(--gut)"></div></div></div>' for a,b,x0,x1,lab in t['f1r'])
    ref = f'<div class="rp-ref" style="left:calc(28% + 10px + (100% - 28% - 10px) * {pct(35,lo,hi)/100:.4f})"><span class="rp-refl">{t["f1ref"]}</span></div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f1t"])}"><h4>{t["f1t"]}</h4><p class="rp-sub">{t["f1s"]}</p><div class="rp-plot" style="padding-top:30px">{ref}{rows}</div>{axis([0,30,60,90],lo,hi,lambda x:f"{x}")}' + \
      table(t['f1t'], t['tabh1'], [(a,lab) for a,b,x0,x1,lab in t['f1r']]) + f'<figcaption>{t["f1c"]}</figcaption></figure>'

def fig2(t):
    lo, hi = 0, 100
    stats = '<div class="rp-stats">' + ''.join(f'<div class="rp-stat"><b>{v}</b><span>{s}</span></div>' for v,s in t['f2stats']) + '</div>'
    rows = ''.join(f'<div class="rp-row"><div class="rp-lab">{a}</div><div class="rp-track" title="{a}: {v}%"><div class="rp-bar" style="left:0;width:{pct(v,lo,hi):.2f}%;background:var(--heat)"></div><div class="rp-val" style="left:{pct(v,lo,hi):.2f}%">{v}%</div></div></div>' for a,v in t['f2r'])
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f2t"])}"><h4>{t["f2t"]}</h4><p class="rp-sub">{t["f2s"]}</p>{stats}{rows}{axis([0,25,50,75,100],lo,hi,lambda x:f"{x}%")}' + \
      table(t['f2s'], t['tabh2'], [(a,f'{v}%') for a,v in t['f2r']]) + f'<figcaption>{t["f2c"]}</figcaption></figure>'

def fig3(t):
    lo, hi = 0, 300
    key = '<div class="rp-key">' + ''.join(f'<span><i style="background:{COL[c]}"></i>{n}</span>' for c,n in t['key3']) + '</div>'
    rows = ''.join(f'<div class="rp-row"><div class="rp-lab">{a}{f"<small>{b}</small>" if b else ""}</div><div class="rp-track" title="{a}: {v} W"><div class="rp-bar" style="left:0;width:{pct(v,lo,hi):.2f}%;background:{COL[c]}"></div><div class="rp-in" style="left:{pct(v,lo,hi):.2f}%;color:{"#FFFFFF" if c=="gut" else "#15171A"}">{v} W</div></div></div>' for a,b,v,c in t['f3r'])
    ref = f'<div class="rp-ref" style="left:calc(28% + 10px + (100% - 28% - 10px) * {pct(277,lo,hi)/100:.4f})"><span class="rp-refl" style="transform:translateX(-90%)">{t["f3ref"]}</span></div>'
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f3t"])}"><h4>{t["f3t"]}</h4><p class="rp-sub">{t["f3s"]}</p>{key}<div class="rp-plot" style="padding-top:30px">{ref}{rows}</div>{axis([0,100,200,300],lo,hi,lambda x:f"{x}")}' + \
      table(t['f3s'], t['tabh3'], [(a,f'{v} W') for a,b,v,c in t['f3r']] + [(t['f3ref'].split(':')[0], '277 W')]) + f'<figcaption>{t["f3c"]}</figcaption></figure>'

def fig4(t):
    lo, hi = -4, 8
    z = pct(0,lo,hi)
    key = '<div class="rp-key">' + ''.join(f'<span><i style="background:{COL[c]}"></i>{n}</span>' for c,n in t['key4']) + '</div>'
    def bar(v):
        if v >= 0:
            return f'<div class="rp-bar" style="left:{z:.2f}%;width:{pct(v,lo,hi)-z:.2f}%;background:var(--gut)"></div><div class="rp-val" style="left:{pct(v,lo,hi):.2f}%">+{v}%</div>'
        return f'<div class="rp-bar" style="left:{pct(v,lo,hi):.2f}%;width:{z-pct(v,lo,hi):.2f}%;background:var(--heat);border-radius:4px 0 0 4px"></div><div class="rp-val" style="left:{z:.2f}%">{v}%</div>'
    rows = ''.join(f'<div class="rp-row"><div class="rp-lab">{a}{f"<small>{b}</small>" if b else ""}</div><div class="rp-track" title="{a}: {"+" if v>0 else ""}{v}%"><div class="rp-zero" style="left:{z:.2f}%"></div>{bar(v)}</div></div>' for a,b,v in t['f4r'])
    return f'<figure class="rp-fig" aria-label="{html.escape(t["f4t"])}"><h4>{t["f4t"]}</h4><p class="rp-sub">{t["f4s"]}</p>{key}{rows}{axis([-4,0,4,8],lo,hi,lambda x:(f"+{x}%" if x>0 else f"{x}%"))}' + \
      table(t['f4s'], t['tabh4'], [(a,f'{"+" if v>0 else ""}{v}%') for a,b,v in t['f4r']]) + f'<figcaption>{t["f4c"]}</figcaption></figure>'

FIGS = [('fig1-carb-targets',fig1),('fig2-seville-intake',fig2),('fig3-late-power',fig3),('fig4-gut-training',fig4)]
out = {}
for L in ('en','es'):
    for name, fn in FIGS:
        snip = fn(T[L])
        open(f'{name}-{L}.html','w').write(CSS + '\n' + snip + '\n')
        out[(name,L)] = snip
prev = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blog 01 figures</title><link rel="stylesheet" href="../../../../assets/fonts/fonts.css">' + CSS + \
 '<style>body{margin:0;background:#F4F2ED;font-family:Inter,sans-serif}main{max-width:720px;margin:0 auto;padding:24px 16px}h2{font-family:"Inter Display",Inter;margin:40px 0 0}</style></head><body><main>'
for L in ('en','es'):
    prev += f'<h2>{L.upper()}</h2>' + ''.join(out[(n,L)] for n,_ in FIGS)
open('preview.html','w').write(prev + '</main></body></html>')
print('ok')
