# query_wifi12306.py
# looks for timetable on com.wifi12306.
# Modified by AgFlore from lfz's version

import json
import requests
import dateutil.parser

header = {
    'Host': 'wifi.12306.cn',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'appName': 'zhongtiexing',
    'appVer': '5.1.0',
    'accessToken': '',
    'Referer': 'https://servicewechat.com/wx4e4bb9a3f684dd0a/112/page-frame.html',
    'Accept-Encoding': 'gzip, deflate, br'
}

def json_parser(rawData):
    data={}
    try:
        data = json.loads(rawData)['data']
    except:
        return ['NO_DATA', rawData]
    return data

def date_to_string(date_input):
    return dateutil.parser.parse(date_input).strftime("%Y-%m-%d")

def date_to_integer(date_input):
    return dateutil.parser.parse(date_input).strftime("%Y%m%d")

def getTrainListFromToStationName(queryDate,fromStationName,toStationName) -> list:
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/stoptime/queryByStationName?fromStationName=%s&toStationName=%s&trainDate=%s "%(fromStationName,toStationName,queryDate), headers=header)
    return json_parser(response.content.decode('utf-8'))

def queryTrainTicketPriceList(startStationCode, endStationCode, trainDate, ticketType=1) -> list:
    '''
        queryTrainTicketPriceList('BJP', 'VIH', '2021-10-01') returns
        [{'trainNo': '24000K16130C', 'softSeat': '--', 'hardBerth': '02150', 'motorCarBerth': '--', 'softBerth': '03360', 'firstBreth': '--', 'secondBreth': '--', 'firstClassSeats': '--', 'secondClassSeat': '--', 'highGradeSoftBerth': '--', 'businessAndSpecialSeat': '--', 'noSeat': '01240', 'hardSeat': '01240', 'distance': 942, 'fromStationTelecode': 'BJP', 'toStationTelecode': 'VIH'}, {'trainNo': '24000G258710', 'softSeat': '--', 'hardBerth': '--', 'motorCarBerth': '--', 'softBerth': '--', 'firstBreth': '--', 'secondBreth': '--', 'firstClassSeats': '--', 'secondClassSeat': '--', 'highGradeSoftBerth': '--', 'businessAndSpecialSeat': '--', 'noSeat': '--', 'hardSeat': '--', 'distance': 792, 'fromStationTelecode': 'VNP', 'toStationTelecode': 'XYU'}]
    '''
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/trainTicketList/queryTrainTicketPriceList?startStationCode=%s&endStationCode=%s&trainDate=%s&ticketType=%s"%(startStationCode, endStationCode, trainDate, ticketType), headers=header)
    return json_parser(response.content.decode('utf-8'))

def getFuxingTrain():
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/trainType/getRevivalTrain", headers=header)
    return json_parser(response.content.decode('utf-8'))


def getStoptimeByStationName(fromStationName, toStationName, trainDate) -> list:
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/stoptime/queryByStationName?fromStationName=%s&toStationName=%s&trainDate=%s"%(fromStationName, toStationName, trainDate), headers=header)
    return json_parser(response.content.decode('utf-8'))

def getStoptimeByTrainCode(trainCode, trainDate, getBigScreen='YES') -> list:
    '''
    Note: Use 'yyyymmdd' only. Query with 'yyyy-mm-dd' could return expired data.
    '''
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/stoptime/queryByTrainCode?trainCode=%s&trainDate=%s&getBigScreen=%s"%(trainCode, trainDate, getBigScreen), headers=header)
    return json_parser(response.content.decode('utf-8'))

def queryStoptimeByStationCode(stationCode, trainDate):
    '''
    Note: Use 'yyyymmdd' only. Query with 'yyyy-mm-dd' could return expired data.
    Only data after 2021-01-20 include infomation about trains' start/end stations.
    '''
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/stoptime/queryByStationCodeAndDate?stationCode=%s&trainDate=%s"%(stationCode, trainDate), headers=header)
    return json_parser(response.content.decode('utf-8'))

