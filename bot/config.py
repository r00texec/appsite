import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "0").split(",") if x.strip()]
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "support")
CHANNEL_ID = os.getenv("CHANNEL_ID", "")
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "bot.db")
