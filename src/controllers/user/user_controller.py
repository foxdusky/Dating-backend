from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks, File, Body
from sqlmodel import Session

from constant.ws_queues import WSQueue
from db import get_session
from middleware.ws_queue_decorator import ws_queue
from models.file.file_model import create_file
from models.user import user_model
from models.user.auth_model import get_current_user
from models.user.auth_model import sign_in
from schemes.user.auth_scheme import AuthToken
from schemes.user.user_scheme import User, UserRegistration, UserInfo

queue_name = WSQueue.USER

user_router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@user_router.post(
    "/create/",
    response_model=AuthToken,
    description="Function for creating user exemplar in database by user him own self"
                " ||username: Require a unique name of user, also it's checking for unique"
                " ||e_mail: Require a user email, also it's checking for unique"
                " ||gender_id: Users gender in int 1 is male, 2 is female",
    responses={
        200: {
            "description": "User successfully registered",
            "content": {"application/json": {"example": {"message": "Registration successful", "user_id": 1}}},
        },
        400: {
            "description": "Bad request - Possible reasons: invalid email format, non-unique username or email",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_email": {"summary": "Invalid email format", "value": {"detail": "Wrong email"}},
                        "non_unique_username": {"summary": "Username not unique",
                                                "value": {"detail": "Login: {username} is not unique"}},
                        "non_unique_email": {"summary": "Email not unique",
                                             "value": {"detail": "E-mail: {email} is not unique"}}
                    }
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {"application/json": {"example": {"detail": "Internal server error"}}},
        },
    })
def registration(
    background_tasks: BackgroundTasks,
    user: UserRegistration = Depends(),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    password = user.password
    user = User(**user.model_dump())
    _user = user_model.create_user(session, user)
    token = sign_in(session, user.username, password)
    file = file.file.read()
    background_tasks.add_task(create_file, session, _user, file)
    return token


@user_router.get("/current/", response_model=UserInfo, description="Func for getting info about current client")
async def get_current_user(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_model.get_user_by_id(session, current_user.id)


# Not in use yet

# @user_router.get("/{client_id}", response_model=User, description="Func for getting info about client by his id")
# async def get_user_by_id(
#     client_id: int,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     return user_model.get_user_by_id(session, client_id)


@user_router.post(
    "/{id}/match",
    response_model=str,
    description="Func for liking a user by their ID",
    responses={
        200: {
            "description": "Sympathy action completed successfully",
            "content": {
                "application/json": {
                    "examples": {
                        "mutual_sympathy": {"summary": "Mutual sympathy",
                                            "value": {"detail": "Congrats your sympathy is mutual check the mail"}},
                        "not_yet_mutual": {"summary": "Not mutual yet", "value": {
                            "detail": "Not liked you yet, we will notify you if the user reciprocates"}},
                    }
                }
            },
        },
        403: {
            "description": "Sympathy already reciprocated",
            "content": {
                "application/json": {
                    "example": {"detail": "You already liked that user, or they liked you back"}
                }
            },
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {"detail": "User with ID {id} not found"}
                }
            },
        },
        429: {
            "description": "Too many requests",
            "content": {
                "application/json": {
                    "examples": {
                        "daily_limit_exceeded": {"summary": "Daily request limit exceeded", "value": {
                            "detail": "Too many requests for today. Relax and try again tomorrow"}},
                        "already_liked": {"summary": "Already liked",
                                          "value": {"detail": "Don't spam, you already liked that user"}}
                    }
                }
            },
        },
    },
)
async def matching(
    id: int,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return user_model.matching(session, current_user, id, background_tasks)

# TODO: Add updating profile photo
# @user_router.put("/", response_model=User, description="Function for update profile by user him own self")
# @ws_queue(queue_name)
# async def update_user(
#     user: User,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     return user_model.update_user(session, user, current_user)

# TODO: Add deleting profile photo
# @user_router.delete("/{user_id}", response_model=User, description="Function for delete profile by user him own self")
# @ws_queue(queue_name)
# async def delete_user(
#     user_id: int,
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     return user_model.delete_user(session, user_id, current_user)
