import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

USERNAME, OFFICE, PLACE, PROBLEM = range(4)


def start(update, context):
    # reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Здравствуйте. Этот бот тех. поддержки.'
        'Отправьте /cancel для отмены.\n\n'
        'Просьба уточнить Ваш логин в сообщении:', reply_markup=ReplyKeyboardRemove())
        # reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return USERNAME


def username(update, context):
    reply_keyboard = [['Первый', 'Второй', 'Третий']]
    user = update.message.from_user
    logger.info("Username of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('В каком офисе вы находитесь?'
                              'если не знаете отправьте /skip',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return OFFICE


def office(update, context):
    reply_keyboard = [['Кабинет1', 'Кабинет1', 'Кабинет1']]
    user = update.message.from_user
    logger.info(f"Офис: {update.message.text}")
    update.message.reply_text('Просьба отправить кабинет.'
                              'или отправьте /skip если не знаете',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return PLACE


def skip_office(update, context):
    user = update.message.from_user
    logger.info("Don't not")
    update.message.reply_text('Незнаете где вы сидите?', reply_markup=ReplyKeyboardRemove())

    return PLACE


def place(update, context):
    user = update.message.from_user
    user_location = update.message.text
    logger.info(f'Number of cabinet is: {user_location}')
    update.message.reply_text('Опишите Вашу проблему:')

    return PROBLEM


def skip_place(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return PROBLEM


def problem(update, context):
    user = update.message.from_user
    logger.info(f"Pronlem: {update.message.text}")
    update.message.reply_text('Ваша проблема будет передана системному администратору')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Мы всегда будем рады',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1103159656:AAGJhmpijCeoxsQk1DZQfxKKgzv_VqdrLvI", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            USERNAME: [MessageHandler(Filters.text, username)],

            OFFICE: [MessageHandler(Filters.regex('^(Первый|Второй|Третий)$'), office), 
                    CommandHandler('skip', skip_office)],

            PLACE: [MessageHandler(Filters.regex('^(Кабинет1|Кабинет1|Кабинет1)$'), place),
                    CommandHandler('skip', skip_place)],

            PROBLEM: [MessageHandler(Filters.text, problem)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()