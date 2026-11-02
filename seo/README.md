# SEO migration preparation

Draft branch only. Wix remains live. Do not change DNS or merge for cutover until deployment checks pass.

## Implemented

- Unique metadata, final www.modernwellspa.com canonical URLs, Organization/WebSite/WebPage schema and accurate DaySpa schema for Framingham and Westwood.
- Retain 10 established therapy addresses plus /private-events and /about. Add /red-light-therapy for Westwood. Reuse approved experience text, photography and mobile styles; link service titles from experience/location cards. Private events remain distinct from ordinary Westwood private sessions.
- 19 canonical sitemap entries, crawlable robots.txt, newsletter/legal PDF/404 noindex, and genuine missing-page handling.
- 53 permanent redirects covering historical redirects, old pricing/utility paths, prototype HTML paths and canonical HTML aliases. 13 rewrites retain useful extensionless page addresses. The CSV records 26 audited Wix page records and 17 historical redirects.
- /cart-page and /thank-you-page are retired utilities, intentionally left as genuine 404s. /blank and /copy-of-home duplicate home records redirect home. /premium-therapies maps to the Framingham service section.
- Staging and this project's generated Vercel preview hostnames get X-Robots-Tag noindex, follow. The final custom domain does not match the host rule. Preserve DNS verification TXT records.

## Build and verify

python scripts/build_service_pages.py
python scripts/prepare_seo.py
python scripts/check_seo.py

Build uses lxml and the Python standard library. Regeneration is idempotent. New service content is sourced from the existing experiences page, so update that approved copy before rebuilding. Metadata is regenerated from script definitions and seo/generated-pages.json. No raw Search Console exports or private reporting is committed.

Checks cover unique titles/descriptions/canonicals, valid JSON-LD, sitemap coverage and targets, all internal links/assets/anchors, redirect destination existence and loops/chains, retained paths, retired utility handling, and staging versus custom-domain host matching.

## Evidence and limits

Available Search Console performance covers only three days. It confirms search visibility for existing service, pricing, FAQ and event pages but cannot establish long-term value or trends. Retaining useful existing URLs is a cautious preservation choice. Absence of clicks in this small sample is not a reason to delete a page. Agency change history and backlink data remain unavailable. No ranking improvements are guaranteed.

Browser QA: retained service page at desktop width; all 21 pages checked for horizontal overflow in 360px frames, with no overflow found; representative service/event pages visually inspected at 360px/390px; mobile menu, pricing choices and Escape tested. This is responsive browser testing, not a physical iPhone/Safari test.

## Required before DNS cutover

1. Verify the draft deployment actually serves all retained paths with 200; historical paths redirect permanently to the correct final page; retired utilities and random missing URLs return 404. Confirm query-string retention and trailing-slash normalization.
2. Verify real HTTP noindex headers on staging/preview and indexable responses on the final custom domain. Do not submit the replacement sitemap while Wix is serving the domain.
3. Validate public structured data with Google's Rich Results Test after the draft is reachable; no rich-result eligibility or rankings are guaranteed by markup.
4. Identify any existing Analytics/Tag Manager setup and preserve business-owned verification/integration methods. Search Console connection alone does not measure bookings.
5. Final business review of service availability, pricing, contact details, hours, booking and gift-card destinations; authenticated booking prices cannot be verified without an account.
6. Mobile Drive video playback remains a known limitation. Compressed source MP4s or a supported video hosting source are still needed for dependable native playback.
7. Retain rollback instructions and original Wix DNS values; change only web DNS records and preserve email DNS. Confirm HTTPS, www/apex redirects and indexing on the real hostname immediately after switching.
8. Submit the final sitemap in Search Console and monitor indexing, old/new URLs, errors and performance after launch. Keep permanent redirects in place long term.

Vercel team access currently requires reauthorization before deployment verification. Local checks are not a substitute for deployed HTTP tests. Nothing in this branch changes Wix, DNS, Google ownership or agency access.
