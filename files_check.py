from tkinter import filedialog, messagebox
from datetime import date
import check_info
import openpyxl
import getpass
import os


def upload():
    file = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx .xlsm")])
    wb = openpyxl.load_workbook(file, data_only=True)
    ws = wb.worksheets[0]
    global anketa_values
    anketa_values = [ws['C3'].value, ws['D3'].value, ws['K3'].value, ws['S3'].value,
               ws['L3'].value, ws['M3'].value, ws['T3'].value, ws['P3'].value,
               ws['Q3'].value, ws['R3'].value, ws['U3'].value, ws['V3'].value,
               ws['N3'].value, ws['O3'].value, ws['Y3'].value, ws['Z3'].value,
               ws['X3'].value, ws['AA3'].value, ws['AB3'].value, ws['AA4'].value,
               ws['AB4'].value, ws['AA5'].value, ws['AB5'].value]
    wb.close()

    os.makedirs('/home/semenenko/MyProjects/' + anketa_values[2], exist_ok=True)
    wb.save('/home/semenenko/MyProjects/' + anketa_values[2] + '/' + 'Анкета ' +
            anketa_values[2] + '-' + anketa_values[4] + '.xlsx')

    return anketa_values

def download_file():
    wb = openpyxl.load_workbook(r'/home/semenenko/MyProjects/Python/Staff_check/DB_check/Заключение.xlsm')
    ws = wb['Заключение']
    # анкетные данные
    ws['C4'] = anketa_values[0]
    ws['C5'] = anketa_values[1]
    ws['C6'] = anketa_values[2]
    ws['C7'] = anketa_values[4]
    # 'Результаты проверки по местам работы'
    ws['A9'] = anketa_values[-6]
    ws['C9'] = anketa_values[-5]
    ws['A10'] = anketa_values[-4]
    ws['C10'] = anketa_values[-3]
    ws['A11'] = anketa_values[-2]
    ws['C11'] = anketa_values[-1]
    # проверка паспорт
    ws['C13'] = check_info.response_check[4]
    # 'Проверка статуса самозанятого'
    ws['C14'] = check_info.response_check[0]
    # 'Проверка ИНН'
    ws['C15'] = check_info.response_check[1]
    # 'Проверка по списку кандидатов'
    ws['C21'] = check_info.response_check[2]
    # 'Проверка по списку дисквалифицированных лиц'
    ws['C20'] = check_info.response_check[3]
    # 'Дата проверки'
    ws['C26'] = date.today().strftime('%d.%m.%Y')
    # имя пользователя
    ws['C27'] = getpass.getuser()

    # создаем папку и сохраняем файл с новым именем
    #os.makedirs('/home/semenenko/MyProjects/' + anketa_values[2], exist_ok=True)
    wb.save('/home/semenenko/MyProjects/' + anketa_values[2] + '/' + 'Заключение ' +
            anketa_values[2] + '-' + anketa_values[4] + '.xlsx')
    
    #db_add()

    messagebox.showinfo(title="Результат проверки", message="Создана папка c файлами проверки. Добавлена запись в БД")
