"""
A WebSub Subscriber is an implementation that discovers the hub and topic URL
given a resource URL, subscribes to updates at the hub, and accepts content
distribution requests from the hub. The subscriber MAY support
[authenticated content distribution](https://www.w3.org/TR/websub/#authenticated-content-distribution).
The conformance criteria are described in
[Conformance Classes](https://www.w3.org/TR/websub/#conformance-classes) above.
"""
import httpx


class Subscriber:
    def __init__(self) -> None:
        raise NotImplementedError("Subscriber not implemented yet.")

    async def discovery(self):
        ...

    async def subscribe(self):
        ...

    async def unsubscribe(self):
        ...
