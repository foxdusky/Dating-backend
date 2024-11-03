from fastapi import HTTPException, status, BackgroundTasks
from sqlmodel import Session

from configs.env import MATCHING_REQUEST_DAILY_LIMITATION
from models.user.auth_model import _get_password_hash
from repositories.matching import matching_repository
from repositories.user import user_repository
from schemes.matching.matching_scheme import Matching
from schemes.user.user_scheme import User, UserListRequestBody, UserInfo, UserResponseAll
from services.mailing import matching_mailing
from geopy.distance import great_circle


def _check_operation_available(current_user: User, user_on_action: User) -> None:
    """
    A function that checks that the user is trying to change their data
    """
    if current_user.id != user_on_action:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied",
        )


def get_user_by_id(session: Session, user_id: int) -> User:
    """
    Function for getting user by his db id
    """
    user = user_repository.get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )

    return user


def _check_login_unique(session: Session, login: str) -> None:
    """
    Function that checks is login unique
    """
    user = user_repository.get_user_by_login(session, login)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Login: {login} is not unique",
        )


def _check_e_mail_unique(session: Session, e_mail: str) -> None:
    """
    Function that checks is e mail unique
    """
    user = user_repository.get_user_by_login(session, e_mail)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"E-mail: {e_mail} is not unique",
        )


def _limit_day_requests(session: Session, user_id: int):
    """
    Function that checks is user out of daily limit for matching
    """
    res = matching_repository.get_today_user_matching_by_id(session, user_id)
    if len(res) >= MATCHING_REQUEST_DAILY_LIMITATION:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests for today get relax, and return here tomorrow",
        )


def matching(session, current_user: User, matching_user_id: int, background_tasks: BackgroundTasks):
    """
    Function that consist all of the matching logix and sending
    """
    # Check for limit of daily requests
    _limit_day_requests(session, current_user.id)
    # Check for user existence
    get_user_by_id(session, matching_user_id)
    # Generating list with users ids
    ids = [current_user.id, matching_user_id]
    # Getting matching record if exists
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
        background_tasks.add_task(matching_mailing, users)

        return "Congrats your sympathy is mutual check the mail"
    else:
        match_obj = Matching(
            user_id=current_user.id,
            liked_user_id=matching_user_id,
        )
        matching_repository.create_matching(session, match_obj)
        return "Not liked you yet, we will notify you if the user reciprocates"


def get_all_users(session: Session, body: UserListRequestBody, current_user: User):
    total_count, result = user_repository.get_all_users(session, body, current_user.id)
    if body.distance_filter:
        _result: list[UserInfo] = []
        if current_user.width and current_user.longitude:
            current_cords = (current_user.width, current_user.longitude)
            for user in result:
                if user.width and user.longitude:
                    user_cords = (user.width, user.longitude)
                    distance = great_circle(current_cords, user_cords).kilometers
                    if distance <= body.distance_filter:
                        _result.append(user)
        return UserResponseAll(
            count=len(_result),
            result=_result
        )
    return UserResponseAll(
        count=total_count,
        result=result
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
