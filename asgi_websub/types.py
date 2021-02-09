import sys
import typing

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


# NOTE: Remove once asgiref releases those types.
Scope = typing.MutableMapping[str, typing.Any]
Message = typing.MutableMapping[str, typing.Any]

Receive = typing.Callable[[], typing.Awaitable[Message]]
Send = typing.Callable[[Message], typing.Awaitable[None]]

ASGIApp = typing.Callable[[Scope, Receive, Send], typing.Awaitable[None]]

DiscoverHeaders = TypedDict(
    "DiscoverHeaders", {"Accept": str, "Accept-Language": str}, total=False
)


class DiscoverURLs(TypedDict):
    hub: typing.Union[str, typing.List[str]]
    topic: str
