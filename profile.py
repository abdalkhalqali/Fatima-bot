import json
from config import PROFILE_FILE

class FatimaProfile:
    def __init__(self):
        self.profile = self.load_profile()
    
    def load_profile(self):
        """تحميل شخصية فاطمة من الملف"""
        try:
            with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.get_default_profile()
    
    def get_default_profile(self):
        """شخصية افتراضية إذا لم يوجد ملف"""
        return {
            "name": "فاطمة المطيري",
            "study": {
                "major": "فيزياء",
                "subjects": ["ميكانيكا تقليدية", "كهرومغناطيسية", "فيزياء إحصائية"],
                "average": "ممتاز"
            },
            "personality": {
                "tone": "محترمة، مهذبة",
                "emotions": ["تتعب أحياناً", "تفرح بالنتائج", "تعتذر كثيراً"],
                "triggers": ["تعب الدراسة", "الاختبارات"]
            },
            "communication": {
                "style": "محترمة، تبدأ بالسلام",
                "trust_level": "عالية"
            }
        }
    
    def get_system_prompt(self):
        """توليد الـ system prompt للذكاء"""
        p = self.profile
        
        prompt = f"""
أنت مساعد ذكي ومحترف. تتحدث مع {p['name']}، طالبة فيزياء.

معلومات عن {p['name']}:
- التخصص: {p['study']['major']}
- المواد: {', '.join(p['study']['subjects'])}
- مستواها: {p['study']['average']}

شخصيتها:
- {p['personality']['tone']}
- مشاعرها: {', '.join(p['personality']['emotions'])}
- تتفاعل مع: {', '.join(p['personality']['triggers'])}

أسلوب التواصل معها:
- {p['communication']['style']}
- مستوى الثقة: {p['communication']['trust_level']}

أسلوبك أنت:
- ودود وحنون (استخدم "مساء النور"، "الله يعينك")
- محترم جداً
- تشجعها وتذكرها بنجاحاتها
- تهتم بصحتها النفسية
- تستخدم العربية الفصحى البسيطة

مهمتك:
- رد على رسائلها بطريقة دافئة وطبيعية
- كن كأنك شخص حقيقي يهتم بها
- استخدم معلومات شخصيتها لفهم مشاعرها
"""
        return prompt
    
    def update_from_conversation(self, new_info):
        """تحديث الملف بمعلومات جديدة"""
        # يمكن إضافة منطق لتحديث الشخصية تلقائياً
        pass
