from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, PicklePersistence, ConversationHandler
from sample import Handlers
from sample import States
from sample import Markups
import logging
import itertools

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
global logger
logger = logging.getLogger(__name__)
global TOKEN
TOKEN = "<UPDATE TOKEN HERE>"

global filename
filename = 'userdata'

def main():
    pp = PicklePersistence(filename=filename)
    updater = Updater(TOKEN, persistence=pp, use_context=True)
    dp = updater.dispatcher

    functions = States.functions
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', Handlers.start)],
        states={
            States.CHOOSING: [MessageHandler(Filters.regex('^(' + functions[0] + ')$'),
                                             Handlers.set_schedule),
                              MessageHandler(Filters.regex('^(' + functions[1] + ')$'),
                                             Handlers.track_weight),
                              MessageHandler(Filters.regex('^(' + functions[2] + ')$'),
                                             Handlers.track_snacking),
                              MessageHandler(Filters.regex('^(' + functions[3] + ')$'),
                                             Handlers.track_exercise),
                              MessageHandler(Filters.regex('^(' + functions[4] + ')$'),
                                             Handlers.show_data),
                            ],

            States.CHOOSING_SCHEDULE: [MessageHandler(Filters.regex("^(" + '|'.join(list(
                itertools.chain.from_iterable(Markups.schedule_keyboard))) + ")$"), Handlers.save_schedule),
                                       MessageHandler(Filters.text, Handlers.set_reminder_time)],
            States.TRACK_WEIGHT: [MessageHandler(Filters.regex("(?i)\s*[1-9]\d*(\.\d+)?(\s*(?i)kg)?\s*$"), Handlers.save_weight)],

            States.TRACK_SNACK: [MessageHandler(Filters.all, Handlers.save_snack)],

            States.GET_TIMEZONE: [MessageHandler(Filters.location, Handlers.set_time_zone),
                                  MessageHandler(Filters.text, Handlers.start)],

            States.REMINDER: [MessageHandler(Filters.regex("^(" + Markups.reminder_keyboard[0][0] + ")$"), Handlers.save_exercise),
                              MessageHandler(Filters.regex("^((?!" + Markups.reminder_keyboard[0][0] + ").)*$"), Handlers.get_excuse)]
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), Handlers.done)],
        name="my_conversation",
        persistent=True
    )

    dp.add_handler(conversation_handler)
    show_data_handler = CommandHandler('show_data', Handlers.show_data)
    dp.add_handler(show_data_handler)
    updater.job_queue.run_repeating(Handlers.callback_reminder, interval=3600, first=0)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
