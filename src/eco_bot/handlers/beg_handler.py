from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from repositories.db import SessionLocal
from repositories.models import User

async def beg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    to_username = context.args[0].replace("@", "") if context.args else None
    from_username = update.effective_user.username
    from_id = update.effective_user.id

    if not to_username:
        await update.message.reply_text("⚠️ Укажи пользователя: /beg @user")
        return

    keyboard = [
        [InlineKeyboardButton(f"💸 Дать 1 ECO @{from_username}", callback_data=f"donate_1_{from_id}")]
    ]
    await update.message.reply_text(
        f"@{to_username}, @{from_username} просит у тебя 1 ECO 🥺",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_donation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from repositories.models import EcoEvent
    from datetime import datetime

    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    amount = float(data[1])
    receiver_id = int(data[2])
    sender_id = query.from_user.id

    try:
        with SessionLocal() as db:
            giver = db.query(User).filter(User.telegram_id == sender_id).first()
            receiver = db.query(User).filter(User.telegram_id == receiver_id).first()

            if not giver or not receiver:
                await query.edit_message_text("❌ Один из пользователей не найден.")
                return

            if giver.eco_balance < amount:
                await query.edit_message_text("💸 Недостаточно ECO.")
                return

            giver.eco_balance -= amount
            receiver.eco_balance += amount

            db.add(EcoEvent(user_id=giver.id, type="transfer", amount=-amount, timestamp=datetime.utcnow()))
            db.add(EcoEvent(user_id=receiver.id, type="receive", amount=amount, timestamp=datetime.utcnow()))

            db.commit()

            await query.edit_message_text(
                f"✅ @{query.from_user.username} подал {amount} ECO @{receiver.custom_title or 'другу'} 🙏"
            )

    except Exception as e:
        await query.edit_message_text(f"❌ Ошибка при передаче ECO: {e}")
