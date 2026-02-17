import sqlite3
import json
from datetime import datetime
from config import DATABASE_NAME

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        """إنشاء الجداول المطلوبة"""
        cursor = self.conn.cursor()
        
        # جدول الرسائل
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_name TEXT,
                message TEXT,
                sender TEXT,
                timestamp DATETIME,
                ai_used BOOLEAN DEFAULT 0
            )
        """)
        
        # جدول الملخصات (للذكاء)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                summary TEXT,
                last_updated DATETIME
            )
        """)
        
        self.conn.commit()
    
    def save_message(self, user_id, message, sender, user_name=None, ai_used=False):
        """حفظ رسالة جديدة"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO messages (user_id, user_name, message, sender, timestamp, ai_used)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, user_name, message, sender, datetime.now(), ai_used))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_chat_history(self, user_id, limit=20):
        """الحصول على تاريخ المحادثة"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT message, sender, timestamp, user_name 
            FROM messages 
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))
        return cursor.fetchall()
    
    def get_recent_messages(self, user_id, hours=24):
        """الحصول على رسائل آخر 24 ساعة"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT message, sender, timestamp 
            FROM messages 
            WHERE user_id = ? AND timestamp > datetime('now', '-? hours')
            ORDER BY timestamp ASC
        """, (user_id, hours))
        return cursor.fetchall()
    
    def update_summary(self, user_id, summary):
        """تحديث ملخص المحادثات للذكاء"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO summaries (user_id, summary, last_updated)
            VALUES (?, ?, ?)
        """, (user_id, summary, datetime.now()))
        self.conn.commit()
    
    def get_summary(self, user_id):
        """الحصول على آخر ملخص"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT summary FROM summaries WHERE user_id = ?
        """, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def get_statistics(self, user_id=None):
        """إحصائيات عامة"""
        cursor = self.conn.cursor()
        
        if user_id:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN sender = 'user' THEN 1 ELSE 0 END) as from_user,
                    SUM(CASE WHEN sender = 'bot' THEN 1 ELSE 0 END) as from_bot,
                    MIN(timestamp) as first,
                    MAX(timestamp) as last
                FROM messages 
                WHERE user_id = ?
            """, (user_id,))
        else:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(DISTINCT user_id) as users
                FROM messages
            """)
        
        return cursor.fetchone()
    
    def close(self):
        """إغلاق الاتصال"""
        self.conn.close()
