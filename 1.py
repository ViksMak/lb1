from bs4 import BeautifulSoup  # импортируем библиотеку BeautifulSoup
import openpyxl  # Импортируем библиотеку openpyxl для работы с Excel
from selenium import webdriver  # Импортируем библиотеку Selenium для автоматизации браузера
import time


def parse():
    url = 'https://novosibirsk.cian.ru/recommendations/'  # передаем необходимый URL адрес
    driver = webdriver.Firefox()  # Инициализируем браузер Firefox через Selenium
    driver.get(url)  # Открываем страницу с помощью Selenium
    time.sleep(5)  # Делаем задержку, чтобы страница загрузилась полностью
    page = driver.page_source  # Получаем исходный код страницы

    soup = BeautifulSoup(page, "html.parser")  # передаем страницу в bs4

    block = soup.select('div._4d935d0799--price--hSzzN')  # находим контейнер с нужным классом
    descriptions = []
    for data in block:  # проходим циклом по содержимому контейнера
        if data.find('span'):  # находим тег
            description = data.text  # записываем в переменную содержание тега
            descriptions.append(description)  # Добавляем описание в список

    driver.quit()  # Закрываем браузер
    return descriptions


if __name__ == '__main__':
    descriptions = parse()
    print(descriptions)


    # Записываем данные в Excel
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet['A1'] = 'Description'
    for idx, description in enumerate(descriptions, start=2):
        cell = sheet.cell(row=idx, column=1)
        cell.value = description
    wb.save('descriptions.xlsx')
