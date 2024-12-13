
import logging
from datetime import datetime
import pytz
from telegram import ParseMode
from telegram.ext import CommandHandler
from railroad_lib import query_wifi12306


def parse_timetable_line(one_train):
    line = "%s(%s)" %(
        one_train.get('trainCode', '?'),
        one_train.get('trainNo', '?'),
    )

    if 'startStationName' in one_train and 'endStationName' in one_train:
        line += "(%s–%s)" % (one_train['startStationName'], one_train['endStationName'])
    arrive_time = one_train.get('arriveTime', '-')
    depart_time = one_train.get('departTime', '-')

    line += " %s/%s" % (arrive_time, depart_time)

    return f"`{line}`\n"


def parse_timetable(station_code, date):
    station_table = query_wifi12306.queryStoptimeByStationCode(station_code, date)

    answer = []
    if station_table and (station_table[0] != "NO_DATA"):
        result_str = "Timetable: \n"
        station_table.sort(key=lambda one_train:one_train.get('departTime'))
        for one_train in station_table:
            if len(result_str) > 4000 or result_str.count('\n') >= 100:
                answer.append(result_str)
                result_str = parse_timetable_line(one_train)
            else:
                result_str += parse_timetable_line(one_train)
        answer.append(result_str)
        return answer
    return []


def station_timetable(update, context):
    if len(context.args) <= 0:
        update.message.reply_text(
            "Usage: /station <Station Telecode> [Date]\n\nFor a list of station telecodes consult https://kyfw.12306.cn/otn/resources/js/framework/station_name.js",
            reply_to_message_id=update.message.message_id,)
        return
    elif len(context.args) > 2:
        context.bot.send_message(chat_id=update.message.chat_id,
            text="Invalid arguments. Usage: /station <Station Telecode> [Date]",
            reply_to_message_id=update.message.message_id)
        return
    if len(context.args) == 1:
        date = datetime.now(tz).strftime("%Y%m%d")
    else:
        date = query_wifi12306.date_to_integer(context.args[1])

    # Loading...
    text = "Please wait while I retrieve the station's timetable from wifi12306..."
    msg = context.bot.send_message(chat_id=update.message.chat_id, text=text,
        reply_to_message_id=update.message.message_id)

    try:
        station_code = context.args[0].upper()
        result_str = parse_timetable(station_code, date)


        # Edit message, replace placeholder
        context.bot.edit_message_text(chat_id=update.message.chat_id, text=result_str[0], message_id=msg.message_id, parse_mode=ParseMode.MARKDOWN_V2)

        if len(result_str) > 1:
            result_str.pop(0)
            for i in result_str:
                context.bot.send_message(chat_id=update.message.chat_id, text=i, parse_mode=ParseMode.MARKDOWN_V2, reply_to_message_id=msg.message_id)

        # Logs down each query.
        logging.info("User %s (id: %s) queryed for the station %s on %s.", update.message.from_user.username, update.message.from_user.id, station_code, date)
    except Exception as e:
        context.bot.edit_message_text(chat_id=update.message.chat_id, text="An error occurred: %s" % e, message_id=msg.message_id)


station_timetable_handler = CommandHandler('station', station_timetable, pass_args=True, run_async=True)
