from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler

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

def market(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(f"{item['title']} — {item['price']} ECO", callback_data=f"buy_{key}")]
        for key, item in NFT_CATALOG.items()
    ]
    update.message.reply_text("🛒 NFT-маркет (заглушка):", reply_markup=InlineKeyboardMarkup(keyboard))

def handle_market_purchase(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    item_id = query.data.replace("buy_", "")
    item = NFT_CATALOG.get(item_id)

    if not item:
        query.edit_message_text("❌ Невалидный товар.")
        return

    user_id = query.from_user.id
    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == user_id).first()

        if not user:
            query.edit_message_text("❌ Пользователь не найден.")
            return

        if user.eco_balance < item['price']:
            query.edit_message_text("💸 Недостаточно ECO.")
            return

        user.eco_balance = round(user.eco_balance - item['price'], 2)
        db.add(InventoryItem(user_id=user.id, name=item['title'], description=item['description']))
        db.commit()

        query.edit_message_text(f"✅ Куплено: {item['title']}!\n\n{item['description']}")

def register_market_handler(app):
    app.add_handler(CommandHandler("market", market))
    app.add_handler(CallbackQueryHandler(handle_market_purchase, pattern=r"^buy_"))