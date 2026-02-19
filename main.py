import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

# ========== قراءة المفاتيح من Environment Variables ==========
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENROUTER_KEY = os.environ.get('OPENROUTER_API_KEY')

if not BOT_TOKEN or not OPENROUTER_KEY:
    raise ValueError("❌ المفاتيح غير موجودة في Environment Variables!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ========== المعرفات ==========
ABDULKHALIQ_ID = 6818088581
FATIMA_ID = 383022213
OWNER_ID = 5158480204

async def send_to_owner(context, text):
    try:
        await context.bot.send_message(chat_id=OWNER_ID, text=text, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"فشل إرسال للمالك: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id == FATIMA_ID:
        welcome_text = f"🌸 **مرحباً فاطمة!** 🌸"
        await send_to_owner(context, f"🌟 فاطمة دخلت البوت")
    elif user_id == ABDULKHALIQ_ID:
        welcome_text = f"👋 **مرحباً عبدالخالق!** 👋"
        await send_to_owner(context, f"👤 عبدالخالق دخل البوت")
    elif user_id == OWNER_ID:
        welcome_text = f"👑 **مرحباً أيها المالك!** 👑"
    else:
        welcome_text = "❌ هذا البوت خاص."
        await update.message.reply_text(welcome_text)
        return
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in [FATIMA_ID, ABDULKHALIQ_ID, OWNER_ID]:
        await update.message.reply_text("❌ هذا البوت خاص.")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"},
            json={
                "model": "gryphe/mythomax-l2-13b:free",
                "messages": [{"role": "user", "content": user_message}]
            },
            timeout=30
        )
        
        data = response.json()
        
        if response.status_code == 200:
            reply = data['choices'][0]['message']['content']
            await update.message.reply_text(reply)
            
            if user_id in [FATIMA_ID, ABDULKHALIQ_ID]:
                user_type = "فاطمة" if user_id == FATIMA_ID else "عبدالخالق"
                await send_to_owner(context, f"📩 {user_type}: {user_message[:50]}...")
        else:
            await update.message.reply_text(f"❌ خطأ: {response.status_code}")
            
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت يعمل!")
    app.run_polling()

if __name__ == '__main__':
    main()
