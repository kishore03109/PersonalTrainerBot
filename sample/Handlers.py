from telegram import ReplyKeyboardRemove
from timezonefinder import TimezoneFinder
from sample.Excuse import Excuse
from sample.Exercise import Exercise
from sample.Snack import Snack
from sample.Weight import Weight
from pytz import timezone
from sample import States
from sample import Markups
from telegram.ext import ConversationHandler, CallbackContext
from sample.Reminder import send_reminder
import re


def set_time_zone(update, context):
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    tf = TimezoneFinder()
    tz = timezone(tf.timezone_at(lng=message.location.longitude, lat=message.location.latitude))
    context.user_data["tz"] = tz
    reply_text = "Got it, thanks!"
    update.message.reply_text(reply_text, reply_markup=Markups.main_markup)
    return States.CHOOSING


def set_schedule(update, context):
    if context.user_data and "schedule" in context.user_data:
        reply_text = "You are now updating your schedule, please type your new schedule"
        del context.user_data["schedule"]
    else:
        reply_text = "Ok, please enter your preferred schedule "
    update.message.reply_text(reply_text, reply_markup=Markups.schedule_markup)
    return States.CHOOSING_SCHEDULE


def save_schedule(update, context):
    text = update.message.text
    if "Yup, that's all!" != text:
        if context.user_data and "schedule" in context.user_data \
                and text not in context.user_data["schedule"]:
            current_schedule = context.user_data["schedule"]
            current_schedule.append(text)
            context.user_data["schedule"] = current_schedule
            return States.CHOOSING_SCHEDULE
        else:
            context.user_data["schedule"] = [text]
        print(type(update))
        return States.CHOOSING_SCHEDULE

    else:
        update.message.reply_text('Alright, I have updated your schedule for you! '
                                  'Your planned days to work out are: {}. Around what '
                                  'time do you normally intend to work out? (eg. enter 19:00 '
                                  'if you plan to workout at 7pm)'
                                  .format(", ".join(context.user_data["schedule"])),
                                  reply_markup=ReplyKeyboardRemove())
        return States.CHOOSING_SCHEDULE


def set_reminder_time(update,context):
    text = update.message.text
    regex = r"^\s*([0-1]?[0-9]|2[0-3]):[0-5][0-9]\s*$"

    if context.user_data["tz"] is None:
        reply_text = "Hey, I have realised you have yet to set your time-zone. " \
                     "I cannot properly send you reminders without it :( " \
                     "Would you like to set it up now?"
        context.user_data["reminder"] = text
        update.message.reply_text(reply_text, reply_markup=Markups.location_markup)
        return States.GET_TIMEZONE

    elif re.match(regex, text):
        context.user_data["reminder"] = text
        reply_text = "Alright, I have noted it down."
        update.message.reply_text(reply_text, reply_markup=Markups.main_markup)
        return States.CHOOSING

    else:
        reply_text = "Opps, please write the time like '13:00' if you intend to work out at 1pm"
        update.message.reply_text(reply_text)
        return States.GET_TIMEZONE


def track_weight(update, context):
    update.message.reply_text("Enter your weight in kg, for example: 54.5")
    return States.TRACK_WEIGHT


def save_weight(update, context):
    text = update.message.text.strip()
    print(text)
    if text[-2:].lower() == "kg":
        text = text[:-2]
    tz = context.user_data["tz"]
    current_weight = Weight(text, tz=tz)
    if "weight" in context.user_data:
        context.user_data["weight"].append(current_weight)
    else:
        context.user_data["weight"] = [current_weight]
    update.message.reply_text('Alright, I have updated your current weight of :'
                              ' {}kg'.format(context.user_data["weight"][-1].value), reply_markup=Markups.main_markup)
    return States.CHOOSING


def track_snacking(update,context):
    update.message.reply_text("Try to be as descriptive as you can, best if you know the exact quantity "
                              "the meal. Eg. 2 slices of wholemeal bread with peanut butter")
    return States.TRACK_SNACK


