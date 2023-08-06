import datetime
import random
import re


# 随机返回请求头
def getHeaders():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
    ]

    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    return headers


# 解析2天前、2分钟等这种日期格式
def format_datetime(dt):
    try:
        ret = ''
        pattern = re.compile('\\d+[-年/]+\\d+[-月/]+\\d+[日]?\s?\\d*[:]?\\d*[:]?\\d{1,2}')
        pattern1 = re.compile('\\d{1,2}[-月]+\\d{1,2}[日]?')
        pattern2 = re.compile('\\d{1,2}:\\d{1,2}')
        pattern3 = re.compile('\\d{1,2}[-月/]+\\d{1,2}[日]?[\\s]*\\d{1,2}:\\d{1,2}')
        if '+0800' in dt:
            if len(dt) > 25:
                dtformat = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0800 %Y')
            else:
                dtformat = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0800')
                year = datetime.datetime.now().year
                dtformat = dtformat.replace(year)
            ret = datetime.datetime.strftime(dtformat, '%Y-%m-%d %H:%M:%S')
        elif '分钟前' in dt:
            # m = int(dt.split('分钟')[0].strip())
            mpattern = re.compile('(\\d+)分钟前')
            m = int(re.findall(mpattern, dt)[0])
            ret = (datetime.datetime.now() - datetime.timedelta(minutes=m)).strftime("%Y-%m-%d %H:%M:%S")
        elif '小时前' in dt:
            # ms = int(dt.split('小时')[0].strip()) * 60
            hpattern = re.compile('(\\d+)小时前')
            ms = int(re.findall(hpattern, dt)[0]) * 60
            ret = (datetime.datetime.now() - datetime.timedelta(minutes=ms)).strftime("%Y-%m-%d %H:%M:%S")
        elif '秒前' in dt:
            # secs = int(dt.split('秒')[0].strip())
            secspattern = re.compile('(\\d+)秒前')
            secs = int(re.findall(secspattern, dt)[0])
            ret = (datetime.datetime.now() - datetime.timedelta(seconds=secs)).strftime("%Y-%m-%d %H:%M:%S")
        elif '天前' in dt:
            d = int(dt.split('天')[0].strip())
            ret = (datetime.datetime.now() - datetime.timedelta(days=d)).strftime("%Y-%m-%d %H:%M:%S")
        elif '昨天' in dt:
            tt = dt.split('昨天')[-1].strip()
            strdate = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d ") + tt
            df = datetime.datetime.strptime(strdate, '%Y-%m-%d %H:%M')
            ret = datetime.datetime.strftime(df, '%Y-%m-%d %H:%M:%S')
        elif '前天' in dt:
            ret = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
        elif re.search(pattern, dt):
            result = re.search(pattern, dt)
            r = result.group(0)
            r = re.sub('[-年月/]', '-', r)
            r = re.sub('日', '', r).strip()
            if len(r) <= 10:
                try:
                    dtformat = datetime.datetime.strptime(r, '%Y-%m-%d')
                except:
                    dtformat = datetime.datetime.strptime(r, '%y-%m-%d')
            elif len(r) <= 16:
                dtformat = datetime.datetime.strptime(r, '%Y-%m-%d %H:%M')
            elif len(r) <= 19:
                dtformat = datetime.datetime.strptime(r, '%Y-%m-%d %H:%M:%S')
            ret = datetime.datetime.strftime(dtformat, '%Y-%m-%d %H:%M:%S')
        elif re.search(pattern3, dt):
            dt = re.search(pattern3, dt).group(0)
            strdate = str(datetime.datetime.now().year) + '-' + dt
            dtformat = re.sub('[月/]', '-', strdate)
            dtformat = re.sub('日', '', dtformat).strip()
            dtformat = datetime.datetime.strptime(dtformat, '%Y-%m-%d %H:%M')
            ret = datetime.datetime.strftime(dtformat, '%Y-%m-%d %H:%M:%S')
        elif re.search(pattern1, dt):
            dt = re.search(pattern1, dt).group(0)
            strdate = str(datetime.datetime.now().year) + '-' + dt
            dtformat = re.sub('[月/]', '-', strdate)
            dtformat = re.sub('日', '', dtformat).strip()
            dtformat = datetime.datetime.strptime(strdate, '%Y-%m-%d')
            ret = datetime.datetime.strftime(dtformat, '%Y-%m-%d %H:%M:%S')
        elif re.search(pattern2, dt):
            dt = re.search(pattern2, dt).group(0)
            dtformat = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d') + ' ' + dt
            dtformat = datetime.datetime.strptime(dtformat, '%Y-%m-%d %H:%M')
            ret = datetime.datetime.strftime(dtformat, '%Y-%m-%d %H:%M:%S')
        else:
            ret = dt
    except Exception as e:
        print(e.args)
    finally:
        return ret


def format_source(source):
    if '来源：' in source:
        source = re.sub('.*?来源：', '', source).strip()
        source = re.sub('[\s\W].*', '', source)
    elif '出处：' in source:
        source = re.sub('.*?出处：', '', source).strip()
        source = re.sub('[\s\W].*', '', source)
    return source


def format_string(text):
    pattern = re.compile('<[A-Za-z\\/].*?>')
    text = re.sub(pattern, '', text)
    return text


def format_phone(phone):
    phone = re.sub(u"([^0-9+])", "", phone)
    return phone
