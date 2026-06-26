import asyncio
import logging
import ssl
import os
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import init_db
from middlewares.user_middleware import UserMiddleware
from handlers import start, catalog, cart, cabinet, admin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

CA_BUNDLE = "/root/.ccr/ca-bundle.crt"


class ProxyAwareSession(AiohttpSession):
    """Overrides session creation to trust the proxy MITM CA and honour HTTPS_PROXY."""

    async def create_session(self) -> aiohttp.ClientSession:
        if self._should_reset_connector:
            await self.close()
        if self._session is None or self._session.closed:
            ssl_ctx = (
                ssl.create_default_context(cafile=CA_BUNDLE)
                if os.path.exists(CA_BUNDLE)
                else True
            )
            connector = aiohttp.TCPConnector(ssl=ssl_ctx)
            self._session = aiohttp.ClientSession(
                connector=connector,
                trust_env=True,
                headers={"User-Agent": "aiogram/3"},
            )
            self._should_reset_connector = False
        return self._session


async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не задан! Скопируйте .env.example в .env и заполните.")
        return

    await init_db()
    logger.info("База данных инициализирована.")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=ProxyAwareSession(),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())

    dp.include_router(start.router)
    dp.include_router(catalog.router)
    dp.include_router(cart.router)
    dp.include_router(cabinet.router)
    dp.include_router(admin.router)

    logger.info("Бот запущен. Ожидание сообщений...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
