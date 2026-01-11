import logging

from aiogram import Bot
from aiohttp import web
from settings import settings as s

logger = logging.getLogger(__name__)


async def send_notification(request: web.Request) -> web.Response:
    bot: Bot = request.app["notify-bot"]

    data = await request.json()
    message = data.get("message")

    try:
        await bot.send_message(chat_id=s.bot.target_chat_id, text=message)
        return web.json_response({"ok": True})
    except Exception as e:
        logger.exception("Telegram send failed")
        return web.json_response(
            {"error": str(e)},
            status=500,
        )


async def ping(request: web.Request) -> web.Response:
    bot: Bot = request.app["notify-bot"]
    try:
        info = await bot.get_me()
        return web.json_response({"ok": True, "bot": info.username})
    except Exception as e:
        logger.exception("Bot ping failed")
        return web.json_response({"ok": False, "error": str(e)}, status=503)


def register_routes(app: web.Application) -> None:
    app.router.add_post("/notify-bot/send-notification", send_notification)
    app.router.add_get("/notify-bot/ping", ping)
