import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from config import TOKEN
from handlers import new_handler, edit_handler, delete_handler, page_delete_handler, push_handler, check_handler, button_handler, message_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", new_handler.start))
    dispatcher.add_handler(CommandHandler("new", new_handler.new))
    dispatcher.add_handler(CommandHandler("edit", edit_handler.edit))
    dispatcher.add_handler(CommandHandler("delete", delete_handler.delete))
    dispatcher.add_handler(CommandHandler("page_delete", page_delete_handler.page_delete))
    dispatcher.add_handler(CommandHandler("push", push_handler.push))
    dispatcher.add_handler(CommandHandler("check", check_handler.check))
    dispatcher.add_handler(CallbackQueryHandler(button_handler.button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler.handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()