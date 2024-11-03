import uvicorn
from fastapi import FastAPI, Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session

from configs.env import PICTURES_DIR, IS_DEV_ENV
from controllers.user.auth_controller import auth_router
from controllers.user.user_controller import user_router
from db import get_session
from models.user import user_model
from models.user.auth_model import get_current_user
from schemes.user.user_scheme import User, UserResponseAll, UserListRequestBody
from ws import ws_manager

app = FastAPI(
    title="Dating API",
    description="API Dating",
    version="0.0.1",
    pics_url="/pics",
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


# ############################### #


@app.get("/healthcheck")
def health_check():
    return {"status": "ok"}


@app.post(
    "/list",
    response_model=UserResponseAll,
    description="Function for getting list of users with sort and filters"
)
def get_list_of_clients(
    body: UserListRequestBody,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_model.get_all_users(session, body, current_user)


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
