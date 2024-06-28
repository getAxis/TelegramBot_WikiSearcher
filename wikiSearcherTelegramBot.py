import wikipedia
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Класс для обработки запроса к Википедии
class WikiResponse:
    def __init__(self, query, num_sentences):
        self._query = query
        self._num_sentences = num_sentences
        wikipedia.set_lang("ru")
        self._summary = wikipedia.summary(self._query, sentences=self._num_sentences)
        self._page = wikipedia.page(self._query)

    def get_summary(self):
        return self._summary

    def get_page_url(self):
        return self._page.url

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Отправь мне запрос, и я найду информацию в Википедии.')

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: CallbackContext):
    user_query = update.message.text
    try:
        wiki_res = WikiResponse(user_query, 2)
        summary = wiki_res.get_summary()
        page_url = wiki_res.get_page_url()
        response_text = f'{summary}nnПолная статья: {page_url}'
    except wikipedia.exceptions.DisambiguationError as e:  
        response_text = f'Запрос неоднозначен. Возможные варианты: {", ".join(e.options)}'
    except wikipedia.exceptions.PageError:
        response_text = 'Статья не найдена.'
    except wikipedia.exceptions.WikipediaException as e:
        response_text = f'Произошла ошибка: {str(e)}'
    await update.message.reply_text(response_text)

# Основная функция для запуска бота
def main():
    # Вставь свой токен здесь
    TOKEN = '7298998177:AAHIvPLIKCAmOQiB1jq0vhNO-PIPa1PNryA'

    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Обработчики команды  start
    application.add_handler(CommandHandler("start", start))

    # Обработчик всех текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()





