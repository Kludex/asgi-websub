from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup
from httpx import Response

from asgi_websub.exceptions import HubNotFoundException
from asgi_websub.types import DiscoverURLs


def discover_urls(res: Response) -> DiscoverURLs:
    """
    When performing discovery, subscribers MUST implement all three discovery mechanisms
    in the following order, stopping at the first match:
    1. Issue a GET or HEAD request to retrieve the topic URL. Subscribers MUST check for
        HTTP Link headers first.
    2. In the absence of HTTP Link headers, and if the topic is an XML based feed or an
        HTML page, subscribers MUST check for embedded link elements.

    Reference: https://www.w3.org/TR/websub/#discovery
    """
    links = res.headers.get_list("link")
    if links:
        return links
    if res.headers.get("content-type") == "text/xml":
        root = ET.ElementTree(ET.fromstring(res.content)).getroot()
        return {
            "hub": [url.get("href") for url in root.findall(".//*[@rel='hub']")],
            "topic": root.find(".//*[@rel='self']").get("href"),
        }
    if res.headers.get("content-type") == "text/html":
        soup = BeautifulSoup(res.content, "html.parser")
        return {
            "hub": [url.get("href") for url in soup.find_all(attrs={"rel": "hub"})],
            "topic": soup.find(attrs={"rel": "self"}),
        }
    raise HubNotFoundException(f"Can't parse data from {res.url}")
