from sqlalchemy import BigInteger, DECIMAL, Boolean
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


class Product(Base):
    artikul: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str]
    price: Mapped[float] = mapped_column(DECIMAL)
    raiting: Mapped[float] = mapped_column(DECIMAL)
    total_quantity: Mapped[int] = mapped_column(BigInteger)
    subscribe: Mapped[bool] = mapped_column(Boolean, default=False)
