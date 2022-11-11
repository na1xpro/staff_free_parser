import lxml.html
from loguru import logger
from proxy_auth import proxies
from cfg_main_constants import headers
from cfg_main_constants import name_file_json,name_file_txt
from cfg_main_constants import name_category_link
from lxml import html
import requests
import json



def parse_diskounts():
    try:
        for i in range(8, 192, 24):
            url = f"https://api.staff-clothes.com/api/v2/product/discount/by-consumer-category/1207eb2e-b501-4dec-9dcf-e870f06f0ce5?access_token=MDFiNjdiNGFhZjU4ZDU0YzVkMjQ4NDMxYTI5YWM0Y2QzZjQzNjJhYjI4ZjY1ODJlOTZjN2QxMmQxNjM2OTMyNQ&locale=ua&limit=24&offset={i}"
            req = requests.get(url=url, headers=headers, proxies=proxies)
            json_list = json.loads(req.text)
            logger.info(f'JSon  офсет под номером {i} получен ')

    except:
        logger.warning("Парсинг не удался")

    with open(name_file_txt['free_price_txt'], 'w+') as save_txt:
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

    with open(name_file_json['free_price_js'], 'w') as save_js:
        json.dump(json_list, save_js, indent=2)
        logger.info("Данные в  json записаны")


def parse_tracksuits_man(name_category):
    req = requests.get(name_category_link[name_category], headers=headers, proxies=proxies)
    parsed_body = html.fromstring(req.text)
    name_commodity = parsed_body.xpath("//span[@class = 'product-card__info--title']/text()")
    size_commodity = parsed_body.xpath("//span[@class = 'product-card__info--sizes']/text()")
    link_commodity = parsed_body.xpath("//div[@class = 'catalog__product-catalog']/div/a/@href")
    price_commodity = parsed_body.xpath("//span[@class = 'product-card__info--price']/text()")

    with open(name_file_txt[name_category], 'w+') as save_txt:
        file_read = save_txt.read()
        for name, size, link, price in zip(name_commodity, size_commodity, link_commodity, price_commodity):
            save_txt.write(f' Назва товару - {name}''\n'
                           f' Ціна  - {price}''\n'
                           f' Розміри - {size}''\n'
                           f' Силка на товар - {link}''\n' + 2 * "_____" '\n')

    with open(name_file_json[name_category], 'w') as file:
        for name, size, link, price in zip(name_commodity, size_commodity, link_commodity, price_commodity):
            file.write(json.dumps(['product', {'name':name,
                                           "price":price,
                                           "size": size,
                                           "link":link}],indent=2))

