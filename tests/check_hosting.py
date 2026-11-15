"""Exercise actual Hosting responses from the Firebase emulator or a deployed site."""

import sys
import unittest
from html import unescape
from urllib.error import HTTPError
from urllib.request import urlopen
from xml.etree import ElementTree

from check_site import ORIGIN, SITE, Page


BASE_URL = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8768").rstrip("/")


class HostingChecks(unittest.TestCase):
    def test_indexable_pages_and_headers(self):
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        sitemap = ElementTree.parse(SITE / "sitemap.xml")
        for node in sitemap.findall("s:url/s:loc", namespace):
            path = node.text.removeprefix(ORIGIN)
            with self.subTest(path=path), urlopen(BASE_URL + path, timeout=10) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers.get_content_type(), "text/html")
                self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
                self.assertEqual(
                    response.headers.get("Referrer-Policy"),
                    "strict-origin-when-cross-origin",
                )
                self.assertIn("frame-ancestors 'none'", response.headers["Content-Security-Policy"])
                self.assertIn("geolocation=()", response.headers["Permissions-Policy"])
                local = SITE / path.lstrip("/") / "index.html"
                self.assertIn(Page(local).title, unescape(response.read().decode("utf-8")))

    def test_trailing_slashes_match_canonical_urls(self):
        for path in ("/support", "/privacy", "/apps/tap-and-count"):
            with self.subTest(path=path), urlopen(BASE_URL + path, timeout=10) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.url, BASE_URL + path + "/")

    def test_unknown_and_configuration_paths_return_custom_404(self):
        for path in (
            "/this-page-does-not-exist",
            "/_headers",
            "/_redirects",
            "/firebase.json",
            "/.git/config",
            "/tests/check_site.py",
        ):
            with self.subTest(path=path):
                with self.assertRaises(HTTPError) as caught:
                    urlopen(BASE_URL + path, timeout=10)
                error = caught.exception
                try:
                    self.assertEqual(error.code, 404)
                    body = error.read().decode("utf-8")
                    self.assertIn("This one flew", body)
                    self.assertIn('name="robots" content="noindex"', body)
                finally:
                    error.close()

    def test_static_assets_and_sitemap(self):
        for path, mime in (
            ("/assets/styles.css", "text/css"),
            ("/assets/favicon.svg", "image/svg+xml"),
            ("/assets/app-count.webp", "image/webp"),
            ("/assets/social.png", "image/png"),
            ("/assets/tap-count-social.png", "image/png"),
            ("/sitemap.xml", "application/xml"),
            ("/robots.txt", "text/plain"),
        ):
            with self.subTest(path=path), urlopen(BASE_URL + path, timeout=10) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers.get_content_type(), mime)
                self.assertTrue(response.read())


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]], verbosity=2)
