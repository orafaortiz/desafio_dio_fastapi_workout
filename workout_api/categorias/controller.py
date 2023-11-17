from fastapi import APIRouter, status, Body, HTTPException
from pydantic import UUID4

from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaSchemaIn, CategoriaSchemaOut
from workout_api.contrib.dependencies import DatabaseDependency
from uuid import uuid4
from sqlalchemy.future import select

router = APIRouter()


@router.post(
    "/",
    summary="Criar nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaSchemaOut
)
async def post(
    db_session: DatabaseDependency,
    categoria_in: CategoriaSchemaIn = Body(...)
) -> CategoriaSchemaOut:

    categoria_out = CategoriaSchemaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out


@router.get(
    "/",
    summary="Listar todas as categorias",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaSchemaOut]
)
async def query(
    db_session: DatabaseDependency
) -> list[CategoriaSchemaOut]:

    categorias: list[CategoriaSchemaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return categorias


@router.get(
    "/{id_categoria}",
    summary="Buscar categoria por id",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaSchemaOut
)
async def get(db_session: DatabaseDependency, id_categoria: UUID4) -> CategoriaSchemaOut:
    categoria_out: CategoriaSchemaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id_categoria))
    ).scalars().first()

    if not categoria_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada")

    return categoria_out
