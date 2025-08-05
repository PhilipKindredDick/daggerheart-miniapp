import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
WEBAPP_URL = os.environ.get('WEBAPP_URL')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Простая команда /start"""
    user = update.effective_user
    
    message = f"🎭 {user.first_name}, играем в Daggerheart!\n\n🎲 Игра: {WEBAPP_URL}"
    
    await update.message.reply_text(message)
    logger.info(f"/start от {user.first_name}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    
    logger.info("🤖 Простой бот запущен!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()