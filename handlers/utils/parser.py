from selenium import webdriver
from selenium.webdriver.common.by import By
import os


class Hata:
    '''
    Класс представления данных
    '''
    id: str # id объявления
    title: str # название
    link: str # ссылка
    price: str # цена
    material: str # контент
    lift: str # лифт
    floor: str # этаж
    type: str # тип недвижимости
    year: str # год постройки
    balcony: str # балкон
    pics: list[str] # картинки

    def __init__(self, id, utitle, ulink):
        self.id = id
        self.title = utitle
        self.link = ulink


def get_chars(driver: webdriver.Chrome(), hatas: list[Hata]):
    for hata in hatas:
        driver.get(hata.link)

        try:
            price = driver.find_element(By.XPATH,
                                        "/html/body/div[1]/section[1]/div/div[1]/div[2]/div/div[1]/h2").text
        except:
            price = 0

        characteristics = driver.find_element(By.XPATH,
                                              "/html/body/div[1]/section[2]/div/div/div[1]/div/div[2]/div/div")

        try:
            pic_cols = (driver.find_element(By.CSS_SELECTOR,
                                            "#mm-0 > section.listing-title-area.pt-lg-5.pb-lg-5 > "
                                            "div > div:nth-child(2)").find_elements(By.TAG_NAME, "div"))

            pics = [pic_cols[0].find_element(By.TAG_NAME, "a").get_attribute("href")]

            pic_col2 = driver.find_element(By.CSS_SELECTOR,
                                           "#mm-0 > section.listing-title-area.pt-lg-5.pb-lg-5 "
                                           "> div > div:nth-child(2) > div.col-12.col-sm-5.col-lg-4 "
                                           "> div").find_elements(By.CLASS_NAME, "col-6")

            if len(pic_col2) == 6:
                pic_col2 = pic_col2[:-1]

            for i in range(len(pic_col2)):
                pics.append(pic_col2[i].find_element(By.CLASS_NAME, "popup-img").get_attribute("href"))
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


def find_char(table, char) -> str:
    cols = table.find_elements(By.TAG_NAME, "div")
    for col in cols:
        names = col.find_elements(By.TAG_NAME, "ul")[0].find_elements(By.TAG_NAME, "li")
        values = col.find_elements(By.TAG_NAME, "ul")[1].find_elements(By.TAG_NAME, "li")

        for i, li in enumerate(names):
            if li.text == char:
                return values[i].text

    return "Не указано"


def get_first_n(n: int, source: str):

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    driver=webdriver.Chrome(options=options)
    # driver=webdriver.Chrome()

    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, source)

    with open(file_path, "r+") as file:
        objects = file.read().split(",")

        status = False
        data = []
        i = 1
        count = 0

        while not status:
            driver.get(f"https://proestate.24sn.ru/catalog/sale/all/?p={i}")

            arr = driver.find_element(By.CSS_SELECTOR, "#catalog-property > div > div > div.col-md-12.col-lg-8 > div")
            posts = arr.find_elements(By.CLASS_NAME, "col-lg-12")[:-1]
            if len(posts) == 0:
                break

            for post in posts:
                details = post.find_element(By.TAG_NAME, "div").find_element(By.CLASS_NAME, "details")

                id = details.find_element(By.CLASS_NAME, "float-right").text
                id = id[id.find("№") + 1:]
                title = details.find_element(By.TAG_NAME, "h4").text

                if id not in objects:
                    link = details.find_element(By.CLASS_NAME, "fp_price").get_attribute("href")
                    data.append(Hata(id, title, link))
                    file.write(f"{id}\n")

                count += 1

                if count == n:
                    status = True
                    break

            i += 1

        if len(data) != 0:
            get_chars(driver, data)

        return data


def find_new(source: str) -> list[Hata]:
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    driver=webdriver.Chrome(options=options)
    # driver=webdriver.Chrome()

    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, source)

    with open(file_path, "r+") as file:
        objects = file.read().split("\n")

        data = []
        status = False
        i = 1

        while not status:
            driver.get(f"https://proestate.24sn.ru/catalog/sale/all/?p={i}")

            arr = driver.find_element(By.CSS_SELECTOR, "#catalog-property > div > div > div.col-md-12.col-lg-8 > div")
            posts = arr.find_elements(By.CLASS_NAME, "col-lg-12")[:-1]
            if len(posts) == 0:
                break

            for post in posts:
                details = post.find_element(By.TAG_NAME, "div").find_element(By.CLASS_NAME, "details")

                id = details.find_element(By.CLASS_NAME, "float-right").text
                id = id[id.find("№")+1:]
                title = details.find_element(By.TAG_NAME, "h4").text

                if id not in objects:
                    link = details.find_element(By.CLASS_NAME, "fp_price").get_attribute("href")
                    data.append(Hata(id, title, link))
                    file.write(f"{id}\n")
                else:
                    status = True

            i += 1

        if len(data) != 0:
            get_chars(driver, data)

        return data