def save_snack(update,context):
    text = update.message.text # could be either hunger_level or description
    tz = context.user_data["tz"]
    if "snack" in context.user_data:
        last_snack = context.user_data["snack"][-1]
        if last_snack.hunger_level is None:
            last_snack.hunger_level = text
            context.user_data["snack"][-1] = last_snack
            update.message.reply_text(text='Alright, I have updated your latest snack', reply_markup=Markups.main_markup)
            return States.CHOOSING
        else:
            snack = Snack(text,None,tz=tz)
            context.user_data["snack"].append(snack)

    else:
        snack = Snack(text, None,tz=tz)
        context.user_data["snack"] = [snack]
    update.message.reply_text(text='On a scale of 1 to 5, how hungry were you prior to eating this snack? '
                                   '(With 1 being "Meh, the food looked good and colourful" to 5 being "I am '
                                   'so hungry I would enjoy eating hostel food right now"', reply_markup=Markups.scale_markup)
    return States.TRACK_SNACK


def callback_reminder(context: CallbackContext):
    send_reminder()

def track_exercise(update, context):
    update.message.reply_text(text="Hey, have you done your exercise that you planned for today?",
                              reply_markup=Markups.reminder_markup)
    return States.REMINDER


def get_excuse(update, context):
    text = update.message.text
    if text == Markups.reminder_keyboard[-1][0]:
        update.message.reply_text(text="Oh no :( What happened?")
        return States.REMINDER
    else:
        if "tz" in context.user_data:
            excuse = Excuse(text, tz=context.user_data["tz"])
        else:
            excuse = Excuse(text)
        if "excuse" in context.user_data:
            context.user_data["excuse"].append(excuse)
        else:
            context.user_data["excuse"] = [excuse]
        update.message.reply_text(text="That's alright, try not to miss your schedule the next time",
                                  reply_markup=Markups.main_markup)
        return States.CHOOSING


def save_exercise(update, context):
    tz = context.user_data["tz"]
    current_exercise = Exercise(tz)
    if "exercise" in context.user_data :
        if context.user_data["exercise"][-1] != current_exercise: # prevent multiple tracking of exercise in the same day
            context.user_data["exercise"].append(current_exercise)

    else:
        context.user_data["exercise"] = [current_exercise]

    update.message.reply_text("Good job in completing your workout for today!", reply_markup=Markups.main_markup)
    return States.CHOOSING


def start(update, context):
    user = update.message.from_user
    name = user.first_name
    reply_text = "Hi " + name + "! "
    if context.user_data:
        reply_text = "What would you like to do now?"
    else:
        reply_text += "I am a personal fitness trainer bot, it is nice to meet you!" \
                      "I am here to help you achieve your fitness goals! Before we proceed, " \
                      "I would like to know your time zone. Can I please get your location?"

        context.user_data["tz"] = None  # Tz is set to none unless user gives gives location
        update.message.reply_text(reply_text, reply_markup=Markups.location_markup)
        return States.GET_TIMEZONE

    update.message.reply_text(reply_text,reply_markup=Markups.main_markup)
    return States.CHOOSING


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        if key == "tz":
            if user_data["tz"] is None:
                facts.append("You have yet to set your timezone :(")
            else:
                facts.append("Your timezone is " + str(user_data['tz']))
        elif key == "weight":
            facts.append("Your recorded weights are ")
            for weight in user_data["weight"]:
                facts.append(weight.datetime + " : " + weight.value)
        elif key == "reminder":
            facts.append("You usually exercise at " + user_data["reminder"] + " on " + ','.join(user_data["schedule"]))
        elif key == "exercise":
            facts.append("Here is a list days you exercised : ")
            for exercise in user_data['exercise']:
                facts.append(str(exercise)[10:-1])
        elif key == "excuse":
            facts.append("Here are the reasons in which you missed out on exercising : ")
            for excuse in user_data["excuse"]:
                facts.append(excuse.datetime + " - " + excuse.text)
    return "\n".join(facts)


def show_data(update, context):
    update.message.reply_text("This is what you already told me:\n"
                              "{}".format(facts_to_str(context.user_data)), reply_markup=Markups.main_markup)
    return States.CHOOSING


def done(update, context):
    if 'choice' in context.user_data:
        del context.user_data['choice']

    update.message.reply_text("I learned these facts about you:\n"
                              "{}"
                              "\nPlease type /start to use me again!".format(facts_to_str(context.user_data)))
    return ConversationHandler.END
