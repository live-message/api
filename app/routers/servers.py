from app.schemas.models import Servers
from app.services.database import get_async_session
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

router = APIRouter()


@router.get(
    "/",
    response_model=list[Servers],
    summary="Список серверов",
    description="Полный список серверов с пагинацией",
)
async def get_all_servers(
    session: AsyncSession = Depends(get_async_session),  # noqa: B008
    offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(
        default=100, ge=1, le=1000, description="Количество записей на странице"
    ),
):
    """
    Получение списка серверов с пагинацией

    Args:
        session: Асинхронная сессия базы данных
        offset: Смещение (начиная с 0)
        limit: Максимальное количество записей (от 1 до 1000)

    Returns:
        Список серверов
    """
    query = select(Servers).offset(offset).limit(limit)
    result = await session.execute(query)
    servers = result.scalars().all()

    return servers
