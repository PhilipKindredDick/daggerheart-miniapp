import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
WEBAPP_URL = os.environ.get('WEBAPP_URL')

if not TOKEN:
    print("Ошибка: BOT_TOKEN не найден!")
    exit(1)

if not WEBAPP_URL:
    print("Ошибка: WEBAPP_URL не найден!")
    exit(1)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🎮 Играть в Daggerheart", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🎭 Добро пожаловать, {user.first_name}!\n\n🎲 Нажмите кнопку для запуска игры:",
        reply_markup=reply_markup
    )

def main():
    """Main function"""
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    
    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()