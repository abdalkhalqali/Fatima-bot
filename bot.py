import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os
from datetime import datetime

# ========== قراءة المفاتيح من Environment Variables (بعد التعديل) ==========
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')              # ✅ تم التعديل
OPENROUTER_KEY = os.environ.get('OPENROUTER_API_KEY')         # ✅ تم التعديل

if not BOT_TOKEN or not OPENROUTER_KEY:
    raise ValueError("❌ المفاتيح غير موجودة في Environment Variables!")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ========== المعرفات ==========
ABRAR_ID = 1406525284
ABDULKHALIQ_ID = 6818088581
OWNER_ID = 5158480204
FATIMA_ID = 383022213  # فاطمة المطيري

async def send_to_owner(context, text):
    """إرسال إشعار للمالك"""
    try:
        await context.bot.send_message(chat_id=OWNER_ID, text=text, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"فشل إرسال للمالك: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.message.from_user.first_name
    
    welcome_text = "👋 **مرحباً بك في بوت الذكاء الاصطناعي!**\n\n✨ أرسل لي أي سؤال وسأجيبك."
    
    # رسائل خاصة
    if user_id == ABRAR_ID:
        welcome_text = f"🌸 **أهلاً أبرار!** 🌸\n\nأهلاً بك!"
        await send_to_owner(context, f"🌟 أبرار دخلت البوت")
    
    elif user_id == ABDULKHALIQ_ID:
        welcome_text = f"👋 **مرحباً عبدالخالق!** 👋"
        await send_to_owner(context, f"👤 عبدالخالق دخل البوت")
    
    elif user_id == FATIMA_ID:
        welcome_text = f"🌸 **مرحباً فاطمة!** 🌸\n\nأهلاً بك!"
        await send_to_owner(context, f"👤 فاطمة المطيري دخلت البوت")
    
    elif user_id == OWNER_ID:
        welcome_text = f"👑 **مرحباً أيها المالك!** 👑"
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

# قائمة بالنماذج المجانية التي قد تعمل
FREE_MODELS = [
    "gryphe/mythomax-l2-13b:free",
    "google/gemini-2.0-flash-exp:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free"
]

async def try_model(model_name, user_message):
    """محاولة استخدام نموذج معين"""
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
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=15
        )
        
        data = response.json()
        
        if response.status_code == 200:
            return True, data['choices'][0]['message']['content']
        else:
            error_msg = data.get('error', {}).get('message', 'خطأ غير معروف')
            return False, f"{model_name}: {error_msg}"
            
    except Exception as e:
        return False, f"{model_name}: {str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    user_name = update.message.from_user.first_name

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    # محاولة النماذج واحداً تلو الآخر
    for model in FREE_MODELS:
        success, result = await try_model(model, user_message)
        
        if success:
            await update.message.reply_text(result)
            
            # إرسال نسخة للمالك للمستخدمين المهمين
            if user_id in [ABRAR_ID, ABDULKHALIQ_ID, FATIMA_ID]:
                user_type = "أبرار" if user_id == ABRAR_ID else "عبدالخالق" if user_id == ABDULKHALIQ_ID else "فاطمة"
                await send_to_owner(
                    context,
                    f"📩 **رسالة من {user_type}**\n"
                    f"👤 {user_name}\n"
                    f"💬 {user_message[:100]}...\n"
                    f"🤖 {result[:100]}...\n"
                    f"⏰ {datetime.now().strftime('%H:%M:%S')}"
                )
            return
        
        logging.warning(f"النموذج {model} فشل: {result}")
    
    # إذا فشلت كل النماذج
    error_msg = "❌ عذراً، جميع نماذج الذكاء الاصطناعي غير متاحة حالياً. الرجاء المحاولة لاحقاً."
    await update.message.reply_text(error_msg)
    
    if user_id in [ABRAR_ID, ABDULKHALIQ_ID, FATIMA_ID]:
        await send_to_owner(context, f"⚠️ فشل الذكاء الاصطناعي لـ {user_name}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("=" * 60)
    print("🤖 بوت OpenRouter - النسخة النهائية")
    print("=" * 60)
    print(f"👤 أبرار: {ABRAR_ID}")
    print(f"👤 عبدالخالق: {ABDULKHALIQ_ID}")
    print(f"👤 فاطمة: {FATIMA_ID}")
    print(f"👑 المالك: {OWNER_ID}")
    print("✅ المتغيرات البيئية: TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY")
    print("=" * 60)
    
    app.run_polling()

if __name__ == '__main__':
    main()
