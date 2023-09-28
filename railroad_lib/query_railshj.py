# query_railshj.py
# looks for timetable on jk.railshj.com

import dateutil.parser
import requests

def date_to_string(date_input):
    return dateutil.parser.parse(date_input).strftime("%Y-%m-%d")

def date_to_int(date_input):
    return int(dateutil.parser.parse(date_input).strftime("%Y%m%d"))

def request_shj(data: dict, endpoint: str):
    response = requests.post(
        url="https://jk.railshj.com/12306app" + endpoint,
        json=data, timeout=10
    ).json()
    if response['returnCode'] == '200' and response["success"]:
        return response["data"]
    else:
        # record error
        return None

def get_train_detail(date, train_number: str):
    response = request_shj(data={
        "date": date_to_string(date),
        "trainNumber": train_number
    }, endpoint="/datasearch/bigscreen/getTrainDetail")

    if response.get("data"):
        data = response["data"]
        return [{k: v.strip() if isinstance(v, str) else v for k, v in stop.items()} for stop in data]


def get_all_stations():
    return request_shj(endpoint="/datasearch/bigscreen/getTeleStation", data={})
    ''' {'initial': 'H', 'fullCode': 'heijing',  'stationName': '黑井', 'stationCode': 'HIM',  'longitude': None, 'latitude': None}'''

def get_bigscreen_stations():
    return request_shj(endpoint="/datasearch/bigscreen/getStations", data={})
    ''' {'stationName': '北京西', 'stationCode': 'BXP', 'stationTelecode': 'BXP', 'longitude': '116.327', 'latitude': '39.901'}'''

def get_train_state(train_number):
    return request_shj({
        "trainNumber": train_number
    }, endpoint="/datasearch/bigscreen/getStationTrainState")

def get_station_to_station(date, station_left_code, station_right_code):
    return request_shj({
        "date": date_to_int(date),
        "startStationTeleCode": station_left_code,
        "arriveStationTeleCode": station_right_code
    }, endpoint="/datasearch/bigscreen/getStationToStation")

'''
getBigscreenStations:function(e){return(0,n.request)({header:(0,n.header)(),url:this.baseUrl+"/datasearch/bigscreen/getStations",data:e,method:"POST",noShow:!0})}
station.getBigscreenStations({})

getWaitStationTrains:function(e){return(0,n.request)({header:(0,n.header)(),url:this.baseUrl+"/datasearch/bigscreen/getWaitStationTrains",data:e,method:"POST",noShow:!0})}
getWaitStationTrains({stationCode:this.stationCode})

getArriveStationTrains:function(e){return(0,n.request)({header:(0,n.header)(),url:this.baseUrl+"/datasearch/bigscreen/getArriveStationTrains",data:e,method:"POST",noShow:!0})}
getArriveStationTrains({stationCode:this.stationCode})

getStationTrainState:function(e){return(0,n.request)({header:(0,n.header)(),url:this.baseUrl+"/datasearch/bigscreen/getStationTrainState",data:e,method:"POST",noShow:!0})}
getStationTrainState({trainNumber:this.trainNumber})

getStationToStation:function(e){return(0,n.request)({header:(0,n.header)(),url:this.baseUrl+"/datasearch/bigscreen/getStationToStation",data:e,method:"POST",noShow:!0})}
getStationToStation({date:this.train_date_2.split("-").join(""),startStationTeleCode:this.stationLeftCode,arriveStationTeleCode:this.stationRightCode})

getTrain_no:function(e){return(0,n.request)({header:(0,n.header)(),url:"https://search.12306.cn/search/v1/train/search",data:e,method:"GET",noShow:!0})}
getTrain_no({keyword:this.trainNumber,date:this.$time.timestampToDate_Num(parseInt(this.$time.getNowTimestamp()))})

'''

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
