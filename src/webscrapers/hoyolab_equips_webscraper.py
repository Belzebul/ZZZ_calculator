import json
import requests
from pathlib import Path

# precisa dessas infos de auth do hoyolab, user_id e os 2 token de cookies
USER_ID = ''
LTOKEN_V2 = ''
LTUID_V2 = ''

TOKEN = f'ltoken_v2={LTOKEN_V2};ltuid_v2={LTUID_V2};'

HTTP_OK = 200
URL_LIST_BASE = 'https://sg-act-nap-api.hoyolab.com'
URL_LIST_BASE_OPTIONS = '/event/game_record_zzz/api/zzz/avatar/basic?server=prod_gf_us&role_id='
URL_CHAR_DATA = 'https://sg-act-nap-api.hoyolab.com/event/game_record_zzz/api/zzz/avatar/info?id_list[]='
URL_CHAR_OPTIONS = '&need_wiki=true&server=prod_gf_us&role_id='

HEADERS = {
    'Cookie':TOKEN,
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip',
    'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'),
    'Referer': 'https://act.hoyolab.com/',
    'Origin': 'https://act.hoyolab.com'}

class HoyolabCharacterDataScraper:
    def __init__(self):
        resquested_chars_id:dict = self.__request_json(URL_LIST_BASE + URL_LIST_BASE_OPTIONS + USER_ID)
        chars_id:dict = resquested_chars_id['data']['avatar_list']
        self.chars_data:list = self.__request_chars_data(chars_id)

    def __request_json(self, url) -> dict:
        resp = requests.get(url,headers=HEADERS)
        return json.loads(resp.text)

    def __request_chars_data(self,json_char_list):
        char_json_list = []
        for char_name in json_char_list:
            url = URL_CHAR_DATA + str(char_name['id']) + URL_CHAR_OPTIONS + USER_ID
            json_char = self.__request_json(url)
            char_json_list.append(json_char)

        return char_json_list

    def write_files(self, chars_data_list):
        path = Path(__file__).parent.parent.parent.resolve() / 'hoyolab_data'
        Path(path).mkdir(parents=True, exist_ok=True)
        for char_data in chars_data_list:
            self.__write_json_to_file(path, char_data)

    def __write_json_to_file(self, directory, char_data_json):
        file_name = char_data_json['data']['avatar_list'][0]['name_mi18n'] + '_data.json'
        file_path = Path (directory / file_name)
        with open(file_path, 'w') as file:
            file.write(json.dumps(char_data_json, indent=4))

    
if __name__ == '__main__':
    webscraper = HoyolabCharacterDataScraper()
    # webscraper.write_files(webscraper.chars_data)
    pass
