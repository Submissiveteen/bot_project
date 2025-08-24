# services/admin_service.py
from repositories.db import SessionLocal
from repositories.models import User, EcoTransaction


def get_admin_stats() -> str:
    with SessionLocal() as db:
        total_users = db.query(User).count()
        total_eco = round(sum(user.eco_balance for user in db.query(User).all()), 4)
        total_plastic = round(sum(user.plastic_total for user in db.query(User).all()), 2)
        total_tx = db.query(EcoTransaction).count()

        return (
            f"📊 Админ-статистика:\n"
            f"👥 Пользователей: {total_users}\n"
            f"💰 Всего ECO: {total_eco}\n"
            f"♻️ Переработано (всего): {total_plastic} кг\n"
            f"🔁 Переводов ECO: {total_tx}"
        )


def get_top_users(limit: int = 10) -> str:
    with SessionLocal() as db:
        top = (
            db.query(User)
            .order_by(User.eco_balance.desc())
            .limit(limit)
            .all()
        )
        if not top:
            return "Нет данных."

        leaderboard = "🏆 ТОП ECO по пользователям:\n"
        for idx, user in enumerate(top, start=1):
            leaderboard += f"{idx}. ID {user.telegram_id} — {round(user.eco_balance, 2)} ECO\n"
        return leaderboard
