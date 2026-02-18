from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN, AUTHORIZED_USERS, OWNER_ID, FATIMA_ID
from database import Database
from ai import OpenRouterAI

class FatimaBot:
    def __init__(self):
        self.db = Database()
        self.ai = OpenRouterAI()
        self.application = Application.builder().token(TELEGRAM_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """تسجيل جميع الأوامر"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("chat", self.chat_command))
        self.application.add_handler(CommandHandler("history", self.history_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("broadcast", self.broadcast_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """رسالة الترحيب حسب المستخدم"""
        user_id = update.effective_user.id
        
        if user_id == OWNER_ID:
            await update.message.reply_text(
                "👑 **مرحباً أيها المالك**\n\n"
                "الأوامر المتاحة:\n"
                "/chat user_id الرسالة - إرسال رسالة\n"
                "/history user_id - عرض تاريخ المحادثة\n"
                "/stats - إحصائيات عامة\n"
                "/broadcast رسالة - إرسال للجميع\n\n"
                "✅ البوت يعمل ويراقب فاطمة"
            )
        elif user_id in AUTHORIZED_USERS:
            await update.message.reply_text(
                "🎯 **مرحباً عبدالخالق**\n\n"
                "الأوامر المتاحة:\n"
                "/chat 383022213 الرسالة - إرسال لفاطمة\n"
                "/history 383022213 - عرض تاريخ المحادثة\n\n"
                "📩 أي رسالة من فاطمة سأعرضها هنا"
            )
        elif user_id == FATIMA_ID:
            await update.message.reply_text(
                "✨ مرحباً فاطمة! أنا مساعدك الذكي. كيف يمكنني مساعدتك اليوم؟"
            )
        else:
            await update.message.reply_text(
                "مرحباً! أنا بوت مخصص. للأسف لا أستطيع مساعدتك."
            )
    
    async def chat_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """إرسال رسالة إلى مستخدم معين"""
        user_id = update.effective_user.id
        
        # التحقق من الصلاحية
        if user_id not in AUTHORIZED_USERS and user_id != OWNER_ID:
            await update.message.reply_text("⛔ هذا الأمر خاص بالمشرفين فقط.")
            return
        
        if len(context.args) < 2:
            await update.message.reply_text("❗ استخدم: /chat user_id الرسالة")
            return
        
        try:
            target_id = int(context.args[0])
            message = " ".join(context.args[1:])
            
            # إرسال الرسالة
            await context.bot.send_message(chat_id=target_id, text=message)
            
            # حفظ في قاعدة البيانات
            self.db.save_message(target_id, message, "admin", str(user_id))
            
            # تأكيد للمرسل
            await update.message.reply_text(f"✅ تم إرسال الرسالة إلى {target_id}")
            
            # إشعار المالك إذا كان المرسل غير المالك
            if user_id != OWNER_ID:
                await context.bot.send_message(
                    chat_id=OWNER_ID,
                    text=f"📤 عبدالخالق أرسل رسالة إلى {target_id}:\n\n{message}"
                )
        
        except Exception as e:
            await update.message.reply_text(f"❌ فشل الإرسال: {str(e)}")
    
    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض تاريخ المحادثة"""
        user_id = update.effective_user.id
        
        if user_id not in AUTHORIZED_USERS and user_id != OWNER_ID:
            await update.message.reply_text("⛔ غير مصرح")
            return
        
        # تحديد المستهدف
        if context.args:
            target_id = int(context.args[0])
        else:
            target_id = FATIMA_ID
        
        history = self.db.get_chat_history(target_id, limit=15)
        
        if not history:
            await update.message.reply_text("📭 لا توجد رسائل سابقة.")
            return
        
        response = f"📜 **تاريخ المحادثة مع {target_id}**\n\n"
        for msg, sender, ts, name in history:
            emoji = "👤" if sender == "user" else "🤖" if sender == "bot" else "📤"
            sender_name = "فاطمة" if sender == "user" else "البوت" if sender == "bot" else "مرسل"
            response += f"{emoji} {sender_name}: {msg[:50]}...\n⏱️ {ts[:16]}\n\n"
        
        # تقسيم الرسالة الطويلة
        if len(response) > 4000:
            for i in range(0, len(response), 4000):
                await update.message.reply_text(response[i:i+4000])
        else:
            await update.message.reply_text(response)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """إحصائيات البوت"""
        user_id = update.effective_user.id
        
        if user_id not in AUTHORIZED_USERS and user_id != OWNER_ID:
            await update.message.reply_text("⛔ غير مصرح")
            return
        
        stats = self.db.get_statistics(FATIMA_ID)
        
        if stats:
            total, from_user, from_bot, first, last = stats
            response = f"📊 **إحصائيات محادثة فاطمة**\n\n"
            response += f"إجمالي الرسائل: {total}\n"
            response += f"من فاطمة: {from_user}\n"
            response += f"من البوت: {from_bot}\n"
            response += f"أول رسالة: {first[:16]}\n"
            response += f"آخر رسالة: {last[:16]}"
        else:
            response = "📊 لا توجد إحصائيات بعد"
        
        await update.message.reply_text(response)
    
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """إرسال رسالة للجميع (للمالك فقط)"""
        user_id = update.effective_user.id
        
        if user_id != OWNER_ID:
            await update.message.reply_text("⛔ هذا الأمر للمالك فقط")
            return
        
        if not context.args:
            await update.message.reply_text("❗ استخدم: /broadcast الرسالة")
            return
        
        message = " ".join(context.args)
        
        # إرسال للمشرفين
        for uid in AUTHORIZED_USERS:
            try:
                await context.bot.send_message(chat_id=uid, text=f"📢 إشعار عام:\n\n{message}")
            except:
                pass
        
        # إرسال لفاطمة
        try:
            await context.bot.send_message(chat_id=FATIMA_ID, text=message)
        except:
            pass
        
        await update.message.reply_text("✅ تم البث للجميع")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة جميع الرسائل الواردة"""
        user_id = update.effective_user.id
        user_message = update.message.text
        user_name = update.effective_user.first_name
        
        # حفظ الرسالة في قاعدة البيانات
        self.db.save_message(user_id, user_message, "user", user_name)
        
        # إذا كانت الرسالة من فاطمة
        if user_id == FATIMA_ID:
            # إرسال إشعار للمشرفين
            notification = f"📩 **رسالة جديدة من فاطمة**\n\n{user_message}"
            
            for admin_id in AUTHORIZED_USERS:
                try:
                    await context.bot.send_message(chat_id=admin_id, text=notification)
                except:
                    pass
            
            # إشعار المالك
            await context.bot.send_message(
                chat_id=OWNER_ID,
                text=f"📩 فاطمة: {user_message}"
            )
            
            # توليد رد ذكي باستخدام الذكاء
            ai_response = self.ai.generate_response(user_id, user_message, user_name)
            
            # إرسال الرد إلى فاطمة
            await update.message.reply_text(ai_response)
            
            # حفظ الرد في قاعدة البيانات
            self.db.save_message(user_id, ai_response, "bot", "AI", ai_used=True)
            
            # إعلام المشرفين بالرد
            for admin_id in AUTHORIZED_USERS:
                try:
                    await context.bot.send_message(
                        chat_id=admin_id,
                        text=f"🤖 **رد البوت على فاطمة:**\n\n{ai_response}"
                    )
                except:
                    pass
        
        # إذا كانت الرسالة من مشرف (ونحن نتعامل معها)
        elif user_id in AUTHORIZED_USERS:
            # يمكن إضافة منطق خاص لردود المشرف
            pass
        
        # إذا كانت من شخص آخر
        elif user_id != OWNER_ID:
            # رد آلي لطيف
            await update.message.reply_text(
                "مرحباً! أنا بوت مخصص لمساعدة فاطمة فقط."
            )
    
    def run(self):
        """تشغيل البوت"""
        print("🚀 بوت فاطمة يعمل...")
        self.application.run_polling()
            
