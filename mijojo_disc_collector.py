#from typing import List
#from bs4 import BeautifulSoup
#from bs4.element import Tag
import requests
import json

USER_ID = ''
LTOKEN_V2 = ''
LTUID_V2 = ''
TOKEN = f'ltoken_v2={LTOKEN_V2};ltuid_v2={LTUID_V2};'

HTTP_OK = 200
URL_CHAR_LIST = 'https://sg-act-nap-api.hoyolab.com/event/game_record_zzz/api/zzz/avatar/basic?server=prod_gf_us&role_id='
URL_CHAR_DATA = 'https://sg-act-nap-api.hoyolab.com/event/game_record_zzz/api/zzz/avatar/info?id_list[]='
URL_CHAR_OPTIONS = '&need_wiki=true&server=prod_gf_us&role_id='

HEADERS = {
    'Cookie':TOKEN,
    'Accept': '*/*',
    'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'),
    'Referer': 'https://act.hoyolab.com/',
    'Origin': 'https://act.hoyolab.com'}

class CharacterHTMLCollector:

    def __init__(self):

        json_resquested_chars_name = json.loads(self.http_content(URL_CHAR_LIST + USER_ID))
        json_char_list = json_resquested_chars_name['data']['avatar_list']
        chars_data_list = self.load_chars_data(json_char_list)
        self.write_char_files(chars_data_list)
        print("")

    def write_char_files(self, chars_data_list):
        for char_data in chars_data_list:
            self.write_json_to_file(char_data)

    def write_json_to_file(self, char_data_json):
        file_name = char_data_json['data']['avatar_list'][0]['name_mi18n'] + '_data.json'
        with open(file_name, 'w') as file:
            file.write(json.dumps(char_data_json, indent=4))

    def load_chars_data(self,json_char_list):
        char_json_list = []
        for char_name in json_char_list:
            url = URL_CHAR_DATA + str(char_name['id']) + URL_CHAR_OPTIONS + USER_ID
            json_char = json.loads(self.http_content(url))
            char_json_list.append(json_char)

        return char_json_list

    def http_content(self, url):
        return self.load_data(url).content.decode('utf-8')

    def load_data(self, url):
        http_request = requests.get(url, headers=HEADERS)
        if( http_request.status_code != HTTP_OK):
            raise RequestException(url)

        return http_request


class RequestException(Exception):
    '''invalid url'''

    def __init__(self, url, message = 'invalid url: '):
        super().__init__(message + url)


if __name__ == '__main__':
    test_collector = CharacterHTMLCollector()
