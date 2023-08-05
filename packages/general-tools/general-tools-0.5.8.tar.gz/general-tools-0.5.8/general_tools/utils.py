import json
import datetime
import time
from dateutil import parser
import re
import shortuuid


def dump_json(data):
    return json.dumps(data, ensure_ascii=False)


def load_json(data):
    try:
        return json.loads(data)
    except:
        return None


def sleep(seconds):
    time.sleep(seconds)


def parse_date(str):
    return parser.parse(str)


def timestamp_to_str(time1, format='%Y-%m-%d'):
    return datetime.datetime.fromtimestamp(time1).strftime(format)


def make_timestamp(time_str=None, format='%Y-%m-%d'):
    if not time_str or time_str == 'NaT':
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        format = '%Y-%m-%d %H:%M:%S'
    d = datetime.datetime.strptime(time_str, format)
    t = d.timetuple()
    _timestamp = int(time.mktime(t))
    return _timestamp


def timstamp_to_str(stamp, format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format, time.localtime(stamp))


def get_current_millisecond():
    return int(round(time.time() * 1000))


def get_current_second():
    return int(round(time.time()))


def now_time(format='%Y-%m-%d %H:%M:%S'):
    # 获取当前时间str
    now = datetime.datetime.now().strftime(format)
    return now


def format_time_cost(val):
    result = ''
    if val >= 3600:
        hour = int(val / 3600)
        result += str(hour) + '小时'
        val -= hour * 3600
    if val >= 60:
        min = int(val / 60)
        result += str(min) + '分'
        val -= min * 60
    result += str(val) + '秒'
    return result


def format_blank(content):
    clear_list = {
        u'\u2002': '', u'\u2003': '', u'\u2009': '', u'\u200c\u200d': '', u'\xa0': '', '&nbsp;': '',
        '&ensp;': '', '&emsp;': '', '&zwj;': '', '&zwnj;': ''
    }
    rep = dict((re.escape(k), v) for k, v in clear_list.items())
    pattern = re.compile('|'.join(rep.keys()))
    content = pattern.sub(lambda x: rep[re.escape(x.group(0))], content)
    return content


def get_url_uuid(url):
    return shortuuid.uuid(name=url)


class TimeCost(object):
    __start = get_current_millisecond()

    @classmethod
    def show_time_diff(cls):
        return format_time_cost((get_current_millisecond() - cls.__start) / 1000)

    @classmethod
    def reset_time(cls):
        cls.__start = get_current_millisecond()

    @classmethod
    def time_diff(cls):
        return get_current_millisecond() - cls.__start


# ['总论', '自然', '自然辩证法', '自然辩证法总论']

def str_list_element_drop_contain(str_list: list, reverse=True):
    remove_elements = set()
    all_elements = set(str_list)

    group_dict = dict()
    for obj in all_elements:
        group_dict[len(obj)] = group_dict.get(len(obj), []) + [obj]

    name_group_list_tuple = sorted(group_dict.items(), key=lambda x: x, reverse=True)

    for i in range(1, len(name_group_list_tuple)):
        layer_elements_list = name_group_list_tuple[i][1]
        for elements_tuple in name_group_list_tuple[:i]:
            current_str = '、'.join(elements_tuple[1])
            for ele in layer_elements_list:
                if ele in current_str:
                    remove_elements.add(ele)

    remain_elements = all_elements - remove_elements
    if reverse:
        remain_elements = sorted(remain_elements, key=lambda x: len(x), reverse=reverse)
    return list(remain_elements)


import smtplib  # 加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr


def send_mail(subject, content, receiver):
    my_sender = 'm13911639030@163.com'
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(["DailyCheck", my_sender])
    msg['To'] = formataddr(["xuwei", receiver])
    msg['Subject'] = subject  # 邮件的主题，也可以说是标题
    server = smtplib.SMTP("smtp.163.com", 25)
    server.login(my_sender, "sdai@2018")
    server.sendmail(my_sender, [receiver], msg.as_string())
    server.quit()


if __name__ == '__main__':
    str_list = ['总论', '自然xw', '自然辩证法', '自然辩证法总论']
    r = str_list_element_drop_contain(str_list)
    print(r)
