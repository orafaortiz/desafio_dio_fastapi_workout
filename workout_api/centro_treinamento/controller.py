from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoSchemaIn, CentroTreinamentoSchemaOut
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()


@router.post(
    "/",
    summary="Cria um novo centro de treinamento",
    response_model=CentroTreinamentoSchemaOut,
    status_code=status.HTTP_201_CREATED
)
async def post(
        db_session: DatabaseDependency,
        centro_treinamento_in: CentroTreinamentoSchemaIn = Body(...)
) -> CentroTreinamentoSchemaOut:
    centro_treinamento_out = CentroTreinamentoSchemaOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out


@router.get(
    "/",
    summary="Lista todos os centros de treinamento",
    response_model=list[CentroTreinamentoSchemaOut],
    status_code=status.HTTP_200_OK
)
async def query(
        db_session: DatabaseDependency
) -> list[CentroTreinamentoSchemaOut]:
    centros_treinamento: list[CentroTreinamentoSchemaOut] = (
        await db_session.execute(select(CentroTreinamentoModel))
    ).scalars().all()

    return centros_treinamento


@router.get(
    "/{id}",
    summary="Busca um centro de treinamento por id",
    response_model=CentroTreinamentoSchemaOut,
    status_code=status.HTTP_200_OK
)
async def get(
        db_session: DatabaseDependency,
        id: UUID4
) -> CentroTreinamentoSchemaOut:
    centro_treinamento_out: CentroTreinamentoSchemaOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro_treinamento_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centro de treinamento não encontrado")

    return centro_treinamento_out
