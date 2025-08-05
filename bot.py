import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
WEBAPP_URL = os.environ.get('WEBAPP_URL')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🎮 Играть в Daggerheart", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🎭 Добро пожаловать, {user.first_name}, 🎲 Нажмите кнопку для запуска игры:",
        reply_markup=reply_markup
    )

async def any_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Реагируем на любое упоминание бота или команды"""
    text = update.message.text.lower()
    
    if any(word in text for word in ['старт', 'start', 'игра', 'daggerheart', 'играть']):
        user = update.effective_user
        
        keyboard = [
            [InlineKeyboardButton("🎮 Daggerheart", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🎲 {user.first_name}, го играть!",
            reply_markup=reply_markup
        )

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    
    app.add_handler(MessageHandler(
        filters.TEXT & (filters.Entity("mention") | filters.Regex(r'(?i)(старт|start|игра|daggerheart|играть)')), 
        any_mention
    ))
    
    logger.info("🤖 Бот запущен для групп!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()