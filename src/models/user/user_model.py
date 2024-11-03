from fastapi import HTTPException, status
from sqlmodel import Session

from models.user.auth_model import _get_password_hash
from repositories.user import user_repository
from schemes.user.user_scheme import User


def _check_operation_available(current_user: User, user_on_action: User) -> None:
    if current_user.id != user_on_action:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied",
        )


def get_user_by_id(session: Session, user_id: int) -> User:
    user = user_repository.get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    return user


def get_by_login(session: Session, login: str) -> User:
    user = user_repository.get_user_by_login(session, login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with login {login} not found",
        )
    return user


def _check_login_unique(session: Session, login: str) -> None:
    user = user_repository.get_user_by_login(session, login)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Login: {login} is not unique",
        )


def _check_e_mail_unique(session: Session, e_mail: str) -> None:
    user = user_repository.get_user_by_login(session, e_mail)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"E-mail: {e_mail} is not unique",
        )





def create_user(session: Session, user: User) -> User:
    """
    Function for create user sample in database
    also checks if users login unique and email
    returns 400 Bad Request if login or e_mail isn't unique with detail string
    """
    _check_login_unique(session, user.username)
    _check_e_mail_unique(session, user.e_mail)

    user.password = _get_password_hash(user.password)
    return user_repository.create_user(session, user)


def update_user(session: Session, user: User, current_user: User) -> User:
    db_user = get_user_by_id(session, user.id)
    _check_operation_available(current_user=current_user, user_on_action=db_user)

    if db_user.username != user.username:
        _check_login_unique(session, user.username)
    if user.password is not None:
        user.password = _get_password_hash(user.password)

    return user_repository.update_user(session, user)


def delete_user(session: Session, user_id: int, current_user: User):
    db_user = get_user_by_id(session, user_id)
    _check_operation_available(current_user=current_user, user_on_action=db_user)
    return user_repository.delete_user(session, db_user)
