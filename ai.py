import os
import requests
import json

class OpenRouterAI:
    def __init__(self):
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            print("⚠️ تحذير: OPENROUTER_API_KEY غير موجود")
    
    def generate_response(self, user_message, user_name="فاطمة"):
        """توليد رد ذكي باستخدام OpenRouter"""
        
        if not self.api_key:
            return "عذراً، الذكاء الاصطناعي غير متاح حالياً."
        
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-chat",
                    "messages": [
                        {"role": "system", "content": f"أنت مساعد {user_name} الذكي. كن ودوداً ومفيداً."},
                        {"role": "user", "content": user_message}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                error_data = response.json()
                print(f"خطأ API: {error_data}")
                return f"عذراً، حدث خطأ في الذكاء الاصطناعي: {response.status_code}"
        
        except Exception as e:
            print(f"استثناء: {e}")
            return "عذراً، حدث خطأ تقني. سأرد عليك قريباً."
