from app.schemas import models
from app.schemas.servers import Servers
from app.utils.paginations import PaginationDep, Session
from fastapi import APIRouter, Query
from sqlmodel import col, select

router = APIRouter()


@router.get(
    "/",
    response_model=list[Servers],
    summary="Список серверов",
    description="Полный список серверов с пагинацией и фильтрами",
)
async def list_servers(
    session: Session,
    pagination: PaginationDep,
    name: str | None = Query(
        None,
        min_length=1,
        max_length=255,
        description="Поиск по имени сервера",
    ),
    verified: bool | None = Query(
        None,
        description="Фильтр по верификации",
    ),
) -> list[Servers]:
    stmt = select(models.Servers)

    if name is not None:
        stmt = stmt.where(col(models.Servers.name).ilike(f"%{name}%"))

    if verified is not None:
        stmt = stmt.where(col(models.Servers.verified) == verified)

    stmt = (
        stmt.order_by(col(models.Servers.id))
        .offset(pagination.offset)
        .limit(pagination.limit)
    )

    result = await session.execute(stmt)
    servers = result.scalars().all()

    # Преобразуем ORM-объекты в Pydantic-модели
    return [Servers.model_validate(server) for server in servers]
