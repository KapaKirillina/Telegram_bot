from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from telegram import Update
from bot_logic import bot, stats

# Обработка команды /start
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    pass

# Обработка команды /help_command
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def run_bot(update: Update, context: CallbackContext) -> None:
    replica = update.message.text
    answer = bot(replica)
    update.message.reply_text(answer)

    print(replica)
    print(answer)
    print()


with open('bot_token.txt', 'r') as file:
    BOT_TOKEN = file.read().strip()


def main():
    """Start the bot."""
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~ Filters.command, run_bot))

    # Start the Bot
    updater.start_polling()
    updater.idle()
