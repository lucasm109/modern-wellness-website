"""Retain useful Wix service URLs using the site's approved experience copy."""
from pathlib import Path
from lxml import html,etree
import copy,json
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist'
SPECS=[('infrared-sauna','Infrared sauna','both'),('cold-plunge','Cold plunge','both'),('compression-therapy','Normatec compression','both'),('guided-meditation','BrainTap meditation','framingham'),('salt-chamber','Salt chamber','framingham'),('steam-room','Eucalyptus steam room','framingham'),('hot-tub','Warm-water hydrotherapy','framingham'),('biocharger','BioCharger','framingham'),('pemf-therapy','PEMF therapy','premium'),('flowpresso','Flowpresso','premium'),('red-light-therapy','Red light therapy','westwood')]
# Keep retained overview/event pages discoverable through useful internal links.
for filename in ['index.html','experiences.html','framingham.html','westwood.html','faq.html','pricing.html','newsletter.html']:
 p=DIST/filename;d=html.parse(str(p))
 faq=d.xpath('//footer//a[@href="faq.html"]')
 if faq and not d.xpath('//footer//a[@href="/about"]'):
  para=etree.Element('p');etree.SubElement(para,'a',href='/about').text='About Modern Wellness';faq[0].getparent().addprevious(para)
 if filename=='faq.html':
  answer=d.xpath('//details[summary[contains(.,"private event")]]//div[contains(@class,"faq-answer")]')
  if answer and not answer[0].xpath('.//a[@href="/private-events"]'):
   para=etree.SubElement(answer[0],'p');etree.SubElement(para,'a',href='/private-events').text='Explore Framingham private events →'
 p.write_text('<!doctype html>'+html.tostring(d.getroot(),encoding='unicode',method='html'))
base=html.parse(str(DIST/'experiences.html'))
header=html.tostring(base.xpath('//header')[0],encoding='unicode')
footer=html.tostring(base.xpath('//footer')[0],encoding='unicode')
# Keep the same quick booking access and scripts used by the main site.
booking=''.join(html.tostring(e,encoding='unicode') for e in base.xpath('//body/*[not(self::header or self::main or self::footer or self::script)]'))
scripts=''.join(html.tostring(e,encoding='unicode') for e in base.xpath('//body/script'))
note=html.tostring(base.xpath('//p[contains(@class,"therapy-note")]')[0],encoding='unicode')
meta={}
def esc(s):return __import__('html').escape(s,quote=True)
def page(slug,title,description,body):
 meta[slug+'.html']={'path':'/'+slug,'title':title,'description':description}
 (DIST/(slug+'.html')).write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><meta name="description" content="'+esc(description)+'"><link rel="stylesheet" href="/style.css"></head><body>'+header+booking+'<main>'+body+'</main>'+footer+scripts+'</body></html>')
for slug,title,kind in SPECS:
 card=base.xpath('//article[contains(@class,"service-card")][h3[normalize-space(.)=$t]]',t=title)[0]
 intro=card.xpath('./p[1]')[0].text_content()
 image=card.xpath('./img')[0]
 detail=card.xpath('./details')[0]
 paragraphs=''.join(html.tostring(p,encoding='unicode') for p in detail.xpath('./p'))
 duration=''.join(html.tostring(p,encoding='unicode') for p in card.xpath('./p[contains(@class,"service-duration")]'))
 loc='Framingham & Westwood' if kind=='both' else ('Westwood' if kind=='westwood' else 'Framingham')
 body='<section class="hero"><div><a class="breadcrumb" href="/experiences.html">← All experiences</a><div class="eyebrow">'+loc+'</div><h1>'+esc(title)+'</h1><p>'+esc(intro)+'</p>'+duration+'</div>'+html.tostring(image,encoding='unicode')+'</section>'
 body+='<section class="services"><h2>A little time for yourself.</h2>'+paragraphs+'</section><section><h2>Plan your visit.</h2>'
 if kind in ('both','framingham','premium'):
  body+='<h3>Framingham Longevity Spa</h3><p>'+('This is a dedicated premium appointment, booked separately from the 3-hour day pass.' if kind=='premium' else 'Explore this experience as part of your Framingham visit. The day pass gives you up to 3 hours; suggested portions of a day-pass visit differ from individually booked appointment lengths.')+'</p><p>Reservations are highly encouraged. Walk-ins are accommodated subject to availability.</p><a href="/framingham.html#pricing">Framingham pricing and ways to visit →</a>'
 if kind in ('both','westwood'):
  body+='<h3>Westwood Recovery Room</h3><p>Inside PEX, choose a private 90-minute session by reservation on Friday evenings and weekends, subject to availability. Bring a group of up to four people, with an additional charge for each guest. Shared flex-hour access is exclusively for PEX clients.</p><a href="/westwood.html#private-pricing">Westwood pricing and ways to visit →</a>'
 body+='</section><section class="services">'+note+'</section>'
 page(slug,title+' in '+loc+', MA | Modern Wellness',intro+' Explore '+title.lower()+' at Modern Wellness in '+loc+', MA, with location details and ways to visit.',body)
