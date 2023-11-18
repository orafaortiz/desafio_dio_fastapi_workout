from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoSchemaIn, CentroTreinamentoSchemaOut
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from fastapi_pagination import Page, paginate

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
    centro_treinamento_out = None

    try:
        centro_treinamento_out = CentroTreinamentoSchemaOut(id=uuid4(), **centro_treinamento_in.model_dump())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

        db_session.add(centro_treinamento_model)
        await db_session.commit()

    except IntegrityError as e:
        await db_session.rollback()
        if "duplicate key value" in str(e):
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
                                detail=f"Já existe um centro de treinamento com o nome {centro_treinamento_in.nome}")

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro ao criar centro de treinamento")

    return centro_treinamento_out


@router.get(
    "/",
    summary="Lista todos os centros de treinamento",
    response_model=Page[CentroTreinamentoSchemaOut],
    status_code=status.HTTP_200_OK
)
async def query(
        db_session: DatabaseDependency
) -> Page[CentroTreinamentoSchemaOut]:

    query_centros_treinamento = select(CentroTreinamentoModel)
    result = await db_session.execute(query_centros_treinamento)
    centros_treinamento: list[CentroTreinamentoSchemaOut] = result.scalars().all()
    return paginate(centros_treinamento)


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
