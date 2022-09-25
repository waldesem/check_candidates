import httpx
import datetime as dt
import requests
import openpyxl
import menu_upload
import csv
import sqlite3

def check():
    ### проверка по списку самозанятых
    def check_npd_status(inn: str, req_date: dt.date = None) -> dict:
        req_date = dt.date.today().isoformat()
        url = "https://statusnpd.nalog.ru/api/v1/tracker/taxpayer_status"
        data = {
            "inn": inn,
            "requestDate": req_date,
        }
        resp = httpx.post(url=url, json=data)
        return resp.json()

    ### проверка инн
    def suggest(surname: str, name: str, patronymic: str, birthdate: str, 
                doctype: str, docnumber: str, docdate: str) -> dict:
        url = "https://service.nalog.ru/inn-proc.do"
        data = {
            "fam": surname,
            "nam": name,
            "otch": patronymic,
            "bdate": birthdate,
            "bplace": "",
            "doctype": doctype,
            "docno": docnumber,
            "docdt": docdate,
            "c": "innMy",
            "captcha": "",
            "captchaToken": "",
        }
        resp = requests.post(url=url, data=data)
        resp.raise_for_status()
        return resp.json()

    ### проверка по списку кандидатов
    def candidates():
        #file = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Кандидаты\Кандидаты.xlsm'
        file = r'/home/semenenko/MyProjects/Python/Staff_check/DB_check/Кандидаты.xlsm'
        wb = openpyxl.load_workbook(file, read_only=True, data_only=True)
        ws = wb.worksheets[0]
        col_range = ws['B1':'B30000']
        flag = False
        for cell in col_range:
            for c in cell:
                if str(c.value).strip() == menu_upload.lst_ank[2].strip():
                    row_num = c.row
                    birtday = ws['C'+str(row_num)].value
                    birtday = dt.datetime.strftime(birtday, '%d.%m.%Y')
                    if birtday == menu_upload.lst_ank[4]:
                        response_candidates = 'Найдены полные совпадения в списке Кандидатов по ФИО и дате рождения'
                        flag = True
                        break
                    else:
                        continue
                else:
                    response_candidates = 'Не найдены совпадения в списке Кандидатов (возможно только совпадение по ФИО)'
            if flag:
                break
        wb.close()
        return response_candidates
    #проверка по списку дисквалифицировнных
    def disqualed():
        #file = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Кандидаты\Кандидаты.xlsm'
        file_csv = r'/home/semenenko/MyProjects/Python/Staff_check/DB_check/data-18092022-structure-24062015.csv'
        search_for = str(menu_upload.lst_ank[2])+';'+str(menu_upload.lst_ank[3])
        with open(file_csv) as fc:
            reader = csv.reader(fc)
            for line in reader:
                if search_for in line:
                    response_disqual = 'Найден в списке дисквалифицированных лиц'
                else:
                    response_disqual = 'Отсутствует в списке дисквалифицированных лиц'
        return response_disqual
    #проверка по списку паспортов в БД
    def passport():
        try:
            sqlite_connection = sqlite3.connect('/home/semenenko/Загрузки/passportDB.db')
            cursor_obj = sqlite_connection.cursor()
            cursor_obj.execute('SELECT * FROM list_of_expired_passports WHERE PASSP_SERIES = '+str(menu_upload.lst_ank[7])+' and PASSP_NUMBER = '+str(menu_upload.lst_ank[8]))
            record = cursor_obj.fetchall()
            if len(record) != 0:
                passport_response = "Найден в списке недействительных паспортов"
            else:
                passport_response = 'В списке недействительных паспортов не найден'
            cursor_obj.close()
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()
        return passport_response
    
    #собираем проверенные данные
    global response_check
    response_check = []
    #проверка самозанятого
    npd_response = check_npd_status(menu_upload.lst_ank[11])
    response_check.append(npd_response.get('message'))
    #проверка инн
    document = {'passport_foreign' : 10, 'residence_permit' : 12, 'passport_russia' : 21}
    inn_response = suggest(
        surname=menu_upload.lst_ank[2].split()[0],
        name=menu_upload.lst_ank[2].split()[1],
        patronymic=menu_upload.lst_ank[2].split()[2],
        birthdate=menu_upload.lst_ank[4],
        doctype=document.get('passport_russia'),
        docnumber=menu_upload.lst_ank[7][:2]+' '+menu_upload.lst_ank[7][2:]+' '+menu_upload.lst_ank[8],
        docdate=menu_upload.lst_ank[9],
    )
    response_check.append(inn_response.get('inn'))
    #проверка по списку Кандидатов
    candidates_response = candidates()
    response_check.append(candidates_response)
    #проверка по списку Кандидатов
    response_disqual = disqualed()
    response_check.append(response_disqual)
    #проверка по списку паспортов
    passport_response = passport()
    response_check.append(passport_response)
    return response_check
