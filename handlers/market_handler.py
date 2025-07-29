from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from repositories.db import SessionLocal
from repositories.models import User, InventoryItem

NFT_CATALOG = {
    "eco_badge": {
        "title": "🌱 ECO-Бейдж",
        "description": "Символ любви к переработке",
        "price": 5.0
    },
    "plastic_god": {
        "title": "👑 Повелитель Пластика",
        "description": "Выдал 100 кг!",
        "price": 20.0
    }
}

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{item['title']} — {item['price']} ECO", callback_data=f"buy_{key}")]
        for key, item in NFT_CATALOG.items()
    ]
    await update.message.reply_text("🛒 NFT-маркет:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_market_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from repositories.models import EcoEvent
    from datetime import datetime

    query = update.callback_query
    await query.answer()

    item_id = query.data.replace("buy_", "")
    item = NFT_CATALOG.get(item_id)
    if not item:
        await query.edit_message_text("❌ Невалидный товар.")
        return

    user_id = query.from_user.id

    try:
        with SessionLocal() as db:
            user = db.query(User).filter(User.telegram_id == user_id).first()
            if not user:
                await query.edit_message_text("❌ Пользователь не найден.")
                return

            if user.eco_balance < item['price']:
                await query.edit_message_text("💸 Недостаточно ECO.")
                return

            user.eco_balance = round(user.eco_balance - item['price'], 2)

            new_item = InventoryItem(
                user_id=user.id,
                name=item["title"],
                description=item["description"]
            )
            db.add(new_item)
            db.add(EcoEvent(user_id=user.id, type="buy", amount=item['price'], timestamp=datetime.utcnow()))
            db.commit()

            await query.edit_message_text(f"✅ Ты купил {item['title']}!")

    except Exception as e:
        await query.edit_message_text(f"❌ Ошибка при покупке: {e}")
