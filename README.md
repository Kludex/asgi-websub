<h1 align="center">
    <strong>asgi-websub</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/asgi-websub" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/asgi-websub" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/Kludex/asgi-websub/Test">
        <img src="https://img.shields.io/codecov/c/github/Kludex/asgi-websub">
    <br />
    <a href="https://pypi.org/project/asgi-websub" target="_blank">
        <img src="https://img.shields.io/pypi/v/asgi-websub" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/asgi-websub">
    <img src="https://img.shields.io/github/license/Kludex/asgi-websub">
</p>

This project implements WebSub for ASGI applications.

Code inspiration:
- https://github.com/ShadowJonathan/pywebsub/
- https://github.com/encode/starlette/
- https://github.com/django/asgiref/blob/master/asgiref/typing.py
- https://github.com/hemerajs/websub-hub

## Installation

``` bash
pip install asgi-websub
```

## Roadmap

For the purposes of evaluating exit criteria, each of the following is considered a feature:

- [X] Discovering the hub and topic URLs by looking at the HTTP headers of the resource URL.
- [X] Discovering the hub and topic URLs by looking at the contents of the resource URL as an XML document.
- [X] Discovering the hub and topic URLs by looking at the contents of the resource URL as an HTML document.
- [X] Subscribing to the hub with a callback URL.
- [X] Subscribing to the hub and requesting a specific lease duration.
- [ ] Subscribing to the hub with a secret and handling authenticated content distribution.
- [X] Requesting that a subscription is deactivated by sending an unsubscribe request.
- [ ] The Subscriber acknowledges a pending subscription on a validation request.
- [ ] The Subscriber rejects a subscription validation request for an invalid topic URL.
- [ ] The Subscriber returns an HTTP 2xx response when the payload is delivered.
- [ ] The Subscriber verifies the signature for authenticated content distribution requests.
- [ ] The Subscriber rejects the distribution request if the signature does not validate.
- [ ] The Subscriber rejects the distribution request when no signature is present if the subscription was made with a secret.
- [ ] The Hub respects the requested lease duration during a subscription request.
- [ ] The Hub allows Subscribers to re-request already active subscriptions, extending the lease duration.
- [ ] The Hub sends the full contents of the topic URL in the distribution request.
- [ ] The Hub sends a diff of the topic URL for the formats that support it.
- [ ] The Hub sends a valid signature for subscriptions that were made with a secret.


## License

This project is licensed under the terms of the MIT license.
