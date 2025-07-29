

```markdown
# ♻️ EcoBot MVP – Telegram Web3-базовый бот

**Цель проекта:**  
Telegram-бот, позволяющий пользователям генерировать криптовалютные кошельки (Polygon и Tron), а также отправлять токены. Предназначен как MVP для будущей экосистемы Web3-геймификации, связанной с переработкой пластика.

---

## 📁 Структура проекта

```

.
├── bot.py                 # Основной entry-point: Telegram-бот
├── registre\_wallet.py     # Генерация и сохранение кошельков (Polygon, Tron)
├── connect\_polygon.py     # Отправка токенов (Polygon реализован, Tron - нет)
├── database.py            # Инициализация структуры SQLite
├── .env                   # Конфигурация токенов, RPC и ключей
├── users.db               # Локальная база данных пользователей
├── test\_wallet.py         # Простой CLI-тест генерации кошельков
├── tets.py                # Ошибочный тест (не используется)

````

---

## 📌 Компоненты и функции

### 1. `bot.py` — Telegram-интерфейс (основной entry-point)

Запускает асинхронного Telegram-бота. Реализует команды:

#### `/start`
- Приветственное сообщение.

#### `/wallet`
- Получает Telegram ID пользователя.
- Вызывает `register_wallet(telegram_id)` из `registre_wallet.py`.
- Возвращает пользователю адреса Polygon и Tron кошельков.

#### `/send <blockchain> <address> <amount>`
- Валидирует входные данные.
- Поддерживает: `polygon`, `tron` (Tron пока не реализован).
- Вызывает `send_crypto(blockchain, address, amount)` из `connect_polygon.py`.
- Возвращает hash транзакции или ошибку.

---

### 2. `registre_wallet.py` — Генерация и регистрация кошельков

#### `generate_wallet()`
- Генерирует Ethereum/Polygon-совместимый адрес:
  - Использует `secrets.token_hex(20)` → `0x`-префикс.

#### `generate_tron_wallet()`
- Генерирует Tron-адрес:
  - Через `tronpy.keys.PrivateKey.random()`

#### `register_wallet(telegram_id)`
- Проверяет, есть ли кошельки в базе по `telegram_id`.
- Если есть — возвращает.
- Если нет:
  - Генерирует ETH и TRON-кошельки.
  - Записывает их в таблицу `users` базы `users.db`.
  - Использует UPSERT по `telegram_id`.

---

### 3. `connect_polygon.py` — Логика отправки токенов

#### Конфигурация:
- Читает из `.env`:
  - `INFURA_URL`, `PRIVATE_KEY`, `SENDER_ADDRESS`
  - `TRON_PRIVATE_KEY`, `TRON_ADDRESS`, `TRON_NODE`

#### `send_crypto(blockchain, to_address, amount)`
- Роутер: отправляет на `send_polygon()` или `send_tron()` (Tron — не реализован)

#### `send_polygon(to_address, amount)`
- Проверяет баланс отправителя.
- Сбор и подпись транзакции (`web3.eth.account.sign_transaction`)
- Отправка через `web3.eth.send_raw_transaction`
- Возвращает `tx_hash`

❗ **Tron**: `send_tron()` упомянута, но не реализована.

---

### 4. `database.py` — Создание таблицы `users`

#### `create_database()`
- Открывает/создаёт `users.db`
- Создаёт таблицу `users`, если не существует:
  - `id`, `telegram_id`, `eth_wallet`, `tron_wallet`
- Добавляет индекс по `telegram_id`

📦 Запускается вручную: `python database.py`

---

### 5. `.env` — Файл конфигурации

Пример содержимого:

```env
BOT_TOKEN=<токен Telegram-бота>

# Polygon
PRIVATE_KEY=<приватный ключ>
INFURA_URL=https://polygon-rpc.com/
SENDER_ADDRESS=0x...

# Tron
TRON_PRIVATE_KEY=<приватный ключ>
TRON_ADDRESS=0x...
TRON_NODE=https://api.trongrid.io
````

---

### 6. `test_wallet.py` — Ручной тест

Пример использования:

```python
from registre_wallet import register_wallet

telegram_id = 123456789
wallets = register_wallet(telegram_id)
print("Созданные кошельки:", wallets)
```

---

### 7. `tets.py` — Ошибочный тест

```python
from wallet_manager import register_wallet  # ❌ Ошибка импорта
```

❗ Удалить или переименовать в корректный тест.

---

## 🛠 Зависимости

```bash
pip install python-telegram-bot
pip install tronpy
pip install web3
pip install python-dotenv
```

---

## ▶️ Запуск

```bash
# Убедитесь, что .env заполнен
# Инициализируйте базу (однократно)
python database.py

# Запуск бота
python bot.py
```

---

## 🧩 TODO / Потенциал расширения

* [ ] Реализовать `send_tron()`
* [ ] Добавить команды `/recycle`, `/balance`, `/profile`
* [ ] Ввести локальную валюту ECO (баланс, XP)
* [ ] Имитация NFT/ачивок
* [ ] Панель администратора для метрик
* [ ] Перевести базу с SQLite на PostgreSQL (в будущем)

---

## 🔒 Безопасность

* Не коммитьте `.env` в репозиторий
* Приватные ключи должны быть зашифрованы в продакшене
* SQLite подходит только для MVP/тестирования

---

## 📃 Лицензия

Проект находится в прототипной стадии и предназначен для демонстрации MVP Web3-интерфейса.

```

---

