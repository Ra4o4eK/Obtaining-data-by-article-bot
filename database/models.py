from sqlalchemy import BigInteger, DECIMAL, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Product():
    __tablename__ = "Products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    article: Mapped[int] = mapped_column(BigInteger)
    price: Mapped[float] = mapped_column(DECIMAL)
    raiting: Mapped[float] = mapped_column(DECIMAL)
    total_quantity: Mapped[int] = mapped_column(BigInteger)
    scheduled: Mapped[bool] = mapped_column(Boolean, default=False)
