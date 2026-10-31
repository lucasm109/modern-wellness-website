# SEO launch preparation

This phase changes head metadata and crawler configuration, not visible page content. Wix remains live and DNS must remain unchanged until migration review is complete.

Implemented: unique metadata on seven pages, final www.modernwellspa.com canonical URLs, Organization/WebSite/WebPage schema, two DaySpa locations from visible footer addresses and phones, six canonical sitemap entries, crawlable robots.txt, newsletter/legal PDF noindex, duplicate homepage redirect.

The exact staging hostname modern-wellness-website.vercel.app receives an HTTP X-Robots-Tag noindex header. Final custom domains do not match that rule. Vercel preview deployment indexing protection and actual response headers still need deployment verification. Do not add a global noindex rule or block crawling in robots.txt. Do not submit this partial sitemap while Wix is still live.

Run python scripts/prepare_seo.py and python scripts/check_seo.py. Generation is idempotent. The scripts use Python standard libraries; validation also uses lxml.

redirect-map-draft.csv inventories 26 Wix static-page records and 17 historic redirects. This is a proposal, not active configuration. Blank destinations await Search Console evidence and content review. Therapy-page consolidation and archived/utility routes remain unresolved. Existing prototype redirects are preserved. Do not cut over with unresolved important old URLs.

Before launch:
- Obtain available historical Search Console Pages/Queries exports and verify which property has history.
- Decide which dedicated therapy/private-events pages to retain; implement direct permanent redirects for remaining old and historic URLs.
- Compare final page inventory with sitemap and redirect map; test query strings, trailing slashes, fragments and actual deployed final statuses.
- Preserve business-owned DNS verification TXT records, and identify any Analytics/Tag Manager configuration before replacing it.
- Verify address/hours accuracy and structured data with Google's Rich Results Test. PEX flex hours are not advertised as public opening hours in schema.
- Check actual staging noindex and custom-domain indexability, canonical URLs, HTTPS, mobile navigation and booking links.
- Switch DNS only after checks pass, preserving email DNS. Then submit final sitemap in Search Console and monitor indexing/errors/performance.

No traffic or ranking improvements are guaranteed; Search Console evidence is still pending. No agency access, Google integration, Wix settings, or domain DNS is modified by these files.
