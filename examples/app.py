# def app(scope):
#     async def asgi(receive, send):
#         await send(
#             {
#                 "type": "http.response.start",
#                 "status": 200,
#                 "headers": [[b"content-type", b"text/plain"]],
#             }
#         )
#         await send({"type": "http.response.body", "body": b"Hello, world!"})

#     return asgi


async def app(scope, receive, send):
    assert scope["type"] == "http"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        }
    )
    await send({"type": "http.response.body", "body": b"Hello world!"})


# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.create_task(app)
#     loop.run_forever
