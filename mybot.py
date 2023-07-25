import logging
import os
import sys

import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton,
                      ReplyKeyboardMarkup, TelegramError)

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

NO_TOKENS = 'Переменные окружения отсутствуют: {missed_tokens}'
TRY_MESSAGE = 'Попытка отправки сообщения'
STATUS_OF_MESSAGE = 'Сообщение: "{message}", {my_key}'
BOT_IS_WORKING = 'Бот работает'
WORK_WAS_ENDED = 'Работа бота не осуществляется'
HELLO_MESSAGE = 'Hello, i can describe and show the projects ' \
                'of my author - l8beOne'
ABOUT_ME = '/about_me'
MY_PROJECTS = '/my_projects'
TEXT_ABOUT_ME = 'I am a beginner developer and by creating ' \
                'this bot i can practice my knowledge'
TEXT_MY_PROJECTS = 'Вы выбрали "my_projects". Нажми на кнопку ниже, ' \
                   'чтобы перейти на GitHub и увидеть код данных проектов.'
ABOUT_ME_BOT = "AboutMeBot"
FOODGRAM = "Foodgram"
HOMEWORK_BOT = "HomeworkBot"
YATUBE = "Social Network Yatube"
REST_API_YATUBE = "REST API for Yatube"
YAMDB = "Проект YaMDb: отзывы пользователей на произведения"
URL_ABOUT_ME_BOT = "https://github.com/l8beOne/description_bot"
URL_FOODGRAM = "https://github.com/l8beOne/foodgram-project-react"
URL_HOMEWORK_BOT = "https://github.com/l8beOne/homework_bot"
URL_YATUBE = "https://github.com/l8beOne/hw05_final"
URL_REST_API_YATUBE = "https://github.com/l8beOne/api_final_yatube"
URL_YAMDB = "https://github.com/l8beOne/api_yamdb"


def check_tokens():
    """Проверка токенов."""
    missed_tokens = []
    for token_name in (
        'TELEGRAM_TOKEN',
        'TELEGRAM_CHAT_ID'
    ):
        if globals()[token_name] is None:
            missed_tokens.append(token_name)
            if len(missed_tokens) > 0:
                logging.critical(
                    NO_TOKENS.format(missed_tokens=missed_tokens)
                )
        else:
            return token_name


def send_message(bot, message):
    """Бот отправляет сообщение в чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(TRY_MESSAGE, exc_info=True)
    except TelegramError as error:
        my_value = f'не отправлено. {error}'
        logging.exception(
            STATUS_OF_MESSAGE.format(
                message=message,
                my_key=my_value),
            exc_info=True
        )
    else:
        my_value = 'отправлено.'
        logging.info(
            STATUS_OF_MESSAGE.format(message=message, my_key=my_value)
        )


def start(update, context):
    """Обработка кнопки start."""
    keyboard = [[MY_PROJECTS, ABOUT_ME]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(HELLO_MESSAGE, reply_markup=reply_markup)


def about_me(update, context):
    """Обработка кнопки about_me."""
    update.message.reply_text(TEXT_ABOUT_ME)


def my_projects(update, context):
    """Обработка кнопки my_projects."""
    label_to_url = {
        ABOUT_ME_BOT: URL_ABOUT_ME_BOT,
        FOODGRAM: URL_FOODGRAM,
        HOMEWORK_BOT: URL_HOMEWORK_BOT,
        YATUBE: URL_YATUBE,
        REST_API_YATUBE: URL_REST_API_YATUBE,
        YAMDB: URL_YAMDB
    }
    keyboard = [
        [InlineKeyboardButton(label, url)]
        for label, url in label_to_url.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(TEXT_MY_PROJECTS, reply_markup=reply_markup)


def main():
    """Основная логика работы бота."""
    logging.info(BOT_IS_WORKING)
    if not check_tokens():
        logging.critical(NO_TOKENS)
        sys.exit(WORK_WAS_ENDED)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    updater = Updater(token=TELEGRAM_TOKEN)
    try:
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(
            CommandHandler('my_projects', my_projects)
        )
        updater.dispatcher.add_handler(CommandHandler('about_me', about_me))
        updater.start_polling()
        updater.idle()
    except Exception as error:
        message = f'Сбой в работе программы: {error}'
        send_message(bot, message)
        logging.error(message)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='program.log',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    main()
