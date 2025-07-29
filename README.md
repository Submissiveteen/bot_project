# ♻️ EcoBot — Web3 Telegram Бот для Экомотивации

**EcoBot** — это Telegram-бот, который поощряет переработку пластика, отслеживает прогресс пользователя через XP и уровни, и использует шифрование и Web3-кошельки для взаимодействия с Polygon и Tron.

---

## 🚀 Основной функционал

* 🪪 Генерация Polygon/Tron кошельков (автоматически, реальные ключи)
* ♻️ Переработка пластика → ECO токены (внутренняя мотивационная валюта)
* 📈 XP + уровни, мотивация через геймификацию
* 💸 ECO-переводы между пользователями (`/sendeco`)
* 🏆 `/top10` лидерборд
* 📊 `/admin`, `/exportcsv` — статистика + CSV-экспорт
* 🔐 Приватные ключи шифруются через `Fernet`

---

## 🧱 Логика работы (по функциям)

### 🔐 `/wallet`

* Проверяет наличие пользователя по telegram\_id
* Если нет: генерирует `eth_priv` и `tron_priv`

  * `eth_wallet` — через `secrets + eth_account`
  * `tron_wallet` — через `tronpy`
* Приватные ключи шифруются и сохраняются в `key_storage.db`
* Возвращаются только открытые адреса

### ♻️ `/recycle <кг>`

* Увеличивает `eco_balance` на переданное значение
* +XP: `kg * 10`, с учётом левела (`xp >= level * 100` → уровень повышается)
* Возвращает прогресс + сообщение о повышении уровня, если есть

### 🧾 `/balance`, `/profile`

* Возвращают `eco_balance`, `plastic_total`, XP и прогресс до следующего уровня

### 💸 `/sendeco <user_id> <amount>`

* Проверка баланса
* Перевод ECO между пользователями в БД
* Возвращает результат перевода (с amount и ID получателя)

### 👑 `/admin`, `/top10`, `/exportcsv`

* `/admin`: считает общее количество пользователей, суммарные показатели
* `/top10`: топ пользователей по ECO
* `/exportcsv`: создаёт `exports/users_export.csv` с таблицей всех пользователей

---

## 🔧 Заглушки и mock-функции

### 📦 `transfer_service.py`

```python
async def send_crypto(blockchain: str, address: str, amount: float) -> str:
    return f"mock_tx_hash_for_{blockchain}_{address}_{amount}"
```

* Используется командой `/send`
* Пока что **не производит настоящих транзакций**
* Возвращает фиктивный `tx_hash`

> В будущем можно реализовать через `web3.py` (Polygon) и `tronpy` (Tron)

---

## 🏗 Структура проекта

```bash
project/
├── main.py                  # Точка входа
├── .env                    # Конфигурация токенов и ключей
├── config/                 # Конфигурация из .env
├── handlers/               # Telegram-команды
├── services/               # Логика бота: wallet, gamification, admin
├── repositories/           # БД, ORM, init_db
├── utils/                  # Шифрование и keyvault
├── tests/                  # Pytest юнит-тесты
├── scripts/                # Утилиты, генераторы, отладка
├── exports/                # CSV-файлы выгрузки
├── requirements.txt
```

---

## ⚙️ Установка

```bash
# Клонирование проекта и установка зависимостей
pip install -r requirements.txt

# Настройка .env файла
cp .env.example .env

# Создание базы данных
python -m repositories.init_db

# Запуск бота
python main.py
```

---

## 🔐 Пример .env

```env
BOT_TOKEN=your_bot_token
KEY_ENCRYPTION_SECRET=rXIML9kuYqZxHCoWBDeDMzee-cYogTeD7zKK0qtMWx8=
ADMIN_ID=123456789
```

---

## 🧠 Архитектура

* `main.py` → инициализация `telegram.ext.Application`
* `handlers/telegram_handlers.py` → регистрация команд `/wallet`, `/recycle`, `/balance`, `/admin`, ...
* `services/` → бизнес-логика (`wallet_service`, `gamification_service`, `sendeco_service`, `export_service`)
* `repositories/` → ORM-модели (`User`), инициализация базы, доступ к SQLite
* `utils/vault.py` → безопасное шифрование приватных ключей

---

## 🧪 Тестирование

```bash
pytest -v
```

> Покрытие включает работу с Vault, WalletService, и базовые интеграции.

---

## 📦 Поддерживаемые команды Telegram

| Команда        | Назначение                                |
| -------------- | ----------------------------------------- |
| `/start`       | Приветствие                               |
| `/wallet`      | Генерация кошельков                       |
| `/recycle 3.5` | Получить ECO и XP за переработку          |
| `/balance`     | Посмотреть баланс ECO и вес               |
| `/profile`     | Уровень, XP и прогресс                    |
| `/sendeco`     | Перевод ECO между пользователями          |
| `/top10`       | ТОП пользователей по ECO                  |
| `/admin`       | Статистика админа                         |
| `/exportcsv`   | CSV-файл со всеми пользователями (ECO/XP) |

---

## 🛡 Безопасность

* Приватные ключи шифруются с `cryptography.Fernet`
* Хранятся в SQLite `key_storage.db`
* `KEY_ENCRYPTION_SECRET` обязателен
* `ADMIN_ID` защищает команды `/admin`, `/exportcsv`

---

## 📈 Будущее

* `eco_model.json` — конфиг XP и левелов
* NFT `/achievements` (награды за переработку)
* Интеграция с DAO и веб-интерфейс аналитики
* Деплой на Heroku / Docker / AWS Lambda

---

## 👨‍💻 Авторы

Разработка, архитектура и безопасность: @yourname
