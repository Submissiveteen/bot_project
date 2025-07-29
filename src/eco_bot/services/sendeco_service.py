# services/sendeco_service.py
from repositories.db import SessionLocal
from repositories.models import User, EcoTransaction


def send_eco(sender_telegram_id: int, receiver_telegram_id: int, amount: float) -> str:
    if amount <= 0:
        return "❌ Сумма должна быть положительной."

    with SessionLocal() as db:
        sender = db.query(User).filter(User.telegram_id == sender_telegram_id).first()
        receiver = db.query(User).filter(User.telegram_id == receiver_telegram_id).first()

        if not sender or not receiver:
            return "❌ Отправитель или получатель не найден."

        if sender.eco_balance < amount:
            return "❌ Недостаточно средств."

        sender.eco_balance -= amount
        receiver.eco_balance += amount

        tx = EcoTransaction(
            sender_id=sender.id,
            receiver_id=receiver.id,
            amount=amount
        )
        db.add(tx)
        db.commit()

        return (
            f"✅ Перевод {amount} ECO завершён.\n"
            f"От: {sender.telegram_id}\n"
            f"Кому: {receiver.telegram_id}"
        )
