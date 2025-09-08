from datetime import timedelta, date
import requests
import datetime


def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if (n < 0):
        n = abs(n)
        return str(date.today() - timedelta(days=n))
    else:
        return str(date.today() + timedelta(days=n))


def holiday_data_list():
    date_list_str = (get_day_of_day(0)
                     + "," + get_day_of_day(1)
                     + "," + get_day_of_day(2)
                     + "," + get_day_of_day(3)
                     + "," + get_day_of_day(4)
                     + "," + get_day_of_day(5))
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
    }
    holiday_data_result = requests.get(
        'https://api.qqsuu.cn/api/dm-jiejiari?date=' + date_list_str, headers=header).json()
    holiday_data_list = holiday_data_result['data']['list']
    holiday_list = []
    today = True
    for holiday_data in holiday_data_list:
        if today:
            holiday_list.append('今天:   ' + holiday_data['date'] + '   ' + holiday_data['info'])
            today = False
        else:
            holiday_list.append(holiday_data['cnweekday'].replace("星期", "周") + ':   '
                                + holiday_data['date']
                                + '   ' + holiday_data['info'].replace("调休日", "调休(补班)"))
    return holiday_list


def holiday_data_list_timo():
    date_list_str = (get_day_of_day(0)
                     + "," + get_day_of_day(1)
                     + "," + get_day_of_day(2)
                     + "," + get_day_of_day(3)
                     + "," + get_day_of_day(4)
                     + "," + get_day_of_day(5))
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
    }
    holiday_data_result = requests.get(
        'https://timor.tech/api/holiday/batch?d=' + date_list_str + '&type=Y', headers=header).json()
    holiday_data_map = holiday_data_result['type']
    holiday_list = []
    today = True
    for holiday_data_index in range(len(holiday_data_map)):
        date_name = get_day_of_day(holiday_data_index)
        if today:
            if str(holiday_data_map[date_name]['type']) == "0":
                holiday_list.append('今天:   工作日')
            elif str(holiday_data_map[date_name]['type']) == "1":
                holiday_list.append('今天:   周末')
            elif str(holiday_data_map[date_name]['type']) == "2":
                holiday_list.append('今天:   节日')
            else:
                holiday_list.append('今天:   调休(补班)')
            today = False
        else:
            if str(holiday_data_map[date_name]['type']) == "0":
                holiday_list.append(holiday_data_map[date_name]['name'] + ':   工作日')
            elif str(holiday_data_map[date_name]['type']) == "1":
                holiday_list.append(holiday_data_map[date_name]['name'] + ':   周末')
            elif str(holiday_data_map[date_name]['type']) == "2":
                holiday_list.append(holiday_data_map[date_name]['name'] + ':   节日')
            else:
                holiday_list.append(holiday_data_map[date_name]['name'] + ':   调休(补班)')
    return holiday_list


def special_data_list(special_list_config):
    # 当天时间
    today_str = str(datetime.datetime.today().strftime("%Y-%m-%d"))
    today = datetime.datetime.strptime(today_str, '%Y-%m-%d')
    # 获取思源笔记日程列表
    schedule_list = special_list_config
    important_schedule_list = []
    for schedule_info in schedule_list:
        it_day = datetime.datetime.strptime(schedule_info['date'], '%Y-%m-%d')
        gap_day = (it_day - today).days
        # 筛序以后的数据
        if gap_day <= 0:
            continue
        schedule_info['gap_day'] = str(gap_day)
        important_schedule_list.append(schedule_info)
    important_schedule_list = sorted(important_schedule_list, key=lambda x: x['date'])
    return important_schedule_list
