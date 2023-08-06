import json
import requests

from octopus_py.index import newOctopus
from octopus_py.tool import interceptor, exist

class text:

    def __init__(self, text):
        octopus = newOctopus()
        self.addr = octopus.addr
        self.devices = octopus.devices
        self.headers = octopus.headers
        self.text = text

    def clickByOCR(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/clickByOCR"
        data = {
            'uuids': uuids,
            'text': self.text
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=self.headers).text)
        interceptor(text)

    def clickByXml(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/clickByXml"
        data = {
            'uuids': uuids,
            'text': self.text
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=self.headers).text)
        interceptor(text)

    def existByOCR(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/existTextByOCR"
        data = {
            'uuids': uuids,
            'text': self.text
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=self.headers).text)
        return exist(text)

    def existByXML(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/existTextByXML"
        data = {
            'uuids': uuids,
            'text': self.text
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=self.headers).text)
        return exist(text)

    def input(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/inputText"
        data = {
            'uuids': uuids,
            'text': self.text
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=self.headers).text)
        interceptor(text)

    def getPointsByXML(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/getPointsByXML"
        data = {
            'uuids': uuids,
            'text': self.text
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=self.headers).text)
        interceptor(text)
        return text["data"]

    def getPointsByOCR(self, uuids=""):
        if uuids == "":
            uuids = self.devices
        url = self.addr + "/getPointsByOCR"
        data = {
            'uuids': uuids,
            'text': self.text
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=self.headers).text)
        interceptor(text)
        return text["data"]