import requests
import logging

from pydantic import BaseModel
from fastapi import HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from database.queries import ProductsQueries
from config.config import settings


class ProductRequest(BaseModel):
    artikul: int


class Token(BaseModel):
    access_token: str
    token_type: str


jobstores = {
    'default': SQLAlchemyJobStore(url=settings.get_db_url_for_scheduler())
}
scheduler = AsyncIOScheduler(jobstores=jobstores)


async def get_product_data(artikul: int) -> tuple:
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"

    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Товар не найден на Wildberries")

    data = response.json()
    product_data = data.get("data", {}).get("products", [])
    if not product_data:
        raise HTTPException(status_code=404, detail="Товар не найден")

    product_info = product_data[0]
    name = product_info.get("name")
    price = product_info.get("salePriceU") / 100
    rating = product_info.get("rating")
    total_quantity = product_info.get("totalQuantity")

    return name, price, rating, total_quantity


async def update_product_data(artikul: int):
    query = ProductsQueries()
    try:
        name, price, rating, total_quantity = await get_product_data(artikul)

        db_product = await query.get_product(artikul)
        if db_product is not None:
            await query.update_product({
                "artikul": artikul,
                "name": name,
                "price": price,
                "rating": rating,
                "total_quantity": total_quantity,
                "subscribe": True
            })
    except Exception as e:
        logging.error(f"Ошибка при обновлении данных для товара {artikul}: {e}")
