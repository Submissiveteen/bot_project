# services/transfer_service.py

async def send_crypto(blockchain: str, address: str, amount: float) -> str:
    """
    Фейковая реализация отправки криптовалюты.
    Возвращает псевдо-транзакцию для теста /send команды.
    """
    return f"mock_tx_hash_for_{blockchain}_{address}_{amount}"
