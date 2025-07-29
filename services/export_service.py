# services/export_service.py
import csv
import os
from datetime import datetime
from repositories.db import SessionLocal
from repositories.models import User


def export_users_to_csv(dir_path: str = "exports") -> str:
    os.makedirs(dir_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(dir_path, f"users_{timestamp}.csv")

    with SessionLocal() as db, open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["telegram_id", "eco_balance", "plastic_total", "xp", "level"])
        for user in db.query(User).all():
            writer.writerow([
                user.telegram_id,
                round(user.eco_balance, 4),
                round(user.plastic_total, 2),
                user.xp,
                user.level,
            ])

    return file_path
