import json
from pathlib import Path
import requests

URL_CHARS_LIST = 'https://api.hakush.in/zzz/data/character.json'
URL_CHARS_DATA = 'https://api.hakush.in/zzz/data/en/character/'
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'),
    'Referer': 'https://zzz.hakush.in/'}

class CharacterBaseScraper:
    def __init__(self) -> None:
       self.chars_data:list = []
       self.chars_ids:dict = self.__request_json(URL_CHARS_LIST)
       self.__load_chars()

    def __request_json(self, url) -> dict:
        resp = requests.get(url, headers=HEADERS)
        return json.loads(resp.text)

    def __load_chars(self):
         for char_id in self.chars_ids.keys():
            url = f'{URL_CHARS_DATA}{char_id}.json'
            self.chars_data.append(self.__request_json(url))

    def write_chars(self):
        directory = Path(__file__).parent.parent.parent.resolve() / 'character_database'
        Path(directory).mkdir(parents=True, exist_ok=True)

        for char_data in self.chars_data:
            url = f'{URL_CHARS_DATA}{char_data['Name']}.json'
            self.__write_char_file(directory, char_data)

    def __write_char_file(self, directory, char_dict):
        file_name = f'{char_dict['Name']}.json'
        file_path = Path (directory / file_name)
        with open(file_path, 'w') as file:
            file.write(json.dumps(char_dict, indent=4))

if __name__ == '__main__':
    webscraper = CharacterBaseScraper()
    # webscraper.write_chars()
    webscraper.chars_data
    webscraper.chars_ids
    pass


