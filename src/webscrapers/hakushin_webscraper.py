import json
from pathlib import Path

import requests

URL_CHARS_LIST = "https://api.hakush.in/zzz/data/character.json"
URL_CHARS_DATA = "https://api.hakush.in/zzz/data/en/character/"
HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    ),
    "Referer": "https://zzz.hakush.in/",
}


def load_character_base_data():
    chars_ids: dict = _request_json(URL_CHARS_LIST)
    return _load_chars(chars_ids)


def _request_json(url: str) -> dict:
    resp = requests.get(url, headers=HEADERS, timeout=5)
    return json.loads(resp.text)


def _load_chars(chars_ids: dict) -> dict:
    chars_data: dict = {}
    for char_id in chars_ids.keys():
        url = f"{URL_CHARS_DATA}{char_id}.json"
        chars_data[char_id] = _request_json(url)

    return chars_data


def write_chars(chars_data: dict) -> None:
    directory = Path(__file__).parent.parent.parent.resolve() / "character_database"
    Path(directory).mkdir(parents=True, exist_ok=True)
    file_name = "characters_base.json"
    file_path = Path(directory / file_name)
    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(json.dumps(chars_data, indent=4))


"""
def write_chars(chars_data:list):
    directory = Path(__file__).parent.parent.parent.resolve() / 'character_database'
    Path(directory).mkdir(parents=True, exist_ok=True)

    for char_data in chars_data:
        _write_char_file(directory, char_data)


def _write_char_file(directory, char_dict):
    file_name = f'{char_dict['Name']}.json'
    file_path = Path (directory / file_name)
    with open(file_path, 'w') as file:
        file.write(json.dumps(char_dict, indent=4))
"""

if __name__ == "__main__":
    chars_data = load_character_base_data()
    write_chars(chars_data)
