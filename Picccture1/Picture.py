import re
import requests
from bs4 import BeautifulSoup
href = re.compile(r'.*="(.*)"><.*')
requests.packages.urllib3.disable_warnings()
def get_info(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'
 }
    respons = requests.get(url,headers=headers,verify=False)
    return respons.content.decode('utf-8',errors='ignore')
def get_link(respond):
    list = []
    sour = BeautifulSoup(respond,"html.parser")
    sour_plus = sour.find_all('div',class_='image-list')
    for i in sour_plus:
        i = str(i)
        # print(i)
        i1 = re.findall(href,i)
        for o in i1:
            list.append(o)
    return list
def get_picture(list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'
    }
    for i in list:
        i = str(i)
        filename = i.split('/')[-1]
        link = "https://wallroom.io"+i+"/download"
        # print(link)
        respond = requests.get(link,headers=headers)
        filename = "/home/heaven/Picture/"+filename+".jpg"
        with open(filename,'wb') as f:
            f.write(respond.content)
if __name__ == "__main__":
    url = "https://wallroom.io/1920x1080"
    respond = get_info(url)
    list = get_link(respond)
    get_picture(list)