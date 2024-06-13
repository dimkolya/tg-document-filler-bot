import aiogram
import asyncio
import config
from app import db, handler

bot = aiogram.Bot(token=config.TOKEN)
dp = aiogram.Dispatcher()


async def main():
    db.init()
    dp.include_router(handler.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
