import requests
from bs4 import BeautifulSoup
import pymysql
def get_info(url):
    header = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 85.0.4183.121Safari / 537.36Edg / 85.0.564.67",
        "Cookie": "__mta = 48632217.1613905864029.1613905864029.1613905864029.1;uuid_n_v = v1;uuid = 7C7D0970743511EBB1708BFF4D9991F9FFC96DCA649241B0ACB6A15782A59C3A;_csrf = 530c1066c502b116dcb93e44b9f38445bb29cf3f3a4c42ccd79939a25d8fabed;Hm_lvt_703e94591e87be68cc8da0da7cbd0be2 = 1613905864;Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2 = 1613905864;_lx_utm = utm_source % 3DBaidu % 26utm_medium % 3Dorganic;_lxsdk_cuid = 177c44924d0c8 - 03ea48971ac99c - 7e647b61 - e1000 - 177c44924d1c8;_lxsdk = 7C7D0970743511EBB1708BFF4D9991F9FFC96DCA649241B0ACB6A15782A59C3A;_lxsdk_s = 177c44924d2 - 5bb - 2c2 - bca % 7C % 7C3"
    }
    info = requests.get(url=url,headers=header)
    return info.content.decode("UTF-8")
def clean_info(info):
    sour = BeautifulSoup(info,"lxml")
    stars = sour.find_all(attrs={"class":"star"})
    names = sour.find_all(attrs={"class":"name"})
    times = sour.find_all(attrs={"class":"releasetime"})
    scores = sour.find_all(attrs={"class":"score"})
    star = [] #演员
    name = [] #名字
    time = [] #时间
    score = [] #评分
    for i in stars:
        i = i.string
        i = str(i)
        star.append(i.strip().split("：")[1])
    for i in names:
        name.append(i.string)
    for i in times:
        i = i.string
        time.append(str(i).split("：")[1])
    for i in scores:
        score_one =  i.find_all(name='i')[0].string+i.find_all(name='i')[1].string
        score_one = float(score_one)
        score.append(score_one)
    return  name,star,time,score
def save_mysql(data):
    connect = pymysql.connect(host="localhost",port=3306,user="root",password="match.123",db="movic")
    cursor =  connect.cursor()
    sql = '''create table if not exists movic100(
        id int not null AUTO_INCREMENT,
        name varchar(30) not NULL,
        star varchar(40) not NULL,
        time varchar(30) not NULL,
        score float not NULL,
        primary key (id)
        )Engine InnoDB
    '''
    cursor.execute(sql)
    sql = '''insert into movic100(name,star,time,score) values(%s,%s,%s,%s)
    '''
    for i,o,p,q in zip(data[0],data[1],data[2],data[3]):
        cursor.execute(sql,[i,o,p,q])
    connect.commit()
    connect.close()
if __name__ == "__main__":
    for i in range(0,100,10):
        url = "https://maoyan.com/board/4?offset="+str(i)
        info = get_info(url)
        data = clean_info(info)
        save_mysql(data)