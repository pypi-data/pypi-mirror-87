import uuid
import json
import requests
from jdOctopus.tool import interceptor

octopus = None

class Octopus:
    def __init__(self, add="localhost:8080"):
        self.addr = 'http://' + add + '/api'
        self.uuid = uuid.uuid1()
        self.headers = {
            'Uuid': str(self.uuid),
            'Content-Type': 'application/json',
        }
        self.devices = []

    def ping(self):
        url = self.addr + "/ping"
        text = json.loads(requests.get(url=url, headers=self.headers).text)
        interceptor(text)

def newOctopus(add="localhost:8080"):
    global octopus
    if octopus is None:
        octopus = Octopus(add)
    return octopus