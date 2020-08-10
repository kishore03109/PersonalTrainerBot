import pickle
import telegram
from datetime import datetime
from sample.__main__ import TOKEN


def send_reminder():
    with open('userdata','rb') as infile:
        user_data = pickle.load(infile)
        infile.close()

    data = user_data['user_data']
    for chat_id in data:
        print(chat_id)
        if "schedule" in data[chat_id] and "tz" in data[chat_id] and "reminder" in data[chat_id]:
            # required attributes are available to send reminder
            now = datetime.now(tz=data[chat_id]["tz"])

            if now.strftime("%A") in data[chat_id]["schedule"] and \
                    now.strftime("%H") == data[chat_id]["reminder"].split(":")[0]:
                # send for them to update workout
                bot = telegram.Bot(token=TOKEN)
                bot.sendMessage(chat_id=chat_id, text="Hey, just a reminder to update your "
                                "workout when you are done! :)")
