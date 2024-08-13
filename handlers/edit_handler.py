import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import BLOG_PATH

def edit(update: Update, context: CallbackContext) -> None:
    drafts_path = os.path.join(BLOG_PATH, 'source/_drafts')
    drafts = [file for file in os.listdir(drafts_path) if file.endswith('.md')]
    keyboard = [[InlineKeyboardButton(draft, callback_data=f'edit_{draft}')] for draft in drafts]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose a draft to edit:', reply_markup=reply_markup)
def post_edit(update: Update, context: CallbackContext) -> None:
    drafts_path = os.path.join(BLOG_PATH, 'source/_posts')
    drafts = [file for file in os.listdir(drafts_path) if file.endswith('.md')]
    keyboard = [[InlineKeyboardButton(draft, callback_data=f'post_edit_{draft}')] for draft in drafts]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose a post to edit:', reply_markup=reply_markup)

def handle_edit_choice(update: Update, context: CallbackContext, draft: str) -> None:
    keyboard = [
        [InlineKeyboardButton("Edit Title", callback_data=f'edit_title_{draft}')],
        [InlineKeyboardButton("Edit Content", callback_data=f'edit_content_{draft}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.callback_query.message
    message.reply_text(f'What do you want to edit in "{draft}"?', reply_markup=reply_markup)
def handle_post_edit_choice(update: Update, context: CallbackContext, draft: str) -> None:
    keyboard = [
        [InlineKeyboardButton("Edit Title", callback_data=f'post_edit_title_{draft}')],
        [InlineKeyboardButton("Edit Content", callback_data=f'post_edit_content_{draft}')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.callback_query.message
    message.reply_text(f'What do you want to edit in "{draft}"?', reply_markup=reply_markup)