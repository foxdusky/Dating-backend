from sqlmodel import Session, select

from schemes.matching.matching_scheme import Matching
from schemes.user.user_scheme import User


def get_match_by_ids(session: Session, ids: list[int]) -> Matching | None:
    st = select(Matching).where(
        (Matching.user_id == ids[0] and Matching.liked_user_id == ids[1])
        or
        (Matching.user_id == ids[1] and Matching.liked_user_id == ids[0]))
    return session.exec(st).first()


def create_matching(session: Session, matching: Matching):
    session.add(matching)
    session.commit()
    session.refresh(matching)
    return matching


def set_matching_to_mutual(session: Session, matching: Matching):
    matching.is_mutual = True
    return update_matching(session, matching)


def update_matching(session: Session, matching: Matching):
    db_matching = session.merge(matching)
    session.commit()
    session.refresh(db_matching)
    return db_matching


def delete_user(session: Session, user: User):
    session.delete(user)
    session.commit()
    return user
