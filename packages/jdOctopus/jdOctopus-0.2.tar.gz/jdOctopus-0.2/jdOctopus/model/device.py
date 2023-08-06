import json
import requests

from octopus_py.index import newOctopus
from octopus_py.tool import interceptor
from requests_toolbelt import MultipartEncoder

class device:

    @staticmethod
    def getOnline():
        octopus = newOctopus()
        url = octopus.addr + "/getDevices"
        text = json.loads(requests.get(url=url, headers=octopus.headers).text)
        interceptor(text)
        return text["data"]

    @staticmethod
    def getBindInfo():
        octopus = newOctopus()
        url = octopus.addr + "/bindDevicesInfo"
        text = json.loads(requests.get(url=url, headers=octopus.headers).text)
        interceptor(text)
        return text["data"]

    @staticmethod
    def bindDevices(uuids):
        octopus = newOctopus()
        url = octopus.addr + "/bindDevices"
        data = {
            'uuids': uuids
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)
        for each in uuids:
            octopus.devices.append(each)

    @staticmethod
    def unBindDevices(uuids):
        octopus = newOctopus()
        url = octopus.addr + "/unBindDevices"
        data = {
            'uuids': uuids
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)
        for each in uuids:
            octopus.devices.remove(each)

    @staticmethod
    def screenCapture(imgPath="./", zoom=4, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        for each in uuids:
            url = octopus.addr + "/screenCapture"
            data = {
                'uuids': [each],
                'zoom': zoom
            }
            res = requests.post(url=url, data=json.dumps(data), headers=octopus.headers)
            sub_str = imgPath[-4:]
            ip = imgPath
            if sub_str!='.png' and sub_str!='.jpg':
                filename = ''
                indirect = str(res.headers['content-disposition'])[-17:].replace(':','')
                if indirect and len(indirect)>0:
                    filename = indirect + '.png'
                ip += filename

            if res.headers["content-type"] == "application/octet-stream":
                with open(ip, 'wb') as f:
                    f.write(res.content)
                    f.close()
            else:
                text = json.loads(res.text)
                interceptor(text)

    @staticmethod
    def addFile(filePath, savePath, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/addFile"
        data = MultipartEncoder(fields={'uuids': str(uuids).replace("'", '"'),  'savepath': savePath,
                                     'file': ("weixin.png", open(filePath, 'rb'))})
        header = {
            'Content-Type': data.content_type, 'Uuid': octopus.headers["Uuid"]
        }
        text = json.loads(requests.post(url=url, headers=header, data=data).text)
        interceptor(text)

    @staticmethod
    def runKeyCode(code, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/runKeyCode"
        data = {
            'uuids': uuids,
            'text': str(code)
        }
        print(data)
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)

    @staticmethod
    def startApp(packageName, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/startApp"
        data = {
            'uuids': uuids,
            'text': packageName
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)