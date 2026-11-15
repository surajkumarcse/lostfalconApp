# Lost Falcon

The static website for **lostfalcon.app**, featuring the Tap & Count Android app.
Plain HTML and CSS, with no build step, third-party fonts, analytics, or runtime
dependencies. Only the `site/` directory is published.

## Preview and validate

```sh
python3 tests/check_site.py
python3 -m http.server 8080 --directory site --bind 127.0.0.1
```

Open `http://localhost:8080`. The checks run locally without dependencies.
No GitHub Actions workflow is installed; publishing is handled by Cloudflare
once Git integration is connected.

## Deploy on Cloudflare Pages

1. In Cloudflare, open **Workers & Pages > Create application > Pages > Connect to Git**.
2. Connect GitHub, granting access only to `surajkumarcse/lostfalconApp`.
3. Select this repository and use these settings:

   | Setting | Value |
   | --- | --- |
   | Production branch | `main` |
   | Framework preset | None |
   | Build command | Leave empty |
   | Build output directory | `site` |
   | Root directory | Leave at the repository root |

4. Deploy and check the generated `pages.dev` address.
5. Add `lostfalcon.app` as a Cloudflare zone on the Free plan. Copy existing DNS
   records, especially email MX and TXT records, before changing nameservers.
6. In Namecheap, open **Domain List > Manage > Nameservers > Custom DNS** and enter
   the two nameservers assigned to this zone by Cloudflare. The domain stays
   registered and renewed at Namecheap. If DNSSEC is enabled at Namecheap, disable
   it before the nameserver switch; re-enable it using Cloudflare's values after
   the zone is active.
7. In the Pages project's **Custom domains**, add both `lostfalcon.app` and
   `www.lostfalcon.app`. Wait until both domains and their HTTPS certificates are
   active. The included `_redirects` sends `www` visitors to the main domain,
   preserving the path.
8. Configure Cloudflare's production `pages.dev` address to redirect to the custom
   domain using Bulk Redirects. Enable **Always Use HTTPS** for the zone.

Future pushes to `main` deploy automatically once Git integration is connected.
Alternatively, drag the contents of `site/` into a Pages Direct Upload project.
Cloudflare requires a new project to switch between Direct Upload and Git integration.

Static asset requests are free on Cloudflare Pages. No Pages Functions or paid
services are required. Domain renewal remains a separate Namecheap cost.

## Search launch checklist

- Verify a Domain property for `lostfalcon.app` in Google Search Console using
  the TXT record it provides. Add that record in Cloudflare after the DNS switch.
- Submit `https://lostfalcon.app/sitemap.xml`, then inspect the homepage, support,
  and privacy URLs. Request indexing after the production domain works.
- Validate the app JSON-LD with Schema.org Validator. Google app rich results
  additionally require eligible, genuine rating/review and offer information.
  These are deliberately omitted rather than fabricated.
- Run PageSpeed Insights and check mobile layout, links, HTTPS, and a nonexistent
  URL. The custom `404.html` prevents Pages from treating this site as an SPA.
- Add the website and privacy policy URLs to the app's Google Play listing.
- Use Search Console queries to guide future original counting tutorials.
- The site contains canonical URLs, page descriptions, Open Graph/social cards,
  a favicon, app/publisher structured data, an XML sitemap, and a robots file.
  None of these guarantees indexing, rankings, or rich results.
- Do not add keyword stuffing, purchased backlinks, fake reviews, or FAQ markup
  expecting Google FAQ rich results; Google discontinued those results in May 2026.

## Content maintenance

Update `site/index.html`, `site/support/index.html`, and `site/privacy/index.html`
directly. Update sitemap `lastmod` dates only when the corresponding page changes
meaningfully. Keep metadata, structured data, and visible text consistent.

The screenshots come from the app owner's Google Play listing and are served
locally; visitors do not request images from Google. Sound and vibration are
described without claiming in-app customization, which the reviewed code does
not implement. Cloud sync, widgets, and voice commands are not advertised.

The privacy page distinguishes locally stored count history, Android-managed
backup, support email, and hosting request processing. Keep it aligned with
released app behavior and Google Play Data safety disclosures. Review the policy
whenever SDKs, permissions, backup behavior, or hosting services change.

## Official references

- [Cloudflare Pages Git integration](https://developers.cloudflare.com/pages/get-started/git-integration/)
- [Cloudflare Pages custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/)
- [Cloudflare Pages pricing](https://developers.cloudflare.com/pages/functions/pricing/)
- [Namecheap nameserver instructions](https://www.namecheap.com/support/knowledgebase/article.aspx/767/10/how-to-change-dns-for-a-domain/)
- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google software app structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app)
- [Android Auto Backup](https://developer.android.com/identity/data/autobackup)
- [Tap & Count on Google Play](https://play.google.com/store/apps/details?id=com.lostfalcon.tapcount)
