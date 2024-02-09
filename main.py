import time
from TOKEN import TOKEN, BOT_USERNAME
from scraper import get_title
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

post_text = None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global post_text
    await update.message.reply_text("Hello! Thanks for using our BOT")
    post_text = get_title()
    if post_text is not None:
        await update.message.reply_text(post_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("contact admin")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")


async def get_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_auto_update(update)


def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'start' not in processed:
        return 'Hey there! We are an automated bot so we cannot reply to you'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '')
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def handle_auto_update(update: Update):
    global post_text
    new_post_text = get_title()
    if new_post_text is not None and new_post_text != post_text:
        await update.message.reply_text(new_post_text)
        print(new_post_text)
        post_text = new_post_text

    time.sleep(5)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error: {context.error}')

if __name__ == '__main__':
    print('Starting bot')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('get_updates', get_updates))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error
    app.add_error_handler(error)

    # polling
    print("Polling")
    app.run_polling(poll_interval=3)
