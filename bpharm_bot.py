import asyncio
import logging
import os
from flask import Flask, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from threading import Thread

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Flask App
app = Flask(__name__)

# Telegram Bot Token (read from environment variables)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME", "YOUR_BOT_USERNAME")

# Flask Routes
@app.route('/')
def home():
    return render_template('index.html', bot_username=BOT_USERNAME)

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/contact')
def contact():
    return render_template('contact.html', bot_username=BOT_USERNAME)

# Telegram Bot Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Show semester selection"""
    keyboard = [
        [InlineKeyboardButton("1st Semester", callback_data='sem_1')],
        [InlineKeyboardButton("2nd Semester", callback_data='sem_2')],
        [InlineKeyboardButton("3rd Semester", callback_data='sem_3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        "🎓 *Welcome to B.Pharm Helper Bot!*\n\n"
        "Select your semester to get papers and guess questions:\n"
    )
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    # Get the callback data
    data = query.data
    
    if data.startswith('sem_'):
        semester = data.split('_')[1]
        await query.edit_message_text(
            text=f"📚 *Semester {semester}*\n\n🚧 Coming Soon!\n\n"
                 f"Papers and guess questions will be available soon.",
            parse_mode='Markdown'
        )

# Initialize Telegram Bot
def setup_telegram_bot():
    """Setup and run Telegram bot"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Run the bot
        logging.info("Telegram bot is now running...")
        application.run_polling(drop_pending_updates=True)
    except Exception as e:
        logging.error(f"Error starting Telegram bot: {e}")

# Run Flask in a separate thread
def run_flask():
    app.run(host='0.0.0.0', port=10000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run Telegram bot in main thread
    logging.info("Starting Telegram Bot...")
    setup_telegram_bot()
