from sqlmodel import Session, select

from schemes.file.file_scheme import File


def get_all_files(session: Session) -> list[File]:
    st = select(File)
    result = session.exec(st).all()
    return list(result)


def get_files_count(session: Session) -> int:
    return session.query(File).count()


def get_file_by_id(session: Session, file_id: int):
    result = session.get(File, file_id)
    return result


def create_file(session: Session, file: File) -> File:
    session.add(file)
    session.commit()
    session.refresh(file)
    return file


def delete_file(session: Session, file: File) -> File:
    session.delete(file)
    session.commit()
    return file
