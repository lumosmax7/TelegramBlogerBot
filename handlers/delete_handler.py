import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

def delete(update: Update, context: CallbackContext) -> None:
    drafts_path = os.path.join("/app/bloger", 'source/_drafts')
    drafts = [file for file in os.listdir(drafts_path) if file.endswith('.md')]
    keyboard = [[InlineKeyboardButton(draft, callback_data=f'delete_{draft}')] for draft in drafts]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose a draft to delete:', reply_markup=reply_markup)



