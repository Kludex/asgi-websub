import uvicorn
from fastapi import FastAPI, Request

from asgi_websub.subscriber import Subscriber


class FastAPISubscriber(Subscriber):
    def __init__(self, app: FastAPI, callback_url: str):
        super().__init__()

        self.callback_url = callback_url

        async def callback(request: Request):
            print(request.query_params.get("hub.mode"))  # "denied", "subscribe", "un"
            print(request.query_params.get("hub.topic"))
            print(request.query_params.get("hub.reason"))
            print(request.query_params.get("hub.lease_seconds"))
            print(request.headers)
            challenge = request.query_params.get("hub.challenge")
            return challenge

        app.add_api_route(callback_url, callback)


app = FastAPI()


@app.on_event("startup")
async def startup():
    subs = FastAPISubscriber(app, "/")
    topic_url = "https://www.youtube.com/xml/feeds/videos.xml?channel_id=UCpdagXDNCWHnztIbwRviPXQ"
    urls = await subs.discover(topic_url)
    await subs.subscribe(
        hub_url=urls["hub"][0],
        callback_url="https://b1fde2b4c038.ngrok.io",
        topic_url=topic_url,
    )


if __name__ == "__main__":
    uvicorn.run(app)