def getRunRuleByTrainNoAndDateRange(trainNo, start, end):
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/trainDetailInfo/queryTrainRunRuleByTrainNoAndDateRange?trainNo=%s&start=%s&end=%s"%(trainNo, start, end), headers=header)
    return json_parser(response.content.decode('utf-8'))

def getTrainEquipmentByTrainNo(trainNo) -> list:
    '''
    Sample: [{'eId': 157047494, 'bureaName': '京', 'trainsetType': 'CRH6F-A', 'trainsetName': 'CRH6F-A-0494', 'deploydepotName': '京动', 'depotName': '北京北所', 'trainsetStatus': '载客运行', 'date': '2021-10-03'}]
    Only matches the current trainCode from trainNo, and returns the current status; will answer to even non-existent trainNo like '24000000G199'.
    '''
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/trainDetailInfo/queryTrainEquipmentByTrainNo?trainNo=%s"%trainNo, headers=header)
    return json_parser(response.content.decode('utf-8'))

def getTrainCompileListByTrainNo(trainNo) -> list:
    '''
        queryTrainCompileListByTrainNo('800000D9300A') returns
        [{'startDate': '20190105', 'trainNo': '800000D9300A', 'coachNo': '01', 'stopDate': '20401231', 'coachType': 'RW    ', 'limit1': 40, 'limit2': 0, 'commentCode': ' ', 'trainGroupNo': 0, 'origin': 'M1', 'runningStyle': 1, 'runningRule': 1, 'seatFeature': '3'}, {'startDate': '20190105', 'trainNo': '800000D9300A', 'coachNo': '02', 'stopDate': '20401231', 'coachType': 'RW    ', 'limit1': 60, 'limit2': 0, 'commentCode': ' ', 'trainGroupNo': 0, 'origin': 'M1', 'runningStyle': 1, 'runningRule': 1, 'seatFeature': '3'}, ...]
    '''
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/trainDetailInfo/queryTrainCompileListByTrainNo?trainNo=%s"%trainNo, headers=header)
    return json_parser(response.content.decode('utf-8'))

# For interpreting the "seatFeature"
seat_feature_dict = {
    '0': '非空',
    '3': '新空',
}

coach_type_dict = {
    'CA': '餐车',
    'FD': '发电车',
    'GR': '高级软卧车',
    'KD': '空调发电车',
    'PC': '棚车',
    'RW': '软卧车',
    'RYW': '软硬卧车',
    'RYZ': '软硬座车',
    'RZ': '软座车',
    'RZ1': '一等软座车',
    'RZ2': '二等软座车',
    'SRW': '双层软卧车',
    'SRZ': '双层软座车',
    'SYW': '双层硬卧车',
    'SYZ': '双层硬座车',
    'UZ': '邮政车',
    'XL': '行李车',
    'XU': '行邮车',
    'YW': '硬卧车',
    'YZ': '硬座车',
    'RZXL': '软座行李',
    'RZBB': '一等半包',
    'JYYZ': '简易硬座',
}

