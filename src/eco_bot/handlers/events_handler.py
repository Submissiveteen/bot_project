from repositories.db import SessionLocal
from repositories.models import User
from services.gamification_service import calc_rewards_for_recycle, get_level_info
from eco_bot.handlers.mylook_handler import generate_avatar

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

import random

def recycle(telegram_id: int, kg: float) -> str:
    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not user:
            return "❌ Пользователь не найден."

        rewards = calc_rewards_for_recycle(kg)

        user.plastic_total += kg
        user.eco_balance = round(user.eco_balance + rewards["eco"], 4)
        user.xp += rewards["xp"]

        leveled_up = False
        while True:
            level_xp_needed = user.level * 100
            if user.xp >= level_xp_needed:
                user.xp -= level_xp_needed
                user.level += 1
                user.upgrade_available = True
                leveled_up = True
            else:
                break

        db.commit()

        level_info = get_level_info(user.xp)
        phrases = [
            "Ты спас 🐢 от пластикового ада!",
            "Макулатура трепещет перед тобой!",
            "Чистый ты человек, хоть и воняет... 🤢",
            "Пакетики дрожат при звуке твоего имени",
            "💥 Ты переработал, Земля благодарит!"
        ]
        flavor = random.choice(phrases)

        msg = (
            f"{level_info['emoji']} {level_info['title']}\n"
            f"♻️ Переработано: {kg} кг\n"
            f"💰 ECO: {user.eco_balance}\n"
            f"📈 XP: {user.xp}\n"
            f"🏅 Уровень: {user.level}\n"
            f"\n{flavor}"
        )

        if leveled_up:
            msg += "\n🎉 Поздравляем, новый уровень!"

        return msg

def get_balance(telegram_id: int) -> str:
    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not user:
            return "❌ Пользователь не найден."

        return (
            f"💰 ECO: {user.eco_balance}\n"
            f"📦 Переработано: {user.plastic_total} кг"
        )

def get_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = update.effective_user.id

    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not user:
            update.message.reply_text("❌ Пользователь не найден.")
            return

        xp_to_next = user.level * 100 - user.xp
        level_info = get_level_info(user.xp)

        percent = user.xp / (user.level * 100)
        filled_blocks = int(percent * 5)
        bar = "█" * filled_blocks + "░" * (5 - filled_blocks)

        caption = (
            f"👤 Профиль:\n"
            f"{level_info['emoji']} {level_info['title']}\n"
            f"🏅 Уровень: {user.level}\n"
            f"📈 XP: {user.xp} / {user.level * 100} {bar}\n"
            f"💰 ECO: {user.eco_balance}\n"
            f"📦 Пластика сдано: {user.plastic_total} кг"
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏆 Ачивки", callback_data="achievements"),
             InlineKeyboardButton("🎒 Инвентарь", callback_data="inventory")],
            [InlineKeyboardButton("🧱 Апгрейд", callback_data="upgrade")]
        ])

        avatar = generate_avatar(user)
        update.message.reply_photo(photo=avatar, caption=caption, reply_markup=keyboard)
