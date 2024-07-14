from telegram import Update
from telegram.ext import CallbackContext
from config import GIT_REPO_URL

def check(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Your site is live at: {GIT_REPO_URL.replace(".git", "")}')