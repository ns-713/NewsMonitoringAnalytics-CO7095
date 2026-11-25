"""
RSS Collection and Normalisation Service
Downloads, parses, and normalises XML RSS feeds into standard NewsArticle models.
Responsibility: Nikitha Sarpur (ns713) - US03, US13, US14, US15, US26

Features:
- Standard library XML parsing (xml.etree.ElementTree)
- Timeout, HTTP error, URLError, and malformed XML fault isolation
- Missing tag fallbacks
- Offline / Demo fallback ingestion
"""

import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from email.utils import parsedate_to_datetime
from config.settings import DEFAULT_RSS_TIMEOUT_SECONDS, USER_AGENT, DEMO_DATASET_FILE
from models.article import NewsArticle
from storage.json_storage import JsonStorage


class RssService:
    """
    Parses RSS feeds, isolates ingestion errors, and normalises items to NewsArticle instances.
    """

    def __init__(self, timeout: int = DEFAULT_RSS_TIMEOUT_SECONDS):
        self.timeout = timeout

    def fetch_feed_xml(self, feed_url: str) -> Tuple[bool, str, str]:
        """
        Retrieves raw XML string from feed_url.
        Returns:
            Tuple[bool, str, str]: (success, xml_content_or_empty, error_message)
        """
        if not feed_url or not isinstance(feed_url, str):
            return False, "", "Invalid feed URL supplied."

        feed_url = feed_url.strip()

        # Handle local file feeds cross-platform (Windows, Linux, macOS)
        if feed_url.startswith("file://"):
            raw_path = feed_url[7:]
            if len(raw_path) >= 3 and raw_path[0] == '/' and raw_path[2] == ':':
                local_path = raw_path[1:]
            else:
                local_path = raw_path
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    return True, f.read(), ""
            except Exception as e:
                return False, "", f"Failed to read local file feed: {str(e)}"

        # HTTP/HTTPS requests
        headers = {"User-Agent": USER_AGENT}
        req = urllib.request.Request(feed_url, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                xml_data = response.read().decode(charset, errors="replace")
                return True, xml_data, ""
        except urllib.error.HTTPError as he:
            return False, "", f"HTTP Error {he.code}: {he.reason}"
        except urllib.error.URLError as ue:
            return False, "", f"Network/URL Error: {ue.reason}"
        except TimeoutError:
            return False, "", f"Feed request timed out after {self.timeout}s."
        except Exception as ex:
            return False, "", f"Unexpected network error: {str(ex)}"

    def parse_pub_date(self, raw_date: Optional[str]) -> str:
        """
        Normalises RFC 822 / RSS dates to ISO YYYY-MM-DD.
        """
        if not raw_date:
            return datetime.now().strftime("%Y-%m-%d")

        try:
            dt = parsedate_to_datetime(raw_date.strip())
            return dt.strftime("%Y-%m-%d")
        except Exception:
            # Fallback to current date or simple prefix
            clean = raw_date.strip()
            if len(clean) >= 10 and clean[:4].isdigit() and clean[4] == '-':
                return clean[:10]
            return datetime.now().strftime("%Y-%m-%d")

    def clean_html(self, text: str) -> str:
        """Strips basic HTML markup from description fields."""
        if not text:
            return ""
        import re
        clean = re.sub(r"<[^>]+>", " ", text)
        clean = " ".join(clean.split()).strip()
        clean = re.sub(r"\s+([.,!?;:])", r"\1", clean)
        return clean

    def parse_rss_xml(self, xml_content: str, default_source_name: str = "RSS Source") -> Tuple[bool, List[NewsArticle], str]:
        """
        Parses XML string into a list of NewsArticle objects.
        Returns:
            Tuple[bool, List[NewsArticle], str]: (success, articles, error_message)
        """
        if not xml_content or not xml_content.strip():
            return False, [], "XML payload is empty."

        try:
            root = ET.fromstring(xml_content.strip())
        except ET.ParseError as pe:
            return False, [], f"Malformed XML: {str(pe)}"

        articles = []
        # Look for standard RSS 2.0 channel/item or Atom entry
        items = root.findall(".//item")
        if not items:
            # Check Atom
            items = root.findall(".//{http://www.w3.org/2005/Atom}entry")

        for item in items:
            title_node = item.find("title")
            if title_node is None:
                title_node = item.find("{http://www.w3.org/2005/Atom}title")

            headline = title_node.text.strip() if title_node is not None and title_node.text else ""

            # Skip entries without headline
            if not headline:
                continue

            link_node = item.find("link")
            if link_node is None:
                link_node = item.find("{http://www.w3.org/2005/Atom}link")

            link = ""
            if link_node is not None:
                if link_node.text:
                    link = link_node.text.strip()
                elif link_node.get("href"):
                    link = link_node.get("href").strip()

            desc_node = item.find("description")
            if desc_node is None:
                desc_node = item.find("summary")
            if desc_node is None:
                desc_node = item.find("{http://www.w3.org/2005/Atom}summary")

            description = self.clean_html(desc_node.text) if desc_node is not None and desc_node.text else ""

            content_node = item.find("content")
            if content_node is None:
                content_node = item.find("{http://purl.org/rss/1.0/modules/content/}encoded")

            content = self.clean_html(content_node.text) if content_node is not None and content_node.text else ""

            date_node = item.find("pubDate")
            if date_node is None:
                date_node = item.find("published")
            if date_node is None:
                date_node = item.find("updated")
            if date_node is None:
                date_node = item.find("{http://www.w3.org/2005/Atom}updated")

            raw_date = date_node.text if date_node is not None and date_node.text else None
            pub_date = self.parse_pub_date(raw_date)

            article = NewsArticle(
                headline=headline,
                source_name=default_source_name,
                article_url=link or f"http://example.com/rss/{abs(hash(headline))}",
                description=description,
                content=content or description,
                publication_date=pub_date
            )
            articles.append(article)

        return True, articles, ""

    def collect_from_feed(self, source) -> Tuple[bool, List[NewsArticle], str]:
        """
        Executes fetch and parse for a NewsSource object.
        """
        ok, xml_str, err = self.fetch_feed_xml(source.feed_url)
        if not ok:
            return False, [], err

        ok_parse, articles, parse_err = self.parse_rss_xml(xml_str, default_source_name=source.name)
        if not ok_parse:
            return False, [], parse_err

        return True, articles, ""

    def load_offline_demo_feed(self) -> List[NewsArticle]:
        """
        Provides offline demonstration articles when network access is unavailable.
        """
        data = JsonStorage.load_data(DEMO_DATASET_FILE, default=[])
        articles = [NewsArticle.from_dict(d) for d in data if isinstance(d, dict)]
        return articles
