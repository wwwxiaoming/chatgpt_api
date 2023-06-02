from datetime import datetime
import utils.ComKey as ComKey
import pytz
from dateutil import tz
def getNowText():
    current_time = datetime.now()
    formatted_time = current_time.strftime(ComKey.TIME_STRING)
    return formatted_time;

def getNowTime():
    current_time = datetime.now()

    # 获取本地时区
    local_timezone = tz.gettz()

    # 定义目标时区
    target_timezone = tz.gettz('Asia/Shanghai')

    # 将时间转换为目标时区
    converted_time = current_time.replace(tzinfo=local_timezone).astimezone(target_timezone)
    return converted_time;

def getTimeByStr(time):
    date_time_obj = datetime.strptime(time, ComKey.TIME_STRING)
    return date_time_obj;

