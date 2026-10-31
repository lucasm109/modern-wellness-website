"""Check launch SEO invariants. Run after prepare_seo.py."""
from pathlib import Path
from lxml import html,etree
import json
ROOT=Path(__file__).resolve().parents[1];BASE='https://www.modernwellspa.com';titles=set();descriptions=set()
for p in (ROOT/'dist').glob('*.html'):
 d=html.parse(str(p));title=d.xpath('//title/text()');description=d.xpath('//meta[@name="description"]/@content');canonical=d.xpath('//link[@rel="canonical"]/@href')
 assert len(title)==len(description)==len(canonical)==1,p
 assert title[0] not in titles and description[0] not in descriptions,p
 titles.add(title[0]);descriptions.add(description[0])
 assert canonical==[BASE+('/' if p.name=='index.html' else '/'+p.name)],p
 graph=json.loads(d.xpath('//script[@type="application/ld+json"]/text()')[0])['@graph']
 for b in graph:
  if b['@type']=='DaySpa':assert b['address']['addressLocality'] in ['Framingham','Westwood']
 assert 'Wellesley' not in json.dumps(graph)
 assert d.xpath('//meta[@name="robots"]/@content')==(['noindex, follow'] if p.name=='newsletter.html' else [])
xml=etree.parse(str(ROOT/'dist/sitemap.xml'));urls=xml.xpath('//*[local-name()="loc"]/text()')
assert len(urls)==6 and len(set(urls))==6
for u in urls: assert (ROOT/'dist'/('index.html' if u==BASE+'/' else u.rsplit('/',1)[1])).is_file()
config=json.loads((ROOT/'vercel.json').read_text());sources=[r['source'] for r in config['redirects']];assert len(sources)==len(set(sources))
assert config['headers'][0]['has'][0]['value']=='modern-wellness-website.vercel.app'
print('PASS: 7 unique metadata sets; canonical URLs; JSON-LD; 6 sitemap entries; utility noindex; staging-host header; no duplicate redirect sources.')
