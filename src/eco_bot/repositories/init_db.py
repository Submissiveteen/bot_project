# repositories/init_db.py
from repositories.db import engine
from repositories.models import Base

# Инициализация схемы базы данных (однократный запуск)
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ База данных инициализирована.")
