from telegram import Update
from telegram.ext import CallbackContext
from handlers import user_state_handler

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! This bot can help you manage your Hexo blog. Command lists are below: \n'
                              ' /new command you can create a new draft.\n'
                              ' /edit command you can edit a previous draft.\n'
                              ' /post_edit command you can edit a post.\n'
                              ' /delete command you can delete a previous draft.\n'
                              ' /page_delete command you can delete a previous page.\n'
                              ' /push command you can push your changes to your blog.\n'
                              ' /check command you can get your blog URL.\n')

def new(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Please enter the title of the draft:')
    user_state_handler.set_user_state('new_title')


