import requests
import os
from lxml import html
from itertools import zip_longest


class Hata:  # Класс представления данных
    id: str
    address: str
    contract: str
    title: str
    link: str
    price: str
    material: str
    lift: str
    floor: str
    type: str
    year: str
    balcony: str
    square: str
    pics: list[str]
    advert_type: str

    def __init__(self, id, utitle, ulink, contract, address, advert_type):  # Конструктор
        self.id = id
        self.title = utitle
        self.link = ulink
        self.contract = contract
        self.address = address
        self.advert_type = advert_type

        
def find_char(table, char) -> str: # Функция поиска конкретной харакетристики
    cols = table.xpath(".//div")
    for col in cols:
        names = col.xpath(".//ul[@class='list-inline-item w135p']")[0].xpath(".//li")
        values = col.xpath(".//ul[@class='list-inline-item']")[0].xpath(".//li")

        for i, li in enumerate(names):
            if char in li.xpath(".//text()")[0]:
                return values[i].xpath(".//text()")[0]

    return "Не указано"


def get_chars(hatas: list[Hata]): # Функция задания всех характеристик объекту
    for hata in hatas:
        r = requests.get(f"https://proestate.24sn.ru{hata.link[0]}")

        tree = html.fromstring(r.text)

        try:
            price = tree.xpath("/html/body/div[1]/section[1]/div/div[1]/div[2]/div/div[1]/h2/text()")[0]
        except:
            price = 0

        characteristics = tree.xpath("/html/body/div[1]/section[2]/div/div/div[1]/div/div[2]/div/div")[0]

        try:
            pic_cols = tree.xpath("/html/body/div[1]/section[1]/div/div[2]")[0].xpath("./div")

            pics = [f"""https://proestate.24sn.ru{pic_cols[0].xpath(".//a/@href")[0]}"""]

            pic_col2 = pic_cols[1].xpath(".//div[@class='col-6']")

            if len(pic_col2) == 6:
                pic_col2 = pic_col2[:-1]

            for i in range(len(pic_col2)):
                pics.append(f"""https://proestate.24sn.ru{pic_col2[i].xpath(".//a[@class='popup-img']/@href")[0]}""")
        except:
            pics = []
            
        hata.price = price
        hata.pics = pics
        hata.material = find_char(characteristics, "Материал")
        hata.lift = find_char(characteristics, "Лифт")
        hata.floor = find_char(characteristics, "Этаж")
        hata.type = find_char(characteristics, "Тип")
        hata.year = find_char(characteristics, "Год")
        hata.balcony = find_char(characteristics, "Балкон")
        hata.square = find_char(characteristics, "Площадь")


def get_first_n_personal(n: int, source: str, link_site: str) -> list[Hata]: # Получение первых n объектов

    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, source)

    file = open(file_path, "r+")
    objects = file.read().split("\n")

    data = []
    status = False
    i = 1
    count = 0

    while not status:
        url = f"{link_site}&p={i}"
        r = requests.get(url)

        tree = html.fromstring(r.text)
        arr = tree.xpath("//*[@id='catalog-property']/div/div/div[2]/div")[0]
        posts = arr.xpath(".//div[@class='col-lg-12']")

        if len(posts) == 0:
            break

        for post in posts:
            details = post.xpath(".//div[@class='details']")[0]

            id = details.xpath(".//span[@class='float-right']/text()")[0]
            id = id[id.find("№") + 1:]

            title = details.xpath(".//h4/text()")[0]

            contract = details.xpath(".//*[@class='list-inline-item']/text()")[0]

            address = details.xpath(".//*[@class='address']/text()")[0]

            if id not in objects:
                link = details.xpath(".//a[@class='fp_price']/@href")
                advert_type: str = "продажа"
                if source == "source_sale.txt":
                    advert_type = "продажа"
                else:
                    advert_type = "аренда"
                data.append(Hata(id, title, link, contract, address, advert_type))
                file.write(f"{id}\n")

            count += 1

            if count == n:
                status = True
                break

        i += 1

    if len(data) != 0:
        get_chars(data)

    # for hata in data:
    #     print(f"\n\nhata from get_first_n_personal with {source}\t", f"{hata.id} {hata.title} {hata.address} {hata.contract} {hata.price} {hata.pics} {hata.material} {hata.lift} {hata.floor} {hata.type} {hata.year} {hata.balcony} {hata.advert_type}\n\n")

    file.close()
    return data


def get_first_n(n: int) -> list[Hata]:
    sale = get_first_n_personal(n, "source_sale.txt", "https://proestate.24sn.ru/catalog/?address=&contract=sale&category=all&price_min=&price_max=&currency=RUB")
    rent = get_first_n_personal(n, "source_rent.txt", "https://proestate.24sn.ru/catalog/?address=&contract=rent&category=all&mortgage=N&price_min=&price_max=&currency=RUB")
    sale.reverse()
    rent.reverse()
    return [item for pair in zip_longest(sale, rent) for item in pair if item is not None]


def find_new_personal(source: str, link_site: str) -> list[Hata]: # Поиск новых объектов
    
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, source)

    file = open(file_path, "r+")
    objects = file.read().split("\n")

    data = []
    status = False
    i = 1

    while not status:
        url = f"{link_site}&p={i}"
        r = requests.get(url)

        tree = html.fromstring(r.text)
        arr = tree.xpath("//*[@id='catalog-property']/div/div/div[2]/div")[0]
        posts = arr.xpath(".//div[@class='col-lg-12']")

        if len(posts) == 0:
            break

        for post in posts:
            details = post.xpath(".//div")[0].xpath(".//div[@class='details']")[0]

            details = post.xpath(".//div")[0].xpath(".//div[@class='details']")[0]

            id = details.xpath(".//span[@class='float-right']/text()")[0]
            id = id[id.find("№") + 1:]

            title = details.xpath(".//h4/text()")[0]

            contract = details.xpath(".//*[@class='list-inline-item']/text()")[0]

            address = details.xpath(".//*[@class='address']/text()")[0]

            if id not in objects:
                link = details.xpath(".//a[@class='fp_price']/@href")
                advert_type: str = "продажа"
                if source == "source_sale.txt":
                    advert_type = "продажа"
                else:
                    advert_type = "аренда"
                data.append(Hata(id, title, link, contract, address, advert_type))
                file.write(f"{id}\n")
            else:
                status = True
                break

        i += 1

    if len(data) != 0:
        get_chars(data)

    # for hata in data:
    #     print(f"\n\nhata from get_first_n_personal with {source}\t", f"{hata.id} {hata.title} {hata.address} {hata.contract} {hata.price} {hata.pics} {hata.material} {hata.lift} {hata.floor} {hata.type} {hata.year} {hata.balcony} {hata.advert_type}\n\n")

    file.close()
    return data


def find_new() -> list[Hata]:
    sale = find_new_personal("source_sale.txt", "https://proestate.24sn.ru/catalog/?address=&contract=sale&category=all&price_min=&price_max=&currency=RUB")
    rent = find_new_personal("source_rent.txt", "https://proestate.24sn.ru/catalog/?address=&contract=rent&category=all&mortgage=N&price_min=&price_max=&currency=RUB")
    sale.reverse()
    rent.reverse()
    return [item for pair in zip_longest(sale, rent) for item in pair if item is not None]
