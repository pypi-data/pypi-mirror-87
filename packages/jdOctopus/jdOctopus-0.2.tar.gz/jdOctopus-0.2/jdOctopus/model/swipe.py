import json
import requests

from octopus_py.index import newOctopus
from octopus_py.tool import interceptor

class swipe:

    @staticmethod
    def swipe(points, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/swipe"
        data = {
            'uuids': uuids,
            'points': points
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)

    @staticmethod
    def smoothSwipe(points, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/smoothSwipe"
        data = {
            'uuids': uuids,
            'points': points
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)

    @staticmethod
    def verticalRoll(extent, uuids=""):
        octopus = newOctopus()
        if uuids == "":
            uuids = octopus.devices
        url = octopus.addr + "/verticalRoll"
        data = {
            'uuids': uuids,
            'extent': extent
        }
        text = json.loads(requests.post(url=url, data=json.dumps(data), headers=octopus.headers).text)
        interceptor(text)