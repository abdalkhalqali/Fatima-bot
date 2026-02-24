async def simple_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        return
    
    text = update.message.text.replace('/simplequiz', '').strip()
    if not text:
        await update.message.reply_text("أرسل /simplequiz ثم النص مباشرة في نفس الرسالة")
        return
    
    questions = parse_quiz_text(text)
    if questions:
        await update.message.reply_text(f"✅ تم استقبال {len(questions)} سؤال")
    else:
        await update.message.reply_text("❌ فشل التحليل")

app.add_handler(CommandHandler("simplequiz", simple_quiz))
