# query_time.py
# Used to search for timetable on 12306.
# By waymao in 2019

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from railroad_lib import query12306, query_railshj
from telegram import ParseMode
from telegram.ext.dispatcher import run_async
import requests, json
import logging
import pytz
from datetime import datetime

# Setting appropiate timezone.
tz = pytz.timezone('Asia/Shanghai')

#train_info = TrainNoDB()
#train_info.update()

# function timetable
# main handler for the command.
def timetable_unifier(update, context, source="12306"):
    # Check valid args:
    if len(context.args) == 0:
        # calendar_func(bot, update)
        update.message.reply_text(text="Please enter the train no. \
                The calendar function is being developed.",
            reply_to_message_id=update.message.message_id)
        return
    if len(context.args) == 1:
        date = datetime.now(tz).strftime("%Y-%m-%d")
    elif len(context.args) != 2:
        context.bot.send_message(chat_id=update.message.chat_id,
            text="Invalid arguments. Usage: `/tt <Train Number> (Date)`",
            reply_to_message_id=update.message.message_id)
        return
    else:
        date = context.args[1]

    # Loading...
    text = "Please wait while I retrieve the timetable..."
    msg = context.bot.send_message(chat_id=update.message.chat_id, text=text,
        reply_to_message_id=update.message.message_id)

    train = context.args[0]

    try:
        # Calling lfz's code
        if source == "railshj":
            train_data = query_railshj.get_train_detail(date, train)
            train_no = train_data[0].get("station_train_code")
        else:
            if len(train) > 10:
                train_no = train
            else:
                _train_no_list = query12306.getTrainNo(train, query_railshj.date_to_int(date))
                train_no = _train_no_list[0].get("train_no")
            train_data = query12306.getTimeList(train_no, date)

        # If no data returned, raise KeyError
        if not train_data:
            raise KeyError

        # First line
        result_str = "<pre>"

        train_class_name = train_data[0].get("train_class_name")
        if train_class_name:
            result_str += f"{train_class_name} "

        result_str += "{}\t{} ".format(
            train_no,
            query_railshj.date_to_string(date),
        )

        running_time = train_data[-1].get("running_time")
        if running_time:
            result_str += f"(全程 {running_time}) "
        arrive_day_str = train_data[0].get("arrive_day_str")
        if arrive_day_str:
            result_str += f"{arrive_day_str} "

        # detailed timetable
        for one_station in train_data:
            result_str += "\n"

            station_no = one_station.get("station_no")
            if station_no:
                result_str += "{} ".format(station_no)

            result_str += "{} \t {} \t {} {}".format(
                one_station.get("station_name").ljust(4, '　'),
                one_station.get("arrive_time"),
                one_station.get("start_time"),
                one_station.get("station_train_code"),
            )

        # Edit message, replace placeholder
        result_str += "</pre>"
        context.bot.edit_message_text(chat_id=update.message.chat_id, text=result_str, message_id=msg.message_id, parse_mode=ParseMode.HTML)

    # Error Handling.
    # KeyError: somehow 12306 returned something with status code != 200
    except (KeyError, IndexError, json.JSONDecodeError):
        context.bot.edit_message_text(chat_id=update.message.chat_id,
            text="Sorry, there is no such train no or the train does not run this day.",
            message_id=msg.message_id)
    # ConnectionError, Timeout: cannot access 12306
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        context.bot.edit_message_text(chat_id=update.message.chat_id,
            text="Sorry. Could not establish a secure connection to the 12306 server.",
            message_id=msg.message_id)
    # Not found or blocked?
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 404:
            # a guess
            context.bot.edit_message_text(chat_id=update.message.chat_id,
                text="Sorry, there is no such train no or the train does not run this day. (response code 404)",
                message_id=msg.message_id)
        else:
            context.bot.edit_message_text(chat_id=update.message.chat_id,
                text=f"Sorry. Could not establish a connection to the 12306 server. status code: {status_code}",
                message_id=msg.message_id)

    # Logs down each query.
    logging.info("User %s (id: %d) searched for train %s", update.message.from_user.username, update.message.from_user.id, train)

def timetable(update, context):
    return timetable_unifier(update, context, source="12306")

def timetable_shj(update, context):
    return timetable_unifier(update, context, source="railshj")

# Add handler for the functions.
timetable_handler = CommandHandler('tt', timetable, pass_args=True, run_async=True)
timetable_shj_handler = CommandHandler('tts', timetable_shj, pass_args=True, run_async=True)
