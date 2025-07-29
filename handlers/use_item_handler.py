from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from repositories.db import SessionLocal
from repositories.models import User, InventoryItem, EcoEvent

async def use_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if not args:
        if update.message:
            await update.message.reply_text("⚠️ Укажи название предмета: /use_item <название>")
        return

    item_name = " ".join(args).strip().lower()

    try:
        with SessionLocal() as db:
            user = db.query(User).filter(User.telegram_id == user_id).first()
            if not user:
                if update.message:
                    await update.message.reply_text("❌ Пользователь не найден.")
                return

            item = db.query(InventoryItem).filter(
                InventoryItem.user_id == user.id,
                InventoryItem.name.ilike(f"%{item_name}%")
            ).first()

            if not item:
                if update.message:
                    await update.message.reply_text("🎒 У тебя нет такого предмета.")
                return

            if "повелитель" in item.name.lower():
                user.custom_title = "Повелитель Пластика"
                msg = "👑 Теперь ты — Повелитель Пластика!"
            elif "eco" in item.name.lower():
                user.custom_title = "Эко-Воин"
                msg = "🌱 Теперь ты — Эко-Воин!"
            else:
                msg = "✅ Ты использовал предмет, но ничего не произошло... пока что."

            db.delete(item)

            # Логирование использования
            db.add(EcoEvent(user_id=user.id, type="use_item", amount=0, timestamp=datetime.utcnow()))

            db.commit()
            db.refresh(user)

            if update.message:
                await update.message.reply_text(msg)

    except Exception as e:
        if update.message:
            await update.message.reply_text(f"❌ Ошибка: {e}")
