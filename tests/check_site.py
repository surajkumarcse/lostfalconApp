"""Check the actual publish directory without installing dependencies."""

import json
import struct
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


SITE = Path(__file__).resolve().parents[1] / "site"
ORIGIN = "https://lostfalcon.app"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.links = []
        self.metadata = {}
        self.canonical = []
        self.json_ld = []
        self.h1_count = 0
        self.title = ""
        self.in_title = False
        self.in_json = False
        self.json_text = ""
        self.has_main = False
        self.lang = None
        self.issues = []
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "main":
            self.has_main = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            self.metadata[key] = attrs.get("content", "")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))
        for attribute in ("href", "src"):
            if attribute in attrs:
                self.links.append(attrs[attribute])
        if tag == "img":
            if not all(key in attrs for key in ("alt", "width", "height")):
                self.issues.append("Image missing alt text or dimensions")
        if tag == "script":
            if attrs.get("type") != "application/ld+json":
                self.issues.append("Unexpected executable or tracking script")
            else:
                self.in_json = True
                self.json_text = ""

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.in_json:
            self.json_ld.append(json.loads(self.json_text))
            self.in_json = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_json:
            self.json_text += data


def resolve_url(url):
    relative = unquote(urlsplit(url).path).lstrip("/")
    path = SITE / relative
    if path.is_dir():
        path /= "index.html"
    return path


class SiteChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {path: Page(path) for path in SITE.rglob("*.html")}

    def test_page_metadata_and_accessibility_basics(self):
        titles = []
        descriptions = []
        for path, page in self.pages.items():
            with self.subTest(page=path.relative_to(SITE)):
                self.assertEqual(page.lang, "en")
                self.assertEqual(page.h1_count, 1)
                self.assertTrue(page.has_main)
                self.assertIn("main", page.ids)
                self.assertEqual(len(page.ids), len(set(page.ids)))
                self.assertTrue(page.title.strip())
                self.assertTrue(page.metadata.get("description"))
                self.assertIn("width=device-width", page.metadata.get("viewport", ""))
                self.assertFalse(page.issues, page.issues)
                titles.append(page.title)
                descriptions.append(page.metadata["description"])
                if path.name == "404.html":
                    self.assertEqual(page.metadata.get("robots"), "noindex")
                    self.assertFalse(page.canonical)
                else:
                    expected_path = "/" + path.relative_to(SITE).as_posix().removesuffix("index.html")
                    self.assertEqual(page.canonical, [ORIGIN + expected_path])
                    self.assertEqual(page.metadata.get("og:url"), page.canonical[0])
                    self.assertEqual(page.metadata.get("twitter:card"), "summary_large_image")
                    self.assertTrue(page.metadata.get("og:image:alt"))
                    self.assertTrue(page.json_ld)
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_internal_links_assets_and_fragments(self):
        for path, page in self.pages.items():
            urls = page.links + [
                page.metadata[key]
                for key in ("og:image", "twitter:image")
                if key in page.metadata
            ]
            for url in urls:
                parts = urlsplit(url)
                if parts.scheme == "mailto" or parts.netloc not in ("", "lostfalcon.app"):
                    continue
                with self.subTest(page=path.relative_to(SITE), url=url):
                    target = path if not parts.path else resolve_url(url)
                    self.assertTrue(target.is_file(), f"Missing local target: {target}")
                    if parts.fragment:
                        self.assertIn(target, self.pages)
                        self.assertIn(unquote(parts.fragment), self.pages[target].ids)

    def test_sitemap_covers_exactly_the_indexable_pages(self):
        root = ElementTree.parse(SITE / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [node.text for node in root.findall("s:url/s:loc", namespace)]
        expected = [
            page.canonical[0] for page in self.pages.values() if page.canonical
        ]
        self.assertEqual(sorted(urls), sorted(expected))
        self.assertEqual(len(urls), len(set(urls)))
        robots = (SITE / "robots.txt").read_text()
        self.assertIn("Sitemap: " + ORIGIN + "/sitemap.xml", robots)
        self.assertNotIn("Disallow: /", robots)

    def test_structured_data_references_real_content(self):
        for page in self.pages.values():
            for data in page.json_ld:
                self.assertEqual(data["@context"], "https://schema.org")
                for entity in data.get("@graph", [data]):
                    self.assertNotIn("aggregateRating", entity)
                    self.assertNotIn("review", entity)
                    if entity["@type"] == "MobileApplication":
                        self.assertIn("Tap & Count", page.title)
                        self.assertIn(entity["downloadUrl"], page.links)
                        self.assertTrue(resolve_url(entity["screenshot"]).is_file())

    def test_social_image_is_a_shareable_png(self):
        image = (SITE / "assets/social.png").read_bytes()
        self.assertEqual(image[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", image[16:24]), (1200, 630))


if __name__ == "__main__":
    unittest.main(verbosity=2)
