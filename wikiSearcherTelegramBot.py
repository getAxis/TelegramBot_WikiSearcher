import wikipedia
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# A class for processing a Wikipedia request
class WikiResponse:
    def __init__(self, query, num_sentences):
        self._query = query
        self._num_sentences = num_sentences
        wikipedia.set_lang("en")
        self._summary = wikipedia.summary(self._query, sentences=self._num_sentences)
        self._page = wikipedia.page(self._query)

    def get_summary(self):
        return self._summary

    def get_page_url(self):
        return self._page.url

# The handler of the /start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Hi! Send me a request and I will find the information on Wikipedia')

# The handler of the text messages
async def handle_message(update: Update, context: CallbackContext):
    user_query = update.message.text
    try:
        wiki_res = WikiResponse(user_query, 2)
        summary = wiki_res.get_summary()
        page_url = wiki_res.get_page_url()
        response_text = f'{summary}nnПолная статья: {page_url}'
    except wikipedia.exceptions.DisambiguationError as e:  
        response_text = f'The request is ambiguous. Possible options: {", ".join(e.options)}'
    except wikipedia.exceptions.PageError:
        response_text = 'The article was not found.'
    except wikipedia.exceptions.WikipediaException as e:
        response_text = f'An error has occurred: {str(e)}'
    await update.message.reply_text(response_text)

# main func
def main():
    # Insert your token here
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

    # Creating of aplication
    application = Application.builder().token(TOKEN).build()

    # Handlers of the start command
    application.add_handler(CommandHandler("start", start))

    # The handler of the text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()





