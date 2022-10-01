from datetime import date
from tkinter import messagebox as mb
import openpyxl
import os
import menu_upload
import check_main
import getpass


# today_date = date.today().strftime('%d.%m.%Y')
def download_file():
    wb = openpyxl.load_workbook(r'/home/semenenko/MyProjects/Python/Staff_check/DB_check/Заключение.xlsm')
    ws = wb['Заключение']
    # анкетные данные
    ws['C4'] = menu_upload.lst_ank[0]
    ws['C5'] = menu_upload.lst_ank[1]
    ws['C6'] = menu_upload.lst_ank[2]
    ws['C7'] = menu_upload.lst_ank[4]
    # 'Результаты проверки по местам работы'
    ws['A9'] = menu_upload.lst_ank[-6]
    ws['C9'] = menu_upload.lst_ank[-5]
    ws['A10'] = menu_upload.lst_ank[-4]
    ws['C10'] = menu_upload.lst_ank[-3]
    ws['A11'] = menu_upload.lst_ank[-2]
    ws['C11'] = menu_upload.lst_ank[-1]
    # проверка паспорт
    ws['C13'] = check_main.response_check[4]
    # 'Проверка статуса самозанятого'
    ws['C14'] = check_main.response_check[0]
    # 'Проверка ИНН'
    ws['C15'] = check_main.response_check[1]
    # 'Проверка по списку кандидатов'
    ws['C21'] = check_main.response_check[2]
    # 'Проверка по списку дисквалифицированных лиц'
    ws['C20'] = check_main.response_check[3]
    # 'Дата проверки'
    ws['C26'] = date.today().strftime('%d.%m.%Y')
    # имя пользователя
    ws['C27'] = getpass.getuser()

    # создаем папку и сохраняем файл с новым именем
    os.makedirs('/home/semenenko/MyProjects/' + menu_upload.lst_ank[2], exist_ok=True)
    wb.save('/home/semenenko/MyProjects/' + menu_upload.lst_ank[2] + '/' + 'Заключение ' +
            menu_upload.lst_ank[2] + '-' + menu_upload.lst_ank[4] + '.xlsx')
    mb.showinfo(title="Результат проверки", message="Создана целевая папка и файл заключения")
