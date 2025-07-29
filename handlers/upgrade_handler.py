from telegram import Update
from telegram.ext import ContextTypes
from repositories.db import SessionLocal
from repositories.models import User

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from repositories.models import EcoEvent
    from datetime import datetime

    user_id = update.effective_user.id

    try:
        with SessionLocal() as db:
            user = db.query(User).filter(User.telegram_id == user_id).first()
            if not user:
                await update.message.reply_text("❌ Пользователь не найден.")
                return

            if not user.upgrade_available:
                await update.message.reply_text("🔒 Пока нет доступных улучшений.")
                return

            user.upgrade_available = False
            user.eco_balance += 5
            user.xp_multiplier += 0.25
            db.add(EcoEvent(user_id=user.id, type="upgrade", amount=5, timestamp=datetime.utcnow()))
            db.commit()

            await update.message.reply_text(
                "🎉 Улучшение применено!\n💰 +5 ECO\n⚡ XP множитель увеличен!"
            )

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при апгрейде: {e}")
