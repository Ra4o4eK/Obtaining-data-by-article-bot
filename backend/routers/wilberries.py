from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter, Depends

from database.queries import ProductsQueries
from utils import get_product_data, update_product_data, ProductRequest
from utils import scheduler
from jwt import get_current_token


router = APIRouter()


@router.post("/api/v1/products")
async def collecting_data_by_article(
    product: ProductRequest, token_payload: dict = Depends(get_current_token)
) -> None:
    artikul = product.artikul

    name, price, raiting, total_quantity = await get_product_data(artikul)

    query = ProductsQueries()
    db_product = await query.create_product(
        artikul=artikul,
        name=name,
        price=price,
        raiting=raiting,
        total_quantity=total_quantity,
    )

    return db_product


@router.get("/api/v1/subscribe/{artikul}")
async def getting_subscribed(
    artikul: int, token_payload: dict = Depends(get_current_token)
) -> None:
    query = ProductsQueries()
    db_product = await query.get_product(artikul)
    name, price, raiting, total_quantity = await get_product_data(artikul)

    if db_product is not None:
        await query.update_product(
            artikul,
            {
                "name": name,
                "price": price,
                "raiting": raiting,
                "total_quantity": total_quantity,
                "subscribe": True,
            },
        )
    else:
        db_product = await query.create_product(
            artikul=artikul,
            name=name,
            price=price,
            raiting=raiting,
            total_quantity=total_quantity,
            subscribe=True,
        )
    scheduler.add_job(
        update_product_data,
        trigger=IntervalTrigger(minutes=30),
        args=(artikul,),
        id=f"update_product_{artikul}",
        replace_existing=True,
    )

    return {"message": f"Подписка на товар {artikul} успешно создана"}