# For interpreting the "commentCode"
# TBA:
# 'A' appeared in 280000818702 and 270000881707 (YZ25B, capacity=116).
# 'F' appeared in 280000818702 and 270000881707 (YZ25B, capacity=106).
# 'J' appeared once in 12000K12270V (YZ25G, capacity=108)
# 'M' appeared in 4a000070051A (CA, capacity=0), 410000700312 (YW25G, capacity=36)
# '.' appeared in 43000K82210K (YW25G, capacity=66)
# '0' appeared once in 190000K4300S (YZ25G, capacity=118)
compile_comment_dict = {
    'B': '㊙️宿营车',
    'C': '🎙️带广播室',
    'D': '👮‍♀️带列车长办公席',
    'E': '㊙️🎙️宿营车+广播室',
    'H': '➡️联运出境',
    'I': '↩️回转',
    'K': '👮‍♀️🎙️广播室+办公席',
    'L': '❌欠编',
    'N': '♿️无障碍',
    'O': '🎙️♿️无障碍+广播室',
    'P': '👮‍♀️♿️无障碍+办公席',
    'Q': '🤫静音车厢'
}
# For interpreting the "origin". First digit is bureau, second digit represents 直通/管内.
bureau_dict = {
    'B': '哈局',
    'C': '呼局',
    'D': '锦局', 'L': '吉局', 'T': '沈局',
    'F': '郑局',
    'G': '南局', 'S': '福局',
    'H': '上局', 'U': '新上局',
    'J': '兰局',
    'K': '济局', 'I': '济局',
    'M': '昆局',
    'N': '武局',
    'O': '青藏',
    'P': '京局',
    'Q': '广铁', 'A': '新广铁',
    'R': '乌局',
    'V': '太局',
    'W': '成局', 'E': '新成局',
    'X': '境外',
    'Y': '西局',
    'Z': '宁局'
}

def queryPreseqTrainsByTrainCode(trainCode, trainDate):
    '''
    Note: only the current plan for the given trainCode is returned, even if you query for an earlier date where the current plan does not apply.
    '''
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/preSequenceTrain/getPreSequenceTrainInfo?trainCode=%s&trainDate=%s"%(trainCode, trainDate), headers=header)
    return json_parser(response.content.decode('utf-8'))

def getTrainsetTypeByTrainCode(trainCode):
    response = requests.get("https://wifi.12306.cn/wifiapps/ticket/api/trainDetailInfo/getTrainsetTypeByTrainCode?trainCode=%s"%trainCode, headers=header)
    return json_parser(response.content.decode('utf-8'))

def getBigScreenByLocation(latitude, longitude, DA_type='D'):
    response = requests.get("https://wifi.12306.cn/wifiapps/appFrontEnd/v2/kpBigScreen/getBigScreenByLocation?latitude=%s&longitude=%s&type=%s"%(latitude, longitude, DA_type), headers=header)
    return json_parser(response.content.decode('utf-8'))

def getBigScreenByStationCodeAndDate(stationCode, queryDate, DA_type='A') -> list:
    '''
    queryDate must be "yyyymmdd"
    status: 1=正在候车, 2=正在检票, 3=停检, 4=正点, 5=晚点, 6=预计晚点, 7=已到站, 8=停运
    '''
    response = requests.get("https://wifi.12306.cn/wifiapps/appFrontEnd/v2/kpBigScreen/getBigScreenByStationCodeAndTrainDate?stationCode=%s&trainDate=%s&type=%s"%(stationCode, queryDate, DA_type), headers=header)
    return json_parser(response.content.decode('utf-8'))

# For interpreting "status"
bigscreen_status_dict = {1:'候车', 2:'开检', 3:'停检', 4:'正点', 5:'晚点', 6:'预计晚点', 7:'到站', 8:'停运'}

def test_module(label, response, answer):
    if (response==answer):
        print("Module %s: Test OK."%label)
    else:
        print("Module %s returns %s"%(label, response))

