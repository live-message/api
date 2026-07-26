from collections.abc import Sequence
from typing import Annotated

from app.schemas import models
from app.schemas.servers import ServerRead
from app.utils.paginations import PaginationDep, Session
from fastapi import APIRouter, Query
from sqlmodel import select

router = APIRouter()


@router.get(
    "/",
    response_model=list[ServerRead],
    summary="Список серверов",
    description="Полный список серверов с пагинацией и фильтрами",
)
async def list_servers(
    session: Session,
    pagination: PaginationDep,
    name: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=255,
            description="Поиск по имени сервера",
        ),
    ] = None,
    status: Annotated[
        str | None,
        Query(
            description="Фильтр по статусу",
        ),
    ] = None,
) -> Sequence[models.Servers]:
    stmt = select(models.Servers)

    if name:
        stmt = stmt.where(models.Servers.name.ilike(f"%{name}%"))

    if status:
        stmt = stmt.where(models.Servers.status == status)

    stmt = (
        stmt.order_by(models.Servers.id)
        .offset(pagination.offset)
        .limit(pagination.limit)
    )

    result = await session.execute(stmt)
    servers = result.scalars().all()

    return servers
