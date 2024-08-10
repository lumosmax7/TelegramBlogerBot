import os
from telegram import Update
from telegram.ext import CallbackContext
from config import BLOG_PATH
from handlers.edit_handler import handle_edit_choice
from handlers import user_state_handler
from handlers.page_delete_handler import handle_page_delete_choice
from handlers.push_handler import handle_push_choice
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data
    if data.startswith('edit_'):
        draft = data[len('edit_'):]
        if data.startswith('edit_title_'):
            draft = data[len('edit_title_'):]
            draft = draft[:-3]
            query.message.reply_text(f'Please enter the new title for the draft "{draft}":')
            user_state_handler.set_user_state('edit_title')
            user_state_handler.set_user_draft(draft)
        elif data.startswith('edit_content_'):
            draft = data[len('edit_content_'):]
            draft_path = os.path.join(BLOG_PATH, 'source/_drafts', draft)
            draft = draft[:-3]
            if os.path.exists(draft_path):
                with open(draft_path, 'r') as f:
                    content = f.readlines()[3:]
                content=''.join(content)
                query.message.reply_text(f'Current content:\n{content}\n\nPlease enter the new content for the draft "{draft}":')
                user_state_handler.set_user_state('edit_content')
                user_state_handler.set_user_draft(draft)
        else:
            handle_edit_choice(update, context, draft)
    elif data.startswith('delete_'):
        title = data[len('delete_'):]
        draft_path = os.path.join(BLOG_PATH, 'source/_drafts', title)
        if os.path.exists(draft_path):
            os.remove(draft_path)
            query.message.reply_text(f'Draft deleted: {title}')
    elif data.startswith('page_delete'):
        page_name = data[len('page_delete_'):]
        handle_page_delete_choice(update, context, page_name)

    elif data.startswith('confirm_push'):
        handle_push_choice(update, context)

    elif data.startswith('cancel_push'):
        query.message.reply_text('Push cancelled.')
