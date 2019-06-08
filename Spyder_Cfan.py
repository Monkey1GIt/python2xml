import requests
import bs4
import time
import os
import sys
import codecs
# import EmailSSL
import AddXML

# 重新加载sys模块,重新设置字符集
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
root = os.path.dirname(os.path.realpath(__file__))
path_log = root + '/Log.txt'
path_database = root + '/Database.txt'
url_index = 'http://www.cfan.com.cn/technic/'
# url_head = 'http://cxks.xju.edu.cn'


def get_urllist(url):
    urllist = []
    soup = bs4.BeautifulSoup(text_index, 'html.parser')
    for pos in soup.find_all('div'):
        if pos.get('class') == ['left-post']:
            # print(pos.contents[3].get('href'))
            urllist.append(pos.contents[3].get('href'))

    for i in range(len(urllist)):
        print('\n%d of ' % i + str(len(urllist)))
        # print('getPageList():' + slst[i])
        record(urllist[i])


def record(slst):
    key = slst
    #print('record(): ' + slst + ' ' + key)
    flag = 1
    # 打开工作日志，若Log.txt不存在，新建
    try:
        with open(path_database, 'r', encoding='UTF-8') as f:
            line = f.readlines()
            f.close()
    except FileNotFoundError:
        with open(path_database, 'wb+') as f:
            #old_log = f.read()
            line = ''
            f.close()
    # 过滤掉重复的网址
    for i in range(len(line)):
        if key == line[i].strip('\n'):
            print('Repeated! ' + key + ' ' + str(i))
            flag = 0
    # flag为写入数据标志，1默认为写入
    if flag == 1:
        com_html(key)
        url_log.append(key)  # 抓取网址记录在url_log中
        with open(path_database, 'a') as f:
            f.write(key + '\n')
            f.close


def get_text(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('获取文本失败')


def com_html(url):
    # print(url_body) #输出测试
    html_text = get_text(url)
    soup = bs4.BeautifulSoup(html_text, 'html.parser')
    #
    for link in soup.find_all('h1'):
        title = link.text
        break
    #
    for link in soup.find_all('div'):
        if link.get('class') == ['maincontent']:  # 'maincontent' 加不加 [] 结果不一样
            content = link
            # print(link)
            break
    # print(title)
    # print(content)
    # 以xml形式存储
    AddXML.add_newxml(title, str(content), url)


# 记录工作日志
def log():
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(time1)
    # 读取原来的旧log
    try:
        with open(path_log, 'r', encoding='UTF-8') as f:
            old_log = f.read()
            f.close()
    except FileNotFoundError:
        with open(path_log, 'wb+') as f:
            old_log = ''
            f.close()
    with open(path_log, 'w', encoding='UTF-8') as f:
        f.seek(0, 0)
        f.writelines('----更新时间：%s-----\n' % time1)
        for i in range(len(url_log)):
            f.seek(0, 2)
            f.writelines(url_log[i] + '\n')
        f.seek(0, 2)
        f.writelines('%s 条更新完成。\n\n' % len(url_log))
        f.seek(0, 2)
        f.write(old_log)
        f.close()


if __name__ == '__main__':
   # print(root)
   # print(path_log)
    url_log = []
    text_index = get_text(url_index)
    urllist = get_urllist(text_index)
    log()
