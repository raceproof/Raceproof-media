import re, csv, io
def parts(f):
    s=open(f).read()
    d={}
    for k,v in re.findall(r'<!-- (\w+) -->\n(.*?)(?=\n<!-- \w+ -->|\Z)',s,re.S): d[k]=v.strip()
    return d
en,es=parts('en.md'),parts('es.md')
meta={
 'slug':'heat-acclimation-how-long',
 'meta_title_en':'How long does heat acclimation take? What studies show',
 'meta_title_es':'¿Cuánto tarda la aclimatación al calor? Qué dice la ciencia',
 'meta_description_en':'Plan on 1 to 2 weeks of heat sessions; some changes start within 5 days. What the studies show, how long it lasts and when to start for your race.',
 'meta_description_es':'Cuenta con 1 a 2 semanas de sesiones en calor; algunos cambios llegan en 5 días. Qué dicen los estudios, cuánto dura y cuándo empezar.',
 'study_slugs':'',
 'published_date':'2026-10-28',
 'cover_stat_en':'5 days','cover_stat_es':'5 días',
 'cover_label_en':'of hot rides raised plasma volume 7.3% in trained men',
 'cover_label_es':'de bici en calor subieron 7.3% el volumen de plasma',
 'cover_pillar':'Heat',
}
for k in ['cover_label_en','cover_label_es']: assert len(meta[k].split())<12,k
for k in ['meta_title_en','meta_title_es']: assert len(meta[k])<60,(k,len(meta[k]))
for k in ['meta_description_en','meta_description_es']: assert len(meta[k])<155,(k,len(meta[k]))
def embed(text, lang):
    first=[True]
    def rep(m):
        snip=open(f"figures/{m.group(1)}-{lang}.html").read()
        if not first[0]: snip=snip.split('</style>',1)[1].strip()
        first[0]=False
        return snip.strip()
    return re.sub(r'<!-- fig:([\w-]+) -->', rep, text)
def body(d, lang='en'): return embed(d['body'], lang)+'\n\n'+d['cta']
import json
def faq_json(t):
    items=[]
    for blk in re.split(r'\n(?=### )', t.strip()):
        q,_,a=blk.partition('\n'); items.append({'q':q.lstrip('#').strip(),'a':a.strip()})
    return json.dumps(items, ensure_ascii=False)
def study_urls(*texts):
    seen=[]
    for t in texts:
        for u in re.findall(r'\((https://(?:doi\.org|pubmed\.ncbi\.nlm\.nih\.gov)/[^)\s]+)\)', t):
            if u not in seen: seen.append(u)
    return json.dumps(seen)
meta['study_slugs']=study_urls(en['body'],en['faq'])
row={'slug':meta['slug'],'title_en':en['title'],'title_es':es['title'],'answer_en':en['answer'],'answer_es':es['answer'],
 'body_en':body(en,'en'),'body_es':body(es,'es'),'faq_en':faq_json(en['faq']),'faq_es':faq_json(es['faq']),
 'meta_title_en':meta['meta_title_en'],'meta_title_es':meta['meta_title_es'],'meta_description_en':meta['meta_description_en'],
 'meta_description_es':meta['meta_description_es'],'study_slugs':meta['study_slugs'],'published_date':meta['published_date'],'cover_stat_en':meta['cover_stat_en'],'cover_stat_es':meta['cover_stat_es'],'cover_label_en':meta['cover_label_en'],'cover_label_es':meta['cover_label_es'],'cover_pillar':meta['cover_pillar']}
hdr='slug,title_en,title_es,answer_en,answer_es,body_en,body_es,faq_en,faq_es,meta_title_en,meta_title_es,meta_description_en,meta_description_es,study_slugs,published_date,cover_stat_en,cover_stat_es,cover_label_en,cover_label_es,cover_pillar'.split(',')
with open('heat-acclimation-how-long.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=hdr,quoting=csv.QUOTE_ALL); w.writeheader(); w.writerow(row)
def wc(t): t=re.sub(r'<!--.*?-->','',t); t=re.sub(r'\]\([^)]*\)',']',t); return len(re.findall(r"[A-Za-zÀ-ÿ0-9][\w'.%/-]*",t))
print({k:(len(meta[k])) for k in meta if k.startswith('meta')})
print('words en',wc('\n'.join(en.values())),'es',wc('\n'.join(es.values())))
allt=open('en.md').read()+open('es.md').read()
print('dashes',len(re.findall('[–—]',allt)))
# Validation
import json
rows=list(csv.reader(open('heat-acclimation-how-long.csv',newline='')))
assert rows[0]==hdr and len(rows)==2 and all(len(r)==20 for r in rows), 'field count'
d=dict(zip(rows[0],rows[1]))
for k in ['faq_en','faq_es','study_slugs']: json.loads(d[k])
for f in json.loads(d['faq_en'])+json.loads(d['faq_es']): assert f['q'] and f['a']
assert d['cover_pillar'] in ['Gut','Hydration','Heat','Terrain','Durability','Pacing','Taper']
for u in json.loads(d['study_slugs']):
    assert u in d['body_en'] and u in d['body_es'], ('not linked in body', u)
full=open('heat-acclimation-how-long.csv').read()
assert not re.search('[–—]',full), 'dash in csv'
assert '!' not in re.sub(r'<!--.*?-->|<!doctype','',d['body_en']+d['body_es']+d['answer_en']+d['answer_es']+d['faq_en']+d['faq_es']), 'exclamation'
print('valid; studies',len(json.loads(d['study_slugs'])))
