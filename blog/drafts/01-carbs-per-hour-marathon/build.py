import re, csv, io
def parts(f):
    s=open(f).read()
    d={}
    for k,v in re.findall(r'<!-- (\w+) -->\n(.*?)(?=\n<!-- \w+ -->|\Z)',s,re.S): d[k]=v.strip()
    return d
en,es=parts('en.md'),parts('es.md')
meta={
 'slug':'carbs-per-hour-marathon',
 'meta_title_en':'Carbs per hour in a marathon: what the research says',
 'meta_title_es':'Carbohidratos por hora en un maratón: qué dice la ciencia',
 'meta_description_en':'Most marathoners should aim for 60 to 90 g of carbs an hour, set by finish time. What the guidelines and studies say, and how to train your gut.',
 'meta_description_es':'Apunta a 60 a 90 g de carbohidratos por hora según tu tiempo final. Qué dicen las guías y los estudios, y cómo entrenar tu estómago.',
 'study_slugs':'ada-dc-acsm-2016;burke-2011;jeukendrup-2014;jimenez-alfageme-2025;smyth-2021;rapoport-2010;norte-2026;mazza-2026;costa-2017a;miall-2018;von-kanel-cordoba-2026;morton-2026;ravikanti-2025;hearris-2022',
 'published_date':'2026-10-17',
}
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
row={'slug':meta['slug'],'title_en':en['title'],'title_es':es['title'],'answer_en':en['answer'],'answer_es':es['answer'],
 'body_en':body(en,'en'),'body_es':body(es,'es'),'faq_en':en['faq'],'faq_es':es['faq'],
 'meta_title_en':meta['meta_title_en'],'meta_title_es':meta['meta_title_es'],'meta_description_en':meta['meta_description_en'],
 'meta_description_es':meta['meta_description_es'],'study_slugs':meta['study_slugs'],'published_date':meta['published_date']}
hdr='slug,title_en,title_es,answer_en,answer_es,body_en,body_es,faq_en,faq_es,meta_title_en,meta_title_es,meta_description_en,meta_description_es,study_slugs,published_date'.split(',')
with open('carbs-per-hour-marathon.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=hdr,quoting=csv.QUOTE_ALL); w.writeheader(); w.writerow(row)
def wc(t): t=re.sub(r'<!--.*?-->','',t); t=re.sub(r'\]\([^)]*\)',']',t); return len(re.findall(r"[A-Za-zÀ-ÿ0-9][\w'.%/-]*",t))
print({k:(len(meta[k])) for k in meta if k.startswith('meta')})
print('words en',wc('\n'.join(en.values())),'es',wc('\n'.join(es.values())))
allt=open('en.md').read()+open('es.md').read()
print('dashes',len(re.findall('[–—]',allt)))
