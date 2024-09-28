import json
import os
from pathlib import Path

import requests
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# precisa dessas infos de auth do hoyolab, user_id e os 2 token de cookies
USER_ID = os.getenv("USER_ID")
LTOKEN_V2 = os.getenv("LTOKEN_V2")
LTUID_V2 = os.getenv("LTUID_V2")
TOKEN = f"ltoken_v2={LTOKEN_V2};ltuid_v2={LTUID_V2};"

URL_LIST_BASE: str = "https://sg-act-nap-api.hoyolab.com"
URL_LIST_BASE_PARAMS: str = (
    "/event/game_record_zzz/api/zzz/avatar/basic?server=prod_gf_us&role_id="
)
URL_CHAR_DATA: str = (
    "https://sg-act-nap-api.hoyolab.com/event/"
    "game_record_zzz/api/zzz/avatar/info?id_list[]="
)
URL_CHAR_PARAM: str = "&need_wiki=true&server=prod_gf_us&role_id="

HEADERS = {
    "Cookie": TOKEN,
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    ),
    "Referer": "https://act.hoyolab.com/",
    "Origin": "https://act.hoyolab.com",
}


def load_chars_data() -> dict:
    resquested_chars_id: dict = _request_json(
        f"{URL_LIST_BASE}{URL_LIST_BASE_PARAMS}{USER_ID}"
    )
    chars_id: dict = resquested_chars_id["data"]["avatar_list"]
    chars_data: dict[int, dict] = _request_chars_data(chars_id)
    return chars_data


def _request_json(url: str) -> dict:
    resp = requests.get(url, headers=HEADERS, timeout=5)
    return json.loads(resp.text)


def _request_chars_data(json_char: dict) -> dict:
    char_json_list = []
    char_json: dict[int, dict] = {}
    for char_name in json_char:
        url = f'{URL_CHAR_DATA}{str(char_name['id'])}{URL_CHAR_PARAM}{USER_ID}'
        json_char = _request_json(url)
        char_json[char_name["id"]] = json_char["data"]["avatar_list"]
        char_json_list.append(json_char)

    return char_json


def write_files(chars_data: dict) -> None:
    path = Path(__file__).parent.parent.parent.resolve() / "hoyolab_data"
    Path(path).mkdir(parents=True, exist_ok=True)
    file_name = "hoyolab_character.json"
    file_path = Path(path / file_name)
    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(json.dumps(chars_data, indent=4))


if __name__ == "__main__":
    hoyolab_chars: dict[int, dict] = load_chars_data()
    write_files(hoyolab_chars)
    pass
