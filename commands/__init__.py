# __init__.py
# init.py for the commands folder
# By waymao in 2019

from . import basics, timetable, train_plan_graph, history, train_wifi12306, pids_realtime, station_timetable

handlers = [
    basics.start_handler,
    timetable.timetable_handler,
    timetable.timetable_shj_handler,
    train_plan_graph.graph_handler,
    history.train_info_handler,
    history.train_no_handler,
    train_wifi12306.train_handler,
    train_wifi12306.train_handler_short,
    pids_realtime.pids_handler,
    station_timetable.station_timetable_handler,
]
