"""Simple web-search tool for the MVP agent.

Uses DuckDuckGo HTML without an extra dependency. This is a learning/demo
searcher, not a production research crawler.
"""
from html.parser import HTMLParser
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


class ResultParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self._link = None
        self._text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "result__a" in attrs.get("class", ""):
            self._link = attrs.get("href")
            self._text = []

    def handle_data(self, data):
        if self._link is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._link:
            title = " ".join("".join(self._text).split())
            if title:
                self.results.append({"title": title, "url": self._link})
            self._link = None
            self._text = []


def search(query: str, max_results: int = 5) -> list[dict]:
    url = "https://html.duckduckgo.com/html/?q=" + quote(query)
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", errors="ignore")

    parser = ResultParser()
    parser.feed(html)

    output = []
    seen = set()
    for item in parser.results:
        domain = urlparse(item["url"]).netloc
        if item["url"] not in seen and domain:
            seen.add(item["url"])
            output.append({**item, "domain": domain})
        if len(output) >= max_results:
            break
    return output
