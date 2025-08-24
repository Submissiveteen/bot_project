# services/wallet_service.py
from repositories.wallet_repository import WalletRepository
from utils.keygen import generate_eth_wallet, generate_tron_wallet
from utils.vault import KeyVault


def get_or_create_wallet(telegram_id: int):
    repo = WalletRepository()
    vault = KeyVault()

    wallet = repo.get_wallet(telegram_id)
    if wallet:
        return wallet

    eth_wallet, eth_priv = generate_eth_wallet()
    tron_wallet, tron_priv = generate_tron_wallet()

    repo.save_wallet(telegram_id, eth_wallet, tron_wallet)
    vault.store_keys(telegram_id, eth_priv, tron_priv)

    return eth_wallet, tron_wallet
