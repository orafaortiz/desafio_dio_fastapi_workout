from typing import Annotated
from pydantic import Field, UUID4
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoSchemaIn(BaseSchema):
    nome: Annotated[str, Field(max_length=20, description="Nome do centro de treinamento", example="CT King")]
    endereco: Annotated[str, Field(max_length=60, description="Endereço do centro de treinamento", example="Rua 1, 123")]
    proprietario: Annotated[str, Field(max_length=30, description="Nome do proprietário do centro de treinamento", example="João")]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(max_length=20, description="Nome do centro de treinamento", example="CT King")]


class CentroTreinamentoSchemaOut(CentroTreinamentoSchemaIn):
    id: Annotated[UUID4, Field(description="Identificador único do centro de treinamento")]
