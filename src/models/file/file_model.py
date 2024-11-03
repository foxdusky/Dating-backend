import io
import os
from datetime import datetime
from typing import Any

from PIL import Image, ImageEnhance
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from sqlmodel import Session

from configs.env import PICTURES_DIR
from repositories.file import file_repository
from repositories.user.user_repository import update_user
from schemes.file.file_scheme import File
from schemes.user.user_scheme import User

watermark_image_path = f'{PICTURES_DIR}/watermark.png'


def get_file_by_id(session: Session, file_id: int) -> File:
    file = file_repository.get_file_by_id(session, file_id)

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File with ID {file_id} not found",
        )

    return file


def get_file_response(file_path: str, filename: str) -> FileResponse:
    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=filename,
    )


def get_file_source(filename: str):
    file_path = os.path.join(PICTURES_DIR, filename)

    if os.path.exists(file_path):
        return get_file_response(file_path, filename)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File with name {filename} not found locally",
    )


def get_file_source_by_id(
    session: Session,
    file_id: int,
):
    file = get_file_by_id(session, file_id)
    return get_file_source(file.name)


async def create_file(
    session: Session,
    user: User,
    file: Any,
    position: tuple = (-1, -1),
    transparency: float = 0.5
):
    name = f"{user.username}-{datetime.now()}.jpg"
    output_image_path = f'{PICTURES_DIR}/{name}'
    # Opens watermark image
    watermark = Image.open(watermark_image_path).convert("RGBA")

    # Opens image from byte object
    base_image = Image.open(io.BytesIO(file)).convert("RGBA")

    base_width, base_height = base_image.size
    watermark = watermark.resize((base_width // 4, base_height // 4), )
    watermark = ImageEnhance.Brightness(watermark).enhance(transparency)
    base_image.paste(watermark, position, watermark)
    base_image.convert("RGB").save(output_image_path, "JPEG")

    _file = file_repository.create_file(
        session,
        File(
            filename=f'{name}',
            front_name=f"Profile photo of {user.username}",
        )
    )
    updating_user_info = User(
        id=user.id,
        profile_photo=_file.id
    )
    update_user(session, updating_user_info)
