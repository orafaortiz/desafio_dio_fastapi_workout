from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.contrib.schemas import BaseSchema
from workout_api.contrib.schemas import OutMixin
from workout_api.categorias.schemas import CategoriaSchemaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta


class AtletaSchema(BaseSchema):
    nome: Annotated[str, Field(max_length=100, description="Nome do atleta", example="João da Silva")]
    cpf: Annotated[str, Field(max_length=11, description="CPF do atleta", example="12345678900")]
    idade: Annotated[int, Field(description="Idade do atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=75.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.75)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaSchemaIn, Field(description="Categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]


class AtletaSchemaIn(AtletaSchema):
    pass


class AtletaSchemaOut(AtletaSchema, OutMixin):
    pass


class AtletaSchemaPatch(BaseSchema):
    nome: Annotated[Optional[str], Field(None, max_length=100, description="Nome do atleta", example="João da Silva")]
    cpf: Annotated[Optional[str], Field(None, max_length=11, description="CPF do atleta", example="12345678900")]
    idade: Annotated[Optional[int], Field(None, description="Idade do atleta", example=25)]
    peso: Annotated[Optional[PositiveFloat], Field(None, description="Peso do atleta", example=75.5)]
    altura: Annotated[Optional[PositiveFloat], Field(None, description="Altura do atleta", example=1.75)]
    sexo: Annotated[Optional[str], Field(None, description="Sexo do atleta", example="M", max_length=1)]
    categoria: Annotated[Optional[CategoriaSchemaIn], Field(None, description="Categoria do atleta")]
    centro_treinamento: Annotated[Optional[CentroTreinamentoAtleta], Field(
        None, description="Centro de treinamento do atleta")]


class AllAthletesSchemaOut(BaseSchema):
    nome: Annotated[str, Field(max_length=100, description="Nome do atleta", example="João da Silva")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]
    categoria: Annotated[CategoriaSchemaIn, Field(description="Categoria do atleta")]
