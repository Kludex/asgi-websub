class ASGIWebSubException(Exception):
    ...


class HubNotFoundException(ASGIWebSubException):
    ...


class TopicNotFoundException(ASGIWebSubException):
    ...


class SubscriptionException(ASGIWebSubException):
    ...
