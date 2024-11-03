from sqlalchemy import and_, asc, desc, func, literal_column
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select, AutoString

from schemes.user.user_scheme import User, UserListRequestBody, UserResponseAll


def get_all_users(
    session: Session,
    body: UserListRequestBody,
) -> UserResponseAll:
    st = select(User).options(
        joinedload(User.gender), joinedload(User.photo),
    )

    # Фильтрация по параметрам из search_filter
    if body.search_filter:
        search_params = body.search_filter.dict(exclude_unset=True)
        filter_clauses = []
        for key, value in search_params.items():
            col = getattr(User, key, None)
            if col is not None and value is not None:
                if type(col.type) == AutoString:
                    filter_clauses.append(col.ilike(f"%{value}%"))
                else:
                    st = st.where(col == value)
        if filter_clauses:
            st = st.where(and_(*filter_clauses))

    # Order by sort field and direction
    if body.sort_field and body.sort_direction:
        sort_column = getattr(User, body.sort_field, None)

        if sort_column:
            if body.sort_direction.lower() == "asc":
                st = st.order_by(asc(sort_column))

            elif body.sort_direction.lower() == "desc":
                st = st.order_by(desc(sort_column))

    # Подзапрос для получения общего количества записей
    subquery = st.subquery()
    count_query = select(func.count(literal_column("*"))).select_from(subquery)
    total_count = session.exec(count_query).one()

    # Лимит и офсет для пагинации
    if body.limit:
        st = st.limit(body.limit)
    if body.offset:
        st = st.offset(body.offset)

    # Выполнение основного запроса и возврат результата
    result = session.exec(st).unique().all()

    # return {"count": total_count, "result": list(result)}
    return UserResponseAll(
        count=total_count,
        result=list(result),
    )


def get_user_by_id(session: Session, user_id: int) -> User | None:
    st = select(User)
    st = st.where(User.id == user_id)
    return session.exec(st).first()


def get_user_by_login(session: Session, login: str) -> User | None:
    st = select(User)
    st = st.where(User.username == login)
    return session.exec(st).first()


def get_user_by_e_mail(session: Session, e_mail: str) -> User | None:
    st = select(User)
    st = st.where(User.e_mail == e_mail)
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
