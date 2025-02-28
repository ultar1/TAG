import logging
import os
from telegram import Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import MessageHandler, Filters, CallbackQueryHandler
import psycopg2
from datetime import datetime, timedelta

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

# Define owner
OWNER_USERNAME = 'star_ies1'

# Define a few command handlers

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Group Commands", callback_data='group_commands')],
        [InlineKeyboardButton("Owner", url='https://t.me/star_ies1')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hi! I am your group management bot. Choose an option:', reply_markup=reply_markup)

# Group commands menu
def group_commands(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Sign In", callback_data='signin')],
        [InlineKeyboardButton("Balance", callback_data='balance')],
        [InlineKeyboardButton("Withdraw", callback_data='withdraw')],
        [InlineKeyboardButton("Help", callback_data='help')],
        [InlineKeyboardButton("Add", callback_data='add')],
        [InlineKeyboardButton("Remove", callback_data='remove')],
        [InlineKeyboardButton("List", callback_data='list')],
        [InlineKeyboardButton("Kick", callback_data='kick')],
        [InlineKeyboardButton("Pin", callback_data='pin')],
        [InlineKeyboardButton("Unpin", callback_data='unpin')],
        [InlineKeyboardButton("Mute", callback_data='mute')],
        [InlineKeyboardButton("Unmute", callback_data='unmute')],
        [InlineKeyboardButton("Stats", callback_data='stats')],
        [InlineKeyboardButton("Info", callback_data='info')],
        [InlineKeyboardButton("Antilink", callback_data='antilink')],
        [InlineKeyboardButton("Warn", callback_data='warn')],
        [InlineKeyboardButton("Ban", callback_data='ban')],
        [InlineKeyboardButton("Unban", callback_data='unban')],
        [InlineKeyboardButton("Promote", callback_data='promote')],
        [InlineKeyboardButton("Demote", callback_data='demote')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Choose a group command:', reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Available commands: /add, /remove, /list, /kick, /pin, /unpin, /mute, /unmute, /stats, /info, /antilink, /warn, /ban, /unban, /promote, /demote, /signin, /balance, /withdraw')

# Helper function to check if user is admin
def is_admin(update: Update) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    member = update.effective_chat.get_member(user_id)
    return member.status in ['administrator', 'creator']

# Group management commands
def add(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = context.args[0]
    update.message.reply_text(f'Add command for user {user_id}')

def remove(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = context.args[0]
    update.message.reply_text(f'Remove command for user {user_id}')

def list_members(update: Update, context: CallbackContext) -> None:
    members = [member.user.username for member in update.effective_chat.get_members()]
    update.message.reply_text(f'Members: {", ".join(members)}')

def kick(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = context.args[0]
    context.bot.kick_chat_member(update.effective_chat.id, user_id)
    update.message.reply_text(f'User {user_id} kicked.')

def pin(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        update.message.reply_to_message.pin()
        update.message.reply_text('Message pinned.')
    else:
        update.message.reply_text('Reply to a message to pin it.')

def unpin(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    context.bot.unpin_all_chat_messages(update.effective_chat.id)
    update.message.reply_text('All messages unpinned.')

def mute(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = context.args[0]
    context.bot.restrict_chat_member(update.effective_chat.id, user_id, ChatPermissions(can_send_messages=False))
    update.message.reply_text(f'User {user_id} muted.')

def unmute(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = context.args[0]
    context.bot.restrict_chat_member(update.effective_chat.id, user_id, ChatPermissions(can_send_messages=True))
    update.message.reply_text(f'User {user_id} unmuted.')

def stats(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Stats command')

def info(update: Update, context: CallbackContext) -> None:
    chat = update.effective_chat
    update.message.reply_text(f'Chat info: {chat.title}, {chat.id}')

def antilink(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Antilink command')

def warn(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = context.args[0]
    cursor.execute("INSERT INTO warnings (user_id) VALUES (%s) ON CONFLICT (user_id) DO UPDATE SET count = warnings.count + 1", (user_id,))
    conn.commit()
    update.message.reply_text(f'User {user_id} warned.')

def ban(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = context.args[0]
    context.bot.ban_chat_member(update.effective_chat.id, user_id)
    cursor.execute("INSERT INTO bans (user_id) VALUES (%s)", (user_id,))
    conn.commit()
    update.message.reply_text(f'User {user_id} banned.')

def unban(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = context.args[0]
    context.bot.unban_chat_member(update.effective_chat.id, user_id)
    cursor.execute("DELETE FROM bans WHERE user_id = %s", (user_id,))
    conn.commit()
    update.message.reply_text(f'User {user_id} unbanned.')

def promote(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = context.args[0]
    context.bot.promote_chat_member(update.effective_chat.id, user_id, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True)
    update.message.reply_text(f'User {user_id} promoted to admin.')

def demote(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    else:
        user_id = context.args[0]
    context.bot.promote_chat_member(update.effective_chat.id, user_id, can_change_info=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=False, can_promote_members=False)
    update.message.reply_text(f'User {user_id} demoted from admin.')

# Message handler for antilink
def handle_message(update: Update, context: CallbackContext) -> None:
    if 'http' in update.message.text:
        update.message.delete()
        update.message.reply_text('Links are not allowed!')

# Sign in command
def signin(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    cursor.execute("SELECT last_signin FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if result:
        last_signin = result[0]
        if datetime.now() - last_signin < timedelta(hours=24):
            update.message.reply_text('You can only sign in once every 24 hours.')
            return
    cursor.execute("INSERT INTO users (user_id, balance, last_signin) VALUES (%s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET balance = users.balance + 50, last_signin = %s", (user_id, 50, datetime.now(), datetime.now()))
    conn.commit()
    update.message.reply_text('You have signed in and received 50 NGN.')

# Balance command
def balance(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if result:
        balance = result[0]
        update.message.reply_text(f'Your balance is {balance} NGN.')
    else:
        update.message.reply_text('You have no balance.')

# Withdraw command
def withdraw(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    if context.args:
        user_id = context.args[0]
        amount = int(context.args[1])
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            balance = result[0]
            if balance >= amount and amount >= 1000:
                cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (amount, user_id))
                conn.commit()
                update.message.reply_text(f'User {user_id} has withdrawn {amount} NGN. New balance is {balance - amount} NGN.')
            else:
                update.message.reply_text('Insufficient balance or amount less than 1000 NGN.')
        else:
            update.message.reply_text('User not found.')
    else:
        update.message.reply_text('Usage: /withdraw <user_id> <amount>')

# Set welcome message command
def setwelcome(update: Update, context: CallbackContext) -> None:
    if not is_admin(update):
        update.message.reply_text('You are not authorized to use this command.')
        return
    chat_id = update.effective_chat.id
    welcome_message = ' '.join(context.args)
    cursor.execute("INSERT INTO settings (chat_id, welcome_message) VALUES (%s, %s) ON CONFLICT (chat_id) DO UPDATE SET welcome_message = %s", (chat_id, welcome_message, welcome_message))
    conn.commit()
    update.message.reply_text('Welcome message set.')

# Welcome new members
def welcome(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    cursor.execute("SELECT welcome_message FROM settings WHERE chat_id = %s", (chat_id,))
    result = cursor.fetchone()
    if result:
        welcome_message = result[0]
        for member in update.message.new_chat_members:
            update.message.reply_text(f'{welcome_message} {member.full_name}')

# Callback query handler
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'group_commands':
        group_commands(update, context)
    elif query.data == 'signin':
        signin(update, context)
    elif query.data == 'balance':
        balance(update, context)
    elif query.data == 'withdraw':
        withdraw(update, context)
    elif query.data == 'help':
        help_command(update, context)
    elif query.data == 'add':
        add(update, context)
    elif query.data == 'remove':
        remove(update, context)
    elif query.data == 'list':
        list_members(update, context)
    elif query.data == 'kick':
        kick(update, context)
    elif query.data == 'pin':
        pin(update, context)
    elif query.data == 'unpin':
        unpin(update, context)
    elif query.data == 'mute':
        mute(update, context)
    elif query.data == 'unmute':
        unmute(update, context)
    elif query.data == 'stats':
        stats(update, context)
    elif query.data == 'info':
        info(update, context)
    elif query.data == 'antilink':
        antilink(update, context)
    elif query.data == 'warn':
        warn(update, context)
    elif query.data == 'ban':
        ban(update, context)
    elif query.data == 'unban':
        unban(update, context)
    elif query.data == 'promote':
        promote(update, context)
    elif query.data == 'demote':
        demote(update, context)
    elif query.data == 'setwelcome':
        setwelcome(update, context)

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
    dispatcher.add_handler(CommandHandler("signin", signin))
    dispatcher.add_handler(CommandHandler("balance", balance))
    dispatcher.add_handler(CommandHandler("withdraw", withdraw))
    dispatcher.add_handler(CommandHandler("setwelcome", setwelcome))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    # Start the Bot
    port = int(os.environ.get('PORT', 443))
    updater.start_webhook(listen="0.0.0.0", port=port, url_path=token)
    updater.bot.set_webhook(f'https://{os.environ.get("HEROKU_APP_NAME")}.herokuapp.com/{token}')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
