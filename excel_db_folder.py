import os.path
import sqlite3
import shutil
from datetime import date

from database_app import CONNECT

#сегодняшняя дата
DATE_TODAY = date.today().strftime('%Y-%m-%d') + ' 00:00:00'
#главный файл кандидатов
MAIN_FILE = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Кандидаты\Кандидаты.xlsm'
#рабочая папка кандидатов
OUT_FILE = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Кандидаты\\'
#место хранения отработанных кандидатов
DEST_DIR = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-2\\'

# функция для записи в БД
def response_db(db, query):
    try:
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(query)
            record_db = cur.fetchall()
    except sqlite3.Error as error:
        print('Ошибка', error)       
    return record_db

# создаем пустой список
columns = []

print('Начинаем работу... Создаем резервную копию книги Exel в', DEST_DIR)
shutil.copy(MAIN_FILE, DEST_DIR)

print('Открываем книгу по адресу:', MAIN_FILE, 'для чтения и записи данных')
wb = openpyxl.load_workbook(MAIN_FILE, keep_vba=True)
#Берем первый лист
ws = wb.worksheets[0]
print('Идет поиск ячеек с датами согласования сегодня') #(огранbчение 30 тыс. строк)
col_range = ws['K1':'K30000']
for cell in col_range:
    for c in cell:
        #если запись в ячейке равна сегодняшней дате
        if str(c.value) == DATE_TODAY:
            print('Найдены записи с сегодняшней датой', DATE_TODAY)
            #берем номер строки
            row_num = c.row
            #берем значение из ячейки фамилия, которое советствууюет номеру строки дата
            fio = ws['B'+str(row_num)].value
            fio = ws['B'+str(row_num)].value
            birthday = ws['C'+str(row_num)].value
            staff = ws['D'+str(row_num)].value
            checks = ws['E'+str(row_num)].value
            recruter = ws['F'+str(row_num)].value
            date_in = ws['G'+str(row_num)].value
            officer = ws['H'+str(row_num)].value
            date_out = ws['I'+str(row_num)].value
            result = ws['J'+str(row_num)].value
            fin_date = ws['K'+str(row_num)].value
            url = ws['L'+str(row_num)].value
            print('Получены анкетные данные кандидата:', fio)
            #Перебираем каталоги в исходной папке
            for dirs, subdirs, files in os.walk(OUT_FILE):
                for subdir in subdirs:
                    #если имя папки такое же как и значение в ячейке фамилия
                    if subdir.lower().rstrip() == fio.lower().rstrip():
                        print('Найдена папка,', subdir, 'которая соответствует ФИО кандидата')
                        #разбираем посимвольно имя папки
                        letter = [i for i in fio]
                        #создаем ссылку для целевой деректории с первым именем буквы по алфавиту, добавляем к имени уникальный ID
                        hlink = DEST_DIR+'\\'+letter[0]+'\\'+subdir+' - '+str(ws['A'+str(row_num)].value)
                        print('Создана гиперссылка:', hlink)
                        #переносим папку из исходной в целевую папку
                        shutil.move(OUT_FILE+subdir, hlink)
                        #добавляем в файл книги гиперссылку, куда помещена папка
                        ws['L'+str(row_num)].hyperlink = hlink
                    else:
                        continue
            columns.extend(fio, birthday, staff, checks, recruter, date_in, officer, date_out, result, fin_date, url)
            # передаем данные в БД
            query = (f"INSERT INTO reestr ('fio, birthday, staff, checks, recruter, date_in, officer, date_out, result, fin_date, url') VALUES ({columns})")
            resp = response_db(CONNECT, query)
            if len(resp):
                print('Error') 
            else:
                print('OK')
        else:
            continue                
print('Cохраняем книгу Excel')
wb.save(MAIN_FILE)
