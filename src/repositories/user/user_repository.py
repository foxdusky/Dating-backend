from sqlmodel import Session, select

from schemes.user.user_scheme import User


def get_all_users(session: Session) -> list[User]:
    st = select(User)
    result = session.exec(st).all()
    return list(result)


def get_user_by_id(session: Session, user_id: int) -> User | None:
    st = select(User)
    st = st.where(User.id == user_id)
    return session.exec(st).first()


def get_user_by_login(session: Session, login: str) -> User | None:
    st = select(User)
    st = st.where(User.username == login)
    return session.exec(st).first()


def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, user: User):
    db_user = session.merge(user)
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, user: User):
    session.delete(user)
    session.commit()
    return user
