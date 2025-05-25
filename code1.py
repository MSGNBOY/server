import asyncio
from datetime import datetime, timedelta
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

BOT_TOKEN = "7971220423:AAFhRIfH35NtpvfoNdckejgX-eCd_JMIsGg"

reminders = []  # Store reminders in memory

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm your Reminder Bot. Use /remind <minutes> <message> to set a reminder.")

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /remind <minutes> <message>")
            return

        minutes = int(context.args[0])
        message = ' '.join(context.args[1:])
        remind_time = datetime.now() + timedelta(minutes=minutes)

        reminders.append({
            "chat_id": update.effective_chat.id,
            "message": message,
            "time": remind_time
        })

        await update.message.reply_text(f"Got it! I'll remind you in {minutes} minutes.")
    except Exception as e:
        await update.message.reply_text("Something went wrong. Try again.")

async def check_reminders(application):
    while True:
        now = datetime.now()
        for reminder in reminders[:]:
            if now >= reminder["time"]:
                try:
                    await application.bot.send_message(chat_id=reminder["chat_id"], text=f"Reminder: {reminder['message']}")
                    reminders.remove(reminder)
                except:
                    continue
        await asyncio.sleep(5)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remind", remind))

    app.job_queue.run_repeating(lambda *_: None, interval=60)  # dummy to start loop

    asyncio.create_task(check_reminders(app))
    app.run_polling()
