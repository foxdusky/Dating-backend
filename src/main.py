import uvicorn
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from configs.env import PICTURES_DIR, IS_DEV_ENV
from controllers.chat.chat_controller import chat_router
from controllers.message.message_controller import message_router
from controllers.user.auth_controller import auth_router
from controllers.user.user_controller import user_router
from ws import ws_manager

app = FastAPI(
    title="RedBread Chat API",
    description="API RedBread Chat",
    version="0.0.1",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

# TEST Sector
app.mount("/static", StaticFiles(directory=PICTURES_DIR), name="static")

# Auth sector
app.include_router(auth_router)

# ############################### #

app.include_router(user_router)
app.include_router(chat_router)
app.include_router(message_router)


# ############################### #


# logger.remove()
# logger.add("file_{time}.log", rotation="1 day", retention="10 days", level="DEBUG", format="{time} {level} {message}")
#
#
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logger.info(f"Incoming request: {request.method} {request.url}")
#     response = await call_next(request)
#     logger.info(f"Response status: {response.status_code}")
#     return response

@app.get("/healthcheck")
def health_check():
    return {"status": "ok"}


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


if __name__ == "__main__":
    if IS_DEV_ENV:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8080,
            use_colors=True,
            reload=True,
            log_level="info",
        )
    else:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8080,
            use_colors=True,
            reload=False,
            log_level="info",
            ssl_keyfile="/app/key_file.pem",
            ssl_certfile="/app/ssl_cert.pem",
        )
