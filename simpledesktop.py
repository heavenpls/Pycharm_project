import requests
from bs4 import BeautifulSoup
import re
import lxml
image = re.compile(r'(.*?).\d+x\d+.*')
def get_info(url):
    headers = {
        'User-Agent': 'Mozilla / 5.0(X11;Linuxx86_64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36'
    }
    info = requests.get(url=url,headers=headers)
    return info.content
def clean_info(info):
    sour = BeautifulSoup(info,"lxml")
    print(sour.div.attrs)
    list = []
    name = []
    for img in sour.find_all(name='img'):
        img_links = img.attrs['src']
        img_link = re.findall(image,img_links)
        list.append(img_link[0])
        name.append(img.attrs['title'])
    return list,name
def save_info(list,name):
    for i,j in zip(list,name):
        try:
            name = "/home/heaven/Data/images/"+j+".png"
            with open(name,'wb+') as f:
                f.write(get_info(i))
        except:
            continue
if __name__ == "__main__":
    for i in range(6,51):
        url = 'http://simpledesktops.com/browse/'+str(i)
        info = get_info(url)
        info = info.decode("utf-8")
        list = clean_info(info)
        save_info(list[0],list[1])
        print("----------------------------------------------------------"+str(i)+"------------------------------------------------")