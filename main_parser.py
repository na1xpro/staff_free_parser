from loguru import logger
from proxy_auth import proxies
from cfg_main_constants import headers
from cfg_main_constants import name_file
import requests
import json


def main_proces():
    try:
        for i in range(8, 192, 24):
            url = f"https://api.staff-clothes.com/api/v2/product/discount/by-consumer-category/1207eb2e-b501-4dec-9dcf-e870f06f0ce5?access_token=MDFiNjdiNGFhZjU4ZDU0YzVkMjQ4NDMxYTI5YWM0Y2QzZjQzNjJhYjI4ZjY1ODJlOTZjN2QxMmQxNjM2OTMyNQ&locale=ua&limit=24&offset={i}"
            req = requests.get(url=url, headers=headers, proxies=proxies)
            json_list = json.loads(req.text)
            logger.info(f'JSon  офсет под номером {i} получен ')

    except:
        logger.warning("Парсинг не удался")

    with open(name_file['file2'], 'w+') as save_txt:
        file_read = save_txt.read()
        for lines in json_list:
            save_txt.write(f' Назва товару - {lines["title"]}''\n'
                           f' Артикль товару (з магазину) - {lines["article"]}''\n'
                           f' Розміри  - {lines["sizes"][0]["size"]}''\n'
                           f' Ціна  - {lines["price"]} грн''\n'
                           f' Ціна без знижки - {lines["priceOld"]} грн''\n'
                           f' Ціна Долар ($) - {lines["priceUSD"]} $''\n'
                           f' Фото товару  - {lines["mainImage"]["origin"]}''\n ' + 2 * "_____" '\n')
        logger.info("Данные в  txd записаны")

    with open(name_file['file1'], 'w') as save_js:
        json.dump(json_list, save_js, indent=2)
        logger.info("Данные в  json записаны")


main_proces()
