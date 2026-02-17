import asyncio
from telegram import Bot

async def test_bot():
    TOKEN = "YOUR_BOT_TOKEN"  # ضع التوكن هنا
    bot = Bot(token=TOKEN)
    print("✅ محاولة الاتصال...")
    me = await bot.get_me()
    print(f"✅ تم الاتصال! البوت اسمه: {me.first_name}")

asyncio.run(test_bot())
