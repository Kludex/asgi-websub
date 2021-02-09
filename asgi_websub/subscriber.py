"""
A WebSub Subscriber is an implementation that discovers the hub and topic URL
given a resource URL, subscribes to updates at the hub, and accepts content
distribution requests from the hub. The subscriber MAY support
[authenticated content distribution](https://www.w3.org/TR/websub/#authenticated-content-distribution).
The conformance criteria are described in
[Conformance Classes](https://www.w3.org/TR/websub/#conformance-classes) above.

Reference: https://www.w3.org/TR/websub/#subscriber
"""
import asyncio

import httpx

from asgi_websub.exceptions import HubNotFoundException
from asgi_websub.types import ASGIApp, DiscoverHeaders
from asgi_websub.utils import discover_urls


class Subscriber:
    def __init__(self, app: ASGIApp) -> None:
        ...

    async def discover(self, resource_url: str, headers: DiscoverHeaders = None):
        """
        This package doesn't support content negotiation as stated on section 4.1.
        Reasons for that choice can be found [here](https://wiki.whatwg.org/wiki/Why_not_conneg).

        Reference: https://www.w3.org/TR/websub/#content-negotiation
        """
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(resource_url, headers=headers)
                if res.is_error:
                    raise HubNotFoundException(f"Response error for {res.url}")
        except httpx.HTTPError as exc:
            raise HubNotFoundException(f"HTTP Exception for {exc.request.url}") from exc
        return discover_urls(res)

    async def subscribe(self):
        ...

    async def unsubscribe(self):
        ...


async def main():
    subs = Subscriber("haha")
    await subs.discover(
        "https://www.youtube.com/xml/feeds/videos.xml?channel_id=UCpdagXDNCWHnztIbwRviPXQ"
    )
    # await subs.discover("haha")


if __name__ == "__main__":
    asyncio.run(main())
