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
    HOST_NAME = ('bb219-75-27-16.singnet.com.sg')
    AUTH_USERS = os.environ.get("AUTH_USERS", "7841326954").split(',')
    AUTH_USERS = [int(user) for user in AUTH_USERS]

    GROUPS = os.environ.get("GROUPS", "-1002300391155").split(',')
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
PORT = int(os.getenv("PORT", '9506'))

# Start Bot
bot = Client("bot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

async def start_services():
    LOGGER.info("Starting Web Server & Bot...")
    await bot.start()
    web.run_app(app, host="219.75.27.16", port=9506)
    await idle()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(start_services())
