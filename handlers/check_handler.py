from telegram import Update
from telegram.ext import CallbackContext
from config import GP_URL

def check(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Your site is live at: {GP_URL}')