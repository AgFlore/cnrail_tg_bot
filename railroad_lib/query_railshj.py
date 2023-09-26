# query_railshj.py
# looks for timetable on jk.railshj.com

import dateutil.parser
import requests

def date_to_string(date_input):
    return dateutil.parser.parse(date_input).strftime("%Y-%m-%d")

def get_train_detail(date, train_number: str):
    response = requests.post(
        url="https://jk.railshj.com/12306app/datasearch/bigscreen/getTrainDetail",
        json={"date": date_to_string(date), "trainNumber": train_number}, timeout=10
    ).json()

    if response['returnCode'] == '200' and response["success"]:
        data = response["data"]["data"]
        return [{k: v.strip() if isinstance(v, str) else v for k, v in stop.items()} for stop in data]


def test_module(label, response, answer):
    if (response==answer):
        print(f"Module {label}: Test OK.")
    else:
        print(f"Module {label} returns {response}")

if __name__ == '__main__':
    test_module("getTrainDetail", get_train_detail("20181001", "Z37"), [
        {'arrive_day_str': None, 'station_name': '北京西', 'train_class_name': None,  'is_start': None, 'service_type': None, 'end_station_name': '武昌', 'arrive_time': '20:46', 'start_station_name': '北京西', 'station_train_code': 'Z37', 'arrive_day_diff': '1', 'start_time': '20:46', 'station_no': None,  'wz_num': None, 'running_time': '00:00'},
        {'arrive_day_str': None, 'station_name': '武昌', 'train_class_name': None, 'is_start': None, 'service_type': None, 'end_station_name': None, 'arrive_time': '07:24', 'start_station_name': None, 'station_train_code': 'Z37','arrive_day_diff': None, 'start_time': '07:24', 'station_no': None, 'wz_num': None, 'running_time': '10:38'}
    ])
