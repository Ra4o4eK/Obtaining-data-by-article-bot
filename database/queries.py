from sqlalchemy import select, update

from database.models import Product
from database.database import async_session_maker


class ProductsQueries:
    def __init__(self):
        self.session_factory = async_session_maker

    async def create_product(
        self,
        name: str,
        artikul: int,
        price: float,
        raiting: float,
        total_quantity: int,
        subscribe: bool = False
    ) -> Product:
        async with self.session_factory() as session:
            async with session.begin():
                product = Product(
                    name=name,
                    artikul=artikul,
                    price=price,
                    raiting=raiting,
                    total_quantity=total_quantity,
                    subscribe=subscribe
                )
                session.add(product)
                return product

    async def get_product(
        self,
        artikul: int
    ) -> Product | None:
        async with self.session_factory() as session:
            async with session.begin():
                product = await session.execute(
                    select(Product).
                    where(Product.artikul == artikul))
                result = product.scalar()
                return result

    async def update_product(
        self,
        artikul: int,
        params: dict
    ) -> None:
        async with self.session_factory() as session:
            async with session.begin():
                await session.execute(
                    update(Product).
                    where(Product.artikul == artikul).
                    values(params))
