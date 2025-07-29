# check_env.py

from cryptography.fernet import Fernet
from config.config import settings

print("🔍 Проверка .env и KEY_ENCRYPTION_SECRET")

key = settings.KEY_ENCRYPTION_SECRET
print(f"Значение ключа: {key}")
print(f"Длина строки: {len(key)}")

try:
    fernet = Fernet(key)
    print("✅ Ключ валиден и готов к шифрованию")
except Exception as e:
    print("❌ Ошибка инициализации Fernet:", e)
