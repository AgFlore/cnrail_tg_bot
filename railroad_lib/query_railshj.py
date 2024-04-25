# query_railshj.py
# looks for timetable on jk.railshj.com

import json
import base64
import time
import dateutil.parser
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA1, MD5

AES_KEY = '8ab0' + 'aa3e08b9' + 'ca4c'
cipher = AES.new(AES_KEY.encode('utf-8'), AES.MODE_ECB)

headers = {
    'version': 'WX-APPLET_1.3.15',
    'User-Agent': 'MicroMessenger XWEB/9115',
}


def date_to_string(date_input):
    return dateutil.parser.parse(date_input).strftime("%Y-%m-%d")


def date_to_int(date_input):
    return int(dateutil.parser.parse(date_input).strftime("%Y%m%d"))


def b64_JSONify(data: dict):
    return base64.b64encode(json.dumps(data, separators=(',', ':')).encode('utf-8'))


def signext(x: bytes):
    return SHA1.new(MD5.new(x).hexdigest().encode()).hexdigest()[6:26]


def request_shj(data: dict, endpoint: str):
    data_sorted = dict(sorted(data.items()))

    payload = {
        'signext': signext(b64_JSONify(data_sorted)),
        'timestampext': int(time.time() * 1000),
        **data_sorted,
    }

    encrypted_payload = cipher.encrypt(pad(b64_JSONify(payload), AES.block_size))

    response = requests.post(
        url="https://jk.railshj.com/12306app" + endpoint,
        json={'data': base64.b64encode(encrypted_payload).decode('utf-8')},
        timeout=10, headers=headers
    ).json()
    if response['returnCode'] == '200' and response["success"]:
        answer = base64.b64decode(response["data"])
        answer_decrypted = unpad(cipher.decrypt(bytes.fromhex(answer.decode())), AES.block_size)
        return json.loads(answer_decrypted.decode('utf-8'))

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
    if (response == answer):
        print(f"Module {label}: Test OK.")
    else:
        print(f"Module {label} returns {response}")


if __name__ == '__main__':

    test_module("getTrainDetail", get_train_detail("20220101", "Z38"), [
        {'start_station_name': '武昌', 'end_station_name': '北京西', 'arrive_day_diff': '1',

         'station_name': '武昌', 'station_train_code': 'Z38', 'arrive_time': '19:46', 'start_time': '19:46', 'running_time': '00:00'},
        {'station_name': '孝感', 'station_train_code': 'Z38', 'arrive_time': '20:40', 'start_time': '20:45', 'running_time': '0:54'},
        {'station_name': '北京西', 'station_train_code': 'Z38', 'arrive_time': '06:43', 'start_time': '06:43', 'running_time': '10:57'}
    ])
