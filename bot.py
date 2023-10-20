from utils.states import *
from aiogram import Bot, Dispatcher, Router
from handlers.handlers import handler
import asyncio
from utils.config import token

async def main():
    bot = Bot(token)
    dp = Dispatcher()
    dp.include_router(handler)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())