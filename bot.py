import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("❌ التوكن غير موجود!")

print(f"✅ التوكن موجود: {BOT_TOKEN[:10]}...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل!")

def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        print("✅ البوت بدأ العمل...")
        app.run_polling()
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == '__main__':
    main()
