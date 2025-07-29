import os
from dotenv import load_dotenv

load_dotenv()  # Подгружаем переменные из .env


class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DB_PATH = os.getenv("DB_PATH", "users.db")

    KEY_ENCRYPTION_SECRET = os.getenv("KEY_ENCRYPTION_SECRET")
    ADMIN_ID = int(os.getenv("ADMIN_ID"))

    # Optional Web3 settings (пока не используются напрямую)
    INFURA_URL = os.getenv("INFURA_URL", "https://polygon-rpc.com/")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
    TRON_PRIVATE_KEY = os.getenv("TRON_PRIVATE_KEY")
    TRON_ADDRESS = os.getenv("TRON_ADDRESS")
    TRON_NODE = os.getenv("TRON_NODE", "https://api.trongrid.io")


settings = Settings()