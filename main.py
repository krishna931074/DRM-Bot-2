import os
import logging
import asyncio
from aiohttp import web
from pyrogram import Client, idle
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatMember
import tgcrypto
from pyromod import listen
from tglogging import TelegramLogHandler

# Define prefixes to fix the import error
prefixes = ["/", "!"]

# Config
class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_ID = int(os.environ.get("API_ID", "23442913"))
    API_HASH = os.environ.get("API_HASH", "864a97e16b4ff7dc65ff5e2d1549b4a2")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    SESSIONS = "./SESSIONS"
    AUTH_USERS = os.environ.get("AUTH_USERS", "7841326954").split(',')
    AUTH_USERS = [int(user) for user in AUTH_USERS]

    GROUPS = os.environ.get("GROUPS", "1002300391155").split(',')
    GROUPS = [int(group) for group in GROUPS]

    LOG_CH = os.environ.get("LOG_CH", "-1002381344447")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        TelegramLogHandler(
            token=Config.BOT_TOKEN,
            log_chat_id=Config.LOG_CH,
            update_interval=2,
            minimum_lines=1,
            pending_logs=200000
        ),
        logging.StreamHandler()
    ]
)
LOGGER = logging.getLogger(__name__)
LOGGER.info("Live log streaming to Telegram.")

# Web Server
app = web.Application()
routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Hello, Docker!")

app.add_routes(routes)
PORT = int(os.getenv("PORT", '8080'))
web.run_app(app, host="0.0.0.0", port=8080)
    
async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await bot.polling()  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
    

