from bs4 import BeautifulSoup
import requests
import json


class TennoDriver:

    def __init__(self):
        return

    def getArbi(self):
        url = 'https://api.warframestat.us/pc/arbitration'
        page = requests.get(url).content

        soup = BeautifulSoup(page, 'html.parser')
        if soup.text == "{}":
            return None
        else:
            try:
                arbiDic = json.loads(soup.text)
                try:
                    temp = arbiDic['enemy']
                    temp = arbiDic['node']
                    temp = arbiDic['type']
                except KeyError:
                    return None
                return json.loads(soup.text)
            except json.decoder.JSONDecodeError:
                return None





