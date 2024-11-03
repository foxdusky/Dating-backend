from fastapi import HTTPException, status
from sqlmodel import Session

from configs.env import RESEND_API_KEY
from models.user.auth_model import _get_password_hash
from repositories.matching import matching_repository
from repositories.user import user_repository
from schemes.matching.matching_scheme import Matching
from schemes.user.user_scheme import User
import resend

resend.api_key = RESEND_API_KEY


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


def matching(session, current_user: User, matching_user_id: int):
    ids = [current_user.id, matching_user_id]
    matching_record = matching_repository.get_match_by_ids(
        session=session,
        ids=ids
    )
    # check for sympathy is mutual
    if matching_record:
        if current_user.id == matching_record.user_id:
            return "Don't spam, you already liked that user"
        if matching_record.is_mutual:
            return "You already liked that user, or he liked u backwards"
        matching_repository.set_matching_to_mutual(session, matching_record)
        users: list[User] = []
        for user_id in ids:
            users.append(user_repository.get_user_by_id(session, user_id))
        # Sending email messages
        for i in range(len(users)):
            recipient_index = (i + 1) % len(users)  # Получаем индекс следующего пользователя
            r = resend.Emails.send({
                "from": "dating@redbread.tech",
                "to": f"{users[i].e_mail}",
                "subject": "Somebody liked your profile",
                "html": f"{users[recipient_index].name} liked you. Participant's email address: {users[recipient_index].e_mail}"
            })
        return "Congrats your sympathy is mutual check the mail"
    else:
        match_obj = Matching(
            user_id=current_user.id,
            liked_user_id=matching_user_id,
        )
        matching_repository.create_matching(session, match_obj)
        return "Not liked you yet, we will notify you if the user reciprocates"


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
