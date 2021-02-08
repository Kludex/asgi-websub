"""
A WebSub Hub is an implementation that handles subscription requests and distributes
the content to subscribers when the corresponding topic URL has been updated. Hubs
MUST support subscription requests with a secret and deliver
[authenticated requests](https://www.w3.org/TR/websub/#authenticated-content-distribution)
when requested. Hubs MUST deliver the full contents of the topic URL in the request, and
MAY reduce the payload to a diff if the content type supports it. The conformance
criteria are described in Conformance Classes above.
"""


class Hub:
    ...
