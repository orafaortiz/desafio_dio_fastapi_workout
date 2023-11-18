from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, status, Body, HTTPException, Query
from pydantic import UUID4

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaSchemaIn, AtletaSchemaOut, AtletaSchemaPatch
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy import func
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

    try:
        atleta_out = AtletaSchemaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Erro no banco ao criar atleta")

    return atleta_out


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Lista atletas ou busca por ID, CPF ou nome",
    response_model=list[AtletaSchemaOut]
)
async def query(
    db_session: DatabaseDependency,
    id_atleta: UUID4 = Query(None),
    nome: str = Query(None),
    cpf: str = Query(None)
) -> list[AtletaSchemaOut]:
    custom_query = select(AtletaModel)

    if id_atleta:
        custom_query = custom_query.filter_by(id=id_atleta)
    elif cpf:
        custom_query = custom_query.filter_by(cpf=cpf)
    elif nome:
        pattern = f"%{nome}%"
        custom_query = custom_query.filter(AtletaModel.nome.ilike(pattern))

    result = await db_session.execute(custom_query)
    atletas: list[AtletaSchemaOut] = result.scalars().all()

    if not atletas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atleta não encontrado")

    return [AtletaSchemaOut.model_validate(atleta) for atleta in atletas]


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
