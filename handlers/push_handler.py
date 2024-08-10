import os
import subprocess

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import BLOG_PATH


def push(update: Update, context: CallbackContext) -> None:
    drafts_path = os.path.join(BLOG_PATH, 'source/_drafts')
    drafts = os.listdir(drafts_path)
    posts_path = os.path.join(BLOG_PATH, 'source/_posts')
    posts = os.listdir(posts_path)
    drafts_all = ''
    posts_all = ''
    for draft in drafts:
        if draft.endswith('.md'):
            drafts_all = drafts_all + draft + '\n'
    for post in posts:
        if post.endswith('.md'):
            posts_all = posts_all + post + '\n'

    keyboard = [
        [InlineKeyboardButton('Confirm Push', callback_data='confirm_push')],
        [InlineKeyboardButton('Cancel', callback_data='cancel_push')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please confirm the data to push:\n'
                              'Posts :\n' + posts_all + '\n'
                                                        'Drafts :\n' + drafts_all,
                              reply_markup=reply_markup)


def handle_push_choice(update: Update,
                       context: CallbackContext) -> None:
    os.chdir(BLOG_PATH)
    for file_name in os.listdir('source/_drafts'):
        if file_name.endswith('.md'):
            subprocess.run(['mv', 'source/_drafts/' + file_name, 'source/_posts/'])

    subprocess.run(['hexo', 'clean'])
    subprocess.run(['hexo', 'generate'])
    # subprocess.run(['hexo', 'deploy'])

    query = update.callback_query
    query.message.reply_text('Site compiled and deployed to GitHub.')
