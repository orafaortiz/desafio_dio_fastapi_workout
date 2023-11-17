from workout_api.contrib.models import BaseModel
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AtletaModel(BaseModel):
    __tablename__ = "atletas"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    categoria: Mapped['CategoriaModel'] = relationship(back_populates="atleta", lazy="selectin")
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.pk_id"), nullable=False)

    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(back_populates="atleta", lazy="selectin")
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey("centros_treinamento.pk_id"))
