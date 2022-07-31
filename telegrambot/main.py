import os
from uuid import uuid4
from telegram import Update, InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, InlineQueryHandler
from dotenv import load_dotenv

load_dotenv()

startText = "I'm TarotBot! You can get a tarot reading with /tarot, or update your settings with /settings. Get help with /help"

# When a user starts interaction with a bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=startText
    )

# For when an unknown command is sent
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=startText
    )

# TODO: edit settings
async def change_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


# TODO: conduct a reading
# TODO: inline query
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    # query = update.inline_query.query

    # if query == "":
    #     return

    results = [
        InlineQueryResultPhoto(
            id=str(uuid4()),
            photo_url=???,
            title=???
            description=???,
            caption=???
        )
    ]

    await update.inline_query.answer(
        results,
        switch_pm_text="Change Tarot Settings"
    )


def main():
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_API_TOKEN')).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('settings', change_settings))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(InlineQueryHandler(inline_query))

    # Should be the last handler
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    
    
    application.run_polling()

if __name__ == '__main__':
    main()