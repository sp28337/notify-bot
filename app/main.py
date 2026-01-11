import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from app.settings import settings as s

from app.service import register_routes


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        url=f"{s.bot.webhook_url}{s.bot.webhook_path}",
        secret_token=s.bot.webhook_secret,
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(
        token=s.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.startup.register(on_startup)

    app = web.Application()
    app["notify-bot"] = bot

    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=s.bot.webhook_secret,
    )
    webhook_handler.register(app, path=s.bot.webhook_path)

    register_routes(app)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=s.bot.host, port=s.bot.port)


if __name__ == "__main__":
    main()
