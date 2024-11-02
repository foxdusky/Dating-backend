from sqlmodel import create_engine, Session, SQLModel

from configs.env import DB_CON_STR, REDIS_HOST, REDIS_PORT

engine = create_engine(DB_CON_STR)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_redis():
    yield Redis(host=REDIS_HOST, port=REDIS_PORT)
