#!/usr/bin/env python3
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import BadRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
WEBAPP_URL = os.environ.get('WEBAPP_URL')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start с WebApp"""
    user = update.effective_user
    chat = update.effective_chat
    
    try:
        # ВАЖНО: используем WebAppInfo для открытия внутри Telegram
        keyboard = [
            [InlineKeyboardButton("⚔️ Играть в Daggerheart", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if chat.type == 'private':
            message = f"🎭 Добро пожаловать, {user.first_name}!\n\n Нажми кнопку для старта:"
        else:
            message = f"🎭 Добро пожаловать, {user.first_name}!\n\n Нажми кнопку для старта:"
        
        await update.message.reply_text(
            message,
            reply_markup=reply_markup
        )
        
        logger.info(f"WebApp кнопка отправлена пользователю {user.first_name}")
        
    except BadRequest as e:
        logger.error(f"Ошибка WebApp: {e}")
        
        # Fallback на обычную ссылку
        keyboard = [
            [InlineKeyboardButton("🌐 Открыть в браузере", url=WEBAPP_URL)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🎭 {user.first_name}, игра:\n\n⚠️ WebApp не настроен, открывается в браузере",
            reply_markup=reply_markup
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start_command))
    app.add_error_handler(error_handler)
    
    logger.info("🤖 Бот с WebApp запущен!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()