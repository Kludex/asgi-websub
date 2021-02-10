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
from typing import Any, Dict, Literal

import httpx

from asgi_websub.exceptions import (
    HubNotFoundException,
    SubscriptionException,
    TopicNotFoundException,
)
from asgi_websub.types import DiscoverHeaders
from asgi_websub.utils import discover_urls


class Subscriber:
    def __init__(self) -> None:
        self.topic_url = None

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
        urls = discover_urls(res)
        self.topic_url = urls["topic"]
        return urls

    async def subscription_request(
        self,
        hub_url: str,
        callback_url: str,
        mode: Literal["subscribe", "unsubscribe"],
        *,
        topic_url: str = None,
        lease_seconds: int = None,
        secret: str = None,
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
    ):
        """
        Allow `topic_url` for backward portability to
        [PubSubHubbub-Core-0.4](https://pubsubhubbub.github.io/PubSubHubbub/pubsubhubbub-core-0.4.html).
        """
        self.topic_url = topic_url or self.topic_url
        if self.topic_url is None:
            raise TopicNotFoundException("Run discover() method first")

        optional_data = {}
        if lease_seconds is not None:
            optional_data["hub.lease_seconds"] = lease_seconds
        if secret is not None:
            optional_data["hub.secret"] = secret
        headers = headers or {}
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    hub_url,
                    data={
                        "hub.callback": callback_url,
                        "hub.mode": mode,
                        "hub.topic": self.topic_url,
                        **optional_data,
                    },
                    params=params,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        **headers,
                    },
                )
                if res.is_error:
                    if res.headers.get("content-type") == "plain/text":
                        raise SubscriptionException(res.content)
                    raise SubscriptionException("Hub found errors in the request")
                if res.status_code != 202:
                    raise SubscriptionException(
                        'Hub should send a 202 "Accepted" in case of acceptance. '
                        "Reference: https://www.w3.org/TR/websub/#subscription-response-details"
                    )
        except httpx.HTTPError as exc:
            raise HubNotFoundException(f"HTTP Exception for {exc.request.url}") from exc

    async def subscribe(
        self,
        hub_url: str,
        callback_url: str,
        *,
        topic_url: str = None,
        lease_seconds: int = None,
        secret: str = None,
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
    ):
        await self.subscription_request(
            hub_url=hub_url,
            callback_url=callback_url,
            mode="subscribe",
            topic_url=topic_url,
            lease_seconds=lease_seconds,
            secret=secret,
            params=params,
            headers=headers,
        )

    async def unsubscribe(
        self,
        hub_url: str,
        callback_url: str,
        *,
        topic_url: str = None,
        lease_seconds: int = None,
        secret: str = None,
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
    ):
        await self.subscription_request(
            hub_url=hub_url,
            callback_url=callback_url,
            mode="unsubscribe",
            topic_url=topic_url,
            lease_seconds=lease_seconds,
            secret=secret,
            params=params,
            headers=headers,
        )


async def main():
    topic_url = "https://www.youtube.com/xml/feeds/videos.xml?channel_id=UCpdagXDNCWHnztIbwRviPXQ"
    subs = Subscriber("")
    urls = await subs.discover(topic_url)
    await subs.subscribe(
        hub_url=urls["hub"][0],
        callback_url="https://8371f0fade04.ngrok.io",
        topic_url=topic_url,
    )


if __name__ == "__main__":
    asyncio.run(main())
