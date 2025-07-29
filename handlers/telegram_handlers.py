from telegram import Update, InputFile
from telegram.ext import CommandHandler, ContextTypes, Application
from services.wallet_service import get_or_create_wallet
from services.transfer_service import send_crypto
from services.gamification_service import recycle, get_balance, get_profile
from services.sendeco_service import send_eco
from services.admin_service import get_admin_stats, get_top_users
from services.export_service import export_users_to_csv
from config.config import settings
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я EcoBot. Используй /wallet для генерации кошельков.")

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = update.effective_user.id
    wallets = get_or_create_wallet(telegram_id)
    if wallets:
        eth, tron = wallets
        await update.message.reply_text(f"🪪 Ваши кошельки:\nPolygon: {eth}\nTron: {tron}")
    else:
        await update.message.reply_text("❌ Не удалось создать кошельки.")

async def send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 3:
        await update.message.reply_text("❌ Использование: /send <blockchain> <address> <amount>")
        return
    blockchain, address, amount_str = context.args
    try:
        amount = float(amount_str)
        tx_hash = await send_crypto(blockchain, address, amount)
        if tx_hash:
            await update.message.reply_text(f"✅ Транзакция отправлена! TX: {tx_hash}")
        else:
            await update.message.reply_text("❌ Не удалось отправить транзакцию.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def recycle_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("♻️ Использование: /recycle <кг>")
        return
    try:
        kg = float(context.args[0])
        telegram_id = update.effective_user.id
        result = recycle(telegram_id, kg)
        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("❌ Введите число. Пример: /recycle 3.5")

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = update.effective_user.id
    result = get_balance(telegram_id)
    await update.message.reply_text(result)

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = update.effective_user.id
    result = get_profile(telegram_id)
    await update.message.reply_text(result)

async def sendeco_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2:
        await update.message.reply_text("💸 Использование: /sendeco <user_id> <amount>")
        return
    try:
        receiver_id = int(context.args[0])
        amount = float(context.args[1])
        sender_id = update.effective_user.id
        result = send_eco(sender_id, receiver_id, amount)
        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("❌ Неверный формат. Пример: /sendeco 12345678 10")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = update.effective_user.id
    if str(telegram_id) != str(settings.ADMIN_ID):
        await update.message.reply_text("⛔ Нет доступа.")
        return
    result = get_admin_stats()
    await update.message.reply_text(result)

async def top10_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = get_top_users()
    await update.message.reply_text(result)

async def exportcsv_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = update.effective_user.id
    if str(telegram_id) != str(settings.ADMIN_ID):
        await update.message.reply_text("⛔ Нет доступа.")
        return
    path = export_users_to_csv()
    with open(path, "rb") as f:
        await update.message.reply_document(document=InputFile(f, filename=os.path.basename(path)))

def register_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wallet", wallet))
    app.add_handler(CommandHandler("send", send))
    app.add_handler(CommandHandler("recycle", recycle_command))
    app.add_handler(CommandHandler("balance", balance_command))
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(CommandHandler("sendeco", sendeco_command))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("top10", top10_command))
    app.add_handler(CommandHandler("exportcsv", exportcsv_command))
