import os
import logging
import asyncio
from pyrogram import Client, idle
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram.types import ChatMember
from pyromod import listen
from aiohttp import web
from tglogging import TelegramLogHandler

# **Configuration Class**
class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7740228677:AAHqK2f_p8DdYWJcnQazuLPw_H8YHUEUD0w")
    API_ID = int(os.environ.get("API_ID", "23442913"))
    API_HASH = os.environ.get("API_HASH", "864a97e16b4ff7dc65ff5e2d1549b4a2")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    SESSIONS = "./SESSIONS"

    AUTH_USERS = list(map(int, os.environ.get("AUTH_USERS", "7841326954").split(",")))
    GROUPS = list(map(int, os.environ.get("GROUPS", "-1002300391155").split(",")))
    LOG_CH = int(os.environ.get("LOG_CH", "-1002381344447"))

# **Logging Setup**
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
            pending_logs=200000,
        ),
        logging.StreamHandler(),
    ],
)

LOGGER = logging.getLogger(__name__)
LOGGER.info("Live log streaming to Telegram.")

# **Pyrogram Bot Instance**
bot = Client(
    "my_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins"),  # If you have plugins, define them here
)

# **Aiohttp Web Server**
app = web.Application()
routes = web.RouteTableDef()

@routes.get("/")
async def home(request):
    return web.Response(text="Hello, Docker!")

app.add_routes(routes)

# **Run Both the Bot and Web Server**
async def start_services():
    LOGGER.info("Starting Web Server & Bot...")

    # Start Web Server
    PORT = int(os.getenv("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    
    # Start the Bot
    await bot.start()
    LOGGER.info("Bot started successfully!")

    # Keep Running
    await idle()

    # Cleanup on shutdown
    await bot.stop()
    LOGGER.info("Bot stopped!")

# **Run the Main Event Loop**
if __name__ == "__main__":
    asyncio.run(start_services())
