import logging
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')

if not BOT_TOKEN:
    logger.error("BOT_TOKEN не найден!")
    exit(1)
    
if not WEBAPP_URL:
    logger.error("WEBAPP_URL не найден!")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start - запуск Mini App"""
    try:
        user = update.effective_user
        
        keyboard = [[
            InlineKeyboardButton("🎮 Играть в Daggerheart", web_app=WebAppInfo(url=WEBAPP_URL))
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = f"🎭 Привет, {user.first_name}!\n\n🎲 Запускай Daggerheart и создавай своего персонажа!"
        
        await update.message.reply_text(
            message,
            reply_markup=reply_markup
        )
        
        logger.info(f"Пользователь {user.first_name} ({user.id}) запустил бота")
        
    except Exception as e:
        logger.error(f"Ошибка в start: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуйте позже.")

def main():
    """Запуск бота"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        
        logger.info("🤖 Бот Daggerheart запущен!")
        
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        exit(1)

if __name__ == '__main__':
    main()