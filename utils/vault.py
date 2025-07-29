# utils/vault.py
import base64
from config.config import settings
from cryptography.fernet import Fernet
import sqlite3

class KeyVault:
    def __init__(self, db_path="key_storage.db"):
        self.key = settings.KEY_ENCRYPTION_SECRET
        print(f"🔐 Fernet key: {self.key} (length={len(self.key)})")
        self.fernet = Fernet(self.key)
        self.db_path = db_path
        self._init_db()


    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS keys (
                    telegram_id INTEGER PRIMARY KEY,
                    eth_key TEXT,
                    tron_key TEXT
                )
            """)
            conn.commit()

    def store_keys(self, telegram_id: int, eth_priv: str, tron_priv: str):
        encrypted_eth = self.fernet.encrypt(eth_priv.encode()).decode()
        encrypted_tron = self.fernet.encrypt(tron_priv.encode()).decode()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO keys (telegram_id, eth_key, tron_key)
                VALUES (?, ?, ?)
                ON CONFLICT(telegram_id) DO UPDATE SET
                    eth_key=excluded.eth_key,
                    tron_key=excluded.tron_key
            """, (telegram_id, encrypted_eth, encrypted_tron))
            conn.commit()

    def load_keys(self, telegram_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT eth_key, tron_key FROM keys WHERE telegram_id = ?", (telegram_id,))
            row = cur.fetchone()
            if row:
                eth_priv = self.fernet.decrypt(row[0].encode()).decode()
                tron_priv = self.fernet.decrypt(row[1].encode()).decode()
                return eth_priv, tron_priv
            return None
