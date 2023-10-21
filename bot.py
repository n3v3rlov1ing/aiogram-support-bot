from utils.states import *
from aiogram import Bot, Dispatcher, Router
from handlers.admin import admin_router
from handlers.user import user_router
import asyncio
from utils.config import token
from utils.filters import IsAdmin

async def main():
    bot = Bot(token)
    dp = Dispatcher()
    dp.include_routers(admin_router, user_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())