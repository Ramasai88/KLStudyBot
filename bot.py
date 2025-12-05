from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import datetime
from openpyxl import Workbook, load_workbook

TOKEN = "8510356081:AAFrHnmw9ui7iQ-y4ADcEcXl1Tbd35rt8Eo"  # Your Telegram bot token
ADMIN_CHAT_ID = "6125907347"  # Your Telegram user ID for receiving feedback privately

waiting_for_feedback = False  # flag for tracking feedback input


def save_feedback_to_excel(username, feedback):
    file_name = "feedback.xlsx"

    try:
        workbook = load_workbook(file_name)
        sheet = workbook.active
    except:
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Username", "Feedback", "Date", "Time"])  # header row

    now = datetime.datetime.now()
    sheet.append([username, feedback, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")])
    workbook.save(file_name)


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🏖 Holidays", callback_data="holidays")],
        [InlineKeyboardButton("💡Exam Motivation", callback_data="motivation")],
        [InlineKeyboardButton("📝 Feedback", callback_data="feedback")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Hello! I am your KL Study Assistant Bot 🤖\n\nChoose what you need:",
        reply_markup=reply_markup
    )


def button_handler(update: Update, context: CallbackContext):
    global waiting_for_feedback
    query = update.callback_query
    query.answer()

    if query.data == "holidays":
        query.edit_message_text(
            "🏖 *KL University – Public Holidays 2025*\n\n"
            "1. *13-01-2025 to 15-01-2025* (Mon–Wed)\n"
            "   Pongal Holidays / Bhogi / Sankranthi / Kanuma\n\n"
            "2. *26-02-2025* (Wed)\n"
            "   Maha Shivaratri\n\n"
            "3. *31-03-2025* (Mon)\n"
            "   Ramzan (Id–Ul–Fitr)\n\n"
            "4. *08-08-2025* (Fri)\n"
            "   Varalakshmi Vratham\n\n"
            "5. *16-08-2025* (Sat)\n"
            "   Krishnashtami\n\n"
            "6. *27-08-2025* (Wed)\n"
            "   Vinayaka Chavithi\n\n"
            "7. *29-09-2025 to 04-10-2025* (Mon–Sat)\n"
            "   Dussehra Vacation\n\n"
            "8. *20-10-2025 & 21-10-2025* (Mon & Tue)\n"
            "   Deepavali\n\n"
            "9. *25-12-2025* (Thu)\n"
            "   Christmas",
            parse_mode="Markdown"
        )

    elif query.data == "motivation":
        tips = [
            "🔥 Success doesn't come from what you do occasionally, but from what you do consistently!",
            "📚 Study while others are sleeping. Dream while others are wishing.",
            "💪 Don’t stop when you're tired. Stop when you are done!",
            "🎯 Small daily progress adds up to big results.",
            "⏳ 45 minutes of focused study > 3 hours of distracted study!",
            "🚫 Stop doubting yourself — work hard and make it happen.",
            "You’ve got this. Don’t stop.",
            "📚Work hard in silence; results will make the noise.",
            "Start now. Get ahead."
        ]

        import random
        query.edit_message_text("💡 *Daily Motivation*\n\n" + random.choice(tips), parse_mode="Markdown")

    elif query.data == "feedback":
        waiting_for_feedback = True
        query.edit_message_text("📝 Please type your feedback below.\nYour feedback will help improve the bot 😊")


def text_handler(update: Update, context: CallbackContext):
    global waiting_for_feedback

    if waiting_for_feedback:
        feedback = update.message.text
        waiting_for_feedback = False
        username = update.message.from_user.username or "No Username"

        # Save to Excel
        save_feedback_to_excel(username, feedback)

        # Send to admin
        context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"📩 *New Feedback Received:*\n\n{feedback}\n\nFrom: @{username}",
            parse_mode="Markdown"
        )

        # User response after feedback sent
        update.message.reply_text(
            "Thanks a lot for your feedback! ❤️ We’ll look into your suggestion and try to implement it as soon as possible. Stay tuned! 🚀"
        )

    else:
        update.message.reply_text("Use /start to open the menu 🙂")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text, text_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
