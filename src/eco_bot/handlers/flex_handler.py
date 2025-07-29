from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from repositories.db import SessionLocal
from repositories.models import User
from services.gamification_service import get_level_info
from eco_bot.handlers.mylook_handler import generate_avatar

def flex(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    username = update.effective_user.username or f"user_{user_id}"

    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if not user:
            update.message.reply_text("❌ Пользователь не найден.")
            return

        level_info = get_level_info(user.xp)
        title = user.custom_title or level_info['title']

        caption = (
            f"🔥 @{username} делает флекс!\n"
            f"{level_info['emoji']} {title}\n"
            f"🏅 Уровень: {user.level}\n"
            f"📈 XP: {user.xp}\n"
            f"💰 ECO: {user.eco_balance}\n"
            f"📦 Пластик: {user.plastic_total} кг"
        )

        avatar = generate_avatar(user)
        update.message.reply_photo(photo=avatar, caption=caption)

def register_flex_handler(app):
    app.add_handler(CommandHandler("flex", flex))
