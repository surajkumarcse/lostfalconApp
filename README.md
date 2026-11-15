# Lost Falcon

The static developer portfolio for **lostfalcon.app**, showcasing the Android
apps published under the **LostFalcon** Google Play developer account.
Plain HTML and CSS, with no build step, third-party fonts, analytics, or runtime
dependencies. Only the `site/` directory is published.

## Preview and validate

```sh
python3 tests/check_site.py
python3 -m http.server 8080 --directory site --bind 127.0.0.1
```

Open `http://localhost:8080`. The content checks run locally without dependencies.
This basic preview does not apply hosting headers or redirects. To check actual
Firebase Hosting behavior, install the Firebase CLI and run:

```sh
firebase emulators:exec --only hosting --project demo-lostfalcon \
  "python3 tests/check_hosting.py http://127.0.0.1:8768"
```

The `demo-` project is local-only and does not deploy or bill cloud resources.
The Hosting emulator binds only to localhost. No GitHub Actions workflow is installed.

## Deploy on Firebase Hosting

Use **Firebase Hosting (classic)**, not Firebase App Hosting. No Firebase SDK,
database, Cloud Functions, billing account, or build step is needed for this site.

1. Create or choose a Firebase project in the Firebase console. For no-cost hosting,
   use a project on the **Spark** plan without linking a billing account. Confirm
   that its default Hosting site does not already serve another website.
2. Install the Firebase CLI if it is missing: `npm install -g firebase-tools`.
3. Run `firebase login` locally and sign in to the account that owns the project.
4. From this repository's root, run:

   ```sh
   python3 tests/check_site.py
   firebase deploy --only hosting --project YOUR_PROJECT_ID
   ```

   Replace `YOUR_PROJECT_ID` with the exact project ID from the console. The explicit
   project argument prevents accidentally deploying to an unrelated default project.
   Do not run `firebase init hosting`: this repository already has `firebase.json`,
   and initialization could overwrite the prepared configuration or HTML.
5. Test the generated `YOUR_PROJECT_ID.web.app` site, including app details, support,
   privacy, images, and a nonexistent path that should return the custom 404.

`firebase.json` publishes only `site/`, sets the security headers, keeps canonical
trailing-slash URLs, and does not rewrite unknown paths to the homepage. Old
Cloudflare `_headers` and `_redirects` files have been removed and are explicitly
excluded if reintroduced. Firebase handles hostname redirects through its custom
domain settings, not a host-specific rule in this path-based configuration.

Pushes to GitHub do **not** automatically deploy. Run the deploy command after
pulling future changes; GitHub automation can be configured separately later.

The Spark plan currently includes 10 GB of Hosting storage and 10 GB/month data
transfer. Exceeding the no-cost transfer quota can disable the website until the
next month; upgrading to Blaze enables paid overage. Domain renewal remains
a separate Namecheap cost.

## Connect lostfalcon.app

1. In **Firebase Console > Hosting**, choose **Add custom domain** and enter
   `lostfalcon.app`. Follow the wizard's verification and DNS instructions.
2. If the domain uses Namecheap BasicDNS, open **Domain List > Manage > Advanced DNS**
   in Namecheap. Add the TXT verification record using host `@`, if requested, and
   the A or other records with the exact values Firebase supplies.
3. Keep the verification TXT record for continued ownership verification and
   certificate renewal. Remove only conflicting website records for the hostname
   being connected; preserve email MX, SPF, DKIM, and other unrelated records.
4. Keep Namecheap as the registrar and DNS provider; no nameserver switch is needed.
   If you already changed nameservers to another provider, manage the records at
   that authoritative DNS provider instead of Namecheap's inactive DNS editor.
5. Add `www.lostfalcon.app` using Firebase's option to redirect it to `lostfalcon.app`.
   Follow the records supplied for `www` as well.
6. Wait for the domain to show **Connected** and HTTPS to become active. Certificate
   provisioning can take up to 24 hours. Test both hostnames and page paths.

## Search launch checklist

- Verify a Domain property for `lostfalcon.app` in Google Search Console using
  the TXT record it provides. Add that record at your authoritative DNS provider.
- Submit `https://lostfalcon.app/sitemap.xml`, then inspect the homepage, app
  detail, support, and privacy URLs. Request indexing after the production domain works.
- Validate the app JSON-LD with Schema.org Validator. Google app rich results
  additionally require eligible, genuine rating/review and offer information.
  These are deliberately omitted rather than fabricated.
- Run PageSpeed Insights and check mobile layout, links, HTTPS, and a nonexistent
  URL. The custom `404.html` serves a real error page; no SPA fallback is configured.
- Add the website and privacy policy URLs to the app's Google Play listing.
- Use Search Console queries to guide future original counting tutorials.
- The site contains canonical URLs, page descriptions, Open Graph/social cards,
  a favicon, app/publisher structured data, an XML sitemap, and a robots file.
  None of these guarantees indexing, rankings, or rich results.
- Do not add keyword stuffing, purchased backlinks, fake reviews, or FAQ markup
  expecting Google FAQ rich results; Google discontinued those results in May 2026.

## Content maintenance

The homepage is a developer overview and app directory; app-specific marketing
and features live at `site/apps/tap-and-count/index.html`. Support and privacy
remain at their existing URLs. Update these HTML files directly.

The public LostFalcon developer listing was checked on November 15, 2026 in both
US and India storefronts; it showed only **Tap & Count - Count things**. The directory
does not invent additional apps or promise unreleased products. It links to the
developer profile for the latest catalogue.

For a new published app, add an app card to the homepage and a detail page under
`site/apps/`. Update the homepage `CollectionPage` / `ItemList` JSON-LD and sitemap,
and link the correct app support and privacy information. Run the content checks.
This is a manually maintained static directory, not a live Google Play scraper.

Update sitemap `lastmod` dates only when the corresponding page changes
meaningfully. Keep metadata, structured data, and visible text consistent. The
developer homepage and Tap & Count have separate social-preview PNGs; regenerate
them from the corresponding SVG if the preview wording changes.

The screenshots come from the app owner's Google Play listing and are served
locally; visitors do not request images from Google. Sound and vibration are
described without claiming in-app customization, which the reviewed code does
not implement. Cloud sync, widgets, and voice commands are not advertised.

The privacy page distinguishes locally stored count history, Android-managed
backup, support email, and hosting request processing. Keep it aligned with
released app behavior and Google Play Data safety disclosures. Review the policy
whenever SDKs, permissions, backup behavior, or hosting services change.

## Official references

- [Firebase Hosting quickstart](https://firebase.google.com/docs/hosting/quickstart)
- [Firebase Hosting configuration](https://firebase.google.com/docs/hosting/full-config)
- [Firebase custom domains](https://firebase.google.com/docs/hosting/custom-domain)
- [Firebase Hosting quotas and pricing](https://firebase.google.com/docs/hosting/usage-quotas-pricing)
- [Firebase privacy and security](https://firebase.google.com/support/privacy)
- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google software app structured data](https://developers.google.com/search/docs/appearance/structured-data/software-app)
- [Android Auto Backup](https://developer.android.com/identity/data/autobackup)
- [Tap & Count on Google Play](https://play.google.com/store/apps/details?id=com.lostfalcon.tapcount)
- [LostFalcon developer profile](https://play.google.com/store/apps/developer?id=LostFalcon)
