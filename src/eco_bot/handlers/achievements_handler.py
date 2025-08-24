from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from repositories.db import SessionLocal
from repositories.models import Achievement, User

def achievements(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            update.message.reply_text("❌ Пользователь не найден.")
            return

        ach_list = db.query(Achievement).filter(Achievement.user_id == user.id).all()

        if not ach_list:
            update.message.reply_text("🏆 У тебя пока нет достижений. Перерабатывай пластик!")
            return

        text = "🏅 Твои достижения:\n\n"
        for ach in ach_list:
            text += f"• {ach.title} ({ach.awarded_at.strftime('%Y-%m-%d')})\n"

        update.message.reply_text(text)

def register_achievement_handlers(app):
    app.add_handler(CommandHandler("achievements", achievements))
