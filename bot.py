import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
WEBAPP_URL = os.environ.get('WEBAPP_URL')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start с WebApp"""
    user = update.effective_user
    
    # После настройки WebApp в @BotFather используем WebAppInfo
    keyboard = [
        [InlineKeyboardButton("🎮 Играть в Daggerheart", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🎭 {user.first_name}, запускай игру! 🎲\n\n✨ Игра откроется внутри Telegram",
        reply_markup=reply_markup
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    
    logger.info("🤖 WebApp бот запущен!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()