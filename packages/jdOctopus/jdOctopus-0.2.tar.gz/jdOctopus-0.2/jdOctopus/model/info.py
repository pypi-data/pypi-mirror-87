import json
import requests

from octopus_py.index import newOctopus
from octopus_py.tool import interceptor

class info:

    @staticmethod
    def getOCR(uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/getOCRInfo"
        data = {
            'uuids': uuids
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)
        return text["data"]

    @staticmethod
    def getXML(uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/getHierarchy"
        data = {
            'uuids': uuids
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)
        return text["data"]