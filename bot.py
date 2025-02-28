import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi!')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')

# Group management commands
def add(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Add command')

def remove(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Remove command')

def list_members(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('List command')


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR_TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("remove", remove))
    dispatcher.add_handler(CommandHandler("list", list_members))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
