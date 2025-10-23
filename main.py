import os
import logging
import asyncio
import redis.asyncio as aioredis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv
from app.handlers import router
from app.database.models import async_main

load_dotenv()
logging.basicConfig(level=logging.INFO)

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "supersecret")

bot = Bot(
    token=os.getenv("TG_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота 🚀"),
        BotCommand(command="report", description="Жалоба 🚫"),
        BotCommand(command="profile", description="Моя ссылка 👤"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())

async def on_startup(app: web.Application):
    logging.info("Bot startup...")
    await set_bot_commands(bot)
    await async_main()

async def on_shutdown(app: web.Application):
    logging.info("Bot shutdown...")

async def create_app():
    redis = await aioredis.from_url(  # you're ip
    "redis://"
)
    dp = Dispatcher(storage=RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True)))
    dp.include_router(router)

    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    return app

if __name__ == '__main__':
    web.run_app(asyncio.run(create_app()), host='0.0.0.0', port=int(os.getenv("PORT", 8080)))


