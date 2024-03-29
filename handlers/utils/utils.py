import re


# # проверка номера телефона
# def check_phone_number(phone_number: str) -> bool:
#     pattern = r'^\+\d{1,2}\(\d{3}\)\d{3}-\d{2}-\d{2}$'
#     match = re.match(pattern, phone_number)
#     if match:
#         return True
#     return False


# проверка номера телефона
def check_phone_number(phone_number: str) -> bool:
    pattern = r'^\+\d{11}$' # +78881114433
    match = re.match(pattern, phone_number)
    if match:
        return True
    return False


# создание поста-заявки
def create_post(fio: str, phone: str, type: str, locate: str, comment: str) -> str:
    res: str = f"<u><b>Заявка на консультацию</b></u>" + \
            f"\n\nКлиент: {fio}\nНомер телефона: {phone}" + \
            f"\nИнтересующая категория недвижимости: {type}" + \
            f"\nИнтересующий район: {locate}"
    
    if comment != "Нет":
        res = res + f"\nПримечание от клиента: {comment}\n\n"

    return res