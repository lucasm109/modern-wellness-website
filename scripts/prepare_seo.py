"""Generate deterministic launch-domain SEO metadata without changing visible content."""
from pathlib import Path
import html,json,re
from xml.etree.ElementTree import Element,SubElement,ElementTree
ROOT=Path(__file__).resolve().parents[1]
BASE='https://www.modernwellspa.com'
PAGES={
'index.html':('Modern Wellness | Wellness Spa in Framingham & Westwood, MA','Find your reset at Modern Wellness in Framingham and Westwood, MA. Explore therapies, Framingham 3-hour day passes, and Westwood private sessions.'),
'framingham.html':('Framingham Wellness Spa, Therapies & Pricing | Modern Wellness','Explore Modern Wellness in Framingham: sauna, cold plunge, salt therapy and more. Compare 3-hour day passes, individual sessions, memberships and pricing.'),
'westwood.html':('Westwood Recovery Room & Private Sessions | Modern Wellness','Explore the Modern Wellness Recovery Room inside PEX in Westwood, MA. Book a private 90-minute visit or learn about access exclusively for PEX clients.'),
'experiences.html':('Wellness Therapies in Framingham & Westwood | Modern Wellness','Explore sauna, cold plunge, compression and other wellness experiences. Find which therapies are available at each Modern Wellness location.'),
'faq.html':('Visit FAQs, Reservations & What to Bring | Modern Wellness','Plan your Modern Wellness visit with answers about booking, walk-ins, day passes, private sessions and what to bring to Framingham or Westwood.'),
'pricing.html':('Framingham & Westwood Spa Pricing | Modern Wellness','Compare ways to visit Modern Wellness, from Framingham 3-hour day passes to Westwood private 90-minute sessions. Find pricing for your location.'),
'newsletter.html':('Modern Moments Newsletter | Modern Wellness','Stay connected with Modern Wellness. Learn how to join Modern Moments for news and updates from our Framingham and Westwood locations.')}
def url(name):return BASE+('/' if name=='index.html' else '/'+name)
def business(key,name,street,city,zip,phone,image,social):
 return {'@type':'DaySpa','@id':BASE+'/#'+key,'name':name,'url':url(key+'.html'),'telephone':phone,'image':BASE+'/'+image,'address':{'@type':'PostalAddress','streetAddress':street,'addressLocality':city,'addressRegion':'MA','postalCode':zip,'addressCountry':'US'},'sameAs':[social],'parentOrganization':{'@id':BASE+'/#organization'}}
locations=[business('framingham','Modern Wellness Longevity Spa','1644 Concord St. (Mill 1)','Framingham','01702','+1-781-400-0594','salt.jpg','https://www.instagram.com/modernwellspa/'),business('westwood','Modern Wellness Recovery Room','32 Everett St.','Westwood','02090','+1-508-988-0692','westwood-09.webp','https://www.instagram.com/modernwellness.westwood/')]
for name,(title,description) in PAGES.items():
 p=ROOT/'dist'/name;s=p.read_text()
 s=re.sub(r'<title>.*?</title>','<title>'+html.escape(title)+'</title>',s, count=1)
 s=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+html.escape(description,quote=True)+'">',s,count=1)
 s=re.sub(r'<!-- SEO START -->.*?<!-- SEO END -->','',s,flags=re.S)
 graph=[{'@type':'Organization','@id':BASE+'/#organization','name':'Modern Wellness','url':BASE+'/','logo':BASE+'/wordmark.svg'},{'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'Modern Wellness'},{'@type':'WebPage','@id':url(name)+'#webpage','url':url(name),'name':title,'description':description,'isPartOf':{'@id':BASE+'/#website'}}]
 if name=='index.html':graph+=locations
 elif name in ('framingham.html','westwood.html'):graph += [b for b in locations if b['url']==url(name)]
 tags='<!-- SEO START --><link rel="canonical" href="'+url(name)+'">'
 if name=='newsletter.html':tags+='<meta name="robots" content="noindex, follow">'
 for prop,value in [('og:type','website'),('og:site_name','Modern Wellness'),('og:title',title),('og:description',description),('og:url',url(name)),('og:image',BASE+'/salt.jpg')]:tags+='<meta property="'+prop+'" content="'+html.escape(value,quote=True)+'">'
 tags+='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},separators=(',',':'))+'</script><!-- SEO END -->'
 s=s.replace('</head>',tags+'</head>');p.write_text(s)
root=Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for name in PAGES:
 if name!='newsletter.html':SubElement(SubElement(root,'url'),'loc').text=url(name)
ElementTree(root).write(ROOT/'dist/sitemap.xml',encoding='utf-8',xml_declaration=True)
(ROOT/'dist/robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
