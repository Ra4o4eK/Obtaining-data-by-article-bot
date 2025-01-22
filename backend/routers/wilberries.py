from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter

from database.queries import ProductsQueries
from utils import scheduler, get_product_data, update_product_data, ProductRequest


router = APIRouter()


@router.post("/api/v1/products")
async def collecting_data_by_article(product: ProductRequest) -> None:
    artikul = product.artikul

    name, price, rating, total_quantity = get_product_data(artikul)

    query = ProductsQueries()
    db_product = await query.create_product(
        artikul=artikul,
        name=name,
        price=price,
        rating=rating,
        total_quantity=total_quantity
    )

    return {"message": "Данные о товаре успешно сохранены", "product": db_product}


@router.get("/api/v1/subscribe/{artikul}")
async def getting_subscribed(artikul: int) -> None:
    query = ProductsQueries()
    db_product = await query.get_product(artikul)
    name, price, rating, total_quantity = get_product_data(artikul)

    if db_product is not None:
        await query.update_product({
            "artikul": artikul,
            "name": name,
            "price": price,
            "rating": rating,
            "total_quantity": total_quantity,
            "subscribe": True
        })
    else:
        db_product = await query.create_product(
            artikul=artikul,
            name=name,
            price=price,
            rating=rating,
            total_quantity=total_quantity,
            subscribe=True
        )

    scheduler.add_job(
        update_product_data,
        trigger=IntervalTrigger(minutes=30),
        args=artikul,
        id=f"update_product_{artikul}",
        replace_existing=True
    )

    return {"message": f"Подписка на товар {artikul} успешно создана"}
