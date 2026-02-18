import os
import requests
import sys

print("=" * 50)
print("🧪 اختبار الذكاء الاصطناعي - OpenRouter")
print("=" * 50)

# 1. التحقق من وجود المفتاح
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    print("\n❌ OPENROUTER_API_KEY غير موجود في المتغيرات البيئية")
    print("الرجاء إضافته في Secrets (Replit) أو Environment Variables (Render)")
    sys.exit(1)

print(f"\n✅ تم العثور على المفتاح: {api_key[:15]}...")

# 2. اختبار صلاحية المفتاح
print("\n🔍 التحقق من صلاحية المفتاح...")

try:
    response = requests.get(
        "https://openrouter.ai/api/v1/auth/key",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ المفتاح صالح")
        print(f"   الرصيد/الحد: {data.get('data', {}).get('limit', 'غير معروف')}")
    else:
        print(f"❌ المفتاح غير صالح: {response.status_code}")
        print(f"   {response.text}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ خطأ في الاتصال: {e}")
    sys.exit(1)

# 3. اختبار إرسال رسالة حقيقية
print("\n🤖 إرسال رسالة اختبار إلى DeepSeek...")

test_messages = [
    {"role": "system", "content": "أنت مساعد ذكي ومفيد. أجب باللغة العربية."},
    {"role": "user", "content": "مرحباً! كيف حالك؟ أجب بجملة واحدة قصيرة."}
]

try:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": test_messages,
            "temperature": 0.7,
            "max_tokens": 100
        },
        timeout=15
    )
    
    if response.status_code == 200:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        print(f"\n✅ الرد من الذكاء الاصطناعي:")
        print(f"   \"{reply}\"")
        print(f"\n📊 الإحصائيات:")
        print(f"   - النموذج: {data.get('model', 'غير معروف')}")
        print(f"   - التوكنات: {data.get('usage', {}).get('total_tokens', 'غير معروف')}")
    else:
        print(f"\n❌ فشل الاتصال: {response.status_code}")
        print(f"   {response.text}")
        
except Exception as e:
    print(f"\n❌ خطأ في الطلب: {e}")

print("\n" + "=" * 50)
print("✅ انتهى الاختبار")
