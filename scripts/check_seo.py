"""Validate migration routes, metadata, sitemap, assets and internal anchors."""
from pathlib import Path
from lxml import html,etree
from urllib.parse import urlsplit,unquote
import csv,json
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist';BASE='https://www.modernwellspa.com'
extra=json.loads((ROOT/'seo/generated-pages.json').read_text());noindex={'newsletter.html','404.html'}
config=json.loads((ROOT/'vercel.json').read_text());redirects={r['source']:r['destination'] for r in config['redirects']};rewrites={r['source']:r['destination'] for r in config['rewrites']}
assert len(redirects)==len(config['redirects']),'duplicate redirect source'
def resolve(u):
 p=urlsplit(u);path=unquote(p.path) or '/';seen=set()
 while path in redirects:
  assert path not in seen,('redirect loop',u);seen.add(path);p=urlsplit(redirects[path]);path=p.path
  if p.netloc:return None,p.fragment
 path=rewrites.get(path,path);f=DIST/('index.html' if path=='/' else path.lstrip('/'))
 return f,p.fragment
seen_titles=set();seen_desc=set();canonicals=set();docs={}
for p in DIST.glob('*.html'):
 d=html.parse(str(p));docs[p.name]=d;t=d.xpath('//title/text()');desc=d.xpath('//meta[@name="description"]/@content');canon=d.xpath('//link[@rel="canonical"]/@href')
 assert len(t)==len(desc)==len(canon)==1,p
 assert t[0] not in seen_titles and desc[0] not in seen_desc,p
 seen_titles.add(t[0]);seen_desc.add(desc[0])
 expected=BASE+(extra[p.name]['path'] if p.name in extra else ('/' if p.name=='index.html' else '/'+p.name))
 assert canon==[expected],p
 graph=json.loads(d.xpath('//script[@type="application/ld+json"]/text()')[0])['@graph'];assert 'Wellesley' not in json.dumps(graph)
 for b in graph:
  if b['@type']=='DaySpa':assert b['address']['addressLocality'] in ['Framingham','Westwood']
 assert d.xpath('//meta[@name="robots"]/@content')==(['noindex, follow'] if p.name in noindex else []),p
 if p.name not in noindex:canonicals.add(expected)
 for u in d.xpath('//a/@href|//img/@src|//script/@src|//link[@rel="stylesheet"]/@href'):
  if urlsplit(u).scheme or u.startswith('//'):continue
  # Relative files are rooted because all published pages are one segment deep.
  f,anchor=resolve(u if not u.startswith('#') else '/'+p.name+u)
  assert f is None or f.is_file(),(p.name,u,'missing target')
  if f and anchor and f.suffix=='.html':
   target=html.parse(str(f));assert target.xpath('//*[@id=$a]',a=anchor),(p.name,u,'missing anchor')
urls=etree.parse(str(DIST/'sitemap.xml')).xpath('//*[local-name()="loc"]/text()');assert set(urls)==canonicals and len(urls)==len(set(urls))
for source,target in redirects.items():
 f,anchor=resolve(source);assert f is None or f.is_file(),(source,target)
 if f and anchor:assert html.parse(str(f)).xpath('//*[@id=$a]',a=anchor),(source,target)
 assert urlsplit(target).path not in redirects,(source,'unnecessary redirect chain')
for row in csv.DictReader((ROOT/'seo/redirect-map-draft.csv').open()):
 f,a=resolve(row['old_path'])
 if row['handling'].startswith('retired'):assert f and not f.exists(),row
 else:assert f is None or f.exists(),row
assert 'Allow: /' in (DIST/'robots.txt').read_text()
import re
pattern=config['headers'][0]['has'][0]['value'].replace('(?<preview>','(')
assert re.fullmatch(pattern,'modern-wellness-website.vercel.app')
assert re.fullmatch(pattern,'modern-wellness-website-example-lucas.vercel.app')
assert not re.fullmatch(pattern,'www.modernwellspa.com')
print(f'PASS: {len(docs)} pages; {len(urls)} sitemap URLs; {len(redirects)} one-hop redirects; {len(rewrites)} retained routes; all internal links, images and anchors; schema and indexability configuration.')
