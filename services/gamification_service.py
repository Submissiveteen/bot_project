from repositories.db import SessionLocal
from repositories.models import User


from datetime import datetime

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
            level_xp_needed = user.level * 100  # TODO: заменить на calc_xp_for_level(user.level) если потребуется динамика
            if user.xp >= level_xp_needed:
                user.xp -= level_xp_needed
                user.level += 1
                leveled_up = True
            else:
                break

        db.commit()

        level_info = get_level_info(user.xp)

        msg = (
            f"{level_info['emoji']} {level_info['title']}\n"
            f"♻️ Переработано: {kg} кг\n"
            f"💰 ECO: {user.eco_balance}\n"
            f"📈 XP: {user.xp}\n"
            f"🏅 Уровень: {user.level}"
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

def get_profile(telegram_id: int) -> str:
    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not user:
            return "❌ Пользователь не найден."

        xp_to_next = user.level * 100 - user.xp  # TODO: заменить на calc_xp_for_level(user.level)
        level_info = get_level_info(user.xp)

        # Прогрессбар XP (5 блоков)
        percent = user.xp / (user.level * 100)
        filled_blocks = int(percent * 5)
        bar = "█" * filled_blocks + "░" * (5 - filled_blocks)

        return (
            f"👤 Профиль:\n"
            f"{level_info['emoji']} {level_info['title']}\n"
            f"🏅 Уровень: {user.level}\n"
            f"📈 XP: {user.xp} / {user.level * 100} {bar}\n"
            f"💰 ECO: {user.eco_balance}\n"
            f"📦 Пластика сдано: {user.plastic_total} кг"
        )
