from fastapi import APIRouter, Depends
from sqlmodel import Session

from constant.ws_queues import WSQueue
from db import get_session
from middleware.ws_queue_decorator import ws_queue
from models.user import user_model
from models.user.auth_model import sign_in
from models.user.auth_model import get_current_user
from schemes.user.auth_scheme import AuthToken
from schemes.user.user_scheme import User

queue_name = WSQueue.USER

user_router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@user_router.post(
    "/create/",
    response_model=AuthToken,
    description="Function for creating user exemplar in database by user him own self"
)
def registration(
    user: User,
    session: Session = Depends(get_session),
):
    password = user.password
    user_model.create_user(session, user)
    token = sign_in(session, user.username, password)
    return token


@user_router.get("/current/", response_model=User, description="Func for getting info about current client")
async def get_current_user(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_model.get_user_by_id(session, current_user.id)


@user_router.put("/", response_model=User, description="Function for update profile by user him own self")
@ws_queue(queue_name)
async def update_user(
    user: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_model.update_user(session, user, current_user)


@user_router.delete("/{user_id}", response_model=User, description="Function for delete profile by user him own self")
@ws_queue(queue_name)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_model.delete_user(session, user_id, current_user)
