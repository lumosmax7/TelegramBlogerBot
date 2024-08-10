import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import BLOG_PATH

def page_delete(update: Update, context: CallbackContext) -> None:
    posts_path = os.path.join(BLOG_PATH, 'source/_posts')
    posts = [file for file in os.listdir(posts_path) if file.endswith('.md')]
    keyboard = [[InlineKeyboardButton(post, callback_data=f'page_delete_{post}')] for post in posts]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose a post to delete:', reply_markup=reply_markup)

def handle_page_delete_choice(update: Update, context: CallbackContext, page_name: str) -> None:
    posts_path = os.path.join(BLOG_PATH, 'source/_posts')
    post_path = os.path.join(posts_path, page_name)
    query = update.callback_query.message
    if os.path.exists(post_path):
        os.remove(post_path)
        query.reply_text(f'Post deleted: {page_name}, Please use /push to refresh site.')
    else:
        query.reply_text('Post not found.')