import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os
from datetime import datetime

# ========== قراءة المفاتيح من Environment Variables ==========
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENROUTER_KEY = os.environ.get('OPENROUTER_API_KEY')

if not BOT_TOKEN or not OPENROUTER_KEY:
    raise ValueError("❌ المفاتيح غير موجودة في Environment Variables!")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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

# قائمة بالنماذج المجانية
FREE_MODELS = [
    "meta-llama/llama-3.2-3b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free",
    "cognitivecomputations/dolphin-2.9-llama3-8b:free",
    "gryphe/mythomax-l2-13b:free"
]

async def try_model(model_name, user_message):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://t.me/your_bot",
                "X-Title": "Telegram Bot"
            },
            json={
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "أنت مساعد ذكي ومفيد. رد باللغة العربية دائماً."},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            },
            timeout=15
        )
        
        data = response.json()
        
        if response.status_code == 200:
            return True, data['choices'][0]['message']['content']
        else:
            return False, f"خطأ {response.status_code}"
            
    except Exception as e:
        return False, str(e)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    user_name = update.message.from_user.first_name

    # التأكد أن المستخدم مصرح له
    if user_id not in [FATIMA_ID, ABDULKHALIQ_ID, OWNER_ID]:
        await update.message.reply_text("❌ هذا البوت خاص.")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    # محاولة النماذج واحداً تلو الآخر
    for model in FREE_MODELS:
        success, result = await try_model(model, user_message)
        
        if success:
            await update.message.reply_text(result)
            
            if user_id in [FATIMA_ID, ABDULKHALIQ_ID]:
                user_type = "فاطمة" if user_id == FATIMA_ID else "عبدالخالق"
                await send_to_owner(
                    context,
                    f"📩 **رسالة من {user_type}**\n"
                    f"👤 {user_name}\n"
                    f"💬 {user_message[:100]}..."
                )
            return
        
        logging.warning(f"النموذج {model} فشل")
    
    await update.message.reply_text("❌ عذراً، جميع نماذج الذكاء الاصطناعي غير متاحة حالياً.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("=" * 60)
    print("🤖 بوت فاطمة - يعمل على Render")
    print("=" * 60)
    print(f"👤 فاطمة: {FATIMA_ID}")
    print(f"👑 المالك: {OWNER_ID}")
    print("=" * 60)
    
    app.run_polling()

if __name__ == '__main__':
    main()
