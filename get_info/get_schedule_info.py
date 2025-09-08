import json
import os.path
import datetime


# 思源数据路径
root_path = r"X:\docker\siyuan\data"
# 日程路径
schedule_path = r"\20230214175805-k88kujg"


def get_schedule_list():
    """
    获取思源笔记中的日程
    """
    schedule_info_list = []
    try:
        # 打开思源笔记日程文件路径
        root_dir = os.path.abspath(root_path + schedule_path)
        for parent, dir_names, filenames in os.walk(root_dir):
            for filename in filenames:
                # 构建每个文件的绝对路径
                schedule_file_path = os.path.join(parent, filename)
                if not schedule_file_path.endswith(".sy"):
                    continue
                with open(schedule_file_path, 'r', encoding='utf-8') as f:
                    # 读取json格式的文件
                    schedule_file_data = json.load(f)
                    f.close()
                    # 提取标题
                    title = schedule_file_data['Properties']['title']
                    if "模板" in title or "月份" in title:
                        continue
                    one_day_list = []
                    task_list = schedule_file_data['Children'][0]['Children']
                    for task in task_list:
                        if task['Children'][0]['Type'] == "NodeTaskListItemMarker" \
                                and task['Children'][1]['Type'] == "NodeParagraph"\
                                and len(task['Children'][1]['Children']) == 1:

                            one_day_list.append({
                                "type": "daily",
                                "task": str(task['Children'][1]['Children'][0]['Data']),
                                "state": True if "TaskListItemChecked" in task['Children'][0] else False
                            })
                        elif task['Children'][0]['Type'] == "NodeTaskListItemMarker" \
                                and task['Children'][1]['Type'] == "NodeParagraph"\
                                and len(task['Children'][1]['Children']) == 2:
                            # print(task['Children'][1]['Children'][0]['TextMarkTextContent'])
                            one_day_list.append({
                                "type": "important",
                                "task": str(task['Children'][1]['Children'][1]['Data']).replace("​", ""),
                                "state": True if "TaskListItemChecked" in task['Children'][0] else False
                            })
                    if len(one_day_list) == 0:
                        continue
                    schedule_info = {
                        "date": title,
                        "list": one_day_list
                    }
                    schedule_info_list.append(schedule_info)
    except Exception as e:
        print("获取思源笔记中的日程失败：")
        print(e)
    return schedule_info_list


def get_important_schedule_list():
    """
    获取思源笔记中的重要日程列表
    """
    # 当天时间
    today_str = str(datetime.datetime.today().strftime("%Y-%m-%d"))
    today = datetime.datetime.strptime(today_str, '%Y-%m-%d')
    # 获取思源笔记日程列表
    schedule_list = get_schedule_list()
    important_schedule_list = []
    for schedule_info in schedule_list:
        for schedule_info_item in schedule_info['list']:
            # 筛序重要的日程
            if schedule_info_item['type'] != "important":
                continue
            schedule_info_item['date'] = schedule_info['date']
            it_day = datetime.datetime.strptime(schedule_info_item['date'], '%Y-%m-%d')
            gap_day = (it_day - today).days
            # 筛序以后的数据
            if gap_day <= 0:
                continue
            schedule_info_item['gap_day'] = str(gap_day)
            important_schedule_list.append(schedule_info_item)
    important_schedule_list = sorted(important_schedule_list, key=lambda x: x['date'])
    return important_schedule_list


def get_daily_schedule_list():
    """
    获取思源笔记中的当天日程列表
    """
    # 当天时间
    today_str = str(datetime.datetime.today().strftime("%Y-%m-%d"))
    # 获取思源笔记日程列表
    schedule_list = get_schedule_list()
    important_schedule_list = []
    for schedule_info in schedule_list:
        for schedule_info_item in schedule_info['list']:
            schedule_info_item['date'] = schedule_info['date']
            if schedule_info_item['date'] != today_str:
                continue
            important_schedule_list.append(schedule_info_item)
    important_schedule_list = sorted(important_schedule_list, key=lambda x: x['date'])
    delete_item_count = 0
    delete_item_list = []
    if len(important_schedule_list) >= 7:
        for i in range(len(important_schedule_list)):
            if important_schedule_list[i]['state']:
                delete_item_count += 1
                delete_item_list.append(important_schedule_list[i])
                if delete_item_count >= (len(important_schedule_list) - 7):
                    break
    for delete_item in delete_item_list:
        important_schedule_list.remove(delete_item)
    return important_schedule_list
