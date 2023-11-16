from typing import Annotated
from pydantic import Field, PositiveFloat
from workout_api.contrib.schemas import BaseSchema
from workout_api.contrib.schemas import OutMixin


class AtletaSchema(BaseSchema):
    nome: Annotated[str, Field(max_length=100, description="Nome do atleta", example="João da Silva")]
    cpf: Annotated[str, Field(max_length=11, description="CPF do atleta", example="12345678900")]
    idade: Annotated[int, Field(description="Idade do atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=75.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.75)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]


class AtletaSchemaIn(AtletaSchema):
    pass


class AtletaSchemaOut(AtletaSchema, OutMixin):
    pass