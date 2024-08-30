import json
from urllib3 import PoolManager
import urllib3
from urllib3.util import create_urllib3_context

HTTP_OK = 200
URL_CHARS_LIST = 'https://api.hakush.in/zzz/data/character.json'
URL_CHARS_DATA = 'https://api.hakush.in/zzz/data/en/character/'
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'),
    'Referer': 'https://zzz.hakush.in/'}

class CharacterBaseDataHTTPCollector:
    def __init__(self) -> None:
        char_list = self.load_data_json(URL_CHARS_LIST)

        for char_id in char_list.keys():
            url = f'{URL_CHARS_DATA}{char_id}.json'
            char_dict = self.load_data_json(url)
            self.write_dict_to_file(char_dict)

    def write_dict_to_file(self, char_dict):
        file_name = f'character_database/{char_dict['Name']}.json'
        with open(file_name, 'w') as file:
            file.write(json.dumps(char_dict, indent=4))

    def load_data_json(self, url) -> dict:
        http = urllib3.PoolManager()
        resp = http.request('GET', url, HEADERS)
        data_raw = resp.data.decode('utf-8')
        return json.loads(data_raw)

        return char_list


    def load_data(self):
        pass

class RequestException(Exception):
    '''invalid url'''

    def __init__(self, url, message = 'invalid url: '):
        super().__init__(message + url)

if __name__ == '__main__':
    test_collector = CharacterBaseDataHTTPCollector()