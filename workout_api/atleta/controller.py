from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, status, Body, HTTPException, Query
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaSchemaIn, AtletaSchemaOut, AtletaSchemaPatch, AllAthletesSchemaOut
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo atleta",
    response_model=AtletaSchemaOut
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaSchemaIn = Body(...)
) -> AtletaSchemaOut:
    categoria = ((await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome)))
                 .scalars().first())

    if categoria is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria não encontrada")

    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome)
    )).scalars().first()

    if centro_treinamento is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Centro de treinamento não encontrado")

    atleta_out = None
    try:
        atleta_out = AtletaSchemaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.dict())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError as e:
        await db_session.rollback()
        if "duplicate key value" in str(e):
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
                                detail=f"Já existe um atleta com o CPF {atleta_in.cpf}")

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro ao criar atleta")

    return atleta_out


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista atletas ordenados por nome",
    response_model=list[AllAthletesSchemaOut]
)
async def query(
    db_session: DatabaseDependency
) -> list[AllAthletesSchemaOut]:
    atletas: list[AllAthletesSchemaOut] = (
        await db_session.execute(select(AtletaModel).order_by(AtletaModel.nome))
    ).scalars().all()

    return atletas


@router.get(
    "/by",
    status_code=status.HTTP_200_OK,
    summary="Busca um atleta por id, cpf ou nome",
    response_model=AtletaSchemaOut
)
async def get(
    db_session: DatabaseDependency,
    id_atleta: UUID4 = Query(None),
    nome: str = Query(None),
    cpf: str = Query(None)
) -> AtletaSchemaOut:
    custom_query = select(AtletaModel)

    if id_atleta:
        custom_query = custom_query.filter_by(id=id_atleta)
    elif cpf:
        custom_query = custom_query.filter_by(cpf=cpf)
    elif nome:
        pattern = f"%{nome}%"
        custom_query = custom_query.filter(AtletaModel.nome.ilike(pattern))

    result = await db_session.execute(custom_query)
    atleta: AtletaSchemaOut = result.scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")

    return atleta


@router.patch(
    "/{id_atleta}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um atleta por id",
    response_model=AtletaSchemaOut
)
async def patch(
    db_session: DatabaseDependency,
    id_atleta: UUID4,
    atleta_patch: AtletaSchemaPatch = Body(...)
) -> AtletaSchemaOut:

    atleta: AtletaSchemaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id_atleta))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")

    atleta_update = atleta_patch.model_dump(exclude_unset=True).items()
    for key, value in atleta_update:
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    "/{id_atleta}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um atleta por id"
)
async def delete(
    db_session: DatabaseDependency,
    id_atleta: UUID4
) -> None:
    atleta: AtletaSchemaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id_atleta))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")

    await db_session.delete(atleta)
    await db_session.commit()
