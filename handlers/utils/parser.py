import os
import requests
from lxml import html


class Hata:  # Класс представления данных
    id: str
    title: str
    link: str
    price: str
    material: str
    lift: str
    floor: str
    type: str
    year: str
    balcony: str
    pics: list[str]

    def __init__(self, id, utitle, ulink):  # Конструктор
        self.id = id
        self.title = utitle
        self.link = ulink

def find_char(table, char) -> str: # Функция поиска конкретной харакетристики
    cols = table.xpath(".//div")
    for col in cols:
        names = col.xpath(".//ul[@class='list-inline-item w135p']")[0].xpath(".//li")
        values = col.xpath(".//ul[@class='list-inline-item']")[0].xpath(".//li")

        for i, li in enumerate(names):
            if li.xpath(".//text()")[0] == char:
                return values[i].xpath(".//text()")[0]

    return "Не указано"

def get_chars(hatas: list[Hata]): # Функция задания всех характеристик объекту
    for hata in hatas:
        r = requests.get(f"https://proestate.24sn.ru{hata.link[0]}")

        # if r.status_code != 200:
        #     print(r.status_code)

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
        hata.material = find_char(characteristics, "Материал дома :")
        hata.lift = find_char(characteristics, "Лифт :")
        hata.floor = find_char(characteristics, "Этаж :")
        hata.type = find_char(characteristics, "Тип :")
        hata.year = find_char(characteristics, "Год постройки :")
        hata.balcony = find_char(characteristics, "Балкон :")

def get_first_n(n: int, source: str) -> list[Hata]: # Получение первых n объектов

    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, source)

    file = open(file_path, "r+")
    objects = file.read().split("\n")

    data = []
    status = False
    i = 1
    count = 0

    while not status:
        url = f"https://proestate.24sn.ru/catalog/sale/all/?p={i}"
        r = requests.get(url)

        # if r.status_code != 200:
        #     print(r.status_code)

        tree = html.fromstring(r.text)
        arr = tree.xpath("//*[@id='catalog-property']/div/div/div[2]/div")[0]
        posts = arr.xpath(".//div[@class='col-lg-12']")

        if len(posts) == 0:
            break

        for post in posts:
            details = post.xpath(".//div")[0].xpath(".//div[@class='details']")[0]

            id = details.xpath(".//span[@class='float-right']/text()")[0]
            id = id[id.find("№") + 1:]

            title = details.xpath(".//h4/text()")[0]

            if id not in objects:
                link = details.xpath(".//a[@class='fp_price']/@href")
                data.append(Hata(id, title, link))
                file.write(f"{id}\n")

            count += 1

            if count == n:
                status = True
                break

        i += 1

    if len(data) != 0:
        get_chars(data)

    # for hata in data:
    #     print(f"{hata.id} {hata.title} {hata.price} {hata.pics} {hata.material} {hata.lift} {hata.floor} {hata.type} {hata.year} {hata.balcony}")

    file.close()
    return data


def find_new(source: str) -> list[Hata]: # Поиск новых объектов
    
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, source)

    file = open(file_path, "r+")
    objects = file.read().split("\n")

    data = []
    status = False
    i = 1

    while not status:
        url = f"https://proestate.24sn.ru/catalog/sale/all/?p={i}"
        r = requests.get(url)

        # if r.status_code != 200:
        #     print(r.status_code)

        tree = html.fromstring(r.text)
        arr = tree.xpath("//*[@id='catalog-property']/div/div/div[2]/div")[0]
        posts = arr.xpath(".//div[@class='col-lg-12']")

        if len(posts) == 0:
            break

        for post in posts:
            details = post.xpath(".//div")[0].xpath(".//div[@class='details']")[0]

            id = details.xpath(".//span[@class='float-right']/text()")[0]
            id = id[id.find("№") + 1:]

            title = details.xpath(".//h4/text()")[0]

            if id not in objects:
                link = details.xpath(".//a[@class='fp_price']/@href")
                data.append(Hata(id, title, link))
                file.write(f"{id}\n")
            else:
                status = True
                break

        i += 1

    if len(data) != 0:
        get_chars(data)

    # for hata in data:
    #     print(f"{hata.id} {hata.title} {hata.price} {hata.pics} {hata.material} {hata.lift} {hata.floor} {hata.type} {hata.year} {hata.balcony}")

    file.close()
    return data