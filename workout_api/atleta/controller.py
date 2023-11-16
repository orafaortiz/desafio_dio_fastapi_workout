from fastapi import APIRouter, status, Body
from workout_api.atleta.schemas import AtletaSchemaIn
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post("/", summary="Create a new Atleta", status_code=status.HTTP_201_CREATED)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaSchemaIn = Body(...)
):
    pass
