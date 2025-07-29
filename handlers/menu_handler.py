from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("♻ Переработать", callback_data="recycle")],
        [InlineKeyboardButton("📊 Баланс", callback_data="balance"),
         InlineKeyboardButton("🧍 Профиль", callback_data="profile")],
        [InlineKeyboardButton("🏆 Ачивки", callback_data="achievements"),
         InlineKeyboardButton("💸 Перевести", callback_data="sendeco")],
        [InlineKeyboardButton("🧱 Апгрейд", callback_data="upgrade")]
    ]
    return InlineKeyboardMarkup(keyboard)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Ты на дне... но пластик спасёт тебя! ♻️\n\nНажми, чтобы начать путь эко-героя:",
        reply_markup=get_main_menu()
    )

def menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "📋 Главное меню:",
        reply_markup=get_main_menu()
    )

def menu_callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    data = query.data
    if data == "recycle":
        query.edit_message_text("♻ Введите команду `/recycle <кг>` для переработки.", parse_mode='Markdown')
    elif data == "balance":
        query.edit_message_text("💰 Используй `/balance` чтобы узнать счёт.")
    elif data == "profile":
        query.edit_message_text("📈 Используй `/profile` чтобы увидеть свой путь бомжа.")
    elif data == "achievements":
        query.edit_message_text("🏆 Команда `/achievements` покажет твою коллекцию эко-славы.")
    elif data == "sendeco":
        query.edit_message_text("💸 Используй `/sendeco <user_id> <amount>` для перевода.")
    elif data == "upgrade":
        query.edit_message_text("🧱 Используй `/upgrade` если доступен новый уровень.")
    else:
        query.edit_message_text("❓ Неизвестная команда.")

def register_menu_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(menu_callback_handler))
