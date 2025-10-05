from flask import Flask, render_template, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

BOT_TOKEN = "YOUR_BOT_TOKEN"  # apna token yahan daalna

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/privacy-policy')
def privacy_policy():
    return render_template("privacy-policy.html")

@app.route('/terms')
def terms():
    return render_template("terms.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1st Semester", callback_data='1st_Semester')],
        [InlineKeyboardButton("2nd Semester", callback_data='2nd_Semester')],
        [InlineKeyboardButton("3rd Semester", callback_data='3rd_Semester')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select your semester 👇", reply_markup=reply_markup)

app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
app_bot.add_handler(CommandHandler("start", start))

async def run_bot():
    await app_bot.initialize()
    await app_bot.start()
    await app_bot.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=10000)
