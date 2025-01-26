import os
from telegram import Update
from telegram.ext import CallbackContext
from handlers.edit_handler import handle_edit_choice, handle_post_edit_choice
from handlers import user_state_handler
from handlers.page_delete_handler import handle_page_delete_choice
from handlers.push_handler import handle_push_choice

MESSAGEMAXLENGTH = 4096
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data
    if data.startswith('edit_'):
        draft = data[len('edit_'):]
        if data.startswith('edit_title_'):
            file_name = data[len('edit_title_'):]
            file_name = file_name[:-3]
            file_path = os.path.join("/app/bloger", 'source/_drafts', f'{file_name}.md')
            with open(file_path, 'r+') as f:
                content = f.readlines()
                draft = content[1]
                draft = draft[len('title: '):].strip()
            query.message.reply_text(f'Please enter the new title for the draft {file_name}.md.\n Title is "{draft}":')
            user_state_handler.set_user_state('edit_title')
            user_state_handler.set_user_file_name(file_name)
            user_state_handler.set_user_draft(draft)
        elif data.startswith('edit_content_'):
            file_name = data[len('edit_content_'):]
            file_name = file_name[:-3]
            user_state_handler.set_user_file_name(file_name)
            path = os.path.join("/app/bloger", 'source/_drafts', f'{file_name}.md')
            if os.path.exists(path):
                with open(path, 'r+') as f:
                    content = f.readlines()
                    draft = content[1]
                    draft = draft[len('title: '):].strip()
                    content = content[5:]
                content=''.join(content)
                if len(content) > MESSAGEMAXLENGTH:
                    query.message.reply_text(
                        f"File name is {user_state_handler.get_user_file_name()}.md\n"
                        "Content is too long to display in the chat. Sending the file instead..."
                    )
                    query.message.reply_document(open(path, 'rb'))
                else:
                    query.message.reply_text(
                        f"File name is {user_state_handler.get_user_file_name()}.md\n"
                        f"Title:\n{draft}\n"
                        f"Current content:\n{content}\n"
                        "Please enter the new content:"
                    )
                user_state_handler.set_user_state('edit_content')
                user_state_handler.set_user_draft(draft)
        else:
            handle_edit_choice(update, context, draft)
    elif data.startswith('delete_'):
        title = data[len('delete_'):]
        draft_path = os.path.join("/app/bloger", 'source/_drafts', title)
        if os.path.exists(draft_path):
            os.remove(draft_path)
            query.message.reply_text(f'Draft deleted: {title}')
    elif data.startswith('page_delete'):
        page_name = data[len('page_delete_'):]
        handle_page_delete_choice(update, context, page_name)
    elif data.startswith('post_edit'):
        post = data[len('post_edit_'):]
        if data.startswith('post_edit_title_'):
            file_name = data[len('post_edit_title_'):]
            file_name = file_name[:-3]
            file_path = os.path.join("/app/bloger", 'source/_posts', f'{file_name}.md')
            with open(file_path, 'r+') as f:
                content = f.readlines()
                post = content[1]
                post = post[len('title: '):].strip()
            query.message.reply_text(f'Please enter the new title for the draft "{file_name}.md.\nTitle is "{post}":')
            user_state_handler.set_user_state('post_edit_title')
            user_state_handler.set_user_post(post)
            user_state_handler.set_user_file_name(file_name)
        elif data.startswith('post_edit_content_'):
            file_name = data[len('post_edit_content_'):]
            file_name = file_name[:-3]
            user_state_handler.set_user_file_name(file_name)
            path = os.path.join("/app/bloger", 'source/_posts', f'{file_name}.md')
            if os.path.exists(path):
                with open(path, 'r+') as f:
                    content = f.readlines()
                    post = content[1]
                    post = post[len('title: '):].strip()
                    content = content[5:]
                content=''.join(content)
                if len(content) > MESSAGEMAXLENGTH:
                    query.message.reply_text(
                        f"File name is {user_state_handler.get_user_file_name()}.md\n"
                        "Content is too long to display in the chat. Sending the file instead..."
                    )
                    query.message.reply_document(open(path, 'rb'))
                else:
                    query.message.reply_text(
                        f"File name is {user_state_handler.get_user_file_name()}.md\n"
                        f"Title:\n{post}\n"
                        f"Current content:\n{content}\n"
                        "Please enter the new content:"
                    )
                user_state_handler.set_user_state('post_edit_content')
                user_state_handler.set_user_post(post)
        else:
            handle_post_edit_choice(update, context, post)
    elif data.startswith('confirm_push'):
        handle_push_choice(update, context)

    elif data.startswith('cancel_push'):
        query.message.reply_text('Push cancelled.')
