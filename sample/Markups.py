from sample import States
from telegram import ReplyKeyboardMarkup, KeyboardButton


functions = States.functions
main_keyboard = [[functions[0], functions[1]],
                  [functions[2], functions[3]],
                  [functions[4]]]
main_markup = ReplyKeyboardMarkup(main_keyboard, one_time_keyboard=True)

schedule_keyboard = [["Monday", "Tuesday", "Wednesday"],
                      ["Thursday", "Friday", "Saturday",],
                      ["Sunday", "Yup, that's all!"]]
schedule_markup = ReplyKeyboardMarkup(schedule_keyboard)

scale_keyboard = [['1', '2', '3', '4', '5']]
scale_markup = ReplyKeyboardMarkup(scale_keyboard, one_time_keyboard=True)

location_keyboard = [[KeyboardButton(text="send location", request_location=True), "I'll do this later"]]
location_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)

reminder_keyboard = [["Yes, I have done my workout for today!"],
                     ["I am going to take a break today!"]]
reminder_markup = ReplyKeyboardMarkup(reminder_keyboard, one_time_keyboard=True)


