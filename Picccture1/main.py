import requests
from bs4 import BeautifulSoup
import re
import threading
href=re.compile(r'.*="(.*)" .*')
href1=re.compile(r'.*="(.*)" tar.*')
requests.packages.urllib3.disable_warnings()
def get_url(url):
    headers = {
        'User - Agent': 'Mozilla / 5.0(X11;Linux x86_64;rv: 84.0) Gecko / 20100101Firefox / 84.0'
    }
    respond = requests.get(url, headers=headers, verify=False)
    return respond.content.decode("utf-8")
def get_info(info):
    sour = BeautifulSoup(info,"html.parser")
    sour_plus = sour.find_all('h2')
    return sour_plus
def get_link(sour):
    list = []
    for i in sour:
        i = str(i);
        middle = re.findall(href, i)
        link = "https://www.meijiao.vip" + middle[0]
        list.append(link)
    return list
def get_info2(url):
    info = get_url(url)
    sour = BeautifulSoup(info,'html.parser')
    sour1 = sour.find_all('div',id='bigpic')
    return sour1
def get_link2(sour1):
    global num
    num = 0
    headers = {
        'User - Agent': 'Mozilla / 5.0(X11;Linux x86_64;rv: 84.0) Gecko / 20100101Firefox / 84.0'
    }
    for o in sour1:
        o = str(o)
        link = re.findall(href1, o)
        respon = requests.get(link[0],headers=headers)
        filename = link[0].split('/')[-1]
        filename = "/home/heaven/Picture/"+filename
        with open (filename,'wb') as f:
            num += 1
            print("第"+str(num)+"张图片下载完成")
            f.write(respon.content)

def Start(i):
    sour1 = get_info2(i)
    get_link2(sour1)
if __name__ == '__main__':
    url = 'https://www.meijiao.vip/tupian/siwa/aiss/list_20_2.html'
    info = get_url(url)
    sour = get_info(info)
    list = get_link(sour)
    for i in list:
        threading.Thread(target=Start,args=(i,)).start()





