import httpx
import yadisk
from ..config import settings

from urllib.parse import quote
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession

from .. import database, schemas, oauth2
from ..utils import cloud
from ..schemas import Role
from ..service import hometask

router = APIRouter(prefix="/hometask", tags=['Hometasks'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.HomeTaskOut)
async def create_home_task(
        home_task_form: schemas.HomeTaskCreate,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if user.role == Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только репетиторы могут создавать формы для сдач домашних заданий."
        )
    new_home_task = await hometask.add_home_task(db, home_task_form, user.id)
    return new_home_task


@router.post("/{home_task_id}", status_code=status.HTTP_201_CREATED)
async def upload_home_task(
        home_task_id: int,
        file: UploadFile,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
) -> schemas.HomeTaskOut:
    if user.role == Role.tutor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только студенты могут сдавать домашние задания"
        )
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Формат файла отличается от pdf")

    async_client = yadisk.AsyncYaDisk(token=settings.yandex_disk_token)
    destination_path = f"/TutorStudentApp/{home_task_id}"
    async with async_client:
        await cloud.create_folder_disk(async_client, destination_path)
        await async_client.upload(file.file, f"{destination_path}/{file.filename}")
        home_task = await hometask.add_response_to_task(db, home_task_id, file.filename)
        return home_task


@router.get("/{home_task_id}", status_code=status.HTTP_200_OK)
async def download_home_task(
        home_task_id: int,
        user: schemas.UserOut = Depends(oauth2.get_current_user),
        db: AsyncSession = Depends(database.get_db)
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Скачивание домашних заданий доступно только авторизованным пользователям"
        )
    y = yadisk.AsyncYaDisk(token=settings.yandex_disk_token)
    async with y:
        home_task_path = f"/TutorStudentApp/{home_task_id}"
        if not await y.exists(home_task_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Home task was not created before"
            )
        home_task = await hometask.get_home_task_by_id(db=db, home_task_id=home_task_id)
        home_task_path = f"{home_task_path}/{home_task.filename}"
        download_link = await y.get_download_link(home_task_path)
        async with httpx.AsyncClient() as client:
            response = await client.get(download_link, follow_redirects=True)
            headers = {'Content-Disposition': f'attachment; filename={quote(home_task.filename)}'}
            return Response(content=response.content, media_type='application/pdf', headers=headers)
