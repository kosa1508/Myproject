from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key = True)
    hotel_id: Mapped[int] = mapped_column(ForeignKeyConstraint("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]