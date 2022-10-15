from loguru import logger
from proxy_auth import proxies
from cfg_main_constants import headers
import requests
import lxml

import json
import sqlite3

try:
    for i in range(8, 192, 24):
        url = f"https://api.staff-clothes.com/api/v2/product/discount/by-consumer-category/1207eb2e-b501-4dec-9dcf-e870f06f0ce5?access_token=MDFiNjdiNGFhZjU4ZDU0YzVkMjQ4NDMxYTI5YWM0Y2QzZjQzNjJhYjI4ZjY1ODJlOTZjN2QxMmQxNjM2OTMyNQ&locale=ua&limit=24&offset={i}"
        req = requests.get(url=url, headers=headers, proxies=proxies)
        json_list = json.loads(req.text)
        logger.info(f'JSon  офсет под номером {i} получен ')
except:
     logger.warning("Парсинг не удался")
