# utils/keygen.py
from eth_account import Account
from tronpy.keys import PrivateKey


def generate_eth_wallet():
    acct = Account.create()
    return acct.address, acct.key.hex()


def generate_tron_wallet():
    priv = PrivateKey.random()
    return priv.public_key.to_base58check_address(), priv.hex()
