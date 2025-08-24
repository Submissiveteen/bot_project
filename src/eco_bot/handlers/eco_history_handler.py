from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from repositories.db import SessionLocal
from repositories.models import User, EcoEvent

def eco_history(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            update.message.reply_text("❌ Пользователь не найден.")
            return

        events = db.query(EcoEvent).filter(EcoEvent.user_id == user.id).order_by(EcoEvent.timestamp.desc()).limit(10).all()

        if not events:
            update.message.reply_text("📭 История пуста. Начни с переработки!")
            return

        text = "📜 Последние действия:\n\n"
        for e in events:
            text += f"[{e.timestamp.strftime('%Y-%m-%d %H:%M')}] {e.type}: {e.amount} ECO\n"

        update.message.reply_text(text)

def register_eco_history_handler(app):
    app.add_handler(CommandHandler("eco_history", eco_history))
