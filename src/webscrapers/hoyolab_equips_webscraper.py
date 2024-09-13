import json
import os
import dotenv
import requests
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# precisa dessas infos de auth do hoyolab, user_id e os 2 token de cookies
USER_ID = os.getenv('USER_ID')
LTOKEN_V2 = os.getenv('LTOKEN_V2')
LTUID_V2 = os.getenv('LTUID_V2')

TOKEN = f'ltoken_v2={LTOKEN_V2};ltuid_v2={LTUID_V2};'

HTTP_OK = 200
URL_LIST_BASE:str = 'https://sg-act-nap-api.hoyolab.com'
URL_LIST_BASE_OPTIONS:str = '/event/game_record_zzz/api/zzz/avatar/basic?server=prod_gf_us&role_id='
URL_CHAR_DATA:str = 'https://sg-act-nap-api.hoyolab.com/event/game_record_zzz/api/zzz/avatar/info?id_list[]='
URL_CHAR_OPTIONS:str = '&need_wiki=true&server=prod_gf_us&role_id='

HEADERS = {
    'Cookie':TOKEN,
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip',
    'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'),
    'Referer': 'https://act.hoyolab.com/',
    'Origin': 'https://act.hoyolab.com'}


def load_chars_data() -> list:
    resquested_chars_id:dict = _request_json(f'{URL_LIST_BASE}{URL_LIST_BASE_OPTIONS}{USER_ID}')
    chars_id:dict = resquested_chars_id['data']['avatar_list']
    chars_data:list = _request_chars_data(chars_id)
    return chars_data


def _request_json(url:str) -> dict:
    resp = requests.get(url, headers=HEADERS)
    return json.loads(resp.text)


def _request_chars_data(json_char:dict) -> list:
    char_json_list = []
    for char_name in json_char:
        url = f'{URL_CHAR_DATA}{str(char_name['id'])}{URL_CHAR_OPTIONS}{USER_ID}'
        json_char = _request_json(url)
        char_json_list.append(json_char)

    return char_json_list


def write_files(chars_data:list) -> None:
        path = Path(__file__).parent.parent.parent.resolve() / 'hoyolab_data'
        Path(path).mkdir(parents=True, exist_ok=True)
        for char_data in chars_data:
            _write_json_to_file(path, char_data)


def _write_json_to_file(directory:Path, char_data_json:dict) -> None:
        file_name = char_data_json['data']['avatar_list'][0]['name_mi18n'] + '_data.json'
        file_path = Path (directory / file_name)
        with open(file_path, 'w') as file:
            file.write(json.dumps(char_data_json, indent=4))


if __name__ == '__main__':
    chars_data = load_chars_data()
    write_files(chars_data)
    pass
