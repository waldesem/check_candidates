import openpyxl
from datetime import date
import os
from tkinter import messagebox as mb
import menu_upload
import check_main

today_date = date.today().strftime('%d.%m.%Y')
def download_file():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.merge_cells('A1:C1')
    ws['A1'] = 'Заключение'
    ws.merge_cells('A2:C2')
    ws['A2'] = 'о проверке кандидата'
    ws['A4'] = 'Должность'
    ws.merge_cells('B4:C4')
    ws['B4'] = menu_upload.lst_ank[0]
    ws['A5'] = 'Подразделение'
    ws.merge_cells('B5:C5')
    ws['B5'] = menu_upload.lst_ank[1]
    ws['A6'] = 'Фамилия Имя Отчество'
    ws.merge_cells('B6:C6')
    ws['B6'] = menu_upload.lst_ank[2]
    ws['A7'] = 'Дата рождения'
    ws.merge_cells('B7:C7')
    ws['B7'] = menu_upload.lst_ank[4]
    ws.merge_cells('A8:C8')
    ws['A8'] = 'Результаты проверки по местам работы'
    ws['A9'] = menu_upload.lst_ank[-5]
    ws['B9'] = menu_upload.lst_ank[-6]   
    ws['A10'] = menu_upload.lst_ank[-3]
    ws['B10'] = menu_upload.lst_ank[-4]
    ws['A11'] = menu_upload.lst_ank[-1]
    ws['B11'] = menu_upload.lst_ank[-2]
    ws.merge_cells('A12:C12')
    ws['A12'] = 'Результаты проверки по информационным системам'
    ws['A13'] = 'Проверка статуса самозанятого'
    ws.merge_cells('B13:C13')
    ws['B13'] = check_main.response_check[0]
    ws['A14'] = 'Проверка ИНН'
    ws.merge_cells('B14:C14')
    ws['B14'] = check_main.response_check[1]
    ws['A15'] = 'Проверка по списку кандидатов'
    ws.merge_cells('B15:C15')
    ws['B15'] = check_main.response_check[2]
    ws['A16'] = 'Проверка по списку дисквалифицированных лиц'
    ws.merge_cells('B16:C16')
    ws['B16'] = check_main.response_check[3]
    #
    ws['A20'] = 'Дата проверки'
    ws.merge_cells('B20:C20')
    ws['B20'] = today_date 
    os.makedirs('/home/semenenko/MyProjects/'+menu_upload.lst_ank[2], exist_ok=True)
    wb.save('/home/semenenko/MyProjects/'+menu_upload.lst_ank[2]+'/'+'Заключение '+
            menu_upload.lst_ank[2]+'.xlsx')
    mb.showinfo(title="Результат проверки", message="Создана целевая папка и файл заключения")