from telegram import Update
from telegram.ext import CallbackContext
from handlers import user_state_handler
import os
from config import REPO_PATH

def handle_edit_message(update: Update, context: CallbackContext) -> None:
    if user_state_handler.get_user_state() == 'edit_title':
        new_title = update.message.text
        old_path = os.path.join(REPO_PATH, 'source/_drafts', user_state_handler.get_user_draft()+'.md')
        new_path = os.path.join(REPO_PATH, 'source/_drafts', f'{new_title}.md')
        os.rename(old_path, new_path)
        with open(new_path, 'r+') as f:
            content = f.readlines()
            content[1] = f'title: {new_title}\n'
            f.seek(0)
            f.writelines(content)
            f.truncate()
        update.message.reply_text(f'Title updated to: {new_title}.md')
        user_state_handler.set_user_state(None)
        user_state_handler.set_user_draft(None)
    elif user_state_handler.get_user_state() == 'edit_content':
        new_content = update.message.text
        draft_path = os.path.join(REPO_PATH, 'source/_drafts', user_state_handler.get_user_draft()+'.md')
        with open(draft_path, 'w') as f:
            f.write('---\n')
            f.write(f'title: {user_state_handler.get_user_draft()}\n')
            f.write('---\n')
            f.write(new_content)
        update.message.reply_text(f'Content updated for: {user_state_handler.get_user_draft()}.md')
        user_state_handler.set_user_state(None)
        user_state_handler.set_user_draft(None)
def handle_new_message(update: Update, context: CallbackContext) -> None:
    if user_state_handler.get_user_state() == 'new_title':
        user_state_handler.set_user_draft(update.message.text)
        update.message.reply_text(f'Title received: {user_state_handler.get_user_draft()}\nNow please enter the content of the draft:')
        user_state_handler.set_user_state('new_content')
    elif user_state_handler.get_user_state() == 'new_content':
        content = update.message.text
        draft_path = os.path.join(REPO_PATH, 'source/_drafts', f'{user_state_handler.get_user_draft()}.md')
        with open(draft_path, 'w') as f:
            f.write('---\n')
            f.write(f'title: {user_state_handler.get_user_draft()}\n')
            f.write('---\n')
            f.write(f'{content}')
        update.message.reply_text(f'New draft created: {user_state_handler.get_user_draft()}')
        user_state_handler.set_user_state(None)
        user_state_handler.set_user_draft(None)


def handle_message(update: Update, context: CallbackContext) -> None:
    if user_state_handler.get_user_state() == 'new_title' or user_state_handler.get_user_state() == 'new_content':
        handle_new_message(update, context)
    elif user_state_handler.get_user_state() in ['edit_title', 'edit_content']:
        handle_edit_message(update, context)
