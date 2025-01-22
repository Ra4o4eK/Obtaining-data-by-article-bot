import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
from aiogram.types.bot_command import BotCommand

from config.config import settings
from bot.handlers import router


logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='w'
)

bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
commands = [BotCommand(command="start", description="start")]


async def main() -> None:
    dp.include_routers(router)
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
