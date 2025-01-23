from aiogram import types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.router import Router
from aiogram.filters.command import Command

from database.queries import ProductsQueries


router = Router()


def first_step():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Получить данные по товару")]],
        resize_keyboard=True,
    )


@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Добро пожаловать, этот бот позволяет получить данные товара по артикулу",
        reply_markup=first_step(),
    )


@router.message(F.text == "Получить данные по товару")
async def button_pressed(message: types.Message):
    await message.answer("Введите артикул товара")


@router.message()
async def give_info(message: types.Message):
    try:
        artikul = int(message.text)
        query = ProductsQueries()
        product = await query.get_product(artikul)
        await message.answer(
            f"Данные по товару:\n\nНазвание: {product.name}\nЦена: {product.price} р.\nРейтинг: {product.raiting}\nОбщее количество: {product.total_quantity}"
        )
    except ValueError:
        await message.answer("Введите корректный артикул")
