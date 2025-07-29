from eco_bot.repositories.wallet_repository import WalletRepository
from utils.vault import KeyVault
from eco_bot.repositories.models import User

def test_wallet_creation():
    test_id = 999999
    repo = WalletRepository()
    vault = KeyVault()

    # Очистка: удалить пользователя если уже есть
    repo.db.query(User).filter_by(telegram_id=test_id).delete()
    repo.db.commit()

    # Сохранить и получить
    repo.save_wallet(test_id, "test_eth", "test_tron")
    eth, tron = repo.get_wallet(test_id)

    assert eth == "test_eth"
    assert tron == "test_tron"
