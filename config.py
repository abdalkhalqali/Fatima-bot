import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

# -------------------- الأسرار --------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# -------------------- معرفات المستخدمين --------------------
OWNER_ID = int(os.getenv("OWNER_ID", 0))
ABDULKHALIQ_ID = int(os.getenv("ABDULKHALIQ_ID", 0))
FATIMA_ID = int(os.getenv("FATIMA_ID", 0))

# -------------------- إعدادات المشروع --------------------
DATABASE_NAME = "fatima_chat.db"
PROFILE_FILE = "fatima_profile.json"

# -------------------- التحقق من صحة الإعدادات --------------------
def validate_config():
    """التحقق من وجود جميع الإعدادات الأساسية"""
    errors = []
    
    if not TELEGRAM_TOKEN:
        errors.append("❌ TELEGRAM_BOT_TOKEN غير موجود في ملف .env")
    
    if not OPENROUTER_API_KEY:
        errors.append("❌ OPENROUTER_API_KEY غير موجود في ملف .env")
    
    if OWNER_ID == 0:
        errors.append("❌ OWNER_ID غير موجود في ملف .env")
    
    if ABDULKHALIQ_ID == 0:
        errors.append("❌ ABDULKHALIQ_ID غير موجود في ملف .env")
    
    if FATIMA_ID == 0:
        errors.append("❌ FATIMA_ID غير موجود في ملف .env")
    
    if errors:
        print("\n".join(errors))
        return False
    
    print("✅ جميع الإعدادات سليمة")
    return True

# قائمة المستخدمين المسموح لهم بالتحكم
AUTHORIZED_USERS = [OWNER_ID, ABDULKHALIQ_ID]

if __name__ == "__main__":
    validate_config()
