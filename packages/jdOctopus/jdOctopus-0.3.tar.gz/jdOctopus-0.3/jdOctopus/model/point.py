import json
import requests

from jdOctopus.index import newOctopus
from jdOctopus.tool import interceptor

class point:

    @staticmethod
    def clickLong(x, y, time, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/clickLong"
        data = {
            'uuids': uuids,
            'x': x,
            'y': y,
            'time': time
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)

    @staticmethod
    def clickByPixel(x, y, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/clickByPixel"
        data = {
            'uuids': uuids,
            'x': x,
            'y': y
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)

    @staticmethod
    def clickByPercentage(x, y, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/clickByPercentage"
        data = {
            'uuids': uuids,
            'x': x,
            'y': y
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)