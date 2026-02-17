#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
بوت فاطمة الذكي
مدعوم بـ OpenRouter AI
"""

import sys
import os
from pathlib import Path

# إضافة المجلد الحالي إلى مسار Python
sys.path.append(str(Path(__file__).parent))

from config import validate_config
from bot import FatimaBot

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    
    print("=" * 50)
    print("🚀 بوت فاطمة الذكي - جاهز للتشغيل")
    print("=" * 50)
    
    # التحقق من الإعدادات
    if not validate_config():
        print("\n❌ فشل التحقق من الإعدادات. يرجى مراجعة ملف .env")
        sys.exit(1)
    
    print("\n✅ الإعدادات سليمة. بدء التشغيل...\n")
    
    try:
        # إنشاء وتشغيل البوت
        bot = FatimaBot()
        bot.run()
    
    except KeyboardInterrupt:
        print("\n\n👋 تم إيقاف البوت بواسطة المستخدم")
    
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
