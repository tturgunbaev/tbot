import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

USERNAME, OFFICE, PLACE, PROBLEM = range(4)

problems = []

def start(update, context):
    global problems
    problems = []
    
    update.message.reply_text(
        'Здравствуйте. Этот бот тех. поддержки.'
        'Отправьте /cancel для отмены.\n\n'
        'Просьба уточнить Ваш логин в сообщении:', reply_markup=ReplyKeyboardRemove())
     
    return USERNAME


def username(update, context):
    problems.append(f"Telegram username: @{update.message.from_user.username}")
    problems.append(f"Username: {update.message.text}")
    reply_keyboard = [['Первый', 'Второй', 'Третий']]
    user = update.message.from_user
    logger.info("Username of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('В каком офисе вы находитесь?'
                              'если не знаете отправьте /skip',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))

    return OFFICE


def office(update, context):
    problems.append(f"Офис: {update.message.text}")
    reply_keyboard = [['Кабинет1', 'Кабинет2', 'Кабинет3']]
    user = update.message.from_user
    logger.info(f"Офис: {update.message.text}")
    update.message.reply_text('Просьба отправить кабинет.'
                              'или отправьте /skip если не знаете',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))

    return PLACE


def skip_office(update, context):
    user = update.message.from_user
    logger.info("Don't not")
    update.message.reply_text('Незнаете где вы сидите?', reply_markup=ReplyKeyboardRemove())

    return PLACE


def place(update, context):
    problems.append(f"Место: {update.message.text}")
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
    problems.append(f"Описание: {update.message.text}")
    context.bot.send_message(chat_id=367951128, text="\n".join(problems))

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

    updater = Updater("1103159656:AAGJhmpijCeoxsQk1DZQfxKKgzv_VqdrLvI", use_context=True)


    dp = updater.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            USERNAME: [MessageHandler(Filters.text, username)],

            OFFICE: [MessageHandler(Filters.regex('^(Первый|Второй|Третий)$'), office), 
                    CommandHandler('skip', skip_office)],

            PLACE: [MessageHandler(Filters.regex('^(Кабинет1|Кабинет2|Кабинет3)$'), place),
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


    updater.idle()


if __name__ == '__main__':
    main()