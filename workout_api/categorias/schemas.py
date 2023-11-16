from workout_api.contrib.schemas import BaseSchema
from typing import Annotated
from pydantic import Field, UUID4


class CategoriaSchemaIn(BaseSchema):
    nome: Annotated[str, Field(max_length=50, description="Nome da categoria", example="Scale")]


class CategoriaSchemaOut(CategoriaSchemaIn):
    id: Annotated[UUID4, Field(description="Identificador da categoria")]
