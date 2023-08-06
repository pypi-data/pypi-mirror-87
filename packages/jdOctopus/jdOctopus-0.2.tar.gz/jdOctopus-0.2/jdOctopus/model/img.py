import json
import requests
from octopus_py.index import newOctopus
from octopus_py.tool import interceptor, exist
from requests_toolbelt import MultipartEncoder

class img:

    def __init__(self, imgPath):
        octopus = newOctopus()
        self.addr = octopus.addr
        self.devices = octopus.devices
        self.headers = octopus.headers
        self.imgPath = imgPath

    def click(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/clickByImage"
        data = MultipartEncoder(fields={'uuids': str(uuids).replace("'", '"'), 'imgPath': self.imgPath,
                                     'img': ("weixin.png", open(self.imgPath, 'rb'))})
        header = {
            'Content-Type': data.content_type, 'Uuid': self.headers["Uuid"]
        }
        text = json.loads(requests.post(url=url, headers=header, data=data, timeout=5).text)
        interceptor(text)

    def exists(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/existImage"
        data = MultipartEncoder(fields={'uuids': str(uuids).replace("'", '"'), 'imgPath': self.imgPath,
                                     'img': ("weixin.png", open(self.imgPath, 'rb'))})
        header = {
            'Content-Type': data.content_type, 'Uuid': self.headers["Uuid"]
        }
        text = json.loads(requests.post(url=url, headers=header, data=data).text)
        return exist(text)

    def save(self, savePath, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/addImg"
        data = MultipartEncoder(fields={'uuids': str(uuids).replace("'", '"'), 'imgPath': self.imgPath, 'savepath': savePath,
                                     'img': ("weixin.png", open(self.imgPath, 'rb'))})
        header = {
            'Content-Type': data.content_type, 'Uuid': self.headers["Uuid"]
        }
        text = json.loads(requests.post(url=url, headers=header, data=data).text)
        interceptor(text)

    def getPointsByImage(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/getPointsByImage"
        data = MultipartEncoder(fields={'uuids': str(uuids).replace("'", '"'), 'imgPath': self.imgPath,
                                     'img': ("weixin.png", open(self.imgPath, 'rb'))})
        header = {
            'Content-Type': data.content_type, 'Uuid': self.headers["Uuid"]
        }
        text = json.loads(requests.post(url=url, headers=header, data=data).text)
        interceptor(text)
        return text["data"]