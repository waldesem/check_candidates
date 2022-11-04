import csv
import sqlite3
import urllib.request

from bs4 import BeautifulSoup as bs
import requests

from database_app import response_db

# константы - местонахождение БД и для скачивания файлов
PATH = '/home/semenenko/Загрузки/'
DB = '/home/semenenko/MyProjects/Python/Staff_check/DB_check/resourses.db'

# скачивание файла из интернета
def download_file(url, file):
    urllib.request.urlretrieve(url, filename=file)

# обновление списка дисквалифицированных с сайта ФНС
url = 'https://www.nalog.gov.ru/opendata/7707329152-registerdisqualified/'
# получаем страницу
page = requests.get(url)
soup = bs(page.text, "html.parser")
# ищем таблицу
items = soup.find('table', class_='border_table')
# выбираем гиперссылки по маске, берем первую
for a in items.find_all('a', href=True):
    if 'registerdisqualified' in str(a):
        # адрес списка дисквалифицированных лиц
        url_disqual = ''.join(a['href'])
        break

# создаем адрес ссылку на диске для списка дисквалифицированных лиц
file_disquial = f"{PATH}disqual.csv"

# запрос файла со списком дисквалифицированных лиц
disqual_upd = download_file(url_disqual, file_disquial)

# удаляем таблицу из БД, если она есть
response_db(DB, query = "DROP TABLE IF EXISTS disqual")

# открываем загруженный файл, создаем таблицу с полями на основе заголовков
with open(file_disquial,'r') as f: 
    reader = csv.reader(f)
    columns = next(reader)
    # создаем заголовки полей
    column = ', '.join(''.join(columns).split(';'))
    # созадем таблицу
    response_db(DB, query = f"CREATE TABLE disqual ({column})")
    # всавляем данные в таблицу
    query = 'INSERT INTO disqual({0}) values ({1})'
    query = query.format(column, ', '.join('?' * len(''.join(columns).split(';'))))
    with sqlite3.connect(DB) as con:
        cursor = con.cursor()
        for data in reader:
            cursor.execute(query, ''.join(data).split(';'))
        con.commit()
    