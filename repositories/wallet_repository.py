# repositories/wallet_repository.py
from sqlalchemy.orm import Session
from repositories.db import SessionLocal
from repositories.models import User

class WalletRepository:
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_wallet(self, telegram_id: int):
        user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            return user.eth_wallet, user.tron_wallet
        return None

    def save_wallet(self, telegram_id: int, eth_wallet: str, tron_wallet: str):
        user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            user = User(
                telegram_id=telegram_id,
                eth_wallet=eth_wallet,
                tron_wallet=tron_wallet,
            )
            self.db.add(user)
        else:
            user.eth_wallet = eth_wallet
            user.tron_wallet = tron_wallet
        self.db.commit()
