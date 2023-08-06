from time import sleep
from octopus_py.index import newOctopus
from octopus_py.model import *

newOctopus("10.222.50.39:8080")
uuid = ["7e:03:ab:92:73:13"]
device.bindDevices(uuid)

def slideDown(x):
    point.clickByPixel(540,450)
    sleep(2)
    for i in range(x):
        point.clickByPixel(540,1902)
        sleep(1)
    point.clickByPixel(950,1350)
    sleep(3)

def qiehuan(x,y,shangquan,city):
    for j in range(len(shangquan)):
        if j >12 :
            y = 2164
            for i in range(j-12):
                swipe.verticalRoll(0.0625)
                sleep(2)

        point.clickByPixel(x,y)
        sleep(2)
        point.clickByPixel(50,270)
        sleep(2)
        y+=124

img("./img/趣玩街.png").click()
sleep(4)
img("./img/允许.png").click()
sleep(2)
point.clickByPixel(50, 270)
sleep(2)
cityList= ["上海","佛山","北京","厦门","广州","西安","郑州","重庆"]
for i in range(len(cityList)):
    x = 200
    y = 676
    if i == 0 :
        list =["世纪汇广场","世博源广场","百联中环购物广场","静安大悦城","爱琴海微站","世茂广场","爱琴海B1"]
        slideDown(i)
        qiehuan(x,y,list,cityList[i])
    if i == 1 :
        list = ["九珑璧支行", "季华支行", "澜普支行", "世纪康城支行", "盛南新都支行", "影萌路支行", "锦华支行", "绿景三路支行", "大福南支路", "普君新城支路", "广佛路支行",
                "同济支行", "同福路支行", "东方水岸支行", "榴子支行", "莲华支行", "厚辉支行", "江湾支行", "威尔斯广场支行", "佛平路支行"]
        slideDown(i)
        qiehuan(x,y,list,cityList[i])
    if i == 2 :
        list = ["京东6号楼四层C1区09", "京东商超移动点位5区"]
        slideDown(i)
        qiehuan(x,y,list,cityList[i])

    if i == 3 :
        list = ["厦门国际会议展览中心"]
        slideDown(i)
        qiehuan(x,y,list,cityList[i])

    if i == 4 :
        list = ["中国银行广州合景支行"]
        slideDown(i)
        qiehuan(x,y,list,cityList[i])

    if i == 5 :
        list = ["西安曲江大悦城"]
        slideDown(i)
        qiehuan(x,y,list,cityList[i])

    if i == 6 :
        list = ["郑州农商银行老鸦陈支部"]
        slideDown(i)
        qiehuan(x,y,list,cityList[i])

    if i == 7 :
        list = ["京东电器超级体验店"]
        slideDown(i)
        qiehuan(x,y,list,cityList[i])

device.runKeyCode(4)
sleep(2)
device.runKeyCode(3)
sleep(2)
