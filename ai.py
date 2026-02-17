import requests
import json
from config import OPENROUTER_API_KEY
from profile import FatimaProfile
from database import Database

class OpenRouterAI:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.profile = FatimaProfile()
        self.db = Database()
    
    def generate_response(self, user_id, user_message, user_name="فاطمة"):
        """توليد رد ذكي باستخدام OpenRouter"""
        
        # الحصول على تاريخ المحادثة
        history = self.db.get_chat_history(user_id, limit=10)
        
        # تحضير تاريخ المحادثة
        history_text = ""
        for msg, sender, ts, name in history:
            sender_name = user_name if sender == "user" else "المساعد"
            history_text += f"{sender_name}: {msg}\n"
        
        # الحصول على system prompt من شخصية فاطمة
        system_prompt = self.profile.get_system_prompt()
        
        # إضافة السياق الأخير
        context = f"""
آخر محادثة مع {user_name}:
{history_text}

رسالتها الحالية: {user_message}

الرد المناسب:
"""
        
        # إعداد الطلب
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek/deepseek-chat",  # أو أي نموذج تفضل
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context}
            ],
            "temperature": 0.8,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                
                # تحديث الملخص (اختياري)
                self.update_conversation_summary(user_id, user_message, reply)
                
                return reply.strip()
            
            else:
                error_data = response.json()
                return f"⚠️ عذراً، حدث خطأ: {error_data.get('error', {}).get('message', 'غير معروف')}"
        
        except requests.exceptions.Timeout:
            return "⚠️ عذراً، استغرق الطلب وقتاً طويلاً. حاول مرة أخرى."
        except Exception as e:
            return f"⚠️ حدث خطأ تقني: {str(e)}"
    
    def generate_emotional_response(self, situation):
        """توليد رد عاطفي مناسب لموقف معين"""
        
        prompt = f"""
الموقف: {situation}

المطلوب: رد عاطفي دافئ ومقنع، يجعلها تشعر بالاهتمام الحقيقي.
"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "system", "content": "أنت صديق مقرب وداعم عاطفياً."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9,
            "max_tokens": 300
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return "الله يكون في عونك."
        except:
            return "الله يعينك ويقويك."
    
    def update_conversation_summary(self, user_id, last_message, last_reply):
        """تحديث ملخص المحادثة (يمكن تطويره)"""
        # هنا يمكن إضافة منطق لتحديث شخصية فاطمة تلقائياً
        pass
