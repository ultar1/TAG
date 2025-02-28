import logging
import os
from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import MessageHandler, Filters
import psycopg2

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

# Define a few command handlers

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your group management bot.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Available commands: /add, /remove, /list, /kick, /pin, /unpin, /mute, /unmute, /stats, /info, /antilink, /warn, /ban, /unban, /promote, /demote')

# Group management commands
def add(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Add command')

def remove(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Remove command')

def list_members(update: Update, context: CallbackContext) -> None:
    members = [member.user.username for member in update.effective_chat.get_members()]
    update.message.reply_text(f'Members: {", ".join(members)}')

def kick(update: Update, context: CallbackContext) -> None:
    if context.args:
        user_id = context.args[0]
        context.bot.kick_chat_member(update.effective_chat.id, user_id)
        update.message.reply_text(f'User {user_id} kicked.')
    else:
        update.message.reply_text('Usage: /kick <user_id>')

def pin(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        update.message.reply_to_message.pin()
        update.message.reply_text('Message pinned.')
    else:
        update.message.reply_text('Reply to a message to pin it.')

def unpin(update: Update, context: CallbackContext) -> None:
    context.bot.unpin_all_chat_messages(update.effective_chat.id)
    update.message.reply_text('All messages unpinned.')

def mute(update: Update, context: CallbackContext) -> None:
    if context.args:
        user_id = context.args[0]
        context.bot.restrict_chat_member(update.effective_chat.id, user_id, ChatPermissions(can_send_messages=False))
        update.message.reply_text(f'User {user_id} muted.')
    else:
        update.message.reply_text('Usage: /mute <user_id>')

def unmute(update: Update, context: CallbackContext) -> None:
    if context.args:
        user_id = context.args[0]
        context.bot.restrict_chat_member(update.effective_chat.id, user_id, ChatPermissions(can_send_messages=True))
        update.message.reply_text(f'User {user_id} unmuted.')
    else:
        update.message.reply_text('Usage: /unmute <user_id>')

def stats(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Stats command')

def info(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    update.message.reply_text(f'Chat info: {chat.title}, {chat.id}')

def antilink(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Antilink command')

def warn(update: Update, context: CallbackContext) -> None:
    if context.args:
        user_id = context.args[0]
        cursor.execute("INSERT INTO warnings (user_id) VALUES (%s) ON CONFLICT (user_id) DO UPDATE SET count = warnings.count + 1", (user_id,))
        conn.commit()
        update.message.reply_text(f'User {user_id} warned.')
    else:
        update.message.reply_text('Usage: /warn <user_id>')

def ban(update: Update, context: CallbackContext) -> None:
    if context.args:
        user_id = context.args[0]
        context.bot.ban_chat_member(update.effective_chat.id, user_id)
        cursor.execute("INSERT INTO bans (user_id) VALUES (%s)", (user_id,))
        conn.commit()
        update.message.reply_text(f'User {user_id} banned.')
    else:
        update.message.reply_text('Usage: /ban <user_id>')

def unban(update: Update, context: CallbackContext) -> None:
    if context.args:
        user_id = context.args[0]
        context.bot.unban_chat_member(update.effective_chat.id, user_id)
        cursor.execute("DELETE FROM bans WHERE user_id = %s", (user_id,))
        conn.commit()
        update.message.reply_text(f'User {user_id} unbanned.')
    else:
        update.message.reply_text('Usage: /unban <user_id>')

def promote(update: Update, context: CallbackContext) -> None:
    if context.args:
        user_id = context.args[0]
        context.bot.promote_chat_member(update.effective_chat.id, user_id, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True)
        update.message.reply_text(f'User {user_id} promoted to admin.')
    else:
        update.message.reply_text('Usage: /promote <user_id>')

def demote(update: Update, context: CallbackContext) -> None:
    if context.args:
        user_id = context.args[0]
        context.bot.promote_chat_member(update.effective_chat.id, user_id, can_change_info=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=False, can_promote_members=False)
        update.message.reply_text(f'User {user_id} demoted from admin.')
    else:
        update.message.reply_text('Usage: /demote <user_id>')

# Message handler for antilink
def handle_message(update: Update, context: CallbackContext) -> None:
    if 'http' in update.message.text:
        update.message.delete()
        update.message.reply_text('Links are not allowed!')


def main() -> None:
    # Read the bot token from the environment variable
    token = os.getenv("TOKEN")
    if not token:
        logger.error("No token provided. Set the TOKEN environment variable.")
        return

    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("remove", remove))
    dispatcher.add_handler(CommandHandler("list", list_members))
    dispatcher.add_handler(CommandHandler("kick", kick))
    dispatcher.add_handler(CommandHandler("pin", pin))
    dispatcher.add_handler(CommandHandler("unpin", unpin))
    dispatcher.add_handler(CommandHandler("mute", mute))
    dispatcher.add_handler(CommandHandler("unmute", unmute))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("antilink", antilink))
    dispatcher.add_handler(CommandHandler("warn", warn))
    dispatcher.add_handler(CommandHandler("ban", ban))
    dispatcher.add_handler(CommandHandler("unban", unban))
    dispatcher.add_handler(CommandHandler("promote", promote))
    dispatcher.add_handler(CommandHandler("demote", demote))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
