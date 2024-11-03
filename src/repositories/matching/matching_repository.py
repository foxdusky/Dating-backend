from sqlmodel import Session, select

from schemes.matching.matching_scheme import Matching
from datetime import date, timedelta


def get_today_user_matching_by_id(session: Session, user_id: int):
    today = date.today()
    st = select(Matching).where(Matching.user_id == user_id)
    st = st.where(Matching.created_at >= today)
    st = st.where(Matching.created_at < today + timedelta(days=1))
    return session.exec(st).all()


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


def delete_matching(session: Session, matching: Matching):
    session.delete(matching)
    session.commit()
    return matching
