import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')

if not BOT_TOKEN or not WEBAPP_URL:
    logger.error("Не найдены BOT_TOKEN или WEBAPP_URL!")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start - запуск Mini App"""
    user = update.effective_user
    
    keyboard = [[
        InlineKeyboardButton("🎮 Играть в Daggerheart", web_app=WebAppInfo(url=WEBAPP_URL))
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🎭 Привет, {user.first_name}!\n\n🎲 Запускай Daggerheart и создавай своего персонажа!",
        reply_markup=reply_markup
    )

def main():
    """Запуск бота"""
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    logger.info("🤖 Бот запущен!")
    app.run_polling()

if __name__ == '__main__':
    main()