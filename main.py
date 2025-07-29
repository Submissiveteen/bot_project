import logging
from telegram.ext import Application

from config.config import settings

# Регистраторы хендлеров
from handlers.telegram_handlers import register_handlers
from handlers.menu_handler import register_menu_handlers
from handlers.upgrade_handler import register_upgrade_handlers
from handlers.achievements_handler import register_achievement_handlers
from handlers.flex_handler import register_flex_handler
from handlers.mylook_handler import register_mylook_handler
from handlers.eco_history_handler import register_eco_history_handler
from handlers.market_handler import register_market_handler
from handlers.inventory_handler import register_inventory_handler
from handlers.use_item_handler import register_use_item_handler
from handlers.beg_handler import register_beg_handler
from handlers.events_handler import register_events_handler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    application = Application.builder().token(settings.BOT_TOKEN).build()

    # Регистрация всех фич
    register_handlers(application)                    # базовые команды
    register_menu_handlers(application)              # /start, /menu + inline
    register_upgrade_handlers(application)           # /upgrade
    register_achievement_handlers(application)       # /achievements
    register_flex_handler(application)               # /flex
    register_eco_history_handler(application)        # /eco_history
    register_mylook_handler(application)             # /mylook
    register_market_handler(application)             # /market
    register_inventory_handler(application)          # /inventory
    register_use_item_handler(application)           # /use_item
    register_beg_handler(application)                # /beg
    register_events_handler(application)             # /events

    logger.info("\u2705 Бот запущен.")
    application.run_polling()


if __name__ == "__main__":
    main()