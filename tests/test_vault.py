# tests/test_vault.py
import pytest
from utils.vault import KeyVault


def test_key_vault_roundtrip():
    vault = KeyVault("test_keys.db")
    telegram_id = 424242
    eth_priv = "0xABCDEF0123456789"
    tron_priv = "a1b2c3d4e5f6"

    vault.store_keys(telegram_id, eth_priv, tron_priv)
    loaded = vault.load_keys(telegram_id)

    assert loaded is not None
    eth_out, tron_out = loaded
    assert eth_out == eth_priv
    assert tron_out == tron_priv
