import asyncio
from telegram import Bot
import os

async def test():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "ضع_التوكن_هنا_مباشرة")
    print(f"🔍 جرب استخدام التوكن: {TOKEN[:10]}...")
    
    bot = Bot(token=TOKEN)
    
    try:
        me = await bot.get_me()
        print(f"✅ نجح الاتصال! البوت: @{me.username}")
        
        # أرسل رسالة لنفسك
        await bot.send_message(chat_id=5158480204, text="✅ البوت يعمل!")
        print("✅ تم إرسال رسالة اختبار")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")

asyncio.run(test())