# Private events retain their established URL and stay distinct from ordinary Westwood bookings.
page('private-events','Private Spa Events in Framingham | Modern Wellness','Plan a private event at Modern Wellness in Framingham. Email our team to discuss your group, preferred date and the experiences you would like to enjoy.','<section><a class="breadcrumb" href="/framingham.html">← Framingham Longevity Spa</a><div class="eyebrow">Gather in Framingham</div><h1>A little space to come together.</h1><p>Our Framingham Longevity Spa can be booked for private events. Bring people together for time to unwind and enjoy the space.</p><h2>Let’s plan your event.</h2><p>Email us with your preferred date, group size, and what you have in mind. Our team will help you plan the details and confirm availability and pricing.</p><p class="contact-email">hello@modernwellspa.com</p><a href="/framingham.html#services">Explore Framingham experiences →</a><h2>Looking for a small private visit in Westwood?</h2><p>The Westwood Recovery Room offers private 90-minute reservations for up to four people. This is a separate way to visit, with its own pricing and availability.</p><a href="/westwood.html#private-pricing">Explore Westwood private sessions →</a></section>')
page('about','About Modern Wellness | Framingham & Westwood, MA','Get to know Modern Wellness: a Longevity Spa in Framingham and a Recovery Room inside PEX in Westwood, with different ways to make time for yourself.','<section><div class="eyebrow">Modern Wellness</div><h1>Two spaces. Your kind of reset.</h1><p>Modern Wellness brings together warmth, water, stillness, and restorative experiences in Framingham and Westwood, Massachusetts.</p><h2>Framingham Longevity Spa</h2><p>Come for an individual service, enjoy our day pass for up to 3 hours, or make wellness part of your routine. Our team will help guide your visit.</p><a href="/framingham.html">Explore Framingham →</a><h2>Westwood Recovery Room</h2><p>Inside PEX, enjoy a private 90-minute reservation on Friday evenings and weekends, subject to availability. PEX clients also have exclusive shared access during flex hours.</p><a href="/westwood.html">Explore Westwood →</a></section>')
# Link service pages from existing cards without adding a second top-level menu.
lookup={title:slug for slug,title,_ in SPECS}
for filename in ['experiences.html','framingham.html','westwood.html']:
 p=DIST/filename;doc=html.parse(str(p))
 for card in doc.xpath('//article[contains(@class,"service-card")]'):
  heading=card.find('h3')
  if heading is None:continue
  title=heading.text_content();slug=lookup.get(title)
  if not slug:continue
  if not heading.xpath('./a'):
   heading.text=None;a=etree.SubElement(heading,'a',href='/'+slug);a.text=title
 (p).write_text('<!doctype html>'+html.tostring(doc.getroot(),encoding='unicode',method='html'))
# A helpful genuine 404, not a homepage rewrite that masks missing URLs.
page('404','Page Not Found | Modern Wellness','This page is unavailable. Find Modern Wellness locations, experiences, pricing and booking information.','<section><div class="eyebrow">Page not found</div><h1>Let’s find your way.</h1><p>This address is no longer available. Explore our locations or visit our frequently asked questions to plan your visit.</p><div class="actions"><a class="button" href="/">Explore Modern Wellness</a><a class="button light" href="/faq.html">Visit FAQs</a></div></section>')
(DIST.parent/'seo/generated-pages.json').write_text(json.dumps(meta,indent=2)+'\n')
print('Generated',len(meta),'pages; linked existing service cards.')