if __name__ == '__main__':
    test_module("getTrainListFromToStationName", getTrainListFromToStationName('202110-01','十渡','奇峰塔'), [{'fromStationCode': 'SEP', 'fromStationName': '十渡', 'fromStationDate': '202110-01 ', 'fromStationArriveTime': '2005', 'fromStationDepartTime': '2007', 'fromStationArriveDateTime': 1633055100000, 'fromStationDepartDateTime': 1633055220000, 'fromStationNo': '10', 'fromTrainCode': '6437', 'isStartStation': False, 'fromStationDistance': 92, 'toStationCode': 'QVP', 'toStationName': '奇峰塔', 'toStationArriveTime': '2143', 'toStationDepartTime': '2145', 'toStationDate': '202110-01 ', 'toStationArriveDateTime': 1633063380000, 'toStationDepartDateTime': 1633063500000, 'toStationNo': '18', 'toTrainCode': '6437', 'trainNo': '24000064370K', 'isEndStation': False, 'toStationDistance': 149, 'dayDifference': 0, 'travelDistance': 57, 'travelTimeSpan': 8160000}])

    # test_module("getStoptimeByStationName", getStoptimeByStationName('深圳', '苏州', '20211003'), [{'fromStationCode': 'IOQ', 'fromStationName': '深圳北', 'fromStationDate': '20211003', 'fromStationArriveTime': '0950', 'fromStationDepartTime': '0950', 'fromStationArriveDateTime': 1633225800000, 'fromStationDepartDateTime': 1633225800000, 'fromStationNo': '01', 'fromTrainCode': 'D2282', 'isStartStation': True, 'fromStationDistance': 0, 'toStationCode': 'SZH', 'toStationName': '苏州', 'toStationArriveTime': '2153', 'toStationDepartTime': '2155', 'toStationDate': '20211003', 'toStationArriveDateTime': 1633269180000, 'toStationDepartDateTime': 1633269300000, 'toStationNo': '28', 'toTrainCode': 'D2282', 'trainNo': '6i000D22820F', 'isEndStation': False, 'toStationDistance': 1707, 'dayDifference': 0, 'travelDistance': 1707, 'travelTimeSpan': 43380000, 'controlledTrainFlag': '0', 'controlledTrainMessage': '正常车次，不受控'}, {'fromStationCode': 'SZQ', 'fromStationName': '深圳', 'fromStationDate': '20211003', 'fromStationArriveTime': '1206', 'fromStationDepartTime': '1206', 'fromStationArriveDateTime': 1633233960000, 'fromStationDepartDateTime': 1633233960000, 'fromStationNo': '01', 'fromTrainCode': 'K34', 'isStartStation': True, 'fromStationDistance': 0, 'toStationCode': 'SZH', 'toStationName': '苏州', 'toStationArriveTime': '1152', 'toStationDepartTime': '1152', 'toStationDate': '20211004', 'toStationArriveDateTime': 1633319520000, 'toStationDepartDateTime': 1633319520000, 'toStationNo': '15', 'toTrainCode': 'K35', 'trainNo': '6500000K3409', 'isEndStation': True, 'toStationDistance': 1725, 'dayDifference': 1, 'travelDistance': 1725, 'travelTimeSpan': 85560000, 'controlledTrainFlag': '0', 'controlledTrainMessage': '正常车次，不受控'}])
    test_module("getStoptimeByStationName", getStoptimeByStationName('十渡', '奇峰塔', '20211003'), [{'fromStationCode': 'SEP', 'fromStationName': '十渡', 'fromStationDate': '20211003', 'fromStationArriveTime': '2005', 'fromStationDepartTime': '2007', 'fromStationArriveDateTime': 1633262700000, 'fromStationDepartDateTime': 1633262820000, 'fromStationNo': '10', 'fromTrainCode': '6437', 'isStartStation': False, 'fromStationDistance': 92, 'toStationCode': 'QVP', 'toStationName': '奇峰塔', 'toStationArriveTime': '2143', 'toStationDepartTime': '2145', 'toStationDate': '20211003', 'toStationArriveDateTime': 1633268580000, 'toStationDepartDateTime': 1633268700000, 'toStationNo': '18', 'toTrainCode': '6437', 'trainNo': '24000064370K', 'isEndStation': False, 'toStationDistance': 149, 'dayDifference': 0, 'travelDistance': 57, 'travelTimeSpan': 5760000}])
    # querying with yyyy-mm-dd is deprecated, see:
    test_module("getStoptimeByTrainCode", getStoptimeByTrainCode('Z29', '2021-09-30'), [{'trainDate': '2021-09-30', 'startDate': '20201012', 'stopDate': '20210119', 'trainNo': '2400000Z290F', 'stationNo': '01', 'stationName': '北京', 'bureauCode': 'P', 'stationTelecode': 'BJP', 'stationTrainCode': 'Z29', 'dayDifference': 0, 'arriveTime': '2133', 'arriveTimestamp': 1607560380000, 'startTime': '2133', 'startTimestamp': 1607560380000, 'ticketDelay': 0, 'waitingRoom': '-', 'wicket': '-', 'distance': 0, 'timeSpan': 0, 'oneStationCrossDay': False}, {'trainDate': '20201210', 'startDate': '20201012', 'stopDate': '20210119', 'trainNo': '2400000Z290F', 'stationNo': '02', 'stationName': '扬州', 'bureauCode': 'H', 'stationTelecode': 'YLH', 'stationTrainCode': 'Z29', 'dayDifference': 1, 'arriveTime': '0800', 'arriveTimestamp': 1607558400000, 'startTime': '0800', 'startTimestamp': 1607558400000, 'ticketDelay': 0, 'waitingRoom': '-', 'wicket': '-', 'distance': 1228, 'timeSpan': 37620000, 'oneStationCrossDay': False}])
    # where the correct query goes
    test_module("getStoptimeByTrainCode_Correct", getStoptimeByTrainCode('Z29', '20210930'), [{'trainDate': '20210930', 'startDate': '20210120', 'stopDate': '20501231', 'trainNo': '2400000Z290G', 'stationNo': '01', 'stationName': '北京', 'bureauCode': 'P', 'stationTelecode': 'BJP', 'stationTrainCode': 'Z29', 'dayDifference': 0, 'arriveTime': '2133', 'arriveTimestamp': 1633008780000, 'startTime': '2133', 'startTimestamp': 1633008780000, 'ticketDelay': 0, 'waitingRoom': '-', 'wicket': '-', 'distance': 0, 'timeSpan': 0, 'oneStationCrossDay': False}, {'trainDate': '20211001', 'startDate': '20210120', 'stopDate': '20501231', 'trainNo': '2400000Z290G', 'stationNo': '02', 'stationName': '明光', 'bureauCode': 'H', 'stationTelecode': 'MGH', 'stationTrainCode': 'Z29', 'dayDifference': 1, 'arriveTime': '0622', 'arriveTimestamp': 1633040520000, 'startTime': '0626', 'startTimestamp': 1633040760000, 'ticketDelay': 0, 'waitingRoom': '-', 'wicket': '-', 'distance': 1040, 'timeSpan': 31740000, 'oneStationCrossDay': False}, {'trainDate': '20211001', 'startDate': '20210120', 'stopDate': '20501231', 'trainNo': '2400000Z290G', 'stationNo': '03', 'stationName': '扬州', 'bureauCode': 'H', 'stationTelecode': 'YLH', 'stationTrainCode': 'Z29', 'dayDifference': 1, 'arriveTime': '0800', 'arriveTimestamp': 1633046400000, 'startTime': '0800', 'startTimestamp': 1633046400000, 'ticketDelay': 0, 'waitingRoom': '-', 'wicket': '-', 'distance': 1228, 'timeSpan': 37620000, 'oneStationCrossDay': False}])
    # also note that only yyyymmdd returns correctly; yyyy-mm-dd returns expired data.
    test_module("queryStoptimeByStationCode_old", queryStoptimeByStationCode('XPH', '20210119'), [{'trainNo': '5l000G711070', 'trainCode': 'G7110', 'stationName': '仙林', 'stationCode': 'XPH', 'arriveTime': '1444', 'departTime': '1449'}, {'trainNo': '54000G704571', 'trainCode': 'G7045', 'stationName': '仙林', 'stationCode': 'XPH', 'arriveTime': '0938', 'departTime': '0940'}])
    # only later data have startStation
    test_module("queryStoptimeByStationCode_new", queryStoptimeByStationCode('XPH', '20210120'), [{'trainNo': '5l000G711070', 'trainCode': 'G7110', 'stationName': '仙林', 'stationCode': 'XPH', 'arriveTime': '1444', 'departTime': '1449'}, {'trainNo': '54000G711151', 'trainCode': 'G7111', 'stationName': '仙林', 'stationCode': 'XPH', 'startStationName': '南京', 'startStationCode': 'NJH', 'endStationName': '上海虹桥', 'endStationCode': 'AOH', 'arriveTime': '1039', 'departTime': '1040'}])

    test_module("getRunRuleByTrainNoAndDateRange", getRunRuleByTrainNoAndDateRange('6i0000D9280P',20210919,20210922), {'20210921': '1', '20210920': '0', '20210922': '0', '20210919': '0'})

    test_module("getTrainEquipmentByTrainNo", getTrainEquipmentByTrainNo('800000D9300A'), {})
    # Should be like [{'eId': 156773881, 'bureaName': '京', 'trainsetType': 'CRH2E', 'trainsetName': 'CRH2E-2464', 'deploydepotName': '京动', 'depotName': '北京南所', 'trainsetStatus': '载客运行', 'date': '2021-10-01'}]

    test_module("getTrainCompileListByTrainNo", getTrainCompileListByTrainNo("240000S50108"), [{'startDate': '20210120', 'trainNo': '240000S50108', 'coachNo': '01', 'stopDate': '20501231', 'coachType': 'RZ2   ', 'limit1': 48, 'limit2': 0, 'commentCode': ' ', 'trainGroupNo': 0, 'origin': 'PM', 'runningStyle': 1, 'runningRule': 1, 'seatFeature': '3'}, {'startDate': '20210120', 'trainNo': '240000S50108', 'coachNo': '02', 'stopDate': '20501231', 'coachType': 'RZ2   ', 'limit1': 56, 'limit2': 0, 'commentCode': ' ', 'trainGroupNo': 0, 'origin': 'PM', 'runningStyle': 1, 'runningRule': 1, 'seatFeature': '3'}, {'startDate': '20210120', 'trainNo': '240000S50108', 'coachNo': '03', 'stopDate': '20501231', 'coachType': 'RZ2   ', 'limit1': 56, 'limit2': 0, 'commentCode': ' ', 'trainGroupNo': 0, 'origin': 'PM', 'runningStyle': 1, 'runningRule': 1, 'seatFeature': '3'}, {'startDate': '20210120', 'trainNo': '240000S50108', 'coachNo': '04', 'stopDate': '20501231', 'coachType': 'RZ2   ', 'limit1': 40, 'limit2': 0, 'commentCode': ' ', 'trainGroupNo': 0, 'origin': 'PM', 'runningStyle': 1, 'runningRule': 1, 'seatFeature': '3'}])

    test_module("getTrainsetTypeByTrainCode", getTrainsetTypeByTrainCode("C2201"), {'trainsetTypeName': 'CR400BF', 'trainsetType': '复兴号', 'trainsetTypeImgUrl': 'https://eximages.12306.cn/wificloud/wifiapps/trainbodypic/CR.png', 'trainsetTypeAllImgUrl': 'https://eximages.12306.cn/wificloud/wifiapps/trainbodypic/CR400short-all.png', 'networkType': 'Wi-Fi', 'mealCoach': '05车', 'maxSpeed': '420km/h', 'currentSpeed': '350km/h', 'coachCount': '8', 'capacity': '576人', 'fullLength': '209.06m', 'coachOrganization': '4节动车,4节拖车', 'first': [{'coachNo': '01', 'seatType': '一等/商务座', 'capacity': '33人', 'coachImageUrl': 'https://eximages.12306.cn/wificloud/wifiapps/trainbodypic/CR400short-01(09).png', 'powerType': '拖车(控制车)'}, {'coachNo': '02', 'seatType': '二等座', 'capacity': '90人', 'coachImageUrl': 'https://eximages.12306.cn/wificloud/wifiapps/trainbodypic/CR400short-02-03-06-07(10-11-14-15).png', 'powerType': '动车'}, {'coachNo': '03', 'seatType': '二等座', 'capacity': '90人', 'coachImageUrl': 'https://eximages.12306.cn/wificloud/wifiapps/trainbodypic/CR400short-02-03-06-07(10-11-14-15).png', 'powerType': '拖车(受电弓)'}, {'coachNo': '04', 'seatType': '二等座', 'capacity': '75人', 'coachImageUrl': 'https://eximages.12306.cn/wificloud/wifiapps/trainbodypic/CR400short-04(12).png', 'powerType': '动车'}, {'coachNo': '05', 'seatType': '二等/餐车', 'capacity': '63人', 'coachImageUrl': 'https://eximages.12306.cn/wificloud/wifiapps/trainbodypic/CR400short-05(13).png', 'powerType': '动车'}, {'coachNo': '06', 'seatType': '二等座', 'capacity': '90人', 'coachImageUrl': 'https://eximages.12306.cn/wificloud/wifiapps/trainbodypic/CR400short-02-03-06-07(10-11-14-15).png', 'powerType': '拖车(受电弓)'}, {'coachNo': '07', 'seatType': '二等座', 'capacity': '90人', 'coachImageUrl': 'https://eximages.12306.cn/wificloud/wifiapps/trainbodypic/CR400short-02-03-06-07(10-11-14-15).png', 'powerType': '动车'}, {'coachNo': '08', 'seatType': '二等/商务座', 'capacity': '45人', 'coachImageUrl': 'https://eximages.12306.cn/wificloud/wifiapps/trainbodypic/CR400short-08(16).png', 'powerType': '拖车(控制车)'}], 'manufacturer': '中车唐山机车车辆有限公司,中车长春轨道客车股份有限公司', 'indexKey': 'CR400BF'})

    test_module("queryStoptimeByStationCode", queryStoptimeByStationCode('AFP', '2019-05-05'), [{'trainNo': '24000064380F', 'trainCode': '6438', 'stationName': '云居寺', 'stationCode': 'AFP', 'startStationName': '大涧', 'startStationCode': 'DFP', 'endStationName': '北京西', 'endStationCode': 'BXP', 'arriveTime': '1024', 'departTime': '1026'}, {'trainNo': '24000064370I', 'trainCode': '6437', 'stationName': '云居寺', 'stationCode': 'AFP', 'arriveTime': '1937', 'departTime': '1939'}])

    import datetime

    test_module('queryTrainTicketPriceList', queryTrainTicketPriceList('BJP', 'SEP', datetime.date.today()), '1')

    test_module("getBigScreenByStationCodeAndDate", getBigScreenByStationCodeAndDate('NEH', datetime.datetime.now().strftime('%Y%m%d'), 'A'), '0')

    test_module("queryPreseqTrainsByTrainCode", queryPreseqTrainsByTrainCode('G403', '20210101'), [{'trainDate': '20201231', 'trainCode': 'G406', 'startTime': '10:58', 'endTime': '23:18', 'startStation': '昆明南', 'endStation': '北京西', 'startStationTelecode': 'KOM', 'endStationTelecode': 'BXP', 'distance': '2398', 'trainStatus': '1', 'trainStopTime': '停留8小时42分钟', 'trainDescripe': '已到达北京西'}, {'trainDate': '20210101', 'trainCode': 'G403', 'startTime': '08:00', 'endTime': '18:49', 'startStation': '北京西', 'endStation': '昆明南', 'startStationTelecode': 'BXP', 'endStationTelecode': 'KOM', 'distance': '2398', 'trainStatus': '1', 'trainStopTime': '停留16小时9分钟', 'trainDescripe': '已到达昆明南'}])
